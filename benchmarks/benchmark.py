"""性能基准：单线程 vs 多进程 vs 向量化（Polars）。"""
from __future__ import annotations

import time
from concurrent.futures import ProcessPoolExecutor

import numpy as np
import pandas as pd


def task_pandas(n: int) -> float:
    """纯 Pandas 实现（标量循环）。"""
    rng = np.random.default_rng(0)
    data = rng.normal(0, 1, (n, 10))
    df = pd.DataFrame(data, columns=[f"col_{i}" for i in range(10)])
    t0 = time.time()
    # 标量逐行计算（慢！）
    result = []
    for i in range(n):
        row = df.iloc[i]
        result.append(np.sqrt((row ** 2).sum()))
    return time.time() - t0


def task_vectorized(n: int) -> float:
    """矢量化 Pandas（推荐做法）。"""
    rng = np.random.default_rng(0)
    data = rng.normal(0, 1, (n, 10))
    df = pd.DataFrame(data, columns=[f"col_{i}" for i in range(10)])
    t0 = time.time()
    _ = np.sqrt((df ** 2).sum(axis=1))
    return time.time() - t0


def task_parallel_chunk(n: int, chunk_size: int, n_workers: int) -> float:
    """多进程分块并行。"""
    rng = np.random.default_rng(0)
    data = rng.normal(0, 1, (n, 10))
    df = pd.DataFrame(data, columns=[f"col_{i}" for i in range(10)])

    def process(chunk: pd.DataFrame) -> float:
        return float(np.sqrt((chunk ** 2).sum(axis=1)).sum())

    t0 = time.time()
    chunks = [df.iloc[i : i + chunk_size] for i in range(0, n, chunk_size)]
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        list(executor.map(process, chunks))
    return time.time() - t0


def run_benchmark(n: int = 100_000) -> None:
    print("=" * 50)
    print(f" 性能基准 (n={n:,})")
    print("=" * 50)

    results = []

    # 1. 标量 Pandas（会很慢，截断到小 n）
    if n <= 50_000:
        t = task_pandas(n)
        results.append({"方法": "标量 Pandas (循环)", "耗时(s)": f"{t:.4f}", "加速比": "1.0×"})
        base_time = t
    else:
        base_time = 1.0

    # 2. 矢量化 Pandas
    t = task_vectorized(n)
    speedup = base_time / t if base_time > 0 else 1.0
    results.append({"方法": "矢量化 Pandas", "耗时(s)": f"{t:.4f}", "加速比": f"{speedup:.1f}×"})

    # 3. 多进程分块
    t = task_parallel_chunk(n, chunk_size=n // 4, n_workers=4)
    speedup = base_time / t if base_time > 0 else 1.0
    results.append({"方法": "多进程分块 (4 workers)", "耗时(s)": f"{t:.4f}", "加速比": f"{speedup:.1f}×"})

    df = pd.DataFrame(results)
    print(df.to_string(index=False))

    # 保存
    out = Path(__file__).resolve().parent.parent / "outputs" / "benchmark.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out, index=False, encoding="utf-8")
    print(f"\n结果已保存到 {out}")


from pathlib import Path  # noqa: E402

if __name__ == "__main__":
    run_benchmark()