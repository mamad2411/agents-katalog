---
name: rule-review
description: Audit how often claudzilla rules slip, from local transcripts; optionally share the counts (no text) as a GitHub issue.
disable-model-invocation: true
---

# Rule review

1. Run `node ~/.claude/skills/rule-review/scan.mjs --save` (add `--days N` if the user gave a window).
2. Show one table from `report.rules`: rule · applies · slips · hook fires · false fires · Δ slips vs `previous`, the last report over the same number of days (`—` when `previous` is null). Skip all-zero rows. `unparsed` > 0 → say counts may drift. `tableWidth` counts hook fires only; its slips are not counted.
3. Below it: up to 3 rules with the highest slips/applies, one line each with a fix idea (new gate, trigger, wording). No fix idea → say so.
4. Run `node ~/.claude/skills/rule-review/scan.mjs --issue --brief` and show its output verbatim in a ```text block. Say the issue body is the step-2 table without Δ, plus the same numbers as one collapsed JSON line; full body: `scan.mjs --issue`. Ask: share these counts with claudzilla?
5. Yes → run `node ~/.claude/skills/rule-review/scan.mjs --share` and report the issue URL or the fallback link it prints. No → stop; the report stays in `~/.claude/claudzilla-reports/`.

Never add transcript text to the share. Never share without the user's explicit yes to the step 4 question.
