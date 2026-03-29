# Job Application Tracker

A full-stack, AI-native job application tracker with three interfaces — a REST API, a web dashboard, and an MCP server that lets AI assistants manage your applications through natural language.

---

## Architecture
 
```
┌─────────────────────────────────────────────────────┐
│                    Interfaces                        │
│                                                      │
│   FastAPI (REST)   Streamlit (UI)   FastMCP (AI)    │
│   Render           Streamlit Cloud  Render           │
└────────────┬───────────────┬──────────────┬─────────┘
             │               │              │
             └───────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │   PostgreSQL    │
                    │   Render        │
                    └─────────────────┘
```

One database. Three ways to interact. All live.

---

## Live Demos

| Interface | URL |
|-----------|-----|
| REST API (Swagger) | https://job-application-tracker-api-eu2z.onrender.com/docs |
| Streamlit Dashboard | *https://mt-job-application-tracker.streamlit.app/* |
| MCP Server | https://job-application-mcp.onrender.com/mcp |

> **Note:** Render free tier spins down after 15 minutes of inactivity. First request may take ~30 seconds.

---

## Features

### REST API (FastAPI)
- Full CRUD for job applications
- Filtering by status, search term, date range
- Sorting and pagination
- Dedicated `/applications/all` endpoint for analytics (no pagination)
- Auto-generated Swagger docs at `/docs`

### Web Dashboard (Streamlit)
- Add, update, and delete applications
- Filter and search
- Visual analytics — status breakdown, application trends
- Connects to the same live database as the API

### MCP Server (FastMCP)
- 8 tools accessible to any MCP-compatible AI assistant
- Natural language interface: *"Add an application for Data Scientist at Google"*
- Deployed over HTTP — connectable from Claude.ai browser, Claude Desktop, Cursor, and more
- Same PostgreSQL database as the REST API — consistent data across all interfaces

---

## MCP Tools

| Tool | Description |
|------|-------------|
| `add_application` | Add a new job application |
| `update_application_status` | Update status of an existing application |
| `delete_application` | Delete an application by ID |
| `get_all_applications` | List all applications (most recent first) |
| `get_application_by_id` | Get details of a specific application |
| `search_applications` | Filter by company, role, status, date range |
| `get_statistics` | Status breakdown, trends, top companies |
| `get_status_options` | List of recommended status values |

---

## Connecting the MCP Server

### Claude.ai (Browser)
Go to **Settings → Integrations → Add MCP Server** and paste:
```
https://job-application-mcp.onrender.com/mcp
```

### Claude Desktop
Add to `claude_desktop_config.json`:
```json
{
  "mcpServers": {
    "job-tracker": {
      "type": "http",
      "url": "https://job-application-mcp.onrender.com/mcp"
    }
  }
}
```

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| REST API | FastAPI, Pydantic v2 |
| Web UI | Streamlit, Pandas |
| MCP Server | FastMCP |
| Database | PostgreSQL (psycopg2) |
| Hosting | Render (API + MCP + DB), Streamlit Cloud |
| Config | python-dotenv, Streamlit Secrets |

---

## Project Structure

```
job-application-tracker/                        # Main repo
├── backend/
│   ├── main.py                     # FastAPI app
│   ├── crud.py                     # Database operations
│   ├── database.py                 # PostgreSQL connection
│   └── models.py                   # Pydantic schemas
├── frontend/
│   └── app.py                      # Streamlit dashboard
└── requirements.txt

job-application-mcp/                # MCP repo
├── server.py                       # FastMCP server (8 tools)
└── requirements.txt
```

---

## Local Development

### Prerequisites
- Python 3.10+
- PostgreSQL (or use the Render cloud DB)

### Setup

```bash
# Clone the repo
git clone https://github.com/transformer1234/job-tracker
cd job-tracker

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Add your DATABASE_URL to .env

# Run FastAPI
python -m uvicorn backend.main:app --reload

# Run Streamlit (separate terminal)
streamlit run frontend/app.py
```

### MCP Server

```bash
git clone https://github.com/transformer1234/job-application-mcp
cd job-application-mcp
pip install -r requirements.txt

# Add DATABASE_URL to .env
python server.py
```

---

## Key Design Decisions

- **Single database, multiple interfaces** — FastAPI, Streamlit, and the MCP server all share one PostgreSQL instance on Render, ensuring consistent data across all interfaces
- **Dedicated analytics endpoint** — `/applications/all` bypasses pagination to give analytics accurate counts across the full dataset
- **HTTP transport for MCP** — deployed over `streamable-http` instead of `stdio`, making the MCP server accessible from browser-based AI clients without local installation
