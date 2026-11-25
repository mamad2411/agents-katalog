---
name: annotate
description: Annotate AI log entries: was the AI input adopted, adapted, rejected or just information, and for which chapter. Use after receiving help, or when the pane shows unannotated turns.
---

# Annotate AI log entries

1. Show the recent turns: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/ailog.py" list --last 10`
2. Ask the author, for each unannotated turn they want to annotate: use (`adopted` / `adapted` / `rejected` / `info`), optional chapter, optional note.
3. Record each answer:
   `python3 "${CLAUDE_PLUGIN_ROOT}/tools/ailog.py" annotate <id|last> --use <use> [--chapter "<chapter>"] [--note "<note>"] [--category <category>]`
4. Confirm briefly. Never decide the annotation yourself; it is the author's statement.
