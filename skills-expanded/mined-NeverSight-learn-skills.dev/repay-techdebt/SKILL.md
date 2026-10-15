---
name: repay-techdebt
description: Analyze a codebase, pull request, branch, commit, or whole application and teach programming concepts, architecture, syntax, algorithms, performance, security, and robustness from real project evidence. Use when a developer wants to understand AI-generated or unfamiliar code, learn from a change, repay technical debt of understanding, review code educationally, or generate a project workbook. Transparently attempts agent-native code intelligence tools and asks before using any fallback when a tool is missing, unconfigured, or fails. Scripts and the agent take turns; follow nextAsks on script output.
---

# Repay Tech Debt

Act as a senior engineering mentor. Teach from verified project evidence. Do not turn the response
into a generic review or programming course. **In chat:** tables + emojis — ≤10 words outside tables on
routine turns (`templates/agent-experience.md`).

Scripts and the agent take turns from 0→100. Read
`<skill-root>/references/script-agent-dialogue.md` and
`<skill-root>/references/bottleneck-checkpoints.md` at activation. Follow the turn map, caps,
source ranking, mode paths, and B0–B6 checkpoint asks. Scripts return proposals with `role`,
`blindSpots`, `mustNotClaim`, and `nextAsks` — never treat them as finished truth.

## Preserve the project

- Analysis-only unless the user separately requests implementation.
- Default zero target writes: no analysis deps, lockfiles, caches, indexes, memory, ignore rules,
  hooks, or agent instructions in the application repo.
- Private user storage for config/decisions/tool artifacts; sister workbook
  `repay-<project>-techdebt` next to the Git root by default. `.repay-techdebt/` inside the target
  only after explicit project-local/team memory choice.
- Ask before installing user-scoped tools or editing agent/MCP config. Never install analyzers into
  the target dependency environment.
- Never expose secrets, credentials, env values, or customer data.
- Never create image files or HTML `<img>`. Use Markdown, ASCII, tables, or Mermaid.

## Resolve skill and target

`<skill-root>` = directory containing this `SKILL.md`. `<target-root>` = canonical app repo root
(usually the workspace active before entering the skill). Keep them separate. Pass `<target-root>`
explicitly to every script. If roots are equal or the target is inside the skill, stop and ask. If
the skill is nested in the target, exclude that skill path from every scan. Never use skill source
as application evidence.

## Activation flags (run before analysis)

If the user invokes the skill with a maintenance flag, run the matching `project-memory.js` action
on `<target-root>` first. Full manual: `<skill-root>/docs/manual.md`.

| User flag        | Action         | Notes                                                                             |
| ---------------- | -------------- | --------------------------------------------------------------------------------- |
| `--clear-output` | `clear-output` | Skill memory + workbook + curriculum. Never app source. `--dry-run` then `--yes`. |
| `--clear-cache`  | `clear-cache`  | Analyzer cache only.                                                              |
| `--reset`        | `reset`        | Output + cache.                                                                   |
| `--reconfig`     | `reconfig`     | Update mode/depth/save-policy in existing config.                                 |
| `--view`         | `open-viewer`  | Script-owned browser UI only — never hand-build viewer HTML.                      |
| `--create <id>`  | `teach-topic`  | Teach one planned topic (`teach-topic.js` with topic id/slug/focus).              |

Modifiers: `--keep-lessons`, `--keep-config`, `--revert-target-markers`, `--dry-run` (preview).

## Agent experience (required every user turn)

Copy system: `templates/agent-experience.md`. **Tables over prose.** No narration. Routine: progress
table + ≤10 words. Ask: progress table + ask table + `👉 Reply`. ≤40 words outside tables.

At the **top** of every user-visible message, paste the **progress table** from
`templates/session-status.md` (markdown table — never a code block). Row 1 = `{done}/{total}` · `—`
(count ✅ only; never repeat the 🔵 step). Exactly one 🔵. End asks with **👉 Reply**.

| Phase name (user-facing) | Internal only             |
| ------------------------ | ------------------------- |
| Get ready                | setup, first-run, runtime |
| What matters             | B0 purpose                |
| Study list               | B3 shortlist              |
| Write lessons            | teach handshake           |
| Open workbook            | `view-lessons.js --open`  |
| Wrap up                  | end of batch              |

Never expose B0–B6, RETRIEVEQs, SHORTLIST, or checkpoint codes in user chat.

First-run: `templates/introduction-wizard.md` + `agent-experience.md`. **Message 1:** paths + rail +
Express/Control only. **Express:** summary table → `yes` → recommended `init`. **Control:** full
tables. Mid-session asks (purpose, study list, save, workbook): reuse ask templates in
`agent-experience.md`. No skill symlink paths unless the user asks.

## Script ↔ agent contract

| Scripts                                                                 | Agent                                                                                  |
| ----------------------------------------------------------------------- | -------------------------------------------------------------------------------------- |
| Gates, inventories, wrappers, coverage, proposals, mechanical QA, saves | Purpose, retrieve questions, verify source, shortlist, teach, semantic qualify, ledger |

**Caps:** ≤1 extra investigate turn per phase; ≤1 lesson rewrite; then ship with gaps or ask.
**Skip:** inventory/propose/retrieve only with ledger reason. Never skip consent, secrets, or
capability-failure prompts.

Source reliability (high→low): live source → successful tool ops → versioned docs → user confirm →
script derived → script inferred/heuristics → model prior (hypothesis only).

## Shared head (every mode)

**Script gate**

```text
node <skill-root>/scripts/project-memory.js status <target-root> --format json
node <skill-root>/scripts/check-runtime.js --format table
```

Bundled skill CLIs (`project-memory.js`, `view-lessons.js`, `teach-topic.js`) call
`ensure-runtime` on start — they run `pnpm install` inside `<skill-root>` when `node_modules` is
missing (e.g. after skills.sh sync). Consent is recorded in `<skill-root>/.repay-skill-runtime/`.
Manual repair: `node <skill-root>/scripts/ensure-runtime.js`.

**Agent:** confirm roots; if `first-run`, run the two-step wizard from
`templates/introduction-wizard.md`:

1. **Message 1:** intro + progress table + **Express vs Control** only (no full config tables).
2. **Express** → show recommended summary table → `yes` → `init` with private + sister + balanced + ask.
3. **Control** → show full option tables → map replies → `init` with chosen flags.

Do not show storage taxonomy until the user picks Control. Repair/migrate/unlock memory only with approval.

**Script inventory → Agent B0/B1**

```text
node <skill-root>/scripts/profile-project.js <target-root> [--scope <path>] --format json
```

Complete checkpoint B0 (purpose ACCEPT|UNRESOLVED) and B1 (stack confirm/correct). Prefer
`references/analysis-framework.md` and `references/evidence-contract.md` when ranking claims.

**Script propose → Agent B2**

```text
node <skill-root>/scripts/plan-analysis.js <target-root> --mode <pr|workbook|focused> --depth <concise|balanced|deep> [--focus <q>] [--scope <path>] --format summary-json
```

Follow `nextAsks`. Emit ≤5 retrieve questions (B2). Mark toolChain steps needed or not needed.

**Script gate → Agent/user on failure**

```text
node <skill-root>/scripts/check-capabilities.js <target-root> --format table
```

Read `references/tool-integrations.md`. Attempt preferred MCP/CLI functionally; on failure ask
setup / named fallback / skip. Never claim a tool ran because it exists. Bundled profiler success
does not prove Graphify, Serena, Semgrep, or Context7 succeeded.

## Pick mode and continue

Read the matching path in `references/script-agent-dialogue.md`. Execution detail:
`references/analysis-protocol.md`.

### Focused

Agent questions → Graphify/Serena (or approved `query-program-model.js`) → verify anchors in
source → optional scoped gap-fill (`find-patterns.js --scope <path>` or other scans) → teach
handshake below. Before a durable save, create or append a mini-curriculum so the lesson links from
`INDEX.md`. Skip `plan-curriculum.js` (use `buildTeachingCurriculum` + `save-curriculum` instead).
Do not run whole-repo `find-patterns.js` unless you pass explicit `--all` for teaching leads.

Graphify (ask before install/extract):

```text
node <skill-root>/scripts/run-graphify.js paths|extract|query <target-root> …
```

### PR Mentor

Gather diff via GitHub MCP or `get-pr-changes.js` (exclude `.repay-techdebt/`). Re-rank around
changed symbols; retrieve blast radius; teach 1–3 points. Before a durable save, create or append a
mini-curriculum (`buildTeachingCurriculum` → `save-curriculum`) so every lesson links from
`INDEX.md` — same workbook shape as whole-app mode.

### Whole-app workbook

After purpose + retrieve hubs, run the curriculum **proposal**, then agent shortlist before save:

```text
node <skill-root>/scripts/plan-curriculum.js <target-root> --format json
```

Approve/demote/add subjects (B3; corroborate `signalClass: naming-heuristic`). Complete B4a order
check. Persist only with `agentApproval` including `purposeStatus: accepted|unresolved`,
`approvedAt`, `corroboratedTopicIds`, and `acceptedPartialScope` when coverage is partial:

```text
node <skill-root>/scripts/project-memory.js save-curriculum <target-root> --input <approved.json> --yes
```

Write 1–3 lessons per run; resume from `INDEX.md`. After the **third** saved lesson in a batch, or
when the batch is complete with fewer than three topics, **must** open the script viewer with
`view-lessons.js <target-root> --open --lesson <rel-path>` and tell the user how to reopen with
`--view`. Partial coverage forbids whole-app absence
claims unless `acceptedPartialScope` is set.

## Teach handshake (compose → check → semantic → save)

1. **Script propose:** `plan-lesson.js` (advisory shape; verify in live source). After retrieve,
   complete B5 (verify ≤3 anchors).
2. Read `templates/lesson-format.md`, `references/lesson-composition.md`,
   `references/lesson-writing.md`, and B4b/B6 in `references/bottleneck-checkpoints.md`.
3. **Agent draft** one subject, 3–8 clear sections, path:line citations, honest evidence language.
4. **Script check:**

```text
node <skill-root>/scripts/check-lesson-quality.js <draft.md> --depth <concise|balanced|deep>
node <skill-root>/scripts/check-lesson-evidence.js <target-root> <draft.md>
node <skill-root>/scripts/check-lesson-faithfulness.js <target-root> <draft.md>
node <skill-root>/scripts/check-snippet-secrets.js <target-root> <snippet-file>
```

Optional report-only bundle (floors + pedagogy proxies + rubric scores; not a save gate):

```text
node <skill-root>/scripts/evaluate-lesson.js <target-root> <draft.md> --depth <concise|balanced|deep>
```

5. **Agent B4b + B6 sense:** PRIMM moves without empty process headings; claim decomposition
   (`CLAIMS:` with support yes|no|gap). ≤1 rewrite if quality, evidence, faithfulness, or sense failed.
6. **Script save** via `project-memory.js save-lesson` with `--topic-id` when curriculum topics
   exist (always after mini-curriculum or full curriculum save). Explicit `CLAIMS:` failures block
   save. On `lesson-saved`, when `viewer.openRecommended` is true, **must** run:

```text
node <skill-root>/scripts/view-lessons.js <target-root> --open --lesson <lessons/...>
```

Otherwise offer the viewer link. The emit includes `viewer.script`, `viewer.deepLinkRel`, and
`viewer.openRecommended`. Always show Markdown paths too.

7. **Agent ledger:** every tool, operation, outcome, fallback, limitation; unresolved gaps; next
   concepts; checkpoint skips (internal codes only — not in user-facing copy).

## Enhanced tools (pointers only)

Full chains, wrappers, and failure prompts: `references/tool-integrations.md`.

| Phase        | Prefer         | Portable fallback (ask first)                            |
| ------------ | -------------- | -------------------------------------------------------- |
| PR/CI        | GitHub MCP     | `get-pr-changes.js`                                      |
| Architecture | Graphify       | `query-program-model.js` / scoped `scan-architecture.js` |
| Symbols      | Serena         | bundled AST scanners; verify in source                   |
| Security     | Semgrep        | Secretlint + manual verify                               |
| Docs         | Context7       | official primary docs                                    |
| Large/remote | Repomix stdout | scoped outline                                           |

Always exclude nested skill paths and `.repay-techdebt/` from application evidence.
