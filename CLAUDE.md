# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the Application

```bash
# Activate virtual environment (if not already active)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start the development server (runs on http://127.0.0.1:8000)
python main.py
```

The server runs with hot-reload enabled—changes to `main.py`, `static/app.js`, or `static/index.html` trigger automatic reloads.

## Architecture Overview

This is a simple full-stack todo application:

- **Backend**: FastAPI REST API in `main.py`
  - REST endpoints under `/api/todos` for CRUD operations
  - Static file serving for the frontend
  - Single-page app index at `/`
  
- **Frontend**: HTML + vanilla JavaScript in `static/`
  - `index.html`: Markup with Bootstrap styling
  - `app.js`: Handles UI rendering and API calls
  
- **Data Storage**: JSON file (`todos.json`) persisted to disk
  - No database; todos are loaded/saved as a JSON array
  - Each todo has `id` (UUID), `title` (string), and `done` (boolean)

## API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/todos` | List all todos |
| POST | `/api/todos` | Create a new todo |
| PATCH | `/api/todos/{todo_id}` | Toggle todo done status |
| DELETE | `/api/todos/{todo_id}` | Delete a todo |
| GET | `/` | Serve index.html |

## Key Design Notes

- **Validation**: Empty titles are rejected (400) at creation time in both frontend and backend
- **Concurrency**: No locking mechanism; assumes single user. For multi-user scenarios, would need database and proper concurrency handling
- **Frontend data fetching**: `fetchTodos()` is called after every mutation to keep UI in sync
