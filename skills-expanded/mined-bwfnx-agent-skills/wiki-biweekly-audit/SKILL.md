---
name: wiki-biweekly-audit
description: Biweekly SBDC wiki content audit — coverage, accuracy, and synthesis gaps
---

> **Schedule:** Every two weeks
> **Needs:** workspace files
> **Helper scripts (yours, not included):** learnings.py

Run the wiki-system-biweekly-audit workflow.

Read your full instructions from this file and follow them exactly:

    {{WORKSPACE_ROOT}}/Scheduled/wiki-system-biweekly-audit/SKILL.md

That file is the single source of truth for this task. Read it fresh on every run.
This prompt is deliberately thin so the workflow can be edited in one place without
re-pasting anything here.

Before you start, query {{USER}}'s durable learnings store. Do NOT read
learnings.jsonl whole -- it overflows the tool-result cap:

    cd /d "{{WORKSPACE_ROOT}}"
    py {{WORKSPACE_ROOT}}/learnings.py list --skill wiki-system-biweekly-audit
    py {{WORKSPACE_ROOT}}/learnings.py list --grep <topic>     (if the above returns nothing)

Prioritise entries of type "pitfall". A learnings entry that contradicts the
SKILL.md wins -- it is newer.

If you cannot read that file, STOP and report that you could not read it. Do not
reconstruct the workflow from the task name or from memory, and do not fall back to
any older copy of these instructions.