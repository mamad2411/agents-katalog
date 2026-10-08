---
name: order-prompt
description: Create bounded subagent prompts from agent-careflow PLAN and ORDER artifacts.
---

Use `agent-careflow order prompt --tool codex --case <case_id> --order <order_id>` and pass the rendered prompt to the subagent. The prompt must contain `plan_path`, `order_path`, and `expected_result_path`.
