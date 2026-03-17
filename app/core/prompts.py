SYSTEM_PROMPT = """You are a professional academic advising assistant working for a private tutoring school that supports students preparing for higher education and career planning.

Your task:
Given a homeroom teacher's raw, casual meeting memo, rewrite it into a structured monthly meeting report.

Rules:
1. Preserve every concrete detail and number exactly (scores, dates, counts, names, etc.).
2. Reorganize the content into clear, professional, easy-to-read English without changing the facts.
3. If a required field is not mentioned in the memo, write "Not mentioned this month" in that field. Do not invent information.
4. If you can reasonably infer a potential risk from context, you may note it explicitly as an inference (label it as "Inference").
5. Keep a neutral and objective tone.

Output requirements:
Return ONLY valid JSON. Do not include any other text. Do not wrap JSON in markdown code blocks. Output in Japanese."""

USER_PROMPT_TEMPLATE = """Create a structured monthly meeting report based on the following information.

Student information:
- student_id: {student_id}
- student_name: {student_name}
- university: {university}
- major: {major}
- toeic: {toeic}
- jlpt: {jlpt}
- meeting_date: {meeting_date}

Raw memo:
{raw_memo}

Return JSON in exactly this structure (output JSON only, output in Japanese):

{{
  "student_id": "{student_id}",
  "student_name": "{student_name}",
  "meeting_date": "{meeting_date}",
  "events": "Summarize what the student has been engaging in. Include concrete facts and numbers when present. If missing, write: Not mentioned this month",
  "process": "Describe what is going well and what is not going well, based strictly on the memo. If missing, write: Not mentioned this month",
  "suggestions": "List advice, guidance, and information provided to the student. If missing, write: Not mentioned this month",
  "mental": "Summarize any mental/health/wellbeing signals or check-ins mentioned. If missing, write: Not mentioned this month"
}}"""

def build_user_prompt(
        student_id: str,
        student_name: str,
        university: str,
        major: str,
        toeic: str,
        jlpt: str,
        raw_memo: str,
        meeting_date: str,
) -> str:
    return USER_PROMPT_TEMPLATE.format(
        student_id=student_id,
        student_name=student_name,
        university=university,
        major=major,
        toeic=toeic,
        jlpt=jlpt,
        raw_memo=raw_memo,
        meeting_date=meeting_date,
    )