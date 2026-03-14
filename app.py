from flask import Flask, request, jsonify, render_template
from agents import analyze_code, analyze_github_pr, analyze_github_repo
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        d = request.get_json()
        result = analyze_code(d.get("code",""), d.get("filename","pasted_code"))
        return jsonify(result)
    except Exception as e:
        print(f"Analyze error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/analyze-pr", methods=["POST"])
def analyze_pr():
    try:
        d = request.get_json()
        results = analyze_github_pr(d.get("repo",""), d.get("pr_number", 1))
        return jsonify({"results": results})
    except Exception as e:
        print(f"PR error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/analyze-repo", methods=["POST"])
def analyze_repo():
    try:
        d = request.get_json()
        results = analyze_github_repo(d.get("url",""))
        return jsonify({"results": results})
    except Exception as e:
        print(f"Repo error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("\n  CodeGuard AI — 7 Agents Running")
    print("  Open: http://localhost:5000\n")
    app.run(debug=True, port=5000)