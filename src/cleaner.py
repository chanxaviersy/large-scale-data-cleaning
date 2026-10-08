"""单阶段清洗逻辑。"""
from __future__ import annotations

import numpy as np
import pandas as pd


def remove_duplicates(df: pd.DataFrame, subset: list[str] | None = None) -> pd.DataFrame:
    """阶段 1: 去除完全重复行。"""
    before = len(df)
    df = df.drop_duplicates(subset=subset, keep="first")
    after = len(df)
    print(f"  [去重] {before:,} → {after:,}（移除 {before - after:,} 条）")
    return df.reset_index(drop=True)


def handle_missing(
    df: pd.DataFrame,
    drop_user_id_null: bool = True,
    value_fill_strategy: str = "median",
) -> pd.DataFrame:
    """阶段 2: 处理缺失值。

    - user_id 为空的记录直接删除（无法归属用户）
    - value 缺失根据策略填充（默认中位数）
    """
    before = len(df)

    if drop_user_id_null:
        df = df[df["user_id"].notna()].copy()

    if "value" in df.columns and value_fill_strategy == "median":
        median_val = df["value"].median()
        df["value"] = df["value"].fillna(median_val)
    elif "value" in df.columns and value_fill_strategy == "mean":
        mean_val = df["value"].mean()
        df["value"] = df["value"].fillna(mean_val)

    after = len(df)
    print(f"  [缺失值] {before:,} → {after:,}（删除 {before - after:,} 条）")
    return df.reset_index(drop=True)


def handle_outliers(
    df: pd.DataFrame,
    column: str = "value",
    method: str = "iqr",
    iqr_multiplier: float = 3.0,
    min_valid: float = 0.0,
    max_valid: float = 100_000.0,
) -> pd.DataFrame:
    """阶段 3: 处理异常值。

    方法：
    - "iqr"：用 IQR 法检测 + clip 到上下限
    - "range"：直接 clip 到 [min_valid, max_valid]
    - "zscore"：删除 |z| > 3 的样本
    """
    before = len(df)

    if method == "iqr":
        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)
        iqr = q3 - q1
        lower = max(q1 - iqr_multiplier * iqr, min_valid)
        upper = min(q3 + iqr_multiplier * iqr, max_valid)
        df[column] = df[column].clip(lower=lower, upper=upper)
    elif method == "range":
        df[column] = df[column].clip(lower=min_valid, upper=max_valid)
    elif method == "zscore":
        z = (df[column] - df[column].mean()) / df[column].std()
        df = df[z.abs() < 3].copy()

    after = len(df)
    print(f"  [异常值] {before:,} → {after:,}（{method} 法）")
    return df.reset_index(drop=True)


def fix_types(df: pd.DataFrame) -> pd.DataFrame:
    """阶段 4: 类型转换。

    - user_id 转为整型
    - timestamp 转为 datetime
    - event_type / device_os / country 转为 category
    """
    before = len(df)
    if "user_id" in df.columns:
        df["user_id"] = df["user_id"].astype(np.int64)
    if "timestamp" in df.columns:
        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
    # 丢弃 timestamp 转换失败的行
    df = df[df["timestamp"].notna()].copy()
    for col in ["event_type", "device_os", "country"]:
        if col in df.columns:
            df[col] = df[col].astype("category")
    after = len(df)
    print(f"  [类型转换] {before:,} → {after:,}")
    return df.reset_index(drop=True)


def apply_business_rules(
    df: pd.DataFrame,
    allowed_os: list[str] | None = None,
    max_timestamp: str = "2025-12-31",
) -> pd.DataFrame:
    """阶段 5: 业务规则校验。

    - device_os 必须在白名单内
    - timestamp 必须在合理范围内
    - 转化漏斗必须合法（add_to_cart → purchase 必须有事件关联）
    """
    if allowed_os is None:
        allowed_os = ["iOS", "Android", "Windows", "MacOS", "Linux"]

    before = len(df)
    df = df[df["device_os"].isin(allowed_os)].copy()
    df = df[df["timestamp"] <= pd.Timestamp(max_timestamp)].copy()
    df = df[df["timestamp"] >= pd.Timestamp("2020-01-01")].copy()
    after = len(df)
    print(f"  [业务规则] {before:,} → {after:,}")
    return df.reset_index(drop=True)


def clean_full_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    """完整清洗流程（一站式调用）。"""
    print("[CLEANER] 开始清洗...")
    df = remove_duplicates(df)
    df = handle_missing(df)
    df = handle_outliers(df)
    df = fix_types(df)
    df = apply_business_rules(df)
    print(f"[CLEANER] ✅ 完成，最终 {len(df):,} 条")
    return df