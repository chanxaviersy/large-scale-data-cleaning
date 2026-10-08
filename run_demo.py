"""一键运行 Demo：生成数据 → 清洗 → 写入数据库 → benchmark。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "benchmarks"))

from pipeline import run_pipeline  # noqa: E402
from benchmark import run_benchmark  # noqa: E402


def main() -> None:
    print("=" * 60)
    print("  大规模数据清洗管道 - 一键 Demo")
    print("=" * 60)

    # 1. 完整管道（生成 100 万条数据 + 清洗 + 入库）
    print("\n[DEMO] Part 1: 数据清洗管道")
    report = run_pipeline()
    print(f"\n  原始数据: {report['raw_rows']:,} 条")
    print(f"  清洗后:   {report['clean_rows']:,} 条")
    print(f"  保留率:   {report['clean_ratio']:.2%}")
    print(f"  清洗速度: {report['rows_per_second']:,.0f} 行/秒")

    # 2. 性能 benchmark
    print("\n[DEMO] Part 2: 性能基准对比")
    run_benchmark(n=100_000)

    print("\n[DEMO] ✅ 全部完成！")
    print("[DEMO] 输出：")
    print("  - data/events_clean.db          (清洗后数据库)")
    print("  - outputs/quality_report.csv     (数据质量报告)")
    print("  - outputs/benchmark.csv          (性能对比)")


if __name__ == "__main__":
    main()