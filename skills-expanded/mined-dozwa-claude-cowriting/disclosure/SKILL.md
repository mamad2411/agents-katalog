---
name: disclosure
description: Generate the AI-use disclosure (KI-Verzeichnis / AI register) for the paper from the AI log, in English or German, as Markdown or LaTeX. Use before submission or when the author needs to declare AI use.
---

# Disclosure

1. Check for unannotated turns: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/ailog.py" stats`. If there are any, suggest annotating first (/cowrite:annotate); continue if the author wants.
2. Ask for language (en/de), format (md/tex), and the target (journal, university, funder) if not known.
3. Generate: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/ailog.py" disclosure --lang <en|de> --format <md|tex>`. Output goes to `disclosure/ai-register.<lang>.<format>`. If `stats` listed manuscript changes during AI tool calls, point the author at that section of the register: they must check those changes (git diff) and say what remained.
4. If the target requires the prompts (many German universities do), add the appendix: `python3 "${CLAUDE_PLUGIN_ROOT}/tools/ailog.py" prompts --lang <en|de> --format <md|tex> [--answers]` writes `disclosure/ai-prompts.<lang>.<format>`.
5. Help adapt it to the target's rules: point out what the target typically requires (e.g. tool + version + purpose + extent; prompts in an appendix; many journals forbid listing AI as author). Look up the actual policy if the author names the target, and cite where you found it. The author edits and signs the final statement.
6. Remind: the DFG asks to disclose *which* models were used *for what* and *to what extent*; pure grammar/spelling tools need no disclosure for DFG proposals, but universities may require it.
