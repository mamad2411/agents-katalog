---
name: "capture-aha-moment"
description: "Capture sudden agent insights, root-cause discoveries, and mental model shifts as lightweight knowledgebase entries in real-time (not during end-of-session distillation)."
version: 1
created: "2026-05-24"
updated: "2026-05-24"
---
## When to Use
Use when the agent has a sudden breakthrough realization during work — NOT for routine progress, task completion, or planned work. Trigger examples: "aha!", "oh wait", "I see now", "that's why", root cause discovered after chasing wrong path, realizing an assumption was wrong, understanding how something actually works vs how it was assumed to work, discovering a hidden constraint or dependency that changes the approach.

## Procedure
1. Recognize the aha: It's not about finishing a task — it's about a sudden shift in understanding. Signs: realizing a root cause, discovering why earlier attempts failed, understanding a system's actual behavior vs assumed behavior, finding a hidden constraint.
2. Format: Write a lightweight YAML entry to knowledgebase/patterns/ or knowledgebase/decisions/ depending on nature. Use the structure: id (kebab-case), title (descriptive, captures the insight), created (YYYY-MM-DD), tags (relevant tech/topic tags), problem (what confused us), breakthrough (the aha realization — what was actually happening), implications (how this changes things).
3. Write the file: knowledgebase/patterns/<id>.yaml or knowledgebase/decisions/<id>.yaml
4. Update knowledgebase/index.yaml — add the entry to the patterns or decisions section.
5. Index (if available): Run load-kb-to-memory.py for vector DB or kb submit for Central KB, but don't block — the KB file itself is the primary record.
6. Do NOT create a full session summary entry — that's for distill-and-index at session end. Aha moments are single-insight entries.

## Pitfalls
- Don't overuse — not every solved problem is an aha moment. Reserve for genuine breakthroughs that changed understanding.
- Don't skip writing because indexer is unavailable — the KB file itself is the durable record.
- Don't replace the session summary — aha entries and session summaries serve different purposes (single insight vs whole-session context).
- Don't pad with context the reader already knows — focus on the surprising/shift part.
- Aha moments from earlier in a session should be captured when they happen, not batched at the end.

## Verification
1. File exists at knowledgebase/{patterns,decisions}/<id>.yaml
2. Entry referenced in knowledgebase/index.yaml
3. Entry is self-contained — someone reading it a month later would understand the insight without the surrounding conversation
