"""测试 storage.py"""
from __future__ import annotations

import sqlite3

import pandas as pd
import pytest


@pytest.fixture
def sample_clean_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4, 5],
            "value": [10.0, 20.0, 30.0, 40.0, 50.0],
            "timestamp": pd.to_datetime([
                "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"
            ]),
            "event_type": ["click", "view", "click", "purchase", "view"],
        }
    )


def test_save_to_sqlite_creates_db(tmp_path, sample_clean_df):
    """save_to_sqlite 应创建 SQLite 文件"""
    from storage import save_to_sqlite

    db_path = tmp_path / "test.db"
    save_to_sqlite(sample_clean_df, db_path)
    assert db_path.exists()


def test_save_to_sqlite_inserts_data(tmp_path, sample_clean_df):
    """save_to_sqlite 应能写入所有行"""
    from storage import save_to_sqlite

    db_path = tmp_path / "test.db"
    save_to_sqlite(sample_clean_df, db_path)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM events_clean")
        count = cur.fetchone()[0]
        assert count == 5


def test_save_to_sqlite_creates_indexes(tmp_path, sample_clean_df):
    """save_to_sqlite 应创建 user_id 和 timestamp 索引"""
    from storage import save_to_sqlite

    db_path = tmp_path / "test.db"
    save_to_sqlite(sample_clean_df, db_path)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='index'")
        indexes = [row[0] for row in cur.fetchall()]
        # 至少应有一个 user_id 索引和一个 timestamp 索引
        assert any("user" in idx for idx in indexes)
        assert any("ts" in idx for idx in indexes)


def test_get_summary_returns_dict(tmp_path, sample_clean_df):
    """get_summary 应返回包含 rows / unique_users 的字典"""
    from storage import get_summary, save_to_sqlite

    db_path = tmp_path / "test.db"
    save_to_sqlite(sample_clean_df, db_path)
    summary = get_summary(db_path)

    assert isinstance(summary, dict)
    assert "rows" in summary
    assert "unique_users" in summary
    assert summary["rows"] == 5
    assert summary["unique_users"] == 5


def test_save_to_sqlite_overwrites(tmp_path, sample_clean_df):
    """save_to_sqlite 应覆盖已有表"""
    from storage import save_to_sqlite

    db_path = tmp_path / "test.db"
    save_to_sqlite(sample_clean_df, db_path)
    # 第二次调用应覆盖
    save_to_sqlite(sample_clean_df.head(2), db_path)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM events_clean")
        count = cur.fetchone()[0]
        assert count == 2
