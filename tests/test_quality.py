"""测试 quality.py"""
from __future__ import annotations

import numpy as np
import pandas as pd


def test_compute_quality_report_keys(clean_data):
    """应返回 8 个质量指标"""
    from quality import compute_quality_report

    report = compute_quality_report(clean_data)
    assert "总行数" in report
    assert "user_id 完整率" in report
    assert "value 完整率" in report
    assert "timestamp 完整率" in report
    assert "value 最小值" in report
    assert "value 最大值" in report
    assert "event_type 种类数" in report
    assert "device_os 种类数" in report


def test_compute_quality_report_clean_data(clean_data):
    """干净数据的完整率应为 1.0"""
    from quality import compute_quality_report

    report = compute_quality_report(clean_data)
    assert report["总行数"] == 5
    assert report["user_id 完整率"] == 1.0
    assert report["value 完整率"] == 1.0
    assert report["timestamp 完整率"] == 1.0


def test_compute_quality_report_dirty_data(sample_dirty_data):
    """脏数据的完整率应 < 1.0"""
    from quality import compute_quality_report

    report = compute_quality_report(sample_dirty_data)
    assert report["user_id 完整率"] < 1.0
    assert report["value 完整率"] < 1.0


def test_compare_quality_returns_dataframe(clean_data):
    """compare_quality 应返回对比 DataFrame"""
    from quality import compare_quality, compute_quality_report

    before = compute_quality_report(clean_data)
    after = compute_quality_report(clean_data)
    result = compare_quality(before, after)
    assert isinstance(result, pd.DataFrame)
    assert "指标" in result.columns
    assert "清洗前" in result.columns
    assert "清洗后" in result.columns
    assert "提升" in result.columns
    assert len(result) == len(before)


def test_compare_quality_shows_improvement(sample_dirty_data):
    """清洗后完整性应提升"""
    from quality import compare_quality, compute_quality_report
    from cleaner import clean_full_pipeline

    before = compute_quality_report(sample_dirty_data)
    after_df = clean_full_pipeline(sample_dirty_data)
    after = compute_quality_report(after_df)
    result = compare_quality(before, after)

    # 找到 user_id 完整率那一行
    row = result[result["指标"] == "user_id 完整率"].iloc[0]
    # 提升应为正数或为零
    assert row["提升"] in ["+0.0000"] or "+" in str(row["提升"])
