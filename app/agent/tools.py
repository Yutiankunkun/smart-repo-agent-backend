def _tool(name: str, description: str, properties: dict, required: list) -> dict:
    return {
        "type": "function",
        "function": {
            "name": name,
            "description": description,
            "parameters": {
                "type": "object",
                "properties": properties,
                "required": required,
            },
        },
    }


TOOLS = [
    # Tool 1: Summarize Interview Notes
    _tool(
        "summarize_memo",
        "Convert a homeroom teacher's interview notes into a structured report. "
        "Use this when the input contains records, observations, or notes from a student meeting. "
        "Do not use for querying, updating information, or non-summarization tasks.",
        {
            "student_id": {"type": "string", "description": "Student ID"},
            "raw_memo": {"type": "string", "description": "Raw notes to be summarized"},
            "meeting_date": {"type": "string", "description": "Meeting date in format YYYY-MM-DD"},
        },
        ["student_id", "raw_memo"],
    ),

    # Tool 2: Query Student Interview History
    _tool(
        "query_history",
        "Retrieve historical interview records of a student. "
        "Use when the teacher wants to review or compare past meeting reports. "
        "Returns structured reports for each meeting.",
        {
            "student_id": {"type": "string", "description": "Student ID"},
            "limit": {"type": "integer", "description": "Maximum number of records to return (default: 3)"},
        },
        ["student_id"],
    ),

    # Tool 3: Update Student Information
    _tool(
        "update_student_info",
        "Update a student's basic information such as TOEIC score, JLPT level, or target exam. "
        "Use when the teacher mentions updates to student records. "
        "Only update one field at a time.",
        {
            "student_id": {"type": "string", "description": "Student ID"},
            "field": {
                "type": "string",
                "description": "Field to update",
                "enum": ["toeic", "jlpt", "university", "major", "name", "teacher_id"],
            },
            "value": {"type": "string", "description": "New value"},
        },
        ["student_id", "field", "value"],
    ),

    # Tool 4: Get Student Information
    _tool(
        "get_student_info",
        "Retrieve a student's basic information such as name, target exam, and scores. "
        "Use when the teacher asks about a student's profile.",
        {
            "student_id": {"type": "string", "description": "Student ID"},
        },
        ["student_id"],
    ),

    # Tool 6: Ask Follow-up Questions
    _tool(
        "ask_follow_up",
        "Ask for additional information when the provided interview notes are insufficient "
        "to generate a complete report. "
        "Use only when key details are missing (e.g., very short or incomplete input). "
        "Avoid over-questioning—if the information is mostly sufficient, use summarize_memo instead.",
        {
            "questions": {
                "type": "string",
                "description": "Specific follow-up questions for the teacher, written in natural language",
            },
        },
        ["questions"],
    ),
]
