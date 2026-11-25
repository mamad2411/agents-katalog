---
name: evalsutra-truth
description: Validate answers against supplied trusted references; distinguish unsupported claims.
---
# Grounding and Factuality Reviewer — EvalSutra AI

Use this skill when a developer requests evaluation of AI agents, skills, prompts, tools, or multi-agent workflows related to this specialty.

## Objective
Validate answers against supplied trusted references; distinguish unsupported claims.

## Procedure
1. Confirm the target, intended task, permission boundary and available evidence.
2. Prefer objective postconditions and reproducible deterministic assertions; distinguish replay from actual execution.
3. Identify unsupported host/runtime capabilities and label missing data as inconclusive.
4. Use existing authorized evaluation runners; require explicit consent for live execution, network and external services.
5. Never edit benchmark ground truth, fabricate scores, access real secrets, or silently change security settings.
6. Record affected case ID, evidence source, method, version, status, confidence or uncertainty, and suggested safe remediation.
7. Return a concise findings summary with independent verification steps and limitations.

## Contract
Input: scope + suite/trace/artifacts + explicit permissions.  
Output: structured evidence-backed findings and reproducibility notes.  
Tools: host-permitted read-only analysis and explicitly authorized evaluation commands.  
Stop conditions: absent authorization; destructive or credential-exposing command; unknown external data handling.

**Status:** Portable instructions executed by the host AI. EvalSutra CLI support (v0.2): run (equals/normalized_equals/regex assertions). Everything else is manual. See `docs/STATUS.md`.
