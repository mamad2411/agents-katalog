---
name: decidir
description: Use TypedDecisionMCP for comando, subagente, diff, ficheiro, commit.
---

# decidir

Call the MCP tool `decidir` with `preset` and `state`. For `ficheiro` or `pacote`, put 2–20 paths in `state.candidates`.

The motor is local logits. It does not generate answer tokens. Trust `action` and the typed `answers`. Never invent a probability in the chat text.
