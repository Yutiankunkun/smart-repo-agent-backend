# Smart Repo Agent

A FastAPI-based backend system that helps homeroom teachers at private tutoring schools manage student meetings with AI assistance. The system uses an LLM agent to process meeting memos, query student history, and update student information through natural language.

## Features

- **AI Chat Agent**: Natural language interface for homeroom teachers to interact with student data
- **Meeting Memo Summarization**: Convert raw meeting notes into structured reports (events, process, suggestions, mental health)
- **Student Management**: CRUD operations for students and teachers
- **Meeting History**: Query and manage meeting records per student
- **PDF Report Generation**: Optional PDF export for meeting reports (requires `pdfkit`)

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **LLM**: Alibaba DashScope (Qwen) via OpenAI-compatible API
- **Templates**: Jinja2 for PDF reports

## Project Structure

```
smart-repo-agent-backend/
├── app/
│   ├── agent/          # AI agent with tool-calling
│   │   ├── agent.py    # Agent loop and orchestration
│   │   ├── executor.py # Tool execution handlers
│   │   └── tools.py    # Tool definitions for LLM
│   ├── api/            # FastAPI route handlers
│   ├── core/           # Database, prompts, config
│   ├── crud/           # Database operations
│   ├── models/         # SQLAlchemy models
│   ├── schemas/        # Pydantic schemas
│   ├── services/       # LLM, PDF generation
│   └── templates/      # Jinja2 templates
├── main.py
├── Dockerfile
└── requirements.txt
```

## Getting Started

### Prerequisites

- Python 3.10+
- DashScope API key (Alibaba Cloud)

### Installation

```bash
# Create virtual environment (recommended)
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root:

```env
DASHSCOPE_API_KEY=your_api_key_here
# Optional: custom base URL
# DASHSCOPE_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
```

Optional: override the SQLite location (defaults to `./report_agent_system_lantian.db` in the working directory):

```env
DATABASE_URL=sqlite:////absolute/path/to/your.db
```

### Run the Server

```bash
python main.py
```

The API will be available at `http://localhost:8000`. Interactive docs: `http://localhost:8000/docs`.

### Optional: PDF Generation

To enable PDF report generation, install `pdfkit` and `wkhtmltopdf`:

```bash
pip install pdfkit
# Install wkhtmltopdf: https://wkhtmltopdf.org/downloads.html
```

## Docker (full stack from repo root)

The parent monorepo ships **Docker Compose** and **Nginx** so you can run the UI and API together (for example on **AWS EC2**). The public HTTP port is **8080**; Nginx serves the SPA and proxies `/api/*` to this service on port 8000 inside the network.

From the repository root (where `docker-compose.yml` lives):

1. Ensure `smart-repo-agent-backend/.env` exists with at least `DASHSCOPE_API_KEY`.
2. Build and start:

```bash
docker compose up -d --build
```

3. Open `http://<host>:8080`. API via the proxy: `http://<host>:8080/api/...`. FastAPI docs: `http://<host>:8080/docs`.

SQLite data is stored in the Docker volume `backend_data` (path inside the container: `/app/data/report_agent_system_lantian.db`).

**Backend image only** (no Nginx):

```bash
docker build -t smart-repo-agent-backend ./smart-repo-agent-backend
docker run --rm -p 8000:8000 --env-file ./smart-repo-agent-backend/.env \
  -e DATABASE_URL=sqlite:////app/data/report_agent_system_lantian.db \
  -v smart_repo_data:/app/data smart-repo-agent-backend
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/health` | Health check |
| POST | `/chat/` | Chat with the AI agent |
| GET/POST | `/students/` | List or create students |
| GET/PUT/DELETE | `/students/{id}` | Student CRUD |
| GET/POST | `/teachers/` | List or create teachers |
| GET | `/meetings/students/{id}/meetings` | Get meetings by student |
| GET/DELETE | `/meetings/{id}` | Get or delete a meeting |
| GET | `/meetings/pdf/{id}` | Download meeting PDF |

## Agent Tools

The chat agent can use these tools based on user intent:

- **summarize_memo**: Convert meeting notes into a structured report
- **query_history**: Retrieve a student's meeting history
- **update_student_info**: Update student fields (toeic, jlpt, university, etc.)
- **get_student_info**: Get student profile
- **ask_follow_up**: Request additional information when memo is incomplete
