---
name: rj-skills-hbr-finder
description: v2026.05.07.01；使用远端锐捷 skills 服务的哈佛商业评论中文版检索能力时调用：按关键词检索哈佛商业评论中文版文章，获取文章详情，输出带正文和内联图片的 Markdown。适用于“查 HBR”“哈佛商业评论中文版”“找管理文章”“管理文章检索”等请求；搜索结果按批展示，每批后用 functions.request_user_input 询问是否继续获取 5 条或 10 条。
---

# 锐捷-哈佛商业评论

这是锐智内置“锐捷插件”提供的 skill。Codex 通过插件的 `skills/rj-skills-hbr-finder` 发现并触发本 skill。

## 使用方式

执行时先读取当前 `SKILL.md` 所在目录，把 `scripts/search-hbr.mjs` 解析为该目录内脚本的绝对路径，然后调用。不要使用开发机绝对路径。

```powershell
node <当前 skill 目录>\scripts\search-hbr.mjs "AI 战略"
```

可选参数：

```powershell
node <当前 skill 目录>\scripts\search-hbr.mjs "组织管理" --limit 5
node <当前 skill 目录>\scripts\search-hbr.mjs "组织管理" --limit 20 --json
node <当前 skill 目录>\scripts\search-hbr.mjs "组织管理" --last-id 2 --exclude-ids 481309,478039 --json
node <当前 skill 目录>\scripts\search-hbr.mjs "最新 AI 管理" --json
node <当前 skill 目录>\scripts\search-hbr.mjs article 481309
```

后端地址已在脚本中固定为 `http://skills.rjagi.cn/`。

## 搜索续取

- 用户只触发本 skill、但没有给任何搜索关键词或文章 ID 时，必须先调用 `functions.request_user_input` 让用户输入 HBR 搜索关键词；不要直接结束，也不要随便猜关键词。拿到关键词后再执行搜索。
- 搜索文章时优先调用 JSON 模式，并用 `--limit 20` 拉取一批候选缓存；默认先展示前 5 条，除非用户明确指定展示数量。
- 在对话内维护 `shownIds`、本地未展示的 `results`、`nextLastId` 和 `hasMore`。续取时先消费本地缓存；本地缓存耗尽但 `hasMore` 为 `true` 且存在 `nextLastId` 时，再调用脚本继续取：

```powershell
node <当前 skill 目录>\scripts\search-hbr.mjs "组织管理" --limit 20 --last-id <nextLastId> --exclude-ids <shownIds 逗号分隔> --json
```

- 每次输出完一批后，只要仍有可展示数据，就调用 `functions.request_user_input`。选项按剩余数量给出：
  - 剩余不少于 10 条：`继续获取 5 条数据`、`继续获取 10 条数据`、`结束`
  - 剩余 5 到 9 条：`继续获取 5 条数据`、`继续获取剩余数据`、`结束`
  - 剩余不足 5 条且后端没有更多：直接展示剩余数据，然后停止，不再调用 `functions.request_user_input`
- 如果用户选择的数量超过当前缓存，但后端还有更多，先展示缓存，再用 `nextLastId` 补拉，直到满足数量或确认没有更多。
- 如果脚本返回空结果，或 `hasMore` 为 `false` 且没有本地剩余数据，明确说明“没有更多结果”，不要继续弹选择。

## 行为约定

- 不要求用户配置哈佛商业评论中文版账号、密码或 token；访问能力由锐捷 skills 服务处理。
- 服务端返回的 `markdown` 中已经生成好的文章链接必须原样展示；URL query 中的 `token` 是本服务链接参数，不是用户登录凭证，不要删除、隐藏、脱敏或改写。
- 如果后端服务未启动、配置缺失、接口变更或登录失败，直接报告失败原因，不要编假结果。
- 如果用户要把结果塞进某个应用，优先输出 Markdown；调用方自己负责持久化或展示。
