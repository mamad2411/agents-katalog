---
name: blueprint-refactor-report
description: "Write up what this campaign changed, how each change was proved, what was not proved, and what was declined and why."
---

# The record you leave

The next person reads this instead of rediscovering it. Write `.blueprint/refactor-report.md` in the language
the build's prompt says the person reads (without one, in Japanese),
from `.blueprint/targets.json`, `.blueprint/spec.md` and the pull requests themselves (`gh pr view <url>`).

1. **Per target**, by its id: what was done, the pull request, how the review went (its `review` field),
   how behaviour was proved (replica over
   generated inputs, driven through a seam, or only the verbatim body — say which), which mutations went red,
   and **what was not proved**.
2. **Declined targets**: the cost written down, and the open question the next attempt has to answer.
3. **Not looked at**: the parts of the repository the survey did not cover.
4. **Candidates left** for a later run, if the survey found more than this run's limit.

Say what moved and how, never by how much. Nothing in this step changes the repository.

Done when the check passes: the report exists and names every target.

## Always

- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
