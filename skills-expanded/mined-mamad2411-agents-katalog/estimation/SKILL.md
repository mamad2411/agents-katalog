---
name: estimation-skill
description: "Provide story point and time estimates for features and tasks using complexity analysis, historical patterns, and risk assessment. Use when the user asks \"how long will this take\", \"estimate this feature\", \"story points\", \"effort estimation\", \"sprint planning\", or needs to plan timelines. Also use when breaking down work into sized chunks for sprint planning."
allowed-tools: Read, Grep, Glob
---

# Estimation Skill

Provide realistic effort estimates for features and tasks. Estimates should be ranges (not single numbers) and account for unknowns. The goal is to help with planning decisions, not to promise delivery dates.

## When to Use

- User asks how long a feature will take to build
- Sprint planning requires story point assignments
- Comparing effort between different approaches
- Determining if a task is SMALL/MEDIUM/BIG for the orchestrator
- Scoping work for a milestone or release

## Estimation Process

Follow this sequence for every estimate:

### Step 1: Decompose the Feature

Break the feature into concrete tasks before estimating. Estimate the parts, then sum — never estimate a vague whole.

```markdown
## Feature: Add OAuth2 Login (Google + GitHub)

### Tasks:
1. Set up OAuth2 configuration and environment variables
2. Implement Google OAuth callback handler
3. Implement GitHub OAuth callback handler
4. Create/update user on first OAuth login
5. Link OAuth accounts to existing email-based accounts
6. Add OAuth login buttons to frontend
7. Write tests for OAuth flows
8. Update API documentation
```

### Step 2: Score Each Complexity Factor

| Factor | Low (1) | Medium (2) | High (3) |
|--------|---------|-----------|----------|
| Code Changes | 1-3 files | 4-10 files | 10+ files |
| New Concepts | None | 1-2 new patterns | New architecture |
| Dependencies | None | 1-2 services | Cross-team / external |
| Testing | Simple unit tests | Integration tests | E2E + edge cases |
| Risk | Well-understood | Some unknowns | Significant unknowns |

### Step 3: Map to Effort

| Total Score | Size | Story Points | Solo Dev Time |
|------------|------|-------------|--------------|
| 5-7 | S | 1-2 | < 4 hours |
| 8-10 | M | 3-5 | 1-2 days |
| 11-13 | L | 8-13 | 3-5 days |
| 14-15 | XL | 13-21 | 1-2 weeks |

### Step 4: Apply Risk Multipliers

| Risk Factor | Multiplier | When to Apply |
|-------------|-----------|--------------|
| New technology | x1.5 | First time using a framework, API, or pattern |
| External API dependency | x1.3 | Relying on third-party API with unknown behavior |
| No existing tests | x1.4 | Changing code that has no test coverage |
| Unclear requirements | x1.5-2.0 | Requirements are vague, contradictory, or incomplete |
| Cross-team coordination | x1.3 | Requires another team to make changes or review |

### Step 5: Produce the Estimate

Always give a range, not a single number. The range reflects uncertainty.

## Worked Example

```markdown
## Estimation: Add OAuth2 Login (Google + GitHub)

### Task Breakdown
| Task | Files | New? | Deps | Tests | Risk | Score |
|------|-------|------|------|-------|------|-------|
| OAuth config setup | 3 | No | 0 | Unit | Low | 5 (S) |
| Google callback | 4 | Yes | 1 | Integration | Med | 10 (M) |
| GitHub callback | 4 | No* | 1 | Integration | Low | 8 (M) |
| User create/link | 3 | No | 0 | Integration | Med | 9 (M) |
| Account linking | 5 | Yes | 1 | E2E | High | 12 (L) |
| Frontend buttons | 2 | No | 0 | Unit | Low | 5 (S) |
| Test suite | 6 | No | 0 | All | Med | 9 (M) |
| Documentation | 2 | No | 0 | None | Low | 5 (S) |

*GitHub follows same pattern as Google — lower risk after Google is done.

### Summary
| Metric | Value |
|--------|-------|
| Total Score | 63 across 8 tasks |
| Size | L (Large) |
| Story Points | 13 |
| Base Estimate | 3-5 days |
| Risk Multiplier | x1.3 (external API: Google/GitHub OAuth) |
| **Final Estimate** | **4-7 days** |
| Confidence | Medium (OAuth flows are well-documented but account linking has edge cases) |
```

## Output Format

```markdown
## Estimation: [Feature Name]

| Factor | Score | Reasoning |
|--------|-------|-----------|
| Code Changes | [1-3] | [why] |
| New Concepts | [1-3] | [why] |
| Dependencies | [1-3] | [why] |
| Testing | [1-3] | [why] |
| Risk | [1-3] | [why] |
| **Total** | **[sum]** | |
| **Size** | **[S/M/L/XL]** | |
| **Story Points** | **[range]** | |
| **Estimated Time** | **[range]** | |
| **Risk Multiplier** | **[if any]** | [reason] |
| **Final Estimate** | **[adjusted range]** | |
| **Confidence** | **[Low/Medium/High]** | [what's uncertain] |
```

## Anti-Patterns

- **Single-number estimates** — "it'll take 3 days" is always wrong; give a range that reflects uncertainty ("3-5 days, could be 7 if account linking has edge cases")
- **Estimating without decomposition** — estimating a whole feature without breaking it into tasks leads to underestimates; always decompose first
- **Anchoring bias** — letting the user's initial guess influence your estimate; score the complexity factors independently
- **Ignoring testing effort** — testing typically takes 30-50% of implementation time; if your estimate doesn't include testing, double it
- **Optimistic assumptions** — assuming everything will go smoothly; apply risk multipliers for unknowns
- **Estimating effort you can't control** — don't include waiting time for code review, stakeholder approval, or deployment; estimate development effort only

## Checklist

- [ ] Feature decomposed into concrete tasks
- [ ] Each task scored on all 5 complexity factors
- [ ] Mapped to size (S/M/L/XL) and story points
- [ ] Risk multipliers applied where warranted
- [ ] Estimate expressed as a range (not single number)
- [ ] Confidence level stated with reasoning
- [ ] Testing effort explicitly included
- [ ] Assumptions documented
