"""数据库存储：把清洗后的数据写入 SQLite（生产可换 PostgreSQL）。"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import pandas as pd


def save_to_sqlite(
    df: pd.DataFrame, db_path: str | Path, table_name: str = "events_clean"
) -> None:
    """把清洗后的 DataFrame 写入 SQLite。"""
    db_path = Path(db_path)
    db_path.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(db_path) as conn:
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        # 建索引
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_user ON {table_name}(user_id);")
        conn.execute(f"CREATE INDEX IF NOT EXISTS idx_{table_name}_ts ON {table_name}(timestamp);")
        conn.commit()
    print(f"[STORAGE] 已写入 {db_path}，共 {len(df):,} 条")


def get_summary(db_path: str | Path, table_name: str = "events_clean") -> dict:
    """从 SQLite 中获取摘要统计。"""
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT COUNT(*), COUNT(DISTINCT user_id) FROM {table_name}")
        n_rows, n_users = cur.fetchone()
    return {"rows": n_rows, "unique_users": n_users}