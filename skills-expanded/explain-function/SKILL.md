---
name: explain-function
description: Explain one function properly. What it does, its inputs and outputs, who calls it and what it calls, with names that make sense.
---

# Explain a function

1. Call `current_view` (eleven) to see which function the user is on, unless they named one.
2. Read it with `procedure_pseudo_code`, and `procedure_assembly` when the pseudocode looks wrong or too clever.
3. Look at `procedure_callers` and `procedure_callees` to place it in the program.
4. Work out the parameters and the return value from how callers use them.

Then:
- `rename_function` (eleven) it, and any FUN_ callees you understood, to plain C names.
- `add_note` one sentence on what it does.
- `open_function` the most important callee when the story continues there.

Answer with: what it does, how it does it in three to six steps, and anything surprising (error paths, magic numbers, side effects). Quote at most a few lines of code.
