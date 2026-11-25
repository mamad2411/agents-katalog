---
name: mr-submit
description: >-
  Commit with a mandatory ticket reference, push, and open an MR or PR. Commit,
  branch, and title conventions are read from
  `.agentic/guides/standards/git-workflow.md`; the MR/PR adapter (a CLI, MCP
  server, or custom command) is read from the `## Review Adapter` section of
  `.agentic/guides/project.md`. No source-control platform is hardcoded. Invoke
  on explicit review-workflow requests — "commit changes", "push changes",
  "create MR", "make merge request", "open a PR", and similar. Every commit is
  rejected unless it carries a ticket reference in the guide's pattern.
  Not for: monitoring an already-open MR/PR (mr-watch), merging, or committing without a ticket reference.
authors:
  - agentic-os
---

# Commit, Push, and Open MR/PR

Blast radius **R3** — the create step reaches an external service. Treat MR/PR
creation as gated: it fires only on a direct user request, never as a side
effect of another skill.

> This skill hardcodes no VCS platform. Commit and branch shapes come from the
> git-workflow guide; the create/check mechanism comes from a runtime **adapter**
> declared in the project guide. Everything platform-specific is resolved, not
> assumed.

## When this runs

Trigger only on an explicit user ask to commit, push, or open a review request.
`sdlc-auto` does **not** call this skill on its own — the autonomous
pipeline never self-triggers commit/push/MR side effects.

Route by request:

| User says | Do |
| --- | --- |
| "commit changes" | Commit only (ticket required) |
| "push changes" | Push only |
| "create MR" / "open a PR" | Full push + create workflow |

## Inputs

| Source | Provides |
| --- | --- |
| `.agentic/guides/standards/git-workflow.md` | Commit pattern, branch pattern, MR title format |
| `.agentic/guides/project.md` → `## Review Adapter` | Adapter status, adapter handle, instructions, body template |
| `references/mr-adapters.md` | Adapter contract + sample configs (check/create operations, auth notes, no-adapter fallback) |
| Conversation context | Ticket reference, user request type |

## Outputs

- A commit whose message begins with a validated ticket reference.
- A pushed branch tracking `origin`.
- A created MR/PR (URL surfaced to the user), unless one already exists.
- A run-journal entry at `.agentic/runs/<branch>.json`.
- A user-gated handoff suggestion to `mr-watch` (never auto-invoked).

## Step 0 — Load conventions and resolve the adapter

Read `.agentic/guides/standards/git-workflow.md`. If it is not present, **stop
immediately** and emit this marker verbatim:

```
[GUIDE MISSING] `.agentic/guides/standards/git-workflow.md` not found.
Run the `repo-guides` skill to generate project guides before using `mr-submit`.
```

`repo-guides` is a hard upstream dependency — without the guide there is no
convention to enforce, so do not fall through to defaults.

From the guide, extract three strings:

- **Commit pattern** — e.g. `PREFIX-NNN: Description`
- **Branch pattern** — e.g. `PREFIX-NNN_description`
- **MR title format** — identical to the commit pattern; both begin with the ticket reference

Then read `.agentic/guides/project.md` and locate the `## Review Adapter` section.
Read these fields:

| Field | Meaning |
| --- | --- |
| `**Status**` | `configured` or `not configured` |
| `**Adapter**` | The CLI, MCP server, or command that exposes the check/create operations |
| `**Instructions**` | Extra usage notes for invoking the adapter |
| `**Body Template**` | Optional MR/PR body template with `{{TITLE}}` / `{{BODY}}` tokens |

**No-adapter fallback.** If `project.md` is absent, or the section reads
`Status: not configured`, drop to the no-adapter sequence documented in
`references/mr-adapters.md`:

1. Infer the platform from the git remote's hostname.
2. Probe for installed platform CLIs.
3. Ask the user only if both fail.

Announce the inferred assumption to the user before you act on it.

Load `references/mr-adapters.md` for the full adapter contract and sample
configurations before invoking any check or create operation.

## Step 1 — Inspect current state

```bash
git branch --show-current
git status --short
```

Then run the adapter's declared **check** operation to learn whether the current
branch already has an open MR/PR. Invoke it exactly as the adapter section
declares — do not substitute your own platform call.

## Step 2 — Validate the ticket reference (commits only)

A commit **must never proceed without a ticket reference.** Before committing:

- Scan the conversation for the ticket pattern loaded from the guide.
- Check whether the user already supplied a ticket number.
- If none is present, ask for one in the guide's shape and **wait**:

  > What is the ticket number? Format: `[TICKET]-NNN`

  (substitute the real pattern from the guide). Validate the reply against the
  pattern before continuing.

## Step 3 — Branch guard

If the current branch is `main`, cut a feature branch before any
commit/push/create:

```bash
git checkout -b <type>/<description>
```

Branch types follow the guide — e.g. `feat/…`, `fix/…`, `docs/…`.

## Step 4 — Execute the request

**Commit** (ticket validated):

```bash
git add .
git commit -m "PREFIX-NNN: Description"   # exact shape from git-workflow.md
```

**Push:**

```bash
git push --set-upstream origin $(git branch --show-current)
```

**Create MR/PR:**

- If the check operation found an existing MR/PR → **push only** to it; do not
  open a second one. Report the existing URL.
- Otherwise, push, then run the adapter's declared **create** operation.

Assemble the request from:

- **Title** — the commit/MR pattern from the guide, always beginning with the
  ticket reference.
- **Body** — use `**Body Template**` from the adapter section if present;
  otherwise the built-in template below.

Substitute `{{TITLE}}` and `{{BODY}}` wherever the adapter instructions
reference those tokens, then invoke the adapter exactly as declared.

Built-in body template (used only when the adapter provides none):

```
## What this does
[two to four sentences — what changed and why]

## Worth looking at
- [only the parts a reviewer would otherwise miss]

## What a user notices
[before and after, when the change is user-facing; omit when it is not]

## Checklist
- [ ] Self-reviewed
- [ ] Manual testing performed
- [ ] Documentation updated (if needed)
- [ ] No breaking changes (or documented)
```

## Step 5 — Record the run journal

Read `.agentic/runs/<branch>.json` (`<branch>` = current branch). Create it if
absent. Append or update this entry, then write the file **before** presenting
the handoff:

```json
{
  "step": "06",
  "agent_skill": "mr-submit",
  "primitive": "skill",
  "started_at": "<when this skill began, ISO8601>",
  "completed_at": "<now, ISO8601>",
  "status": "completed",
  "outcome": "...",
  "artifacts": ["<URL>"],
  "next_step": "mr-watch"
}
```

## Step 6 — Hand off to monitoring (user's call)

After the MR/PR exists, surface the URL and offer `mr-watch`. Whether to start
monitoring is always the user's decision — suggest, never auto-invoke.

```
---
mr-submit complete.

**Outcome**: MR/PR <ID> created at <URL>.

**Recommended next step**: `mr-watch` — watch CI, reviewer comments, and merge
conflicts until the MR/PR merges (optional).

How would you like to proceed?
- yes / proceed → I'll invoke `mr-watch` now
- no / skip     → stop here and wait for your instruction
- other         → tell me what to do instead
```

## Reference formats

**Commit** — loaded from the guide, e.g. `PREFIX-NNN: Description`. The ticket
reference and the colon are both required.

```bash
git commit -m "PREFIX-123: Add documentation"    # valid
git commit -m "Add documentation"                # rejected — no ticket
git commit -m "feat: add documentation"          # rejected — wrong format
git commit -m "PREFIX-123 add documentation"     # rejected — missing colon
```

**Branch** — loaded from the guide, e.g. `PREFIX-NNN_description`. Type-prefixed
examples: `feat/add-user-profile`, `fix/auth-timeout`, `docs/api-guide`.

**MR/PR title** — identical to the commit pattern; always leads with the ticket.

## Troubleshooting

| Symptom | Resolution |
| --- | --- |
| Adapter reports not configured | Infer from remote, probe CLIs; if both fail ask the user. Persist config by adding `## Review Adapter` to `.agentic/guides/project.md` (see `references/mr-adapters.md`). |
| Not authenticated with the platform tool | Run the adapter's auth command — e.g. `glab auth login`, `gh auth login`, `az login`. |
| No ticket in context | Ask for the number in the guide's pattern, wait, validate, then commit. |
| On `main` | `git checkout -b <type>/<short-description>` first. |
| Nothing to commit | Check `git status --short` — tree is clean or already staged. |
| MR/PR already exists | Push updates to it; do not create a second one. |

## Boundaries

- Never hardcodes a source-control platform, hosting service, or ticket backend.
- Never opens a second MR/PR when one already exists.
- Never commits without a validated ticket reference.
- Never self-triggers from `sdlc-auto` and never auto-starts `mr-watch`.
