---
name: hermes-forge
description: >
  Hermes⇄Forge boundary: Hermes CONSUMES Forge state, never a second source of truth. Use
  whenever a Hermes session runs on a Forge repo: at session start, before acting on an issue,
  or when you need CURRENT state. Read state ONLY via `forge orient` / `forge recap
  <issue-id>` (bounded JSON envelope), citing each source's `path`/`authority`; never
  reconstruct it from raw stores or kernel internals. Writeback ONLY via `forge
  comment`/`update`/`create`; NEVER leak Hermes profile or session memory into Forge state.
  Triggers: "orient me / current project state", "where did this fact come from, cite it",
  "orient came back truncated", "persist a decision into Forge", "safe to store in kernel
  state?". NOT the Forge session router over stage skills (kernel), NOT the human "what stage
  am I in" report (status), NOT everyday issue create/update/close/search CRUD (issue-basics),
  NOT ranking the next ready issue (triage-ready), NOT live PR monitoring (shepherd—outside
  Hermes, unseen by orient).
compatibility: >
  Requires the Forge CLI (`forge`) on PATH in a Forge-initialized repo. Install
  path — like every Forge skill pack (e.g. parallel-deep-research,
  sonarcloud-analysis) this is delivered by the unified Skills CLI; run
  `skills sync` to install it into `.hermes/skills/hermes-forge/`. (`forge setup`
  initializes the skills registry via `skills init` but does not sync packs to
  agents.) Read-only orientation works anywhere; writeback requires a Forge
  Kernel issue backend. CLI-only — no direct file or profile writes into Forge
  state.
metadata:
  author: forge
  version: "1.0.0"
  roadmap: forge-2agy.9.7.x
chainExempt: true
---

# Hermes ⇄ Forge consumption contract

Hermes is a *consumer* of Forge project state, not an owner of it. This skill
defines how a Hermes session reads, cites, and writes back to a Forge project
without ever becoming a second source of truth.

The boundary between what Forge owns and what Hermes owns is specified in the
Forge repo at `docs/reference/HERMES_INTEGRATION.md` (repo-relative path — this
skill is synced to `.hermes/skills/hermes-forge/`, so relative links would not
resolve from the installed location).

## When to use

- At the start of any Hermes session on a Forge repo (orientation).
- Before acting on a specific issue (issue recap).
- Whenever you need current project state — never reconstruct it from raw files.

## Authority: orient / recap are the only state source

The Forge Kernel is the single source of truth. Hermes obtains project state
**exclusively** through two thin CLI wrappers and must not infer state by
reading raw issue stores, design files, or kernel internals directly:

```bash
forge orient --json                # bounded project orientation (envelope)
forge orient --budget 4000 --json
forge recap <issue-id> --json      # bounded per-issue recap (envelope)
```

`forge orient` and `forge recap <issue-id>` emit the deterministic JSON envelope
described below (assembly `deterministic-file-assembly-v1`). Parse the JSON; do
not screen-scrape the human text form.

> Note: `forge recap` always requires an issue id — bare `forge recap --json`
> (no id) prints its usage and exits non-zero rather than returning a summary.
> Use `forge orient` for project-level orientation, or `forge recap <issue-id>`
> for a single issue; both emit the deterministic envelope.

### Envelope shape

| Field | Meaning |
| --- | --- |
| `schema_version` | Contract version (currently `1`). Reject unknown majors. |
| `kind` | `orientation`, `issue_recap`, or `prime`. |
| `generated_at` | Assembly timestamp. |
| `assembly` | `deterministic-file-assembly-v1` — same inputs ⇒ same output. |
| `token_budget` | Budget accounting (see below). |
| `sections[]` | Ordered content blocks, each independently cited. |
| `sources[]` | Deduplicated provenance across all sections. |
| `next_commands[]` | Suggested follow-up `forge` commands. Prefer these for navigation. |

Each `sections[]` entry: `{ id, title, content, sources, truncated, estimated_tokens }`.

## Token budget

`forge orient` / `forge recap <issue-id>` are bounded so they fit a context
window deterministically.

- Default budget: **2000** estimated tokens. Minimum honored: **40**.
- Estimation is approximate: `token_budget.approximate === true`,
  `token_budget.chars_per_token === 4`.
- `token_budget.requested` is what you asked for; `token_budget.used` is the
  estimate actually emitted.
- Raise the ceiling with `--budget N` when you need more depth; do not retry
  blindly — request a specific larger budget.

## Citation & provenance model

Every fact Hermes surfaces to a user MUST be attributable. Each section carries
`sources: [{ path, source_kind, authority, role }]`:

- `path` — the file the content came from.
- `source_kind` — the kind of artifact (e.g. design, decision, claim, queue).
- `authority` — how authoritative the source is. Prefer higher-authority
  sources when two sources conflict; surface the conflict rather than silently
  picking one.
- `role` — the role the source plays in the section.

When Hermes states a project fact, cite at least the `path` and `authority` of
the backing source. The top-level `sources[]` is the deduplicated set for the
whole payload.

## Truncation policy

Truncation is deterministic, never random:

- Non-preserved sections are trimmed in the order given by
  `token_budget.truncation_order`; when the budget is exhausted, sections later
  in that order are trimmed first. Preserved sections are kept whole and trimmed
  only as a last resort if the payload is still over budget. The authoritative
  per-section signal is each section's `truncated` flag and `estimated_tokens` —
  there is no per-section `priority` field; the overall trim order is
  `token_budget.truncation_order`.
- A trimmed section ends with the literal marker
  `[truncated deterministically by token budget]` and has `truncated: true`.
- `token_budget.truncated === true` means the payload as a whole was trimmed.

Treat any `truncated` section as **incomplete**. Do not present a truncated
section as exhaustive; if completeness matters, re-request with a higher
`--budget` or recap the specific issue.

## Writeback path: Hermes → Forge Kernel

Evidence and decisions discovered during a Hermes session flow back into the
Forge Kernel **only** through Forge CLI commands. Use the issue command surface
documented in the Forge repo at
`docs/reference/forge-kernel-issue-command-contract.md`:

```bash
forge comment <id> <body...>   # attach evidence, a decision, or a note to an issue
forge update <id...> [flags]   # update issue state/fields
forge create [title] [flags]   # open a new issue for follow-up work
```

> Note: `forge audit` is verify-only (`forge audit verify`) and does **not**
> append evidence — record evidence as an issue comment via `forge comment`.

These writes land in the Forge Kernel issue store, where they become part of the
issue's durable history (view them via the issue itself, e.g. `forge show <id>`).
Note the read/write asymmetry: the bounded `forge orient` / `forge recap`
envelope is assembled from project docs, `docs/work` artifacts, and the issue
summary — it surfaces issue/design/decision state but does **not** echo
individual issue comments back. Do not assume evidence added via `forge comment`
reappears verbatim in the next orient/recap payload; it lives in the issue
history, reachable from the issue record.

## No-profile-write guard (hard boundary)

Hermes **MUST NOT write Hermes profile** state, conversation memory, or any
Hermes-native artifact into Forge Kernel state — not into kernel storage, not
into design/decision files, not into the issue backend. Hermes-native memory
stays in Hermes' own store.

- ✅ Read state via `forge orient` / `forge recap`.
- ✅ Write evidence/decisions via `forge comment` / `forge update`.
- ❌ Never persist Hermes profile/session memory into Forge Kernel state.
- ❌ Never edit Forge state files directly to record Hermes-side context.

If a piece of context only matters to Hermes, it belongs in Hermes-native
memory. If it is a project fact, decision, or evidence item, write it through
the Forge CLI so it becomes part of the shared, cited source of truth.

## PR shepherd (external scheduler, not orientation)

The PR shepherd runs **outside** Hermes. An external scheduler invokes
`forge shepherd <pr>` as discrete bounded passes — each pass reads CI/check
state, takes at most one idempotent action (re-run a flaky required check), or
escalates, then exits. It **never merges** (the human merges in the GitHub UI)
and **never resolves review threads**.

Hermes does not run the shepherd and does not learn shepherd progress through
`forge orient` (which is deterministic-source orientation with no live PR
awareness). Shepherd progress is durable on the **PR itself** — its comments and
labels. When a Hermes session needs PR/CI status, read the PR directly; do not
expect `orient` to carry it.
