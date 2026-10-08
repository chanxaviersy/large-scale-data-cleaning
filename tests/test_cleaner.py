"""测试 cleaner.py"""
from __future__ import annotations

import numpy as np
import pandas as pd
import pytest


def test_remove_duplicates_no_dup(clean_data):
    """无重复时应保持原样"""
    from cleaner import remove_duplicates

    result = remove_duplicates(clean_data)
    assert len(result) == len(clean_data)


def test_remove_duplicates_with_dup(sample_dirty_data):
    """有重复时应当去重"""
    from cleaner import remove_duplicates

    before = len(sample_dirty_data)
    result = remove_duplicates(sample_dirty_data)
    # (1, 10, '2024-01-01', ...) 出现 2 次
    assert len(result) < before


def test_remove_duplicates_subset(sample_dirty_data):
    """按指定列去重"""
    from cleaner import remove_duplicates

    result = remove_duplicates(sample_dirty_data, subset=["user_id"])
    # user_id=1 出现 2 次，去重后应只剩 1 个
    assert result["user_id"].duplicated().sum() == 0


def test_handle_missing_drops_null_user_id(sample_dirty_data):
    """user_id 为空的行应被删除"""
    from cleaner import handle_missing

    result = handle_missing(sample_dirty_data)
    assert result["user_id"].notna().all()


def test_handle_missing_fills_value_median(sample_dirty_data):
    """value 缺失应被中位数填充"""
    from cleaner import handle_missing

    result = handle_missing(sample_dirty_data, value_fill_strategy="median")
    assert result["value"].notna().all()
    # 填充值 = 删除 user_id 空后剩余的 value 中位数
    non_null = sample_dirty_data[sample_dirty_data["user_id"].notna()]["value"].dropna()
    expected_median = non_null.median()
    # 第 2 行（index=2）的 value 原本是 NaN，现在应为中位数
    assert result["value"].iloc[1] == expected_median


def test_handle_missing_fills_value_mean(sample_dirty_data):
    """value 缺失应用均值填充（指定 mean 策略）"""
    from cleaner import handle_missing

    result = handle_missing(sample_dirty_data, value_fill_strategy="mean")
    assert result["value"].notna().all()


def test_handle_outliers_iqr_clip(sample_dirty_data):
    """IQR 法应 clip 极端值"""
    from cleaner import handle_outliers

    result = handle_outliers(sample_dirty_data, method="iqr")
    # 原本 1,000,000 的异常值应被 clip
    assert result["value"].max() < 1_000_000


def test_handle_outliers_range_clip(sample_dirty_data):
    """range 法应 clip 到 [min, max]"""
    from cleaner import handle_outliers

    result = handle_outliers(sample_dirty_data, method="range", min_valid=0, max_valid=500)
    assert result["value"].max() <= 500
    assert result["value"].min() >= 0


def test_fix_types_user_id_int(sample_dirty_data):
    """user_id 应转为 int64"""
    from cleaner import fix_types

    result = fix_types(sample_dirty_data)
    assert result["user_id"].dtype == np.int64


def test_fix_types_timestamp_datetime(sample_dirty_data):
    """timestamp 应转为 datetime"""
    from cleaner import fix_types

    result = fix_types(sample_dirty_data)
    assert pd.api.types.is_datetime64_any_dtype(result["timestamp"])


def test_apply_business_rules_filters_invalid_os(sample_dirty_data):
    """device_os 不在白名单应被过滤"""
    from cleaner import apply_business_rules

    result = apply_business_rules(sample_dirty_data)
    # Symbian 不在默认白名单
    assert "Symbian" not in result["device_os"].values


def test_apply_business_rules_filters_old_timestamp(sample_dirty_data):
    """timestamp 太早应被过滤"""
    from cleaner import apply_business_rules

    result = apply_business_rules(sample_dirty_data)
    assert result["timestamp"].min() >= pd.Timestamp("2020-01-01")


def test_clean_full_pipeline_runs(sample_dirty_data):
    """完整 pipeline 应能跑通"""
    from cleaner import clean_full_pipeline

    result = clean_full_pipeline(sample_dirty_data)
    assert isinstance(result, pd.DataFrame)
    assert len(result) > 0
    # 最终数据应无缺失
    assert result["user_id"].notna().all()
    assert result["timestamp"].notna().all()
