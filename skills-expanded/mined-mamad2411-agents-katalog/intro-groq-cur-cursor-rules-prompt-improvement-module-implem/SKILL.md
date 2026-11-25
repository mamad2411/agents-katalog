---
description:
globs:
alwaysApply: false
---

# Prompt Improvement Module: Implementation Instructions

## Who is the LLM? ("The Twin")

**The LLM ("the twin") is a dedicated language model agent used for grading and improving prompts.**

- The twin is **not** your production chatbot.
- The twin is **not** a human reviewer.
- The twin is a separate, trusted LLM (such as GPT-4, Claude, or another advanced model) that acts as an expert grader and improver in the prompt improvement loop.
- All grading, suggestions, and rationale are provided by the twin, and every decision is logged for auditability.

---

## Overview
This document provides step-by-step instructions for implementing the prompt improvement module, including LLM-in-the-loop grading and improvement, logging, and review.

---

## Implementation Steps

1. **Read Planning Docs**
   - Review all `.md` files in `prompt_improvement_module/` to understand requirements, flow, and rules.

2. **Prepare Inputs**
   - Ensure `intro_groq_cur/app/api/chat/prompts/opinionMbpPrompts.ts` is present and up to date.
   - Ensure `desired_outputs/all_desired_outputs.md` contains all gold-standard outputs, formatted as specified in `desired_output_format.md`.
   - Ensure `grading_criteria.md` and `prompt-format.md` are present.
   - (Optional) Set up `config.json` for module settings.

3. **Set Up Logging**
   - Create a `conversation_history/` folder for iteration logs.
   - Ensure logs include prompt text, model output, desired output, grading, twin suggestions, timestamps, and iteration number.

4. **Implement Iteration Loop**
   - For each prompt:
     - Run the prompt through the chatbot and capture the output.
     - Retrieve the desired output from `all_desired_outputs.md`.
     - Send the prompt, output, desired output, rubric, and context to the twin for grading and improvement.
     - Log all steps and results.
     - If the prompt does not pass, update it as suggested by the twin and repeat.
     - If the prompt cannot be improved, flag it for manual review.

5. **LLM-in-the-Loop Handoff (The Twin)**
   - The LLM (the twin) is responsible for grading, logging, and suggesting improvements. The app/module orchestrates execution and handles the improvement loop, sending logs and outputs to the twin as needed.
   - See `llm_iteration_handoff.md` for the detailed handoff and iteration procedure.

6. **Review and Approve**
   - After all prompts pass, review improved prompts and logs.
   - Only merge improved prompts into production after human approval.

---

## General Notes
- Keep code and planning docs separate for maintainability.
- All steps and decisions must be logged for traceability.
- Output formats are designed for easy review and integration.

---

Next: See `llm_iteration_handoff.md` for the twin handoff and collaboration details.
