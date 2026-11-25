---
name: curriculum-review
description: "Reviews and improves existing course curricula with gap analysis, modern content updates, and engagement optimization."
allowed-tools: Read Write Glob
metadata:
  author: Salah-XD
  version: "1.0"
---

# Curriculum Review

## When to Use This Skill

Use this skill when you need to:
- Audit an existing course or training program for quality and relevance
- Identify content gaps, outdated material, and engagement weak points
- Modernize a curriculum with current best practices and updated examples
- Optimize course structure for better completion rates and learning outcomes

**DO NOT** use this skill for creating a new course from scratch or reviewing non-educational content. This is for improving existing curricula.

---

## Core Principle

A CURRICULUM REVIEW IS NOT ABOUT ADDING MORE — IT IS ABOUT IDENTIFYING WHAT IS MISSING, WHAT IS OUTDATED, AND WHAT IS KILLING ENGAGEMENT, THEN MAKING SURGICAL IMPROVEMENTS THAT RAISE COMPLETION RATES AND OUTCOMES.

---

## Phase 1: Brief

### Required Inputs

| Input | What to Ask | Default |
|-------|------------|---------|
| **Course to review** | "Share your current course outline, syllabus, or curriculum document." | No default — must be provided |
| **Original goals** | "What outcomes was this course designed to deliver?" | No default — must be provided |
| **Known problems** | "What feedback have you received? Where do students drop off?" | None — will assess from structure |
| **Audience changes** | "Has your target audience shifted since the course was created?" | Same audience |
| **Completion data** | "What is your current completion rate? Which modules have the lowest engagement?" | Unknown — will estimate from structure |

**GATE: Confirm the brief and receive the existing curriculum before proceeding.**

---

## Phase 2: Audit

Analyze the existing curriculum across five dimensions.

### Audit Framework

```
## 1. Content Relevance Audit
- Which topics are still current and accurate?
- Which examples or case studies are outdated?
- What industry changes require updated content?
- Score: [1-10]

## 2. Gap Analysis
- What essential topics are missing?
- Where do students need more depth?
- What prerequisites are assumed but not taught?
- Score: [1-10]

## 3. Engagement Assessment
- Where are the longest stretches without interaction?
- Which modules lack exercises or application?
- Where is the content dense without variety?
- Score: [1-10]

## 4. Structure and Flow
- Does the sequence build logically?
- Are there difficulty spikes that could cause drops?
- Is the pacing consistent across modules?
- Score: [1-10]

## 5. Outcome Alignment
- Does each module connect to the stated course outcome?
- Are there modules that do not serve the final goal?
- Is the final outcome achievable given what is taught?
- Score: [1-10]
```

**GATE: Present the audit findings and wait for the user to prioritize improvements.**

---

## Phase 3: Recommend

Create a prioritized improvement plan.

### Improvement Categories

**Critical (do now):**
- Factually incorrect or outdated content
- Missing foundational topics that cause confusion later
- Modules with zero interaction or application

**Important (do soon):**
- Outdated examples that weaken credibility
- Engagement dead zones longer than 15 minutes without interaction
- Pacing issues causing difficulty spikes

**Nice to have (do later):**
- Additional examples or case studies
- Supplementary resources
- Visual or format upgrades

### Recommendation Format

For each recommendation:

```
## Recommendation: [Title]
**Priority:** Critical / Important / Nice to have
**Current state:** [What exists now]
**Problem:** [Why it needs to change]
**Recommended change:** [Specific action]
**Estimated effort:** [Low / Medium / High]
**Impact on completion:** [Low / Medium / High]
```

---

## Phase 4: Polish

### 1. Updated Curriculum Map

Provide a revised outline showing all changes:
- Marked additions (new content)
- Marked removals (cut content)
- Marked revisions (updated content)
- New module order if restructured

### 2. Implementation Roadmap

```
## Phase 1 (This week): Critical fixes
- [ ] [Specific action]

## Phase 2 (This month): Important improvements
- [ ] [Specific action]

## Phase 3 (This quarter): Enhancements
- [ ] [Specific action]
```

### 3. Ongoing Review Schedule

Recommend a quarterly content freshness check:
- Review examples and data for accuracy
- Check completion rate trends per module
- Survey recent graduates for feedback
- Update one module per quarter minimum

---

## Example 1: Outdated Marketing Course Review

```
Audit finding: 40% of examples reference platforms or features that no longer exist.
Recommendation: Replace 12 case studies with current examples. Priority: Critical.
Estimated effort: Medium (8-10 hours of content updates).
```

## Example 2: Low-Completion Coding Bootcamp

```
Audit finding: Module 4 has a 60% drop-off rate. Content jumps from basic to advanced with no bridge.
Recommendation: Add an intermediate exercise module between 3 and 4. Priority: Critical.
Estimated effort: High (new module creation, 15-20 hours).
```

---

## Anti-Patterns

- **Reviewing without data** — gut feelings are not a curriculum review. Use completion rates, feedback, and drop-off data wherever available.
- **Adding without cutting** — if you add 3 modules, consider removing or merging 2. Course bloat kills completion.
- **Surface-level updates** — changing screenshots while ignoring structural problems wastes time.
- **Ignoring the audience shift** — a course built for beginners in 2020 may now attract intermediates. Adjust depth accordingly.
- **Recommending a full rebuild** — the goal is improvement, not replacement. Focus on highest-impact changes first.

---

## Recovery

- **No curriculum document provided:** Ask the user to list module titles and one-sentence descriptions for each. Work from that outline.
- **No completion data:** Estimate engagement risk based on module length, interactivity, and content type. Flag modules over 20 minutes with no exercises.
- **User wants to add everything:** Force-rank recommendations by impact. Limit Phase 1 to the top 3 critical fixes.
- **Course is beyond repair:** If more than 70% of content needs replacement, recommend building a new course using the working 30% as a foundation rather than patching the old one.
