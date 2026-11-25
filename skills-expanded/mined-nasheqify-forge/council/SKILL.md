---
name: council
description: >
  Structured architectural / strategic decision-making — context-isolated
  members + a chief consolidation, you decide (light / standard / full /
  interactive modes). Use when a decision has more than one viable path AND
  is hard to reverse AND you're uncertain — spawn it yourself when stuck on
  an architecture/strategy call, before escalating to the user. NOT for a
  single-path or easily-reversible choice, or a cross-scope contradiction
  you can settle in the current scope.
status: active
verification_tier: 1
evidence_layout: per_finding
relevant_for: ["solution-expert"]
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
modes: [light, standard, full, interactive]
uses: [_protocols/plan-review, _protocols/context-isolation, _protocols/dispatch-template, _protocols/consolidation-preservation, _protocols/content-preservation, _protocols/piebald-budget, _protocols/analysis-mode-gate, _protocols/evidence-pointer-schema, _protocols/discourse]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.
Without Buddy (plugin): if this session holds no Buddy boot entry, run `python3 <root>/scripts/forge_setup.py offer-check` once, as its own call (`<root>`: two levels above this skill's folder); if it prints a line, pass that offer to the user in one sentence, then continue with this skill.


# Skill: council

Generic reasoning method. Required inputs: problem, constraints, evidence/context,
method options; optional authorized output destination. No user repo, Git repository,
development workflow, task or automatic writeback is required. Without a destination,
use a private temporary execution root and the dispatch protocol's complete-return
transport. Supplied intent/values anchor standalone work; a repository intent is
required only when that repository is the selected caller. Report rationale,
alternatives, uncertainty and usable evidence inline. Proposals are not accepted
user decisions. Optional domain adapters (§12–§13 in `development.md`) apply only to selected development.

Buddy checklist (§4 in `run.md`) + operational detail.

## 0. Plan + review (required without a frame)

Without a frame: derive plan scope from project intent (or supplied intent for standalone work) and the local
objective (owner: framework/invariants.md §Intent-driven). Add tool and alternatives, then self-review and dispatch
`plan-adversary` on non-trivial plans. With a frame: reference it. Templates + triggers: `_protocols/plan-review.md`.

## 1. Mode determination

### 1.0 Proportionality gate (MANDATORY — runs before §1.1)

Default = escalate. Answer 4:

1. >1 genuinely viable path AND hard to reverse?
2. >1 layer / component affected by the decision?
3. Substantial impact on security / sovereignty / simplicity / experience / compatibility / scale?
4. Buddy genuinely uncertain (not "looking for confirmation")?

**Answer pattern:**
- **≥3 yes** → council (proceed to §1.1).
- **≤2 yes** → no council. Document skip: *"Council not needed: <rationale>"*. Decide directly.

**Override floor (forces standard or full regardless of count):** security / sovereignty hard constraint AND multi-component · new state-vocabulary or new public-API contract · new normative cross-spec rule · foundational pattern replacement.

**Anti-pattern (cross-scope vs current-scope):** if the question presents as "spec corpus has multiple representations of X" but current-scope path is internally consistent (producer + consumer + adjacent uses all aligned) and contradictions live in different scopes → **NO council**. Preserve current path; file normalisation as follow-up task. Council on cross-scope when current is decidable wastes a cycle + introduces re-framing risk (Council recommendation adopted autonomously becomes a frame user has to unwind).

Walk-through: (1) Is CURRENT-SCOPE path internally consistent? Check producer + consumer + adjacent uses. All same representation → path IS decidable. (2) Contradictions in DIFFERENT scopes (legacy / future / cross-cutting infra)? (3) Way to preserve current path + file normalisation as follow-up? All three yes → NO council.

### 1.1 Mode choice (after gate passes)

Detailed mode-profile table (complete here; `workflows/templates/council.yaml`
is an optional development integration, not a runtime dependency):

| Mode | Members | Adversary | Chief | Frame-check | Coherence-check (Buddy-side) | Discourse | Development ADR |
|------|---------|-----------|-------|-------------|------------------------------|-----------|-----|
| **light** (default) | 3 | — | yes (all modes — Inv 1) | — | required | — | optional |
| **standard** | 3 | yes | yes | yes (`plan-adversary`) | required | — | yes |
| **full** | 4-6 | yes | yes | yes | required | on dissent | yes |
| **interactive** | dialog-perspectives | conceptual | — | — | required | per-round | optional |

Trigger short-form:
- **light** — default on §1.0 pass.
- **standard** — ≥1 of §1.0 override-floor items, OR ≥2 of {hard-to-reverse, multi-component, security/sovereignty}.
- **full** — >2 dimensions OR foundational pattern OR ≥2 hard constraints.
- **interactive** — user explicit ask only (Buddy moderates a dialog — see §10).

**Chief is required for all independent-member council modes (light/standard/full)**. Interactive is explicitly moderated dialogue, not a claim of independent-agent execution. Chief consolidates member
outputs; Buddy owns the decision and verifies pivotal claims per Invariant 1.
Light omits adversary/frame-check/discourse, not the Chief.

**Coherence-check:** after every Chief return, check the recommendation against supplied intent, constraints, source evidence and viable alternatives. Buddy owns the decision. Development callers additionally apply their architectural obligations.

**Member model config**: members, the adversary and the Chief take the Design row of
`framework/models.md`, named in each call, from the host's available,
authorized models; the `model:` keys in a council template's `member_config`
do not set it. Do not invent unavailable models or claim model diversity
from different role names.

Default = light (proportional release valve). **Mode escalation** (light → standard → full) is criterion-driven, not Buddy-uncertain — picking standard/full just because Buddy feels uncertain is mode inflation. If §1.0 warrants Council and the alternative is escalating an unresolved decision to the user, use Council first within existing authorization. Escalate only unresolved dissent, consequential user-owned decisions or scope changes. Selected development callers additionally follow their operational contract.

## 2–4, 9–10. Running the council (frame check, briefing, dispatch, perspectives, interactive)

Once the §1 mode is picked, before drafting the briefing and dispatching members (light / standard / full), and
before opening an interactive council: read and follow `skills/council/run.md` (§2 pre-council frame check, §3
briefing format with the required `intent_chain` anchoring, §4 Buddy dispatch checklist, §9 perspective profiles,
§10 interactive council phases 1-2-3). Section numbers are skill-wide: §0–§1, §5–§8, §11 and §14 here, §2–§4 and
§9–§10 in `run.md`, §12–§13 in `development.md`.

## 5. Anti-patterns

- **NOT** Buddy's proposal in briefing → cold-start per §3; proposal stays in frame-check artifact.
- **NOT** consolidate without council-chief (≥3 members) → Inv 1 hard rule; chief is consolidator-tool.
- **NOT** skip pre-council frame check on standard/full → frame-check IS how you find brief contamination.
- **NOT** adopt a Chief recommendation without checking pivotal claims and fit to supplied constraints. A present file is not evidence its interpretation is correct. Falsified or consequential ungroundable claims require reframing or a stated decision limit. Development-specific C-VERIFY obligations remain with that caller.
- **NOT** `code-adversary` for council adversary → `council-adversary` (architecture-decision-tuned).
- **NOT** light mode on hard-to-reverse → standard or full.

## 6. Contract

**INPUT:** decision-question + intent_chain + context-files. Optional: frame report, ADR catalogue, deploy-state observations.

**OUTPUT:** inline decision/rationale, alternatives, uncertainty and usable evidence; complete execution artifacts at the caller-owned destination (§7). An authorized development caller retains its decision artifact and required ADR pointer. No automatic durable writeback.

**DOES NOT:** implement; write spec; choose autonomously (user decides on user-facing decisions; Buddy decides on framework-internal per soul.md).

**FAIL handling:** chief reports NO-CONVERGENCE → check whether briefing framing is wrong (re-frame + new council on revised question) OR escalate to user. On ≥1 adversary BLOCKER + member disagreement: when the chief's consolidation keeps the BLOCKER, no member output contradicts its premise or evidence (tracking table), and the disagreement is only which option to take on a decision the user makes, the user gets the dissenting positions with the recommendation and no discourse round runs; the decision artifact records that and carries the positions under §11. Otherwise Standard → Full, with its discourse round.

## 7. Output paths

With an authorized durable repository destination, base: `docs/reviews/council/<date>-<topic>-{briefing,frame-check,{perspective},consolidated,decision}.md`. Build-context backward-compat: `docs/tasks/{task_id}-council-*.md` per `workflows/templates/council.yaml`.

Without that destination, all §2/§4/§7 paths are relative to the private temporary
execution root; this is execution transport, not durable knowledge writeback.
Returned inline evidence must remain usable without inaccessible temporary links.
Persist an accepted result only through the caller's selected continuity owner.

## 8. Boundary

Spec review → `spec_board`. Code diff → `code_review_board`. Pre-code plan → `impl_plan_review`. Technical architecture moderator → `solution-expert` (instantiates this skill, 6 fixed perspectives per the user's values). Non-technical → this skill with situational perspectives (see §9 in `run.md`).

## 11. Risk carry-forward schema (council-side)

Mirrors `code_review_board/verdict.md` §Risk carry-forward. Decision artifact YAML `remaining_positions:` per entry: `id`, `severity`, `option`, `argument_summary`, `rationale_for_carry_over`, `proposed_action` (`re_council` / `ADR` / `monitor` / `accept`).

## 12–13. Development caller: ADR triggers and engine handshake

Only for an explicitly selected development caller, before a build-context or solve-refine council starts, when
deciding whether an ADR is required (§4 step 8), and when a ruling splits a capability: read and follow
`skills/council/development.md` (§12 ADR-trigger conditions, §13 optional development caller handshake with split
rulings). Standalone invocation needs neither.

## 14. Skip rationales (template)

Acceptable §1.0 skip phrases (write inline at decision point):
- `"Council not needed: single viable path (X), reversible (Y)."`
- `"Council not needed: cross-scope contradiction, current-scope decidable (producer/consumer/adjacent all aligned on X)."`
- `"Council not needed: HARD constraint already binds choice (sovereignty rules out cloud-only options)."`

Unacceptable: silent skip, "obvious", "no time".
