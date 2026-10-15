---
name: repo-to-wiki
description: Use when you need to quickly get familiar with an unfamiliar code repository and turn that understanding into a Chinese multi-page Feishu/Lark wiki doc tree with hand-drawn illustrations — onboarding onto a new project, documenting a codebase for the team, or producing shareable architecture/business docs from a repo.
---

# repo-to-wiki

> 当前版本以本 skill 目录下的 `VERSION` 文件为准。

## 版本与更新自检（每次使用前先做，第 0 步）

开始干活前先比对远端最新版，避免用旧版。`<SKILL_DIR>` = 本 skill 的 Base directory（harness 在加载时会告诉你）。

```bash
LOCAL=$(cat "<SKILL_DIR>/VERSION" 2>/dev/null || echo "0.0.0")
REMOTE=$(curl -fsSL https://raw.githubusercontent.com/pw-OpenCapsule/repo-to-wiki/main/skills/repo-to-wiki/VERSION 2>/dev/null | tr -d '[:space:]')
```

- 拿不到 `REMOTE`（离线 / GitHub 限流）→ 跳过检查，正常继续。
- `REMOTE` 与 `LOCAL` 相等 → 静默继续。
- `REMOTE` 比 `LOCAL` 新（按 semver 比较）→ **必须明确提示用户**，例如：
  > ⚠️ repo-to-wiki 本地 v`$LOCAL` 落后，最新 v`$REMOTE`。建议先更新再用：
  > `npx skills update -g`（更新全部已装 skill）；只更这个用 `npx skills add pw-OpenCapsule/repo-to-wiki --skill repo-to-wiki -g`。

  征得同意后可代为执行更新；**更新后请让用户重新调用本 skill**（当前对话里已加载的还是旧版正文）。用户坚持用旧版可继续，但要说明可能缺新功能/修复。

## Overview

One skill that chains the team's existing tools to take a repository from「看不懂」to a published, illustrated, Chinese **多子页飞书 wiki 文档树**. It ORCHESTRATES — it does not reimplement — these skills:

`understand-anything` · `codegraph` · `code-search` · `chatgpt-imagegen` · `lark-doc` · `lark-wiki` · `portwind-wiki`

Core idea: 先拿地图（自动分层+图谱）→ 读主链路（仓内）→ 理解上下游（跨仓）→ 补业务 → 配「固定烂图风」插图 → 沉淀成飞书 wiki 多子页。

## When to use

- 接手陌生仓库，要快速吃透并能讲给团队
- 给一个 codebase 产出架构 / 业务理解文档
- 把项目理解沉淀进飞书 wiki（多子页，含插图）

## Prerequisites

- 已安装这些 skill：`understand-anything`、`codegraph`（可选）、`code-search`（可选，跨仓）、`chatgpt-imagegen`、`lark-doc`、`lark-wiki`、`portwind-wiki`
- `lark-cli` 已登录且具备 wiki + docx + 图片上传 scope。粗粒度 `lark-cli auth login --scope "wiki,doc"`；实际需要细粒度 `wiki:node:create`、`docx:document:write_only`、`docs:document.media:upload`、`wiki:space:retrieve`。注意 `auth check --scope wiki` 用的是粗名，可能误报 `ok=false`，以 `auth status` 里的细粒度 scope 为准。
- `chatgpt-imagegen` 的 web backend（chrome-use 已登录 chatgpt.com）或 codex backend 可用

## Pipeline（按顺序）

1. **拿地图** — 对目标仓跑 `/understand --language zh`（understand-anything）→ `knowledge-graph.json`（分层 + 导览 + 节点/边）。可选 `/understand-dashboard` 看交互页。
2. **读主链路（仓内）** — 用 codegraph（`codegraph_context` / `codegraph_trace` / `codegraph_callers`）只读地图主线上的文件；没有 `.codegraph/` 就直接读核心文件。结构性问题查图谱比 grep 准。
3. **理解上下游（跨仓）** — 用 code-search 查跨仓「这接口谁在调、在哪个仓、前后端怎么对」。独立服务可跳过。
4. **补业务** — 跑 understand-anything 的 domain-analyzer（understand-domain）→ `domain-graph.json`（业务域 + 业务流）。源码理解 ≠ 业务理解，这层补「替谁解决什么生意问题」。
5. **配图** — 用 chatgpt-imagegen 按**固定提示词**出图（见 [references/image-prompt.md](references/image-prompt.md)）：1 张 hero + 每页 1 张概念图。**丑是风格，内容必须对**（正确的框/箭头/短英文标签）。
6. **沉淀** — 发布中文多子页到飞书 wiki，按 portwind-wiki 路由归到「各项目知识库 / 对应项目组」下。发布机制（建节点、插图置顶、流程图用 mermaid 画板、归档行）见 [references/wiki-publish.md](references/wiki-publish.md)；页面规划见 [references/page-plan.md](references/page-plan.md)。

## 用法（默认 = Workflow 模式）

> **默认就走 Workflow 模式。** 被调用时，除非用户明确说「一步步 / 手动 / Skill 模式 / 边看边来」，否则**默认**凑齐 args 后调用 `Workflow` 工具跑脚本，**不要**自己手动把链路跑一遍。
>
> （opt-in 说明：用户调用本 skill，而本 SKILL 指示你调用 `Workflow` 工具——这本身就满足 Workflow 工具「用户调用了一个其指令要求调用 Workflow 的 skill」的触发条件，可直接调用，无需额外让用户说出 workflow 关键词。）

### Workflow 模式（默认）

  > **你的唯一职责是调用 `Workflow` 工具去跑 [`repo-to-wiki.workflow.js`](repo-to-wiki.workflow.js)。不要自己手动跑 understand / domain / 配图 / 发布**——那是 Skill 模式。手动把整条链路跑一遍 = 没启动 workflow 模式（常见错误）。

  照这个顺序做，**几步之内就要调用 Workflow 工具**：
  1. 版本自检（上面第 0 步）。
  2. 凑齐 3 个必需 args（缺啥问用户，别自己脑补）：
     - `repoPath`：目标仓库绝对路径（默认当前项目根）。
     - `parentNodeToken`：发布到哪个父节点。按 portwind-wiki 路由，项目理解归「各项目知识库 / 对应项目组」；不确定就问用户，或 `lark-cli wiki +node-list --space-id <SP> --parent-node-token <各项目知识库>` 里找项目组。
     - `spaceId`：`lark-cli wiki spaces get_node --params '{"token":"<parent>"}'` 读 `data.node.space_id`（团队空间通常是 `7642234757744496151`）。
  3. **立即调用**（`<SKILL_DIR>` = 本 skill 的 Base directory）：
     ```
     Workflow({ scriptPath: "<SKILL_DIR>/repo-to-wiki.workflow.js", args: {
       repoPath, spaceId, parentNodeToken, imageBackend: "codex"
     }})
     ```
  4. 首次跑 workflow，harness 可能弹「multi-agent workflow 用量确认」，接受即可。脚本会起多 agent、确定性并行、最后顺序发布。

  也可把脚本放进 `.claude/workflows/` 后 `Workflow({ name: "repo-to-wiki", args:{…} })`。发布会真往飞书写多子页，先确认 `parentNodeToken`。

### Skill 模式（回退 / 显式手动）

仅在以下情况用：Workflow 功能被禁用 / 不可用，或用户明确要「一步步 / 手动 / 边看边来」，或暂时拿不到 wiki 目标节点（先补齐再说）。此时 agent 读本文件按上面 6 步自己做，灵活、能随时插话调整。

## 增量 / 补充（别重复生成、别建重复页）

重跑或只想补几页时，**默认增量、幂等**，不要从头重做：

- **拿地图**：understand-anything 本身增量（git commit hash + fingerprints）——同 commit 自动跳过/只重分析改动文件，重跑很便宜，放心跑。
- **配图**：图已存在就**跳过**（`chatgpt-imagegen -o` 会覆盖，所以先 `test -f` 判断），只有改了内容或 `force` 才重生成。
- **发布（关键）**：**先查后建**。发布前 `lark-cli wiki +node-list --space-id <SP> --parent-node-token <P>`（数据在 `data.nodes`）查父/索引节点下是否已有同标题页：
  - 有 → **更新**该页（block 级增量编辑，**别用 overwrite**，它会把标题冲成 Untitled），图只在重生成时替换。
  - 没有 → 才 `+node-create`。
  - **绝不无脑 node-create**，否则会建出一整棵重复子页树。
- **只补某几页**：Workflow 传 `args.only: ["02-redirect-flow", ...]`（索引页自动保留用于挂子页+更新目录）；Skill 模式直接说「只补 X、Y 页，其它别动」。`force:true` 才强制重做已存在的图/正文。

## Quick reference

| 步 | 用什么 skill | 产出 |
|---|---|---|
| 1 拿地图 | understand-anything `/understand --language zh` | 分层 + 导览 + knowledge-graph.json |
| 2 读主链路（仓内） | codegraph | 谁调谁、X 怎么流到 Y |
| 3 理解上下游（跨仓） | code-search | 接口在哪个仓、谁在调、前后端怎么对 |
| 4 补业务 | domain-analyzer (understand-domain) | 业务域 + 业务流 domain-graph.json |
| 5 配图 | chatgpt-imagegen（固定提示词） | 手绘示意图（丑风格、内容正确） |
| 6 沉淀 | lark-doc / lark-wiki + portwind-wiki | 飞书 wiki 多子页 |

## Common mistakes

- `docs +update overwrite` 会把页面标题冲成 `Untitled` —— 整篇重写后**必须** `str_replace "Untitled"` 改回标题。能避免就用增量编辑（`block_insert_after` / `block_replace`），别动不动 overwrite。
- `docs +media-insert` 把图插在文档**末尾** —— 要置顶得 `block_move_after --block-id <title_id> --src-block-ids <img>`。
- 流程图别用 ``` 代码块 —— 用 `<whiteboard type="mermaid">`（飞书原生画板，能拖能编）。mermaid 标签里别用引号/斜杠包特殊字符，否则渲染失败。
- 插图：提示词只写风格会出一堆只好看不解释的装饰画 —— 必须写清「正确的框 + 箭头 + 短英文标签」，见 image-prompt.md。
- code-search 是**跨仓**、codegraph 是**单仓**，分工别混。
- `lark-cli wiki +node-list --parent-node-token` 必须同时带 `--space-id`，返回数据在 `nodes` 键（不是 `items`）。

## See also

- [references/image-prompt.md](references/image-prompt.md) — 固定的「烂图风 + 内容正确」生图提示词
- [references/wiki-publish.md](references/wiki-publish.md) — lark-cli 发布飞书 wiki 的命令配方
- [references/page-plan.md](references/page-plan.md) — 多子页结构规划
