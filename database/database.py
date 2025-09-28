import sqlite3
from typing import Optional, List, Any
import logging

logger = logging.getLogger(__name__)

class Database:
    # Путь к файлу базы — можно переопределить в bot.py перед init_db()
    database_src: str = "database/database.db"

    @classmethod
    def connect(cls):
        conn = sqlite3.connect(cls.database_src, timeout=30)
        return conn

    @classmethod
    def init_db(cls) -> None:
        """Создать таблицы и индексы, если их нет."""
        with cls.connect() as conn:
            cur = conn.cursor()

            # Таблица пользователей
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_id INTEGER UNIQUE NOT NULL,
                    full_name TEXT DEFAULT '',
                    admin INTEGER DEFAULT 0
                );
                """
            )

            # Таблица заявок (анкеты) из визарда аудита
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_requests (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tg_id INTEGER,
                    chat_id INTEGER,
                    username TEXT DEFAULT '',
                    q1 TEXT DEFAULT '',
                    q2 TEXT DEFAULT '',
                    q3 TEXT DEFAULT '',
                    q4 TEXT DEFAULT '',
                    q5 TEXT DEFAULT '',
                    q6 TEXT DEFAULT '',
                    q7 TEXT DEFAULT '',
                    q8 TEXT DEFAULT '',
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                );
                """
            )

            # Индексы для быстрых выборок
            cur.execute("CREATE INDEX IF NOT EXISTS idx_users_tg_id ON users(tg_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_audit_tg_id ON audit_requests(tg_id);")
            cur.execute("CREATE INDEX IF NOT EXISTS idx_audit_created_at ON audit_requests(created_at);")

            conn.commit()


class User:
    class Object:
        def __init__(self, id, tg_id, full_name, admin):
            self.id = id
            self.tg_id = tg_id
            self.full_name = full_name
            self.admin = admin

        @staticmethod
        def from_list(lst):
            return User.Object(
                id = lst[0],
                tg_id = lst[1],
                full_name = lst[2],
                admin = lst[3]
            )

    @classmethod
    def get_by_tg_id(cls, tg_id: int) -> Optional[Any]:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE tg_id = ?", (tg_id,))
            row = cur.fetchone()
            return cls.Object.from_list(row) if row else None

    @staticmethod
    def create_if_not_exists(tg_id: int, full_name: str = "") -> None:
        """Создать пользователя если его ещё нет (не пробрасывает ошибку при дубликате)."""
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT OR IGNORE INTO users (tg_id, full_name) VALUES (?, ?)",
                (tg_id, full_name or ""),
            )
            conn.commit()

    @staticmethod
    def update_fullname(tg_id: int, full_name: str) -> None:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET full_name = ? WHERE tg_id = ?", (full_name, tg_id))
            conn.commit()

    @staticmethod
    def appoint_admin(tg_id: int) -> None:
        with Database.connect() as conn:
            cur = conn.cursor()
            # если пользователя нет — создаём и сразу назначаем
            cur.execute("INSERT OR IGNORE INTO users (tg_id, full_name) VALUES (?, '')", (tg_id,))
            cur.execute("UPDATE users SET admin = 1 WHERE tg_id = ?", (tg_id,))
            conn.commit()

    @staticmethod
    def remove_admin(tg_id: int) -> None:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("UPDATE users SET admin = 0 WHERE tg_id = ?", (tg_id,))
            conn.commit()

    @classmethod
    def get_all_admins(cls) -> List[Any]:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE admin = 1")
            rows = cur.fetchall()
            return [cls.Object.from_list(r) for r in rows]

    @classmethod
    def get_all_users(cls) -> List[Any]:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            return [cls.Object.from_list(r) for r in rows]

    @staticmethod
    def delete_by_tg_id(tg_id: int) -> None:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM users WHERE tg_id = ?", (tg_id,))
            conn.commit()


class AuditRequest:
    class Object:
        def __init__(self, id, tg_id, chat_id, username, q1, q2, q3, q4, q5, q6, q7, q8, created_at):
            self.id = id
            self.tg_id = tg_id
            self.chat_id = chat_id
            self.username = username
            self.q1 = q1
            self.q2 = q2
            self.q3 = q3
            self.q4 = q4
            self.q5 = q5
            self.q6 = q6
            self.q7 = q7
            self.q8 = q8
            self.created_at = created_at

        @staticmethod
        def from_list(lst):
            return AuditRequest.Object(
                id = lst[0],
                tg_id = lst[1],
                chat_id = lst[2],
                username = lst[3],
                q1 = lst[4],
                q2 = lst[5],
                q3 = lst[6],
                q4 = lst[7],
                q5 = lst[8],
                q6 = lst[9],
                q7 = lst[10],
                q8 = lst[11],
                created_at = lst[12]
            )

    @staticmethod
    def create(
        tg_id: Optional[int],
        chat_id: Optional[int],
        username: str,
        q1: str,
        q2: str,
        q3: str,
        q4: str,
        q5: str,
        q6: str,
        q7: str,
        q8: str,
    ) -> int:
        """
        Создать запись анкеты. Возвращает id созданной записи.
        """
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO audit_requests
                (tg_id, chat_id, username, q1,q2,q3,q4,q5,q6,q7,q8)
                VALUES (?, ?, ?, ?,?,?,?,?,?,?,?)
                """,
                (tg_id, chat_id, username or "", q1, q2, q3, q4, q5, q6, q7, q8),
            )
            conn.commit()
            return cur.lastrowid

    @classmethod
    def get_by_id(cls, req_id: int) -> Optional[Any]:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit_requests WHERE id = ?", (req_id,))
            row = cur.fetchone()
            return cls.Object.from_list(row) if row else None

    @classmethod
    def get_all(cls, limit: Optional[int] = None, offset: int = 0) -> List[Any]:
        with Database.connect() as conn:
            cur = conn.cursor()
            if limit:
                cur.execute(
                    "SELECT * FROM audit_requests ORDER BY created_at DESC LIMIT ? OFFSET ?",
                    (limit, offset),
                )
            else:
                cur.execute("SELECT * FROM audit_requests ORDER BY created_at DESC")
            rows = cur.fetchall()
            return [cls.Object.from_list(r) for r in rows]

    @classmethod
    def get_by_tg_id(cls, tg_id: int) -> List[Any]:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM audit_requests WHERE tg_id = ? ORDER BY created_at DESC", (tg_id,))
            rows = cur.fetchall()
            logger.info(rows)
            logger.info("text0")
            return [cls.Object.from_list(r) for r in rows]

    @staticmethod
    def delete(req_id: int) -> None:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM audit_requests WHERE id = ?", (req_id,))
            conn.commit()

    @staticmethod
    def count_all() -> int:
        with Database.connect() as conn:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) AS cnt FROM audit_requests")
            row = cur.fetchone()
            return int(row["cnt"]) if row else 0