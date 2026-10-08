---
name: qm-reader-data
description: 读取乔木阅读（rss.qiaomu.ai）的数据：最新文章列表、订阅源列表、单篇文章正文、中文翻译和乔木改写版。当用户想查看乔木/QMReader 上有什么新文章、想读某篇文章内容、想让 AI 总结或翻译乔木上的文章，或在 qmreader-ios 项目中调试涉及 /api/entries、/api/sources、/api/entry 的数据问题时，都应使用本 skill——即使用户没有明确提到"乔木"或"QMReader"，只要意图是获取这个 RSS 数据源的内容就适用。
---

# QMReader 数据读取

通过项目自带的命令行脚本读取 `https://rss.qiaomu.ai` 的数据。脚本位于本 skill 目录下的
`scripts/qm_reader.py`，只依赖 Python 标准库，无需安装任何东西。

## 用法

所有命令都支持 `--json` 输出原始 JSON（需要完整结构化数据时使用）。

```bash
SCRIPT="<skill目录>/scripts/qm_reader.py"

python3 "$SCRIPT" entries --limit 20        # 最新文章列表（默认 60 篇）
python3 "$SCRIPT" sources                   # 订阅源列表（含 id、分类、文章数；禁用源带 ✗ 标记）
python3 "$SCRIPT" source <source_id>        # 某个订阅源下的文章
python3 "$SCRIPT" entry <entry_id>          # 文章正文（原文；原文为空时自动回退到改写版）
python3 "$SCRIPT" entry <entry_id> --translation   # 中文翻译
python3 "$SCRIPT" entry <entry_id> --rewrite       # 乔木改写版
python3 "$SCRIPT" raw "/api/entry/<id>"     # 任意 /api 路径的原始 JSON
```

`<skill目录>` 即本 SKILL.md 所在目录。

## 典型工作流

1. **用户问"最近有什么新文章"** → 跑 `entries`，把标题和时间整理成简洁清单回复。
2. **用户要读/总结某篇文章** → 先用 `entries` 或 `sources` 拿到 entry id，再跑 `entry <id>`；
   如果正文质量差或用户偏好中文表达，改用 `--translation` 或 `--rewrite` 版本作为总结素材。
3. **用户想看某个订阅源的内容** → 先 `sources` 按名字找到 source id，再 `source <id>`。
4. **翻页**：`source` 命令返回 `nextCursor` 时，用
   `raw "/api/sources/<id>/entries?limit=40&ready=rewrite&cursor=<cursor>"` 取下一页。

## 禁用源说明

订阅源可能被服务端**禁用**（`sources --json` 中 `enabled: false`）。禁用源的
`/api/sources/{id}/entries` 接口会返回 **HTTP 404**，其文章也不会出现在跨源
`entries` 列表里——这不是网络故障，不要反复重试。脚本已对此做了友好提示，
遇到时应如实告知用户该源不可用，并建议换一个已启用的类似源。

## 回复用户的注意事项

- 列表输出里每篇文章的方括号内是 **entry id**，读取正文时要原样传给 `entry` 命令。
- 时间戳为服务器返回的毫秒 epoch，脚本已转成本地时间。
- API 只返回已就绪（ready=rewrite）的内容；服务端正在生成的文章不会出现在结果里。
- `sources` 文本输出中带 ✗ 前缀的源是禁用状态，不要对它们跑 `source <id>`。
- 网络失败会以非零退出码结束并打印错误原因（HTTP 状态码或 DNS/连接错误），
  此时如实告知用户即可，不要编造文章内容。

## 数据来源说明

此 API 与 QMReader iOS 客户端使用同一后端，接口契约参见项目中
`QMReader/APIClient.swift` 与 `QMReader/Models.swift`。主要端点：

| 端点 | 说明 |
|---|---|
| `/api/entries?limit=N&ready=rewrite` | 跨源最新文章 |
| `/api/sources?ready=rewrite` | 订阅源列表 |
| `/api/sources/{id}/entries?limit=&cursor=` | 单源文章，cursor 分页 |
| `/api/entry/{id}` | 文章详情（含 content、summary、rewrite.body 等） |
| `/api/entry/{id}/translation` | 中文翻译（段落对数组 content[].target/targetHtml） |
| `/api/entry/{id}/rewrite` | 乔木改写版（markdown body） |
