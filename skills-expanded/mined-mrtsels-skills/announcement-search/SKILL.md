---
name: announcement-search
description: 支持A股、港股、基金、ETF等金融标的公告的查询，包括定期财务报告、分红派息、回购增持、资产重组等。数据来源：同花顺问财。
---

# Announcement Search — 公告搜索

## 技能概述

搜索 A股、港股、基金、ETF 等金融标的公告，支持定期财务报告、分红派息、回购增持、资产重组等类型。

数据来源：**同花顺问财** (https://www.iwencai.com/unifiedwap/chat)

## CLI 使用

```bash
python3 scripts/announcement_search.py "贵州茅台 分红公告" --size 10
python3 scripts/announcement_search.py "上市公司业绩预告" --size 5 --output raw-response.json
```

## 环境变量

- `IWENCAI_BASE_URL` / `IWENCAI_API_KEY` — 已配置

## API 规范

**端点：** `POST /v1/comprehensive/search`

**请求体：**
```json
{"query": "贵州茅台 分红公告", "channels": ["announcement"], "app_id": "AIME_SKILL", "size": 10}
```

**Claw Headers：** 同其他 iwencai skills（X-Claw-Skill-Id: announcement-search）

## 工作流

1. 确认 `IWENCAI_API_KEY` 已设置
2. 将用户问题转为精准查询（每只标的/公告类型一条）
3. 调用 `scripts/announcement_search.py`
4. 解析原始响应，提取标题、摘要、时间、链接
5. 优先返回最新公告
6. 标注数据来源为同花顺问财
