# Bugloo

A web application that provides instant, structured AI-powered code feedback. Built with FastAPI, Supabase, and Groq API.

## Features
- **Auto Language Detection**: Automatically detects programming languages via `highlight.js`.
- **Intelligent Feedback**: Powered by `llama3-70b-8192` via Groq's ultra-fast API.
- **Structured Sections**: Code is reviewed for Bugs, Style Issues, and Improvements, with an overall quality score.
- **Persistent History**: All reviews are saved privately to Supabase PostgreSQL.
- **Brutalist Dark Theme**: A high-end developer tool aesthetic.

## Setup
1. Clone the repo.
2. `pip install -r requirements.txt`
3. Copy `.env.example` to `.env` and fill in credentials.
4. Run `uvicorn app.main:app --reload`.

## Built With
- FastAPI
- Supabase (Auth + DB)
- Groq LLM API
- TailwindCSS

# Folder Structure 

```
└── 📁api
    └──
        ├── index.cpython-311.pyc
    └── index.py
└── 📁app
    └── 
        ├── config.cpython-311.pyc
        ├── dependencies.cpython-311.pyc
        ├── main.cpython-311.pyc
    └── 📁routers
        └── 
        ├── auth.py
        ├── history.py
        ├── review.py
    └── 📁services
        └── 
        ├── groq_service.py
        ├── supabase_service.py
    └── 📁static
        └── 📁css
            ├── custom.css
        └── 📁js
        ├── favicon.svg
    └── 📁templates
        ├── 404.html
        ├── 500.html
        ├── auth.html
        ├── base.html
        ├── history.html
        ├── index.html
        ├── landing.html
    └── 📁utils
        └──error_mapper.py
    ├── config.py
    ├── dependencies.py
    └── main.py
└── .env
└── README.md
└── vercel.json
└── requirements.txt
```