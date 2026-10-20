---
name: tech-debt-triage
description: Inventory technical debt and prioritize it by interest paid, not by annoyance - quantify cost, classify, and produce a ranked paydown plan that survives contact with a roadmap. Use when the user asks what to refactor first, wants a tech debt audit, needs to justify cleanup work to stakeholders, or asks whether to fix or live with a known problem.
license: MIT
compatibility: elyra >=0.1, claude-code
allowed-tools: read, bash, grep
metadata:
  author: elyra-skills
  version: 1.0.0
  tags: [tech-debt, prioritization, refactoring, maintenance]
---

# Tech Debt Triage

Debt isn't bad code — it's code that **charges interest**: slower features, more bugs, harder onboarding. Triage means paying down the highest interest first, not the ugliest file.

## When to use

- "What should we refactor first?" / "How bad is our tech debt?"
- Justifying cleanup time to stakeholders who want features
- Deciding fix-now vs live-with-it for a known problem
- Before a big feature lands in a debt-heavy area

## Principles

- **Interest, not ugliness.** Hideous code nobody touches costs nothing. Mildly awkward code changed weekly costs plenty.
- **Debt = (friction per change) × (change frequency).** Both factors are measurable; measure them.
- **Not all debt should be paid.** "Accepted, documented, revisit-trigger set" is a legitimate outcome.
- **Paydown rides with features.** Standalone "refactor sprints" get cancelled; debt work attached to roadmap items ships.

## Process

### 1. Inventory — collect candidates from evidence

```bash
# Churn: most-changed files (where interest accrues)
git log --since="6 months ago" --format= --name-only | sort | uniq -c | sort -rn | head -20

# Self-reported debt
grep -rn "TODO\|FIXME\|HACK\|XXX" --include="*.{php,ts,js,py}" . | wc -l
```

Plus: bug-dense modules (issue tracker), areas devs complain about, slow/flaky test zones, outdated deps blocking upgrades, missing tests around critical paths.

### 2. Locate the hotspots

Cross churn with complexity: **large + complex + frequently changed = hotspot**. A complex file with zero changes in a year is *not* a priority, whatever the linter says.

### 3. Classify each item

| Type | Example | Typical move |
|---|---|---|
| **Blocking** | Can't upgrade framework; deploy takes a day | Schedule explicitly |
| **Taxing** | Every feature in module X takes 2× | Pay down with next feature there |
| **Risky** | No tests around payments; single point of failure | Insure (tests/monitoring) first, fix second |
| **Cosmetic** | Naming, style, "I'd have done it differently" | Usually: leave it |

### 4. Score: interest vs paydown cost

For each item, estimate honestly:

- **Interest/month:** dev-hours lost, bugs caused, opportunities blocked
- **Paydown cost:** effort to fix, including testing and migration risk
- **Rank by interest ÷ cost.** High interest + low cost = do now. Low interest + high cost = accept and document.

### 5. Plan the paydown

- Attach each top item to a roadmap vehicle: "fix X *as part of* feature Y in that area"
- Keep slices small and independently shippable (see `refactoring` for the how)
- For accepted debt: write down the decision and a revisit trigger ("if module X causes one more sev-2…") — see `adr-author`

### 6. Make it visible

Track 2–3 trend metrics, not twenty: e.g. time-to-ship in the hotspot, bug count in the area, dependency freshness. Report movement, not vibes.

## Output format

```markdown
## Tech debt triage: <project/area>

**Evidence gathered:** churn, TODO count, bug clusters, dev input.

### Ranked debt
| # | Item | Type | Interest/mo | Cost | Action |
|---|------|------|-------------|------|--------|
| 1 | …    | taxing | high (≈X h) | M | pay down with feature Y |
| 2 | …    | risky  | …           | L | add tests now |
| … | …    | cosmetic | low       | M | **accepted** — revisit if … |

### Top 3 recommendation
1. … (why this first)

### Accepted debt log
- <item>: accepted <date>, trigger: …
```

## Anti-patterns

- ❌ Ranking by ugliness or personal taste instead of measured interest
- ❌ The "big rewrite" as the answer to diffuse debt
- ❌ A debt backlog with 200 items and no scores — that's a graveyard, not a plan
- ❌ Refactoring cold spots because they're easy wins (they win nothing)
- ❌ Asking for a "cleanup sprint" with no quantified payoff — it loses to features every time
- ❌ Paying down debt with no tests in place first in risky areas
- ❌ Never re-running the triage — debt rankings rot in months
