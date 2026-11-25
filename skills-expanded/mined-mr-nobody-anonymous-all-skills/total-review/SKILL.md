---
name: total-review
description: 'Run Fable and GPT reviews, then combine their findings for the user''s approval. Use only when the user explicitly invokes /total-review.'
disable-model-invocation: true
source: "https://github.com/davidondrej/skills"
source_repository: "davidondrej/skills"
source_path: "skills/agent-orchestration/total-review/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Total Review

## Workflow

1. **Launch both reviewers in parallel** as two bb threads (default). Follow `/nagent`, `/bb-cli`, and each reviewer skill:
   - One `fable-review` worker (Fable 5 Max 1M).
   - One `gpt-review` worker (GPT 5.6 Sol Max).
   - Follow each reviewer skill exactly: neutral prompt, broad review scope, detailed findings on critical/serious issues, concise plain-English final report.
   - Reuse this thread's environment so both see the same files.
   - If the user names another harness (Cursor Task, cmux, Codex CLI, etc.), use that for both instead.

2. **Wait for both to finish** (`bb thread wait` on each, unless another harness was requested). Do not start triage until both reports are back.

3. **Merge and triage.** Read both reports in full. Then:
   - Combine and deduplicate findings; an issue reported by both counts once.
   - Assess each finding: is it a real bug or risk, or a style preference, theoretical edge case, or non-issue? Agreement alone does not prove an issue is real.
   - Keep only issues that matter.

4. **Output to the user** — clear and very concise:
   - A numbered list of real issues, one line each: what it is + where.
   - Mark which reviewer(s) found each: `[both]`, `[fable]`, or `[gpt]`. Issues found by both go first.
   - One short line at the end: how many findings were dropped as overthinking.
   - Then ask the user: approve fixing these, or adjust the list.

5. **On approval, fix and ship.** Fix only approved issues. Then stage, commit with a clear message, and push to GitHub using the standard ship workflow.

## Rules

- Keep every step's output short and in plain English.
- Show the merged shortlist by default; provide full reviewer reports only if the user asks.
- Never fix an issue before the user approves the shortlist.
