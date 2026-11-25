---
name: pubmed-journal-downloader
description: |
  Download all article titles and abstracts from a specific SCI journal within a specified year range using PubMed E-utilities.
  Use when: (1) User wants to download all articles from a journal, (2) User provides journal name and year limit, (3) User needs bibliographic data for research
---

# PubMed Journal Downloader

根据期刊名称和年份限制，批量下载该期刊的所有文章题目和摘要。

## 使用方式

运行脚本：
```bash
python /Users/richard/Documents/life/.claude/skills/pubmed-journal-downloader/scripts/fetch_journal_articles.py <期刊名称> <年份> [csv|json]
```

## 参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| 期刊名称 | 期刊的英文名 | "Nature" "Lancet" "Cell" |
| 年份 | 往前推的年数 | 5 表示近5年 |
| 输出格式 | csv 或 json，默认 csv | csv |

## 示例

```bash
# 下载 Nature 近5年文章
python fetch_journal_articles.py "Nature" 5

# 下载 Cell 近3年文章，JSON格式
python fetch_journal_articles.py "Cell" 3 json
```

## 注意事项

- 期刊名称需使用英文全称，如 "Journal of the American College of Cardiology"
- 脚本会自动创建以 "期刊名_年份_日期" 命名的文件
- PubMed 约索引 80% 的 SCI 期刊，部分期刊可能不在库中
- API key 已配置，可提高请求速率限制
