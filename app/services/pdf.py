from pathlib import Path
from jinja2 import Environment, FileSystemLoader


try:
    import pdfkit
    PDFKIT_AVAILABLE = True
except ImportError:
    pdfkit = None
    PDFKIT_AVAILABLE = False

PDF_DIR = Path("./pdf_folder/").resolve()
PDF_DIR.mkdir(parents=True, exist_ok=True)

TEMPLATES_DIR = Path("./app/templates/").resolve()

jinja_env = Environment(
    loader=FileSystemLoader(TEMPLATES_DIR),
    autoescape=True,
)

def generate_pdf(
        teacher_specialty: str,
        student_id: str,
        student_name: str,
        university: str,
        major: str,
        toeic: str,
        jlpt: str,
        meeting_date: str,
        raw_memo: str,
        teacher_name: str,
        events: str,
        process: str,
        suggestions: str,
        mental: str,
        teacher_id: str,
) -> dict:
    """
    Generate a PDF report.

    :param teacher_specialty:
    :param student_id:
    :param student_name:
    :param university:
    :param major:
    :param toeic:
    :param jlpt:
    :param meeting_date:
    :param raw_memo:
    :param teacher_name:
    :param events:
    :param process:
    :param suggestions:
    :param mental:
    :param teacher_id:
    :return:
    """

    if not PDFKIT_AVAILABLE:
        return {
            "pdf_path": None,
            "error": "PDFKit is not available. Please install it to generate PDFs."
        }
    try:
        template = jinja_env.get_template("report.html")
        content = template.render(
            teacher_specialty=teacher_specialty,
            student_id=student_id,
            student_name=student_name,
            university=university,
            major=major,
            toeic=toeic,
            jlpt=jlpt,
            meeting_date=meeting_date,
            raw_memo=raw_memo,
            teacher_name=teacher_name,
            events=events,
            process=process,
            suggestions=suggestions,
            mental=mental,
            teacher_id=teacher_id,
        )

        name = f"{student_id}_{student_name}_{meeting_date}"
        filename = f"{name}.pdf"
        filepath = PDF_DIR / filename

        pdfkit.from_string(content, str(filepath))

        return{
            "pdf_path": str(filepath),
            "error": None,
        }

    except Exception as e:
        return {
            "pdf_path": None,
            "error": str(e),
        }