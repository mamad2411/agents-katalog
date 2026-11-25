---
name: onboard-our-stack
description: >-
  Onboard a newcomer to THIS codebase, or answer a targeted "how does our X
  work" question, by walking curated reading lists and synthesizing the mental
  model — never by guessing. Works out of the box: with a committed
  .claude/onboard/topics.yaml it walks that curated path; without one it
  cold-starts from the repo's own authoritative docs (README, CLAUDE.md /
  AGENTS.md, ARCHITECTURE.md, docs/, the dependency manifest, the entry point)
  and says plainly what curated knowledge is still missing. The newcomer never
  creates files, runs setup, or changes code. Use for "I'm new, help me
  understand this project", "where do I start", "onboard me", "explain our auth
  flow", "how does our scheduler work", "walk me through our X". Do NOT use for
  generic programming or public-library questions, debugging a specific error,
  or writing/modifying code. It teaches an existing system; it does not generate
  documentation or code, and it never invents gotchas or asserts a file is
  load-bearing beyond what the sources actually say.
version: 0.3.0
---

# onboard-our-stack

Two jobs, one skill:

- **Broad onboarding** — "I'm new, help me understand this project." The reader
  needs a *route through* the system, in order.
- **Targeted** — "explain our scheduler." The reader needs *one subsystem*, on
  demand.

Tell them apart from the request: a named subsystem -> targeted; "new", "onboard
me", "where do I start", "understand the project" -> broad.

The institutional knowledge — which files are load-bearing, in what order, and
the gotchas that live only in people's heads — is curated in
`.claude/onboard/topics.yaml` by a maintainer, ONCE, and committed. A newcomer
just asks; they never author it and never change code to make this skill work.

## Availability ladder — the "works out of the box" guarantee

Pick the highest tier the repo supports. Never block the newcomer on setup, and
never demand maintainer input from someone who came here to learn.

1. **Curated config present** (`.claude/onboard/topics.yaml` at repo root) ->
   use it. Best tier: real ordering, real gotchas. See Broad / Targeted below.

2. **No config -> COLD START.** Do NOT refuse, and do NOT drop into config
   authoring (that is a maintainer-only flow, below). Orient the newcomer from
   the repo's own authoritative sources, in this order if present: README.md,
   CLAUDE.md / AGENTS.md, ARCHITECTURE.md, docs/ (a product doc and a runbook if
   they exist), the dependency manifest (pyproject.toml / requirements.txt), and
   the entry point (main.py / app). Synthesize a grounded orientation, citing
   each file. Derive getting-started from README/RUNBOOK. Then say plainly:
   "This is auto-read from your repo's docs, not a curated walk — the tribal
   knowledge a teammate would warn you about (stale docs, landmines, why it's
   built this way) isn't captured yet. A maintainer can run the setup, or I can
   help one author it."

   The line you must not cross: reading and citing the team's own docs is
   ALLOWED — that surfaces what's written, it is not a guess. Inventing gotchas,
   or asserting a file is load-bearing without evidence from a doc or the entry
   point's own imports, is NOT allowed. When unsure, attribute it or omit it.

3. **No config and no docs -> minimal.** Show the entry point, the dependency
   manifest, and the top-level tree; say honestly there's little to go on, and
   suggest a maintainer author `.claude/onboard/topics.yaml`.

## Broad onboarding (curated tier)

Walk `onboarding_path` in order — it is the curriculum the maintainer chose;
don't reorder it.

1. Lead with the "why" (the product/vision topic): what this is and who it's
   for, before any code.
2. Getting started: read the docs the `getting_started` topic points at
   (RUNBOOK/README) so the run/test commands stay current — do not hardcode or
   guess them.
3. The keystone: `request_lifecycle` — narrate ONE request end to end across the
   layers. This single story is what gives the model; everything else is depth.
4. Then the deep topics in path order, each as a short synthesis, not a file
   dump.
5. Defer per-topic gotchas to their topic — don't open with a barrage of
   warnings the reader has no model to hold yet. Surface at most one or two
   *global* landmines up front (e.g. a known doc-vs-code drift).
6. Close with a concrete first step: a small, safe area for a first change, and
   which topics to read for it.

Pace it: offer to go one topic at a time rather than dumping all of them.

## Targeted (curated tier)

Match the question to one topic by key or `one_liner`. Read its `read_in_order`
in order; if a path is missing the config is stale — warn, name the file, read
the rest, flag the gap. Synthesize the mental model, surface that topic's
`watch_out_for`, cite files, point at the `adrs`/specs for the why. Orientation,
not a line-by-line walk. Offer the nearest adjacent topic next.

## Config shape

`.claude/onboard/topics.yaml` has two top-level keys:

- `onboarding_path`: ordered list of topic keys — the broad-mode curriculum.
- `topics`: map of `<key>` -> { one_liner, read_in_order, watch_out_for,
  optional adrs }. Two topics are special by convention and belong early in the
  path: `getting_started` (points at the run/test docs) and `request_lifecycle`
  (the end-to-end story).

See `references/topics.example.yaml` for the schema and a worked example.

## Maintaining (maintainer-only; never blocks a newcomer)

A maintainer authors the config once, grounded in files they verify exist, and
commits it. Trigger the authoring flow ONLY when someone explicitly asks to set
up or curate onboarding — never as the default response to a missing config.
Copy `scripts/check_topics.py` out of the installed skill into the repo (e.g.
`ci/check_topics.py`) and run it in CI so stale paths fail the build; a stale
reading list teaches a wrong model, the one failure this skill exists to prevent.
