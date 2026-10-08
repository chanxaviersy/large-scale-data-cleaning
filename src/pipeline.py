"""主管道：编排完整流程。"""
from __future__ import annotations

import time
from pathlib import Path

import pandas as pd

from cleaner import clean_full_pipeline
from quality import compare_quality, compute_quality_report
from storage import get_summary, save_to_sqlite


PROJECT_ROOT = Path(__file__).resolve().parent.parent


def run_pipeline(
    raw_path: str | Path = "data/raw.parquet",
    output_db: str | Path = "data/events_clean.db",
) -> dict:
    """运行完整数据清洗管道。

    返回：包含耗时、质量指标、最终行数的报告
    """
    raw_path = Path(raw_path)
    output_db = Path(output_db)

    if not raw_path.exists():
        from generate_raw_data import generate_raw_data
        generate_raw_data(output_path=raw_path)

    # 1. 读取原始数据
    print("\n[PIPELINE] 读取原始数据...")
    t0 = time.time()
    df_raw = pd.read_parquet(raw_path)
    t_read = time.time() - t0
    print(f"  读取耗时: {t_read:.2f}s，共 {len(df_raw):,} 条")

    # 2. 评估原始数据质量
    print("\n[PIPELINE] 评估原始数据质量...")
    quality_before = compute_quality_report(df_raw)

    # 3. 清洗
    print("\n[PIPELINE] 执行清洗...")
    t0 = time.time()
    df_clean = clean_full_pipeline(df_raw)
    t_clean = time.time() - t0
    print(f"  清洗耗时: {t_clean:.2f}s")

    # 4. 评估清洗后质量
    quality_after = compute_quality_report(df_clean)
    quality_compare = compare_quality(quality_before, quality_after)

    # 5. 写入数据库
    print("\n[PIPELINE] 写入数据库...")
    save_to_sqlite(df_clean, output_db)

    # 6. 数据库摘要
    summary = get_summary(output_db)
    print(f"\n[PIPELINE] 最终入库: {summary}")

    # 7. 生成质量报告
    report = {
        "raw_rows": len(df_raw),
        "clean_rows": len(df_clean),
        "clean_ratio": len(df_clean) / len(df_raw),
        "read_seconds": t_read,
        "clean_seconds": t_clean,
        "rows_per_second": len(df_clean) / t_clean,
        "quality_compare": quality_compare,
        "db_summary": summary,
    }

    # 保存报告
    report_path = PROJECT_ROOT / "outputs" / "quality_report.csv"
    report["quality_compare"].to_csv(report_path, index=False, encoding="utf-8")
    print(f"\n[PIPELINE] ✅ 完成！报告: {report_path}")

    return report


if __name__ == "__main__":
    run_pipeline()