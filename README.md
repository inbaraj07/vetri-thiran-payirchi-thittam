# PocketSmart AI

Full-stack FastAPI + Jinja2 budget recommendation assistant based on the supplied project specification.

Features: Home Interior Planner, Party Planner, Jewelry Planner with optional outfit image, registration/login/logout, JWT token endpoint, session info/data, recommendation history, Gemini multimodal integration, structured outputs, and deterministic fallback recommendations.

## VS Code setup

Install Python 3.11+, VS Code and the Python extension. Open this folder.

Windows PowerShell:
```powershell
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

macOS/Linux:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Leave GEMINI_API_KEY empty for a fully runnable demo using fallback recommendations. To enable Gemini, put your key in `.env` and set GEMINI_MODEL. The original document names Gemini 1.5 Flash Pro; the implementation keeps the model configurable because model availability changes.

## Run
```bash
uvicorn app.main:app --reload
```
Open http://127.0.0.1:8000 and API docs at http://127.0.0.1:8000/docs.

## Test
```bash
pytest -q
```

The app intentionally does not pretend that Amazon, Flipkart, IKEA, Swiggy, Zomato or OYO APIs are connected. The supplied document asks for mock/simulated sourcing, so recommendations use platform search links and clearly label estimates.

For production, use PostgreSQL, HTTPS, a secret manager, object storage, rate limiting, file scanning, observability, and real vendor/commerce APIs or approved affiliate/product feeds.
