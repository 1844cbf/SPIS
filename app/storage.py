import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from threading import Lock

from app.schemas import TaskRecord, TaskStatus


class TaskStore:
    def __init__(self, db_path: str) -> None:
        self.db_path = db_path
        self._lock = Lock()
        Path(db_path).parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    task_id TEXT PRIMARY KEY,
                    payload TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
                """
            )

    def create(self, task: TaskRecord) -> TaskRecord:
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                INSERT INTO tasks
                    (task_id, payload, status, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    task.task_id,
                    task.model_dump_json(),
                    task.status.value,
                    task.created_at.isoformat(),
                    task.updated_at.isoformat(),
                ),
            )
        return task

    def update(self, task: TaskRecord, status: TaskStatus | None = None) -> TaskRecord:
        if status is not None:
            task.status = status
        task.updated_at = datetime.now(UTC)
        with self._lock, self._connect() as conn:
            conn.execute(
                "UPDATE tasks SET payload = ?, status = ?, updated_at = ? WHERE task_id = ?",
                (
                    task.model_dump_json(),
                    task.status.value,
                    task.updated_at.isoformat(),
                    task.task_id,
                ),
            )
        return task

    def get(self, task_id: str) -> TaskRecord | None:
        with self._connect() as conn:
            row = conn.execute("SELECT payload FROM tasks WHERE task_id = ?", (task_id,)).fetchone()
        if row is None:
            return None
        return TaskRecord.model_validate(json.loads(row["payload"]))

    def list_recent(self, limit: int = 20) -> list[TaskRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT payload FROM tasks ORDER BY created_at DESC LIMIT ?",
                (limit,),
            ).fetchall()
        return [TaskRecord.model_validate(json.loads(row["payload"])) for row in rows]
