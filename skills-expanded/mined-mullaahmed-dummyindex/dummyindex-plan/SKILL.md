---
name: dummyindex-plan
description: "Grounded planning for a new feature in a repo with a `.context/` index. Turns a natural-language request into `.context/proposals/{slug}/proposal.json`, `spec.md` with intent and contracts, an ordered `plan.md` naming files and reused symbols, and a wave-grouped `checklist.md` for parallel execution. Runs one lightweight parallel critique round for reuse, risk, and testability, then revises once. Every host prepares the same project capabilities and passes selected policy mandates to native subagents; Claude can add optional discovery adapters and approved plugins. Uses deterministic query retrieval and project conventions instead of guessing. Use for `/dummyindex-plan`, `$dummyindex-plan`, plan a feature, draft a spec and plan, scaffold a proposal, or pressure-test an implementation plan."
---

# /dummyindex-plan / $dummyindex-plan — Grounded planning

> **Installed from dummyindex `__VERSION__`.** Run `dummyindex --version` to confirm the CLI matches. If they diverge, diagnose with `dummyindex context check --versions` (it reports which layer is stale), then run `/dummyindex-update` on Claude or `$dummyindex-update` on Codex to bring the CLI, skills, and this repo's wiring back into sync — the update skill is non-destructive on a curated `.context/`. Don't reach for a blunt `dummyindex install` to "fix" a version skew.

You turn a natural-language feature request into a **consistency-checked proposal** under `.context/proposals/<slug>/`. The deterministic CLI scaffolds the artifact and grounds it against the existing index; **you** draft the prose, then a **lightweight critique panel** (a few specialist agents, one parallel round) pressure-tests your draft so you revise before locking the checklist. Python is the toolbox; the panel is the second pair of eyes.

Use the active host's native skill and delegation mechanism. The portable
host path and Claude follow the same preparation and learning workflow;
Claude-native marketplace installation remains an optional adapter operation.

## What you produce

A `.context/proposals/<slug>/` folder with four files:

| File | Owner | Contents |
|---|---|---|
| `proposal.json` | CLI | Structured head: `slug`, `title`, `status`, `related_features`, `conventions`, `reused_symbols`. |
| `spec.md` | You | Intent, contracts, and an `## Acceptance` checklist of `- [ ]` items. The CLI seeds a `## Consistency` block. |
| `plan.md` | You | Ordered tasks, each naming the file path(s) it touches, citing reused symbols, and when a plugin/skill runs it, tagged `— via <tool>` (step 6). |
| `checklist.md` | You | `- [ ]` items derived from the plan tasks **plus** the spec's Acceptance items, grouped into `## Wave N` parallel groups (mutually independent items per wave; waves ordered by dependency); each item carries the same `— via <tool>` tag its plan task had. |

## The flow

1. **Resolve scope + slug.** Take the feature request as the `--title`. Derive a short `--slug` (lowercase, digits, `-`/`_` only — no spaces, no `/`). Confirm the repo has a `.context/` (run `dummyindex ingest <path>` first if not).

2. **Scaffold + ground (the CLI does this in one call):**

   ```bash
   dummyindex context propose --slug <slug> --title "<request>" [--root <repo>] [--force]
   ```

   This creates the four template files, runs the deterministic consistency scan (reusing `query` — **no LLM**), and writes the hits into `proposal.json` (`related_features` + `conventions`) and a `## Consistency` block in `spec.md`.

3. **Read the consistency hits first.** Open `proposal.json` and the `## Consistency` block in `spec.md`. For each related feature, read `.context/features/<id>/spec.md` to learn what already exists — so the new plan **reuses** rather than reinvents. Skim the listed `conventions/*.md`.

4. **Flesh out `spec.md`** — intent (problem + who), contracts (inputs/outputs/invariants/seams), and a real `## Acceptance` section: concrete, testable `- [ ]` criteria. Keep the CLI-seeded `## Consistency` block. **Read each CLI-scaffolded file (`spec.md`/`plan.md`/`checklist.md`) before editing it** — never replace unread content blindly, and preserve the structure the scaffold already seeded (especially `## Consistency`).

5. **Flesh out `plan.md`** — ordered tasks, each naming the exact file path(s) it touches. Where a task can reuse an existing symbol, cite it by name from `.context/map/symbols.json` (and the feature it lives in). Prefer reuse over net-new code.

6. **Map tasks to the shared capabilities and available native tools.** Before the plan
   hardens, decide how each task gets executed. There are **two tag
   classes**, and they must never be mixed:

   - **Binding `— via <tool>`** is reserved for a tool the *main session*
     must run: a plugin slash-command (`— via <plugin>:<command>`), a skill
     (`— via /<skill>` / `$<skill>`), or an MCP-bound tool — something
     actually installed and callable on the active host.
   - **Agent references** name generated agents and dispatch as subagents:
     either leave the task untagged (build's mapper auto-selects from the
     equipment pool) or tag it explicitly `— via agent:<name>`. Never write
     a bare generated-agent name after a plain `— via`; native subagent
     routing does not need a binding tag.

   Read `.context/equipment.json` and relevant usage docs. Prepare any missing
   generated capabilities with `dummyindex context equip apply --for-proposal
   <slug>`; Claude Code may add `--platform claude` for native references/hooks.
   Resolve the selected entry's `path` and read the capability body, including
   a preserved legacy path. A manifest entry is guidance, not proof that the
   current host can call its `subagent_type` or plugin.

   For an external capability, use the active host's supported discovery and
   installation mechanism. Claude's `equip discover` / `install` manage its
   marketplace integration; do not run that mutation on another host. Show
   source, trust and blast radius before installing an approved plugin. Record
   unavailable native capabilities as gaps without blocking generic delegation.

   Pass each selected capability mandate and the full instructions of policies
   actually selected in this session to its delegate. Ponytail applies by
   default when exposed. When its Claude plugin hooks are active in this
   session, its `SubagentStart` hook already injects it into each subagent; do
   not paste it again. Otherwise pass its loaded mandate unless the user turned
   it off this session. Never silently install it.

7. **Critique panel — ONE parallel round, then revise once (this is the multi-agent step).** Dispatch a small panel to pressure-test the draft before it hardens. This is deliberately **light** — one round, no rebuttals, no debate, the panel only files findings; **you** are the sole reviser.

   Use the active host's native delegation mechanism and paste the full mandate
   into every prompt. On Claude, use the preferred named `subagent_type` when it
   is available and otherwise `general-purpose`. On the portable host path
   (e.g. Codex), these are read-only reviews, so use three parallel built-in `explorer` subagents; if `explorer` is unavailable, use `default`. Do not inspect or create `.claude/agents/` to make a critic available on that host.

   Hand each critic `.context/proposals/<slug>/spec.md` and `plan.md`; tell it to
   ground in `.context/HOW_TO_USE.md`, `.context/PROJECT.md`, the related feature
   specs, and `.context/conventions/`.

   | Critic | Claude preferred type | Mandate (inline this into the prompt) |
   |---|---|---|
   | **Reuse & architecture** | `Software Architect` → `general-purpose` | Read the draft spec.md + plan.md and the `.context/` grounding. Flag, with the exact spec/plan location: (a) net-new code that duplicates an existing symbol/feature the plan should reuse — cite it from `.context/map/symbols.json`; (b) a wrong seam/layer or scope creep beyond the stated intent; (c) a task that contradicts a recorded decision or a `conventions/*.md` rule. Findings only — do **not** rewrite the plan. |
   | **Risk & edge-cases** | `Code Reviewer` → `general-purpose` | Read the draft + grounding. Flag: unhandled failure modes, missing edge cases, error-handling/validation gaps, security / data-exposure / migration risks, ordering hazards between tasks, and anything the plan assumes but never establishes. Each finding: the location + the concrete risk + the minimal mitigating task. Findings only. |
   | **Testability & acceptance** | `Test Results Analyzer` → `general-purpose` | Read the draft spec.md `## Acceptance` + plan.md. Flag: acceptance criteria that aren't concrete/observable/testable, plan tasks with no way to verify them, coverage gaps, and any `— via <tool>` tag that contradicts the named plugin's _When NOT to use_ (or a task left untagged despite an obvious installed-plugin fit). For each, propose the testable rewording or the missing verification. Findings only. |

   Each critic returns concise findings tagged **BLOCK / HIGH / MEDIUM / LOW** with the location + minimal fix. **Then you revise once:** read all three sets, fold the BLOCK/HIGH findings (and any MEDIUM you agree with) into `spec.md` + `plan.md`, and note in one line what you changed and what you deliberately left. Don't re-dispatch; don't invent changes when the panel found nothing material. (Skip the panel only for a trivial, single-file change whose plan is self-evidently correct — say so if you do.)

8. **Derive `checklist.md` as ordered waves** — *after* the revision — turn the revised plan tasks plus the spec's Acceptance items into `- [ ]` items grouped under `## Wave N — <label>` headings. This is the execution surface a later step works through, and the wave structure is what lets `/dummyindex-build` dispatch items **in parallel**:

   - **Items inside one wave must be mutually independent**: they touch **disjoint files** and neither needs the other's output. The build step dispatches a whole wave concurrently — a hidden dependency inside a wave is a race.
   - **Waves run strictly in order** — put a task in the earliest wave whose prerequisites are all in earlier waves. Typical shape: wave 1 = shared scaffolding (models, schema, fixtures), middle waves = independent features/modules fanned out wide, last wave = integration + the spec's Acceptance items.
   - **When unsure whether two tasks are independent, put them in separate waves.** Serial is always correct; parallel is an optimization. A checklist of singleton waves (or no wave headings at all — plain flat list) is valid and simply builds serially.
   - Other headings are free; only `Wave`/`Group` headings open a parallel group.
   - **Open decisions never become plain checklist items.** An unresolved design/approval question (settle the RLS / tenant-isolation model, resolve a `DECISIONS.md` open question, pick between two approaches) is **not** implementable code — if it ships as an ordinary `- [ ]` item, build will try to dispatch the decision to a subagent. Resolve it *before* deriving the checklist: put it in an `## Open questions` block in `spec.md` and ask the user. If a decision is genuinely deferred to build time, mark its item with a leading `**GATE**` so build treats it as a main-session item and escalates to the user instead of dispatching it. Likewise, an item that can only run with tools the **main session** has (a hosted/MCP server a subagent can't reach) should carry a binding `— via <tool>` tag — the build CLI classifies `**GATE**` items and *binding* via-tagged items (plugin commands/skills/MCP-bound tools) as `dispatch: main-session`, so the conductor handles them itself; the other tag class (`— via agent:<name>`) dispatches as a subagent unit.

   Example:
   ```markdown
   # Checklist — <slug>

   ## Wave 1 — schema + scaffolding
   - [ ] Add widgets table migration (db/migrations/...)
   - [ ] Define Widget dataclass (app/models/widget.py)

   ## Wave 2 — independent surfaces
   - [ ] Widget CRUD endpoints (app/api/widgets.py)
   - [ ] Widget list UI component (ui/components/WidgetList.tsx) — via /frontend-design
   - [ ] Build the UI bundle with the project's existing build command

   ## Wave 3 — integration + acceptance
   - [ ] Wire UI to the endpoints (ui/api/client.ts)
   - [ ] Review the generated diff — via /code-review
   - [ ] Acceptance: the route test verifies a created widget appears in the list response
   ```

   **The close-out is procedure, not proposal work.** `/dummyindex-build`
   appends a mandatory closing phase after the last accepted wave — the
   checkpointed `context maintain` recouncil loop ending in a
   `chore(context): re-anchor` commit — unless the build invocation passes
   `--no-recouncil` or `.context/config.json` sets
   `"build": {"auto_recouncil": false}` (config schema v5, default true). Do
   not hand-plan that phase as checklist items; plan the last wave to land the
   code + its tests so the closing loop reconciles finished work.

9. **Prepare the shared project toolkit for this proposal:**

   ```bash
   dummyindex context equip apply --for-proposal <slug> [--root <repo>]
   ```

   On Claude Code, add `--platform claude` when native discovery references and
   hooks are wanted. Missing native equipment never blocks build execution.

## Checklist + spec-led discipline (embed this in how you work)

- **Read `spec.md` first.** It is the source of truth for *what* and *why*. The plan serves the spec; the checklist serves both.
- **Work `checklist.md` wave-by-wave, top-to-bottom.** Items within a wave may run in parallel; a wave starts only when every earlier wave is fully ticked.
- **Tick only after verifying.** Flip `- [ ]` → `- [x]` for an item *only* once you've confirmed it (its test passes / the behavior is observed). Never tick on intent.
- **No live-testing items.** Checklist items never call for live tests, production runs, smoke tests, or manual verification against real services; `waves` exits non-zero on them. Use `<!-- live-ok: reason -->` only for a false positive. Durable docs never cite `.context/proposals/` or `.context/audits/` paths.
- **Stop and report if blocked.** If an item can't be completed (missing dependency, contradictory requirement, ambiguous scope), stop, leave it unticked, and report the blocker with a concrete next step — don't paper over it or skip ahead.

## Done

Report the proposal path, related features, reused symbols, task waves, tooling
and capability gaps, and critique outcome. Confirm shared capabilities were
prepared or explain a preserved/skipped target.
