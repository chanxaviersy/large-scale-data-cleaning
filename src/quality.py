"""数据质量评估。"""
from __future__ import annotations

import pandas as pd


def compute_quality_report(df: pd.DataFrame) -> dict[str, float]:
    """计算全表数据质量指标。"""
    n = len(df)
    return {
        "总行数": n,
        "user_id 完整率": float(df["user_id"].notna().mean()) if "user_id" in df.columns else 0.0,
        "value 完整率": float(df["value"].notna().mean()) if "value" in df.columns else 0.0,
        "timestamp 完整率": float(df["timestamp"].notna().mean()) if "timestamp" in df.columns else 0.0,
        "value 最小值": float(df["value"].min()) if "value" in df.columns else 0.0,
        "value 最大值": float(df["value"].max()) if "value" in df.columns else 0.0,
        "event_type 种类数": int(df["event_type"].nunique()) if "event_type" in df.columns else 0,
        "device_os 种类数": int(df["device_os"].nunique()) if "device_os" in df.columns else 0,
    }


def compare_quality(before: dict, after: dict) -> pd.DataFrame:
    """对比前后质量。"""
    rows = []
    for key in before:
        rows.append({
            "指标": key,
            "清洗前": before[key],
            "清洗后": after[key],
            "提升": (
                f"+{after[key] - before[key]:.4f}"
                if isinstance(before[key], (int, float))
                else "N/A"
            ),
        })
    return pd.DataFrame(rows)