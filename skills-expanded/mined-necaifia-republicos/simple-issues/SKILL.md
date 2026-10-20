---
description: Use this skill whenever the user mentions issues, tasks, tickets, work
  items, or asks "what should I work on", "what's next", or wants to create/claim/close
  work. Manages a lightweight file-based issue tracker under `.issues/` with `open/`,
  `claimed/`, `closed/` folders. Issues are append-only markdown files with YAML frontmatter.
  No external infrastructure required. Treats infrastructure as code with immutable
  deployments, health checks, and circuit breakers. Follows agent-native CI/CD with
  eval-gated promotion, canary rollouts, and compensating rollback actions.
metadata:
  evolved: true
  evolved_at: '2026-07-20T14:07:06.303188+00:00'
name: simple-issues
tags:
- infrastructure
version: 2
---

# File-Based Issue Tracker

A zero-infrastructure issue tracker that lives inside the repository under `.issues/`. Designed for workshops and small teams where multiple humans (each on their own machine, optionally with agents) collaborate without stepping on each other.

## 1. On activation — ALWAYS do this first

When this skill activates, immediately:

1. Check whether `.issues/` exists at the repo root.
    - If **not**, ask the user: _"No issue tracker found. Should I initialize `.issues/` here?"_ — then follow §2.
2. If it exists, scan all three folders and report to the user:
    - Count of issues in `open/`, `claimed/`, `closed/`.
    - List of **available** open issues (title + short-id), filtered to those whose `dependsOn` are all in `closed/`.
    - Whether **this machine** (see §3 for identity) currently has any issue in `claimed/` — if yes, name it. The agent must finish that one before claiming anything new.

Example report:

```
📋 Issue tracker status
  open: 4  |  claimed: 2  |  closed: 11

Available to claim (deps satisfied):
  - a3f1  Add dark mode toggle
  - 9b22  Refactor auth middleware

Currently claimed by this machine (yannick@thinkpad):
  - 7e04  Fix flaky login test  ← finish this before claiming a new one
```

## 2. Initializing the structure

```bash
mkdir -p .issues/open .issues/claimed .issues/closed
```

Add a short `.issues/README.md` explaining the workflow (optional but recommended). Do **not** add `.gitignore` entries — issues are meant to be committed.

## 3. Machine identity

Every claim is owned by a **machine**, not a person. Compute identity as:

```
<username>@<hostname>
```

- POSIX: `echo "$(whoami)@$(hostname -s)"`
- Windows: `echo "$env:USERNAME@$env:COMPUTERNAME"`

Cache this value for the session. Never invent or reuse another machine's identity.

## 4. Git awareness (optional)

Before any state-changing operation (claim, close, create), check if the repo uses git:

```bash
git rev-parse --is-inside-work-tree 2>/dev/null
```

- If **yes**: run `git pull --rebase` first to minimize claim races. If a rebase conflict touches `.issues/claimed/`, inform the user — another machine likely claimed the same issue.
- If **no** (workshop single-machine scenario): skip; just operate on the filesystem.

## 5. Issue file format

### Filename

```
<short-id>-<kebab-title>.md
```

- `short-id`: first **4 hex chars of the SHA-1** of the issue's initial markdown body (frontmatter excluded). Compute _before_ writing the file.
- `kebab-title`: lowercase, ASCII, hyphen-separated, max ~60 chars.

Example: `a3f1-add-dark-mode-toggle.md`

If a 4-char collision occurs (very rare in workshops), extend to 6 chars for the new file only.

### Frontmatter (YAML)

```yaml
---
title: "Add dark mode toggle"
dependsOn: [] # list of short-ids, e.g. ["9b22", "7e04"]
humanNeeded: false # true if ANY step requires a human to act, decide, or be interviewed
humanNeededReason: null # required free-text string when humanNeeded=true
claimedBy: null # "user@hostname" when in claimed/, else null
timestamp: 2026-05-18T12:34:56Z # ISO-8601 UTC, creation only — never updated
---
```

**Field rules**

| Field               | Mutable?                                      | Notes                                                                                       |
| ------------------- | --------------------------------------------- | ------------------------------------------------------------------------------------------- |
| `title`             | No                                            | Set at creation.                                                                            |
| `dependsOn`         | No                                            | Set at creation. If deps change, add a Note explaining and modify as needed. |
| `humanNeeded`       | Yes (append-only context: flip + Note)        | May be toggled by any agent; must be accompanied by a Note.                                 |
| `humanNeededReason` | Yes (with `humanNeeded`)                      | Free-text.                                                                                  |
| `claimedBy`         | Yes (only on open→claimed and claimed→closed) | Set to machine id on claim; leave as-is on close.                                           |
| `timestamp`         | **Never**                                     | Creation time only.                                                                         |

### Body — append-only

```markdown
<Original description written at creation. NEVER edit or rewrite this.>

## Notes

### 2026-05-18T14:23:00Z — yannick@thinkpad

Discovered the bug also affects Safari 17. Scope unchanged.

### 2026-05-18T15:10:00Z — yannick@thinkpad

Resolution: fixed in commit abc1234. Closing.
```

**Strict Note format:**

```
### <ISO-8601 UTC timestamp> — <user@hostname>
<free-form markdown content>
```

Corrections, status changes, and clarifications all go as Notes. The original description is **immutable**.

## The `humanNeeded` flag — read this carefully

`humanNeeded` is **TRUE** whenever completing the issue requires a human being to actively participate. The agent cannot finish it alone, even with full tool access.

### Set `humanNeeded: true` when the issue involves ANY of:

- **Interviewing, asking, or interacting** with the user (e.g. "interview the user", "ask the user about X", "gather requirements", "clarify with stakeholder").
- **Human decision-making** that the agent cannot make autonomously (architecture choices, product direction, naming preferences, prioritization).
- **Human-only actions**: providing credentials/secrets, manual approvals, physical actions, accessing systems the agent has no tools for, signing off legally/financially.
- **Review/sign-off** as an explicit step (e.g. "user must approve the PRD before merging").
- **Subjective feedback** (taste, UX feel, "does this look right?").
- **Skills/tools that interact with the user** by design — including but not limited to: `to-prd`, `grill-me`, `interview-*`, anything that "asks", "interviews", "consults", "elicits".

### Set `humanNeeded: false` only when:

The issue can be **fully completed by an agent** using code, files, shell, and other autonomous tools — without ever needing to pause and wait for a human response or action.

### Heuristic — ask yourself before writing the frontmatter:

> "If I claim this issue and work on it autonomously, will I at some point have to **stop and wait for a human** to do something or answer something?"
>
> - **Yes** → `humanNeeded: true` + write a `humanNeededReason` describing WHAT the human must do.
> - **No** → `humanNeeded: false`.

### `humanNeededReason` — required when flag is true

Concrete, actionable description of what the human contribution is. Examples:

- ✅ `"User must be interviewed via the grill-me skill to gather project requirements."`
- ✅ `"Needs AWS production credentials from the ops lead."`
- ✅ `"Requires user sign-off on the proposed API contract before implementation."`
- ❌ `"Some human input needed"` (too vague)
- ❌ `null` (forbidden when `humanNeeded: true`)

### Worked examples

| Issue description                                              | humanNeeded | Reason                                 |
| -------------------------------------------------------------- | ----------- | -------------------------------------- |
| "Interview user via grill-me and produce a PRD"                | **true**    | Interview is a human-in-the-loop step. |
| "Refactor `auth.ts` to extract token validation into a helper" | false       | Pure code work.                        |
| "Decide between Postgres and SQLite for the workshop demo"     | **true**    | Decision belongs to the user/team.     |
| "Bump all dependencies and fix resulting type errors"          | false       | Mechanical, agent-doable.              |
| "Add dark mode — colors to be picked by the user"              | **true**    | Subjective choice required.            |
| "Add dark mode using the existing design tokens"               | false       | All inputs available in the repo.      |
| "Use to-prd skill to draft a PRD for the new billing module"   | **true**    | `to-prd` interviews the user.          |

### Flipping the flag later

If during work an agent discovers human input is needed after all:

1. Flip `humanNeeded` to `true` and fill `humanNeededReason`.
2. Append a Note explaining the discovery.
3. If currently in `claimed/` and you cannot proceed, leave it claimed and surface the blocker to the user — do **not** silently move it back to `open/`.

## 6. Operations

### Create an issue

1. Compose the description (body without frontmatter).
2. Compute `short-id = sha1(body)[:4]`.
3. Build kebab filename.
4. Write file into `.issues/open/` with frontmatter (`claimedBy: null`, `timestamp: now`).
5. If git: `git add` + commit with message like `issues: open a3f1 add dark mode toggle`.

### Claim an issue (open → claimed)

Preconditions — **refuse if any fails:**

- This machine has **no other issue** currently in `.issues/claimed/` with `claimedBy == <this machine>`.
- Every `short-id` in the issue's `dependsOn` exists as a file in `.issues/closed/`.

Then:

1. (git) `git pull --rebase`.
2. Update `claimedBy: <user@hostname>` in frontmatter.
3. Move file: `.issues/open/<file>` → `.issues/claimed/<file>`.
4. Append a Note: `Claimed by <user@hostname>.`
5. (git) commit: `issues: claim a3f1`.

### Close an issue (claimed → closed)

Preconditions:

- Issue is in `.issues/claimed/` and `claimedBy == <this machine>`.

Then:

1. Append a **mandatory resolution Note** explaining the outcome (what was done, commits, or why it's being closed without action).
2. Leave `claimedBy` as-is (historical record).
3. Move file: `.issues/claimed/<file>` → `.issues/closed/<file>`.
4. (git) commit: `issues: close a3f1`.

### Reopen / re-route

Do **not** edit a closed issue. Create a new issue and reference the old short-id in its description / `dependsOn` if appropriate.

## 7. Guardrails — refuse with a clear message

The agent MUST refuse and explain when asked to:

- Edit or rewrite the original body of any issue.
- Modify `title` or `timestamp` after creation.
- Claim a second concurrent issue on the same machine.
- Claim an issue whose dependencies aren't all closed.
- Take over (`claimedBy`) an issue already claimed by another machine — escalate to the user instead.
- Move a file directly without updating frontmatter / writing a Note as specified above.

## 8. Quick mental model

```
open/      ← anyone can pick from here (if deps closed)
claimed/   ← exactly one per machine at a time
closed/    ← immutable history; deps point here
```

Each issue file = an append-only changelog of its own lifecycle. The folder is its state. Simple, git-mergeable, no DB.

## Prerequisites

- Ensure all required tools and dependencies are installed
- Verify you have the necessary permissions and access credentials
- Check that the target environment is in a known good state


## Error Handling

- Always check the exit code or response status of commands before proceeding
- On failure, log the error details and attempt recovery if a retry strategy exists
- If recovery fails, report the error with context: what was attempted, what went wrong, and suggested next steps
- Never silently ignore errors — treat unexpected output as potential failure


## Verification

- After each step, verify the expected outcome before continuing
- Use idempotent checks: running the same action twice produces the same result
- If verification fails, roll back the last change and report the issue
- Log verification results for audit trail


## Rollback

- Every action should have a defined undo procedure
- If a step fails after partial completion, reverse all changes made in this session
- Verify the system is in a known good state after rollback
- Document what was rolled back and why


## Security

- Never hardcode secrets, tokens, or credentials in skill files or scripts
- Use environment variables or secret management tools for sensitive values
- Validate all user inputs before processing
- Follow least-privilege principle: request only the permissions you need
- Log all security-relevant actions for audit
