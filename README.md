<!-- ============= 顶部徽章 ============= -->
<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Pandas-2.0%2B-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas"/>
  <img src="https://img.shields.io/badge/NumPy-1.24%2B-013243?style=for-the-badge&logo=numpy&logoColor=white" alt="NumPy"/>
  <img src="https://img.shields.io/badge/License-MIT-22C55E?style=for-the-badge" alt="License"/>
</p>

<p align="center">
  <a href="https://github.com/chanxaviersy/large-scale-data-cleaning/actions/workflows/test.yml">
    <img src="https://img.shields.io/github/actions/workflow/status/chanxaviersy/large-scale-data-cleaning/test.yml?label=CI&style=flat-square" alt="CI"/>
  </a>
  <a href="https://github.com/chanxaviersy/large-scale-data-cleaning">
    <img src="https://img.shields.io/github/last-commit/chanxaviersy/large-scale-data-cleaning?style=flat-square" alt="Last Commit"/>
  </a>
  <a href="https://github.com/chanxaviersy/large-scale-data-cleaning/stargazers">
    <img src="https://img.shields.io/github/stars/chanxaviersy/large-scale-data-cleaning?style=flat-square" alt="Stars"/>
  </a>
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen?style=flat-square" alt="PRs Welcome"/>
</p>

<!-- ============= 标题区 ============= -->
<br/>
<div align="center">

# 🧹 大规模用户行为数据清洗管道

### 千万级记录的端到端数据清洗与质量提升流水线

[🚀 快速开始](#-快速开始) · [📖 文档](docs/architecture.md) · [🐛 报告 Bug](https://github.com/chanxaviersy/large-scale-data-cleaning/issues) · [💡 提出新特性](https://github.com/chanxaviersy/large-scale-data-cleaning/issues)

</div>

<!-- ============= 项目亮点卡片 ============= -->
<p align="center">
  <table>
    <tr>
      <td align="center" width="200">
        <h3>📊</h3>
        <b>1000 万 + 行</b><br/>
        <sub><code>端到端处理</code></sub>
      </td>
      <td align="center" width="200">
        <h3>⚡</h3>
        <b>5 阶段清洗</b><br/>
        <sub><code>去重/缺失/异常/类型/规则</code></sub>
      </td>
      <td align="center" width="200">
        <h3>🚀</h3>
        <b>性能优化 40%+</b><br/>
        <sub><code>矢量化 + 多进程</code></sub>
      </td>
      <td align="center" width="200">
        <h3>✅</h3>
        <b>质量保证</b><br/>
        <sub><code>完整/唯一/有效/一致</code></sub>
      </td>
    </tr>
  </table>
</p>

---

<!-- ============= 目录 ============= -->
## 📑 目录

- [🎯 项目目标](#-项目目标)
- [🛠 技术栈](#-技术栈)
- [📂 目录结构](#-目录结构)
- [🚀 快速开始](#-快速开始)
- [🔄 清洗阶段](#-清洗阶段)
- [⚡ 性能优化策略](#-性能优化策略)
- [📊 数据质量指标](#-数据质量指标)
- [🚀 后续可扩展方向](#-后续可扩展方向)
- [📚 更多文档](#-更多文档)
- [📄 License](#-license)

---

## 🎯 项目目标

- 处理千万级（10M+）结构化行为数据
- 多阶段清洗：去重 → 缺失值 → 异常值 → 类型转换 → 业务规则
- 性能优化：矢量化 + 并行化 + 分块处理
- 严格的数据质量指标与可视化报告

> 本项目源自简历中 Insta360（2023.7 - 2024.8）的 Data Analyst 岗位经历。原项目处理 10M+ 条用户/产品行为数据，设计 Python 数据清洗管道，将处理时间减少 40%，并构建 SQL 数据库 + Tableau 仪表板。本仓库将其抽象为可独立运行的工程化版本，重点展示**性能优化与质量保证**。

---

## 🛠 技术栈

<p align="center">
  <img src="https://skillicons.dev/icons?i=python,pandas,numpy,sqlite,git,github,vscode" alt="Tech Stack"/>
</p>

| 类别       | 技术                                       |
| ---------- | ------------------------------------------ |
| **数据**   | Python（Pandas, NumPy）                    |
| **并行**   | multiprocessing / concurrent.futures       |
| **性能分析** | line_profiler / cProfile                 |
| **可视化** | Matplotlib                                  |
| **数据库** | SQLite（生产可换 PostgreSQL）              |

---

## 📂 目录结构

```
05-large-scale-data-cleaning/
├── 📄 README.md
├── 📋 requirements.txt
├── 📂 data/                          # 原始数据（运行时生成）
├── 🐍 src/
│   ├── generate_raw_data.py          # 生成模拟原始数据（含各种"脏"问题）
│   ├── cleaner.py                    # 单阶段清洗逻辑（多种规则）
│   ├── pipeline.py                   # 主管道（多阶段编排）
│   ├── quality.py                    # 数据质量评估
│   ├── parallel.py                   # 并行处理模块
│   └── storage.py                    # 数据库存储
├── 📂 benchmarks/
│   └── benchmark.py                  # 性能基准（单线程 vs 多线程 vs 向量化）
├── 📂 outputs/                       # 报告与图表输出
├── 🧪 tests/                         # 单元测试
├── 📚 docs/                          # 详细文档
│   ├── architecture.md
│   ├── usage.md
│   └── dev-notes.md
└── 🎬 run_demo.py                    # 一键 Demo
```

---

## 🚀 快速开始

### 安装

```bash
git clone https://github.com/chanxaviersy/large-scale-data-cleaning.git
cd large-scale-data-cleaning
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 运行 Demo

```bash
python run_demo.py
```

Demo 会：

1. ✅ 生成 1000 万条带"脏数据"的模拟原始数据
2. ✅ 运行完整清洗管道（多阶段）
3. ✅ 输出数据质量报告 + 可视化图表
4. ✅ 写入 SQLite 数据库
5. ✅ 自动 benchmark：单线程 vs 并行化对比

### 跑测试

```bash
pytest tests/ -v
```

---

## 🔄 清洗阶段

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

| 阶段 | 函数                     | 输入                  | 输出             |
| ---- | ------------------------ | --------------------- | ---------------- |
| 1    | `remove_duplicates`      | 原始 DataFrame        | 去重后 DataFrame |
| 2    | `handle_missing`         | 必填字段非空          | 缺失值填充       |
| 3    | `handle_outliers`        | 数值列                | 异常值 clip/删除 |
| 4    | `fix_types`              | 字符串日期/类型       | 类型标准化       |
| 5    | `apply_business_rules`   | 业务白名单            | 合规 DataFrame   |

---

## ⚡ 性能优化策略

| 策略                          | 适用场景              | 提升效果           |
| ----------------------------- | --------------------- | ------------------ |
| **矢量化**                    | 数值/字符串运算       | 10-100×            |
| **分块处理 (chunked)**        | 单文件超出内存         | 内存可控           |
| **多进程 (multiprocessing)**  | CPU 密集型任务        | 2-8×（视核数）     |
| **Polars 替代 Pandas**        | 真正大规模数据        | 5-10×              |
| **Dask 分布式**               | > 100M 条数据        | 线性扩展           |

### 📸 性能对比图

> 截图待补充：运行 `benchmarks/benchmark.py` 后会生成对比图，保存到 [`assets/`](assets/)。

<details>
<summary>📊 点击展开：预期生成的图表</summary>

- `quality_report.csv` — 清洗前后质量对比
- `cleaning_performance.png` — 耗时 / 加速比
- `db_summary.json` — 入库摘要

</details>

---

## 📊 数据质量指标

每个阶段都计算并对比：

- ✅ **完整性**：非空字段占比
- ✅ **唯一性**：主键重复率
- ✅ **有效性**：业务规则通过率
- ✅ **一致性**：跨表关联正确率
- ✅ **准确性**：抽样人工核验

---

## 🚀 后续可扩展方向

- 接入真实数据源（Kafka / S3）
- 引入 schema 校验（Great Expectations）
- 用 Polars / Dask 改造为分布式版本
- 接入 dbt 做数据建模
- 接入 Airflow 做调度

---

## 📚 更多文档

| 文档 | 说明 |
|------|------|
| [📐 项目架构](docs/architecture.md) | 整体设计、模块关系、数据流 |
| [📖 使用指南](docs/usage.md) | 详细安装、配置、自定义 |
| [🔧 开发笔记](docs/dev-notes.md) | 踩过的坑、性能优化、大数据演进 |
| [📝 CHANGELOG](CHANGELOG.md) | 版本变更记录 |
| [🤝 CONTRIBUTING](CONTRIBUTING.md) | 如何参与贡献 |

---

## 📄 License

本项目基于 [MIT](LICENSE) 协议开源。

---

<div align="center">

**[⬆ 回到顶部](#-大规模用户行为数据清洗管道)**

Made with ❤️ by [Xavier Chen](https://github.com/chanxaviersy)

</div>
