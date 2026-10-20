# Native Codex Specialist-Agent Policy

This repository uses Codex as the decision owner and native registered specialist agents as execution workers.

## Mandatory ownership

- Codex directly performs orchestration, requirements synthesis, architecture, planning, review, and final verdict/approval.
- Codex may inspect the repository and run read-only checks needed for planning or review.
- Native specialist agents perform bounded scouting, research, implementation, testing, documentation, design, database/performance/security scans, and DevOps work.
- Spawn the registered specialist role through Codexâ€™s native multi-agent system. Record the agent, model, access level, artifacts, acceptance criteria, and Codex verdict.
- Do not route work through external delegations or emulate a specialist when the registered role is available.

## Collaborative Agent Roles & Hierarchy

- **Orchestrator**: **GPT 5.6 Sol** (fallback **Opus 4.6**). Directs the workflow, issues commands, and delegates tasks to other agents.
- **Planner**: **Cline**. Runs in a persistent terminal in Orca, receiving prompts and workflow plans directly from the Orchestrator.
- **Reviewer & Deep Thinker**: **Claude Code** (with Bonsai-2 27B) and **Cline** (with Musespark v1.3). Responsible for logic validation, code review, architecture spotting, and executing heavy tasks requiring high cognitive effort.
- **Worker Light**: **Antigravity (agy)** with **Gemini Flash 3.8 High**. Handles scouting, simple implementation, and quick tasks.
- **Worker Hard**: **Antigravity (agy)** with **Gemini Pro 3.1 High**. Handles large-scale refactors and heavy implementation tasks.

## Persistent Terminal Execution (KV Cache Optimization)

- **NEVER close agent terminals.** To preserve KV Cache, save time, and reduce token quota waste, all CLI agents (`cline`, `claude`, `agy`) must run in persistent, continuously open terminals.
- When a task or prompt finishes, **do not exit the process** or close the terminal. Instead, start a new session or send the next prompt within the same open CLI process.

- `:team` means one Codex lead, up to three concurrent native read-only specialists, and at most one native writer.
- Read-only specialists must not modify the workspace; writer agents are serialized.
- Commit, push, and deploy require explicit user approval.
- Code/fix/test may be retried at most twice with review evidence. Never auto-retry deploy, commit, or push.
- Codex issues the final `PASS`, `CHANGES_REQUESTED`, or `BLOCKED` verdict.

## Native model routing

- Codex selects the native model appropriate to complexity and risk.
- Record the selected model and rationale in every specialist contract.
- Escalate high-risk security, data, or production work to the strongest available native specialist and require review evidence.

## Language

- Respond in the user's language.
- Code and comments are always English.
- **All Markdown (`.md`) files repo-wide are 100% English.** No Vietnamese (or any other non-English) prose in any `.md` file. This repo-wide rule (owner-directed, 2026-09-17) supersedes the narrower folder list below; pre-existing non-English `.md` files are grandfathered pending owner-approved conversion (see `plan.md` §5).
- Files under `.reports/`, `.documents/`, and `.brain/` are always English.

The authoritative global rules are managed by the core AI configuration.

## Shared handoff (mandatory)

This repository uses a **single shared handoff** so that any agent (or human) can continue work without losing context or overwriting someone else.

Read, in order:

1. `AGENTS.md` — this policy
2. `.brain/HANDOFF_PROTOCOL.md` — **mandatory** collaboration protocol
3. `.brain/README.md` — which handoff is current
4. the newest `.brain/BRAIN_PACKAGE_<YYYY-MM-DD>.md` — full project context
5. `.brain/brain.json` — business decisions ("why")
6. `src/architecture_guardrails.md` — before touching the 4-phase pipeline

Rules:

- The newest `BRAIN_PACKAGE_*.md` is the single source of truth for **context ("why")**. Git remains the source of truth for **code ("what")**.
- Only **one writer agent** may modify `.brain/` at a time; read-only specialists MUST NOT modify it.
- Handoff files are **immutable**: never edit a packaged handoff — create a new dated one and update `.brain/README.md`.
- Update the handoff whenever you: change prod directly, deploy, change a business rule or architecture, add/remove env vars/credentials, find a new blocker or risk, or finish a large task.
- Never write secrets (API keys, tokens, passwords, `.env` contents) into `.brain/`.

Full protocol: `.brain/HANDOFF_PROTOCOL.md`

---

<!-- gitnexus:start -->
# GitNexus â€” Code Intelligence

This project is indexed by GitNexus as **PM_QUANLY_SH** (11180 symbols, 21401 relationships, 300 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> Index stale? Run `node .gitnexus/run.cjs analyze` from the project root â€” it auto-selects an available runner. No `.gitnexus/run.cjs` yet? `npx gitnexus analyze` (npm 11 crash â†’ `npm i -g gitnexus`; #1939).

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows. For regression review, compare against the default branch: `detect_changes({scope: "compare", base_ref: "main"})`.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol â€” callers, callees, which execution flows it participates in â€” use `context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace â€” use `rename` which understands the call graph.
- NEVER commit changes without running `detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/PM_QUANLY_SH/context` | Codebase overview, check index freshness |
| `gitnexus://repo/PM_QUANLY_SH/clusters` | All functional areas |
| `gitnexus://repo/PM_QUANLY_SH/processes` | All execution flows |
| `gitnexus://repo/PM_QUANLY_SH/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->

