---
name: reviewgate
description: Use for code review against the team's OWN standards — before finishing any coding task, before git push, and whenever asked to "review changes", "check against team rules" or "run the review". Drives the ReviewGate MCP tools get_team_rules and review_changes; the same judge and the same rules that check the merge request. If the tools are missing, use the reviewgate-setup skill first.
---

# Review the changes with the team's standards

ReviewGate reads the agreements the team actually wrote — the rules in
`.reviewgate/config.yml` of the project — and reports where the current change
breaks them. A finding that quotes the team's own rule is one a reviewer acts
on; a finding that quotes a textbook is one they scroll past.

## The two tools

1. **`get_team_rules` — call it BEFORE writing code**, instead of reading the
   ADRs by hand. It returns the team's rules, the preset and the ignore
   patterns for this repository. Code written with the rules in front of you
   passes review; code reviewed after the fact gets rewritten.
2. **`review_changes` — call it BEFORE declaring work done and before
   `git push`.** It reviews the working tree changes with a generator pass and
   a judge pass — the same pipeline that will check the merge request, so
   passing here means passing there.

## Reading the result

- Findings carry severities `blocker / critical / major / minor / info` and an
  overall gate verdict. Fix blockers and majors; then run `review_changes`
  once more to confirm the fix — one re-run, not an endless loop.
- A finding you believe is wrong for THIS code is a conversation with the
  human, not something to silently ignore: show it and say why you disagree.
- Reviews spend the user's own model key. Do not spam re-runs; batch your
  fixes, then verify once.

## When the tools are not available

The MCP server needs the `reviewgate` binary on PATH and a model key in the
user config. If the tools are absent or the server fails to start, switch to
the `reviewgate-setup` skill — do NOT imitate a review with your own reading
of the diff: an imitation looks like a review but carries neither the team's
rules nor the judge.
