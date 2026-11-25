---
name: micro-dev
description: Use when a dev task is small and well-scoped — a bug fix, a tiny feature, a one-file refactor, a config tweak, a guarded edge case — roughly 1-5 files with an outcome that is already understood, and the full GSD pipeline or a Superpowers brainstorming/TDD session would be overkill. Portable across Claude Code, Antigravity (`agy`), and Gemini CLI.
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Bash
  - AskUserQuestion
  - Task
  - mcp__token-savior__search_codebase
  - mcp__token-savior__find_symbol
  - mcp__token-savior__get_call_chain
  - mcp__token-savior__get_function_source
  - mcp__token-savior__get_full_context
  - mcp__token-savior__find_dead_code
  - mcp__token-savior__ts_search
  - mcp__code-review-graph__semantic_search_nodes_tool
  - mcp__code-review-graph__query_graph_tool
  - mcp__code-review-graph__get_impact_radius_tool
  - mcp__code-review-graph__get_affected_flows_tool
  - mcp__code-review-graph__get_minimal_context_tool
  - mcp__code-review-graph__get_review_context_tool
  - mcp__code-review-graph__detect_changes_tool
  - mcp__code-review-graph__refactor_tool
  - mcp__context7__resolve-library-id
  - mcp__context7__query-docs
---

# micro-dev

Act as a senior engineer who refuses to write code before the success criteria are written down.

## Overview

This skill turns a small, vague dev request into a **verifiable plan**: ambiguity check → scope → verifier → plan.

It **writes** the plan and executes fast-path tasks. Every task with a `PLAN.md` is handed to `executing-micro-plans`, which owns execution identically on every harness.

Core principles:
- **Verifier-first**: success criteria before the first line of code.
- **Surgical**: touch only what is required; delete what you replace.
- **Binary**: every criterion is pass/fail, proved by a command.
- **Stop over guess**: an unclear task is a question, not an assumption.

## When to Use

Tasks touching roughly 1-5 files with an outcome that is already understood: bug fix, small feature, one-file refactor, config tweak, guarded edge case.

| Situation | Use instead |
|---|---|
| Multi-phase feature, architecture, roadmap | GSD (`/gsd:new-project`, `/gsd:plan-phase`) |
| Genuinely ambiguous ask needing discussion | `superpowers:brainstorming` |
| Failure whose cause is unknown | `superpowers:systematic-debugging`, then this skill for the fix |
| A `PLAN.md` that already exists | `executing-micro-plans` |
| Architectural, data-model, protocol, or domain-rule decision to record or supersede | `adr` (`docs/adrs/`), standalone or as a step inside the plan |

## Quick Reference

| Decision | Rule |
|---|---|
| Fast path or full plan? | All four fast-path boxes checked → fast path. Otherwise full plan. |
| Where does the plan live? | `docs/micro/<YYYYMMDD>-<slug>/PLAN.md` while active, `docs/micro/archive/<YYYY-MM>/` once done |
| Has this area been touched before? | `grep -i '<keyword>' docs/micro/INDEX.md` — see Finding Past Plans |
| How many steps? | 3-7. More → not micro, reconsider GSD. |
| Who executes? | Fast path: this skill. Full plan: `executing-micro-plans`. |
| When to commit? | Never automatically. |

**Before writing your first plan, read `references/EXAMPLES.md`** — three worked plans (bug fix, mini-feature, refactor). Matching their shape is faster and more reliable than deriving it from the template alone.

## Output Format

The deliverable is one markdown file whose section headings are fixed. Do not rename, reorder, merge, or drop sections — `executing-micro-plans` reads them by name on the other harness.

```markdown
---
task: <one-line description>
description: <keyword-dense one-liner: what changed, in which files/area, with which technology — written for grep/mgrep search, not for a human reading the plan top to bottom>
status: planned
created: <YYYY-MM-DD>
---

# <task title>

## Context
- Existing code checked: <what was found / files involved>
- Fresh info looked up: <library/API researched, or "n/a">
- Git status checked: clean / <what was found and how it was handled>

## Simpler Alternative Considered
<the simpler approach, or "none — request is already the minimal change">

## Surgical Scope
- **Files touched**: [exact list]
- **Files NOT touched**: [list or "all others"]
- **Symbols replaced** (→ to delete before done): [list or "none"]
- **Symbols extended** (→ keep): [list or "none"]

## Definition of Done
- [ ] Build passes: `<exact command>`
- [ ] Tests pass: `<exact command or "n/a — no tests for this path">`
- [ ] No dead code: <replaced symbols confirmed removed, or "n/a — none replaced">
- [ ] Type check: `<exact command or "n/a">`
- [ ] Manual check: `<UI/API action or "n/a">`

## Steps
- [ ] Step 1: <concrete action>
- [ ] Step 2: <concrete action>
- [ ] Step N (teardown): Delete all dead code created by this plan. Run an orphan scan bounded to the replaced symbols. Confirm 0 orphans.

## Code Review
- Dead code removed: yes / no (list remaining if no)
- Build status: pass / fail (fix applied if fail)
- Type errors: none / fixed (describe)
- Unintended side effects: none / (describe)
- Security surface touched: no / yes (semgrep run: pass/fail)
- Verdict: ✅ DONE / ⚠️ BLOCKED (reason)

## Execution Log
(append-only, filled by executing-micro-plans)

## Notes
(deviations from plan, errors hit, corrections made)
```

`references/PLAN_TEMPLATE.md` is the same structure with inline guidance, ready to copy.

**`status`** is exactly one of `planned`, `blocked`, `done` — never `complete` or `completed`. The archive sweep matches `done` literally.

**`description`** exists for search, not for the reader. `task` is what a human sees in a listing; `description` is what a `grep`/`mgrep` query matches months later — pack in the symptom, the area touched, and any library/API name, even ones already in `task`.

## Plan Index

Every full plan (not fast-path tasks — those stay in `DAILY_LOG`) gets one line in `docs/micro/INDEX.md`, created with a `# Micro-dev Plan Index` header if missing:

```markdown
- [20261002-fix-metadata-keyerror](20261002-fix-metadata-keyerror/PLAN.md) — Fix KeyError on missing metadata field in the document router
```

Append the line when the plan file is created (frontmatter `status: planned`), using the folder slug and the `description` value. Link paths are relative to `docs/micro/`, where the index lives. Never rewrite existing lines when revisiting a plan — append-only, like the Execution Log. The one exception is the archive sweep, which rewrites the link path of a plan it moves; the description is never touched.

The index covers every full plan, active and archived, so it is the single entry point for search. It grows by one line per plan: query it with `grep`, never read it whole.

## Plan File Location

```
docs/micro/
├── INDEX.md                         one line per full plan, active and archived
├── DAILY_LOG-<YYYY-MM-DD>.md        fast-path log, current month only
├── <YYYYMMDD>-<slug>/PLAN.md        active plans: planned or blocked
└── archive/<YYYY-MM>/
    ├── <YYYYMMDD>-<slug>/PLAN.md    done plans, bucketed by the month in their folder name
    └── DAILY_LOG-<YYYY-MM-DD>.md    past months' logs
```

One folder per task, one plan inside it. Always forward slashes. The root holds only what is in flight; monthly buckets keep every directory small no matter how many plans accumulate.

**Slug**: derive from the task description, lowercase, `[a-z0-9-]` only, max 60 chars, no `..` and no `/`. Validate against `^[a-z0-9-]{1,60}$` **before** the slug reaches any shell command.

Resolve the slug first, then run the command with the real value substituted. For the slug `fix-metadata-keyerror`:

```bash
mkdir -p "docs/micro/$(date +%Y%m%d)-fix-metadata-keyerror"
```

Never execute a command that still contains a `<placeholder>`.

## Archive Sweep

Run at step 2 of every invocation, fast path included. It moves finished work out of the root:

- a plan folder at the root whose frontmatter reads `status: done` → `archive/<YYYY-MM>/`, and its `INDEX.md` link is rewritten to the new path;
- a `DAILY_LOG` from a month before the current one → `archive/<YYYY-MM>/`.

`planned` and `blocked` plans never move. Neither does a folder whose name does not match `^[0-9]{8}-[a-z0-9-]{1,60}$` — names read from disk are sanitized before they reach a shell command. `executing-micro-plans` never moves a plan: closing a plan leaves it at the root, where the user sees it, until the next sweep.

The sweep runs in two stages: a read-only listing, then one explicit command per item. Never fold the moves into a loop — a script that loops over `mv` and rewrites files with `sed` gets refused by permission classifiers, and redoing it by hand costs more than the two stages. Most invocations find nothing to move, and the listing alone then costs one call.

Where the `micro-archive-sweep.sh` SessionStart hook is installed (Claude Code on this machine), the same sweep already ran at session start and resume, and said so in one line if it moved anything. Still run Stage 1: it catches a plan closed earlier in this session. Stage 2 is then needed only for what Stage 1 lists.

**Stage 1 — list (read-only).** Prints one line per item to move, nothing otherwise:

```bash
cur="$(date +%Y-%m)"
for d in docs/micro/[0-9]*-*/; do
  d="${d%/}"; n="${d#docs/micro/}"
  printf '%s' "$n" | grep -qE '^[0-9]{8}-[a-z0-9-]{1,60}$' || continue
  head -n 8 "$d/PLAN.md" 2>/dev/null | grep -qE '^status: *done *$' || continue
  echo "plan $n archive/$(printf '%s' "$n" | cut -c1-4)-$(printf '%s' "$n" | cut -c5-6)"
done
for f in docs/micro/DAILY_LOG-*.md; do
  [ -e "$f" ] || continue
  n="${f#docs/micro/}"; m="${n#DAILY_LOG-}"; m="${m%-??.md}"
  printf '%s' "$m" | grep -qE '^[0-9]{4}-[0-9]{2}$' || continue
  [ "$m" = "$cur" ] || echo "log $n archive/$m"
done
```

**Stage 2 — move, one command per listed line**, with the real values substituted. For `plan 20260905-fix-currency-format archive/2026-09`:

```bash
mkdir -p docs/micro/archive/2026-09 && git mv docs/micro/20260905-fix-currency-format docs/micro/archive/2026-09/
```

Use plain `mv` when the path is not tracked by git. For a `plan` line, then rewrite its `INDEX.md` link with the Edit tool — `](20260905-fix-currency-format/PLAN.md)` becomes `](archive/2026-09/20260905-fix-currency-format/PLAN.md)`; only the path changes, never the description. A `log` line needs only the move.

Report what moved in one line. The sweep only renames files under `docs/micro/`; it is not a reason to stop in the git safety check.

## Finding Past Plans

Every finished plan stays searchable after archiving. Cheapest first:

```bash
grep -i '<keyword>' docs/micro/INDEX.md                          # every full plan, one line each
grep -ril '<keyword>' docs/micro --include=PLAN.md                # full text, archive included
grep -rh '<keyword>' docs/micro --include='DAILY_LOG-*.md'        # fast-path tasks
```

Where a semantic search tool is installed, `mgrep '<question>' docs/micro` answers "did we already fix something like this?" in one call.

Use it in step 3: a past plan that touched the same files records the decisions, pitfalls and test commands that apply again. Read its `## Notes` and `## Code Review` — not the whole file.

## Fast Path

The fast path skips the folder and the plan file. It is available only when **all four** hold:

- [ ] One file touched
- [ ] One change (typo fix, copy tweak, color/token swap, one-line config change)
- [ ] No realistic risk of interruption
- [ ] The file is **not** on the security surface (see below — membership is a lookup, not a judgment call; a one-line change to an auth file still takes the full plan, because blast radius is not visible from line count)

Any box unchecked → full plan. When genuinely unsure, take the fast path and escalate the moment a second step appears.

### Completing a fast-path task

1. Run the build command and read its exit code **in this same message**. No fresh evidence, no log entry.
2. Confirm the change created no dead code.
3. Append one line to `docs/micro/DAILY_LOG-<YYYY-MM-DD>.md`, creating it with a `# Daily Log <YYYY-MM-DD>` header if missing:

```markdown
- [x] 09:42 fix-metadata-keyerror — Fix KeyError on missing metadata field (`api/routes/document_router.py`)
```

The log is daily, which keeps the active file small and the context window clean. Past months' logs move to `archive/<YYYY-MM>/` with the sweep.

## Process

### 1. Surface ambiguity — before anything else

Is the task interpretable in 2+ ways, or missing a constraint (which file, which behavior on the edge case, which format)?

- Ambiguous → ask the user, then stop and wait. Do not guess and proceed.
- A simpler approach exists than the one the request implies → say so before starting; do not silently pick either one.
- Clear → continue.

### 2. Git safety check — before any file write

Run `git status`. Files inside the expected Surgical Scope carrying uncommitted changes from another session, or an unexpectedly dirty tree → stop and surface it. Never stash or discard silently. A clean, understood starting state is a precondition.

Then run the Archive Sweep.

### 3. Check existing code first

Search past plans first (see Finding Past Plans): one `grep` on `docs/micro/INDEX.md` for the area or symptom. Then search before writing. **Default: semantic search, then a targeted read with a line range.** Escape hatch: for an exact string or symbol, text grep is fine; where a code graph is available, an impact query answers "who calls this" with zero file reads.

The portable rule is the ordering — cheap and narrow before whole-file reads. Tool names are not portable: `mgrep`, `rtk`, `code-review-graph`, and `semgrep` exist only where they are installed. Assume nothing; on any harness or machine without them, native grep/glob plus targeted reads satisfy this step completely.

Never propose new code without confirming there is nothing to extend.

### 4. Fresh info when needed

Task touches a library, framework, SDK, API, or CLI → read current documentation before relying on training knowledge (Context7 or equivalent first, web search as fallback). Skip for pure business logic and refactors.

### 5. Choose fast path or full plan

Run the four-box fast-path checklist. Not all checked → create the plan file.

Aim for 3-7 steps. Apply **simple-first**: the smallest change that solves the stated problem. No speculative abstraction, no unrelated cleanup.

### 6. Fill Surgical Scope and Definition of Done first

Fill these two sections completely **before writing any step and before any code**. They are the contract.

- **Surgical Scope** prevents drift: exactly what will and will not be touched.
- **Definition of Done** defines binary success: each item is an exact runnable command, or `n/a` with a reason.
- **Simpler Alternative Considered** records the push-back from step 1: the option, or "none".

A plan with an unfilled Definition of Done is incomplete and must not proceed to execution.

Writing `description` here, not as an afterthought, forces it to be concrete — scope and DoD are already in front of you.

**Write machine-agnostic commands.** `pnpm build`, not `rtk pnpm build`. A local wrapper inside the Definition of Done makes the plan unrunnable by the next harness — which is the whole point of the file.

**Every requirement the user stated gets its own item.** A build command and a test command cover what the code does, not what the user asked for. If they said keyboard focus must stay visible, the page must work on a phone, no inline styles, French prose never in monospace, every public function documented — each of those is one item, and each is one command away from being binary:

```bash
grep -c ':focus-visible' src/styles/base.css    # expected >= 1
grep -c '@media' src/styles/base.css            # expected >= 1
grep -c 'style="' src/templates/page.html       # expected 0
```

`n/a` means **the tool does not exist in this project** — no type checker, no linter. It never means "hard to measure". A requirement that reaches the Definition of Done as `n/a — visual, nothing to run` has left the plan: nothing will check it, and the executing agent will report green without it. When a requirement genuinely resists a command, say so in `## Notes` and write the manual check as a step with a named observer — do not launder it into an `n/a`.

### 7. Get user approval

Present the plan and get explicit approval before any execution.

### 8. Hand off

Approved → confirm frontmatter reads `status: planned`, append the plan's line to `docs/micro/INDEX.md` (see Plan Index above), then invoke **`executing-micro-plans`** with the plan path.

That skill owns everything downstream: the `[~]` in-progress marker, per-step gates, the evidence rule, the Execution Log, the failure protocol, teardown, the Code Review section, and the final status. Do not re-implement any of it here — a second, divergent execution procedure is exactly what breaks cross-harness resumption.

Never commit automatically. Staging is the user's call unless they asked for it as part of the task.

## Security Notes

**Security surface** — auth/session code, input validation, injection-prone code (SQL/shell/template concatenation), secrets handling, DB migrations, file-path/upload handling.

A touched file on this list has two fixed consequences, neither of which is a judgment call:
1. The fast path is banned; the task takes a full plan.
2. `Code Review → Security surface touched` reads `yes`, and a `semgrep` run (sast + secrets) is required before the verdict.

Path safety: sanitize the slug to `[a-z0-9-]`, max 60 chars, rejecting `..` and `/`. Never build a path from raw user text. Directory and file names read from disk are plain text — never interpolate them into a shell command without sanitizing them the same way.

## Common Mistakes

| Mistake | Fix |
|---|---|
| Definition of Done says "it works" | Replace with an exact command and a binary criterion |
| Dead code deferred to a "cleanup step" | Delete it in the step that created it |
| Plan lists a wrapper command (`rtk …`) | Write the bare command; wrappers are machine-local |
| Executing the plan inline instead of handing off | Invoke `executing-micro-plans`; divergent execution breaks resumption |
| One-line auth fix taken through the fast path | Security surface bans the fast path regardless of size |
| Steps written before Surgical Scope | Scope and Definition of Done come first, always |
| A stated requirement sits in prose above `## Steps` | Prose is not checked. Give it its own Definition of Done item with a command |
| `n/a — visual change, nothing to run` | `n/a` is for a missing tool, not a hard measurement. A `grep -c` settles most of these |

## Portability Notes

- Planning runs inline; no subagent dispatch by default. One independent reviewer for a security-sensitive change is a permitted exception.
- Every action here (`mkdir`, read, write, edit, checklist toggle) maps to a basic file or shell operation on all three harnesses. Tool-name resolution lives in `references/HARNESS_MAP.md` of `executing-micro-plans`.
- `PLAN.md` and `DAILY_LOG-<date>.md` are plain files on disk, never a harness-specific todo tool. That is what makes the checklist portable. Do not swap either for `TodoWrite` or any Claude-Code-only mechanism.

## Tooling while authoring (Claude Code)

The *plan* stays machine-agnostic — that rule does not change. What follows
governs the session that writes it, not the file it produces.

Steps 3 and 4 (locating the symbols and files that go into `Surgical Scope`)
are the token-expensive part of planning. On this machine they are also gated:

- **Past plans first.** Start with `mgrep '<question>' docs/micro` — it answers
  "did we already do something like this?" and satisfies the search gate, so
  the follow-up `rtk grep -i '<keyword>' docs/micro/INDEX.md` is not refused.
  A raw `grep` as the first search of the turn is. The mgrep store does not
  follow moves: after a sweep moved something, use `mgrep search -s` (sync
  first), or a hit may name a pre-archive path. The SessionStart hook already
  launches that sync in the background after its own moves; a Stage 2 move
  made during the session needs it by hand. The folder slug survives the
  move — when a hit does not exist on disk, `rtk grep '<slug>'
  docs/micro/INDEX.md` gives its current path.
- **Project with a code graph** (`code-review-graph` tools present — the
  project's `CLAUDE.md` says so): use it before any file read to fill
  `Surgical Scope`. `semantic_search_nodes_tool` locates the symbol;
  `get_impact_radius_tool` on it lists the files a change reaches;
  `query_graph_tool` with `callers_of` decides *extend* vs *replace*, and with
  `tests_for` names the test file and command for `Definition of Done`. The
  graph can be stale: confirm in the source before writing the plan. An empty
  result means "not indexed", not "does not exist".
- **token-savior: always pass `project`.** Several projects are registered on
  this machine; without `project: "<repo name or absolute path>"`,
  `find_symbol` / `get_call_chain` / `search_codebase` scan the first
  registered project and report a false "not found".
- **Library or API (step 4)**: Context7 (`resolve-library-id` then
  `query-docs`) before any web search.
- Search by need, not by price. A natural-language question about the codebase
  goes to `mgrep '<question>'` first — the subscription is paid for exactly
  this, and a free fallback engages automatically when the quota runs out. A
  symbol whose name you already know goes to `mcp__token-savior__find_symbol`,
  which is exact and free; spending a credit there wastes it. A structural
  pattern goes to `ast-grep -p '<motif>' -l <lang>`, the only tool that can
  express one. Raw `grep`, `rg`, `find -name` and the `Grep` tool are refused
  until one of those has run in the turn.
- `ast-grep outline -l <lang> <file>` lists a file's symbols without reading
  it — enough to fill `Symbols replaced` in most cases.
- `Read` over 500 lines without `offset`/`limit` is refused. Locate, then read
  the zone.

**Never put a local wrapper in the plan.** `rtk` is applied automatically by a
hook when you run a command; writing `rtk pnpm build` into `Definition of Done`
makes the file unrunnable elsewhere. Bare commands, always.

Planning itself runs inline on the main model. When the permitted exception
applies (an independent reviewer for a security-sensitive change), dispatch it
on `sonnet` unless the change is irreversible — schema migration, auth path —
where `opus` earns its cost.

## References

- `references/PLAN_TEMPLATE.md` — the plan structure with inline guidance
- `references/EXAMPLES.md` — three worked plans: bug fix, mini-feature, one-file refactor
- `docs/micro/INDEX.md` — one line per full plan, appended at hand-off (see Plan Index), the entry point for Finding Past Plans
- `docs/micro/archive/<YYYY-MM>/` — done plans and past daily logs, moved by the Archive Sweep
- `executing-micro-plans` — executes, resumes, and closes out the plans this skill writes
