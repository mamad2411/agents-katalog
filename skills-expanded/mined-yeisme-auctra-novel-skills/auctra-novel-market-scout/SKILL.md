---
name: auctra-novel-market-scout
description: Use when an author wants to turn an authorized local ranking snapshot into reviewable market insight (reader-demand signals, reusable recipes, advisory project-fit). Routes platform collection/provider adapters only to future MediaOps and keeps Auctra DecompositionProvider as the LLM owner.
---

# Auctra Novel Market Scout

把授权本地排行榜快照变成可审阅的市场洞察。本 skill 是 Auctra novel-market-intelligence 能力的入口；它绝不抓取平台、登录或保存 cookies/provider secret。

## 何时使用

- 作者持有 `permission=owned` 或 `permission=licensed` 的本地排行榜快照。
- 想从快照得到读者需求 signal、可复用 recipe 或项目契合建议。
- 想了解某个 ranking 趋势是否值得采纳进创作策略。

## 输入

- 授权本地快照文件路径 + permission + scope（如 qidian）。
- 分析 objective、profile（如 reader_demand）、taxonomy version。
- decomposition provider id（默认 fixture；真实 Pi/OMP 待生产授权）。
- idempotency key（用于幂等重放）。

## 输出

- redacted receipt（transition/version/authority/cursor/digest；无 raw body/prompt/payload/secret）。
- analysis state（imported→validated→observed→decomposing→ready/partial/failed）。
- 仅在 ready 时：signal refs、recipe proposal（pending_review）、project-fit proposal（advisory）。
- doctor 输出（ready/unavailable/unsupported + next actions；无 provider payload）。

## 不做的事

- 不抓取平台、不登录、不保存 cookies/provider secret。
- 不在业务层接 provider SDK；DecompositionProvider 是 subprocess/projection adapter。
- 不自动采纳正文或 promotion；accept 只走既有 `auctra review accept|partial|reject`。
- 不把 simulation fixture（`simulation=true`）当作真实 LLM evidence。
- 不把 MediaOps（平台 collection/provider adapter）当作已存在能力；MediaOps 路由只指向未来独立产品。

## LLM gate

确定性代码只产出 observation。signal/recipe/project-fit 只能来自成功的、完整的、非 simulation 的 decomposition projection。LLM unavailable → `DECOMPOSITION_PROVIDER_UNAVAILABLE`，保留 observation，绝不退化为规则结论。partial assignment → `DECOMPOSITION_ASSIGNMENT_PARTIAL`，仅显式 retry 再进 decomposing。

## 命令

- `auctra market snapshot import --from <path> --permission <owned|licensed> --scope <scope>`
- `auctra market analyze <snapshot-id> --runtime <provider> --objective <text> --idempotency-key <key>`
- `auctra market proposal list --status <status>`

## 关联

- 事实源：cli/auctra `docs/novel-market-intelligence.md`、`internal/market`、`internal/runtime/decomposition_*.go`。
- review 决策：复用既有 `auctra review accept|partial|reject`，无 bespoke market accept。
