---
name: deep-investigation
description: Progressive iterative research with persistent knowledge vault, entity tracking, and coverage gates. USE WHEN deep investigation, investigate, deep research, map the landscape, competitive analysis, market mapping, technology survey, thorough research.
---

# Deep Investigation

**Mode:** Progressive iterative research with persistent knowledge vault
**Time:** 10-60 minutes | **Can span multiple sessions** via persistent vault files

## When to Use

- User says "deep investigation", "investigate [topic]", "deep research", "map the [X] landscape"
- Competitive analysis, market mapping, technology surveys, threat landscape analysis
- Any research needing iterative deepening -- broad discovery first, then progressive deep dives
- When surface-level research is insufficient and systematic coverage matters

## Concept

Progressive narrowing funnel:
```
Iteration 1: Broad landscape --> discover entities --> score importance --> deep-dive top entity
Iteration 2: Read vault artifacts --> pick next highest-priority entity --> deep-dive
Iteration 3+: Continue until all critical entities researched and all categories covered
```

**Single-run:** One full cycle (landscape through first deep dive).
**Multi-session:** User returns later; workflow detects existing vault state and continues.

## Available Tools

| Tool | Use For |
|------|---------|
| **WebSearch** | Landscape queries, entity discovery, deep-dive queries |
| **WebFetch** | Deep reads of sources, entity profile research, URL verification |
| **claude-browser MCP** | Auth-walled or JS-heavy pages |

## Vault Location

```
~/.augment/MEMORY/RESEARCH/{YYYY-MM-DD}_{topic-slug}/
```
Vault survives across sessions. Workflow is stateless -- all state lives in files on disk.

---

## Workflow

### Step 0: Detect Iteration State

Check vault directory for existing artifacts:
- LANDSCAPE.md + ENTITIES.md exist --> CONTINUATION: read ENTITIES.md
  - PENDING CRITICAL/HIGH entities? --> Step 4 (Investigate)
  - All CRITICAL/HIGH done but thin categories? --> Step 3 (Discover)
  - All gates pass? --> Step 5 (Summarize)
- Neither exists --> FIRST ITERATION: start at Step 1

### Step 1: Landscape Scan (First Iteration Only)

**Goal:** Map the full landscape. Do this once, reference cheaply in all later iterations.

Run 4-6 WebSearch queries covering: domain overview, key players, recent developments, historical context, adjacent domains, contrarian views. Deep-read top 3-4 results with WebFetch.

**Produce three vault files:**

**LANDSCAPE.md** -- Domain synthesis with sections: Overview (2-3 paragraphs), Domain Structure, Key Dynamics, Entity Categories (discovered dynamically, with estimated counts), Initial Entity Discoveries, Sources (verified URLs only).

**ENTITIES.md** -- Master catalog table with columns: Entity, Category, Status (PENDING/RESEARCHED/SKIP), Value (CRITICAL/HIGH/MEDIUM/LOW), Effort (EASY/MODERATE/HARD), Profile link. Include legend definitions at the top.

**INDEX.md** -- Navigation hub linking to LANDSCAPE.md, ENTITIES.md, and profiles as they are created. Track coverage stats: categories complete, entities researched, CRITICAL/HIGH pending.

### Step 2: Evaluate (Score Entities)

For each PENDING entity, assess two dimensions:

**VALUE:** CRITICAL (category definers, must research) > HIGH (major players) > MEDIUM (notable) > LOW (minor)
**EFFORT:** EASY (abundant public info) > MODERATE (some digging) > HARD (limited info)

**Investigation priority:** CRITICAL+EASY first, then CRITICAL+HARD, HIGH+EASY, HIGH+HARD. MEDIUM+ only after all CRITICAL/HIGH done. Update ENTITIES.md with scores.

### Step 3: Discover (Expand Coverage)

Find entities in categories with fewer than 3 entries. For each thin category:

```
WebSearch(query: "notable {category} in {domain} space")
WebSearch(query: "{domain} {category} key players landscape")
```

WebFetch the best results. Add discoveries to ENTITIES.md as PENDING, then score them (Step 2).

### Step 4: Investigate (Deep Dive -- One Entity)

**Quality over quantity.** Research ONE entity per iteration.

Select the highest-priority PENDING entity (VALUE desc, EFFORT asc). Run 2-3 focused WebSearch queries:
- "[entity] overview analysis {domain}"
- "[entity] recent news funding developments"
- "[entity] vs competitors strengths weaknesses"

Deep-read top 2-3 results with WebFetch.

**Save profile to vault:** `{Category}/{entity-slug}.md` containing: overview, key facts (founding, size, funding, leadership), products, competitive advantages/weaknesses, recent developments, cross-links to related vault entities, verified source URLs.

Update ENTITIES.md (mark RESEARCHED, add link) and INDEX.md (add to navigation).

### Step 5: Progress Check (Coverage Gates)

Two gates must BOTH pass for completion:

**Breadth Gate:** Every entity category has >= 3 entities (excluding SKIP).
**Depth Gate:** Every CRITICAL or HIGH entity is RESEARCHED or SKIP.

**Both pass:** Produce SUMMARY.md (executive synthesis), update INDEX.md with final stats, report completion.
**Either fails:** Report current coverage, identify gaps (thin categories, pending CRITICAL/HIGH entities), ask user whether to continue or stop.

---

## Output Artifacts

```
{vault}/
  INDEX.md          -- Navigation hub with coverage stats
  LANDSCAPE.md      -- Broad domain analysis
  ENTITIES.md       -- Master catalog with status tracking
  SUMMARY.md        -- Executive synthesis (on completion)
  {Category}/       -- Entity profiles by category
    entity-a.md
    entity-b.md
```

All profiles cross-linked. Vault is self-contained and readable standalone.

## Single-Run vs Multi-Session

| Aspect | Single-Run | Multi-Session |
|--------|-----------|---------------|
| Coverage | Landscape + first deep dive | Full breadth + depth gates |
| Exit | After Step 4 | After Step 5 gates pass |
| Time | 10-15 minutes | 30-60 min across sessions |

Single-run: complete Steps 1-4, report what remains PENDING.

## URL Verification

All vault URLs MUST be verified via WebFetch before inclusion. A broken link in a persistent vault is a compounding error -- it misleads every future session that reads it.
