---
name: zhihu-search
version: 2.0.0
description: 搜索知乎站内内容，获取标题、摘要、作者和内容链接等信息
homepage: https://developer.zhihu.com/console/docs?key=zhihu_search
metadata: {"openclaw":{"emoji":"🔍","requires":{"bins":["python3"]}}}
---

# Zhihu Search Skill

通过 `GET /api/v1/content/zhihu_search` 检索知乎内容。

## 认证

设置 `ZHIHU_ACCESS_SECRET`。可选设置：

- `ZHIHU_OPENAPI_BASE_URL`：默认 `https://developer.zhihu.com`
- `ZHIHU_ZHIHU_SEARCH_URL`：完整 endpoint，优先级更高

## 调用

```bash
python3 {baseDir}/scripts/zhihu-search.py '{"query":"如何理解 rave 文化","count":5}'
```

`query` 必填；`count` 默认为 10，并限制到 1-10。

## 响应参数

- `Code`：状态码，`0` 表示成功。
- `Message`：状态说明。
- `Data.HasMore`：是否还有更多结果。
- `Data.SearchHashId`：本次搜索标识。
- `Data.EmptyReason`：无搜索结果时的原因说明。
- `Data.Items`：搜索结果列表；每项包含 `Title`、`ContentType`、`ContentID`、`ContentText`、`Url`、`CommentCount`、`VoteUpCount`、`AuthorName`、`AuthorAvatar`、`AuthorBadge`、`AuthorBadgeText`、`EditTime`、`AuthorityLevel`、`RankingScore` 和 `CommentInfoList`。

命令失败时以非零状态结束。根据错误信息检查输入参数、认证配置、网络状态或调用频率。
