---
name: research-question
description: Answers a caller's question with sources, confidence and gaps in the item's research.md. Use when acting as the researcher, or when asked to research a question, check a claim or find out what a decision or plan depends on.
---
# Research a question

**Role:** researcher. This skill is the method. The researcher's `ROLE.md` holds how you are called (the caller keeps the item), what you reply with, and the quality bar. Follow both.

1. Take the question from the caller's request or the item's `handoff.md`. Create `research.md` with `python3 tools/item_file.py <id> research` and restate the question in it so the caller can confirm it was understood.
2. Check what the repo already says (`docs/INDEX.md`, ADRs) before looking outside.
3. Gather sources. Prefer primary and current ones. Record each claim with its source and date. Mark anything inferred as an assumption.
4. Write the answer first, then the evidence, then the open gaps. Give a confidence level and what would change it.
5. Raw material and long notes go in `work/research/`. If a finding must outlive the work item, say so in your reply: the caller records it in the handoff, and the scribe promotes it into `docs/` as an explanation or reference page.
