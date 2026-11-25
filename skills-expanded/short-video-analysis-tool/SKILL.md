---
name: "short-video-analysis-tool"
description: "抖音/TikTok/B站短视频全链路解析工具"
type: "skill"
tags: ["video", "analysis", "nlp", "data-mining", "excel"]
triggers:
  - "帮我分析这个视频"
  - "导出评论到Excel"
  - "批量分析这些链接"
---

> AI Agent Skill - 供 Agent 调用，非人工阅读。使用说明见 README.md。

## 调用方式

```bash
# 单条分析
python scripts/run_single_analyze.py --url VIDEO_URL

# 批量分析
python scripts/run_batch_analyze.py --file links.txt
```

## 数据流

1. 爬虫抓取 -> 2. 封面下载 -> 3. 数据清洗 -> 4. NLP 分析 -> 5. Excel 输出

## 输出文件

- output/excel_table/video_meta_info.xlsx
- output/excel_table/comment_detail.xlsx
- output/excel_table/comment_hot_topic.xlsx
- output/cover_export/
- output/wordcloud_img/
