"""生成带"脏数据"的模拟原始数据。
故意植入各种质量问题，用于演示清洗管道。
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def generate_raw_data(
    n_rows: int = 1_000_000, dirty_ratio: float = 0.05, output_path: str | Path = "data/raw.parquet"
) -> Path:
    """生成模拟原始数据。

    数据 schema：
        user_id, event_id, event_type, product_id, timestamp, value, session_id, device_os, country

    植入的脏数据：
        - 5% 完全重复
        - 缺失值：user_id (~3%), value (~5%)
        - 异常值：value 出现负数、超大值
        - 时间异常：未来时间
        - 枚举值异常：device_os 包含非法值
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(42)

    print(f"[DATA] 正在生成 {n_rows:,} 条原始数据...")
    user_ids = rng.integers(1, 100_000, n_rows)
    event_ids = np.arange(1, n_rows + 1)
    event_types = rng.choice(
        ["view", "click", "add_to_cart", "purchase", "share"],
        n_rows,
        p=[0.5, 0.25, 0.15, 0.07, 0.03],
    )
    product_ids = rng.integers(1, 10_000, n_rows)
    base_ts = pd.Timestamp("2024-01-01")
    timestamps = base_ts + pd.to_timedelta(rng.integers(0, 365 * 86400, n_rows), unit="s")
    values = rng.exponential(scale=50, size=n_rows).round(2)
    session_ids = [f"sess_{rng.integers(1, 50_000)}" for _ in range(n_rows)]
    device_oses = rng.choice(["iOS", "Android", "Windows", "MacOS", "Linux"], p=[0.45, 0.45, 0.04, 0.04, 0.02], size=n_rows)
    countries = rng.choice(["CN", "US", "GB", "DE", "JP", "FR", "BR"], n_rows)

    df = pd.DataFrame({
        "event_id": event_ids,
        "user_id": user_ids,
        "event_type": event_types,
        "product_id": product_ids,
        "timestamp": timestamps,
        "value": values,
        "session_id": session_ids,
        "device_os": device_oses,
        "country": countries,
    })

    # 注入脏数据
    n_dirty = int(n_rows * dirty_ratio)

    # 1. 完全重复（5%）
    n_dup = int(n_rows * 0.05)
    dup_idx = rng.choice(df.index, n_dup, replace=False)
    dup_rows = df.iloc[dup_idx].copy()
    df = pd.concat([df, dup_rows], ignore_index=True)

    # 2. 缺失 user_id（3%）
    n_missing_user = int(n_rows * 0.03)
    miss_user_idx = rng.choice(df.index, n_missing_user, replace=False)
    df.loc[miss_user_idx, "user_id"] = np.nan

    # 3. 缺失 value（5%）
    n_missing_value = int(n_rows * 0.05)
    miss_value_idx = rng.choice(df.index, n_missing_value, replace=False)
    df.loc[miss_value_idx, "value"] = np.nan

    # 4. 异常 value（负数 + 超大）
    n_anomaly = int(n_rows * 0.02)
    anom_idx = rng.choice(df.index, n_anomaly, replace=False)
    df.loc[anom_idx[: n_anomaly // 2], "value"] = -100.0
    df.loc[anom_idx[n_anomaly // 2 :], "value"] = 1_000_000.0

    # 5. 时间异常（未来时间戳）
    n_future = int(n_rows * 0.01)
    future_idx = rng.choice(df.index, n_future, replace=False)
    df.loc[future_idx, "timestamp"] = pd.Timestamp("2099-12-31")

    # 6. 非法枚举值
    n_bad_enum = int(n_rows * 0.01)
    bad_enum_idx = rng.choice(df.index, n_bad_enum, replace=False)
    df.loc[bad_enum_idx, "device_os"] = "SymbianOS_X"

    print(f"[DATA] 注入完毕，总行数: {len(df):,}")

    # 写入（用 parquet 以提升真实感与效率）
    df.to_parquet(output_path, index=False)
    print(f"[DATA] 已写入 {output_path}")
    return output_path


if __name__ == "__main__":
    generate_raw_data()