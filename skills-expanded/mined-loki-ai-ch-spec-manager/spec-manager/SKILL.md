---
name: spec-manager
description: Spec-driven project iteration workflow: L1 PRD -> L2 Design -> L3 Impl -> Agent Task, with human review gates at each layer.
allowed-tools: Read, Write, Grep, Glob, Bash(spec-manager:*), Bash(git:*)
---

# spec-manager

Use this skill when the user invokes `/spec-manager`, asks for a new feature, PRD, technical design, implementation spec, agent task, iteration plan, test plan, release notes, runbook, postmortem, ADR, or delta change.

## Entry Points

- `/spec-manager <request>` — start from the user's requirement and route to the right subskill.
- `/spec-manager run <taskId>` — execute an existing Agent Task.

For new or non-trivial work, first identify the safe next step or generate an Agent Brief:

```bash
spec-manager next "<work>"
spec-manager brief "<work>"
```

During execution use `spec-manager assist next <taskId> --spec <L3-code>` / `spec-manager assist drift <taskId> --spec <L3-code>` when useful; before final handoff use `spec-manager assist acceptance <taskId> --spec <L3-code>`, then `spec-manager assist delivery <taskId> --spec <L3-code>`.

## Unified Rules

- Feature work MUST go through `spec-manager`.
- New or non-trivial work follows L1 -> L2 -> L3 -> Agent Task.
- Never write implementation code without a frozen L3 spec.
- L1/L2 approval advances `draft -> confirmed`; one explicit L3 approval (an explicit user approval) advances `draft -> frozen`.
- For new or non-trivial work, start with `spec-manager next "<work>"` or `spec-manager brief "<work>"`.
- For agent setup guidance, prefer `spec-manager <platform> install`; use `spec-manager agents install` / `spec-manager skills install` for cross-framework install, and keep `spec-manager project agents --provider <provider>` as the compatible advanced form.
- Before writing any spec/task/decision, check `spec-manager project context --json` or `spec-manager dashboard --json` and confirm the resolved `writeRoot`; external `specStore.path` means writes go to that specs root, while `contextSources` are read-only.
- Before final handoff, generate an acceptance summary with `spec-manager assist acceptance <taskId> --spec <L3-code>` and a user-facing delivery summary with `spec-manager assist delivery <taskId> --spec <L3-code>`.
- Before code edits, read the frozen L3 spec and create/start an Agent Task.
- When the user asks to "confirm and run", "create and execute the task", "continue executing this L3", or uses equivalent wording, prepare an explicit planJson file and use `spec-manager task run <L3-code> --plan <planFile>`.
- When the L3 is already frozen and the user asks to create and execute its task, use `spec-manager task create <L3-code> --plan <planFile> --start`; keep separate `task create` and `task start` commands as the compatible troubleshooting path.
- When the user only asks to confirm/freeze an L3 or gives `spec-manager spec confirm <L3-code>`, only run `spec-manager spec confirm <L3-code>` and stop; do not create a task automatically.
- planJson `coveredSpecs` MUST include the current L3 specCode.
- If adaptive workflow is enabled, Task creation records a `standard` or `governed` Profile snapshot; `governed` requires the frozen L3 to declare `## 关键验收标准` with valid AC IDs, and task complete requires successful verification evidence covering every critical AC. `standard` reports missing coverage as warnings. Use `spec-manager project profile recommend --request "<work>"` for a deterministic, explainable recommendation; it does not auto-enable adaptive workflow and is not a hidden gate. Use `spec-manager project profile metrics [--topic <topic>] [--json]` for a read-only governance report over Profile adoption, governed coverage gaps, standard warnings, and explicit overrides; metrics does not modify config or historical Tasks. Use `spec-manager project readiness critical [--topic <topic>] [--json]` for a read-only critical AC readiness report and repair suggestions; it must not auto-generate or insert critical AC. Before enabling adaptive workflow, use `spec-manager project workflow preview [--json]` for a read-only adoption preview; preview does not write config, migrate historical Tasks, or act as an enable gate.
- For UI/visual/style work, `specs/DESIGN.md` in the resolved write root is the canonical managed design context, with root `DESIGN.md` retained as a legacy fallback. Use `spec-manager brief "<UI request>"` to read the default design context, `spec-manager assist design-template` to create starter `specs/DESIGN.md`, and `spec-manager assist design-export --format tokens-json` when implementation tooling needs tokens. Pass `--path DESIGN.md` or `--path specs/DESIGN.md` only when a specific file must be forced. Use `--format dtcg-json` for the current schema's DTCG subset, `--format tailwind-json` for Tailwind v3 `theme.extend`, and `--format tailwind-css` for Tailwind v4 `@theme`; exports do not modify project Tailwind config files. Use `@verify: design-lint(DESIGN.md)` or `@verify: design-lint(specs/DESIGN.md)` for explicit lint evidence; use `@verify: design-diff(DESIGN.before.md, DESIGN.md)` in review-oriented L3 specs when comparing two explicit DESIGN.md files. `design-diff` reports structural summary, not visual-quality judgment. Briefs include non-blocking Design Guidance: read DESIGN.md prose first, prefer specific inspiration, respect do/don't constraints, and treat unknown sections as possible design intent. Conformance fixtures live under `src/core/__tests__/fixtures/design-context/` for test coverage only; agents should not require or shell out to an external DESIGN.md checkout.
- `quick` remains a restricted lightweight exception and does not create the full L1/L2/L3/Task chain.
- Validate L3 markdown plans with `spec-manager spec validate-plan --from-spec <L3-code>`.
- Record execution with `spec-manager task step`; finish with `spec-manager task complete`.

## Route Table

| Signal | Subskill |
|---|---|
| typo / one-line edit / log level | [subskills/quick.md](subskills/quick.md) |
| inspect / list / search / stats | [subskills/research.md](subskills/research.md) |
| requirement / new feature / user story | [subskills/prd.md](subskills/prd.md) |
| technical plan / architecture / API design | [subskills/design.md](subskills/design.md) |
| implementation / coding / planJson | [subskills/impl.md](subskills/impl.md) |
| plan / milestone / schedule | [subskills/plan.md](subskills/plan.md) |
| test plan / QA / cases | [subskills/testplan.md](subskills/testplan.md) |
| release / changelog | [subskills/release.md](subskills/release.md) |
| runbook / oncall | [subskills/runbook.md](subskills/runbook.md) |
| postmortem / RCA | [subskills/postmortem.md](subskills/postmortem.md) |
| ADR / why choose X | [subskills/adr.md](subskills/adr.md) |
| delta / change / increment | [subskills/change.md](subskills/change.md) |

If intent is unclear, ask the user one concise clarification question before taking action.

## Hard Rules

- Do not write implementation code without a frozen L3 spec.
- Stop after writing L1/L2/L3 content and wait for explicit user approval.
- Status transitions are user actions; one L3 `confirm` approval advances directly to frozen.
- Agent Tasks can only be created from frozen L3 specs.
- Before code edits, read the relevant spec and inspect the actual source files.
- Before release or public handoff, run `spec-manager project docs check` to verify README links, package files, agent guidance consistency, and generated Agent asset boundaries such as `.agents/`, `.claude/`, `.codebuddy/`, and `.codex/`.

## Bundled References

- Rules: [rules/](rules/)
- Templates: [templates/](templates/)
