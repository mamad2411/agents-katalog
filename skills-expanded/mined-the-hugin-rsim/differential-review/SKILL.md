---
name: differential-review
description: Security-focused review of code changes (PRs, commits, diffs) with blast radius estimation and adversarial modeling. Seven-phase workflow from triage to final report. Adapted from Trail of Bits methodology.
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
group: security
triggers:
  - "diff"
  - "PR"
  - "коммит"
  - "что изменилось"
  - "ревью изменений"
output: "security review report with blast radius and risk assessment"
calls: []
---

# Differential Review

Reviews code changes through a security lens: git diffs, PRs, staged changes, or explicit file deltas. Scales automatically to change size.

## When to Use

- User asks to review a PR, commit, or diff
- User asks "what could break" in a change
- Pre-merge security check
- Reviewing changes to auth, crypto, configuration, or data handling
- Starting point is `git diff`, `gh pr`, or a set of changed files

## When NOT to Use

- Full codebase audit from scratch → use deep code reading instead
- Code quality review without security focus → use `backend-code-review`
- Reviewing a single isolated function with no change history
- The change is only comments, docs, or test fixtures with no logic

## Rationalizations to Reject

These are shortcuts that compromise findings. Reject them explicitly:

- **"It's a minor refactor, no security implications"** — refactors regularly reintroduce removed fixes silently
- **"Tests pass, so it's fine"** — tests don't model attackers; passing tests ≠ secure code
- **"The change is internal-only"** — internal code runs with real privileges on real data
- **"The original developer knows what they're doing"** — even experts miss blast radius
- **"This pattern is used elsewhere in the codebase"** — widespread usage doesn't make a pattern correct
- **"It's behind authentication"** — auth bypasses are common; don't reduce security scrutiny

---

## Workflow (7 Phases)

### Phase 0 — Intake & Triage

Determine what changed and assign risk before diving in.

```bash
git diff HEAD~1 --stat          # overview of files changed
git diff HEAD~1                 # full diff
gh pr view --json files         # if reviewing a PR
```

**Classify scope:**
| Size   | Files changed |
|--------|--------------|
| SMALL  | < 20         |
| MEDIUM | 20–200       |
| LARGE  | 200+         |

**Risk tier per file:**
| Tier   | File types / patterns |
|--------|----------------------|
| HIGH   | auth, crypto, session, config/env, external API calls, payment, validation removal, permissions |
| MEDIUM | business logic, state mutations, new public APIs, DB queries |
| LOW    | comments, tests, UI, logging, docs |

---

### Phase 1 — Changed Code Analysis

For every HIGH/MEDIUM file:
- Side-by-side comparison of before/after logic
- Run `git blame <file>` on modified lines — trace history
- **Regression check:** was a security-related commit silently undone?
- Document at least one concrete attack scenario per HIGH-risk change

**Immediate escalation flags:**
- Removed validation without replacement
- Access control downgraded (private → public, admin → user)
- Hardcoded credentials or secrets introduced
- Unchecked return values from security-critical calls
- CVE-fix commit reverted or overwritten

---

### Phase 2 — Test Coverage Analysis

- New functions without tests → escalate to HIGH risk
- Modified validation logic → require updated tests
- Complex logic (> 20 lines) without test coverage → flag

---

### Phase 3 — Blast Radius

Count callers of every modified function using Grep:

| Callers | Blast Radius |
|---------|-------------|
| 1–5     | LOW         |
| 6–20    | MEDIUM      |
| 21–50   | HIGH        |
| 50+     | CRITICAL    |

CRITICAL blast radius + HIGH-risk change = immediate top-priority finding.

---

### Phase 4 — Deep Context (HIGH-risk only)

For files/functions with HIGH or CRITICAL risk:
- Trace full call chains up and down
- Document invariants: what must always be true entering/leaving the function
- Map trust boundaries: where does untrusted data enter?
- Find shared mutable state modified by the change

See [methodology.md](methodology.md) for line-by-line analysis technique.

---

### Phase 5 — Adversarial Modeling

For every HIGH finding, construct:
1. **Attacker model** — who is the attacker, what access do they have
2. **Attack vector** — concrete sequence of actions to exploit
3. **Exploitability** — EASY / MEDIUM / HARD with justification

See [adversarial.md](adversarial.md) for full framework.

---

### Phase 6 — Report Generation

Generate structured markdown report. Template in [reporting.md](reporting.md).

Mandatory sections:
1. Executive Summary (severity table + recommendation)
2. What Changed (file list, risk tiers, blast radius)
3. Critical Findings (HIGH/CRITICAL with attack scenarios)
4. Test Coverage Gaps
5. Recommendations (immediate / pre-production / tech debt)
6. Analysis Limitations (what was NOT covered and why)

---

## Quality Thresholds

Before delivering the report, verify:
- [ ] Every finding cites specific `file:line` reference
- [ ] Every HIGH finding includes a concrete attack scenario
- [ ] Blast radius calculated for every modified function
- [ ] Regression check performed (no silently removed security fixes)
- [ ] No vague language ("probably", "might", "could potentially")
- [ ] Coverage limitations explicitly stated

---

## Supporting Files

| File | Purpose |
|------|---------|
| [methodology.md](methodology.md) | Detailed per-phase analysis techniques |
| [adversarial.md](adversarial.md) | Attack modeling framework |
| [reporting.md](reporting.md) | Report templates |
| [patterns.md](patterns.md) | Vulnerability patterns by category |
