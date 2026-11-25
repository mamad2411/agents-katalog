# Multi-Reviewer Design

## Luba Why / Loophole Repair-First Rule

When Luba asks "why" (in any language), challenges an answer, or says a failure came
from a loophole in plans, guides, skills, agent files, prompts, or governance
rules, this is an answer-first repair trigger, not a normal status question and
not permission to continue product work first.

Required order:
1. Answer Luba's why/loophole question directly.
2. Classify the previous behavior or claim as verified, overclaim, false,
   misread, or governance gap.
3. Identify the exact missing, weak, stale, or contradictory rule that allowed
   the failure.
4. Repair the governing plan, guide, skill, agent file, or start prompt first.
5. Verify the repair with direct readback, marker search, diff check, or another
   evidence-bound check.
6. Only after the repair is verified, resume the nearest already-authorized
   product task.

Do not substitute apology, status, a plan-quality note, or "I will continue" for
this repair. If no file repair is needed, state the exact evidence proving that
before continuing.

## Luba Global Plan-Quality / Skill-Stack Rule

This file inherits the global project rule: when Luba asks which plan is better,
judge by Luba's criteria: human clarity, readable architecture, architectural
reliability, evidence honesty, requirement fidelity, execution-control quality,
and low overclaim risk. Newer status tables, file counts, ledgers, count
freshness, or claimed pass counts are delta evidence only; use valid deltas to
patch the stronger plan instead of treating bookkeeping freshness as plan
superiority.

No executor session may speak as the active product executor until SK-INTENT,
SK-PLAN, SK-REVIEW, and SK-ARCH when applicable are loaded for the current task.
If the stack is not loaded, say "not loaded yet" and load it before plan
comparison, plan choice, status, executor work order, or implementation.

## Core Problem

A design review from a single perspective misses the failure modes visible from
other domains. A security reviewer who doesn't see the domain constraints and a
domain reviewer who doesn't see security requirements each miss legitimate gaps.
This skill defines a structured multi-perspective review where each reviewer
receives only their domain's context and produces independent verdicts.

Accepted reviewer gates are active task authority for downstream repair. Once a
BLOCK or accepted CONCERN is adopted by the governance loop, it must be entered
into the Authority Requirements Ledger with source_authority=reviewer_gate. A
downstream architect or executor must not treat it as a note, preference, or
optional wishlist item.

---

## When to Invoke

- Before any new interface or architecture decision is finalized
- When a design proposal touches multiple domains (security + business + principles)
- When a plan has more than 3 phases and needs multi-stakeholder validation
- When Luba asks for a thorough review before a major implementation starts

---

## Section 1 — The 5 Reviewer Roles

Select reviewers based on the capability's domain and risk level.

| Role | Context package (what they see) | What they check |
|---|---|---|
| **Domain Reviewer** | Capability spec, iron rules, domain context | Intent correctness, domain invariant completeness |
| **Security Reviewer** | Capability spec, DNA Rules 1/2, failure modes | Failure mode coverage, fabric-first compliance |
| **Business Reviewer** | Capability spec, downstream contracts, event schemas | Cross-component consistency, consumer impact |
| **Principles Reviewer** | Capability spec, DNA Rules (all 10), DECISIONS-LOCKED.md | DNA compliance, locked decision adherence |
| **Completeness Reviewer** | Capability spec, structure fields | All outputs reachable from inputs, no missing paths |

**Mandatory by risk level:**
| Capability type | Minimum reviewer set |
|---|---|
| Internal utility | Domain + Principles |
| Public interface (IXxx) | Domain + Security + Principles |
| Cross-component contract | Domain + Security + Business + Principles |
| Architecture decision | All 5 reviewers |

**Never add reviewers for appearance.** A security reviewer on a pure-compute algorithm that touches no storage adds noise without signal.

---

## Section 2 — Context Isolation Rule

Each reviewer receives ONLY their defined context package.

- Domain Reviewer: does NOT see security patterns or principles text
- Security Reviewer: does NOT see iron rules or domain context
- Principles Reviewer: does NOT see domain context or security patterns — only the capability spec and DNA/DECISIONS rules

**Context isolation ensures independent verdicts.** A reviewer who has seen another reviewer's verdict will anchor to it rather than finding independent issues.

---

## Section 3 — Verdict Format

Each reviewer produces a structured verdict:

```markdown
## [Role] Reviewer Verdict

Verdict: APPROVED | CONCERN | BLOCK

BLOCK items (plan cannot proceed without resolving these):
- [specific issue] — [which rule or principle is violated] — [what must change]

CONCERN items (plan may proceed but author must respond in writing):
- [issue] — [what this risks if unaddressed]

Evidence:
- [exact file:line or grep result that supports each BLOCK or CONCERN]
```

**BLOCK class:** Business Logic violations, Security violations (DNA Rule 2 violation, cross-tenant access), Principles violations (DNA Rule 1/10), Iron Rule violations.

**A single BLOCK overrides all APPROVED verdicts.** BLOCK cannot be diluted by averaging.

---

## Section 4 — The Convergence Protocol

After all reviewers produce verdicts:

### Round 1: Collect Verdicts

All reviewers produce verdicts independently. Record:
```
Domain Reviewer:      [APPROVED | CONCERN | BLOCK]
Security Reviewer:    [APPROVED | CONCERN | BLOCK]
Business Reviewer:    [APPROVED | CONCERN | BLOCK]
Principles Reviewer:  [APPROVED | CONCERN | BLOCK]
Completeness Reviewer:[APPROVED | CONCERN | BLOCK]
```

### Decision Rules (applied in order — stop at first match)

**Rule 1: Any BLOCK → Reject**
If any reviewer returns BLOCK:
- The blocked item is identified and must be resolved before proceeding
- Author addresses the BLOCK specifically; generic rewrites are not sufficient
- The BLOCK becomes a binding Authority Requirements Ledger row for repair
- After addressing: only the blocking reviewer re-evaluates (not full restart)

**Rule 2: All APPROVED (0 BLOCKs) with 0–2 CONCERNs → ACCEPTED**
Plan may proceed. Author responds to CONCERNs in writing before Phase 1.

**Rule 3: All APPROVED with 3+ CONCERNs → Targeted cycle**
Author addresses specific CONCERNs. Affected reviewers re-evaluate targeted sections only.

**Rule 4: Same BLOCK persists after 2 address cycles → Escalate to Luba**
If the author has addressed a BLOCK twice and the reviewer still finds it unresolved:
- This is a genuine architectural disagreement
- Escalate to Luba with full context: original BLOCK + both address attempts + reviewer response

**Rule 5: All outputs blocked (no path forward) → Redesign required**
If all reviewer paths produce BLOCKs that cannot be reconciled:
- Plan is not viable as stated
- Produce an ESCALATION report: what specifically blocks each path
- Redesign before new review cycle

### Maximum 3 cycles
After 3 cycles without full approval: escalate. Three cycles of BLOCK without resolution = the problem is architectural, not editorial.

## 10 Review Cycle Gate Compatibility

When Luba requests 10 reviews of an execution plan, this skill supplies reviewer
independence but does not reduce the count. The required output is 10 real
review/fix packets visible as records 1..10, each with reviewer role,
reviewer/sub-agent id or nickname, `requested_model=gpt-5.5`,
`requested_reasoning_effort=xhigh`, visible runtime/request metadata or
`mode_verified_from_work_order=true` when runtime metadata is unavailable and no
concrete contradiction is visible, exact plan section reviewed, verdict,
findings, repair action, files/sections affected, whether the plan/skills
changed, fixes or no-fix rationale, recheck evidence, and whether the plan
proves three full extensions for Claude, Cursor, and Codex.
Generic system/developer identity text such as "GPT-5" is not downgrade evidence
by itself; a stop based only on that text is a false downgrade stop and
premature stop loophole.

A panel table, convergence summary, or repeated verdict row is not a counted
cycle. If a reviewer finds a gap and the author fixes it, the next counted
cycle happens after the fix.

Human-readable output requirement: the 10 records must be understandable without
opening JSON, STATE, hidden transcripts, or machine logs. A valid packet also
feeds the Sub-Agent Visibility Ledger with agent id/nickname, requested
model/effort, task, status, key result, and what parent review accepted or
rejected.

---

## Section 5 — Review Output Format

```markdown
## Multi-Reviewer Design Review (multi-reviewer-design-SKILL)

Design: [capability or interface name]
Date: [date]
Reviewers used: [list roles]

Round [N] results:
| Reviewer | Verdict | BLOCK count | CONCERN count |
|---|---|---|---|
| Domain | APPROVED | 0 | 1 |
| Security | CONCERN | 0 | 2 |
| Principles | APPROVED | 0 | 0 |

Overall verdict: APPROVED_WITH_CONCERNS
Concerns to address: [list]
Next step: author responds to concerns → plan proceeds to Phase 1
```

---

## Section 6 — Escalation Report Format

When escalation to Luba is required:

```markdown
## Design Review Escalation

Capability: [name]
Cycle count: [N]
Still blocked by: [role] — [exact BLOCK text]

Address attempts:
  Attempt 1: [what was changed]
  Reviewer response: [still blocked — specific remaining issue]
  Attempt 2: [what was changed]
  Reviewer response: [still blocked — specific remaining issue]

Root cause assessment: [architectural disagreement / specification ambiguity / missing decision]

Question for Luba: [one specific decision needed to unblock]
```

---

## Anti-Patterns

1. **"One thorough review is enough"** — a single reviewer's blind spots are invisible to them. Multiple independent perspectives are the point.

2. **"Show all reviewers each other's verdicts before they finish"** — anchoring to prior verdicts eliminates the independence that makes multi-reviewer review valuable.

3. **"Average the BLOCKs against the APPROVEDs"** — a BLOCK from one reviewer means the design has a genuine problem. Averaging hides it.

4. **"Skip the CONCERNs because the plan is proceeding"** — CONCERNs that are not addressed in writing become implicit technical debt. The author responds; the concern is not dropped.

---

## Integration

- plan-review-SKILL.md is the detailed gate list, including the allowed
  trainable architecture pattern gate when learned/scorer/selector/router/KNN
  mechanisms are present; this skill provides the multi-perspective structure
- architect-behavior-classifier-SKILL.md FAIL-5 (claims without evidence) applies to every reviewer verdict
- decision-reopening-SKILL.md handles BLOCK items that conflict with locked decisions
- claim-verification-SKILL.md classifies each reviewer's evidence as VERIFIED/INFERRED/ASSUMED
