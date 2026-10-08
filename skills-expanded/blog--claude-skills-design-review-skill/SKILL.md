---
name: design-review
description: Run the multi-persona presentation review of this site — evidence capture, parallel critics, synthesis, HTML report, calibration gate, and optionally the fix phase.
disable-model-invocation: true
---

# Design review

A quality pipeline for this site's presentation: layout, typography, information placement, interaction, accessibility. Never the quality of the writing itself. One primary agent (you) owns evidence, synthesis, and the report; subagents are critics with narrow lanes.

Subagents run on **Opus** (`model: "opus"`), never Fable. Research/browse-only agents may run on Sonnet.

## Judging standard

The site's own documents are the standard: `DESIGN.md` (system + Rulings), `PRODUCT.md` (audience, boundaries), `CONTEXT.md` (vocabulary). A recommendation that conflicts with them is flagged as a **direction question** for Mathieu, never presented as a defect. Most high-value findings are violations of the site's *own* rules — hunt those first, they make fixes uncontroversial.

## Phase 1 — Evidence

1. Own the server: `bun run build && bun run preview`, or restart the dev server yourself — rehype-plugin and content-collection changes only load at server start, and reviewing a stale DOM wastes the whole run.
2. Use a named browser session per agent: `export AGENT_BROWSER_SESSION=<role>`; `agent-browser set viewport 1440 900`; screenshots with `--screenshot-format jpeg --screenshot-quality 80` (viewport + `--full` per route); `agent-browser snapshot > a11y-<route>.txt` per route. Run `agent-browser skills get core` if commands fail.
3. Enumerate routes from `src/pages/` (don't trust a remembered list) plus interactive states: art-stage hover, mid-article scroll, contents scroll-spy, copy button, a nonexistent URL.
4. Produce one **facts sheet** before spawning critics: computed styles and geometry for the load-bearing claims (sticky positions, link colors, element boxes, overflow widths, contrast pairs). Critics consume it instead of each re-measuring; a finding backed by a computed value outranks an impression.

## Phase 2 — Critics (parallel)

Every critic gets the shared brief: evidence paths, the judging standard, the scope rules, the finding schema. Lanes:

- **Craft**: visual hierarchy & layout · typography & color · information architecture · accessibility & interaction (live keyboard testing, a11y trees, axe)
- **Spec conformance**: diff every measurable claim in `DESIGN.md` against the facts sheet — unshipped rules and doc drift both count
- **Impeccable**: an agent that invokes the `impeccable` skill in audit mode
- **Personas** (browse the live site, report friction only): recruiter with 90 seconds · engineer landing on an article from search · someone trying to know the person

Scope rules (verbatim into every brief):
1. Presentation only; copy counts only as UI (labels, headers, standfirsts, invitations), article prose is out of bounds.
2. Findings on known placeholders go to an unranked "Placeholder notes" section.
3. Deliberate decisions (light-only theme, no hamburger, anything in DESIGN.md Rulings) are evaluated against the docs, not flagged as defects.
4. Include a Praise section: 2–3 things that work, so synthesis can protect them.

Finding schema: page/state (cite screenshot) · problem · why it matters (tied to the site's goals) · severity · recommendation (referencing existing tokens/components) · confidence. 4–10 findings per critic; a finding without evidence doesn't ship.

## Phase 3 — Synthesis and report

Dedupe across critics; the number of independent critics behind a finding is its confidence rank. Sort into: **A** clear problems (verified, fix-ready) · **B** weak spots (supported judgment) · **C** direction questions (conflict with docs or identity — Mathieu decides) · **doc corrections** (code right, docs stale).

Publish one HTML artifact with embedded annotated screenshots. Write it in **plain language**: what's wrong, why it matters, how to fix — no design-dialect ("apparatus", "standfirst", "ledger" only where quoting the docs), no jargon compression. Each A-finding carries its concrete fix.

## Phase 4 — Calibration gate

Mathieu reads the report and answers freeform. Every accept/reject on a C-question becomes a timeless rule in `DESIGN.md`'s **Rulings** section — present-tense fact, no dates, no review citations. Nothing from C is implemented without his answer.

## Phase 5 — Fix (separate pass, on request)

- Structural fixes only: fix the mechanism that produced the bug (cascade layering, a real grid track, a shared component), not the symptom. Load `codebase-design` first.
- Parallel implementation agents get **disjoint file lists** and never touch git state (no stash, no checkout); the primary agent owns git.
- Code comments state constraints, never history or review provenance. Markdown states present-tense fact — no "was retired", no prev-vs-now.
- Verify each batch in the browser against the Phase 1 screenshots; `bun run build` and `bun run lint` gate every commit. Commit and push only when Mathieu says so.

## Copy rules (when the run touches words)

- Calibrate on Mathieu's own writing (`src/content/blog/`) before proposing anything: plain, direct, complete sentences, concrete numbers, no aphorisms, no editorial cleverness, **no em-dashes**.
- Propose via multi-choice variants he picks from or corrects; never ship freeform drafts of his voice. His corrections are final text.
- Facts about him come only from him or his files. Blank placeholder beats invented specificity.

## Deferred backlog

Carried between runs: mobile pass (the scroll-driven art stage is the riskiest untested surface per `HANDOFF.md`), production-deploy verification, re-review when field reports and final artwork replace placeholders.
