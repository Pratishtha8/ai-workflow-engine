import json
from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional
from app.engine.runner import Runner
from app.workflows.code_review import get_code_review_workflow

app = FastAPI(title="Mini Workflow Engine - Code Review (Improved)")
runner = Runner(db_path="data/workflows.db")

class CreateGraphResponse(BaseModel):
    graph_id: str

class RunRequest(BaseModel):
    graph_id: str
    code: str
    threshold: Optional[int] = None

@app.post("/graph/create", response_model=CreateGraphResponse)
async def create_graph(threshold: Optional[int] = None):
    workflow = get_code_review_workflow(threshold=threshold or 7)
    graph_id = runner.create_graph(workflow)
    return {"graph_id": graph_id}

@app.post("/graph/run")
async def run_graph(req: RunRequest, background_tasks: BackgroundTasks):
    if req.graph_id not in runner.graphs:
        raise HTTPException(status_code=404, detail="graph_id not found")
    initial_state = {"code": req.code}
    run_id = runner.run(req.graph_id, initial_state)
    return {"run_id": run_id, "status": "started"}

@app.get("/graph/state/{run_id}")
async def graph_state(run_id: str):
    if run_id not in runner.runs:
        raise HTTPException(status_code=404, detail="run_id not found")
    run_info = runner.runs[run_id]
    return {"run_id": run_id, "finished": run_info.get("finished", False), "state": run_info["state"], "logs": run_info["state"].get("logs", [])}

# Simple WebSocket manager to stream logs for a running run_id
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, run_id: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[run_id] = websocket

    def disconnect(self, run_id: str):
        if run_id in self.active_connections:
            del self.active_connections[run_id]

    async def send_log(self, run_id: str, message: str):
        ws = self.active_connections.get(run_id)
        if ws:
            await ws.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{run_id}")
async def websocket_endpoint(websocket: WebSocket, run_id: str):
    await manager.connect(run_id, websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(run_id)
