---
name: ask-bundle
description: Use when deciding which skill or flow fits your situation — the meta-router entry point for this bundle (direct specialist skills, multi-skill flows, local AFK issues), or when the request is vague and needs the quick-start menu. Routes then defers to the chosen specialist — does not execute the work itself.
triggers: [user, model]
---

# Ask Bundle — the bundle router

One entry point: classify the objective, route to matching skills, keep
control through verified completion. You don't remember every skill, so ask.

Detail docs: `modes/orchestration-detail.md` (full orchestration procedure, forbidden
actions, priority hierarchy), `modes/flows-detail.md` (verbose flow map),
`PHASE-BOUNDARIES.md` (context-handoff decision tree).

## TL;DR

1. Self-check: scope exactly, telegraphic, skills first, verify, no opinion.
2. Classify objective; route directly to matching skill(s).
3. Unclear objective ("ask-bundle"/"start") → quick-start menu via `ask_user_question`.
4. 3+ steps → `todo_write`; each step gets a VF (`gate:`/`expect:`/`evidence:`).
5. `qa-ci` re-runs every non-trivial gate on a clean checkout.
6. Run project verification (e.g. `python audit.py`, `pytest`) before done.

## Situation router

| Situation | Entry | Next |
|---|---|---|
| Build/change something | `grilling` (intent) or `execution` cadence if trivial | → `planning` spec→tickets → `execution`+`testing` → `security` (API/DB/secrets/infra) → `code-review` → `gates` → `finishing-a-development-branch` |
| Run AFK/unattended | `execution` execution (needs ready-for-agent issues) | see AFK creation below |
| Hard/intermittent bug | `debugging` | → `testing` regression → `architecture` if no seam |
| CI failing | `debugging` ci mode | |
| Triage incoming issues | `intake` | → `execution` |
| Large foggy multi-session effort | `planning` wayfinder | → spec → tickets → implement |
| Prototype to settle a question | `prototype` (via `handoff`) | back to `grilling`/`planning` |
| Research/deep exploration | `research` | feeds `grilling`/spec |
| Fact-check article/draft | `fact-check` | → `humanizer` on accepted fixes |
| De-AI-ify prose | `humanizer` | |
| Need input from another person | `planning` questionnaire | |
| Git merge/rebase conflict | `git-workflows` | |
| Improve architecture/deep modules | `architecture` | → `grilling` if it generates an idea |
| Evolve skill/rule/hook/MCP | `self-improvement` | → `writing-skills` (one skill), `devin-config` (new capability) |
| Release/deploy/rollback | `deploy` | → `gh`, smoke tests |
| Security assessment | `security` | → `execution` for remediations |
| Data query/analysis/charts | `data-analyst` | |
| UI/UX polish | `impeccable` | → `a11y-audit`/`e2e-testing` |
| Observability infra | `observability-quality` | |
| API or DB design | `api-spec` or `database` | → `execution` |
| Performance/cost | `performance` or `context-hygiene` | |
| Human-only procedure | `wizard` | |
| Guided learning | `teach` | |
| User owns design, agent teaches + writes | `learn-mode` | off-ramp to `execution` once design approved |
| Write PR body/description | `pr` | → `gh` to create/update |
| Session retrospective / improve agent env | `retro` | findings → `continuous-improvement` or issues |
| Husky/lint-staged pre-commit setup | `setup-pre-commit` | |
| Set up repo for Devin | `project-bootstrap` | |
| Not sure / no match | `skill-discovery` | evaluate/install |

## The main flow: idea → ship

1. **`grilling` (with-docs)** — sharpen the idea by interview; stateful in
   `.devin/CONTEXT.md` + `adr/`. Stateless mode when no working directory.
2. **Runnable question?** → detour: `handoff` out → `prototype` → `handoff`
   back.
3. **Multi-session build?**
   - Yes → `planning` spec → tickets (tracer bullets + blocking edges;
     `.devin/scratch/<feature>/issues/` on local tracker) → `execution` per
     ticket, clearing context between. Single focused session alternative:
     `planning` plan-doc → `execution`.
   - No → `execution` implement right here.
4. Either way: `testing` TDD inside → `code-review` (Standards+Spec) →
   `security` when touching API/DB/secrets/endpoints/infra → `gates` →
   `finishing-a-development-branch`.

**Context hygiene:** keep 1–3 in one window until tickets are cut; each
implementation starts fresh. Approaching the smart zone (~150k) → compact at
the nearest phase boundary (`PHASE-BOUNDARIES.md`).

## On-ramps

- **Bugs/requests piling up** → `intake` triage (issues you didn't create).
- **Something's broken** → `debugging` (tight feedback loop first).
- **Huge foggy effort** → `planning` wayfinder (decision-ticket map; hands
  off to spec when clear — never loop straight into implement).
- **Codebase health** → `architecture` (deepening opportunities generate ideas).

## Vocabulary underneath

- `knowledge-modeling` — domain language (`.devin/CONTEXT.md`, ADRs) +
  ontology validation.
- `architecture` — deep-module vocabulary (module/interface/depth/seam).
- `ai-coding-dictionary` — canonical AI-coding jargon.

## Quick-start menu (vague request)

`ask_user_question` with 2–4 options:
- Build/change something → `grilling` or `execution` cadence
- Improve a skill/rule/hook/MCP → `self-improvement`
- Debug/research → `debugging` / `research`
- Set up repo / run AFK → `project-bootstrap` / `execution` afk

## Quick AFK issue creation

1. Confirm feature slug + objective.
2. No spec → `grilling`/`planning` spec → `.devin/scratch/<slug>/spec.md`.
3. `planning` tickets → one file per ticket `issues/<NN>-<slug>.md`,
   `Status: ready-for-agent`, `Blocked by:`, acceptance checkboxes.
4. Verify files + DAG (`glob`, `read`, parse `Status:`/`Blocked by:`).
5. `execution` execution only on explicit user authorization.

## Hard constraints (never violated)

1. Safety + pinned `AGENTS.md` rules (2, 5, 7, 12-19, 21).
2. Verify with tools before asserting.
3. Execute exactly what was asked, without opinion.

Then: usefulness → ease → quality of experience → technical coherence →
performance.

Forbidden: deduce without tools; start non-trivial work without skill
discovery; mark completed without independent `qa-ci` PASS; override qa-ci
FAIL; push/commit with failing checks; AI signatures; display secrets;
destructive actions without confirmation; `subagent_explore`/paid models on
a free parent; `execution` without ready-for-agent issues; read/edit
`tests/held-out/` from implementer context; reuse implementer shell for
qa-ci without reinstalling pinned deps.

## Bundle context

- Validated CLI: `{{VALIDATED_CLI_VERSION}}` (`data/bundle-identity.json`).
- Models: `data/bundle-models.json` — parent `BUNDLE_DEFAULT_MODEL`;
  subagents `BUNDLE_MAX_MODEL`/`BUNDLE_MEDIUM_MODEL`, all free. No paid
  aliases on a free parent.
- Issue tracker: `.devin/scratch/<feature>/` + `.devin/agents/issue-tracker.md`,
  `triage-labels.md`.
- Verification baseline: `python audit.py`, `python -m pytest`.
- Laya is NOT wired into agent routing — zero-shot accuracy was too low
  to justify it (see plan `2026-09-22-laya-frentes-de-acao.md`).
  `extensions/laya-tools` + `implement-laya` remain for per-project use.
