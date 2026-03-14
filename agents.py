import os, json, re, logging, datetime
from groq import Groq
from github import Github, Auth
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(filename='audit.log', level=logging.INFO)

client = Groq(api_key=os.getenv("GROQ_API_KEY"))
gh = Github(auth=Auth.Token(os.getenv("GITHUB_TOKEN")))

# ── Secret masking ──
def mask_secrets(code):
    for p in [r'(password\s*=\s*)["\'].*?["\']', r'(secret\s*=\s*)["\'].*?["\']',
              r'(api_key\s*=\s*)["\'].*?["\']', r'(token\s*=\s*)["\'].*?["\']']:
        code = re.sub(p, r'\1"[HIDDEN]"', code, flags=re.IGNORECASE)
    return code

# ── AI caller ──
def ask_ai(system, code):
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": "Analyze this code:\n\n" + mask_secrets(code)}
        ],
        temperature=0.2
    )
    return r.choices[0].message.content

# ── Safe JSON parser ──
def safe_parse(raw):
    try:
        m = re.search(r'\{.*\}', raw, re.DOTALL)
        if m:
            return json.loads(m.group())
    except:
        pass
    return {"score": 0, "tip": "Could not parse response.", "issues": [],
            "bugs": [], "vulnerabilities": [], "missing": [], "good": [],
            "severity": "UNKNOWN", "risk": "UNKNOWN", "rating": "UNKNOWN"}

# ── Agent prompts ──
CR_PROMPT = """You are a senior code reviewer. Return ONLY valid JSON:
{"score":7,"issues":[{"severity":"HIGH","title":"Short title","description":"One sentence.","fix":"corrected code here","comment":"# comment to add"}],"good":["Good thing"],"tip":"One tip."}
Rules: score 0-10. severity: CRITICAL HIGH MEDIUM LOW. Return ONLY JSON."""

SEC_PROMPT = """You are a cybersecurity expert. Return ONLY valid JSON:
{"score":6,"severity":"HIGH","vulnerabilities":[{"severity":"CRITICAL","title":"SQL Injection","description":"One sentence.","fix":"secure code here","comment":"# security comment"}],"tip":"One fix."}
Rules: score 0-10. Return ONLY JSON."""

BUG_PROMPT = """You are a bug detection expert. Return ONLY valid JSON:
{"score":5,"risk":"HIGH","bugs":[{"severity":"HIGH","title":"Bug title","description":"One sentence.","fix":"fixed code here","comment":"# fix comment"}],"tip":"One tip."}
Rules: score 0-10. risk: HIGH MEDIUM LOW. Return ONLY JSON."""

DOC_PROMPT = """You are a documentation expert. Return ONLY valid JSON:
{"score":3,"missing":[{"severity":"HIGH","title":"Missing docstring","description":"One sentence.","fix":"\"\"\"Add docstring here.\"\"\"","comment":"# Add comment here"}],"good":["Good practice"],"tip":"One tip."}
Rules: score 0-10. Return ONLY JSON."""

PERF_PROMPT = """You are a performance optimization expert. Return ONLY valid JSON:
{"score":6,"rating":"SLOW","issues":[{"severity":"HIGH","title":"Performance issue","description":"One sentence.","fix":"optimized code here","comment":"# performance comment"}],"tip":"One tip."}
Rules: score 0-10. rating: FAST MODERATE SLOW. Return ONLY JSON."""

DEPLOY_PROMPT = """You are a DevOps deployment expert. Return ONLY valid JSON:
{"verdict":"DO NOT DEPLOY","risk_level":"HIGH","score":3,"blockers":["Critical issue 1","Critical issue 2"],"warnings":["Warning 1"],"safe_to_deploy":false,"message":"Fix critical issues before deploying."}
Rules: verdict is SAFE TO DEPLOY or DEPLOY WITH CAUTION or DO NOT DEPLOY. risk_level: LOW MEDIUM HIGH CRITICAL. safe_to_deploy: true or false. Return ONLY JSON."""

AUTO_FIX_PROMPT = """You are an expert programmer. Rewrite the ENTIRE code with ALL issues fixed. Return ONLY valid JSON:
{"fixed_code":"entire corrected code here","changes":["Fixed SQL injection","Removed hardcoded key","Added error handling"],"summary":"One sentence of what was fixed."}
Return ONLY JSON. No extra text."""

# ── Individual agents ──
def code_review_agent(code):
    return safe_parse(ask_ai(CR_PROMPT, code))

def security_agent(code):
    return safe_parse(ask_ai(SEC_PROMPT, code))

def bug_detection_agent(code):
    return safe_parse(ask_ai(BUG_PROMPT, code))

def docs_agent(code):
    return safe_parse(ask_ai(DOC_PROMPT, code))

def performance_agent(code):
    return safe_parse(ask_ai(PERF_PROMPT, code))

def deploy_agent(code):
    return safe_parse(ask_ai(DEPLOY_PROMPT, code))

def auto_fix_agent(code):
    return safe_parse(ask_ai(AUTO_FIX_PROMPT, code))

# ── Main analyze function ──
def analyze_code(code, filename="code"):
    logging.info(f"file={filename} time={datetime.datetime.now()}")
    print(f"Analyzing: {filename}")
    cr     = code_review_agent(code)
    sec    = security_agent(code)
    bug    = bug_detection_agent(code)
    doc    = docs_agent(code)
    perf   = performance_agent(code)
    deploy = deploy_agent(code)
    fix    = auto_fix_agent(code)
    overall = round((
        cr.get('score',0) + sec.get('score',0) +
        bug.get('score',0) + doc.get('score',0) +
        perf.get('score',0)
    ) / 5, 1)
    return {
        "filename": filename,
        "overall": overall,
         "timestamp": datetime.datetime.now().strftime("%d %b %Y — %I:%M %p"),
        "code_review": cr,
        "security": sec,
        "bug_detection": bug,
        "docs": doc,
        "performance": perf,
        "deploy": deploy,
        "auto_fix": fix
    }

# ── GitHub PR analysis ──
def analyze_github_pr(repo_name, pr_number):
    try:
        repo = gh.get_repo(repo_name)
        pr = repo.get_pull(int(pr_number))
        results = []
        for f in pr.get_files():
            print(f"Found file: {f.filename}")
            if f.patch:
                results.append(analyze_code(f.patch[:3000], f.filename))
        print(f"Total files analyzed: {len(results)}")
        return results
    except Exception as e:
        print(f"PR error: {e}")
        return []

# ── GitHub Repo analysis ──
def analyze_github_repo(repo_url):
    try:
        url = repo_url.strip().rstrip('/')
        if 'github.com' in url:
            parts = url.split('github.com/')[-1].split('/')
        else:
            parts = url.split('/')
        repo_name = parts[0] + '/' + parts[1]
        repo = gh.get_repo(repo_name)
        results = []
        files_checked = 0
        contents = list(repo.get_contents(""))
        while contents and files_checked < 5:
            fc = contents.pop(0)
            if fc.type == "dir":
                try:
                    contents.extend(repo.get_contents(fc.path))
                except:
                    pass
            elif fc.name.endswith(('.py','.js','.ts','.java','.css','.html','.rb','.cpp','.c')):
                try:
                    code = fc.decoded_content.decode('utf-8')
                    results.append(analyze_code(code[:3000], fc.path))
                    files_checked += 1
                except:
                    pass
        return results
    except Exception as e:
        print(f"Repo error: {e}")
        return []

if __name__ == "__main__":
    sample = """
def login(user, pwd):
    import sqlite3
    db = sqlite3.connect('app.db')
    q = "SELECT * FROM users WHERE user='"+user+"' AND pwd='"+pwd+"'"
    db.execute(q)
API_KEY = "sk-secret-12345"
x = 100 / 0
"""
    out = analyze_code(sample, "test.py")
    print(json.dumps(out, indent=2))