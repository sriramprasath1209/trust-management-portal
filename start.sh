#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$ROOT_DIR/logs"
mkdir -p "$LOG_DIR"

cd "$ROOT_DIR/backend"
if [ ! -d .venv ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
pip install -r requirements.txt
python -m app.db.seed

nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

cd "$ROOT_DIR/frontend"
npm install
nohup npm run dev -- --host 0.0.0.0 > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

cat <<EOF
Started the app.
Backend: http://localhost:8000/docs
Frontend: http://localhost:5173

Logs:
- $LOG_DIR/backend.log
- $LOG_DIR/frontend.log
EOF

printf 'Backend PID: %s\nFrontend PID: %s\n' "$BACKEND_PID" "$FRONTEND_PID"
