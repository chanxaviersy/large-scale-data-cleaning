"""pytest 共享 fixtures"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

# 把 src/ 加入路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def sample_dirty_data() -> pd.DataFrame:
    """示例脏数据（带重复、缺失、异常值、错误类型）"""
    return pd.DataFrame(
        {
            "user_id": [1, 2, 3, np.nan, 5, 1, 6, 7, 8, 9, 10, 11],
            "value": [10.0, 20.0, np.nan, 40.0, 50.0, 10.0, 1000000.0, 70.0, 80.0, 90.0, 100.0, 110.0],
            "timestamp": [
                "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04",
                "2024-01-05", "2024-01-01", "2024-01-07", "2024-01-08",
                "2024-01-09", "2024-01-10", "2024-01-11", "2024-01-12",
            ],
            "event_type": ["click", "view", "click", "purchase", "view",
                          "click", "click", "purchase", "view", "view", "click", "view"],
            "device_os": ["iOS", "Android", "iOS", "Windows", "Linux",
                          "iOS", "Symbian", "MacOS", "Android", "Windows", "iOS", "Android"],
            "country": ["CN", "US", "CN", "UK", "CN", "CN", "JP", "CN", "US", "UK", "CN", "CN"],
        }
    )


@pytest.fixture
def clean_data() -> pd.DataFrame:
    """完全干净的数据"""
    return pd.DataFrame(
        {
            "user_id": [1, 2, 3, 4, 5],
            "value": [10.0, 20.0, 30.0, 40.0, 50.0],
            "timestamp": pd.to_datetime([
                "2024-01-01", "2024-01-02", "2024-01-03", "2024-01-04", "2024-01-05"
            ]),
            "event_type": ["click", "view", "click", "purchase", "view"],
            "device_os": ["iOS", "Android", "iOS", "Windows", "Linux"],
            "country": ["CN", "US", "CN", "UK", "CN"],
        }
    )
