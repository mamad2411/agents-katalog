---
name: requirements-enricher
description:
  (NS) Enrich requirements before autonomous execution — GitLab issue or chat context.
  **Issue mode:** given ISSUE_URL, read issue and comments via MCP, investigate codebase,
  run grill-me gap analysis, post one internal comment with numbered questions for the
  issue author. **Chat mode:** when the user pastes or describes requirements/scope in
  conversation (no issue), run the same analysis and render numbered questions inline
  in chat only — no files, no GitLab posts. Use whenever the user asks to enrich/refine
  requirements, clarify scope, prepare for execution, run grill-me, or generate blocking
  questions — with or without a GitLab issue. Do NOT use for full issue execution
  (execution-gitlab-issue), code review (code-reviewer), version planning
  (start_execution_planning), or generating requirements.md (pm-requirements-generator).
license: Apache-2.0
metadata:
  author: nextstage-brasil
  version: "1.0"
depends:
  - nextstage-harness
  - mcp-gitlab-usage
---

# Requirements Enricher

Prepare requirements for **autonomous execution** by closing gaps before any branch, code, or status change.

## Mode detection

| Mode | Trigger | Delivery |
| ---- | ------- | -------- |
| **Issue** | `ISSUE_URL` present or user points to a GitLab issue | Post one **internal** GitLab comment (Phase 4) |
| **Chat** | User pastes/describes requirements in conversation — no issue URL | Render verdict + numbered questions **inline in chat only** — no files, no GitLab, no version artifacts |

Both modes share Phases 2–3 (investigation + grill-me). Phase 1 (MCP load) applies only in **issue** mode.

## Harness discovery

See `../nextstage-harness/references/harness-discovery.md` and `../nextstage-harness/references/artifact-layout.md`. Resolve `{product_root}` before codebase investigation.

Read `../mcp-gitlab-usage/SKILL.md` before MCP calls (`get_mcp_gitlab_skill` version check on first access).

## Objective

**Issue mode:** given `ISSUE_URL`, produce one **internal** GitLab comment that:

1. Summarizes what you understood from the issue + comments
2. Opens with a **verdict icon** — `✅` (ready) or `❌` (blocking questions)
3. Lists **all** blocking/open questions **numbered sequentially** (never one-by-one in chat)
4. **@mentions** the issue **author** (who opened it) so they can reply in the issue thread

**Chat mode:** given requirements text from the conversation, produce an **inline** response that:

1. Summarizes what you understood from the user's description
2. Opens with the same **verdict icon** — `✅` or `❌`
3. Lists **all** blocking/open questions **numbered sequentially** in the chat reply
4. Does **not** @mention anyone (no issue author)

Do **not** implement, commit, change issue status, create files, or ask questions interactively one-by-one (except when blocked on missing context or MCP access in issue mode).

## When to use

- User provides `ISSUE_URL` and wants requirements clarified before coding (**issue** mode)
- User pastes a feature brief, scope, or acceptance criteria in chat without a GitLab issue (**chat** mode)
- User invokes grill-me on requirements (issue or chat)
- `code-autonomous` / human flags work as underspecified
- Pre-step before `execution-gitlab-issue` when acceptance criteria are incomplete

## Prerequisites

1. Read `{product_root}/AGENTS.md` — Docker/runtime context if investigation touches tests or services.
2. Read `{product_root}/agents.local.md` when present — use **only** the GitLab MCP server named there.
3. Follow `../mcp-gitlab-usage/SKILL.md` for tool contracts.

## Inputs

| Variable    | Required | Description |
| ----------- | -------- | ----------- |
| `ISSUE_URL` | Issue mode only | Full GitLab issue link |
| Requirements text | Chat mode only | User message, pasted brief, or attached scope |
| `DRY_RUN`   | No       | Issue mode: if true, show comment in chat only; do not post |

## Phase 1 — Load issue context (issue mode only)

**Skip this phase in chat mode.** Use the user's message and any pasted context as the requirements source instead.

**Parse URL** → `project_id` (or `project_name` for discovery) + `issue_iid`.

**Mandatory reads:**

1. `read_issue` — title, description, labels, milestone, **author** (`username`, `name`), assignees, related links.
2. `list_issue_comments` — full thread history; treat comment bodies as requirements source.

### Author username (mandatory — do not guess)

The `@mention` on the first line **must** use the GitLab login exactly as returned by `read_issue`.

**Source of truth (only):**

- `author.username` from the `read_issue` response — the user who **opened** the issue.

**Immediately after `read_issue`, record:**

```text
author_username = <author.username>   # literal string from MCP; case-sensitive
```

**Never use for `@mention`:**

- `author.name` (display name)
- Slug/sanitize derivations from `author.name`
- Assignee username (unless assignee **is** the author)
- Username inferred from comments, email, profile URL, or memory
- Lowercasing or normalizing unless GitLab returned that casing

**If `author` or `author.username` is missing:** stop and report — do not substitute assignee or guess.

**Synthesize** (internal notes, not yet posted):

- **Goal** — one sentence: what should exist when done?
- **Acceptance criteria** — explicit list from description; mark each as clear / partial / missing.
- **Constraints** — note labels/milestone/due date for _your_ context; do **not** turn missing labels into questions.
- **Already answered** — facts from comments that remove ambiguity; do not re-ask these.

If `ISSUE_URL` is missing in issue mode, or MCP is unavailable, stop with a single line telling the human what is missing (do not invent issue content).

In **chat mode**, synthesize Goal, Acceptance criteria, Constraints, and Already answered from the conversation text using the same structure as above.

## Phase 2 — Investigate codebase and product context

Scope investigation to what the issue touches. Goal: discover **real product ambiguities**; keep technical findings in "Current understanding" / "Assumptions", not in the question list.

**Read product context when relevant:**

- `{product_root}/docs/context/brownfield-map.md` — existing modules, legacy constraints.
- `{product_root}/docs/context/system-reverse-spec.agent.md` when present (prefer); else `system-reverse-spec.md`.
- `{harness_root}/rules/architecture-rules.md` — routes, modules, layering.
- `{product_root}/docs/context/gitlab-sync-config.md` — status labels, project ids (for your context only).

**Investigation actions (pick what applies):**

- Grep symbols, routes, module names mentioned in the issue.
- Read controllers, services, views, API routes, and integrations in the affected area.
- Check existing tests for the same area.
- Note: current behavior, extension points, permissions, events/queues, env dependencies.

**Output:** short bullet list of **relevant files/areas** and **assumptions** the issue implies but does not state.

## Phase 3 — Grill-me gap analysis

Apply relentless interview logic: sharpen the plan by exposing what is still unknown for _behavior the requester cares about_.

Cross **issue text + comments + code findings**. For each gap, ask: _"Could an agent implement and verify this without guessing the product intent?"_ If no → candidate question — then **rewrite** it for the requester (see below).

### Audience (mandatory)

Questions are for **who opened the issue** (`author` from `read_issue`), not for a developer, tech lead, or ops.

- Language: **common product/UX language** (screen, button, filter, what appears, when it applies).
- The requester's answers must **imply** the technical decision; you translate later at execution time.
- Put schema, SQL, class names, branches, labels, and file paths in **Current understanding / Assumptions** — never as the question itself.

### Question quality rules

- **Requester-facing** — a non-dev product owner can answer without reading code.
- **Specific** — name the screen/flow the user sees, not the implementation class.
- **Answerable** — one line or a short paragraph; prefer closed choices when useful.
- **Blocking** — omit nice-to-haves that have a safe default (state the default in "Assumptions").
- **Non-duplicative** — skip anything already answered in issue or comments.
- **Numbered** — final list is `1.`, `2.`, … ordered by user journey (what appears → when it applies → edge cases → acceptance).

### Translate technical gaps → product questions

| Technical gap (keep internal / in assumptions) | Ask the requester instead                                                                                                                     |
| ---------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| Which table/column / relation?                 | "Does filtering by Club mean only people linked to that club today?"                                                                          |
| Base branch / GATE 1 / `develop-*` naming      | Do **not** ask (see Out of scope)                                                                                                             |
| Missing label `Team: *`                        | Do **not** ask                                                                                                                                |
| Endpoint payload / SQL join                    | "When Federation and Role are both selected, must a person match both or either?"                                                             |
| Unit vs E2E test path                          | Only if acceptance is unclear — e.g. "How will we validate this is done: on the screen, with specific scenarios?" — not "which phpunit path?" |

### Good vs bad examples

**Good (ask):**

> When the checkbox is checked, does the filter apply immediately or only after clicking Search (like dates/unit)?

**Ignore / never ask:**

> Missing Team label on this issue

> Base branch (GATE 1): milestone is 1.32, but remote only has `develop_1.32` — which branch?

> Should table `agencia_2.linktable` with relation `PESSOA|CLUBE` filter by `id_right_linktable`?

**Milestone (only allowed case):** at most _one_ question like "Is the milestone on this issue correct?" — when product version is genuinely ambiguous. Nothing about branch naming, underscores vs hyphens, or GATE 1.

### Out of scope for the question list

Do **not** promote to numbered questions:

- Missing or wrong **labels** (Team, Type, Priority, Severity, …)
- **Base branch**, remote branch naming, GATE 1 / `develop-{semver}` vs `develop_X.Y.Z`
- Pure engineering choices with a safe default already stated in Assumptions
- "How should we implement…" / schema / class / env var names

### Categories to scan

See `references/question-checklist.md`. Prefer product/UX/acceptance gaps only.

Cap at **15 questions**; merge related micro-questions. If zero gaps remain, say so explicitly and post a short "ready for execution" internal note instead of filler questions.

## Phase 4 — Deliver results

### Issue mode (MCP)

Unless `DRY_RUN=true`, call `add_issue_comment` with:

- `internal: true`
- `body` — Markdown from `references/comment-template.md` (fill all sections)

**Verdict icon (first character of first line):**

| Situation                                 | Icon | First line                                                                                                |
| ----------------------------------------- | ---- | --------------------------------------------------------------------------------------------------------- |
| Zero blocking questions — execution-ready | `✅` | `✅ @{author_username} — requirements enrichment for autonomous execution. **Ready for execution.**`      |
| One or more blocking questions            | `❌` | `❌ @{author_username} — requirements enrichment for autonomous execution. **{N} blocking question(s).**` |

Use the **execution-ready** template when `N = 0`; use the **questions** template when `N ≥ 1`. The icon is mandatory — never omit.

**Mention author:** `author_username` is the **literal** `author.username` captured in Phase 1. Re-read `read_issue` output if unsure — never infer.

**After posting:** reply in chat with:

- Link or `project_id` + `issue_iid`
- Count of questions posted
- One-line note if the issue looks execution-ready vs blocked

Do **not** use `set_issue_status`, `update_issue`, or `create_issue` in this skill.

### Chat mode (inline)

Render the same structure as the comment template **directly in the chat reply**:

- Verdict icon on the first line (`✅` ready / `❌` with question count)
- **Current understanding** — short summary
- **Assumptions** — safe defaults you applied
- **Areas investigated** — relevant files/modules (OK to include paths here)
- **Questions** — numbered list in plain product language (no @mentions)

Do **not** create files, post to GitLab, or write version artifacts (`requirements.md`, task files, etc.).

**After delivery (both modes):** reply in chat with:

- Issue mode: link or `project_id` + `issue_iid`; count of questions posted
- Chat mode: count of questions; one-line note if scope looks execution-ready vs blocked

## Language

- GitLab comment (issue mode): **English** unless the user or `{product_root}` docs explicitly require another language for stakeholder communication.
- Chat reply (chat mode): match the language the user used unless they request otherwise.
- In **Questions**: no file paths, class names, SQL, or env vars
- In **Current understanding / Assumptions / Areas investigated**: code paths OK (for the executing agent)

## Anti-patterns

- Asking questions one-by-one in chat instead of batching in the issue comment
- Posting a public (non-internal) comment
- Hand-crafting `requirements.md` or calling `start_execution_planning` (out of scope)
- Starting implementation or creating branches
- Generic questions ignoring codebase ("How should this work?" without screen/context)
- Re-asking facts already in comments
- Forgetting `@author_username` (opener)
- Using `author.name`, a slug of the display name, or any username not equal to `author.username` from `read_issue`
- Questions aimed at **developers** (table, branch, label, GATE, test path, JSON payload)
- Asking about **missing labels**
- Asking about **base branch** / remote branch naming (except optional "is milestone correct?")
- Putting the **technical solution** inside the question

## Relationship to other skills

| Skill                    | When                                                                |
| ------------------------ | ------------------------------------------------------------------- |
| `execution-gitlab-issue`   | After requirements are clear; implements the issue                  |
| `code-reviewer`          | After code exists; reviews diffs                                    |
| `mcp-gitlab-usage`       | All MCP calls, version check, `add_issue_comment` contract          |
| `pm-clarify-requirements`   | Version-scope clarification in chat before `pm-requirements-generator` |
| `pm-requirements-generator` | Produces `requirements.md` for a version — not per-issue enrichment |

## Quick checklist

- [ ] Mode detected: issue (`ISSUE_URL`) vs chat (conversation text)
- [ ] Issue mode: `read_issue` + `list_issue_comments` done; `author_username` = literal `author.username`
- [ ] Chat mode: requirements synthesized from user message; no MCP issue load
- [ ] Codebase and product context investigated; technical gaps → assumptions or rewritten for requester
- [ ] Questions: requester-facing, plain language, no labels/branch/schema as questions
- [ ] Issue mode: comment uses template; verdict icon; `@author`; `internal: true`
- [ ] Chat mode: verdict + questions inline only; no files, no GitLab posts
- [ ] No status change, no code edits, no interactive Q&A one-by-one

## References

| File                               | When                          |
| ---------------------------------- | ----------------------------- |
| `references/comment-template.md`   | Phase 4 — GitLab comment body |
| `references/question-checklist.md` | Phase 3 — gap scan categories |
