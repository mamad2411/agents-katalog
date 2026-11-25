---
name: Running efficient recurring work
description: >-
  Use when building, running, or auditing any recurring routine or multi-step
  workstream (monitors, digests, briefs, audits), to cut wasted reads, repeated
  checks, and restarts while keeping quality.
---
# Running efficient recurring work

1. **Audit first.** Before changing a recurring job, review up to 5 recent runs. For each step, map its inputs, tool calls, retries, output, and manual fixes. Mark repeated reads, unchanged-source checks, duplicate work, and failures that restarted completed work. Separate observed facts from estimates and mark missing measurements unknown. Fix the biggest waste first and change one thing at a time.
2. **Hand off through files, not chat history.** Keep a short HANDOFF.md (under 400 words) beside the work. It holds the goal, confirmed decisions, file paths, open questions, the next action, and boundaries. Link to evidence instead of copying it. A fresh run reads the brief and handoff first and opens other files only when needed.
3. **Read only what the task needs.** List the exact questions first. Search for the relevant sections, extract only those passages or fields, and keep URLs, dates, units, and qualifiers. Store full originals separately. Never silently truncate evidence.
4. **Don't pay for "nothing changed."** Pick triggers in this order: a narrow event trigger, then a schedule matched to the real deadline, then a cheap change check before any full analysis. Track three outcomes: unchanged, changed, and check failed. A failed check never counts as unchanged.
5. **Give saved results an expiry.** Each saved result records the question it answers, its evidence paths, when it was checked, a refresh rule, and its open unknowns. Before redoing research, reuse the facts that are still current, keep their original check dates, and refresh only the expired parts.
6. **One owner per task.** Before starting, check whether the work is already in progress or done somewhere else. Every handoff includes output paths, evidence, checks done, and open issues. Workers write to separate files.
7. **Limit failures.** Save progress at each step boundary. Allow at most two tries at the same failing operation, and make the second try only with a specific change. Before retrying an action that creates something, check whether the first try already succeeded. If it still fails, record the exact error and the smallest next step, finish the rest of the work, and on resume retry only the unfinished part.
8. **Define done as a checklist.** Before starting, list what must be true for the result to be usable. After drafting, mark each check PASS, FAIL, or UNKNOWN, with its evidence. Make one correction pass on the failures. If anything still fails, return NEEDS REVIEW with the exact issue rather than calling it complete. A bot saying "verified" isn't evidence.
9. **Measure.** Keep a run log with one row per assignment: id, status, source outcome, retries, correction passes, usage (or unknown), and evidence path. Compare versions on the same inputs against the same checklist, and keep a change only if quality holds.
10. **Connectors before browser.** Use a connector or CLI when one exists. The box's browser logins are shared by every bot, so use the browser only when there's no connector, or when a connector read costs money and the browser is free. At a login, 2FA or CAPTCHA, stop and ask once instead of retrying.

## Trim long output (bot-skills#40, Adam GO Nov 2, 2026)
Before reading long tool or log output, trim it, but always keep the error lines and the tail of the output. Kill rule: revert this if any bot misses a fact it needed because the output was trimmed.
