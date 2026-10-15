---
name: todo-infographic
description: Use when the user invokes /todo-infographic, says "make an infographic", "visualize this plan", "I can't read walls of text", or after a plan is finished. Also auto-triggered by the Stop hook when a ready/in-progress project's infographic is missing or stale. Builds artifacts/infographic.html and links it in the project's active or archived registry row.
---

# Project Infographic Skill

You turn a project's `plan.md` + `tasks.md` into a **one-page, self-contained HTML infographic** — a visual the user can review at a glance instead of reading the full plan. The plan stays the source of truth; this is the scannable view.

## Hub location

The hub repo root is `$TODO_HUB` — an environment variable pointing at your hub folder (default `~/todo`). Resolve **every** path against this absolute root — active `index.md`, cold `archive.md`, and each project's files — regardless of the current working directory. This skill may be invoked from another repo; never assume cwd is the hub. Pass this absolute root to each build subagent so it reads and writes there, not into the cwd. (Same convention as `todo-refer`.)

## Execution tier

The infographic generation — the token-heavy, creative design and HTML work in Step 3 —
uses the **balanced** tier with **high** reasoning effort from
[`../todo-llm-routing/SKILL.md`](../todo-llm-routing/SKILL.md). Delegate the build when dispatching is
available; otherwise build inline. The orchestrating session does the light work:
resolve projects, check stubs, register the result, and confirm.

When dispatching, spawn **one subagent per project** and run them in parallel only when
the user explicitly requested several projects. Give each subagent that project's
`plan.md`, `tasks.md`, any existing HTML, and the Step 3 specification. It writes
`artifacts/infographic.html` and returns a one-line confirmation. Then the orchestrator
handles Steps 4–5. Use the host-specific balanced model only when the host supports
per-dispatch model selection; never invent unsupported parameters.

**Compose with design skills.** Instruct each build subagent to load the `artifact-design` skill (if installed) before designing, and `dataviz` before drawing any chart-like element — progress bars, stat cards, phase meters all count. These skills are distilled design procedure; loading them is cheaper than a redesign round. If a design-critique / frontend-design skill is installed, the subagent runs one self-critique pass against it before writing the final file — one pass, not a loop.

**Before dispatching**, check whether `artifacts/infographic.html` already exists for each project. If it does, read its full content and pass it to the subagent as `existingHtml`. The subagent uses this to preserve the theme exactly (see Step 3). Also gather the file footprint (Step 2.5) and pass it as `fileFootprint` — the subagent must never run git itself or invent file paths.

## How the user invokes this

```
/todo-infographic event-fanout   ← one project by short-name
/todo-infographic projects/work/...                ← full path also works
/todo-infographic all                              ← every ready/in-progress/done project (explicit opt-in only)
/todo-infographic                                  ← the project in scope for this session (NOT all stale ones)
```

**Scope: single-project by default.** Generate the infographic only for the project the session is working on. Do **not** fan out to every project. `all` is an explicit opt-in — never inferred. If no single project is clearly in scope and no argument was given, ask which project rather than defaulting to all.

It is also fired automatically by the plugin's **Stop hook** (`infographic-staleness.sh`, auto-registered): when a project whose status is `ready` or `in-progress` has a missing or stale `artifacts/infographic.html`, the hook lists it before ending the turn. The hook's list is a repo-wide staleness scan, **not** a scope instruction — regenerate only the listed project(s) you actually worked on this session, and leave the rest stale. If none of the listed projects relate to this session, stop without generating anything.

## Step 1 — Resolve the project(s)

Resolve named projects active-first in `$TODO_HUB/index.md`, then by exact short-name in
`$TODO_HUB/archive.md`. Record the owning registry.

- Short name → look it up active-first; duplicates are corruption and stop the run.
- Not found in either registry → tell the user and stop.
- Full path → use as-is.
- `all` → read both registries and operate on every `ready`, `in-progress`, or `done`
  project. Only when the user explicitly passes `all`.
- No argument → resolve to the single project in scope for this session. If that's ambiguous, ask — do **not** default to every project.

## Step 2 — Read the plan and guard against stubs

For each target project read `plan.md` and `tasks.md`.

**Stub check (important):** if `plan.md` still contains the template text `What success looks like in one sentence.` or has no real Goal/Scope content, it is an unfilled stub. **Do not generate an infographic for a stub.** Report it: e.g. "reserve-mcp-integration is marked `ready` but plan.md is still the template — run `/todo-plan <name>` to fill it first." Then skip that project.

## Step 2.5 — Gather the file footprint (git evidence, orchestrator side)

The file footprint is **execution-time truth** — it always comes from git in the target repo (the `repo` column / plan.md Repo path), never from what the plan predicted. Run this in the orchestrating session before dispatching:

- On a feature branch → `git diff --name-status $(git merge-base <default-branch> HEAD)..HEAD`, plus `git status --porcelain` for uncommitted/untracked files.
- On the default branch → uncommitted/untracked only; if tasks.md or `artifacts/journal.md` names an identifiable merged range or PR, diff that range instead.
- Repo missing on disk, or no changes attributable to this project → no footprint; the section is dropped (see Step 3).

Produce a flat list of `path` + status (`A` added / `M` modified / `D` removed / `R` renamed). For each file, try to match it to a tasks.md line for a one-line "why"; leave the why blank when no task clearly matches — **never invent one**.

## Step 3 — Build the infographic (balanced tier, high effort)

Produce `artifacts/infographic.html` inside the project folder through the execution path
above. Keep it self-contained: no network, no external assets, everything inline. It
must open offline and print cleanly.

**Theme: existing vs. new — decide first.**

- **`existingHtml` provided** → **preserve the theme exactly.** Extract the CSS — palette (hex values / CSS variables), font stack, card styles, layout structure, spacing, visual personality — and carry it forward unchanged into the new file. Your job is **content-only**: update stat numbers, bullet text, phase progress bars, and section data to match the current `plan.md` / `tasks.md`. Do not change any visual property. **Content additions are allowed**: if the existing file predates the What & why / footprint / trade-off / forgone / limitations sections or the ID chips, add them — styled with the existing theme's CSS, not a new look.
- **No `existingHtml`** → **invent a fresh visual theme.** Pick a distinctive palette, typographic treatment, and layout personality that suits this specific project; let it differ from other projects. Everything visual is yours to design.

In both cases: aim for a polished, genuinely scannable one-pager, not a generic dashboard. The structural constants are the content sections below and the at-a-glance, no-walls-of-text discipline.

Fill these sections from the plan. **Summarise — never transcribe.** No walls of text; if a bullet runs long, compress it to a clause.

- **Header** — project name, short-name · category, status pill (`ready`/`in-progress`/`done`), repo path.
- **Goal** — the one-sentence goal, lightly bolded on the key noun.
- **What & why** (`W1`) — 2–3 sentences from plan.md Context: what is being implemented and the approach taken. Not a restatement of the goal — the goal says *where we end up*, this says *what we're building and how*.
- **Stat cards** — 3–5 at-a-glance numbers. Always include phase count and task count (`N done`). Add 2–3 project-specific metrics that matter (channels, new apps, LOC, before→after footprint, target version — whatever the plan emphasises).
- **Scope** — In (green) vs Out (muted), the most important items only.
- **Flow / Topology** — if the plan has an architecture or data-flow (ASCII diagram, "topology", request path), render it as boxes + arrows. Mark net-new pieces `.new`, the focal path `.accent`, untouched/legacy `.old`. Delete the section entirely if there is no flow — don't ship an empty shell.
- **File footprint** (`F1`, `F2`, …) — render `fileFootprint` as an indented tree grouped by directory. Per-file: a status badge (added = green, modified = amber, removed = red), its `F` ID, and the one-line "why" where known. Collapse directories with many same-status files into one row (`hooks/ +4 added`). No `fileFootprint` data → drop the section entirely.
- **Trade-off ledger** (`D1`, `D2`, …) — one card per Key Decision, keeping the plan's `D` numbering. Each card: the decision one-liner, then a gain (green) / cost (coral) pair from plan.md Trade-offs. Plans without a Trade-offs section fall back to the old style: numbered decision cards with one-line rationale. Note the "don't re-litigate" framing if the plan has it.
- **Forgone** (`X1`, `X2`, …) — a muted strip: alternatives rejected and scope deliberately cut, each with its one-clause why. From Trade-offs **Forgone** plus any Scope Out item that carries a reason. Nothing recorded → drop the section.
- **Limitations** (`L1`, `L2`, …) — amber chips: what this build deliberately does **not** handle. From Trade-offs **Known gaps**. These are accepted gaps, not risks — the risk stays in **Note**. Nothing recorded → drop the section.
- **Constraints** — chips; mark hard non-negotiables with `.warn`.
- **Execution Plan** — one `.phase` block per phase header in `tasks.md`. Each shows a `done/total` badge, a progress bar whose width = `round(done/total*100)%`, and a short summarised bullet list of that phase's tasks. Flag the riskiest/biggest phase with a distinct badge.
- **Note** — the single biggest risk or gotcha from the plan (its `## Notes` section when present, else the sharpest constraint or context caveat). Drop the section when nothing qualifies.
- **Footer** — "Generated from plan.md + tasks.md · <today's date>" + "plan.md remains the source of truth". Use today's date from context — do not invent a timestamp. Below that, one feedback line: *"Feedback: quote an ID in chat ('D2 is wrong because…'). This session: `/todo-revise <short-name>`. Later session: start with `/todo-refer <short-name> resume`."*

### Section IDs — the feedback handle

Every reviewable element carries a short stable ID rendered as a small chip in its corner, so the user can give feedback by pointing at an ID instead of describing a location. The registry:

|Prefix|Element|
|-|-|
|`W1`|What & why|
|`D<n>`|Decision / trade-off card (numbering **must** match plan.md's Key Decisions)|
|`F<n>`|File row in the footprint|
|`X<n>`|Forgone item|
|`L<n>`|Limitation chip|
|(task no.)|Phase tasks already have numbers (`4.5`) — no extra ID|

Rules: assign in document order on first generation. On regeneration, an element that still exists **keeps its ID**; new elements take the next unused number; never renumber or reuse a removed ID. Style the chip small and muted — it's a handle, not decoration.

### Counting tasks for the bars
Count `- [ ]` (open) and `- [x]` (done) checkboxes per phase. **Skip the `## Status` legend block** that the tasks.md template ships (its `- [ ] Not started` / `- [x] Done` lines are documentation, not tasks), **skip `## Notes` / `## Context` sections**, **skip anything inside HTML comments** (the template's `## Revisions` section has a commented-out example with a `- [ ]` line), and **skip fenced code blocks** — the same exclusions the deterministic helpers apply. A shell count, if useful:

```bash
awk '/<!--/{c=1} c{if(/-->/)c=0; next} /^[[:space:]]*(```|~~~)/{f=!f; next} f{next} /^## /{p=($0!~/^## (Status|Notes|Context)([[:space:]]|$)/)} p&&/^[[:space:]]*- \[/{t++} p&&/^[[:space:]]*- \[x\]/{d++} END{print d+0"/"t+0}' tasks.md
```

## Step 4 — Register it in the owning registry

The owning row in `index.md` or `archive.md` has an `infographic` column. Set that cell
to a link to the file you generated:

```
[open](projects/<cat>/<name>/artifacts/infographic.html)
```

Projects without one stay `-`. There is no separate Infographics table — the column is the only place this is tracked, so don't create one.

## Step 5 — Confirm

Tell the user, briefly, which infographics you generated/updated (with clickable paths), which projects you skipped as stubs, and that they can open the `.html` in a browser. Don't paste the HTML.

## Notes
- Visual quality matters — this exists because the user can't review walls of text. Favour structure, colour-coding, and whitespace over completeness. If a detail doesn't earn its place on one screen, leave it in plan.md.
- Give each **new** infographic its own character — a different palette and personality per project is the point. Don't converge on one house style when starting fresh. When updating an existing one, do the opposite: preserve the CSS verbatim so it stays visually consistent across refreshes.
