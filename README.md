# Todo Application (Claude Code Practice Project)

A small full-stack todo app built as a **learning sandbox for exploring [Claude Code](https://claude.com/claude-code)** — its commands, capabilities and workflows. The app itself is intentionally simple so the focus stays on *how* it was built with an AI coding assistant: reading and editing code, running commands, working from a design mockup, and using git/GitHub from the terminal.

## Purpose

- Test Claude Code commands and capabilities (file editing, shell commands, background tasks, git workflows).
- Practice turning a design image into working UI.
- Gain hands-on knowledge of a minimal FastAPI + vanilla JavaScript stack.

## Features

- Add, complete (toggle) and delete tasks
- Input validation: empty titles are rejected (frontend and backend)
- Persistent storage in a local JSON file
- Modern dark-teal UI with glass-style card, gradient input and button, colored task dots and trash icon
- Hot reload during development

## Tech Stack

| Layer    | Technology                                   |
|----------|----------------------------------------------|
| Backend  | Python 3, [FastAPI](https://fastapi.tiangolo.com/), [Uvicorn](https://www.uvicorn.org/) |
| Frontend | HTML5, CSS3, vanilla JavaScript (no framework) |
| Storage  | JSON file (`data/todos.json`)                     |

## Project Structure

```
.
├── run.py                       # Dev server entry point
├── app/                         # Backend
│   ├── main.py                  # create_app(): wires routers + static mount
│   ├── core/config.py           # Settings (env-overridable)
│   ├── api/
│   │   ├── deps.py              # Dependency wiring (service <- repository)
│   │   └── routes/              # todos.py (REST), pages.py (HTML)
│   ├── schemas/todo.py          # Pydantic models
│   ├── services/todo_service.py # Business rules (validation, not-found)
│   └── repositories/            # Storage layer: base.py (interface),
│                                #   json_repository.py, factory.py
├── frontend/
│   ├── pages/index.html
│   └── static/{css,js,media}/   # js split into api.js / ui.js / main.js
├── data/                        # Runtime data (git-ignored)
├── tests/                       # pytest
├── requirements.txt / requirements-dev.txt
├── CLAUDE.md
└── README.md
```

## Adding SQLite later

1. Create `app/repositories/sqlite_repository.py` implementing `TodoRepository`.
2. Add a `"sqlite"` branch in `app/repositories/factory.py`.
3. Run with `STORAGE_BACKEND=sqlite` (path via `SQLITE_PATH`).

Routes and services need no changes.

## Getting Started

### Prerequisites

- Python 3.9+ (developed on 3.13)

### Installation

```bash
git clone git@github.com:YogendraShastri/Todo_Application_using_claude_practice.git
cd Todo_Application_using_claude_practice

python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run

```bash
python run.py
```

Open <http://127.0.0.1:8000>. The server runs with hot reload, so edits to `app/` and `frontend/` are picked up automatically.

## API Reference

| Method | Endpoint               | Description             | Success | Errors |
|--------|------------------------|-------------------------|---------|--------|
| GET    | `/api/todos`           | List all todos          | 200     | —      |
| POST   | `/api/todos`           | Create a todo           | 200     | 400 empty title |
| PATCH  | `/api/todos/{todo_id}` | Toggle done status      | 200     | 404 not found |
| DELETE | `/api/todos/{todo_id}` | Delete a todo           | 200     | 404 not found |
| GET    | `/`                    | Serve the web app       | 200     | —      |

**Todo object**

```json
{ "id": "3f2b8c1e-...", "title": "Buy groceries", "done": false }
```

**Example**

```bash
curl -X POST http://127.0.0.1:8000/api/todos \
  -H "Content-Type: application/json" \
  -d '{"title": "Buy groceries"}'
```

FastAPI also exposes interactive docs at <http://127.0.0.1:8000/docs>.

## Design Notes

- **Storage:** todos are read from and written to `data/todos.json` on every request. Simple and transparent, but there is no locking, so it assumes a single user.
- **Frontend sync:** the UI calls `fetchTodos()` after every mutation to stay consistent with the server.
- **No build step:** plain HTML/CSS/JS served as static files.

## Possible Improvements

- Add a SQLite repository (see above) for concurrency safety
- Edit task titles; due dates and priorities
- User accounts and authentication
- Docker setup

## License

This is a personal learning project. No license has been specified.
