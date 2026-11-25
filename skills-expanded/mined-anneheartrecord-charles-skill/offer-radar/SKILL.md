---
name: offer-radar
description: Use when 用户收到招聘/合作邮件，想快速背调一家公司或某个人是否靠谱（背景、融资、员工评价、口碑、法律风险）。贴入邮件文本，自动提取公司/人名，多渠道并行搜索，输出结构化 Markdown 报告。命令行工具。
---

# offer-radar

收到招聘邮件后，快速背调公司/人物的 CLI 工具。贴入邮件，自动提取公司名和人名，多渠道并行搜索，生成结构化 Markdown 报告。

## 何时用

用户拿到一封招聘或合作邮件，想知道对面公司靠不靠谱、创始人背景、薪资职级、社区口碑、有无法律纠纷，再决定要不要花时间聊。

## 安装与配置

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e .
export XCRAWL_API_KEY=your_key   # XCrawl Search API，免费注册送 1000 credits（约够 70 次调查）
```

## 常用命令

- 贴邮件分析：`offer-radar analyze --text "<邮件正文>"`
- 从文件读：`offer-radar analyze --file email.txt`
- 直接查公司：`offer-radar check --company "滴滴出行"`
- 公司 + 人一起查：`offer-radar check --company "某公司" --person "某人"`
- 省 credits（只提取不搜）：`offer-radar analyze --text "..." --no-search`

## 输出

一份 Markdown 报告：邮件摘要 + 公司调查（综合信息、天眼查工商融资、脉脉职级薪资、知乎口碑、V2EX 讨论、GitHub 技术实力）+ 综合评估。每个渠道给 5 条带链接的结果。
