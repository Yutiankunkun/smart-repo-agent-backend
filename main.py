import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.api import students, teachers, meetings, chat


app = FastAPI(
    title="Smart Repo Agent",
    description="AI-assisted backend for homeroom teachers to manage student meetings, summarize memos, and maintain student records.",
    version="0.1.1",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database
Base.metadata.create_all(bind=engine)

# Routers
app.include_router(students.router, prefix="/students", tags=["Student Management"])
app.include_router(teachers.router, prefix="/teachers", tags=["Teacher Management"])
app.include_router(meetings.router, prefix="/meetings", tags=["Meeting Management"])
app.include_router(chat.router, prefix="/chat", tags=["Agent Chat"])


@app.get("/health")
def health_check():
    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)