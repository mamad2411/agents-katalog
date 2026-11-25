---
name: sharpen
description: "Sharpen a task before starting: the expert approach, what the user is really after, and the right level of specification. Use for /sharpen, /pstack:sharpen in Claude Code, or $pstack:sharpen in Codex."
disable-model-invocation: true
---

Before starting, ask:

1. What would a top expert in this field do here that the task does not ask for?
2. What are the rawest sources they would start from instead of what is already digested?
3. Which specific methods and tools would they use?
4. What, other than the agent or the user, would show the result is right?

Ask also what the user is really after, and whether the task is over- or underspecified. Loosen constraints that don't serve the goal as readily as you add ones that do, and leave choices that are the user's to make open instead of deciding them. Fold in only what makes the work better, not bigger, but always keep one outside check that the result is right, without narrating the framing, then do the work. Rewrite the prompt instead only when the user asks for a rewritten prompt.

Invoke manually in either host. Do not load it implicitly. Preserve explicit user constraints, authorization gates, saved model assignments and spending policy. Loosening a constraint that the user chose requires their agreement; do not treat it as an implementation convenience.
