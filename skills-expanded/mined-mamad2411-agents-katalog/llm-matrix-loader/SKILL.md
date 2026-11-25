---
skill_id: ACU-SKILL-PAN-002
name: llm-matrix-loader
displayname: LLM Matrix Loader — Unified Ranking Matrix Engine
description: Load, normalize, query, and validate the Acuterium LLM Ranking Matrix. Supports both legacy MasterLLMsRankingMatrix.json and current AcuteriumFinalLLMRankingMatrix.json formats. Normalizes all data into Golden Schema format for ADOCP routing consumption.
category: Data Engineering
domain: infrastructure
acuterium_thread: T01 COSM
acuterium_thread_code: T01
acuterium_shard: ADOCP
acuterium_layers: [L5, L6, L7]
sovereignty_score: 10
governance_level: mandatory
author: Acuterium Technologies Inc.
license: Proprietary-ACU
version: 1.0.0
status: published
tags: [llm-matrix, ranking, loader, normalization, golden-schema, adocp, routing]
trigger_keywords: [load matrix, llm ranking, model scores, matrix query, normalize models, golden schema, provider lookup, model comparison, cost lookup, uptime score]
---

# LLM Matrix Loader — Unified Ranking Matrix Engine

## Purpose
The LLM Matrix Loader is the data access layer for the entire Acuterium AI orchestration ecosystem. Every routing decision, allocation, and scoring operation depends on this module to provide consistent, validated matrix data.

## Supported Formats
- **Format A** Legacy Grouped: `MasterLLMsRankingMatrix.json`
- **Format B** Flat Models: `AcuteriumFinalLLMRankingMatrix.json`
- **Format C** Golden Schema Target: `AcuteriumMasterLLMRankingMatrixGolden-RuleSchema.json`

## Core Functions
- `load_llm_matrix(path)` — Load matrix from JSON file. Auto-detects format A, B, or C and returns normalized data structure
- Normalization Rules: Format B/C group flat models by provider field; Format A/C map legacy field names
- Duplicate detection: Models in both legacy files are merged (newer data wins)
- Placeholder handling: Entries with only provider and note fields flagged as incomplete

## Required Fields per Golden Schema
Every loaded matrix entry MUST contain or explicitly mark N/A:
1. `llm` string — Provider name
2. `submodels` — Array with model, api_key, cost, deepresearch, predictive_uptime_score
3. `consciousness` — compatibility, reasoning_depth, ethical_alignment
4. `capabilities` — reasoning, cognition, multimodal, document_handling, code_generation
5. `performance` — latency, hallucination_rate, accuracy
6. `scoring` — reasoning, creativity, accuracy, speed, multimodal, coding

## Data Integrity Rules
1. Never delete legacy entries unless officially confirmed discontinued
2. Scoring values must be 0-100 range validated on load
3. Cost values must be non-negative USD per 1K tokens
4. predictive_uptime_score must be 0.0-1.0
5. fallback_llms must reference models that exist in the matrix
6. Placeholder entries preserved but flagged with `placeholder: true`

## Integration Points
- **ADOCP Router** — Primary consumer; routes tasks to optimal LLMs based on matrix scores
- **Resource Allocator** — Scores candidates using matrix scoring and cost data
- **Swarm Coordinator** — Auto-registers swarm nodes from submodels entries
- **Meta Negotiation** — Queries candidates and scores for task-type matching
- **Task Recovery** — Reads fallback_llms arrays for recovery chain construction
- **Event Triggers** — Loads matrix for model selection on event processing
- **Compliance Validator** — Validates loaded matrix against Golden Schema structure

## Thread
- **Thread:** T01 COSM
- **Shard:** ADOCP
- **Module:** Pan Framework / AcuTect-CODEX

---
*Acuterium Technologies Inc. — ADOCP Shard — T01 COSM — Classification: Proprietary-ACU*
*ASIP v2 Compliant | TokenBridge Authorized | Golden Schema Enforced*
