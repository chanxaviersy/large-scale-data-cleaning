# 开发笔记

## 踩过的坑

### 1. 千万级数据内存爆炸

- **问题**：直接 `pd.read_parquet` 加载 1000 万行爆内存（> 8GB）
- **解决**：
  - 用 Dask 延迟加载
  - 或分块读 + 处理 + 写
  - 或直接用 SQLite / DuckDB

### 2. pandas `pd.np` 已弃用

- **问题**：`src/parallel.py` 中用了 `pd.np.random`（已弃用）
- **解决**：改 `np.random.default_rng`
- **代码**：`src/parallel.py:process_chunk`

### 3. 异常值 clip 边界错误

- **问题**：IQR 法可能让下限 < 0
- **解决**：clip 后取 `max(lower, min_valid)`
- **代码**：`src/cleaner.py:handle_outliers`

### 4. 时间类型转换失败

- **问题**：`pd.to_datetime` 遇到脏数据报错
- **解决**：`errors="coerce"` 然后 dropna
- **代码**：`src/cleaner.py:fix_types`

## 性能优化

### 内存优化

- **类型降级**：`int64` → `int32` / `int8`（节省 50%+）
- **category 化**：`event_type` 等低基数列转 `category`（节省 80%+）
- **chunk 处理**：`chunksize=1_000_000` 逐块处理

### 速度优化

- **多进程**：`ProcessPoolExecutor`（绕过 GIL）
- **numba**：热路径函数 `@jit`
- **polars**：替代 pandas，10x 速度

### IO 优化

- **Parquet** 比 CSV 快 10x，压缩比高 5x
- **分块写**：`to_parquet` 配合 `partition_cols`

## 数据质量框架

| 维度 | 检查 | 工具 |
|------|------|------|
| 完整性 | 必填字段非空 | pandas `.notna()` |
| 一致性 | 业务规则 | 自定义函数 |
| 准确性 | 范围 / 异常值 | IQR / zscore |
| 唯一性 | 主键唯一 | `.duplicated()` |
| 及时性 | 时间戳新鲜度 | 时间差计算 |

## 大数据演进

```
单机 Pandas
  → Dask (本地并行)
    → PySpark (集群)
      → Polars / DuckDB (现代单节点利器)
        → 云原生 (BigQuery / Snowflake)
```
