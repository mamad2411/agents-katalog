---
name: prd-from-code
description: Reverse-engineer an in-depth PRD from an existing codebase or feature - documenting actual behavior, inferring intent, and flagging gaps. Use when the user wants a PRD, spec, or requirements doc for something already built, or needs documentation for legacy/inherited code.
license: MIT
metadata:
  author: andrewr303
  version: "2.0"
---

Reverse-engineer a PRD from existing code. The code is the ground truth for WHAT the system does; the user and history are the source for WHY. Never present inferred intent as verified fact.

**Supporting files** (under `templates/` at the plugin root):
- `templates/prd-template.md` — target structure
- `templates/review-rubric.md` — quality bar

**Input**: A scope — a feature name, module path, service, or the whole product. If ambiguous, ask the user to bound it before analyzing ("PRD for the whole app or just the checkout flow?"). A whole-product PRD for a large codebase should be proposed as several capability-scoped PRDs instead.

## Steps

### 1. Map the territory

Systematically investigate the scoped code (for large scopes, delegate parallel exploration to sub-agents if available):

- **Entry points**: routes/endpoints, CLI commands, UI pages/components, event handlers, scheduled jobs.
- **User-facing behavior**: what can a user actually do? Trace each flow end-to-end: inputs → validation → processing → outputs → side effects.
- **Error handling**: what failure paths exist? What do users see? What is silently swallowed?
- **Data model**: entities, relationships, migrations (migration history reveals evolution), retention.
- **Boundaries**: external APIs consumed/exposed, auth model, permissions/roles, feature flags, config/env vars (each flag/config is a requirement in disguise).
- **Non-functional reality**: caching, rate limits, queues/retries, timeouts, logging/metrics — these encode NFRs someone once cared about.
- **Tests**: test names and assertions are the closest thing to written scenarios — mine them.
- **History** (if git available): `git log --no-pager` on key files; commit messages, PR references, and TODO/FIXME/HACK comments carry intent.

### 2. Classify every finding

Label each behavior with evidence discipline:
- **[verified]** — observed directly in code/tests, with `file:line` citation.
- **[inferred]** — reasonable interpretation of intent (from naming, structure, history). State the basis.
- **[assumed]** — a guess. These MUST land in Open Questions, not requirements.

Also collect:
- **Behavior gaps**: unhandled edge cases, missing validation, dead code, flags always-on/off.
- **Spec-worthy surprises**: behavior that looks accidental rather than intended (e.g., unbounded queries, silent failure swallowing). Flag, don't judge.

### 3. Interview for the WHY (brief)

Code can't tell you goals, metrics, or non-goals. Ask the user 3–5 targeted questions:
- Who uses this and for what job?
- What was the original goal — and is it still the goal?
- What's measured today, if anything?
- Any known pain points or planned changes?
- Is this PRD for onboarding, a rewrite, compliance, or planning changes? (shapes emphasis)

If the user can't answer or isn't available, write those sections as **[inferred]** with your reasoning, and list them under Open Questions.

### 4. Write the PRD

Follow `templates/prd-template.md`, adapted for as-built documentation:

- Mark Document Control status as **"As-Built"** and note the commit hash analyzed.
- **§2 Problem/§3 Goals**: from the interview or clearly `[inferred]`.
- **§6 Requirements**: one FR per verified behavior, SHALL language, WHEN/THEN scenarios derived from code paths and tests. **Cite code** for every FR: `Evidence: src/checkout/cart.ts:142-160`.
- Priorities reflect current reality: P0 = core paths the product breaks without.
- **§6.3 Edge cases**: include both handled cases (verified) and UNHANDLED gaps discovered — mark gaps clearly as `⚠ GAP: not handled in code`.
- **NFRs**: document what the code actually guarantees (observed timeouts, limits, auth), not aspirations.
- **§12 Open Questions**: every [assumed] item, every "is this intentional?" surprise.
- **Appendix**: coverage map (entry points examined vs skipped) so readers know the blast radius of the analysis.

### 5. Verify and deliver

- Self-check against `templates/review-rubric.md` — for as-built PRDs, dimensions 1–3 (problem/goals/metrics) may legitimately score lower if the user provided no context; say so rather than inventing.
- Spot-verify: re-read the code behind 3–5 of your most load-bearing requirements to confirm you didn't misread. Re-derive, don't recall.
- Deliver: file path, summary of what the system does in one paragraph, the top gaps/surprises found, and open questions.
- Also write or refresh `docs/plan/context/platform.md` (`plan-context`) so later REQs stay code-aware.
- Offer: "Want me to turn the ⚠ GAPs into EPICs/REQs (`/ultimate-sdd:project`), or draft a v2 PRD proposing improvements?"

## Guardrails

- **Code is truth for behavior; never document what the code should do as what it does.** Aspirations belong in Open Questions or a clearly-marked "Proposed" section.
- Every functional requirement must cite its evidence. No citation → it's [inferred] or [assumed].
- Don't drown the reader: internal helper details are implementation, not requirements. If it can change without users noticing, it stays out of §6.
- Respect scope: don't wander into unrelated modules; note adjacent areas as out of scope.
- Never include secrets, credentials, or sensitive values discovered in config — reference the config key only.
