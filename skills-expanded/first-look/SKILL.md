---
name: first-look
description: Get oriented in a binary you have never seen. What it is, where it starts, and the handful of functions worth reading first.
---

# First look

Goal: in a few minutes, tell the user what this program is and where the interesting code lives.

1. Call `binary_overview` (eleven-rea) for the format, architecture, size and signing.
2. Read the entry function with `procedure_pseudo_code`, and call `open_function` (eleven) on it so the user sees the same code.
3. Skim `list_strings` for user-facing text, URLs, file paths, error messages and format strings. They name features faster than code does.
4. Skim the external entries in `list_procedures`: networking, crypto, file, process and UI calls say what the program is able to do.
5. Pick up to five functions worth reading, the ones that use the most telling strings or imports. For each, read its pseudocode, then `rename_function` (eleven) it to what it does and `add_note` one sentence.

Report back in plain words:
- What the program is and does, in two sentences.
- The five functions, by their new names, with one line each.
- What you would look at next, and why.

Keep it short. Don't paste whole functions; the user reads those in Eleven.
