---
name: policy-drafting
description: >
  Draft an employment policy for Hong Kong where Employment Ordinance (Cap 57) governs
  the jurisdictional footprint. Use when the user says "draft a [topic]
  policy", "we need a policy on", "update our [topic] policy", or names a
  policy gap.
argument-hint: "[policy topic — e.g., 'remote work', 'parental leave', 'PTO']"
---

# /policy-drafting

1. Load `~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → jurisdictional footprint, handbook location.
2. Use the workflow below.
3. Draft core policy. Check each jurisdiction in footprint for required variants.
4. Output: core policy + state supplements. Flag where law is currently shifting.

---

## Matter context

**Matter context.** Check `## Matter workspaces` in the practice-level CLAUDE.md. If `Enabled` is `✗` (the default for in-house users), skip the rest of this paragraph — skills use practice-level context and the matter machinery is invisible. If enabled and there is no active matter, ask: "Which matter is this for? Run `/employment-legal:matter-workspace switch <slug>` or say `practice-level`." Load the active matter's `matter.md` for matter-specific context and overrides. Write outputs to the matter folder at `~/.claude/plugins/config/claude-for-hk-law/employment-legal/matters/<matter-slug>/`. Never read another matter's files unless `Cross-matter context` is `on`.

---

## Purpose

A policy that's right for California may be wrong (or unnecessary) in Texas. This skill drafts a core policy and generates state supplements where the footprint requires different rules.

## Load context

`~/.claude/plugins/config/claude-for-hk-law/employment-legal/CLAUDE.md` → jurisdictional footprint, handbook location and format.

## Workflow

### Step 1: Scope the policy

- What's the policy for? (Remote work, parental leave, social media, etc.)
- Why now? (Legal requirement, incident, growth, gap noticed)
- Who does it apply to? (All employees, certain roles, certain locations)

### Step 2: HK legislative scan

For each topic, check whether the Employment Ordinance (Cap 57) or related HK legislation prescribes a specific rule that must be reflected in the policy. Unlike the US approach of state-by-state variance, HK has a single legal regime. However, common law principles and Equal Opportunities Commission guidelines may impose additional requirements beyond the statutory text.

**Common topics with jurisdictional variance:**

| Topic | HK legislation / rule |
|---|---|
| Statutory holidays | Must provide 12+ statutory holidays per year (Cap 57 s. 39 Sch. 3); general holidays are not mandatory |
| Annual leave | Statutory minimum 7–14 days depending on length of continuous employment (Cap 57 Part IX) |
| Maternity leave | 14 weeks' entitlement (Cap 57 Part III); 4 weeks' pre-confinement + 10 weeks' post-confinement |
| Paternity leave | 5 days' entitlement (Cap 57 Part IIIA) |
| Sick leave | Accrual of paid sickness days; 4/5 of normal wages (Cap 57 Part VIII) |
| MPF contributions | Mandatory employer 5% of relevant income (Cap 485 s. 7A) |
| End-of-year payment | 13th month / contractual bonus rules (Cap 57 Part IIC) |
| Anti-discrimination | Policies must comply with Cap 480, 487, 527, 602 |
| Restrictive covenants | Enforceability under HK common law (legitimate business interest + reasonableness) |
| Employee data privacy | Must comply with PDPO (Cap 486) — collection, use, retention, and transfer of employee personal data |

If the topic has no jurisdictional variance (dress code, say), skip this step.

### Step 3: Draft the core policy

One policy. Applies everywhere. Clear and readable — employees should understand it without a lawyer.

Structure:
- Purpose (one sentence — why this policy exists)
- Scope (who it applies to)
- The rule (what's required/permitted/prohibited)
- Process (how to request, who approves, what happens if)
- Questions (who to ask)

Avoid: "heretofore," "notwithstanding," nested exceptions. This is a handbook policy, not a contract.

### Step 4: State supplements

For each jurisdiction where the rule differs, a supplement:

```markdown
### [State] Supplement

Employees working in [State] are subject to the following in addition to / instead of the core policy:

- [Specific difference]
- [Cite the state law if helpful]
```

Keep supplements tight. Only what's different — don't repeat the core.

### Step 5: Cross-check

- Does this policy conflict with anything already in the handbook?
- Does it promise more than the company intends to deliver? (A policy can become a contractual term if incorporated into the employment contract.)
- Does it comply with Cap 57 s. 42C statutory particulars requirements?
- Does it conflict with MPF obligations under Cap 485?
- Does it comply with anti-discrimination requirements under the DDO/SDO/FSDO/RDO?

## Output

```markdown
# [Policy Name]

## Core Policy

[Full text]

## References to applicable HK legislation

### Employment Ordinance (Cap 57)
[Relevant sections]

### Anti-Discrimination Ordinances
[Cap 480 / 487 / 527 / 602 as applicable]

---

## Drafting Notes (internal — remove before handbook insertion)

- **Jurisdictional scan:** [which states checked, which have variance]
- **Conflicts with existing handbook:** [none | list]
- **Law currently shifting:** [any state where this is in flux]
- **Review cadence:** [when to revisit — annual, or when X happens]
```

> **Draft, not a policy in effect.** This is a drafting aid for attorney review, not a policy you can publish. Publishing a handbook policy has legal consequences — in several states it can bind the company as a contractual promise, and wage/leave/accommodation policies are routinely read against the employer. A licensed attorney, solicitor, barrister, or other authorised legal professional in your jurisdiction reviews, edits as needed, and takes professional responsibility before the policy is rolled out. Do not publish or distribute this draft unreviewed.

## Handoff

To handbook-updates skill: when this policy is approved, it diffs against the current handbook and flags what changes.

## What this skill does not do

- Approve the policy. It drafts; a human approves.
- Roll out the policy. Communication to employees is an HR workflow.
- Cover every jurisdiction on earth — only the ones in the footprint. If the footprint expands, re-run.
