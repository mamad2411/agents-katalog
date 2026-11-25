---
name: cli-forge-demo
metadata:
  author: clement
description: >
  Generate a reproducible live-demo kit for any project: a staged demo script
  (DEMO.md), deterministic seed and idempotent reset wired into the project's
  own task runner (make / just / task / npm / ansible / flux / chainsaw — never
  an imposed .sh), a pre-flight checklist, and a backup recording. Picks the best
  delivery support for the project (live, terminal GIF via VHS, asciinema cast/SVG,
  subtitled video, or a self-guided 'next-next' interactive walkthrough) and lets
  you force one. Tunes dramaturgy to the audience: technique, fonctionnel,
  commercial, or pédagogique. Use when the user says 'demo', 'démo', 'live demo',
  'demo script', 'demo gif', 'record a demo', 'show this off', 'walkthrough',
  'interactive tutorial', 'present OpenBao', 'sprint review demo', 'sales demo',
  'pitch demo', 'reproducible demo', 'reset demo data', 'seed demo', 'demo magic',
  'asciinema', 'vhs tape', 'demo that does not break'. Do NOT use for slide decks
  (use cli-forge-prez) or for a README (use cli-forge-readme).
argument-hint: "[project-path-or-feature] [--intent ...] [--support ...]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** This skill uses on-demand loading. Heavy content lives in `references/` and is loaded only when needed.

> **Language rule:** Skill instructions are English. Detect the project's primary language (README, comments, docs, commits) and generate the demo kit in that language. If bilingual, ask the user.

> **Diacritics rule:** When the chosen output language uses diacritics (French, Spanish, Portuguese, etc.), render them correctly — including on capitals (É, À, Ç, Ô…). Never strip accents to ASCII: write "sécurité" not "securite", "Rôle" not "Role". ASCII-flattened French is a defect, not a style.

> **Writing style:** Favor clarity — short sentences, one idea per sentence, plain words. A metaphor only when it clarifies. Keep one consistent register (impersonal/infinitive for operational docs). Separate narrative prose, meant to make the reader understand, from telegraphic content (tables, commands, checklists) which stays terse for action.

> **No fabricated output:** Never invent command output, console captures, API responses, metrics, or logs. When real output is needed, emit a clearly-marked placeholder (🚧 "replace with a real capture"), never plausible-but-fake text presented as real.

# Demo Forge — Reproducible Live-Demo Kit

> *"A good production is identical every night — not because the actors are lucky, but because the show is scripted, the marks are taped to the floor, and the stage is reset between performances."*

Generate everything needed to give the **same demo, flawlessly, every time**: a staged script, deterministic data, a one-command reset, a backup recording, and the delivery support that best fits the project.

## Core Principle — The Theatre

A live demo is a **staged performance**, not an improvisation. Eight mappings carry the whole skill (full model in `references/staging.md`):

| Stage craft | What it means for the demo |
|---|---|
| **The script & blocking** | `DEMO.md` — exact lines (what you say) and exact marks (the precise commands). No improvisation on stage. |
| **Same show every night** | Fixed seed: state, data, **clock**, and environment are pinned so the run is deterministic. Reality is seeded like a PRNG. The canonical reproducibility toolkit is `../shared/determinism.md` (consumed by `cli-forge-pipeline`, `cli-forge-resilience`, `cli-forge-perf`, `cli-audit-wizard`, `cli-forge-oci-rootless`) — demo is the *visible* twin of that contract. |
| **Reset the stage** | Returning to `s0` is **idempotent** and fast (`reset ∘ reset = reset`) so you can run the demo back-to-back. |
| **Open with the showstopper** | Do the last thing first — front-load the payoff (Great Demo!'s "Do It"), then peel back how. |
| **Hit your marks** | Golden path / vertical slice only. Every beat earns its place; deviation is where demos die. The golden path is **the T2-T3 rung** of `../shared/gate-ladder.md` made visible — what a demo *shows* is exactly what a fresh deploy + first operation *proves*. |
| **No scene runs long** | No uninterrupted segment over ~76 seconds (Gong data). Segment, checkpoint, interact. |
| **The understudy** | A pre-recorded backup (GIF / asciinema cast) and an offline mode. Never debug live > 45 s. |
| **The matinée** | The self-guided version the audience can re-run alone (interactive walkthrough). |

## Input

`$ARGUMENTS` is one of:
- **Project path / repo** — the skill reads the project and builds a demo of its golden path.
- **Feature or topic** — "demo OpenBao secret rotation", "show the audit-trail feature".
- **Empty** — reads the current project root, detects the headline capability, and asks for intent.

Optional flags: `--intent technique|fonctionnel|commercial|pédagogique`, `--support live|gif|cast|video|interactive` (force a support instead of the recommendation).

## Workflow

### Step 0 — Pick the cell: intent × support

A demo lives at the intersection of **who it's for** and **how it's delivered**. Read `references/tiers.md` for the full matrix and how dramaturgy shifts per cell.

**Axis 1 — Intent / audience** (ask if not given; do not guess the audience):

| Intent | Audience | Proves | Default framework |
|---|---|---|---|
| **technique** | devs / ops, conference, internal | "it works, here's how" | walking-skeleton, golden path end-to-end |
| **fonctionnel** | PO / stakeholders, sprint review | "the feature does the job" | Problem → Solution → Result |
| **commercial** | prospect / buyer, pitch | "this solves *your* pain" | Great Demo! Do-It + Situation |
| **pédagogique** | new user / contributor, onboarding | "you can do it too" | guided steps + verification per step |

**Axis 2 — Support** — **recommend dynamically, let the user force.** Detect signals, propose the best compromise, state why, then proceed unless overridden:

| Signal detected in project / request | Recommended support |
|---|---|
| CLI/TUI tool, README needs a moving picture (e.g. OpenBao) | **gif** (VHS `.tape`) — reproducible, doubles as integration test |
| Live audience, conference, sprint review | **live** + understudy recording |
| Onboarding, "let users try it", tutorial | **interactive** self-guided walkthrough |
| Docs site / README, copy-pasteable, lightweight | **cast/svg** (asciinema) |
| Accessibility / async / wide audience | **video** with subtitles (WebVTT) |

Announce the pick like: *"CLI tool + README → I'll generate a VHS gif demo (forceable with `--support live`)."*

### Step 1 — Reconnaissance

Read the project. Find the **one golden path** worth demoing: the headline capability, end to end, happy path only. Use the shared reconnaissance brief — read `../shared/recon.md` (same model readme and prez use, so all three tell one story). If several candidates, pick the one with the strongest "showstopper" and note the rest as out of scope.

First check the **Upstream inputs** table below: if `cli-forge-resilience` already mapped the golden path, or `cli-audit-test` named the nominal scenario, reuse it instead of re-deriving.

### Step 2 — Detect the runner (no imposed `.sh`)

The demo automation lives in the project's **existing** tooling. Read `references/tooling.md`. Detect in this order and emit targets there:

| Found | Emit |
|---|---|
| `Makefile` | `make demo`, `demo-seed`, `demo-reset`, `demo-gif` |
| `Taskfile.yml` (go-task) | `task demo:run / seed / reset / gif` |
| `justfile` | `just demo / demo-seed / demo-reset` |
| `package.json` scripts | `npm run demo:*` |
| `ansible/` playbooks | `playbooks/demo.yml` (tags: seed, reset, run) |
| Flux / kustomize | demo namespace overlay + seed `Job` |
| `chainsaw` tests | step assertions for k8s demos |
| **nothing** | propose a runner (prefer `make` or `just`); only then fall back to a documented POSIX `sh` snippet |

**Rule:** meet the project where it lives. Never drop a stray `demo.sh` next to a `Makefile`.

### Step 3 — Forge the script

Read `references/dramaturgy.md` (frameworks per intent) and `references/demo-md-template.md` (the skeleton). Write `DEMO.md` with:

- **Cold-open showstopper** — the wow result first, before the setup.
- **Numbered beats**, each with: the **exact command**, the **expected output** (so a mismatch is caught instantly), the **talk-track** (what to say), a **timing budget**, and a **recovery line** ("if this errors, say X and cut to the understudy").
- A **reset section** pointing at the runner target.
- A **fallback pointer** to the backup recording.

### Step 4 — Wire seed + reset + support

- **Seed**: deterministic, with a **fixed seed and fixed clock**, kept **separate from the app's own seed data**. Idempotent.
- **Reset**: idempotent and fast — re-runnable back-to-back (`git reset --hard && git clean -fdx` for repos, DB re-seed, `down && up` for containers, namespace recreate for k8s).
- **Support artifact** per Step 0:
  - **gif/video** → a VHS `.tape` (read `references/gif-video.md`): sizing, `Sleep`/`Type`/`Enter`, `Hide`/`Show` for setup, captions/subtitles for accessibility.
  - **interactive** → a self-guided walkthrough (read `references/interactive.md`): teachme/Killercoda/CodeTour-style stepped markdown with copyable commands and a verification per step.
  - **cast** → asciinema record/convert instructions (`agg` → GIF, `svg-term` → SVG for README).

### Step 5 — Pre-flight checklist

Always emit a short pre-flight in `DEMO.md` (read `references/staging.md` for the full list): notifications off, terminal font size up, aliases loaded, network plan + offline fallback, understudy recording rendered and tested, reset run once to confirm `s0`.

### Step 6 — Quality gate

The 8 boxes below are this skill's post-verification gate; the 3-phase definition-of-done structure (pre → during → post) is canonical in `../shared/done-gate.md`. Before delivering, verify:

- [ ] **Same show every night** — seed + clock pinned; two consecutive dry-runs produce identical output
- [ ] **Reset is idempotent** — running it twice lands on the same `s0`
- [ ] **Showstopper first** — the payoff appears before the setup
- [ ] **Golden path only** — no beat leaves the happy path
- [ ] **No scene > 76 s** — longest uninterrupted beat is under budget
- [ ] **Understudy ready** — a backup recording exists and was tested
- [ ] **Show, don't tell** — the demo shows the running thing; slides (if any) only support
- [ ] **Runner-native** — automation uses the project's tooling, no stray scripts
- [ ] Every beat has an expected output and a recovery line

## Anti-Patterns

Read `references/anti-patterns.md` for the 12 named anti-patterns (Demo Gods, Feature Tour, Cold Open, The Monologue, Yak Shaving, Mystery Data, No Exit, Slideware, Cursor Ballet, Login Fumble, Director's Cut, Silent Movie) — detection + fix for each.

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|---|---|---|
| Wants slides around the demo | `/cli-forge-prez` | The Live-Coding Sandwich: slides → demo → slides |
| Wants the cast/gif embedded in the README | `/cli-forge-readme` | README forge places the asset and writes around it |
| Needs an architecture diagram for the intro | `/cli-forge-schema` | Mermaid for the "here's the system" opener |
| Demo overlaps a smoke/acceptance ladder | `/cli-forge-resilience` | Golden-path demo ≈ top rung of the smoke ladder |
| Ops/infra demo (OpenBao, Vault, Traefik, k8s…) | `/cli-forge-infra` | Pull the real config path and dependency tree first |
| Ready to commit the kit | `/cli-git-conventional` | Conventional commit for `docs/demos/<name>/` |

**Rule:** Recommend, don't auto-execute.

## Rules for the Generator

1. **The demo shows; it never tells.** If it could be a slide, it's not a demo beat.
2. **Reproducible beats impressive.** A demo that works every time beats a flashy one that works sometimes.
3. **Use the project's runner.** Detect make/just/task/npm/ansible/flux/chainsaw before writing any automation. A stray `.sh` is a smell.
4. **Pin the seed and the clock.** Non-deterministic data is the most common silent demo killer.
5. **Always ship an understudy.** Every kit includes a backup recording and an offline plan.
6. **Recommend the support, let the user force it.** State the pick and the reason; honour `--support`.
7. **Gotchas** — read `../gotchas.md` before producing output to avoid known mistakes.

## Output

Write the kit to `docs/demos/<name>/`:

```
docs/demos/<name>/
├── DEMO.md            # the staged script (lines + marks + timing + recovery)
├── PREFLIGHT.md       # the pre-flight checklist  (or a section inside DEMO.md)
├── demo.tape          # VHS tape           (if support = gif/video)
├── walkthrough.md     # self-guided steps  (if support = interactive)
└── (runner targets)   # added to Makefile / justfile / Taskfile / package.json / ansible
```

Standard paths, zero AI markers, output in the project's language.

## Upstream inputs — what to pull *into* a demo

Before forging, check whether these skills have already produced material the demo should consume. **Read, don't re-derive.**

| Source skill | What to pull in | Where it lands in the kit |
|---|---|---|
| `cli-forge-resilience` | The **golden path** (top rung of the T0-T4 smoke ladder) and the **runbook** troubleshooting entries | the demo path = the safe deterministic path; runbook entries → per-beat **recovery lines** |
| `cli-audit-wizard` | The **idempotent setup** flow and the **credential-discovery cascade** (env → scan → OAuth → device → key) | the **interactive/pédagogique** walkthrough reuses the setup; auth handled backstage → anti *Login-Fumble* |
| `cli-audit-test` | The **nominal/golden scenario** and its assertions | each beat's **expected output**; the VHS `.tape` is handed *back* as an integration test |
| `cli-audit-drift` | `CONTRACTS.md` invariants for the headline capability | beats demo contracted behaviour; a demo that no longer matches the contract is a **stale demo** (drift surfaces it) |
| `cli-forge-infra` | The **simplest real config path** + dependency tree + **NFD** (network-first) | minimal backstage setup; the offline plan → anti *No-Exit* |
| `cli-audit-shell` | Shell-quality check **only if** the demo falls back to a `.sh` (last resort) | vets the fallback; its tooling-ladder informs runner detection |

## Integration with other cli-* skills (downstream)

| Skill | Relationship |
|---|---|
| `cli-forge-prez` | Slides wrap the demo (sandwich); this skill is the live act, prez is the framing |
| `cli-forge-readme` | The rendered cast/gif becomes a README hero asset; the README quickstart is often a mini-demo |
| `cli-forge-schema` | Mermaid diagram for the demo's "here's the system" opener; can render the beat flow as a sequence diagram |
| `cli-forge-resilience` | The golden-path demo is the visible twin of the smoke-test ladder (bidirectional) |
| `cli-forge-infra` | Ops demos (OpenBao &co) reuse the real config path and dependency tree |
| `cli-git-conventional` | Commits the demo kit under Conventional Commits |
