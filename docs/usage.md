# 详细使用指南

## 安装

```bash
git clone https://github.com/chanxaviersy/large-scale-data-cleaning.git
cd large-scale-data-cleaning
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 运行

### 一键 Demo

```bash
python run_demo.py
```

流程：
1. 生成 1000 万行模拟数据
2. 跑完整清洗管道
3. 输出质量报告
4. 写入 SQLite

### 分步运行

```bash
# 仅生成数据
python src/generate_raw_data.py

# 仅跑清洗（用已有数据）
python src/cleaner.py

# 跑完整管道
python src/pipeline.py
```

### 跑测试

```bash
pytest tests/ -v
```

## 自定义

### 修改数据量

编辑 `src/generate_raw_data.py`：

```python
N_USERS = 100_000  # 改为你想要的数量
N_EVENTS = 10_000_000
```

### 调整清洗参数

```python
from src.cleaner import clean_full_pipeline

df = pd.read_parquet("data/raw.parquet")
df_clean = clean_full_pipeline(df)
```

或单独调用各阶段：

```python
from src.cleaner import remove_duplicates, handle_missing, handle_outliers

df = remove_duplicates(df)
df = handle_missing(df, value_fill_strategy="mean")
df = handle_outliers(df, method="range", min_valid=0, max_valid=10_000)
```

## 并行处理

```python
from src.parallel import parallel_process

# 处理 1 千万行，chunk=100 万，4 个 worker
results = parallel_process(n_total=10_000_000, chunk_size=1_000_000, n_workers=4)
```

## 常见问题

**Q: 内存不够？**
A: 改用分块处理（`pd.read_parquet` + `iterator=True`）或换 Dask。

**Q: 清洗后行数骤减？**
A: 检查 `apply_business_rules` 的白名单 / 时间范围。

**Q: SQLite 太大？**
A: 换 DuckDB（列式，压缩比高）或 PostgreSQL。

## 扩展

- **流式处理**：换 PySpark / Flink
- **质量监控**：接 Great Expectations
- **DAG 调度**：用 Airflow / Prefect
