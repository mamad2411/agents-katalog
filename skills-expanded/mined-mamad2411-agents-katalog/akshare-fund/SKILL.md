---
name: akshare-fund
description: 使用 AKShare 库获取和分析中国基金市场数据。AKShare 是免费开源的 Python 金融数据接口库，无需注册或 Token。支持：基金实时行情、历史行情数据。当用户需要获取基金数据、分析基金基本面时使用此 skill。
---

# AKShare分析基金Skill

使用AKShare库获取中国基金市场数据并进行分析。AKShare是**免费开源**的金融数据接口，无需注册或Token。

## 快速开始

### 环境准备

```bash
# pip install akshare pandas pyyaml
pip install akshare pandas
```

### 使用脚本

```bash

# 基本信息
/app/working/active_skills/akshare-fund/scripts/get_basic_info.py 000001

# 实时行情
/app/working/active_skills/akshare-fund/scripts/get_realtime_quote.py 000001
# 多只基金
/app/working/active_skills/akshare-fund/scripts/get_realtime_quote.py 000001 000002

# 历史K线
/app/working/active_skills/akshare-fund/scripts/get_history_kline.py 000001 --days 60

# 技术指标
/app/working/active_skills/akshare-fund/scripts/calc_technical.py 000001

```

## 脚本列表

### 数据获取脚本

| 脚本                    | 功能     | 示例                                           |
| ----------------------- | -------- | ---------------------------------------------- |
| `get_basic_info.py`     | 基本信息 | `python get_basic_info.py 000001`              |
| `get_realtime_quote.py` | 实时行情 | `python get_realtime_quote.py 000001`          |
| `get_history_kline.py`  | 历史行情 | `python get_history_kline.py 000001 --days 60` |
| `calc_technical.py`     | 技术指标 | `python calc_technical.py 000001`              |

<!--

### 工具脚本

| 脚本               | 功能     | 说明                   |
| ------------------ | -------- | ---------------------- |
| `cache_manager.py` | 数据缓存 | SQLite 本地缓存        |

-->

## 核心功能

### 1. 技术指标

```bash
/app/working/active_skills/akshare-fund/scripts/calc_technical.py 002475
```

支持指标：

- **MA**: 5/10/20/60日均线
- **MACD**: DIF, DEA, MACD柱
- **RSI**: 6/12/24日
- **KDJ**: K, D, J
- **BOLL**: 上轨/中轨/下轨

<!--

### 3. 数据缓存

自动缓存避免重复请求：

- 实时行情：1分钟
- 日K线：1小时
- 财务数据：7天
- 股东数据：30天

-->

## 输出格式

所有脚本默认输出 **Markdown** 格式，可直接预览或保存：

## 文件结构

```
akshare-fund/
├── SKILL.md                 # 本文档
├── config.yaml              # 配置文件(可选)
├── references/
│   ├── api_reference.md     # API 参考
│   └── official_docs.md     # 官方文档索引
└── scripts/
    ├── calc_technical.py       # 技术指标
    ├── cache_manager.py        # 数据缓存
    ├── get_realtime_quote.py   # 实时行情
    ├── get_history_kline.py    # 历史行情
    └── get_basic_info.py       # 基本信息
```

## 参考资源

- [API 参考文档](references/api_reference.md)
- [AKShare 官方文档](references/official_docs.md)
- **官网**: https://akshare.akfamily.xyz
- **GitHub**: https://github.com/akfamily/akshare
