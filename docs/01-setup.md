# Local setup

## Requirements

- Python 3.11+
- Supabase project (URL + anon key)

## Setup

1. Create a virtual env:
   - Windows: `python -m venv .venv`
   - Activate: `.\.venv\Scripts\activate`

2. Install dependencies:
   - `pip install -e ".[dev]"`

3. Configure environment:
   - Copy `.env.example` → `.env`
   - Fill `SUPABASE_URL` and `SUPABASE_ANON_KEY`

## Run

- `uvicorn app.main:app --reload`
- Home: `http://127.0.0.1:8000/`
- Services: `http://127.0.0.1:8000/services`
