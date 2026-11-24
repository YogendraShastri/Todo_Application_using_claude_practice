# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
source venv/bin/activate          # venv is git-ignored; create with python3 -m venv venv
pip install -r requirements-dev.txt  # or requirements.txt; fastapi, uvicorn (unpinned)
python -m pytest                  # tests use a temp JSON file via dependency override
python run.py                     # dev server on http://127.0.0.1:8000, hot reload on
```

- Interactive API docs: http://127.0.0.1:8000/docs

## Architecture

Layered FastAPI backend (`app/`) plus a no-build vanilla JS frontend (`frontend/`).

- `app/main.py` — `create_app()`; `run.py` starts uvicorn.
- `app/api/routes/` — `todos.py` (REST, maps service errors to HTTP) and `pages.py` (`GET /`). `app/api/deps.py` builds the cached `TodoService`.
- `app/services/todo_service.py` — business rules (strip/empty-title, not-found).
- `app/repositories/` — `TodoRepository` interface, `JsonTodoRepository`, and `factory.py` choosing by `STORAGE_BACKEND`. SQLite = new repository + factory branch.
- `app/core/config.py` — settings/paths (`DATA_FILE`, `STORAGE_BACKEND`, `SQLITE_PATH`).
- `frontend/pages/index.html`, `frontend/static/{css,js,media}`; JS is ES modules (`api.js`, `ui.js`, `main.js`). Mockup JPGs are in `static/media/mockups` (not used by the app).
- `data/` — runtime data (git-ignored except `.gitkeep`). Todos are `{id: uuid4 str, title, done}`.

Routes: `GET/POST /api/todos`, `PATCH /api/todos/{id}` (toggles `done`; no body), `DELETE /api/todos/{id}`.

## Design notes that aren't obvious from a single file

- **Persistence is read-modify-write on every request** in the JSON repository (re-reads and rewrites the whole file). Writes are atomic (temp file + replace) but there is no locking, so concurrent requests can lose updates. Single-user assumption.
- **Responses use the `Todo` Pydantic `response_model`**; `TodoCreate` validates input.
- **Empty-title validation is duplicated**: the frontend skips blank input silently, and the service raises `EmptyTitleError` (400) after `.strip()`. Keep both in sync.
- **Frontend sync model**: every mutation (in `main.js`) calls `refresh()`, which refetches and re-renders the list via `renderTodos()`. Responses are not checked (`res.ok`), so API errors are currently invisible in the UI.
- Task text is rendered with `textContent` (safe); only the static trash-icon SVG uses `innerHTML`. Preserve that when changing rendering.
