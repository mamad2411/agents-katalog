---
name: mc-zenn
description: Turn MulmoClaude work into a Zenn tech article (markdown) inside the workspace. On first use it sets up a Zenn project at `github/zenn/` — clone an existing GitHub repo or `zenn init` a fresh one, idempotent and skipped when already initialized — then writes articles to `github/zenn/articles/<slug>.md` tagged with the `MulmoClaude` topic. Use when the user says "Zenn にまとめて", "この作業を記事にして", "share this on Zenn", "Zenn 始めたい", or "Zenn のリポを用意して".
---

# Zenn

A bundled MulmoClaude preset skill (`mc-` prefix = launcher-managed; do not edit
this file in the workspace, it is overwritten on every server boot).

Help the user share what they did in MulmoClaude as a Zenn tech article. Two
jobs in one skill: **(1) make sure a Zenn project exists in the workspace** and
**(2) write an article from the work**. Writing auto-runs setup first when the
project isn't there yet, so the user can jump straight to "Zenn にまとめて"
without thinking about setup.

Keep the machinery invisible — the user shouldn't have to think about slugs,
frontmatter, or zenn-cli internals.

## Where things live

The Zenn project is a git repo inside the workspace at `github/zenn/`
(cwd-relative — the agent runs with cwd = workspace, so every path here is plain
cwd-relative). Articles are markdown files at `github/zenn/articles/<slug>.md`.
Zenn publishes by syncing a connected GitHub repo, so this directory is a real
git repo the user pushes to.

**Is it initialized?** The project is ready when `github/zenn/articles/` exists.
Use that as the idempotency marker — never re-init a directory that already has
it.

## Workflow 1: set up the Zenn project (idempotent)

**Triggers**: "Zenn のリポを用意して", "Zenn 始めたい", "set up Zenn", "まだ
Zenn 作ってない". Also runs automatically as Step 0 of Workflow 2.

**Step 1 — check first.** If `github/zenn/articles/` already exists, the project
is ready: say so in one line and stop. Re-initializing is never correct. Only
continue when it's missing.

**Step 2 — clone or init.** Ask which with one `presentForm` (two choices),
unless the user already told you:

- **Clone an existing Zenn repo** (they already write Zenn on GitHub). Get the
  repo URL, then:

  ```bash
  git clone <url> github/zenn
  ```

  `npx zenn` fetches zenn-cli on demand, so a missing local dependency is fine.

- **Create a fresh project** (standard zenn-cli flow):
  ```bash
  mkdir -p github/zenn
  cd github/zenn && npm init --yes && npm install zenn-cli && npx zenn init
  ```
  (`yarn add zenn-cli` works too if the user prefers yarn.) `npx zenn init`
  scaffolds `articles/`, `books/`, and a README. Then make it a git repo:
  ```bash
  cd github/zenn && git init -b main
  ```

**Step 3 — confirm + point at the next step.** One line ("Zenn project ready at
github/zenn/."). For a freshly created project, name the one manual step Zenn
needs: connect the GitHub repo on zenn.dev → "Deploy from GitHub" (browser only
— it can't be automated). Then offer to write the first article.

## Workflow 2: write an article from MulmoClaude work

**Triggers**: "この作業を Zenn 記事にして", "今やったことを記事化", "Zenn に
まとめて", "share this on Zenn".

**Step 0 — ensure setup.** If `github/zenn/articles/` doesn't exist, run
Workflow 1 first, then continue.

**Step 1 — gather the material.** Prefer what the user points at (a wiki page,
an artifact, files, a MulmoScript story). Otherwise use the current session's
work: the chat transcript at `conversations/chat/<session-id>.jsonl` (list with
`ls -t conversations/chat/*.jsonl | head` if you don't know the id) plus the
artifacts and files it produced. Pull out **what / why / how / result** and keep
the reproducible commands and code. Ground every claim in what actually
happened — don't invent.

**Step 2 — pick a slug.** Zenn slugs are **12–50 characters, lowercase a–z /
0–9 / `-` / `_`** (pattern `^[a-z0-9_-]{12,50}$`). Build a readable kebab slug
from the title's English keywords (e.g. `mulmoclaude-zenn-workflow`). Pad a
short one with a date (`date '+%Y%m%d'`) or 4 hex chars. Check
`github/zenn/articles/` for collisions. If a clean slug is hard, run
`cd github/zenn && npx zenn new:article` to get a valid random-slug skeleton and
fill it in. **A published slug becomes the article URL and can't change** — pick
it deliberately.

**Step 3 — write the frontmatter** (Zenn house style):

```yaml
---
title: "<a clear title, in the user's language>"
emoji: "<one emoji that fits the topic>"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["MulmoClaude", "<related>"]
published: true
---
```

- **Always include `MulmoClaude` in `topics`.** At most 5 topics, no spaces
  inside a single topic.
- `type` defaults to `tech`; `published` defaults to `true` (use `false` when
  the user wants a draft). `emoji` is exactly one character.

**Step 4 — write the body.** Zenn markdown: intro (what / why) → steps or
implementation (fenced ` ```lang ` blocks, runnable commands) → result → a short
wrap-up. Informative but casual; describe the work, not yourself. Put images in
`github/zenn/images/` and reference them as `![alt](/images/<file>)`.

Write it the way a person would, not the way a model defaults to. Each rule
below comes from real reader feedback — ignore them and the draft reads as
machine output:

- **Sound human, not like a generated listicle.** Prefer flowing prose over
  walls of bullets, use bold sparingly, and let paragraphs connect into an
  argument. If every section is just a heading plus a list, vary the rhythm.
- **No uncommon loanwords or jargon.** Use only terms a typical reader already
  knows. Niche English acronyms, trendy katakana, and insider slang either get
  dropped or replaced with plain words. A term the field itself hasn't settled
  on ("code smell" and the like) is a red flag — say the plain thing instead
  ("code that works now but bites you later").
- **Define every term and acronym on first use**, in plain language, and put the
  foundational ones up front — define "DRY" before the article leans on it. A
  reader should never hit a word they can't parse.
- **Carry a source's essence, don't just cite it.** When an idea comes from a
  book or article, explain the idea itself in your own words; "see <book>"
  teaches nothing. Search for the actual content when you're unsure what it says,
  then write the substance.
- **Make the article self-contained.** Anything project-specific — a repo's
  internals, a config choice, a domain constraint — needs enough general
  background that a reader with zero context can follow. Running longer is fine
  when the extra length buys understanding.
- **Match the stated audience.** "Explain to intermediate developers" means
  patient explanations, concrete examples, real code from the work, and links —
  not a terse summary.

**Step 5 — save + preview.** Write `github/zenn/articles/<slug>.md`. Tell the
user the path and how to preview: `cd github/zenn && npx zenn preview`
(http://localhost:8000). Surface the title, slug, and topics.

## Workflow 3: publish

**Only when the user asks** ("公開して", "push して"). Zenn deploys on push to
the connected branch (usually `main`); this is a content repo, so working on
`main` is expected — no feature-branch / PR dance.

- Stage the changed file(s) **individually** (never `git add .`), then commit
  and push:
  ```bash
  cd github/zenn && git add articles/<slug>.md && git commit -m "docs: add <slug>" && git push
  ```
- Confirm before pushing. If the repo has no `origin` yet (freshly created,
  not connected), the user must create + connect the GitHub repo on zenn.dev
  first — point them there instead of guessing a remote.

## Tone

Practical and quiet about the machinery. The user wants their work shared, not a
lecture on zenn-cli. Ask at most one thing at a time, and only when you genuinely
can't proceed (which repo to clone, publish vs draft). Otherwise write the
article and show them the result.
