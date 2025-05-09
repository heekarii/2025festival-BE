# server.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

app = FastAPI()

# CORS: Next.js(3000)에서 호출 허용
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Table(BaseModel):
    id: int
    name: str
    entryTime: Optional[str] = None  # ISO 문자열

# 메모리상에만 저장하는 예시 (총 5개)
tables: List[Table] = [
    Table(id=i, name=f"테이블 {i}") for i in range(1, 6)
]

@app.get("/tables", response_model=List[Table])
def get_tables():
    return tables

@app.post("/tables/{table_id}/enter", response_model=Table)
def enter_table(table_id: int):
    for t in tables:
        if t.id == table_id:
            t.entryTime = datetime.utcnow().isoformat()
            return t
    raise HTTPException(404, "테이블이 없습니다")

@app.post("/tables/{table_id}/reset", response_model=Table)
def reset_table(table_id: int):
    for t in tables:
        if t.id == table_id:
            t.entryTime = None
            return t
    raise HTTPException(404, "테이블이 없습니다")
