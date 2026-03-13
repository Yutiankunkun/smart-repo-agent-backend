import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from schemas import MeetingInput, Response, MeetingOutput
from service import call_dashscope

app = FastAPI(
    title="Smart Repo Agent",
    description="A smart system to help you generate repo with AI agent.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.post(
    "/api/folder/generate_repo",
    response_model=Response,
)
def generate_repo(meeting_input: MeetingInput):
    result = call_dashscope(
        student_id=meeting_input.student_id,
        student_name=meeting_input.student_name,
        university=meeting_input.university,
        major=meeting_input.major,
        toeic=meeting_input.toeic,
        jlpt=meeting_input.jlpt,
        memo=meeting_input.memo,
        meeting_date=meeting_input.meeting_date,
    )

    return Response(
        report=result["report"],
        error=result["error"],
    )

@app.post(
    "/api/folder/generate_repo_test",
    response_model=Response,
)
def generate_repo_test():
    mock_report = MeetingOutput(
        student_id = "id0001",
        student_name = "藍天",
        meeting_date = "2026年3月29日",
        events = "Student talked about recent job hunting preparation, updating resume, and practicing coding interview problems. Also mentioned attending a university AI seminar last week.",
        process = "The preparation is generally going well. The student has made progress in technical interview practice but still feels slightly uncertain about system design questions.",
        suggestions = "Advised the student to practice more mock interviews, especially focusing on system design and behavioral questions. Recommended preparing several concrete project examples and reviewing common backend architecture patterns.",
        mental = "The student seems slightly stressed due to job hunting pressure but overall maintains a positive attitude and motivation."
    )

    return Response(
        report=mock_report,
        error=None,
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)