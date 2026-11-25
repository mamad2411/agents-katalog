---
name: adversarial-review
description: >
  Adversarial review protocol for brainstorming, product planning, and technical architecture.
  Validate ideas against reality, enforce minimum 3 bugs, severity categorization, 3 resolution paths.

  USE WHEN: "adversarial review", "run adversarial protocol", "validate brainstorming",
  "stress test idea/plan/architecture", or reviewing any planning document.

  CORE PROTOCOL:
  1. Reality vs Claims — web search min 3x diverse angle, status VALID/PARTIAL/INVALID
  2. Acceptance Criteria — stress test specific executor capability
  3. Mandatory Bug Quota — minimum 3 issues, force deeper dig if insufficient
  4. Interactive Resolution — Critical/High/Medium/Low + options A(auto-fix)/B(action items)/C(deep dive)

  DIFFERENTIATOR: Mandatory bug quota prevents superficial reviews. Three resolution options
  make findings actionable. Executor stress test differentiates from generic reviews.
metadata:
  version: 1.0.0
  author: V (OpenClaw)
category: quality
---

## Section 1: Protocol Overview

Adversarial Review consists of 4 mandatory stages executed sequentially.

```
Stage 1: Reality vs Claims     → web_search + web_fetch (min 3x diverse)
Stage 2: Acceptance Criteria  → stress test executor
Stage 3: Mandatory Bug Quota  → minimum 3 specific issues
Stage 4: Interactive Resolution → categorization + 3 resolution options
```

**Core principle:** A good review isn't about throwing criticism, but transforming findings into decisions.

---

## Section 2: Stage 1 — Reality vs Claims

**Objective:** Validate claims and assumptions in the document against real data and libraries.

### Execution Rules

1. Use web_search and web_fetch minimum **3 times** with different angles
2. Don't just search one topic — diversify: library docs, benchmarks, user pain points, known issues
3. Mark each claim with status: **VALID** / **PARTIAL** / **INVALID** / **UNVERIFIED**
4. Include hidden caveats not mentioned in the original document

### Search Angle Guidelines

```
Angle 1: Library/tech being used → find known limitations, version issues
Angle 2: User pain point → find real UX research or forum complaints
Angle 3: Benchmark/performance → find real data, not marketing claims
Angle 4: Competitor/alternative → find if problem has been solved elsewhere
Angle 5: Production failure → find post-mortems or known failure modes
```

### Output Format

```
**Claim:** "[claim from document]"
**Status:** VALID / PARTIAL / INVALID / UNVERIFIED
**Facts:** [data from search]
**Hidden caveat:** [not mentioned in document]
```

---

## Section 3: Stage 2 — Acceptance Criteria

**Objective:** Not just whether the idea can be done, but whether this specific executor can do it.

### Questions to Answer

```
1. Does the chosen tech stack match the executor's skills?
2. Are there components requiring significant learning curve?
3. Is the time estimate realistic for this executor (not team)?
4. Are there external dependencies outside the executor's control?
5. Is there a proof-of-concept needed before committing to production?
```

### Output Format

```
**Component:** [component/bet name]
**Verdict:** Executable / Partial / Needs PoC first / Beyond capability
**Reason:** [specific, honest]
**Recommendation:** [concrete steps if there's a gap]
```

---

## Section 4: Stage 3 — Mandatory Bug Quota

**Objective:** Force discovery of non-obvious problems. Prevent reviews that are too soft.

### Quota Rule (NON-NEGOTIABLE)

```
MINIMUM 3 specific issues must be found.
If < 3 found → SYSTEM MUST SEARCH AGAIN in:
  - Edge cases: what happens during extreme conditions?
  - Performance issues: what happens at scale/high load?
  - Architecture violations: is this design consistent?
  - Dependency risk: what happens if library changes?
  - UX failure mode: what happens when user does unexpected things?
```

### Severity Categories

| Level | Definition | Example |
|-------|------------|---------|
| 🔴 Critical | Will kill the product/project if not fixed | Core promise cannot be delivered |
| 🟠 High | Will cause significant problems in production | Performance degradation, bad UX |
| 🟡 Medium | Real issue but has workaround | File clutter, minor inconsistency |
| 🟢 Low | Needs attention but not urgent | Naming convention, minor inefficiency |

### Bug Report Format

```
### [EMOJI] [LEVEL] #N — [Short Title]

**Problem:** [specific description, not generic]
**Trigger scenario:** [when this issue occurs]
**Impact:** [what happens to user/product]
**Why it's dangerous:** [why this isn't an edge case that can be ignored]
```

---

## Section 5: Stage 4 — Interactive Resolution

**Objective:** Every finding must have a resolution path, not just criticism.

### Three Resolution Options (Always Provide All Three)

```
A. Auto-fix
   → Directly fix the problematic idea/plan
   → Output: new version of the fixed section
   → Suitable for: problems with clear solutions

B. Action Items
   → Checklist to be executed by user
   → Output: [ ] specific item with done criteria
   → Suitable for: problems requiring user decision

C. Deep Dive
   → Detailed problem explanation with concrete examples
   → Output: in-depth analysis + trade-offs
   → Suitable for: problems requiring understanding before deciding
```

### Resolution Summary Table

```markdown
| # | Issue | Severity | Primary Recommendation |
|---|-------|----------|------------------------|
| 1 | [title] | 🔴 Critical | [one sentence fix] |
| 2 | [title] | 🟠 High | [one sentence fix] |
```

---

## Section 6: Full Protocol Template

```markdown
# Adversarial Review — [Document/Project Name]

## Stage 1 — Reality vs Claims
[Results from 3+ web searches with diverse angles]
[Status per claim: VALID/PARTIAL/INVALID/UNVERIFIED]

## Stage 2 — Acceptance Criteria
[Stress test per component/bet]

## Stage 3 — Mandatory Bug Quota (minimum 3)
[Bug #1 — Critical/High/Medium/Low]
[Bug #2 — ...]
[Bug #3 — ...]

## Stage 4 — Interactive Resolution
[Per bug: option A / B / C]

### Summary Priority Matrix
| # | Issue | Severity | Primary Recommendation |
|---|-------|----------|------------------------|

## Meta-Conclusion
[One paragraph: what changed the most? first step priority?]
```

---

## Section 7: Quick Reference

**Do's:**
- Run 4 stages sequentially without skipping
- Diversify web search angles (don't search the same topic 3x)
- Be honest about executor capability
- Provide all three resolution options for each Critical and High finding

**Don'ts:**
- Don't stop at < 3 issues
- Don't create resolutions that are too generic ("just fix it")
- Don't skip Stage 2 — executor stress test is this protocol's main differentiator
- Don't combine multiple components in one bug report

**Trigger phrases:**
```
"run adversarial review protocol for [document]"
"adversarial review this"
"validate this brainstorming hard"
"stress test this plan"
"find weaknesses in [plan/architecture]"
```
