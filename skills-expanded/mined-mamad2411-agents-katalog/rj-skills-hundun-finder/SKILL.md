---
name: rj-skills-hundun-finder
description: 使用远端锐捷 skills 服务的混沌大学能力时调用：按关键词查询混沌大学课程、文章、话题和集合视频/系列课包，获取课程、文章或集合详情，并输出带图片和课程目录的 Markdown。适用于“查混沌”“混沌大学”“混沌课程”“混沌战略课”“找混沌课程”“集合视频”“系列课包”等请求。
---

# 锐捷-混沌大学

这是锐智内置“锐捷插件”提供的 skill。Codex 通过插件的 `skills/rj-skills-hundun-finder` 发现并触发本 skill。

## 使用方式

执行时先读取当前 `SKILL.md` 所在目录，把 `scripts/search-hundun.mjs` 解析为该目录内脚本的绝对路径，然后调用。不要使用开发机绝对路径。

```powershell
node <当前 skill 目录>\scripts\search-hundun.mjs "战略"
```

可选命令：

```powershell
node <当前 skill 目录>\scripts\search-hundun.mjs "战略" --type course
node <当前 skill 目录>\scripts\search-hundun.mjs "战略" --type article
node <当前 skill 目录>\scripts\search-hundun.mjs "战略" --json
node <当前 skill 目录>\scripts\search-hundun.mjs "战略" --type course --limit 3 --offset 3
node <当前 skill 目录>\scripts\search-hundun.mjs course <courseId>
node <当前 skill 目录>\scripts\search-hundun.mjs article <articleId>
node <当前 skill 目录>\scripts\search-hundun.mjs collections "战略"
node <当前 skill 目录>\scripts\search-hundun.mjs collection <packageId>
```

后端地址已在脚本中固定为 `http://skills.rjagi.cn/`。详情页链接由服务端 `RJ_SKILLS_PUBLIC_BASE_URL` 生成。

## 行为约定

- 默认输出 Markdown；`--json` 输出结构化 JSON。
- 不要求用户输入混沌账号密码，也不要让用户提供登录凭证；播放能力由锐捷 skills 服务处理。
- 服务端返回的 `markdown` 中已经生成好的课程详情链接和 `[播放](...)` 链接必须原样展示；URL query 中的 `token` 是本服务链接参数，不是用户登录凭证，不要删除、隐藏、脱敏或改写。
- 搜索结果按用户选择的单一分类展示；除非用户明确要求“全部/分区”，不要默认混合展示。
- 无明确分类的关键词搜索，必须先让用户选择具体类型：`course` 或 `article`；不要先调用 `type=all` 把混合结果甩给用户。
- `type=all` 只在用户明确要求“全部/分区展示”时使用；这种情况下首屏只展示课程、文章和话题。展示后如果还要继续，必须再让用户选择具体分类续页，不要混合续页。
- 集合视频使用 `collections` 搜索分类课包，再用 `collection <packageId>` 打开详情。
- 如果后端服务未启动、配置缺失、接口变更或登录失败，直接报告真实失败原因，不要编假结果。

## 分类与分页交互

- 用户只触发本 skill、但没有给任何搜索关键词或资源 ID 时，必须先调用 `functions.request_user_input` 让用户输入搜索关键词；不要直接结束，也不要随便猜关键词。拿到关键词后再按下面规则选择分类。
- 用户只给关键词、未明确分类时，先调用 `functions.request_user_input`，让用户选择 `课程 course` 或 `文章 article`，再获取数据；不要先请求或展示 `type=all`。
- 分类选择选项固定优先级：
  - `课程 course`：适合找系统课，作为默认推荐。
  - `文章 article`：适合找笔记和文章。
- 如果用户在原始请求里已经明确分类，例如“课程 内卷”“文章 内卷”，直接按对应 `--type` 搜索，不再询问分类。
- 选定分类后，课程使用每批 3 条，文章使用每批 5 条。调用 `node <skill目录>\scripts\search-hundun.mjs "<关键词>" --type course --limit 3 --offset 0 --json` 或 `node <skill目录>\scripts\search-hundun.mjs "<关键词>" --type article --limit 5 --offset 0 --json`，读取 `markdown`、`type`、`limit`、`offset`、`total`、`returned`、`remaining`、`nextOffset`、`hasMore`。
- 必须把 `markdown` 作为正常 Markdown 直接渲染展示给用户；不要包在 ```markdown 代码块里，代码块会让标题、链接和列表都变成死文本，体验很蠢。
- 不要从 `courses[].directory[]`、`detail.directory[]` 或 `collections[].courseList[]` 自己重组目录来替代 `markdown`；这些结构化字段可能没有播放 URL，强行重组会把链接弄丢。
- 如果用户明确要求“全部/分区展示”，才允许先调用 `--json` 默认 `type=all` 并展示分区结果；展示后如果还要继续，必须再让用户选择具体分类续页，不要混合续页。
- 如果 `remaining <= 0`，停止，不调用 `functions.request_user_input`。
- 课程分页：如果 `remaining <= 3`，自动用 `--offset <nextOffset> --limit <remaining>` 获取剩余数据并停止；如果 `remaining >= 6`，调用 `functions.request_user_input`，选项为 `继续获取 3 条`、`继续获取 6 条`、`停止`；如果 `remaining` 为 `4-5`，选项为 `继续获取 3 条`、`继续获取剩余 N 条`、`停止`。
- 文章分页：如果 `remaining <= 5`，自动用 `--offset <nextOffset> --limit <remaining>` 获取剩余数据并停止；如果 `remaining >= 10`，调用 `functions.request_user_input`，选项为 `继续获取 5 条`、`继续获取 10 条`、`停止`；如果 `remaining` 为 `6-9`，选项为 `继续获取 5 条`、`继续获取剩余 N 条`、`停止`。
- 每次继续后使用上一批 JSON 的 `nextOffset` 作为新 `--offset`，只要仍有足够剩余数据就重复上述流程。
