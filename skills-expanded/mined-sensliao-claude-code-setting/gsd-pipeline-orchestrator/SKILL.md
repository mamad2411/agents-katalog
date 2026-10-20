---
name: gsd-pipeline-orchestrator
description: >-
  Master GSD pipeline orchestrator — classifies the current phase, composes the right Tier 1-4 command sequence, embeds agent-team orchestration (single / parallel fan-out / GAN / santa-loop / convergence), and bridges GSD with the front-end UI combo. Invoke ONCE before any non-trivial work: planning and building a feature, starting a project or a new phase, a cross-module refactor, or picking up where the last session left off. Triggers: "let's plan and build X / add a new feature / start a new project / start the next phase / cross-module refactor / continue where we left off / how should I run GSD on X / 开新项目 / 开新 phase / 新功能 / 跨模块改造 / continue 上次 GSD". Skip for 1-3 line bugfixes, reading code, or when the user says no-GSD.
argument-hint: "[phase number or milestone | --classify-only | --print-plan]"
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - AskUserQuestion
  - SlashCommand
  - Skill
  - Agent
---

<objective>
For any non-trivial work in a GSD-managed repo, this skill:

1. **Classifies** the active phase against 8 dimensions (ambiguity, UI, AI, architecture, security, core-logic, CRUD, milestone-boundary).
2. **Composes** the exact ordered list of `gsd-*` commands across 4 tiers — baseline + pre-plan + pre-verify + (optional) milestone boundary.
3. **Embeds** agent-team orchestration into each step — when to run a single agent, when to fan out in parallel, when to invoke GAN-style adversarial loops, when to bring in external AI via Codex.
4. **Bridges** GSD's `gsd-ui-phase` (which only produces UI-SPEC.md contracts) with the user's actual front-end 5-skill design combo (ux-principles + prototyping-ui-directions + taste-skill + anchor-prototype-wave + luxury-editorial-site-builder).
5. **Prints the plan** for user confirmation before executing, then dispatches commands serially. **Stops on first failure**, reports the failed command + artifact + next-action exactly.

This is a meta-orchestrator. It does NOT do work itself — it picks which GSD commands and agent patterns do the work.

**Execution mode: SKILL-direct only** (2026-05-29 user lock) — GSD pipeline orchestrator does **NOT** migrate to Workflow tool workflow-spec mode. Reason: 33 gsd-* agents already orchestrate well via SKILL main thread + slash commands; the multi-cycle checkpoint patterns (`gsd-debug-session-manager`), human-in-the-loop pauses (`gsd-ui-checker` BLOCK/FLAG verdicts), and parallel-research-to-synthesis fan-ins are inherently NOT single-pass DAGs and would lose semantics if forced into workflow-spec. Continue dispatching via SKILL `Skill(...)` / `Agent(...)` / `SlashCommand`. See `~/.claude/CLAUDE.md §3.5` for migration scope decision.
</objective>

<when_to_invoke>

**Required invocation (auto):**

- User says "开新项目 / 开新 phase / 新功能 / 跨模块改造 / 接手这个仓库重新跑 GSD"
- User says "继续 GSD / 接着上次"
- Milestone is about to be closed
- A failed pipeline needs to be resumed and the next step is unclear

**Skip invocation:**

- 1-3 line bugfix
- Answering a question / reading code / explaining behavior
- User explicitly says "不用 GSD / 直接做 / 小事"
- Single-file utility extraction with no behavior change

</when_to_invoke>

<entry_situation_router>

### Tier 0 — Entry-Situation Router（G2 · 2026-06-14：接手 / 探索 / 恢复 / 审计 等**非 phase 入口**先走这里，再进 Tier 1-4）

> 起因：本编排器原先默认"已在 phase 执行语境"直接跑 Tier 1-4，但上游 GSD 命令集远不止 phase 流水线。命中下列入口场景时，先 dispatch 对应命令（`Skill(...)` / `SlashCommand`），完成后再回 `<phase_classifier>` 跑 Tier 1-4。**按场景动态选，不全跑。**

| 入口场景 | 命令 |
|---|---|
| 全新项目起步 | `/gsd-new-project`（深度 context → PROJECT.md），再进 Tier 1 |
| 接手陌生库 / 无 `.planning` 的已有代码 | `/gsd-map-codebase`（并行 mapper → `.planning/codebase/`）+ `/gsd-ingest-docs`（已有 ADR/PRD/SPEC 合并）；需历史考古 → `/gsd-import` · `/gsd-forensics` |
| 旧文档散落要 bootstrap `.planning/` | `/gsd-ingest-docs` |
| 超复杂 / 高歧义规划 | `/gsd-ultraplan-phase`（替代 `/gsd-plan-phase`，更深多轮）；明确小事 → `/gsd-quick` |
| 先验证可行性 / 探索 | `/gsd-spike`（throwaway 验证）· `/gsd-sketch` · `/gsd-explore` · `/gsd-surface` |
| 暂停 / 跨 session 恢复 | `/gsd-pause-work`（写 handoff）· `/gsd-resume-work` · "接着上次" → 输出 Format C resume |
| 健康 / 进度 / 统计 | `/gsd-health` · `/gsd-progress` · `/gsd-stats` |
| 想法 / 任务 / backlog 捕获 | `/gsd-capture` · `/gsd-inbox` · `/gsd-review-backlog` · `/gsd-thread` |
| 审计 | `/gsd-audit-uat`（跨 phase UAT）· `/gsd-audit-fix`（find→fix→test→commit）· `/gsd-audit-milestone` |
| 依赖 / 影响图 | `/gsd-graphify`（`.planning/graphs` typed 节点/边） |
| 多工作流并行 / 工作区 | `/gsd-workstreams` · `/gsd-workspace` |
| 回滚 / 撤销 | `/gsd-undo` |
| 多周期调试 | `/gsd-debug`（持久 debug state；详 `<agent_orchestration_overview>` situation 表） |

完成入口命令后 →（若进入 phase 实施）回 Tier 1-4；纯维护 / 查询类（health / stats / progress / capture）跑完即止，不强进 phase 流水线。

</entry_situation_router>

<phase_classifier>

Given the active phase number `N` (or "new milestone"), read available state first:

- `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md`, `.planning/STATE.md`
- `.planning/phases/N-*/CONTEXT.md`, `PLAN.md`, `UI-SPEC.md`, `AI-SPEC.md`, `VALIDATION.md`, `SECURITY.md`, `UAT.md` if present
- Repository structure relevant to the phase

Then evaluate 8 booleans:

| Flag | True when |
|---|---|
| `AMBIGUOUS_REQUIREMENTS` | Goal, acceptance criteria, user story, API contract, data model, or success condition is unclear in CONTEXT.md / SPEC.md |
| `FRONTEND_OR_UI_HEAVY` | Phase touches React / Next.js / Vue / Svelte / SwiftUI / macOS UI / CSS / Tailwind / shadcn / layout / copy / design system / visual states / accessibility / interaction |
| `AI_INTEGRATION` | Phase touches LLM calls (Claude / OpenAI / Gemini), agents, prompts, evals, RAG, embeddings, vector stores, MCP AI tools, AI classification / summarization / extraction / routing, or model-output quality |
| `CRITICAL_ARCHITECTURE_OR_NEW_FRAMEWORK` | Phase introduces a major architectural decision, new framework, new persistence model, new integration boundary, multi-repo coordination, new agent harness, or cross-service contract |
| `SECURITY_SENSITIVE` | Phase touches auth, authorization, sessions, secrets, tokens, payments / money / billing, database writes, PII, permissions, network egress, file deletion, destructive ops, prod data, admin controls, or supply-chain-sensitive package install |
| `CORE_LOGIC_TDD_RECOMMENDED` | Phase touches business logic, API behavior, algorithmic logic, state machines, database logic, data transformation, validation, backend workflows — anywhere regression tests should drive implementation |
| `ORDINARY_CRUD` | Simple create/read/update/delete, low security risk, no AI, no major UI complexity, no new framework, no core algorithmic behavior |
| `MILESTONE_BOUNDARY` | All phases in current milestone are complete and user is closing or rolling over the milestone |

</phase_classifier>

<master_pipeline>

Compose the pipeline by walking these tiers in order. **Run commands serially. Stop on first failure.**

---

### Tier 1 — Required Baseline (always)

1. If `AMBIGUOUS_REQUIREMENTS`: `/gsd-spec-phase N`
2. Always: `/gsd-discuss-phase N --analyze`
3. **→ Insert Tier 2 commands here**
4. Plan:
   - If `CORE_LOGIC_TDD_RECOMMENDED`: `/gsd-plan-phase N --tdd`
   - Else: `/gsd-plan-phase N`
5. If `CRITICAL_ARCHITECTURE_OR_NEW_FRAMEWORK` or `SECURITY_SENSITIVE`:
   - `/gsd-plan-review-convergence N --codex --max-cycles 3`
6. Execute: `/gsd-execute-phase N`
7. Review + auto-fix: `/gsd-code-review N --fix --auto`
8. **→ Insert Tier 3 commands here**
9. Verify: `/gsd-verify-work N`
10. Ship:
    - `/gsd-pr-branch main`
    - `/gsd-ship N` — **governed release gate** (CLAUDE.md §3.7): the ship verdict comes only from the deterministic spec-runner + `spec_hash` human approval + evidence; Dynamic Workflows / ultracode may scout candidates but NEVER produce a release verdict, and there is no self-approval.
11. Sediment: `/gsd-extract-learnings N`

---

### Tier 2 — Pre-Plan Phase-Type Inserts

Insert BEFORE `/gsd-plan-phase` (after step 2, before step 4).

| Trigger | Insert |
|---|---|
| `FRONTEND_OR_UI_HEAVY` | `/gsd-ui-phase N` **THEN run UI bridge** (see [ui-bridge.md](references/ui-bridge.md)) — the bridge invokes the 5-skill front-end combo before returning to `/gsd-plan-phase` |
| `AI_INTEGRATION` | `/gsd-ai-integration-phase N` |
| `ORDINARY_CRUD` and no other flag | (nothing — skip Tier 2) |

---

### Tier 3 — Pre-Verify Quality Gates

Insert AFTER `/gsd-code-review --fix`, BEFORE `/gsd-verify-work` (after step 7, before step 9). Run all matching, in this order:

1. `AI_INTEGRATION` → `/gsd-eval-review N`
2. `SECURITY_SENSITIVE` → `/gsd-secure-phase N`
   - **G1（2026-06-14）— 高危子集额外升级到企业级编排器**：当 phase 命中高危子集（payment / 钱 / billing · auth / authz / sessions / tokens · admin controls · prod data · PII · multi-tenant · file-upload · GenAI-agent surface），除 `/gsd-secure-phase` 外**额外**（不是替代）route 到：
     - `Skill("appsec-security-orchestrator")` — 完整 defensive（威胁建模 + R&C lens / SAST·SCA·secrets·IaC / ASVS 5.0 / 修复路由），而非仅内置薄版；
     - `Skill("enterprise-qa-testing")` release gate — 高危 phase 上线前走 `/qa-release-readiness`；支付 / 合规走 `/qa-commercial-cert`（强制 budget approval）。
   - 普通 `SECURITY_SENSITIVE`（低危、无上列触发）维持仅 `/gsd-secure-phase`，不强拉重编排器（动态按上下文选，绝不每次全跑）。
   - **边界**：active scan / pentest 永远 manual + ROE 双门；AppSec / QA 的 release verdict 走各自 deterministic spec-runner + `spec_hash` 人类审批，GSD **不自签**（§3.7 governed gate）。
3. `CORE_LOGIC_TDD_RECOMMENDED` and plan was NOT `--tdd` → `/gsd-add-tests N`
4. Plan WAS `--tdd` and phase is high-impact → `/gsd-validate-phase N`
5. (None apply) → skip Tier 3

---

### Tier 4 — Milestone Boundary (only when `MILESTONE_BOUNDARY`)

Not per-phase. Only at milestone close:

1. `/gsd-audit-milestone`
2. `/gsd-complete-milestone`
3. `/gsd-cleanup`
4. `/gsd-milestone-summary`
5. `/gsd-new-milestone`

</master_pipeline>

<agent_orchestration_overview>

GSD commands already encapsulate their own internal agent fan-out (e.g., `gsd-plan-phase` spawns `gsd-pattern-mapper` + `gsd-phase-researcher` + `gsd-planner` + `gsd-plan-checker` in parallel). At the master-pipeline level, the orchestrator decides:

1. **When to run STANDALONE agents OUTSIDE GSD commands** — typically after `/gsd-code-review --fix` to add extra perspectives.
2. **When to invoke ADVERSARIAL loops** — santa-loop (dual reviewer must both approve) or plan-review-convergence (Codex external).
3. **When to use GAN-style PLANNER / GENERATOR / EVALUATOR teams** — for high-craft features (interactive UI prototype iteration, eval-driven AI features).
4. **When to delegate to Codex** — long-chain施工 / parallel grunt work / cross-AI review.

The 7 orchestration patterns are documented in detail in [agent-orchestration-patterns.md](references/agent-orchestration-patterns.md). Quick decision table:

| Situation | Pattern | Key agents / tools |
|---|---|---|
| Default after writing code | **Single-agent review** | `code-reviewer` (sonnet) |
| Security-sensitive change | **Parallel fan-out review** | `code-reviewer` + `security-reviewer` + (if web) `typescript-reviewer` in parallel, all opus |
| Architecture / new framework plan | **Plan-review convergence** | `/gsd-plan-review-convergence --codex` until no HIGH concerns |
| Ship-critical merge | **Santa-loop dual review** | Two independent reviewers must both approve; invoke via `/santa-loop` |
| High-craft interactive UI feature | **GAN team** | `gan-planner` → `gan-generator` ↔ `gan-evaluator` (loop until threshold) |
| Long parallel施工 / cross-AI review | **Codex delegation** | Codex official plugin `codex@openai-codex` — `/codex:rescue` (delegate) · `/codex:review` / `/codex:adversarial-review` (review); quota out → Claude subagent |
| Multi-cycle debug | **Debug session manager** | `gsd-debug` (internally manages debugger sub-agents + checkpoints) |
| 4+ parallel research tasks | **Research fan-out** | Spawn 4 parallel `Agent(subagent_type=Explore)` or research agents in one message |

**Model routing reminder** (per `~/.claude/rules/common/performance.md`):

- **Opus**: planner / architect / security-reviewer / final reviewer in santa-loop / GAN evaluator
- **Sonnet**: code-reviewer / tdd-guide / build-resolver / day-to-day agents / GAN generator
- **Haiku**: doc-updater / format conversion / simple routing
- For **large multi-step tasks (gsd-execute-phase, big planners, large reviews)** prefer **Opus** over the Sonnet default (per the model-routing rules in `~/.claude/CLAUDE.md` §4.5 + `rules/common/performance.md`) — Sonnet's mid-task compaction loses quality.

**Parallel-vs-serial scheduling discipline** (per `~/.claude/CLAUDE.md` §4.5 Universal Execution Discipline rule 1 + `~/.claude/rules/common/agents.md`):

- 能并行（互不依赖）→ **必须并行**：单 message 多 Agent call，不可串行浪费 wall time
- 必须串行（输出→输入 / 同文件 write / 同资源 race）→ **必须串行**：等上游 return 再开下游
- 强制思考依赖再调，不是"默认并发"也不是"默认串行"
- 此规则**全局适用**，不限于本 orchestrator 范围——任何 spawn agent / 任何 tool call 都遵守

</agent_orchestration_overview>

<planner_context_discipline>

> **Added 2026-05-26 — 缘起：Agent Atlas Phase 1 的 4 处 PLAN.md 错误根因分析（详本节末「Why this discipline exists」+ planner-discipline 规则见 `~/.claude/CLAUDE.md` §4.5 Orchestration Hygiene）。**

When this orchestrator composes the `/gsd-plan-phase` step (Tier 1 step 4), it MUST enforce two pre-spawn discipline rules. These exist because the planner agent works only from `<files_to_read>` + general LLM knowledge — if external service contracts (Vercel Cron HTTP verb, Supabase RLS edge cases, Stripe webhook semantics, platform IP allowlist availability) are not in its reading list, it will invent plausible-but-wrong assumptions, and the resulting PLAN.md ships factual errors that surface only at execute-time.

### 1. Platform skill auto-injection（must-do before spawning planner）

Before invoking `/gsd-plan-phase` (or directly spawning `gsd-planner` Agent), this orchestrator reads:
- `.planning/PROJECT.md` — Tech Stack section
- `.claude/manifest.json` — installed skills array (bootstrap-time inventory)
- `package.json` — installed deps (last resort fallback)

Then matches detected platforms / libraries to the corresponding skill SKILL.md, and adds them to the planner's `<files_to_read>` block:

| Detected in stack | Inject into planner reading list |
|---|---|
| Next.js / Vercel | `Skill(vercel:nextjs)` + `Skill(vercel:vercel-functions)` + `Skill(vercel:routing-middleware)` — plugin skills, NOT local dirs (any cron / scheduler endpoint MUST include these — Vercel Cron is HTTP GET, not POST) |
| Supabase | `~/.claude/rules/web/security.md` RLS section + any `supabase-*` skill if installed |
| Stripe / payment | `~/.claude/skills/security-compliance-payment/SKILL.md` (webhook HMAC / idempotency / replay window patterns) |
| Docker / Kubernetes / Terraform / Ansible | `~/.claude/skills/env-parity-baseline/SKILL.md` (cross-env IP / DNS / secret-mgmt drift) |
| Anthropic Claude API | `Skill(claude-api)` — plugin skill, NOT a local dir (model ids / pricing / prompt caching / model migration / tool use) |
| iOS / SwiftUI / macOS | No dedicated skill — instruct planner to consult Apple HIG via web/docs lookup (`docs-lookup` skill) for platform conventions; do not point at a local path |
| Android / Kotlin / Compose | `kotlin-reviewer` agent definition + relevant skills if installed |
| Vertex AI / Google Cloud | Vercel AI Gateway docs + GCP IAM rules (no dedicated skill yet — log gap to STATE.md) |

If platform detected but no matching skill exists locally, log gap in `.planning/STATE.md` Blockers/Concerns and proceed (do not block planner).

### 2. Plan-checker enforcement (gsd-plan-phase Step 10)

`gsd-plan-phase` workflow's Step 10 (spawns `gsd-plan-checker` agent) MUST run unless user passes explicit `--skip-verify`. When this orchestrator composes the plan-phase invocation:

- **DO NOT add `--skip-verify` to "save time / token"** — plan-checker catches cross-plan consistency (e.g., date semantics drift across 3 plans), depth-of-thinking gaps (e.g., missing advisory lock for cost containment), and external-contract assumptions that the planner alone won't catch.
- If a session has already produced PLAN.md without plan-checker (e.g., manual recovery / partial chunked run / token-budget shortcut), this orchestrator's responsibility is to **retroactively spawn `gsd-plan-checker`** before composing further steps.
- Plan-checker run is a fixed ~5-10k token cost; a shipped factual bug costs significantly more in execute-time rework.

### 3. Coordinate with §<agent_orchestration_overview> scheduling rules

When the planner agent spawns its own sub-agents (gsd-pattern-mapper, gsd-phase-researcher, etc.), the parallel-vs-serial rule above applies recursively. This orchestrator does not need to micromanage that — the planner agent's prompt template already encodes it. But this orchestrator SHOULD verify the planner's `model` parameter is `opus` (per model routing — planner is decision layer).

### Why this discipline exists (in one paragraph)

On 2026-05-26 Agent Atlas Phase 1 the orchestrator (operating in single-Claude session, no formal `gsd-pipeline-orchestrator` invocation) bypassed both rules above to "save tokens". Result: 5 PLAN.md files shipped with 4 factual / consistency errors — Vercel Cron written as POST handler (Vercel sends GET); daily directive target-date semantics inconsistent across 3 plans; cron lacked per-agent advisory lock (concurrent dual-invoke could burn LLM+Places cost before INSERT dedup); Vercel IP allowlist assumed available on hobby tier (only Pro+ Static IPs / Enterprise Secure Compute). Cost of rework ≫ cost of running the 2 disciplined steps.

</planner_context_discipline>

<ui_bridge_overview>

GSD's `/gsd-ui-phase` produces **UI-SPEC.md** — a design *contract* (surfaces, states, interactions, accessibility, data shape). It does NOT produce the actual visual design, palette, typography, motion, or hi-fi mock.

For any phase where `FRONTEND_OR_UI_HEAVY` is true, the master pipeline MUST bridge `/gsd-ui-phase` to the user's front-end 5-skill combo before going to `/gsd-plan-phase`. The full bridge spec is in [ui-bridge.md](references/ui-bridge.md). Summary:

```
/gsd-ui-phase N                       ← produce UI-SPEC.md contract (WHAT)
   ↓
Front-end 5-skill combo:              ← actual design (HOW it looks)
   1. ux-principles MODE A (pre)        — laws-of-UX + heuristic pre-check
   2. (if no anchor yet) prototyping-ui-directions Stage 0-3
      OR (if anchor locked) taste-skill (single surface)
      OR (if locked + 4-15 surfaces) anchor-prototype-wave
      OR (if luxury brand landing) luxury-editorial-site-builder
   3. ux-principles MODE C (post audit) — NN 10-heuristic + Built-for-Mars 5-lens
   ↓
Backfill UI-SPEC.md with locked tokens / chassis / surface inventory
   ↓
/gsd-plan-phase N                     ← plan tasks against the locked visual contract
```

**Hard rule:** Do NOT enter `/gsd-plan-phase` while the visual chassis is unlocked. Tasks planned against a vague visual contract will need re-work.

</ui_bridge_overview>

<project_default_mappings>

Per-project defaults are in [project-mappings.md](references/project-mappings.md). High-level:

| Project | Default behavior |
|---|---|
| **AI agents 应用 / dashboard** | This repo. UI-heavy + tech-db scanning + local services. Almost every phase → Tier 1 + Tier 2 UI bridge. Docker-only verify (memory rule). |
| **UniBoard** | FastAPI + Next.js + Supabase + Claude API. AI + UI heavy → Tier 1 + ui-phase + ai-integration-phase + eval-review. Auth/billing/RLS → secure-phase. |
| **Borealis Fabrics / New Sight** | Production live. Conservative. Auth/data writes → secure-phase. Core backend → `--tdd`. |
| **canvas-ed-mcp** | MCP server. Protocol changes → `--tdd`. Issue/PR backlog → `/gsd-inbox`. |
| **ClaudePulse** | Swift HUD. UI-heavy → `/gsd-ui-phase` + taste-skill. Local file/process access → secure-phase. |

</project_default_mappings>

<execution_rules>

1. **Classify first, then compose.** Never start running commands before classifying the 8 flags.
2. **Print the pipeline plan to the user FIRST.** Show the ordered command list with reasons (which flag triggered which insert). Wait for user confirmation unless they've said "直接做" or "--print-plan" mode.
3. **Run serially.** No skipping, no reordering. Tier 2 before plan. Tier 3 after code-review, before verify.
4. **Stop on first failure.** Report:
   - Exact command that failed
   - What failed (error message / failed agent / failed verification)
   - Which artifact appears affected
   - Exact next command or user decision needed
5. **Never silently skip Tier 1 steps** unless user explicitly says skip-this-step.
6. **Plan-review convergence runs BETWEEN plan and execute** — not before plan, not after execute.
7. **Tier 3 quality gates run AFTER code-review-fix, BEFORE verify** — they may surface gaps that need fixing before UAT.
8. **Prefer durable artifacts over chat memory.** Trust `.planning/STATE.md` and phase artifacts over conversational assumptions.
9. **If user says "continue" or "接着上次":** Read `.planning/STATE.md` + phase artifacts, determine the next correct command in this pipeline, propose it, then run.
10. **If user requests a shortcut:** Preserve security + AI eval + verify gates unless they explicitly accept the risk in writing.
11. **End-of-phase summary** (after successful Tier 1 step 11):
    - Phase number + name
    - Commands run (in order)
    - Artifacts produced (`.planning/phases/N/**`)
    - Tests / evals / security checks completed
    - PR / ship status
    - Learnings extracted
12. **Planner context discipline (added 2026-05-26, gates Tier 1 step 4):** Before composing `/gsd-plan-phase` invocation, run platform-skill auto-injection per `<planner_context_discipline>` §1 (read `.planning/PROJECT.md` Tech Stack → inject matching SKILL.md into planner's `<files_to_read>`) AND ensure `gsd-plan-checker` Step 10 will execute (do NOT add `--skip-verify` to "save time"). Retroactively run plan-checker if a prior session produced PLAN.md without it. Skipping these = factual API errors + cross-plan inconsistency leaks (proven by 2026-05-26 Agent Atlas Phase 1).
13. **R&C lens coverage (added 2026-05-26):** When Tier 3 step 2 routes to `/gsd-secure-phase` or any threat-modeling skill is invoked, the threat model output MUST include §3.5 R&C Register (retry storms / concurrent invocation / unbounded resource / failure cascade / cost runaway / capacity ceiling) per `security-governance-threat-modeling §6.5`. STRIDE alone is attacker-centric; R&C catches benign-but-expensive failure modes (cron retry burning cost, platform-tier capacity ceiling, etc.).

</execution_rules>

<output_format>

When invoked, output ONE of these three formats:

### Format A — Plan only (`--print-plan` or `--classify-only`)

```markdown
## GSD Pipeline — Phase {N} | {phase-name}

### Classification
- AMBIGUOUS_REQUIREMENTS: {true/false}
- FRONTEND_OR_UI_HEAVY: {true/false}
- AI_INTEGRATION: {true/false}
- CRITICAL_ARCHITECTURE_OR_NEW_FRAMEWORK: {true/false}
- SECURITY_SENSITIVE: {true/false}
- CORE_LOGIC_TDD_RECOMMENDED: {true/false}
- ORDINARY_CRUD: {true/false}
- MILESTONE_BOUNDARY: {true/false}

### Composed Pipeline ({K} steps)
1. `/gsd-spec-phase N` — (AMBIGUOUS_REQUIREMENTS=true)
2. `/gsd-discuss-phase N --analyze` — (Tier 1 baseline)
3. `/gsd-ui-phase N` — (FRONTEND_OR_UI_HEAVY=true, Tier 2)
4. **UI bridge — 5-skill front-end combo** (see ui-bridge.md)
5. `/gsd-plan-phase N --tdd` — (CORE_LOGIC_TDD_RECOMMENDED=true)
6. ...

### Agent / Team Orchestration
- Step X: parallel fan-out review — code-reviewer + security-reviewer + typescript-reviewer (all opus, parallel)
- Step Y: GAN team — gan-planner → gan-generator ↔ gan-evaluator
- ...

### Artifacts Expected
- `.planning/phases/N/{SPEC,CONTEXT,UI-SPEC,PLAN,...}.md`
- `dashboard/...` source edits
- PR #...

Confirm to run? (yes / modify / cancel)
```

### Format B — Run mode (default)

Print Format A, wait for confirmation, then dispatch commands one at a time via `Skill()` or `SlashCommand()`. After each command:

- Confirm success (artifact written / exit code 0 / no blocking issues)
- Update progress to user with a one-line status
- On failure, halt and report per Execution Rule 4

### Format C — Resume mode (`continue` / "接着上次")

Read `.planning/STATE.md`. Identify the current phase + last-completed command. Compute the next step in this pipeline. Print:

```markdown
## GSD Resume — Phase {N}

Last completed: `/gsd-X N` (at {timestamp})
Next step in pipeline: `/gsd-Y N`
Reason: {why this is next per Tier rules}

Run next step? (yes / show full remaining pipeline / cancel)
```

</output_format>

<anti_patterns>

Do NOT:

- Skip the classification step "because the phase looks obvious"
- Run `/gsd-plan-phase` before the UI bridge completes (visual chassis must be locked first)
- Run `/gsd-execute-phase` before `/gsd-plan-review-convergence` when architecture is critical
- Run `/gsd-verify-work` before `/gsd-eval-review` when AI is in scope
- Run `/gsd-ship` before all Tier 3 gates pass
- Manually edit `.planning/phases/N/*.md` after `/gsd-ship` to "patch in" missed items — re-run the correct GSD command instead
- Fan out 6+ parallel agents when 2 sequential would do — token cost vs. signal
- Default the GAN team for ordinary CRUD — it's for high-craft features

</anti_patterns>

<see_also>

- [agent-orchestration-patterns.md](references/agent-orchestration-patterns.md) — 7 patterns with examples
- [ui-bridge.md](references/ui-bridge.md) — GSD ↔ 5-skill UI combo handoff
- [project-mappings.md](references/project-mappings.md) — per-project defaults
- Global `~/.claude/CLAUDE.md` — GSD 启动协议, 11 能力位, 前端 4-skill 组合工作流
- Project `CLAUDE.md` — repo-specific overrides (e.g. dashboard Docker-only verify rule)

</see_also>
