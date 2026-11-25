---
name: meta-review
description: >-
  Retrospective audit of the user's own Claude Code sessions. Use whenever the
  user wants to review, analyze, or reflect on their Claude Code chat history /
  logs / past sessions to surface recurring patterns, repeated mistakes,
  instruction violations, workflow friction, missing skills or automation, or
  suboptimal tech choices — and to decide what to improve. Triggers include
  "meta-review", "/meta-review", "проанализируй мои чаты/сессии с claude",
  "ретроспектива работы с агентом/claude code", "что можно улучшить в моём
  workflow / как я работаю с claude", "где я / агент работает неоптимально",
  "разбери мои логи claude", "review my claude code sessions", "audit how I use
  claude", "what patterns show up in my history", "what should I automate".
  Fans out review subagents across distinct lenses, presents a color-coded
  prioritized findings list (🔴 important / 🟡 significant / 🟢 minor), asks the
  user what to act on, applies the chosen changes, and appends one JSONL line
  per run to a per-project log (.meta-review.jsonl) that records the
  last-review date so each run resumes from there (defaulting to the past week
  on first run). Use this skill rather than ad-hoc grepping of session files.
---

# meta-review

Audit how the user and Claude Code have actually been working together — over a
window of real session history — then turn that into a short, prioritized,
actionable list and apply what the user picks. Each run is logged so the next
run resumes from where this one stopped.

You are the **orchestrator**. The heavy, noisy reading of session logs happens
inside subagents (one per lens) so this conversation's context stays clean and
you keep only the findings. Do not read 60 session files yourself.

## The data you're reviewing

Claude Code stores each session as a JSONL file under
`~/.claude/projects/<encoded-cwd>/<session-id>.jsonl` (the cwd's absolute path
with every non-alphanumeric char replaced by `-`). Records carry an ISO8601
`timestamp` and the `cwd`. Two ways to read this history:

- **meta-cc MCP tools** (preferred) — purpose-built aggregation over a project's
  sessions, with `since`/`until` time filters and `jq_filter`. Load them with
  `ToolSearch` (query `meta-cc`) since they're deferred. They default to
  `scope: "project"` (current project, all its sessions). See
  `references/meta-cc-queries.md` for the call recipes per lens.
- **Raw JSONL** (fallback) — if meta-cc is unavailable or broken (it's
  hand-patched on this machine and occasionally breaks), read the session files
  directly with `grep`/`jq`. The helper's `plan` output lists the exact files.

## Inputs (optional args)

Parse anything the user passed after the skill name; otherwise use defaults.

| Arg / phrase | Effect |
|---|---|
| _(nothing)_ | Scope = current project. Window = since last review, else past 7 days. |
| `all` / "all projects" / "везде" | Scope = every project under `~/.claude/projects`. |
| `<path>` | Scope = that project's cwd path. |
| `<N>d` / "last N days" / "за N дней" | Force window = past N days (ignore last-review date). |
| `since <DATE>` / "с <дата>" | Force window start. |
| `--default-days <N>` | Change the first-run default (otherwise 7). |

The log lives at `.meta-review.jsonl` in the **cwd where the skill is invoked**
(the project root), regardless of scope.

## Workflow

### 1 — Resolve the window and scope

Get the project dir (so the subagents and helper agree on it):

```
meta-cc get_session_directory(scope="project")   # → the ~/.claude/projects/<...> dir
```

Then resolve the window + session list with the helper:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/meta_review.py" plan \
  --log .meta-review.jsonl \
  --cwd "$PWD" \
  --scope project \
  --project-dir "<dir from get_session_directory, if you have it>"
```

`plan` prints JSON with: `since`/`until` (the window), `default_used`,
`last_review_at`, `project_dirs`, `session_count`, `sessions[]`, and
`open_items[]` (unresolved items carried over from the previous run). If
meta-cc's `get_session_directory` fails, omit `--project-dir` — the helper
resolves the dir itself from `--cwd`.

### 2 — Show the plan, then proceed

Briefly tell the user (in their language): the window (`since` → `until`),
whether it's the first-run default or resumed from the last review, the scope,
how many sessions fall in the window, and any **open items** carried over. Then
proceed — don't wait for approval unless the plan looks clearly wrong or the
user asked to choose the window. If they want a different window/scope, re-run
`plan` with adjusted args.

A high `session_count` is normal (many sessions are tiny). The subagents filter
to real activity via meta-cc's `since`/`until` — they do not open every file.

### 3 — Fan out one subagent per lens (in parallel)

Spawn the review subagents in a **single message with multiple Agent calls** so
they run concurrently. There are five lenses; read `references/lenses.md` for
the full brief of each and embed it in the subagent prompt:

| Lens | Looks for |
|---|---|
| **A · Workflow & repetition** | recurring patterns, repeated manual toil, flow friction, steps that could be collapsed/simplified |
| **B · Errors & dead-ends** | mistakes made, tool errors & retries, wasted loops, things that broke and why |
| **C · Instruction adherence** | where Claude deviated from CLAUDE.md / skills / the user's corrections — and, reciprocally, where an instruction is missing, ambiguous, or should be improved |
| **D · Skill & automation gaps** | multi-step sequences that should become a skill, hook, script, or alias; toil worth automating |
| **E · Tech & approach quality** | suboptimal technology / library / command / architecture choices by the user; better tools or patterns available |

Give every subagent the same context block (window, scope, project dirs, the
session file list, and how to read history) plus its own lens brief and the
**finding schema** from `references/finding-schema.md`. Require it to return a
JSON array of findings (each with evidence: a session id + a short quote or turn
reference — findings without evidence are not allowed). Tell each subagent to
load meta-cc via ToolSearch and prefer it, falling back to raw `grep`/`jq` on
the listed files.

"What can be improved" is not its own lens — every lens proposes improvements.

### 4 — Aggregate

Collect all findings. Then:
- **Merge duplicates** — the same issue often surfaces under several lenses;
  fold them into one finding and note the corroborating lenses (cross-lens
  agreement is itself a strong signal — flag those as key findings).
- **Group** by lens/theme.
- **Re-rank** each finding's severity yourself; subagents over- and under-rate.
- **Fold in open items** from `plan` — re-flag any that still apply; mark
  resolved ones as such.

### 5 — Present a color-coded, prioritized list

Present in the user's language, sorted by severity, grouped sensibly. Use these
three statuses and emojis exactly:

- 🔴 **important** (важно) — high impact; address soon
- 🟡 **significant** (значимо) — meaningful; worth doing
- 🟢 **minor** (не критично) — nice-to-have / low effort

For each finding give: a one-line title, the evidence (which sessions / how
often it recurred), the concrete recommended action, and a rough effort. Lead
with the cross-lens / highest-impact findings. Keep it scannable — this is a
decision aid, not an essay. If nothing material surfaced, say so plainly rather
than padding the list.

### 6 — Ask what to act on

Ask the user, per finding (or in batches), what to do: **apply now**, **defer**
(carry to next run), or **dismiss**. Offer a quick "apply all 🔴" style batch.
Let them add their own items. This is the user's call — don't auto-apply.

### 7 — Act on the chosen items

Execute what the user picked, using the right tool for each:
- **Instruction fixes** → edit `CLAUDE.md` / `CLAUDE.local.md` / memory.
- **New skill** → invoke the `skill-creator` skill.
- **Hook / setting / permission / automated behavior** → invoke `update-config`.
- **Code / tech improvements** → make the change (or, if it's real feature work
  in the itsai repos, follow the project's own workflow, e.g. `/feature`).
- **Dev-heavy or deferred findings → file them in the project tracker** so they
  aren't lost (see below). This is the default home for anything the user defers
  or that needs real implementation work rather than a quick edit.
- **Note-only** → just record it; no change.

Verify each change landed (re-read the edited file / confirm the skill or hook
exists, or that the tracker card was created) before claiming it's done.

#### Filing deferred / dev-heavy findings into the tracker

If a YouGile board is connected (MCP `mcp__yougile-mcp__*`), create one card per
such finding in the **tech-debt column**, **color-coded by severity**:

1. Find the column: `get_projects` → `get_boards` → `get_columns`; match a column
   titled `Tech Loan` / `Tech Debt` / `Техдолг` (case-insensitive). In the itsai
   workspace that's project **Product Dev** → board → column **`Tech Loan`**
   (`000f3310-7b41-4110-be6f-b56fbd405ae1`). If no such column exists, ask before
   creating one.
2. `create_task` with a title **prefixed by the severity emoji** 🔴/🟡/🟢 (the
   MCP exposes no native card-color and the board may have no stickers, so the
   emoji prefix is the reliable colour signal), and a description carrying:
   problem · evidence (session ids / occurrences) · recommendation · effort ·
   `Источник: meta-review <date>, ракурс <X>`.
3. Record each as a `decision` with `action: "deferred"`, `artifact:` the card id.

### 8 — Record the session

Build the session record (schema in `references/finding-schema.md`) and append
it as one line:

```bash
echo '<record-json>' | python3 "${CLAUDE_SKILL_DIR}/scripts/meta_review.py" record --log .meta-review.jsonl
```

The record must include `reviewed_at`, `window`, `scope`, `sessions_analyzed`,
the full `findings[]`, and `decisions[]` (one per finding: `applied` /
`deferred` / `dismissed` / `noted`, with what was changed). `reviewed_at`
becomes the next run's `since`, so set it to `until` (the end of the window you
actually reviewed), not "whenever I happen to finish". Confirm the line was
written.

If this is the first run (`log_exists: false`), mention the new
`.meta-review.jsonl` file and offer to add it to `.gitignore` (don't assume).

## Notes

- Keep findings honest and specific. "You sometimes make mistakes" is useless;
  "across 4 sessions you re-ran failed `make deploy-dev` 3× before checking
  `check_pushed` — add a pre-flight" is actionable.
- Scale the effort to the window. A week of light use → a few finders, terse
  list. "Do a thorough audit" or a long window → push the subagents harder and
  go deeper.
- Respect the user's environment rules (CLAUDE.md / CLAUDE.local.md): never SSH
  or touch prod as part of a review, and present in the user's language.
