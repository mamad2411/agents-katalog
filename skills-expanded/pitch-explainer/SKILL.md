---
name: pitch-explainer
description: >-
  Package the spec, prototype, and implementation notes of finished or
  nearly-finished work into one self-contained document that gets reviewers
  to buy in fast. Use when the user says "pitch doc", "提案文档",
  "打包给评审", "给这轮工作写个提案", "把成果打包成汇报材料",
  "跟团队讲清楚这次改动", asks for a one-pager or explainer aimed at
  reviewers or approvers, or needs sign-off from people out of the loop.
  Not for verifying the user's own understanding (use change-quiz),
  proposals to green-light work not yet started (use implementation-plan),
  routine status reports (日报/周报), or neutral knowledge docs — wikis,
  READMEs, onboarding guides.
---

# Pitch & Explainer

Shipping needs buy-in. Reviewers start with the same unknowns the author
started with; experts want to see that the failure points they'd probe were
accounted for. Write for those unknowns, not the author's pride — the doc
succeeds when the reviewer's first question is already answered in it.

## Workflow

1. **Collect the artifacts.** Look for `implementation-notes.md` (project
   root) and the chosen prototype under `./design-directions/` — sibling
   skills leave them there. Also gather: the plan or spec, the diff, demo
   media (GIF/screenshots). If notes are missing, mine the session history
   and `git log -p` for decisions and surprises instead. Ask once if a key
   artifact is missing, then work with what exists. If a prototype was
   chosen from multiple directions, say so in the doc — "reviewed 4
   directions, ops picked this one" is itself evidence of diligence.
2. **Lead with the demo.** The first thing a reviewer sees should be the
   thing working — a demo GIF, screenshot, or live link. If no demo media
   exists (the common case for agent sessions), embed the work's actual
   output — a rendered report, a before/after diff of real behavior, a
   terminal transcript of the thing running. For pure backend work with
   nothing visual, lead with the single most convincing piece of evidence
   that it works: a worked input→output example, a benchmark against the
   obvious baseline, or a real request/response pair; a bare passing-test
   transcript is the last resort — if used, show named test cases
   (`pytest -v`), not a row of dots. Never skip this slot; never fake
   media — a static recreation or mockup is fine only when labeled as
   such, never presented as the shipped thing. Embed images as base64 data
   URIs so the file survives being dragged into Slack; downscale
   screenshots to ~1200px wide and re-encode (JPEG/WebP, quality ~80),
   keeping the whole file under ~2 MB — if media pushes past that, host it
   or split it out. In markdown venues that strip `data:` URIs (GitHub
   issues/PRs), attach or link images instead of embedding.
3. **Write one self-contained document** (`pitch-<topic>.html` in the
   project root; inline CSS/JS, no network; markdown if the venue demands
   it). Write it in the reviewer's language — default to the language of
   the conversation; if the reviewer's language differs or is unknown, ask
   once. For Chinese reviewers use these slot titles: 演示 / 为什么做 /
   改变了什么 / 做了什么 / 您可能想问 / 边界与开放问题 / 请您拍板.
   Do not commit it unless asked; in a git repo, exclude it:
   `n=pitch-<topic>.html; p="$(git rev-parse --git-path info/exclude 2>/dev/null)" && { mkdir -p "$(dirname "$p")" && { grep -qxF "$n" "$p" || echo "$n" >> "$p"; }; } 2>/dev/null || echo "note: could not exclude — leaving it untracked, never staging it"`
   Structure:
   - **The demo** — show it working, first.
   - **The problem** — why this exists, in the reviewer's terms.
   - **What it changes** — the before/after in numbers the reviewer cares
     about (time saved, errors prevented, money unblocked). One or two,
     honest.
   - **What was built** — the shape of the solution, key decisions and why.
   - **Anticipated questions** — the failure points and edge cases an
     expert reviewer would probe, each answered honestly. Pull from the
     implementation notes' Deviations and Surprises if they exist.
   - **Limitations & open questions** — what this deliberately does not do.
   - **The ask** — end with the exact decision requested: approve to ship,
     or a specific next step with a date.
4. **Make it droppable, then self-check.** One file the user can drop into
   Slack or an issue, readable on a phone — the deliverable is the file
   itself; do not render it as a Cursor canvas. Before handing it over,
   verify: it reads in five minutes — roughly 800 words (or ~1500 Chinese
   characters), count and cut; every link is a URL the reviewer can
   actually reach (issue, repo, doc link — never relative file paths; if
   none exists, inline a short appendix instead); The ask names one exact
   decision.

## Rules

- Do not oversell: limitations stated up front build more trust than
  completeness claimed and disproven.
- Every number must name its source inline: a spec acceptance item (label
  it "target"), an implementation-notes measurement, or a measurement you
  run now and record (git stats, a timed run, a quick benchmark — usually
  cheap for an agent). Never present spec targets as measured results.
- If a number the reviewer will ask for cannot be measured cheaply, state
  the claim qualitatively, mark it "not yet measured", and put the
  measurement plan in The ask — never invent, never go silent.
- If the approach is contestable, add an "Alternatives considered" line to
  What was built: name the strongest rival option and the honest reason it
  lost. One line per alternative, no straw men.
