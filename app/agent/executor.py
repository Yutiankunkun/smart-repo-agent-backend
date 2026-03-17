import json
from datetime import date
from app.crud import student as student_crud
from sqlalchemy.orm import Session
from app.schemas.meeting import MeetingInput
from app.services.llm import call_dashscope
from app.crud import meeting as meeting_crud


def execute_tool(
        tool_name: str,
        tool_input: dict,
        db: Session,
) -> str:
    """
    Set and show how a tool can be executed.

    :param tool_name:
    :param tool_input:
    :param db:
    :return:
    """

    handlers = {
        "summarize_memo": _handler_summarize_memo,
        "query_history": _handler_query_history,
        "update_student_info": _handler_update_student_info,
        "get_student_info": _handler_get_student_info,
        "ask_follow_up": _handler_ask_follow_up,
    }

    handler = handlers.get(tool_name)
    if not handler:
        raise ValueError(f"Tool {tool_name} not found")

    return handler(tool_input, db)


def _handler_summarize_memo(
        input_data: dict,
        db: Session
) -> str:
    """
    Executor -> summarize memo.

    :param input_data:
    :param db:
    :return:
    """

    student_id = input_data["student_id"]
    student = student_crud.get_student(db, student_id)
    if not student:
        return json.dumps({"error": "Student not found"}, ensure_ascii=False)

    memo = input_data["raw_memo"]
    meeting_date = input_data.get("meeting_date") or date.today().strftime("%Y-%m-%d")

    result = call_dashscope(
        student=student,
        raw_memo=memo,
        meeting_date=meeting_date,
    )
    if result.get("error"):
        return json.dumps({"error": result["error"]}, ensure_ascii=False)
    report = result["report"]

    # Save meeting record
    input_object = MeetingInput(
        student_id=student_id,
        raw_memo=memo,
        meeting_date=meeting_date,
    )

    record = meeting_crud.create_meeting(
        db=db,
        input_data=input_object,
        output_data=report,
    )

    return json.dumps({
        "message": "Summarize memo successfully.",
        "record_id": record.id,
        "report": {
            "events": report.events,
            "suggestions": report.suggestions,
            "mental": report.mental,
            "process": report.process,
        }
    }, ensure_ascii=False)


def _handler_query_history(
        input_data: dict,
        db: Session
) -> str:
    """
    Executor -> query history.

    :param input_data:
    :param db:
    :return:
    """

    student_id = input_data["student_id"]
    student = student_crud.get_student(db, student_id)
    if not student:
        return json.dumps({"error": "Student not found"}, ensure_ascii=False)

    records = meeting_crud.get_meetings_by_student(db, student_id)
    limit = input_data.get("limit")
    if limit is not None and limit > 0:
        records = records[:limit]
    if not records:
        return json.dumps({
            "student_id": student_id,
            "student_name": student.name,
            "message": "No meeting records found."
        }, ensure_ascii=False)

    history = []
    for r in records:
        history.append({
            "id": r.id,
            "meeting_date": r.meeting_date,
            "process": r.process,
            "suggestions": r.suggestions,
            "mental": r.mental,
            "events": r.events,
        })

    return json.dumps({
        "student_id": student_id,
        "student_name": student.name,
        "Number of meeting records": len(records),
        "records": history,
    }, ensure_ascii=False)


def _handler_update_student_info(
        input_data: dict,
        db: Session
) -> str:
    """
    Executor -> update student info.

    :param input_data:
    :param db:
    :return:
    """

    student_id = input_data["student_id"]
    student = student_crud.get_student(db, student_id)
    if not student:
        return json.dumps({"error": "Student not found"}, ensure_ascii=False)

    field = input_data.get("field")
    value = input_data["value"]
    if not field:
        return json.dumps({"error": "field is required"}, ensure_ascii=False)

    student_crud.update_student(db, student_id, **{field: value})

    return json.dumps({
        "message": "Update student info successfully.",
    }, ensure_ascii=False)


def _handler_get_student_info(
        input_data: dict,
        db: Session
) -> str:
    """
    Executor -> get student info.

    :param input_data:
    :param db:
    :return:
    """
    student_id = input_data["student_id"]
    student = student_crud.get_student(db, student_id)
    if not student:
        return json.dumps({"error": "Student not found"}, ensure_ascii=False)

    return json.dumps({
        "student_id": student.id,
        "student_name": student.name,
        "university": student.university,
        "major": student.major,
        "toeic": student.toeic,
        "jlpt": student.jlpt,
        "teacher_id": student.teacher_id,
    }, ensure_ascii=False)


def _handler_ask_follow_up(
        input_data: dict,
        db: Session
) -> str:
    questions = input_data.get("questions", "")
    if isinstance(questions, list):
        questions = ", ".join(questions)
    return json.dumps({
        "questions": questions,
    }, ensure_ascii=False)