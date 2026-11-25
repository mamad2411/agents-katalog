---
name: html-progress-report
description: >-
  Maintain ONE living, single-file HTML progress page per project so the user can
  quickly catch up on what a coding agent did, why, and what's next — with
  plain-language explanations and rich visuals (KPI cards, task board, charts,
  flow diagrams, before/after, diffs, timeline). Use when the user asks to
  report / summarize / show progress or methods ("汇报", "进展", "总结一下做了什么",
  "update the progress page", "status report", "what changed"), or after
  finishing a meaningful milestone in a project that already has a progress page
  (.agent-progress/index.html). Do not use for one-off answers that need no record.
---

# HTML Progress Report

The page exists to keep **the user and the agent aligned** while a project moves: the user comes back,
sees in a minute where things are, *and checks whether the agent's understanding still matches theirs*.

You keep a **single living HTML file** (with several pages inside) per project that lets the user catch up on
a coding agent's work in under a minute. It is not a new report each time: you
**update the snapshot** and **prepend one timeline entry**.

The reader is the user themself: technical, short on time, possibly coming back
after hours away. Optimize for *fast re-orientation*, not formality.

## Page anatomy

One HTML file, **several pages** switched from a left sidebar (hash routing: `#overview`,
`#method`, …; keys `1`–`9`; "All" button shows every page on one scroll for Ctrl+F / print).

```
┌ sidebar   project · status · page list (auto-built from <section class="page">)
├ header    status badge · last updated · branch@commit               (rewrite)
├ 📍 overview  TL;DR · KPIs · task board · ⚠ needs your decision      (rewrite)
├ 🤝 align     goal card · my own decisions · assumptions · deviations — user marks ✓/✗/? (update every time)
├ 🧭 method    picture-first: idea → old-vs-new → diagram → real example → formula → why (edit when approach changes)
├ 📊 results   charts · tables · ablations                            (edit when new evidence)
├ …            optional extra pages after <!-- @pages:insert -->
└ 🕒 timeline  newest first; one entry per milestone                  (prepend, never delete)
```

Each region is fenced by HTML comment markers. **Only edit inside markers.**

| Region | Markers | Update rule |
|---|---|---|
| Header | `<!-- @header:start -->` … `<!-- @header:end -->` | Every update |
| Overview | `<!-- @snapshot:start -->` … `<!-- @snapshot:end -->` | Every update (replace whole block) |
| Alignment | `<!-- @align:start -->` … `<!-- @align:end -->` | Every update: add new decisions/assumptions/deviations, apply user feedback |
| Method | `<!-- @method:start -->` … `<!-- @method:end -->` | Only when the approach/architecture changed |
| Results | `<!-- @results:start -->` … `<!-- @results:end -->` | When new numbers/ablations land |
| Extra pages | insert `<section class="page" id="…" data-nav="…" data-icon="…">` after `<!-- @pages:insert -->` | Only if a topic doesn't fit the pages above (e.g. "Data", "Deploy") |
| Timeline | insert right after `<!-- @timeline:insert -->` | Prepend one `<article class="entry">` |
| Archive | `<!-- @archive:start -->` … `<!-- @archive:end -->` | Links to archived pages |

Each page starts with `<header class="page-head"><div class="kicker">…</div><h1>…</h1><p class="lede">…</p></header>`.
Pages stay short: if a page needs more than ~3 screens, split it into another page.

## Workflow

### 1. Locate or create the page
- Root = `git rev-parse --show-toplevel` (fallback: current working directory).
- Page = `<root>/.agent-progress/index.html` (unless the user or project rules name another path).
- If missing: copy `assets/template.html` (path relative to this SKILL.md) there,
  fill the `{{...}}` placeholders, set `<html lang>` to the output language, translate the
  static labels (`data-nav` page names, timeline page head, search placeholder; pager/buttons follow
  `lang` automatically), and
  add `.agent-progress/` to `<root>/.git/info/exclude` (local-only ignore, does not touch
  the repo) unless the user wants it committed.
- If it exists: read the header, the Now block and the **top 2 timeline entries** only
  (not the whole history) to learn the last recorded state and `data-commit`.

### 2. Gather facts (never invent)
- `git log --oneline <last data-commit>..HEAD`, `git diff --stat <last>..HEAD`, current branch/commit.
- **Look beyond the checked-out branch** — the active work is often elsewhere:
  `git for-each-ref --sort=-committerdate --format='%(committerdate:short) %(refname:short) %(upstream:track)' refs/heads refs/remotes | head`
  and `git worktree list`. If another branch has newer commits, read it with `git show <branch>:<path>`
  (never switch branches), and record which branch you treat as mainline as an alignment `decision`.
  Unpushed commits (`[ahead N]`) and deleted worktrees that still own branches are risks worth a claim.
- Note the gap between the newest commit and today; if work may be happening off-repo (a server, a
  notebook), say so as an `assumption` instead of presenting the repo as the whole story.
- Test/lint/build results you actually ran; metric files (csv/json/logs) the work produced.
- What was tried and failed, and decisions made in the conversation.
- Every number on the page must come from a command output or file. If unverified, label it
  `<span class="badge warn">unverified</span>`.

### 3. Decide what to write
- **New entry vs. update:** if the top entry covers the same task in the same session,
  update it in place instead of adding a near-duplicate.
- One entry = one milestone (feature landed, bug fixed, experiment finished, direction changed),
  not one tool call.
- Rewrite **Now** to reflect the present state — it must make sense without reading the timeline.
- Touch **Method** only if the design changed; then mention it in the entry ("method updated").
- When you write or rewrite **Method**, it must be **picture-first** — the reader should get it from the
  figures alone. Follow `references/writing-guide.md` §2b: `.idea` one-liner → old-vs-new `.flow`
  (removed parts `.step.x`) → architecture `.diagram` (JSON → SVG, offline) → **one real example with
  real outputs** (`.imgflow` of actual images/heatmaps, or `ol.walk`) → key `.formula` → `.why` cards →
  limits. Prose between visuals ≤ 2 lines; the validator warns when the method page exceeds its text budget.
- Real pictures beat drawn ones: if the project produces images (inputs, masks, heatmaps, plots), run the
  existing inference/plot code on 1–2 examples and save small thumbnails (≤160 px, jpg/png) to
  `.agent-progress/assets/`, referenced by relative path. Never fabricate an output image.

### 3b. Alignment (the most important page)
Misalignment usually comes from three places; the 🤝 page surfaces each as a `.claim` the user can mark:
- **Goal drift** → the `.goal` card: the goal in *your own words*, done-criteria, constraints, and explicit
  **non-goals**. Rewrite it when your understanding changes; never copy the user's wording verbatim
  (restating is what exposes misunderstanding).
- **Silent decisions** → `data-kind="decision"`: every choice you made without asking (library, scope cut,
  default value, skipped step, simplification in a diagram). Say why, what you rejected, and how costly
  it is to reverse.
- **Wrong beliefs** → `data-kind="assumption"`: facts about the project you rely on. Tag the evidence
  honestly: `run` (you executed it), `code` (you read it), `doc` (README/paper/chat), `guess`.
  Verify cheap guesses before publishing them. Add `data-kind="deviation"` when the work differs from
  what was asked, and `question` for things only the user can answer.
- Keep ≤15 open claims, newest/riskiest first; each has a stable `data-id` (`d3`, `a7`, …) and
  `data-since="<commit>"`.

**Processing feedback.** The user marks claims ✓/✗/? and pastes a block starting with
`[对齐反馈]` / `[Alignment feedback]` into the chat. When you see it:
1. For each ✓: set `data-user="confirmed"` on that claim (it collapses and stops asking).
2. For each ✗ or ?: act on the note (fix code, redo the analysis, or ask), then rewrite or remove the claim.
   Never silently keep a rejected claim.
3. Record the outcome as a `decision`-tagged timeline entry ("Alignment: 3 confirmed, a4 corrected — …").

### 4. Write it (directly in HTML, using components)
- Follow `references/writing-guide.md` for language and structure (conclusion first,
  what → why → result → next, define jargon, analogies, honest failures).
- Pick visuals from `references/components.md`. **Every entry gets at least one visual**
  (flow, chart, compare, board, diff, table, tree). Prefer pictures over paragraphs.
- Use the file-edit tool on marker regions; never regenerate the whole file once it exists.
- Output language = **the language the user is currently using in the conversation**.
  Keep code identifiers, paths, commands and metric names as-is.

### 5. Validate
Run `python3 <skill_dir>/scripts/check_page.py <page>` and fix all errors (markers, page ids, JSON in
charts/diagrams, diagram edges to unknown nodes, missing image files, entry attributes, tag balance) and
the method warnings. It needs only the Python standard library.
If a headless browser is available (e.g. Playwright), screenshot each page (`index.html#method`, …) once
and look at it: overlapping labels and wrapped image strips are only visible this way.

### 5b. Keep it small
If the timeline has more than ~30 entries, move the oldest ones to
`.agent-progress/archive-YYYY-MM.html` (copy the template, put them in its timeline) and add a
link inside the archive markers.

### 6. Hand back
Reply in chat with a clickable link to the page plus ≤3 lines: what changed and any
decision the user must make. Don't repeat the page content.

## Timeline entry contract

```html
<article class="entry" data-time="2026-11-20T21:30:00+08:00" data-tags="feature" data-status="ok" data-commit="a1b2c3d">
  <div class="panel">
    <header>
      <h3>Short outcome-first title</h3>
      <span class="badge ok">done</span>
      <span class="when">11-20 21:30</span>
    </header>
    <p><b>What:</b> … <b>Why:</b> … <b>Result:</b> …</p>
    <!-- ≥1 visual component -->
    <details><summary>Details</summary> commands, files, caveats </details>
    <div class="facts"><span>commit <code>a1b2c3d</code></span><span>+120 −34 in 5 files</span><span>tests 48/48 ✅</span></div>
  </div>
</article>
```

- `data-time`: ISO 8601 with timezone (drives the "NEW since last visit" highlight).
- `data-tags`: space-separated from `feature fix experiment research refactor docs infra decision blocked`.
- `data-status`: `ok | warn | bad | info`.
- `data-commit`: HEAD short hash at time of writing (next update diffs from it).

## Don'ts
- Don't create a new page per report; don't delete history.
- Don't paste raw logs or long code; summarize and put essentials in `<details>`.
- Don't add external dependencies beyond the optional Mermaid CDN already wired in the template;
  the built-in CSS components, `.chart` and `.diagram` renderers work offline. Prefer `.diagram` over Mermaid.
- Don't put everything on one page or write paragraphs where a diagram/card/chart would do.
- Don't claim success without evidence; show failures and dead ends — they are the most useful part.
