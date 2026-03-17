# ⚡ CodeGuard AI — Intelligent Code Review System

<div align="center">

![CodeGuard AI](https://img.shields.io/badge/CodeGuard-AI-00ff8c?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyTDIgN2wxMCA1IDEwLTV6TTIgMTdsNiAzIDQtMiA0IDIgNi0zVjdsLTYgM3YxMGwtNC0yLTQgMlY5TDIgN3oiLz48L3N2Zz4=)
![Groq](https://img.shields.io/badge/Powered%20by-Groq-orange?style=for-the-badge)
![Llama](https://img.shields.io/badge/Model-Llama%203.3%2070B-blue?style=for-the-badge)
![Agents](https://img.shields.io/badge/AI%20Agents-7-purple?style=for-the-badge)
![Storage](https://img.shields.io/badge/Data%20Storage-Zero-green?style=for-the-badge)

**Seven specialized AI agents find bugs, security issues, and quality problems — then fix them automatically.**

[🚀 **Try it live →**](https://codeguard-ai-lovt.onrender.com)

</div>

---

## What is CodeGuard AI?

CodeGuard AI is an intelligent code review system that runs **7 parallel AI agents** on your code simultaneously. Each agent is a specialist — together they catch what a single model would miss.

Built at a hackathon. Powered by **Groq + Llama 3.3 70B**. Zero data stored.

---

## The 7 Agents

| Agent | What it does |
|-------|-------------|
| 📋 **Code Review** | Style, structure, naming conventions, best practices |
| 🔒 **Security** | SQL injection, XSS, hardcoded secrets, OWASP Top 10 |
| 🐛 **Bug Detection** | Null dereferences, off-by-one errors, logic bugs |
| 📚 **Documentation** | Missing docstrings, unclear comments, doc suggestions |
| ⚡ **Performance** | O(n²) loops, memory leaks, redundant DB calls |
| 🚀 **Deploy Check** | Env variables, error handling, production readiness |
| 🔧 **Auto Fix** | Takes findings from all 6 agents and patches your code |

---

## Features

- **3 input modes** — paste code, GitHub PR, or full GitHub repo
- **Visual health dashboard** — radar chart + per-agent score breakdown
- **Auto-fixed code** — copy production-ready corrected code directly
- **Groq-powered speed** — full 7-agent analysis in seconds
- **Zero storage** — your code is never saved or logged
- **Any language** — Python, JS, TS, Go, Rust, Java, C++, and more

---

## Demo

```
$ codeguard analyze ./src/auth.py

  › Loading 7 AI agents...
  ✓ Code Review Agent        — 2 style issues found
  ⚠ Security Agent           — SQL injection risk (HIGH)
  ✓ Bug Detection Agent      — null dereference on line 47
  ✓ Documentation Agent      — missing docstrings (3 functions)
  ⚠ Performance Agent        — O(n²) loop detected
  ✓ Deploy Check Agent       — passed
  ✓ Auto Fix Agent           — 4 issues auto-patched

  Overall health score: 72/100  →  after auto-fix: 94/100
```

---

## Tech Stack

- **Frontend** — HTML, CSS, Vanilla JS
- **Backend** — Python
- **AI** — [Groq API](https://groq.com) with Llama 3.3 70B
- **Deployment** — Render

---

## Getting Started

### Prerequisites

- Python 3.9+
- A [Groq API key](https://console.groq.com)

### Installation

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/codeguard-ai.git
cd codeguard-ai

# Install dependencies
pip install -r requirements.txt

# Set your Groq API key
export GROQ_API_KEY=your_api_key_here

# Run the app
python app.py
```

Then open `http://localhost:5000` in your browser.

### Environment Variables

| Variable | Description |
|----------|-------------|
| `GROQ_API_KEY` | Your Groq API key (required) |
| `GITHUB_TOKEN` | GitHub personal access token (optional, for private repo support) |

---

## Usage

### Paste Code
Copy any code snippet into the editor and click **Analyze Code**.

### GitHub Pull Request
Enter a repo name (e.g. `pallets/flask`) and a PR number to review any public pull request.

### GitHub Repository
Enter a full repo URL (e.g. `https://github.com/pallets/flask`) to scan an entire codebase.

---

## Contributing

Contributions are welcome! Please open an issue first to discuss what you'd like to change.

1. Fork the repo
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

MIT License — see [LICENSE](LICENSE) for details.

---

## Acknowledgements

- Built with ❤️ at a hackathon
- Powered by [Groq](https://groq.com) for ultra-fast inference
- Uses Meta's [Llama 3.3 70B](https://ai.meta.com/llama/) model

---

<div align="center">
  <strong>⭐ Star this repo if CodeGuard helped you ship cleaner code!</strong>
</div>
