# Skill: Prompt Evaluator & Optimizer (FinOps Auditor)

## Meta
- **ID:** SKL-006
- **Name:** prompt_evaluate
- **Trigger:** `/prompt_evaluate [prompt_path]`
- **Objective:** Audit and refactor prompts to minimize Request Per Day (RPD) consumption and Token Per Minute (TPM) volume.

## Execution Logic

### 1. The Audit (Diagnostic)
Scan the target markdown for:
- **Sequential Steps:** Instructions like "First do X, then do Y" which trigger multiple API turns.
- **External Reads:** Phrases like "Read the file..." which force the tool to make extra IO requests.
- **Ambiguity Handshakes:** Phrases requiring confirmation ("Ensure you understand") which burn 1 request on a handshake.

### 2. Optimization Heuristics (The "Flattening" Protocol)
When suggesting a rewrite, apply these priorities in order:
1.  **Request Reduction (Primary):** Convert multi-turn agentic plans into "One-Shot" functional blocks. Replace "Read" instructions with `<<<` file inclusions.
2.  **Token Reduction (Secondary):** Strip non-essential context, redundant file content, and conversational "politeness" tokens.

## Definition of Done (Output Format)

### 📊 FinOps Diagnostic
- **Target File:** `[path/to/prompt]`
- **Baseline Requests:** `[N]` | **Baseline Tokens:** `[N]`
- **Primary Bottleneck:** `[e.g., Sequential Tasking / Implicit File Seeking]`

### 🛠️ Optimized Rewrite Suggestion (The "One-Shot" Version)
> Provide the full, ready-to-use Markdown code here. This version must use `<<<` includes and atomic instructions to ensure it executes in exactly **1 Request**.

### 📉 Projected Savings
- **Request Delta:** `-[N] RPD`
- **Token Delta:** `-[N]% TPM`
- **Strategy Used:** `[e.g., Context Consolidation / Atomic Output Mandate]`

---
**Telemetry Update:** Provide a `forecast_entry` JSON block for `telemetry.json` reflecting the *optimized* version's costs.