@echo off
setlocal
set ROOT=%~dp0

cd /d "%ROOT%backend"
if not exist .venv (
  python -m venv .venv
)
call .venv\Scripts\activate
pip install -r requirements.txt
python -m app.db.seed
start "Backend" cmd /k uvicorn app.main:app --host 0.0.0.0 --port 8000

cd /d "%ROOT%frontend"
npm install
start "Frontend" cmd /k npm run dev -- --host 0.0.0.0

echo Backend: http://localhost:8000/docs
echo Frontend: http://localhost:5173
