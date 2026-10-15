---
name: opsx-prompt
description: >
  Use when drafting, generating, preparing, writing, or asking for an
  opsx:new prompt from a Linear issue (APP-XXXXX) or a freeform change
  request, including the short-form invocations "opsx APP-XXXXX" and
  "opsx:new --deep". Also trigger for deep review, deep discovery,
  extra confidence, a second look, or missed-considerations passes
  before or alongside opsx:new. Not for full proposal/design/spec
  work or rollout planning — those need a different flow.
---

# Opsx Prompt Generator

Generate a ticket-first prompt for `opsx:new`.

## Goal

Answer two questions clearly:

- Why does this issue exist?
- What outcome is it asking for?

The prompt should faithfully represent the ticket's intended change. Code reads are allowed only to correct obvious mistakes or to produce optional follow-up notes.

## Non-goals

This skill does NOT:

- discover extra scope by default
- redesign the ticket
- do full rollout planning or Expand/Migrate/Contract design
- replace proposal, design, or spec work

## Input

- `APP-XXXXX` issue ID
- `--deep APP-XXXXX` or `APP-XXXXX --deep`: generate the prompt and run deep review in the same pass
- freeform change description
- no input: ask what change the user wants to describe

If the input is an issue ID, use the `linear-cli` skill. Do not use Linear MCP tools. If `linear-cli` is unavailable, ask the user to export the issue and paste the result:

```bash
linear issue view APP-XXXXX --json --no-pager > /tmp/APP-XXXXX.json
```

## Flow

| Input | Phase 1: read | Phase 2: extract | Phase 3: sanity | Phase 4: prompt | Phase 5: deep review |
| --- | --- | --- | --- | --- | --- |
| Issue ID | Yes | Yes | If needed | Yes | No |
| Issue ID + `--deep` | Yes | Yes | If needed | Yes | Yes, from same intent |
| Freeform request | Yes | Yes | Usually no | Yes | No |
| Already-done issue | Yes | Yes | No unless symbols need grounding | Ask whether a prompt is still wanted | No unless requested |

Default to the shortest flow that can faithfully express the request. Never re-fetch Linear or re-extract intent between Phase 4 and Phase 5 in `--deep` mode.

## Optional Repo Context

Repo context is needed only for the cheap already-done check, Phase 3, or Phase 5.

Resolve repo context in this order:

1. Explicit repo or service path from the user.
2. `~/Caruso/config.yaml` -> `workspace_path`; treat this as the workspace root, then resolve `{service}` under `worktrees/` or direct service folders.
3. `~/.caruso/config.yaml` -> `workspace_path`; treat this as the workspace root, then resolve `{service}` under `worktrees/` or direct service folders.
4. Current directory if it is inside the target git repo.
5. `~/Caruso/worktrees/{service}-*` when exactly one matching worktree exists.
6. `~/Caruso/{service}`.

Infer `{service}` from the issue title (`service-name | description`) or ask the user. If multiple matching worktrees exist, ask which one to use.

If Phase 3 or Phase 5 is needed but repo context cannot be resolved:

1. Ask the user for the repo or service path.
2. If the user cannot provide it and still wants a prompt, skip code-based checks and surface a user note: `Sanity check skipped: repo unavailable`.
3. Do not silently pretend the ticket was grounded against code.

If repo context is missing only for the Phase 1 already-done check, continue from linked Linear PRs/comments. Do not emit `Sanity check skipped` for that alone.

## Phase 1: Read The Request

Issue mode:

1. Fetch the issue title, description, comments, parent or sub-issue summary, and linked PRs.
2. Check child/sub-issue data from `linear issue view APP-XXXXX --json --no-pager`. Do not use `linear issue relation list`; it reports dependency relations, not parent-child issue membership. If the requested issue is a parent with more than one child issue, stop and ask whether to generate one combined prompt or one prompt per child issue.
3. Run a cheap already-done check when a target repo can be inferred or provided:
   ```bash
   cd {REPO_PATH}
   OWNER_REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)
   gh search prs "APP-XXXXX" --repo "$OWNER_REPO" --json number,title,state,url,updatedAt --limit 20
   git log --all --grep="APP-XXXXX" --oneline -n 20
   ```
4. If `gh` is unavailable or unauthenticated, skip the PR search and keep going; this cheap check is not a blocker. Still run the local `git log` check when repo context exists.
5. Identify work that already landed from linked PRs, searched PRs, or matching commits. Treat a result as `Already done` only when the PR/commit clearly matches the requested outcome.
6. Do not read code yet.

Freeform mode:

1. Read the request as written.
2. If it is mostly implementation detail, ask for the underlying goal.

## Phase 2: Extract Intent

Produce a structured summary for both issue and freeform mode:

- `Why`
- `What`
- `Explicit asks`
- `Non-goals`
- `Already done`
- `Unknowns`
- `Raw claims`

Freeform mode still uses this schema. `Already done` is usually `(n/a)`. `Non-goals` should be `(none)` unless the user states a boundary. `Raw claims` may be `(none)`.

`Raw claims` is internal support data, not prompt content. Use it to preserve:

- named symbols or paths mentioned by the ticket
- explicit scope boundaries like "do not change X"
- literal deliverables that must survive prompt generation

Use this exact line-oriented format:

```text
[symbol] CompletedUnitPrice
[path] proto/pricing/v1/pricing.proto
[boundary] do not change pricing rules
[deliverable] rename CompletedUnitPrice to FinalCompletedUnitPrice
[contract] response field used by downstream consumers
```

If there are no raw claims, write `(none)`.

Rules:

- stay domain-level
- preserve explicit asks
- separate desired outcomes from implementation ideas
- if the ticket is ambiguous, record that in `Unknowns` instead of guessing
- route non-blocking `Unknowns` into Phase 4's `Open questions`
- if an unknown would make the prompt likely false, stop instead of downgrading it to an open question
- keep `Raw claims` literal and tagged; do not turn it into prose

## Phase 3: Light Sanity Check

Run this only when needed. Do not expose internal modes to the user.

Use `triage.md` when the ticket includes any of:

- code symbols, file paths, RPC names, schema names, or fields
- explicit scope boundaries
- wording like "rename", "remove", "migration", or "deprecate"
- AI-style implementation detail that may be pointing at the wrong target

The light sanity check may:

- confirm the ticket points at the right thing
- rewrite the intent against the correct target when the ticket named the wrong thing
- stop and ask for clarification when the ticket premise looks wrong

It must NOT:

- sweep callers or consumers broadly
- discover adjacent work
- add scope the ticket did not ask for
- run at all without a resolved repo path; if repo context is unavailable, use the fallback described above

## Phase 4: Generate The Prompt

Read `output-format.md` and generate the prompt from the extracted intent.

Rules:

- `This change` comes from the ticket's stated goal and explicit asks
- `Already in place` comes from linked PRs or other clearly landed work
- `Non-scope` comes from explicit ticket boundaries
- non-blocking `Unknowns` become `Open questions`
- if Phase 3 found a mismatch, use corrected domain-level wording in the prompt and surface the mismatch as a user note
- if a literal ask names an external API, schema, field, event, RPC, or user-visible contract and that literal is necessary to preserve the deliverable, include it in the main prompt under `Literal deliverables`
- if a literal ask names internal implementation detail such as file paths, helper functions, or private symbols, keep the main prompt domain-level and surface the exact ask in a `Symbol-sensitive requirements` user note
- if the exact symbol-level detail is the core of the request and cannot be represented safely even with a note, stop and ask for clarification
- for freeform requests, derive the title from the requested outcome; use repo-derived service if clear, otherwise `unknown-service`, and use `no-issue`
- if the ticket is still materially unclear, stop and ask for clarification instead of fabricating certainty

## Phase 5: Optional Deep Review

Deep review is optional, not part of the default path.

Only run `code-exploration.md` when:

- the user asks for extra confidence
- the issue is high-risk and the user wants a deeper pass
- the prompt is fine, but the user wants a second look for missed considerations

Deep review may produce user-facing notes:

- `Possible missing considerations`
- `Possible contract risks`
- `Possible already-completed work`

Do NOT merge deep-review findings into the prompt automatically. This includes `Possible already-completed work`. If the user wants any of these findings reflected in the prompt, revise the prompt explicitly.

## Presentation

Present the prompt first. If deep review ran, put deep-review notes after the prompt and outside the fenced prompt. Do not merge deep-review findings into the prompt unless the user explicitly asks to revise it.

User-facing choices should stay simple:

- `Generate prompt`
- `Generate prompt + deep review`

Do not expose internal modes like `Full`, `Narrow`, or `Skip`.

## When To Stop

Stop instead of generating a prompt if:

- the ticket's core goal is unclear
- the ticket appears to target the wrong thing entirely
- the request is self-contradictory
- the prompt would otherwise encode a likely false premise

## Edge Cases

- No argument: ask for an issue ID or short description
- Ticket already done: show `Already in place` and ask whether the user still wants a prompt
- Parent issue with multiple child issues: ask whether to generate one combined prompt or one prompt per child issue
- Multi-repo issue: keep one prompt, but note the affected repos in `Open questions` or the user note
- No repo available: still generate the prompt if Phase 3 and Phase 5 are unnecessary
- No repo available when Phase 3 or Phase 5 would otherwise run: ask for repo path first; if unavailable, proceed only with an explicit `Sanity check skipped` user note
- Freeform request with no clear why: ask for the business goal before generating the prompt
- Freeform request with no clear service name: use `unknown-service`

## Key Principle

This skill is ticket-first:

- the issue defines the intent
- light grounding may correct obvious mistakes
- deep discovery is optional
- the skill should help the user express the requested change clearly, not silently enlarge it
