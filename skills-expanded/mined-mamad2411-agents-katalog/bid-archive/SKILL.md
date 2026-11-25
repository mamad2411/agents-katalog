---
name: bid-archive
description: |
  项目归档，形成闭环。打包 final/ 和 output/ 到 archive/ 目录，生成归档信息，可选清理工作区。
  前置条件：final/ 下有完整标书文件。
  触发关键词：归档、archive、项目归档、存档、打包、闭环。
---

# 项目归档

## 前置检查

用 Glob 确认 `final/` 下有标书文件，不存在则提示先执行 `/bid-integrate-final`。

## Step 1: 提取归档信息（AI 完成）

读取以下文件，提取归档所需信息：

| 文件 | 提取内容 |
|------|---------|
| `output/tender_facts.md` | 招标编号、项目名称、采购人、行业分类 |
| `output/audit_report.md`（如存在） | 审计结论、评分点覆盖率 |
| `output/plan_budget.md` | 方案数量、总字数预算 |

**归档目录名格式**：`{招标编号}_{项目简称}_{YYYYMMDD}`

> 如招标编号不存在，用 `proj_{项目简称}_{YYYYMMDD}` 代替。

## Step 2: 执行归档（脚本完成）

询问用户是否包含 `inputs/` 目录，然后运行 [archive.py](scripts/archive.py)：

参数：`"{归档目录名}" [--include-inputs]`

## Step 3: 生成归档摘要（AI 完成）

在 `archive/{归档目录名}/archive_info.md` 中写入：

```markdown
# 归档信息

| 项目 | 内容 |
|------|------|
| 项目名称 | ... |
| 招标编号 | ... |
| 采购人 | ... |
| 行业分类 | ... |
| 归档时间 | YYYY-MM-DD HH:MM |

## 方案清单

| 方案 | 字数 | 评分点覆盖 |
|------|------|-----------|
| ... | ... | ... |

## 关键承诺摘要

（从各方案 summary 提取核心承诺）

## 审计结论

（从 audit_report.md 提取，如无则标注"未审计"）

## 文件清单

（列出归档目录中的所有文件）
```

## Step 4: 清理工作区（可选）

询问用户是否清理工作区为下一个项目腾出空间：

运行 [archive.py](scripts/archive.py)，参数：`"{归档目录名}" --clean`

清理策略：
- 清空 `output/`、`final/`、`inputs/tender/`、`inputs/cases/`
- **保留** `inputs/company/`（公司资料跨项目复用）
- **保留** `archive/`（归档不清理）

## 输出

- `archive/{归档目录名}/` 完整归档
- 输出归档摘要（项目名、方案数、总字数、归档路径）
