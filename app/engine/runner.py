import uuid, asyncio, os, aiosqlite, json
from typing import Dict

class Runner:
    def __init__(self, db_path: str = 'data/workflows.db'):
        self.graphs: Dict[str, Dict] = {}
        self.runs: Dict[str, Dict] = {}
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self.db_initialized = False  # prevent double initialization

    async def init_db(self):
        """Create DB tables if not created."""
        if self.db_initialized:
            return

        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                'CREATE TABLE IF NOT EXISTS graphs (graph_id TEXT PRIMARY KEY, payload TEXT)'
            )
            await db.execute(
                'CREATE TABLE IF NOT EXISTS runs (run_id TEXT PRIMARY KEY, graph_id TEXT, state TEXT, finished INTEGER)'
            )
            await db.commit()

        self.db_initialized = True

    async def ensure_db(self):
        """Ensure DB is initialized BEFORE any DB action."""
        await self.init_db()

    def create_graph(self, graph_data: Dict):
        graph_id = str(uuid.uuid4())
        self.graphs[graph_id] = graph_data

        # schedule async DB save
        asyncio.create_task(self._persist_graph(graph_id, graph_data))

        return graph_id

    async def _persist_graph(self, graph_id: str, graph_data: Dict):
        await self.ensure_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO graphs (graph_id, payload) VALUES (?, ?)",
                (graph_id, json.dumps(graph_data, default=str)),
            )
            await db.commit()

    def run(self, graph_id: str, initial_state: Dict) -> str:
        if graph_id not in self.graphs:
            raise KeyError("graph not found")

        run_id = str(uuid.uuid4())
        self.runs[run_id] = {"state": {"logs": ["run-started"]}, "finished": False}

        # persist the initial run state
        asyncio.create_task(self._persist_run(run_id, graph_id, self.runs[run_id]["state"], False))

        # execute workflow async
        asyncio.create_task(self._execute_run(run_id, graph_id, initial_state))

        return run_id

    async def _persist_run(self, run_id, graph_id, state, finished):
        await self.ensure_db()
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(
                "INSERT OR REPLACE INTO runs (run_id, graph_id, state, finished) VALUES (?, ?, ?, ?)",
                (run_id, graph_id, json.dumps(state, default=str), int(finished)),
            )
            await db.commit()

    async def _execute_run(self, run_id: str, graph_id: str, initial_state: Dict):
        await self.ensure_db()

        graph = self.graphs[graph_id]
        state = dict(initial_state)
        state.setdefault("logs", [])

        current = graph["start"]
        threshold = graph.get("threshold", 7)

        while current is not None:
            fn = graph["nodes"][current]

            # run node
            try:
                state = await fn(state)
            except Exception as e:
                state.setdefault("logs", []).append(f"error-in-{current}:{e}")
                break

            # persist progress
            self.runs[run_id]["state"] = state
            await self._persist_run(run_id, graph_id, state, False)

            # loop logic
            if current == "compute_quality":
                if state.get("quality_score", 0) < threshold:
                    next_node = "suggest_improvements"
                else:
                    next_node = graph["edges"].get(current)
            else:
                next_node = graph["edges"].get(current)

            current = next_node
            await asyncio.sleep(0.05)

        # workflow finished
        self.runs[run_id]["state"] = state
        self.runs[run_id]["finished"] = True
        await self._persist_run(run_id, graph_id, state, True)
