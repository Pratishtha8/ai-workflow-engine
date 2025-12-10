from pydantic import BaseModel
from typing import Optional

class RunRequest(BaseModel):
    graph_id: str
    code: str
    threshold: Optional[int] = None
