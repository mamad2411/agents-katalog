---
name: think
description: "Brainstorm and converge on solutions — diverge on possibilities, converge to a decision-complete plan, generate an initial PRD. Use when requirements are unclear, multiple implementation paths exist, or the user describes a new feature, architecture decision, or complex task. Trigger words: brainstorm, 构思, plan, how should I, design approach, feasibility, 技术方案."
---

# Think: Brainstorm and Solution Convergence

🥷 Think before you code.

Transform rough ideas into decision-complete plans. Ask one question at a time, each with your recommended answer. Do not write code, generate scaffolds, or write pseudocode until the user explicitly starts an implementation workflow.

If a question can be answered by exploring the codebase or a quick research pass, do that instead of asking.

## Outcome Contract

- **Outcome**: Decision-complete plan. Optionally persisted as a PRD with clear requirements, acceptance criteria, technical approach, and implementation plan
- **Done when**: User approves plan and (optionally) PRD is created for `/grill`
- **Evidence**: Updated `docs/prd/PRD-NNNN-<title>.md` (if user opts to create PRD), or approved design summary
- **Output**: Approved design summary with next step to `/grill`

## Core Principles

1. **Task-first** — capture the idea immediately
2. **Action-before-asking** — derive from codebase/docs before asking. Apply the [Skill Entry Protocol](../rules/entry-protocol.md)
3. **One question at a time** — exactly one **decision** per message, each question carrying a recommended answer, with no piggyback riders ("顺便确认…", "please also mention…") — a second needed decision becomes the *next* single question, after the derivability check. Derive the next question from the user's last answer (an answer resolves, opens, or closes branches — never work a pre-computed list; anti-patterns #3, #4). Update the PRD after each answer
4. **Prefer concrete options** — present 2-3 viable approaches with trade-offs; never silently assume a single path (anti-pattern #28)
5. **Research-first** — query INDEX before proposing; study authoritative sources
6. **Diverge → Converge** — expand on edges, then converge to MVP

## Process Summary

**Step 0 — Quick assessment.** If the request is Trivial (typo, single-line fix, one obvious approach), tell the user `/think` is unnecessary, recommend direct implementation or `/tdd`, and stop. No PRD created.

**Step 1 — Auto-collect context.** Explore the codebase (affected modules, existing patterns, constraints) and docs (prior PRDs, README, ADRs) before asking anything. Write findings into the PRD's `What I already know` and `Technical Notes`.

**Step 2 — Offer to create a PRD.** Ask whether to persist the plan as `docs/prd/PRD-NNNN-<title>.md`. By now you have enough context to explain what the PRD would contain — the user decides with findings in hand. Don't create one automatically. If declined, work conversationally and produce a summary at the end. When creating: run the **PRD Conflict Check** (see REFERENCE.md §PRD Conflict Check) — compare the topic against existing PRDs by title slug and Goal; if a candidate collides, ask whether to resume it (reuse its NNNN) or create a new one with a distinct title. Only then assign next NNNN (max + 1, starting from 0000).

**Step 3 — Classify complexity.** Simple / Moderate / Complex (see REFERENCE.md). Depth of brainstorming scales with complexity.

**Step 4 — Gate your questions.** Only ask **Blocking** (can't continue without input) or **Preference** (multiple valid choices) questions. Derivable questions → inspect the code/research instead. Meta questions ("should I search?") → never ask, just act. If the user packs multiple requests, enumerate and address each one (anti-pattern #20).

**Step 5 — Research-first for technical choices.** When choosing an approach/library/framework:

1. **Query the research INDEX first.** Read `docs/research/INDEX.md` for matching stack + topic + major records:
   - **Hit (verified)** → read TL;DR only; reuse verdict. Don't read full record by default.
   - **Hit (stale)** → read full record's `## Boundary Conditions` to decide if old conclusion applies. Suggest `/research <stack> <topic>-<current-major>` if needed.
   - **Hit but decision depends on implementation detail** → read full record's Findings/Code Snippet even if verified.
   - **Miss** → suggest `/research` to persist, or proceed with inline research and create a record afterward if conclusion is reusable.
2. **Only on a miss**, research 2-4 comparable patterns against **authoritative sources** (official docs/source/spec), map to codebase constraints, present 2-3 options with trade-offs, ask one preference question.
3. Cite reused research records in PRD's `## Research References`.

**Step 6 — Expansion scan (diverge).** Proactively raise 1-2 points each on future evolution, related scenarios, and failure/edge cases before converging. **Scale to complexity** (Step 3): Simple tasks skip this step; Moderate does failure/edge only; Complex does all three. Let the user pick what enters the MVP vs `Out of Scope`.

**Step 7 — Q&A loop (converge).** Exactly one question per message, with a recommended answer (anti-patterns #3, #4; adaptive-selection mechanics in [REFERENCE.md §Step 7](REFERENCE.md)). After each answer, immediately update the PRD: move resolved items from `Open Questions` to `Requirements`, sharpen `Acceptance Criteria`, clarify `Out of Scope`. Continue until the MVP's decision tree is exhausted — every blocking/preference node resolved — not until a question list runs out.

**Step 8 — Propose approaches + record decision.** When requirements are clear, present 2-3 approaches (if not already done via research), ask preference, and record the result in the PRD's `Decision (ADR-lite)` section. If the options can't be separated by reasoning or trade-offs alone — and running code could separate them — suggest `/have-a-try`: a minimal demo adjudicates (selects or eliminates), and the verdict fills the decision plus the PRD's `Prototyped by` field.

**Step 9 — Submit plan for approval.** Present the complete requirements (Goal, Requirements, Acceptance Criteria, Definition of Done, Out of Scope, Technical Approach, small-PR implementation plan). The approval submission asks exactly one thing — approval. Any setup decision still open (tracker or no tracker, PRD language, etc.) must have been settled as its own single question **before** this submission, so the user approves a complete plan with no riders attached. After user approval, proceed to Step 10 (Create Parent Issue & Finalize PRD) — do not wrap up yet.

**Step 10 — Create Parent Issue & Finalize PRD.** After plan approval:
1. **Create the parent Issue** in the issue tracker (required — `/grill` and `/story` downstream rely on the PRD's `## Issue` field)
2. **Record new domain terms** found during brainstorming for `/grill` to refine
3. **Finalize the PRD** — set Status to `Draft`, fill `Created by`, set `Last updated`, ensure all sections are populated
4. Output the approved design summary with next step to `/grill`

See [REFERENCE.md](REFERENCE.md) for complexity classification detail, question-gate rules, and worked message formats. The PRD template and field rules live in [PRD-FORMAT.md](PRD-FORMAT.md) — that file is the single source.

## Gotchas

| What happened | Rule |
|---|---|
| Created PRD without asking user first | Step 2: ask before creating PRD |
| Asked user about code/context that could be derived | Step 1: auto-collect context first |
| Had user choose approach before presenting options | Step 5: research-first for technical choices |
| Re-searched a topic a prior task already captured | Step 5: query `docs/research/INDEX.md` first; reuse the TL;DR on a hit |
| Cited a blog/tutorial as the basis for a technical choice | Step 5: research against authoritative sources (official docs/source/spec) only |
| Asked meta questions like "should I search?" | Step 4: never ask, take action |
| Drifted without updating PRD | Update PRD after every answer |
| Attached a rider sub-ask to a question ("顺便确认/请一并说明") | One decision per message — a second decision becomes the next single question (Step 7 rules) |
| Stayed on initial request without considering edges | Step 6: expansion scan before converging |
| Domain terms introduced but not recorded for grill | Step 10: record new terms in PRD `## Domain Terms` section |
| Same topic got two PRDs (e.g. PRD-0001 + PRD-0002) | Step 2: run PRD Conflict Check (REFERENCE.md) before assigning NNNN |
| Parent Issue not created after plan approval | Step 10: parent issue creation is required before finalizing — unless the no-PRD or no-tracker waiver in REFERENCE 10a applies — `/grill` and `/story` rely on it |

## Output

When plan is approved and parent Issue is created, output:

```
Plan approved. Next: Run /grill to challenge and refine this approach.

**Approved design summary:**
- **Building**: What this is (1 paragraph)
- **Not building**: Explicit exclusion list
- **Approach**: Chosen option + rationale
- **Key decisions**: 3-5 items with rationale
- **Unknowns**: Only explicitly deferred items with reason and owner
- **Parent Issue**: #<num> created | (no PRD, skipped)
```

Stop after output. Implementation only starts on request.
