---
name: triage-todos
description: Collects to-do comments and open issues, then sorts them into do now, later and drop with a short reason for each.
disable-model-invocation: true
---

Triage the open TODOs in: $ARGUMENTS (whole repo if empty).

1. Search with `rg -n "T[O]DO|FIXME|HACK|XXX"` excluding vendor, build and lock files. Record file, line and text.
2. For each, check age and author with `git blame -L <line>,<line> <file>`. Check the surrounding code: has the condition it mentions already changed?
3. If the arguments say "with issues" and gh is available, run `gh issue list --state open --limit 100 --json number,title,labels` and match issues to comments by keywords.
4. Sort into:
   - **Do now**: touches security, data loss, wrong results, or blocks a release.
   - **Later**: real but low risk. Group by theme.
   - **Drop**: obsolete, already done, vague, or older than the code it describes.
5. Give each item one line of reasoning and the evidence (blame date, matching issue).

Show counts per group, the do-now list in full and the other groups as short tables. Ask whether to delete the Drop comments and whether to draft issues for Later. Change nothing before the answer.
