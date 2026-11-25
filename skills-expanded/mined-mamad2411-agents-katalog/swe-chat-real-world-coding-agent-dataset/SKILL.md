---
name: swe-chat-real-world-coding-agent-dataset
description: Applies the first large-scale real-world coding agent dataset (SWE-chat, Baumann et al., Stanford, April 2026) to understand how developers actually use coding agents in production. Use when analyzing coding agent effectiveness, designing real-world evaluation benchmarks, studying human-agent interaction patterns, or evaluating vibe coding vs collaborative coding tradeoffs.
---

# SWE-chat: Real-World Coding Agent Interactions

## Overview
SWE-chat is the first large-scale dataset of real coding agent sessions collected from open-source developers in the wild, enabling evidence-based understanding of how AI coding agents perform in production versus curated benchmarks.

## When to Use
- Designing realistic benchmarks for coding agents beyond curated SWE-bench tasks
- Evaluating the gap between benchmark performance and real-world developer workflows
- Studying vibe coding (agent authors >99% of code) vs collaborative coding tradeoffs
- Understanding user pushback patterns and human oversight in agent sessions
- Assessing security vulnerability introduction rates in agent-written code
- NOT for evaluating single-turn code completion or benchmark-only settings

## Core Process / Workflow

### 1. Dataset Context
- **6,000 sessions** from 200+ public GitHub repositories
- **63,000 user prompts** and **355,000 agent tool calls**
- Complete interaction traces with **line-level human vs. agent code authorship attribution**
- Agents: Claude Code (~85% of data), OpenCode, Gemini CLI, Cursor, Factory AI Droid
- Living dataset that continually discovers and processes new sessions via Entire.io CLI

### 2. Key Empirical Findings

**Coding Mode Distribution (Bimodal):**
- Vibe coding (agent authors >99% of code): **40.8%** of sessions, growing from 20% → 40% in 3 months
- Human-only coding (agent as assistant): **22.7%**
- Collaborative coding: **36.5%**

**Efficiency Gaps:**
- Only **44.3%** of agent-produced code survives into user commits
- Vibe coding consumes **3× more tokens** and dollars per committed line
- Vibe-coded commits introduce **9× more security vulnerabilities** per 1K committed lines (0.76) vs human-only (0.08) and 5× more than collaborative (0.14)
- Collaborative coding is most cost-efficient: $0.05 per 100 committed lines vs $0.13 vibe coding

**Interaction Patterns:**
- Users push back in **41% of turns** (corrections, rejections, failure reports)
- Agents proactively ask for clarification in only **1.1–2.6%** of turns
- Users interrupt agents in **3.3–6.0%** of turns
- Most common user intent: **understanding existing code** (19.0%), not writing new code (13.4%)
- Agent tool calls: 33% bash commands, 48% file read/edit/search

**User Personas:**
- Expert Nitpickers: 39.7% (meticulous correction of agent output)
- Vague Requesters: 33.5% (underspecified goals, delegate decisions)
- Mind Changers: 19.9% (redirect goals mid-session)

### 3. Implications for Agent Design

**Autonomy vs Oversight Asymmetry:**
- Agents are gaining autonomy faster than learning when to seek guidance
- Users compensate through manual oversight, which doesn't scale to background agents
- Collaborative sessions (human + agent co-author) are most efficient

**Security Burden Shift:**
- As autonomy grows, the burden of catching unsafe patterns shifts entirely to users
- Vibe-coded commits fix more vulnerabilities (0.52/1K lines) but introduce more (0.76/1K lines)
- Net vulnerability increase is largest for vibe coding

**Benchmark Design:**
- Current benchmarks reward one-shot patch generation
- Real workflows are iterative, multi-turn, with understanding as the most common intent
- Session trajectories can power user simulators for offline evaluation

### 4. A-Tech Application Framework

**For Open-Source AI Products:**
- Design agent interfaces that encourage collaborative coding over pure vibe coding
- Build verification and trust calibration into the agent workflow
- Instrument real usage to detect when agents are being used as code comprehension tools vs code writers
- Prioritize security scanning integration for agent-written code

**For Developer Experience:**
- Track code survival rate (agent lines surviving to commit) as a DevEx metric
- Monitor pushback rates as a friction indicator
- Design for the "understanding code" use case, not just code generation
- Build interfaces that surface agent uncertainty proactively

## References
- See [references/evidence-base.md](references/evidence-base.md) for full dataset statistics, methodology, and comparison with existing benchmarks.