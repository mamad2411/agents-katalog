---
name: dataset-hub
version: 1.0.0
description: 学术数据集发现与推荐，深度集成 awesome-public-datasets，覆盖 30+ 学科分类
author: tzukwan
---

# Dataset Hub — 数据集发现技能

## 描述

Dataset Hub 是 tzukwan-cli 的数据集发现与管理中心。实时从 GitHub 仓库 [awesomedata/awesome-public-datasets](https://github.com/awesomedata/awesome-public-datasets) 获取最新数据集列表（超过 500 个精选数据集），结合 Kaggle、UCI Machine Learning Repository、Hugging Face Datasets 等多个来源，提供智能搜索、按学科筛选、研究场景匹配等功能。最终为每个推荐数据集生成标准化的 manifest 文件，用于后续实验流水线的自动化配置。

## 功能列表

- **实时拉取 awesome-public-datasets**：每次查询自动检查 GitHub 上的最新版本（带缓存，默认 6 小时刷新）
- **30+ 学科分类覆盖**：从农业到天文，从生物医学到社会科学全面覆盖
- **智能搜索**：支持关键词、类别标签、数据规模、许可证类型多维度筛选
- **研究场景匹配**：根据输入的研究主题自动推荐最适合的数据集组合
- **数据集详情展示**：大小、格式、许可证、引用次数、下载链接、相关论文
- **Manifest 生成**：为每个数据集生成标准化 JSON manifest，供实验技能自动配置
- **数据集健康检查**：验证链接有效性、许可证兼容性
- **引用信息**：自动生成数据集的学术引用格式（BibTeX）

## 命令

- `search`
- `recommend`
- `info`
- `manifest`
- `list`

## 支持的数据集分类（30+ 类）

| 类别标识 | 中文名称 | 示例数据集 |
|----------|----------|-----------|
| `agriculture` | 农业与食品 | USDA National Nutrient Database |
| `astronomy` | 天文与空间科学 | NASA Exoplanet Archive, Sloan Digital Sky Survey |
| `biology` | 生物学 | NCBI GenBank, UniProt |
| `climate` | 气候与天气 | NOAA Climate Data, ERA5 Reanalysis |
| `complex-networks` | 复杂网络 | Stanford SNAP Datasets |
| `computer-vision` | 计算机视觉 | ImageNet, COCO, Open Images |
| `data-challenges` | 数据竞赛 | Kaggle Datasets, DrivenData |
| `economics` | 经济学 | World Bank Open Data, FRED |
| `education` | 教育 | PISA, Common Core |
| `energy` | 能源 | UCI Electricity Load Diagrams |
| `finance` | 金融 | Yahoo Finance, Quandl |
| `gis` | 地理信息 | OpenStreetMap, Natural Earth |
| `government` | 政府开放数据 | Data.gov, EU Open Data Portal |
| `healthcare` | 医疗健康 | PhysioNet, MIMIC-III |
| `image-processing` | 图像处理 | MNIST, CIFAR-10/100, STL-10 |
| `machine-learning` | 机器学习基准 | UCI ML Repository, OpenML |
| `museums` | 博物馆与文化 | Metropolitan Museum Open Access |
| `natural-language` | 自然语言处理 | Common Crawl, Wikipedia Dumps |
| `neuroscience` | 神经科学 | Human Connectome Project, OpenNeuro |
| `physics` | 物理学 | CERN Open Data, LIGO Data |
| `psychology` | 心理学 | Open Psychometrics |
| `public-domains` | 公开领域综合 | Awesome Public Datasets 精选 |
| `search-engines` | 搜索引擎日志 | AOL Query Log |
| `social-networks` | 社交网络 | Twitter Streaming API, Reddit Pushshift |
| `social-sciences` | 社会科学 | General Social Survey, Pew Research |
| `software` | 软件工程 | GitHub Archive, Stack Overflow Data Dump |
| `sports` | 体育 | FiveThirtyEight Sports Data |
| `time-series` | 时间序列 | UCR Time Series Archive |
| `transportation` | 交通运输 | NYC Taxi Trips, Uber Movement |
| `complementary-collections` | 互补合集 | Awesome Datasets 汇总 |

## 使用示例

```bash
# 搜索与图像分类相关的数据集
tzukwan dataset-hub search "image classification" --category computer-vision

# 为研究主题推荐最合适的数据集
tzukwan dataset-hub recommend "sentiment analysis for social media" --top 5

# 查看某个数据集的详细信息
tzukwan dataset-hub info "MIMIC-III" --include citation

# 生成数据集的标准 manifest 文件
tzukwan dataset-hub manifest "ImageNet" --output ./data/imagenet_manifest.json

# 列出所有医疗健康类数据集
tzukwan dataset-hub list --category healthcare --sort citations

# 检查数据集链接有效性
tzukwan dataset-hub search "time series" --validate-links

# 搜索支持商业使用许可证的 NLP 数据集
tzukwan dataset-hub search "text classification" --license commercial --category natural-language
```

### 对话触发示例

```
用户：帮我找适合做文本分类任务的数据集
用户：有哪些公开的医学影像数据集？
用户：推荐几个适合做时间序列预测的数据集
用户：给我生成 MNIST 数据集的 manifest 文件
用户：有没有免费可商用的中文 NLP 数据集？
```

## 触发词

- `dataset`
- `数据集`
- `find data`
- `公开数据`
- `benchmark`
- `训练数据`
- `数据来源`
- `awesome-public-datasets`
- `data source`
- `open data`

## 数据源/API 依赖

| 来源 | 获取方式 | 数据量级 | 更新频率 |
|------|----------|----------|----------|
| awesome-public-datasets (GitHub) | GitHub API / raw content | ~500 个精选数据集 | 社区维护，实时获取 |
| Kaggle Datasets | Kaggle Public API | 50,000+ 数据集 | 实时 |
| Hugging Face Datasets | `datasets` Python 库 / Hub API | 100,000+ 数据集 | 实时 |
| UCI ML Repository | HTML 抓取 + API | ~600 数据集 | 定期更新 |
| OpenML | `https://www.openml.org/api/v1` | 5,000+ 数据集 | 实时 |
| Papers with Code Datasets | `https://paperswithcode.com/api/v1/datasets/` | 6,000+ 基准数据集 | 实时 |

**GitHub API 配置（提升速率限制）：**
```yaml
# ~/.tzukwan/config.yaml
apis:
  github_token: "ghp_your_token_here"   # 从 5000/h 提升速率
  kaggle_username: "your-username"
  kaggle_key: "your-api-key"
```

## 输出格式

### 搜索结果（终端 Markdown）

```markdown
## 数据集搜索结果：image classification（共 12 个）

### 1. ImageNet Large Scale Visual Recognition Challenge (ILSVRC)
- **类别：** computer-vision
- **大小：** ~150 GB（完整版）/ ~13 GB（ILSVRC2012）
- **格式：** JPEG 图像 + XML 标注
- **许可证：** 非商业研究使用
- **引用数：** 90,000+（Russakovsky et al., IJCV 2015）
- **链接：** https://image-net.org/
- **BibTeX：** 见下方

### 2. MS COCO (Common Objects in Context)
...
```

### Manifest 文件格式（JSON）

```json
{
  "name": "ImageNet",
  "version": "ILSVRC2012",
  "description": "Large-scale image recognition benchmark with 1000 classes",
  "url": "https://image-net.org/download",
  "size_bytes": 13700000000,
  "format": ["JPEG", "XML"],
  "license": "ImageNet Terms of Access",
  "license_commercial": false,
  "categories": ["computer-vision", "image-classification"],
  "splits": {
    "train": 1281167,
    "val": 50000,
    "test": 100000
  },
  "classes": 1000,
  "citation": {
    "bibtex": "@article{russakovsky2015imagenet,...}",
    "apa": "Russakovsky, O., et al. (2015). ImageNet large scale visual recognition challenge. IJCV, 115(3), 211-252."
  },
  "download_scripts": {
    "wget": "wget https://image-net.org/data/ILSVRC/2012/ILSVRC2012_img_train.tar",
    "python": "import torchvision; torchvision.datasets.ImageNet('./data', split='train', download=True)"
  },
  "retrieved_at": "2024-01-15T10:30:00Z",
  "source": "awesome-public-datasets"
}
```
