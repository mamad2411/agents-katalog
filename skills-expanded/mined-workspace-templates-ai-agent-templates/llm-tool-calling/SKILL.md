---
name: llm-tool-calling
description: Designs tool schemas and the call loop for LLM function calling, with argument validation, error feedback and a hard step limit.
---

# LLM tool calling

Design the tool surface before writing the loop. The model only sees names, descriptions and schemas, so those are the interface.

## Steps

1. List the real actions the app needs. Merge near-duplicates; five sharp tools beat fifteen overlapping ones.
2. Name each tool as verb plus object (`search_orders`, not `orderTool`). Write the description as when to use it and when not to, with one example.
3. Give every parameter a type, an enum or range where possible, and a description. Mark only truly required fields as required. Prefer IDs the model got from an earlier result over free text.
4. Validate arguments on the server with a schema library before running anything. Never trust the model's JSON, and never build SQL or shell commands from it.
5. Return failures as tool results, not exceptions: say what was wrong and what a valid call looks like, so the model can retry once.
6. Write the loop with a maximum step count (6 to 10 is typical), a total token budget and a repeat check that aborts when the same call with the same arguments appears twice.
7. Require confirmation in code, not in the prompt, before any tool that writes, sends or deletes.

## Rules

- Tool results must be short. Trim, paginate and strip fields the model does not need.
- Log every call with arguments, result size and latency.
- Test with adversarial prompts: missing information, two tools that fit, a request no tool covers.

## Report

Show the final tool list with schemas, the loop code, and the limits chosen with a reason for each.
