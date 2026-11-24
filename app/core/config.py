"""Application settings, overridable through environment variables."""
import os
from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


@dataclass(frozen=True)
class Settings:
    app_title: str = "Todo List"
    frontend_dir: Path = BASE_DIR / "frontend"
    # "json" today; add "sqlite" once SqliteTodoRepository exists.
    storage_backend: str = os.getenv("STORAGE_BACKEND", "json")
    data_file: Path = Path(os.getenv("DATA_FILE", BASE_DIR / "data" / "todos.json"))
    sqlite_url: str = os.getenv("SQLITE_PATH", str(BASE_DIR / "data" / "todos.db"))

    @property
    def static_dir(self) -> Path:
        return self.frontend_dir / "static"

    @property
    def pages_dir(self) -> Path:
        return self.frontend_dir / "pages"


def get_settings() -> Settings:
    return Settings()
