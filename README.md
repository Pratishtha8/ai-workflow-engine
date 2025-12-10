# Mini Workflow Engine – Code Review Agent (Improved)

This project implements a **mini workflow / graph engine** using **FastAPI**, built as part of an AI Engineering assignment.  
It includes a fully working workflow: **Automated Code Review Agent** (Assignment Option A).

The engine demonstrates core ideas used in modern agent frameworks (LangGraph, AutoGPT, CrewAI):

- Node-based execution  
- Directed graph workflows  
- Async processing  
- State tracking and looping  
- Persistence  
- REST + WebSocket interfaces  

---

## Features

### Workflow Engine
- Directed graph (DAG-style) execution  
- Async node functions  
- Looping until a condition (quality threshold) is met  
- Logs stored step-by-step  
- Clean separation of nodes, workflow definition, and runner  

### Persistence
- SQLite database stores:
  - Workflow graphs  
  - Run history  
  - State snapshots  

### API Endpoints
| Endpoint | Description |
|----------|-------------|
| `POST /graph/create` | Create the workflow graph |
| `POST /graph/run` | Run the code-review workflow |
| `GET /graph/state/{run_id}` | Fetch run state & logs |
| `GET /ws/{run_id}` | Live WebSocket log streaming |

---

## Project Structure

```
ai-workflow-engine/
│
├── app/
│   ├── engine/          # Workflow runner, node execution, DB logic
│   ├── models/          # Pydantic schemas for API
│   ├── workflows/       # Code Review workflow definition
│   └── main.py          # FastAPI app & routes
│
├── requirements.txt
├── requests.http         # Sample API tests for VS Code REST Client
└── README.md             # Project documentation
```

---

##  Code Review Workflow (Assignment Option A)

| Node | Purpose |
|------|---------|
| `extract_functions` | Extracts Python function signatures |
| `check_complexity` | Computes basic complexity score |
| `detect_issues` | Flags prints, long lines, unused vars, etc. |
| `suggest_improvements` | Suggests refactoring + improvements |
| `compute_quality` | Generates final quality score |

###  Loop Logic
```
while quality_score < threshold:
    run suggest_improvements
    run compute_quality again
```

This imitates iterative refinement used in agentic LLM systems.

---

##  How to Run Locally

### 1️ Create & activate virtual environment
```bash
python -m venv .venv
source .venv/bin/activate      # macOS/Linux
.\.venv\Scripts\activate       # Windows
```

### 2️ Install dependencies
```bash
pip install -r requirements.txt
```

### 3️ Start the server
```bash
uvicorn app.main:app --reload
```

### 4️ Open API docs
- Swagger: http://127.0.0.1:8000/docs  
- WebSocket logs: ws://127.0.0.1:8000/ws/{run_id}

---

##  Quick Workflow Test

### 1. Create graph
```
POST /graph/create
```

### 2. Run workflow
```
POST /graph/run
{
  "graph_id": "YOUR_GRAPH_ID",
  "code": "def hello(): print('hi')",
  "threshold": 7
}
```

### 3. Fetch state
```
GET /graph/state/{run_id}
```

### Example Output
```json
{
  "finished": true,
  "state": {
    "functions": ["hello"],
    "complexity": 3,
    "issues": ["use-logging-instead-of-print"],
    "suggestions": ["replace-print-with-logging"],
    "quality_score": 7,
    "logs": [
      "extract_functions -> 1 found",
      "check_complexity -> 5",
      "detect_issues -> 1",
      "compute_quality -> 6",
      "compute_quality -> 7"
    ]
  }
}
```

---

##  Tools Used

- FastAPI  
- AsyncIO  
- AioSQLite  
- Uvicorn  
- Pydantic  

---

##  Potential Improvements

- Add authentication + role-based access  
- Add more workflows (RAG evaluator, LLM Summarizer)  
- Parallel node execution  
- Distributed worker queue (Celery/RQ)  
- UI dashboard for workflow monitoring  
- Unit tests  

---

##  Summary

This project demonstrates:

- Understanding of workflow/agent engines  
- Async stateful execution  
- Graph-based reasoning  
- Logging + persistence  
- Clean API design 