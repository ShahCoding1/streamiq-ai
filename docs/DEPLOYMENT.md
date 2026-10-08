# Deployment

Local: python -m uvicorn backend.app.main:app --reload --reload-dir backend, and npm run dev in frontend. Docker: docker compose up --build; frontend on localhost:8080 and API on localhost:8000. CORS_ORIGINS controls browser cross-origin access. No production auth or rate limiting is included; deploy behind a secure gateway for public use.
