# Mini Workflow Engine - Code Review Agent (Improved)

This is an interview-ready FastAPI project implementing a tiny workflow/graph engine and a sample
"Code Review" workflow (Option A). Improvements over the basic version:

- Async node functions (allowing future long-running tasks)
- Background task runner using FastAPI's BackgroundTasks
- SQLite persistence for graphs and runs (simple, file-based DB)
- WebSocket endpoint to stream logs while run is executing
- VS Code launch configuration for easy debugging
- REST client `.http` for quick endpoint testing
- Clearer comments and small unit-test friendly structure

## Run locally (recommended steps)

1. Create & activate virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate       # macOS / Linux
   .\\.venv\\Scripts\\activate  # Windows PowerShell
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Start the server
   ```bash
   uvicorn app.main:app --reload
   ```

4. Open docs:
   - REST API: http://127.0.0.1:8000/docs
   - WebSocket echo: ws://127.0.0.1:8000/ws/{run_id}

## Quick workflow test (use the provided `requests.http` file in VS Code or curl)

1. Create graph: POST /graph/create
2. Run graph: POST /graph/run with graph_id and code
3. Poll /graph/state/{run_id} for status OR connect to ws://127.0.0.1:8000/ws/{run_id} to stream logs

## What to improve further (if you had more time)
- Add authentication & RBAC
- Add richer tools registry with dynamic registration API
- Add tests for each node and the runner
- Use an async task queue (Celery/RQ) for heavy jobs

