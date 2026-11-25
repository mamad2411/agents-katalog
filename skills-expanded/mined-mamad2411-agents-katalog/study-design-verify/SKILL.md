---
name: study-design-verify
description: Evidence-grounded advisory pipeline for "how should this work?" questions about any real system — codebase, database, CRM/ERP, SaaS, API, data pipeline, infra. Three-stage multi-agent method; STUDY the business and the live system with parallel readers returning structured citable findings (read-only, evidence saved to disk), DESIGN with independent designers given deliberately different value systems, VERIFY with an adversarial reviewer that attacks every design against the live schema, code, and usage data before anything is recommended. Use whenever the user asks for advice or a recommendation that must be grounded in how their system actually works — "how should X convert/map/migrate/sync to Y", "study my business and advise", "what's the right way to integrate/restructure/redesign this", "should we copy or link this data", "is this conversion/mapping correct, and if not what should it be", reviewing a planned schema or integration change, or any "give me advice" about a system mechanism. Trigger even when the user never says "advice" but wants a defensible recommendation about an existing system. Do NOT use for quick opinion questions with no system to study, single-file refactors, status updates, or pure greenfield design with no existing system as ground truth (use brainstorming instead).
effort: max
---

# Study → Design → Verify

Turn "how should this work?" into a recommendation that survives scrutiny, by separating three jobs that corrupt each other when one mind does them at once: **gathering facts**, **proposing designs**, and **attacking designs**. Each phase is staffed by agents who only do that one job.

The output is an advisory document: problems ranked by business pain, a phased plan, explicit "do NOT do X because Y" entries, and an evidence trail a skeptic can audit.

## When to invoke

"How should A convert/map/migrate/sync to B?" · "study my business, then advise" · "what's the right design for [change to an existing system]?" · "should we copy, link, or recalculate this data?" · "review this integration plan against reality" · build-vs-extend questions about an existing flow. If the answer should change when the *real system* contradicts the docs, this skill applies.

## Principles (the why)

1. **Conclusions, not raw text.** One context window can't hold the wiki, two codebases, and a live schema. Fan out readers with fresh contexts; keep only their structured findings. You are the orchestrator, not the reader.
2. **Structured findings beat prose.** Force every reader through a JSON schema (`summary`, `keyFindings` with citations, `openQuestions`). Schema-shaped facts can be merged, diffed, and verified; prose can only be trusted.
3. **The live system outranks the docs.** Documentation states conventions; only the live system shows whether they're implemented. Real example of the failure mode: a documented "placeholder records are kept Inactive" convention where every live placeholder was Active — two of three designs built on the fiction. Always check the convention, not just the doc.
4. **Usage data settles arguments.** "Is bucket X dead?" / "does anyone use field Y?" are *queries*, not opinions. A design that maps into a never-used category, or drops a heavily-used one, is wrong in a way only live counts reveal. Every number in the study carries the query that produced it.
5. **Independent designs beat one design iterated.** Designers who can see each other converge on shared blind spots. Give the same study digest to designers with *conflicting value systems* and let the differences surface the real trade-offs.
6. **Plausible-but-wrong is THE failure mode of AI advice.** Designs reference fields that don't exist, assume single sources of truth that are actually duplicated, and inherit errors from the study digest. The adversarial pass is not optional polish — in practice it catches wrong field sources, misdescribed value lists, and unimplemented conventions in *every* run.
7. **Read-only, with receipts.** A study never writes to a live system — GET/SELECT only, stated as a hard rule in every agent prompt. Raw query output is saved to an evidence folder (`tmp/advice-study/` or similar) so a human can audit what was looked at.

## Phase 0 — Scope and scout (inline, before any fan-out)

Do this yourself; it's cheap and determines everything downstream.

1. **Pin the question** into the form *"how should [source thing] become / drive / map to [target thing]?"* — with the user's actual pain named (what confused or hurt them).
2. **Establish current state.** If how-it-works-today isn't already verified, run a current-state audit first (parallel readers + one verifier) and write it down. You cannot advise on changing a mechanism you haven't verified.
3. **Inventory the evidence sources.** The standard five — adapt to what exists:
   - **Domain/business context** — wiki, specs, ADRs, onboarding docs. *Why is the system shaped this way; who consumes what.*
   - **Target-side structure** — live schema/contract of the thing being written to (DB tables, entity metadata, API spec, config).
   - **Source-side structure** — live schema of the thing being read from, plus its adjacent machinery (rules engines, pricing tables, queues).
   - **Usage patterns** — live counts and distributions: which values/categories/paths are actually used, which links are actually populated.
   - **The comparison flow** — how does the *native*, *legacy*, or *competing* path do the same job? It encodes domain decisions the new design should honor or consciously reject.
4. **Verify access before fanning out.** One inline auth test against the live system (a `WhoAmI`, a `SELECT 1`). Five agents failing on auth in parallel wastes a fan-out.
5. **Confirm the environment** you're about to study (URL/connection string shown to the user) if there's any multi-environment ambiguity. Findings from the wrong environment are worse than no findings.

## Phase 1 — Study (parallel readers, one per evidence source)

Spawn one reader per source from the inventory, all in parallel. Each prompt contains:

- The pinned question and the verified current state (so readers know what matters).
- Its specific file paths / endpoints / entity names — scout these in Phase 0; don't make readers guess.
- The **read-only rule** and the **evidence folder** path, verbatim, for anything live.
- Platform gotchas you already know (quirky filters, encoding rules, rate limits) — agents rediscovering known gotchas is pure waste.
- The findings schema (see `references/workflow-template.md`).

Precise questions beat broad mandates: "does the target entity have ANY link back to the source entity — check all lookup/FK attributes" outperforms "study the target schema."

Then **merge mechanically** into one digest (concatenate the structured findings). No agent needed.

## Phase 2 — Design panel (independent, conflicting value systems)

Give the *same* digest to 3 designers who cannot see each other. Default lenses — rename to fit the domain:

| Lens | Optimizes for | Characteristic move |
|---|---|---|
| **Fidelity-first** | No information entered upstream may be lost downstream; full traceability | Adds columns/links; accepts schema growth |
| **Consumer-first** | What the downstream process actually consumes (capacity math, billing, search…) | Maps into the *correct* existing buckets; rejects new categories that break consumers |
| **Minimal-change pragmatist** | Smallest change that removes the worst pain, ranked by live-data evidence | Phases everything; prefers code-only over schema; quantifies pain ("breakbulk is 0.8% of lines") |

Swap lenses when the domain demands it (reliability/cost for infra, consistency/a11y for UX). Three is the sweet spot — two gives a false binary, five repeats itself.

Each designer must: ground every mapping in fields *the study proved exist* or explicitly flag as NEW; give exact transform rules (no "handle appropriately"); cover the awkward topics (what's dropped, what's defaulted, idempotency/retries); and answer the user's specific sub-questions (e.g. "what happens to the surcharges?") in a dedicated field of the design schema.

## Phase 3 — Adversarial feasibility (attack, then recommend)

One reviewer, whose only job is to break the designs. It must **re-verify primary sources itself** — re-open the code, re-query the live schema (read-only) — not just re-read the digest, because the digest itself may carry errors into all three designs. Attack checklist:

- **Existence:** does every referenced field/endpoint/value actually exist in the live system? (The most common kill: a design snapshots a total from a field that doesn't exist.)
- **Breakage:** what existing consumers — jobs, dashboards, state machines, capacity math, pickers — read the things being changed? Verify in code, not by intuition.
- **Data consistency:** do live distributions support the mapping? Are "dead" categories actually dead? Are "always populated" links actually populated?
- **Unimplemented conventions:** which documented conventions does the design rely on that the live system contradicts?
- **Where changes really land:** the file/layer a design names is often not where the behavior actually lives — verify the exact decision point.

Output per design: verified-OK list, problems *with evidence*, concrete fixes. Plus cross-cutting corrections (digest errors affecting all designs) and a recommendation: which design — or hybrid — survives, with which fixes applied.

## Phase 4 — Synthesize and deliver (you, in the main context)

Don't delegate this — judgment about the user's context lives with you.

1. Adopt the reviewer's recommendation unless you can articulate why not; apply **every** correction it found (each one was a falsehood about to be shipped as advice).
2. Write the advisory in this shape:

```markdown
## The N problems worth fixing, ranked by pain   ← business consequence first, mechanism second
## Phase 1 — [quick wins]                        ← small schema/code, kills the worst pain
## Phase 2 — [structural step]
## What NOT to do, and why                       ← the rejected options, each with its reason;
                                                    prevents the next person from re-proposing them
## Phase 3 (optional) — [riskiest piece]         ← last and severable; phases 1–2 must not depend on it
## Why this shape and not the alternatives       ← one paragraph per losing design
## Appendix — exact names, gotchas, evidence     ← for implementers; plus the evidence folder path
```

3. The advisory is a Markdown document — follow the diagram convention in `references/diagram-convention.md`: open with one overview diagram placed before `## The N problems worth fixing…` (typically a `graph TD` of the recommended phases and their key changes), and use `erDiagram` for proposed schema/mapping changes and `flowchart TD` for phase/decision logic.
4. Numbers keep their queries; claims keep their citations; corrections are stated plainly ("field X does not exist — sum the rows instead").
5. If the user maintains a knowledge base, offer to file the advisory there so it compounds.

## Scaling down

The method survives without the multi-agent machinery — the *phase separation* is the skill:

- **No Workflow tool:** sequential subagent calls (readers → designers → reviewer), same prompts and schemas.
- **No subagents at all:** do the phases yourself *in strict order* — write the study digest to a file before designing; write 2–3 genuinely different designs before judging; then switch to attack mode against the live system. Never let design start before study is written down, or the facts bend to fit the design.
- **Small question** (one mapping, one field): a single study pass + a single design + a self-review may suffice — but keep the existence-check and the read-only rule; those are non-negotiable at any scale.

## Red flags

| Thought | Reality |
|---|---|
| "The docs say how it works, skip the live check" | Docs state conventions; the live system decides. Verify both schema *and* convention. |
| "One good design is enough" | One design hides its trade-offs. The panel exists to surface them. |
| "The designs look solid, skip the attack pass" | Every run of this method has caught nonexistent fields or broken consumers. Looking solid is the failure mode. |
| "I'll write to the live system, it's just a test record" | A study writes nothing. Ever. |
| "The digest says it, so it's true" | Digest errors propagate to all designs — the reviewer re-verifies primary sources. |
| "Ship the recommendation without the 'what NOT to do' section" | Rejected options without recorded reasons get re-proposed in three months. |

## Bundled resources

- `references/workflow-template.md` — a ready-to-adapt Workflow script skeleton (Claude Code) with the three JSON schemas (findings, design, feasibility) and placeholder markers. Read it when you're about to run the pipeline with the Workflow tool.
