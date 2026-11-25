---
name: kos-zai-agent-runtime-contract
description: The universal operating contract for any kos- agent running inside a run-zai workflow — the workflow prompt is master; the agent only edits files and returns the prompt's exact JSON; workflow steps own all Git/PR/issue mutations.
user-invocable: true
when_to_use: "Always active for every kos- workflow-driver agent; the enforce layer that keeps agent behavior compatible with (never contradicting) the workflow prompt."
category: utilities
argument-hint: "[workflow name]"
keywords: [runtime-contract, run-zai, prompt-master, no-push, json-output, enforce, compatibility]
related: [kos-zai-run-failure-prevention, kos-claude-turn-budget, kos-gh-automation-tooling, kos-commit-and-push-branch]
metadata:
  author: kos-workflow-improvement
  attribution: distilled from the 18 workflow prompts + run-zai action architecture
  license: repo
  version: "1.0"
---

# Idea

Every `kos-<workflow>` agent executes inside a `run-zai` GitHub Actions run. The workflow YAML's `prompt:` is the **master contract** for that run. The agent's job is to **extend and enforce** that prompt — add run-mined knowledge, prevent repeated mistakes — and **never contradict** it. The single most-important fact, which most agent failures get backwards: **the zai agent only edits files and returns the prompt's exact JSON; the surrounding workflow steps do all Git/PR/issue work.**

## When to invoke this skill directly

Always — it is the baseline operating discipline for every `kos-` agent. Re-read before any workflow-driver task, and whenever a run failed at a `commit-and-push` / `upsert-pull-request` / gate step.

## References
- `.github/actions/run-zai/action.yml` — the runtime that runs Claude Code with the prompt + `allowed-tools`.
- Each workflow's `prompt:` block in `.github/workflows/<name>.yml` — the master contract.
- Workflow steps that own mutations: `commit-and-push`, `upsert-pull-request`, `validate-pr-gate`, `report-failure`, `upsert-rebase-comment`.
- [[kos-zai-run-failure-prevention]] (failure taxonomy), [[kos-claude-turn-budget]] (turn discipline), [[kos-gh-automation-tooling]] (which action/script does what), [[kos-commit-and-push-branch]] (the workflow's commit-and-push step — agents do not push).

## Communication Style
State the master prompt's hard rules in one line, then act within them. Never narrate an action the prompt forbids.

## Core Principles
YAGNI / KISS / DRY. The prompt is the floor; the agent adds knowledge above it, never below. One contract, enforced identically across all 18 workflows.

## The contract (enforce layer)

1. **Prompt is master.** Read the workflow `prompt:` first; its hard rules override any generic instinct. If this skill and the prompt ever seem to conflict, **the prompt wins.**
2. **You only analyze and edit files.** You **never** commit, push, merge, open/approve/close PRs, resolve review threads, post the sticky summary, or mutate PRs/issues/labels — **unless the prompt explicitly instructs it.** The workflow steps (`commit-and-push`, `upsert-pull-request`, `validate-pr-gate`, `report-failure`) own those. A "commit-and-push step failure" in a run is a *workflow step* failure that runs **after** you — not something you do.
3. **Return exactly the prompt's output.** If the prompt specifies JSON / verdict tokens / a section format, emit it **verbatim** (same field names, same token vocabulary). Downstream workflow steps parse your output; a paraphrase breaks them.
4. **GitHub queries:** use `rtk gh …` (not raw `gh`) only when the prompt allows GitHub inspection. If the prompt says "do NOT run git/gh/curl/network," obey absolutely — work only from data the prompt already provided.
5. **Verify with the prompt's exact commands** (e.g. `npm run test && npm run build`, `npm run lint && npx tsc --noEmit`, `npm test`). Don't substitute a lighter check the prompt didn't ask for; don't skip verification.
6. **Stay in the prompt's edit scope.** If the prompt restricts edits to `.planning/**`, `docs/**`, `.github/workflows/**`, or "documentation files only," stay inside it.
7. **Apply the run-knowledge skills** to raise success rate: [[kos-claude-turn-budget]] (phase the work, don't hit `turn_limit_hit`), [[kos-zai-run-failure-prevention]] (avoid the canonical run failure modes), [[kos-gh-automation-tooling]] (use existing actions/scripts).

## Your Approach
1. Open the workflow YAML; read `prompt:`; note its hard rules, output schema, edit scope, verify commands.
2. Confirm which mutations are **yours** (file edits + the exact output) vs **the workflow's** (push/PR/gate/labels/issues).
3. Do your file work within scope and turn budget.
4. Verify with the prompt's commands.
5. Emit the prompt's exact output; stop.

## Anti-patterns (the mistakes this contract prevents)
- **Inverted push boundary** — telling the agent to `git push` / open a PR / force-push when the prompt says "do NOT push — the workflow handles that." (The historical root cause of most kos- incompatibilities.)
- **Output drift** — emitting `APPROVE/REQUEST_CHANGES` or prose where the prompt requires `passed|concerns` JSON with specific fields.
- **Tool-rule violation** — running `gh`/`git`/`curl` when the prompt mandates "no network," or raw `gh` when the prompt mandates `rtk gh`.
- **Scope creep** — editing files outside the prompt's allowed scope.
- **Verify substitution** — running only `tsc` when the prompt requires `npm run test && npm run build`.

## Process Flow (Authoritative)
1. Read `prompt:` → extract {hard rules, output schema, edit scope, verify cmds, tool rules}.
2. Partition actions: yours (edit + output) vs workflow's (push/PR/gate/labels/issues).
3. Edit within scope; apply turn-budget + failure-prevention.
4. Verify with the prompt's commands.
5. Emit the prompt's exact output and stop.

## Output Format
The prompt's exact output — unchanged. If asked to summarize compatibility: `PROMPT_MASTER=<wf.yml>  AGENT_DOES=<edit+output>  WORKFLOW_DOES=<push/PR/gate/labels>  OUT=<schema>`.

## Critical Constraints
- Never instruct or perform a mutation the prompt reserves for workflow steps.
- Never paraphrase the prompt's JSON schema or verdict tokens.
- Never run disallowed tools (gh/git/network) when the prompt forbids them.
- When this skill and the prompt conflict, the prompt wins — and the agent file must be updated to match (see `docs/code-standards.md` → Workflow knowledge layer).
