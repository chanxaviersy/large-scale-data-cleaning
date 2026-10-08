<!-- 徽章 -->
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![CI](https://github.com/chanxaviersy/large-scale-data-cleaning/actions/workflows/test.yml/badge.svg)](https://github.com/chanxaviersy/large-scale-data-cleaning/actions)
[![Last Commit](https://img.shields.io/github/last-commit/chanxaviersy/large-scale-data-cleaning)](https://github.com/chanxaviersy/large-scale-data-cleaning)

---

# 大规模用户行为数据清洗管道

> 千万级记录的端到端数据清洗与质量提升流水线

本项目源自简历中 Insta360（2023.7 - 2024.8）的 Data Analyst 岗位经历。
原项目处理 10M+ 条用户/产品行为数据，设计 Python 数据清洗管道，
将处理时间减少 40%，并构建 SQL 数据库 + Tableau 仪表板。
本仓库将其抽象为可独立运行的工程化版本，重点展示**性能优化与质量保证**。

## 项目目标

- 处理千万级（10M+）结构化行为数据
- 多阶段清洗：去重 → 缺失值 → 异常值 → 类型转换 → 业务规则
- 性能优化：矢量化 + 并行化 + 分块处理
- 严格的数据质量指标与可视化报告

## 技术栈

- **数据**：Python (Pandas, NumPy)
- **并行**：multiprocessing / concurrent.futures
- **性能分析**：line_profiler / cProfile
- **可视化**：Matplotlib
- **数据库**：SQLite（生产可换 PostgreSQL）

## 目录结构

```
05-large-scale-data-cleaning/
├── README.md
├── requirements.txt
├── data/                          # 原始数据（运行时生成）
├── src/
│   ├── generate_raw_data.py       # 生成模拟原始数据（含各种"脏"问题）
│   ├── cleaner.py                 # 单阶段清洗逻辑（多种规则）
│   ├── pipeline.py                # 主管道（多阶段编排）
│   ├── quality.py                 # 数据质量评估
│   ├── parallel.py                # 并行处理模块
│   └── storage.py                 # 数据库存储
├── benchmarks/
│   └── benchmark.py               # 性能基准（单线程 vs 多线程 vs 向量化）
├── outputs/                       # 报告与图表输出
└── run_demo.py                    # 一键 Demo
```

## 快速开始

```bash
pip install -r requirements.txt
python run_demo.py
```

Demo 会：

1. 生成 100 万条带"脏数据"的模拟原始数据
2. 运行完整清洗管道（多阶段）
3. 输出数据质量报告 + 可视化图表
4. 写入 SQLite 数据库
5. 自动 benchmark：单线程 vs 并行化对比

## 清洗阶段

```
原始数据
   ↓
[阶段 1] 去重 → 完全重复 + 模糊重复（基于关键字段）
   ↓
[阶段 2] 缺失值处理 → 删除 / 填充 / 标记
   ↓
[阶段 3] 异常值处理 → IQR / Z-score / 业务规则
   ↓
[阶段 4] 类型转换 → 数值化、日期化
   ↓
[阶段 5] 业务规则 → 时间区间、状态流转合法性
   ↓
清洗后数据
```

## 性能优化策略

| 策略                    | 适用场景              | 提升效果           |
|------------------------|---------------------|------------------|
| **矢量化**             | 数值/字符串运算       | 10-100×          |
| **分块处理 (chunked)**  | 单文件超出内存         | 内存可控           |
| **多进程 (multiprocessing)** | CPU 密集型任务    | 2-8×（视核数）   |
| **Polars 替代 Pandas** | 真正大规模数据        | 5-10×            |
| **Dask 分布式**        | > 100M 条数据        | 线性扩展          |

## 数据质量指标

每个阶段都计算并对比：

- **完整性**：非空字段占比
- **唯一性**：主键重复率
- **有效性**：业务规则通过率
- **一致性**：跨表关联正确率
- **准确性**：抽样人工核验

## 后续可扩展方向

- 接入真实数据源（Kafka / S3）
- 引入 schema 校验（Great Expectations）
- 用 Polars / Dask 改造为分布式版本
- 接入 dbt 做数据建模
- 接入 Airflow 做调度

## License

MIT