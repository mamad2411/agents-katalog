---
name: compare-reports
description: "基于统一索引对比分析不同时期的财报变化，或横向对比不同公司的研报观点。在用户请求跨期对比、同行研报对比时使用。"
keywords: 对比, 比较, 变化, 环比, 同比, 去年, 今年, 上季度, 不同公司, 横向, 差异
---

# compare-reports 技能指南

## 适用场景
- 对比同一公司不同时期的财报数据变化(如 2024年报 vs 2025年报)
- 对比不同公司的研报观点和核心指标
- 分析某家公司在不同券商研报中的评价差异

## 前提条件
- 需要先通过 `preprocess.py` 建立统一索引 (`data/vector_store/`)
- 或者通过 read-pdf 技能建立了单文档索引

## 可用脚本

| 脚本 | 功能 | 参数 |
|------|------|------|
| `scripts/cross_period.py` | 同一公司跨期对比 | `--stock`(股票代码), `--topics`(对比维度), `--index_dir` |
| `scripts/cross_company.py` | 不同公司横向对比 | `--stocks`(多个股票代码,逗号分隔), `--topic`(对比主题), `--index_dir` |

## 工作流程

1. 确认 `data/vector_store/` 存在统一索引
2. 根据用户需求选择跨期对比或跨公司对比
3. 执行对应脚本，自动从索引中检索相关内容并由 LLM 生成对比分析

## 示例对话

用户: "中芯国际2024年和2025年的营收变化"
步骤:
1. 执行 `python skills/compare-reports/scripts/cross_period.py --stock 688981 --topics "营收,净利润,毛利率"`
2. 返回跨期对比分析

用户: "对比中芯国际和贵州茅台的经营状况"
步骤:
1. 执行 `python skills/compare-reports/scripts/cross_company.py --stocks 688981,600519 --topic "经营状况和盈利能力"`
2. 返回横向对比分析

注意：所有路径参数使用相对路径（不带前导 /）。
