---
skill_id: ACU-SKILL-PAN-003
name: adocp-routing-protocol
displayname: ADOCP — Acuterium Dynamic Orchestration Coordination Protocol
description: Sovereign task-to-LLM routing protocol. Analyzes task requirements against the LLM Ranking Matrix scores, applies ASIP v2 soul infusion, and routes to the optimal model with fallback chain construction. Core routing brain for AcuTect-CODEX.
category: Core Orchestration
domain: cognitive
acuterium_thread: T01 COSM
acuterium_shard: ADOCP
acuterium_layers: [L5, L6, L7, L8]
sovereignty_score: 10
governance_level: sovereign
author: Acuterium Technologies Inc.
license: Proprietary-ACU
version: 1.0.0
status: published
tags: [adocp, routing, orchestration, sovereign, asip, task-routing, llm-selection]
trigger_keywords: [route task, select model, adocp, task routing, optimal llm, fallback chain, soul infusion, asip, coordinate agents, orchestrate]
---

# ADOCP — Acuterium Dynamic Orchestration Coordination Protocol

## Purpose
ADOCP is the routing brain of the Acuterium ecosystem. It receives task requests, analyzes requirements against the LLM Ranking Matrix, applies ASIP v2 sovereign personality infusion, and dispatches to the optimal execution model.

## Routing Pipeline
1. **Step 1 — Task Ingestion:** Accepts TaskRequest with task_file YAML schema path
2. **Step 2 — ASIP v2 Soul Infusion:** Calls `codex.asip_v2.infuse_soul(task)` to embed sovereign personality tags
3. **Step 3 — Matrix-Based Routing:** Loads AcuteriumFinalLLMRankingMatrix.json via llm_matrix_loader; matches task.llm_required against submodels.model names
4. **Step 4 — Scoring & Selection:** Scores candidates using scoring.reasoning, scoring.coding, submodels.cost, submodels.predictive_uptime_score, capabilities.multimodal, language_proficiency
5. **Step 5 — Fallback Construction:** Builds ordered fallback chain from submodels.fallback_llms for Task Recovery

## Core Functions
- `route_task(task, matrix)` — Match task requirements to matrix entries. Returns optimal model name. Default fallback GPT-4o
- `execute(task_request: TaskRequest)` — Full execution pipeline: load task, infuse soul, load matrix, route, return result. Returns task_id, selected_llm, asip_version, soul_tags, status

## Golden Schema Integration
ADOCP routing decisions governed by:
- `submodels.cost` — Cost-efficiency scoring
- `submodels.predictive_uptime_score` — Reliability scoring
- `submodels.deepresearch` — Research task matching
- `submodels.fallback_llms` — Recovery chain
- `scoring.*` — Capability matching (reasoning, coding, multimodal)
- `capabilities.deployment` — Sovereign/cloud/edge routing
- `capabilities.security.data_sovereignty` — Sovereign-grade task routing

## Compliance Rules Integration
Monitored via compliance_rules.yaml:
- `llm_cost_sum` — Tracks cost per provider across unified routes
- `LLMUptimeCritical` — Alerts if uptime < 0.8, triggers rerouting

## Protocol Dependencies
| Protocol | Role in ADOCP |
|---|---|
| ASIP v2 | Soul infusion pre-routing |
| Q-ARC | Resource coordination post-routing |
| NEXUS | Mission-level orchestration wrapper |
| QFP | Output fusion for multi-agent results |
| PRISM | Predictive intelligence for routing optimization |

## Thread
- **Thread:** T01 COSM
- **Shard:** ADOCP
- **Module:** Pan Framework / AcuTect-CODEX Core

---
*Acuterium Technologies Inc. — ADOCP Shard — T01 COSM — Classification: Proprietary-ACU*
*ASIP v2 Compliant | TokenBridge Authorized | Sovereign Routing Active*
