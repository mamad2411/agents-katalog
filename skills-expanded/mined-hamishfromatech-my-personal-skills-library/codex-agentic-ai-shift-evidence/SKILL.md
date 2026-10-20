---
name: codex-agentic-ai-shift-evidence
description: Understand how agentic AI diffuses across user populations and job functions using OpenAI Codex usage data. Use when analyzing agentic AI adoption, designing workflow transition strategies, evaluating delegation vs consultation patterns, or planning parallel agent orchestration.
---

# The Shift to Agentic AI: Evidence from Codex

## Overview

OpenAI's analysis of Codex usage data reveals that agentic AI is rapidly replacing conversational AI as the primary work interface. Among OpenAI workers, Codex accounts for 99.8% of output tokens across Codex and ChatGPT; among organizational users, 63.3%; among individual users, 16.5%. The shift is characterized by delegated production rather than consultation, increasing task complexity over time, and frontier users organizing work around parallel, long-running, reusable agent workflows.

## When to Use

- Analyzing how agentic AI adoption diffuses across organizations and roles
- Designing workflow transition strategies from conversational to agentic AI
- Evaluating task complexity growth and delegation patterns
- Planning parallel agent orchestration and skill-based workflow reuse
- Comparing individual, organizational, and frontier adoption patterns
- NOT for: conversational AI optimization, single-turn chat analysis, or non-agentic tool evaluation

## Core Process / Workflow

### 1. Assess Adoption Stage by Population

| Population | Codex Share of Output Tokens | Key Characteristic |
|-----------|------------------------------|-------------------|
| Individual users | 16.5% | Heterogeneous, limited workflow integration |
| Organizational users | 63.3% | Broader adoption, concentrated in technical roles |
| OpenAI workers | 99.8% | Near-universal, replaced business ChatGPT usage |

- Weekly active Codex usage grew 5x+ in first half of 2026
- Adoption is smallest among individual users, largest among OpenAI workers
- Growth is fastest outside the initial developer audience

### 2. Recognize the Four Stylized Facts

**Fact 1: Rapid but uneven shift**
- Agentic tooling much less broadly used than ChatGPT overall
- Shift smallest among individuals, largest within OpenAI
- Technical roles adopt earlier; non-developer use growing quickly

**Fact 2: Delegated production, not consultation**
- Users ask Codex to carry out work (debugging, refactoring, drafting), not just answer questions
- Contrasts with conversational AI where "asking" represented nearly half of prompts
- Task complexity increasing: share of users delegating >8-hour tasks rose ~10x

**Fact 3: Anchored in software, broader at frontier**
- Largest task share: code implementation, understanding, validation, engineering operations
- Within OpenAI: extends to research, planning, communication, data analysis, recruiting, sales
- Software is the leading edge; scope expands as adoption deepens

**Fact 4: Intensive users organize around parallel workflows**
- >10% of users manage 3+ concurrent agents weekly
- 26.6% use skills (reusable workflow instructions)
- Frontier users: 28.6% manage 5+ concurrent agents; 96.2% use skills
- Median OpenAI employee: 2.5 hours/day of active agent runtime; P99: 71 hours

### 3. Design for the Transition

**From consultation to delegation:**
- Standard metrics (active users, chats, messages) become less informative
- Track delegated task complexity, runtime, workflow reuse, concurrency, production output

**Workflow reorganization patterns:**
- Parallel agent management: users delegate, monitor, review across multiple streams
- Skill systematization: codify reusable workflows as skills/plugins
- Role shift: from producing to orchestrating, reviewing, directing

**Organizational complements:**
- Adoption depends on context: file access, management expectations, workforce skills, review processes
- Value depends on workflow redesign, not just tool availability
- analogous to electrification: largest gains from reorganizing production around new capabilities

### 4. Skill and Plugin Systematization

| Skill Source | Description | OpenAI Usage (7-day) |
|-------------|-------------|---------------------|
| Preinstalled | Bundled capabilities (image generation) | — |
| Curated | OpenAI-distributed standalone (PDF handling) | — |
| Plugin | Bundled with integrations (Google Drive) | — |
| Custom plugin | Recognized plugin, not in catalog | — |
| Custom | User/org-specific workflow codification | Highest among OpenAI (96.2%) |

- Skill use grew from 5.4% (March 2026) to 26.6% (June 2026) of active Codex users
- Custom skills most valuable in high-context organizational environments
- Plugins extend general capabilities; custom skills encode local procedural context

## References

- See [references/evidence-base.md](references/evidence-base.md) for full population breakdowns, task taxonomy, and adoption metrics.