---
name: cross-model-review
description: 跨模型对抗审查已锁定的 PLAN.md——自动发现可用 CLI（codex/gemini/claude），推荐两个不同 provider 的组合并让用户选择，reviewer 只读运行输出 VERDICT:APPROVED|REVISE，主 agent 仲裁并把理由写进 PLAN-REVIEW-LOG.md，MAX_ROUNDS 不收敛输出 deadlock。基于 chaseai-yt/grill-me-codex（MIT）的 Act 2 思路。
locale: zh-CN
supported_locales: [zh-CN]
experimental_locales: [en-US]
---

# Cross Model Review

## 强制入口

命中本 skill 时，**必须先完整阅读** [references/cross_model_review.md](references/cross_model_review.md) 并按其中条款执行。

- 不得以 preamble、Cursor 规则摘要或其它二次摘要代替该文件全文。
- 本 skill 是 `plan-grill` 的 Act 2；plan-grill 锁定 PLAN.md 后接力本 skill。

## 五条核心规则

- [CMR-001] **自动发现 reviewer**：直接探测 codex/gemini/claude 三个 CLI 的可用性、版本、non-interactive 与只读模式支持（可用 `command -v <cli>` + `<cli> --version`，本仓库可选辅助脚本为 `skills-engineering/scripts/detect-review-clis.sh`）。可用 provider < 2 时停止并提示安装，不伪造 cross-model。
- [CMR-002] **推荐组合 + 用户选择**：从可用 CLI 中推荐两个不同 provider 的组合（如 codex + gemini），让用户确认。不静默替用户选死。
- [CMR-003] **reviewer 只读**：每个 reviewer 必须以只读模式运行——codex 用 `-s read-only`，gemini 用 `--approval-mode plan`，claude 用 `--permission-mode plan`。reviewer 不写代码，只输出 `VERDICT: APPROVED` 或 `VERDICT: REVISE` + 具体修改建议。> 注：上述 CLI 只读/plan 模式 flag 依凭记忆列出，未经各 CLI 实测核验（`cognitive-reasoning` GR-011）；落地前请对每个 CLI 实测确认 flag 名称与"只读"语义，偏差则以此处修订为准。
- [CMR-004] **主 agent 仲裁**：主 agent（Claude/Codex，视宿主而定）是最终仲裁者。每轮必须收集所有已选 reviewer 的 verdict；reviewer 原始输出、中间输出和交付日志必须保存在当前项目根目录下（推荐 `.plan-reviews/<date>-<slug>/raw/`），不得用 `/tmp` 作为 reviewer 输出缓冲。只有全部 `APPROVED` 才能收敛，任一 `REVISE` 都必须仲裁并进入修订/下一轮。采纳有证据的批评，拒绝不成立的批评并写明理由，记录进 `PLAN-REVIEW-LOG.md`。
- [CMR-005] **MAX_ROUNDS + deadlock**：到 MAX_ROUNDS（默认 5）仍不收敛时，输出 deadlock——列出每个未决点 + 主 agent 的反立场，交给用户裁决。禁止假装 approved。

细则见 [references/cross_model_review.md](references/cross_model_review.md)。登录限流场景的完整运行样例见 `examples/regression-login-rate-limit.md`。

## 何时加载

- **默认触发**：用户说 `cross-model-review` / `cross review` / "对抗审查" / "让两个模型审计划" / "model debate" / "stress-test PLAN.md" / "review PLAN.md" / "让 Gemini/Codex/Claude 审一下计划"。
- **接力 plan-grill**：plan-grill 锁定 PLAN.md 后，用户说"让另一个模型审查"则加载本 skill。
- **跳过**：没有 PLAN.md（先跑 plan-grill）；trivial 改动；用户明确"直接实施"。

## 与相邻 skill 的分工

| Skill | 分工 |
|-------|------|
| `plan-grill`（PG-001~004） | 盘问锁定 PLAN.md（Act 1） |
| **cross-model-review（本 skill）** | 跨模型对抗审查 PLAN.md（Act 2） |
| `problem-analysis`（PA-001~003） | 问题审查，先于 plan-grill |
| `historical-recall`（HR-001~005） | Act 1/2 动手前召回 `.plan-reviews/` 历史线索作待验证上下文 |
| `cognitive-reasoning`（GR-011~013） | 主 agent 仲裁时的真值接地纪律 |
