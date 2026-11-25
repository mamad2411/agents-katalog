---
name: readmedaddy
description: >-
  Use when writing or improving a README — thin, stub, outdated, a wall of text,
  unscannable, or missing; a new repo needs a front page; no quickstart, install,
  badges, or examples; broken instructions or AI slop. Triggers include "write me
  a README", "make this README better", "the readme sucks", "polish the readme",
  "readme.md", "project front page", "documentation landing". Works for any repo:
  CLI, library, framework, app/SaaS, infra, data/ML, agent skill, research,
  monorepo, internal tool. Yields to user and project instructions; never invents
  facts about the code.
license: MIT
metadata:
  version: 0.3.0
---

# readmedaddy

Generate the best possible README for the work in front of you — a "Fable-class"
README — by reading what the project actually is, borrowing the conventions of the
best READMEs *for that kind of project*, drafting candidate sections, and ranking
them through a contextual multi-gate rubric until the front page earns its first
screen.

**What "Fable-class" means here.** A README that, in the first screen, tells a
stranger what this is and why they'd care; gets them to a working first result in
under ~30 seconds; stays skimmable; is honest about limits; and follows the
conventions a reader of *this archetype* already expects. Not a history lesson, not
a feature dump, not AI slop. Front-load value, prove it, then let the curious scroll.

**Core principle.** A README is judged by its archetype. A CLI lives or dies on a
demo and a one-line install; a library on copy-pasteable API usage and trust badges;
a data/ML project on results and citations; an agent skill on what triggers it and a
worked example. The same section that's essential for one is bloat for another. So
detect the archetype *first*, weight the rubric to it, and never apply a generic
template. Match the work to its peers, not to a checklist.

## Run this first: detect the ARCHETYPE

Before drafting a single line, classify the project. Read the repo, don't guess:
check the manifest and entrypoints (`package.json` bin vs main/exports, `pyproject`,
`Cargo.toml` `[[bin]]` vs `[lib]`, `SKILL.md`, `Dockerfile`/compose, notebooks,
`go.mod`), the directory shape, and any existing docs. Assign one primary archetype
(a project may be a blend — pick the dominant reader's expectation):

- **CLI** — installed and run from a terminal. Reader wants: a demo (gif/asciinema)
  and the smallest real command.
- **library / package** — imported into other code. Reader wants: install + minimal
  API usage, badges, API surface.
- **framework** — scaffolds or hosts other code. Reader wants: mental model,
  quickstart, conventions, when-to-use.
- **app / SaaS** — a running product or service. Reader wants: what it does, a
  screenshot, how to deploy/run, status.
- **infra** — deploys or operates systems. Reader wants: prerequisites, topology,
  apply/teardown, safety/secrets.
- **data / ML** — models, datasets, experiments. Reader wants: the result up front,
  benchmarks/tables, reproduce steps, citation.
- **agent-skill / agent-tool** — a Claude Code skill, MCP server, or LLM tool. Reader
  wants: what it does, *when it triggers*, and a worked example.
- **research** — a paper, study, or finding. Reader wants: abstract/result,
  figures, citation, honest scope.
- **monorepo** — many of the above. Reader wants: a map of packages and where to go.
- **internal tool** — audience is teammates, not the public. Reader wants: why it
  exists, ownership, a runbook (run / deploy / rollback), gotchas.

State the detected archetype in one line and proceed. If genuinely ambiguous or the
user contradicts you, ask once; otherwise assume and note it. Load the archetype's
profile from `references/archetypes.md` for its section menu; the gate weights
live in `references/multi-gate-rubric.md`.

## Then: generate → multi-gate-rank → iterate

1. **Pull the patterns.** Open `references/famous-readme-patterns.md` for the
   conventions and exemplars of the detected archetype — section order, what the
   first screen does, what earns its space, what to omit.
2. **Generate candidates.** Draft the README, and where a section has real choices
   (the hook line, the quickstart command, whether a diagram earns its place),
   generate 2–3 genuinely distinct candidates rather than one safe default. Pull
   every fact — commands, install lines, names, claims — from the repo, never from
   assumption. If you can't verify it, don't assert it.
3. **Rank through the gates.** Score the draft against the ten gates below (0–5
   each), **weighted by archetype** per `references/multi-gate-rubric.md`. Keep the
   highest-scoring candidate per section; rewrite anything scoring ≤2 on a
   heavily-weighted gate.
4. **Iterate until it clears.** Re-rank after each rewrite. Stop when the
   heavily-weighted gates for this archetype are strong and nothing material is
   missing — not when a generic template is "filled in".

The full generate→rank→merge workflow — including when to escalate to a full
tournament of whole-README drafts with a judge panel — is in
`references/generation-and-ranking.md`.

Run the draft through the G10 anti-slop tells in
`references/multi-gate-rubric.md` before finishing: kill
"in today's fast-paced world", negative-parallelism stacking ("it's not X, it's Y"
repeated), gratuitous rule-of-three, and empty AI vocabulary. Voice is a gate (G10),
not a finishing polish.

## The multi-gate README ranking rubric

Score each 0–5. **Weights are contextual to the archetype** — see
`references/multi-gate-rubric.md` for the per-archetype weight table.

- **G1 Hook** — the first screen instantly conveys what it is and why you'd care: a
  one-line value prop, not a backstory.
- **G2 Identity & trust** — name, one-liner, badges (CI / version / license /
  downloads), tasteful social proof.
- **G3 Visual** — logo / ASCII / diagram / screenshot / gif that is *apt* and earns
  its space, never gratuitous.
- **G4 Quickstart** — install plus the smallest real usage in under ~30s,
  copy-pasteable and correct.
- **G5 Scannability** — heading hierarchy, short paragraphs, tables, a TOC when long;
  skimmable in seconds.
- **G6 Completeness** — usage, config, examples, links, contributing, license —
  without bloat.
- **G7 Credibility** — real examples, tests/CI signals, honest limitations and
  non-goals.
- **G8 Contextual fit** — follows the conventions of its archetype (CLI vs library vs
  app vs infra vs data/ML vs skill vs research).
- **G9 Community & maintenance** — contributing, code of conduct, changelog,
  support/roadmap signals.
- **G10 Voice** — distinct, confident, no AI slop (no "fast-paced world", no
  negative-parallelism stacking, no rule-of-three padding).

**Archetype weighting (examples).** CLI → G3 (demo) + G4 heavy. Library → G4 (API
usage) + G2 (badges) + G6. App/SaaS → G1 + G3 (screenshot) + G9. Data/ML → G1 + G7
(results/benchmarks) + citations. Agent-skill → G1 + triggers + G4 (examples) + G8.
Research → abstract/results + citations + G7. The full table is in
`references/multi-gate-rubric.md`.

## Composition and precedence

This skill decides README *content and shape*. It yields, highest first, to: host
safety policy; an explicit live user instruction; standing project docs
(CLAUDE.md / CANON.md / AGENTS.md) and any house README template; then this skill's
defaults. If the project mandates a README structure, follow it and apply the gates
*within* it. Never invent facts, results, badges, or links the repo doesn't support —
an honest thin README beats an impressive fictional one.

**Operate offline.** Every fact comes from the local repository; never fetch
anything over the network to write a README — no web searches, no remote
templates, no URL lookups. The repo in front of you is the entire input. (The
patterns this skill draws on are baked into its reference files for exactly
this reason.)

## Keep it fresh (auto-update hook)

A README rots the moment the code moves on without it. An optional Claude Code Stop
hook watches a project's signal files — manifests, entrypoints, CI, install scripts —
and, when they change while the README does not, prompts you to refresh it *through
this skill, in the same session*. It detects drift and asks; it never rewrites files
on its own and never breaks a session. `install.sh` wires it up in one step. Full
behavior, config, and modes are in `references/auto-update-hook.md`.

## init — guard a repo

When the user says "readmedaddy init", "guard this repo", or "set up
readmedaddy": configure the whole system through the wizard script — it is the
single serializer; never write `.readmedaddy.json` or the workflow YAML
directly.

1. Detect first, silently: `git rev-parse --show-toplevel`, README path via
   `git ls-files`, default branch, whether origin is GitHub, existing
   `.readmedaddy.json` (reconfigure mode).
2. Ask at most **three** questions, one at a time, stating every detected fact
   as an assumption the user can veto: nudge mode (auto/notify/enforce/off),
   CI gate (comment/fail/off — comment is the advisory-first default), and
   watch-list confirmation.
3. Two-step through the script: run
   `python3 scripts/readmedaddy-init.py --print` with every answer as a flag
   (`--mode --pr --main --sweep --watch --readme --badge/--no-badge
   --no-hook`), show the user the output as the preview, then on approval
   re-run the same flags **without** `--print` to write. `--yes` = the
   recommended preset.

The wizard makes zero network calls; it writes only the config, the workflow
file, one badge line, and (optionally) the Claude Code hook registration —
each enumerated in the preview.

## What's in references/

- `references/archetypes.md` — the ten archetypes: detection signals, the section
  menu each reader expects, and what to omit.
- `references/famous-readme-patterns.md` — per-archetype exemplars and the patterns
  that make the best READMEs work.
- `references/multi-gate-rubric.md` — the ten gates with 0/5 anchors, the
  per-archetype weight table, the G10 anti-slop tells, and the merge procedure.
- `references/generation-and-ranking.md` — the generate→rank→iterate workflow and
  the whole-README tournament for high-stakes front pages.
- `references/auto-update-hook.md` — the readme-drift Stop hook: how it detects drift,
  its modes (auto / notify / enforce), config, and one-step install.
