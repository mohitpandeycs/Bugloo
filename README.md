<p align="center">
  <img src="app/static/favicon.svg" alt="Bugloo Logo" width="84" />
</p>

<h1 align="center">Bugloo</h1>

<p align="center">
  AI-powered code review — paste your code, get instant structured feedback.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.11-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-0.111-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/Supabase-Auth%20%2B%20DB-3ECF8E?style=flat-square&logo=supabase&logoColor=white" />
  <img src="https://img.shields.io/badge/Groq-llama3--70b-F55036?style=flat-square&logo=groq&logoColor=white" />
  <img src="https://img.shields.io/badge/License-MIT-blue?style=flat-square" />
</p>

---

## What is Bugloo?

Bugloo is a full-stack AI code reviewer built as a portfolio project to demonstrate real-world AI engineering. Paste any code - in any language - and Bugloo auto-detects the language, sends it to Groq's blazing-fast LLM, and returns a clean structured review covering bugs, style issues, improvements, a quality score, and a plain-English explanation.

No manual language selection. No clunky UX. Just fast, intelligent feedback.

---

## Features

- 🔍 **Knows Your Language** : Paste any code and Bugloo figures out the language on its own.
- ⚡ **Fast Enough to Feel Instant** : Groq's LPU hardware makes most reviews land in under 3 seconds. No spinners, no waiting.
- 🧠 **Actually Useful Feedback** : Not a wall of text. Every review comes back in clean sections: Bugs, Style Issues, Improvements, a Quality Score, and a plain-English explanation of what your code does.
- 🔐 **Your Account, Your Reviews** : Sign up once. Everything is tied to your account and locked to you — nobody else sees your code or history.
- 📁 **Review History That Sticks** : Every review you run is saved. Go back anytime to see how your code has improved over time.
- 📄 **Download as PDF** : Export any review as a clean PDF to save, share with a mentor, or drop into your portfolio.
- 🛡️ **Handles Failures Gracefully** : When the AI is slow, the network drops, or something goes sideways; Bugloo shows a helpful message, not a crash.

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Frontend | Jinja2 Templates + HTML/CSS/JS |
| Language Detection | highlight.js (CDN) |
| AI Inference | Groq API — `llama3-70b-8192` |
| Database | Supabase (PostgreSQL) |
| Authentication | Supabase Auth (JWT) |
| Styling | TailwindCSS (CDN) |
| Deployment | Vercel + Render |

---

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mohitpandeycs/Bugloo.git
cd Bugloo

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set up environment variables
cp .env.example .env
# Fill in your credentials in .env

# 4. Run the development server
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
SECRET_KEY=your_secret_key_for_sessions
```

---

## Folder Structure

```
Bugloo/
├── api/
│   └── index.py                  # Vercel serverless entry point
├── app/
│   ├── routers/
│   │   ├── auth.py               # Login / signup routes
│   │   ├── history.py            # Review history page
│   │   └── review.py             # Code review endpoint
│   ├── services/
│   │   ├── groq_service.py       # Groq API integration + prompt logic
│   │   └── supabase_service.py   # Database read/write helpers
│   ├── static/
│   │   ├── css/
│   │   │   └── custom.css
│   │   ├── js/
│   │   └── favicon.svg
│   ├── templates/
│   │   ├── 404.html
│   │   ├── 500.html
│   │   ├── auth.html             # Single-page login/signup toggle
│   │   ├── base.html             # Base layout with navbar
│   │   ├── history.html          # Review history list
│   │   ├── index.html            # Code submission + review display
│   │   └── landing.html          # Public landing page
│   ├── utils/
│   │   └── error_mapper.py       # Maps API errors → friendly messages
│   ├── config.py                 # Pydantic settings from .env
│   ├── dependencies.py           # Auth middleware / JWT validation
│   └── main.py                   # FastAPI app entry point
├── .env.example
├── .gitignore
├── render.yaml
├── requirements.txt
└── vercel.json
```

---

## How It Works

```
User pastes code
      ↓
highlight.js detects language (client-side)
      ↓
POST /api/review → FastAPI
      ↓
Groq API (llama3-70b-8192) analyzes code
      ↓
Structured JSON response parsed
      ↓
Review saved to Supabase + displayed to user
```

---

## Connect With Me :)

Built and maintained by **[Mohit Pandey](https://github.com/mohitpandeycs)**

- GitHub — [@mohitpandeycs](https://github.com/mohitpandeycs)
- LinkedIn — [in/mohitpandeycs](https://linkedin.com/in/mohitpandeycs)
- Twitter / X — [@mohitpandeycs](https://x.com/mohitpandeycs)

---

## License

This project is released under the [MIT License](https://opensource.org/licenses/MIT).

---
<p align="center">
  If you find this useful, consider giving it a ⭐ Star — it helps other developers discover the project.
</p>