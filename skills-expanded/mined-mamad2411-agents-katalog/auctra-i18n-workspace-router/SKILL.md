---
name: auctra-i18n-workspace-router
description: Use when configuring, migrating, diagnosing, documenting, or routing Auctra localized workspaces, especially zh-CN/chinese-novel layouts, display_path fields, layout_preset metadata, .auctra machine-source boundaries, and real CLI command examples.
---

# Auctra i18n 工作区路由器

负责判断 Auctra 项目是否需要 localized workspace 处理，并把请求路由到真实 CLI 命令、文档说明或具体创作技能。不要直接写 `.auctra/**`、SQLite rows、review 决策或 run evidence。

## 输入

- 用户目标、项目路径、已有 `project next/status/init` 输出、locale/layout 需求。
- 可选的 Auctra JSON：`locale`、`layout_preset`、`display_directories`、`machine_root`、`display_path`。
- 当前任务阶段：新建项目、迁移旧项目、解释目录、导入素材/章节、导出、agent 路由或文档同步。

## 路由

1. 新中文小说项目：推荐 `auctra project init <path> --title "..." --genre "..." --locale zh-CN --layout chinese-novel --json`，再交给 `auctra-chinese-project-starter` 规划首轮素材、gate 和章节。
2. 旧项目切换中文显示目录：先运行 `auctra project layout plan <path> --locale zh-CN --layout chinese-novel --json`；只有用户确认后才建议 `apply ... --yes --json`。
3. 用户问目录含义：解释 `章节/`、`大纲/`、`设定/`、`人物/`、`素材/`、`伏笔/`、`审稿/`、`导出/` 是 display directories；`.auctra/` 是机器真源。
4. 导入/导出路径：允许 display path，例如 `auctra chapter import markdown ./章节`、`auctra material add --from 素材/备案制度.md`、`auctra chapter export markdown` 默认导出到 `导出/`。
5. JSON/agent 合同：机器字段继续英文；新增字段是 additive，例如 `layout_preset`、`display_directories`、`display_path`，不得重命名旧字段。
6. 创作任务本身：中文小说规划/写章/审稿交给 `chinese-novel-orchestrator` 或更窄的中文小说技能；小红书等平台内容交给对应平台技能。

## 边界

- 不承诺 localized workspace 等于 scenario first-support 或 mature；readiness 仍看 gates、review evidence、export/handoff 和 integration evidence。
- 不把 `Codex`、`Claude` 或其它 coding agents 注册成 Auctra provider；它们只是 CLI caller。
- 不调用模型 provider SDK，不写平台 secret，不自动发布。
- 不手写 `.auctra/project.yaml`、`.auctra/layout.yaml`、`.auctra/runs/**`、`.auctra/review/**`、`.auctra/exports/**` 或 SQLite 数据。

## 真实命令

```bash
auctra project init ./chichao --title "赤巢备案" --genre "玄幻悬疑" --locale zh-CN --layout chinese-novel --json
auctra project layout plan ./legacy --locale zh-CN --layout chinese-novel --json
auctra project layout apply ./legacy --locale zh-CN --layout chinese-novel --yes --json
auctra project next --path ./chichao --json
auctra chapter import markdown ./章节
auctra material add --kind note --title "备案制度" --from 素材/备案制度.md --json
auctra chapter export markdown
```

## 验证

- 对 CLI 行为改动，运行对应窄测试和 `openspec validate auctra-i18n-workspace-layout --strict`。
- 对 Skill 改动运行 `python3 scripts/validate_skills.py`；涉及 profile 时由宿主项目继续运行其 profile/runtime sync 验证。
