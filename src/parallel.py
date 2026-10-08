"""并行处理模块（演示 chunked + multiprocessing 加速）。"""
from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

import pandas as pd


def process_chunk(args: tuple[int, int, str]) -> int:
    """处理单个数据块。"""
    chunk_id, n_rows, base_path = args
    rng = pd.np.random.default_rng(chunk_id)
    df = pd.DataFrame({
        "x": rng.normal(0, 1, n_rows),
        "y": rng.normal(0, 1, n_rows),
    })
    df["z"] = df["x"] ** 2 + df["y"] ** 2
    df["is_in_circle"] = df["z"] <= 1
    out = Path(base_path) / f"chunk_{chunk_id}.parquet"
    df.to_parquet(out, index=False)
    return chunk_id


def parallel_process(n_total: int, chunk_size: int, n_workers: int = 4) -> list[int]:
    """并行处理数据：分块 → 多进程。"""
    chunks = [(i, chunk_size, "/tmp") for i in range(n_total // chunk_size)]
    results = []
    with ProcessPoolExecutor(max_workers=n_workers) as executor:
        futures = {executor.submit(process_chunk, c): c for c in chunks}
        for future in as_completed(futures):
            results.append(future.result())
    return results