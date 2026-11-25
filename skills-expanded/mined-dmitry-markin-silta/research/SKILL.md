---
name: research
description: Run significant research as a dedicated subagent and deliver the result as a PDF. Use when a question needs more than a quick lookup: comparisons, background reading, planning, anything with several sources.
---
1. React 👀 to the request, then launch the `researcher` agent with `model: opus`, always in the background (`run_in_background: true`, never foreground, so the chat stays responsive), passing the question verbatim, the person's language, and an output path `out/<slug>.md`.
2. When it returns, run `cite.py <file>` from this skill's directory (renumbers `[@](URL)` markers, rebuilds Sources; note its stderr counts, bare URLs mean broken citations), then run the md2pdf skill on the file and send the PDF with send_file, captioned with the agent's short summary. Keep the report itself out of the main context; pass caveats on in the caption or a follow-up line.
3. If the agent fails or the result is thin, say so and offer to retry with a narrower question.
