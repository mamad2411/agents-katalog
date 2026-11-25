---
name: bug-triage-protocol
description: Disciplined bug-fixing — reproduce first, isolate by binary search, make the minimal fix, write a regression note. Never fixes what it can't reproduce. Use when the user says "it's broken", "there's a bug", "this stopped working", "it works sometimes", or pastes an error and wants it fixed. Don't use for verifying a deploy that just went out — use vercel-deploy-check.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Builder Dev, Debugging, QA, Triage]
    related_skills: [api-endpoint-tester, github-pr-review, git-ship-flow, vercel-deploy-check]
---

# Bug Triage Protocol

The anti-flail system for debugging. Rule zero: **never fix what you can't reproduce** — a "fix" for an unreproduced bug is a guess, and guesses in production are how one bug becomes three. This protocol runs reproduce → isolate → minimal fix → regression note, in that order, every time.

## When to Use

- Anything is "broken", "erroring", "not working", or "working sometimes".
- An AI builder shipped a change and something else stopped working.
- User is tempted to prompt "fix all the bugs" at a codebase (this protocol is why not to).
- **Not for:** post-deploy site verification — use `vercel-deploy-check`. Not for systematic endpoint sweeps when nothing is known-broken — use `api-endpoint-tester`.

## Quick Reference

| Action | Command / Call |
|---|---|
| What changed recently? | `git log --oneline -15` and `git diff HEAD~5 --stat` |
| Binary-search history | `git bisect start; git bisect bad; git bisect good <sha>` then test + `git bisect good\|bad` each step; `git bisect reset` when done |
| Reproduce an API bug | `curl -si https://app.com/api/thing -H "Authorization: Bearer $TOKEN"` |
| Watch live logs | `vercel logs <url>` / `tail -f logs/dev.log` / browser devtools console |
| Test one hypothesis | comment out / stub the suspect, re-run the repro |
| Save the repro | `repro/<date>-<bug>.md` — steps, expected, actual |

## Procedure

1. **Precheck** — capture the report verbatim: what did you do, what did you expect, what happened instead, when did it last work? Grab the exact error text/screenshot. If the answer to "when did it last work" is known, half the isolation is already done.
2. **Reproduce** — make the bug happen on demand, then write the shortest step list that triggers it and run it twice to confirm it's deterministic. Flaky? Note the conditions (specific account, empty data, slow network, browser). **If you cannot reproduce it, stop here** — instrument instead: add a log line at the suspected site, ship that, and wait for the bug to report itself. Do not "fix" anyway.
3. **Isolate by binary search** — halve the search space repeatedly, in whichever dimension fits:
   - *Time:* `git bisect` between the last-good commit and now — a few test runs finds the exact commit even across hundreds.
   - *Code path:* does the API return correct data (`curl` it directly)? Yes → bug is frontend. No → bug is backend. Repeat inside the guilty half.
   - *Data:* fails for one user, works for another → diff the two accounts' data (nulls, empty lists, weird characters).
   Success: one sentence — "the bug is in X because Y."
4. **Minimal fix** — change the fewest lines that correct the root cause. Not a refactor, not a cleanup, not "while I'm here." If the diff touches files unrelated to the one-sentence cause, you're fixing the wrong thing or doing too much — shrink it. Fix on a branch (`git-ship-flow`), never live on main.
5. **Verify both directions** — the repro steps now pass, AND the features nearest the change still work (run the 2–3 adjacent flows). A fix that breaks something else is a new bug with your name on it.
6. **Regression note** — 4 lines, saved to `repro/` and pasted into the PR/commit body (template below). This is what makes the same bug cheap the second time it's attempted.

## Output Template

```
## Bug: <one-line symptom>
Repro: <numbered steps — shortest version>   Deterministic: yes / flaky (<conditions>)
Root cause: <one sentence — the X because Y>
Introduced by: <sha/PR, if bisected>
Fix: <files:lines changed and why this is minimal>
Verified: repro passes ✅  adjacent flows checked: <list> ✅
Regression note: "If <symptom> returns, check <place>; it happens when <condition>."
```

### Severity call (when multiple bugs compete)

| Severity | Definition | Response |
|---|---|---|
| P0 | Data loss, security hole, app down for everyone | Drop everything; consider rolling back the deploy first (`vercel-deploy-check`) |
| P1 | Core flow broken for many users, no workaround | Fix today, protocol in full |
| P2 | Broken but workaround exists, or affects few users | Queue it; still write the repro file now while it's fresh |
| P3 | Cosmetic, typo, polish | Batch with the next release |

## Pitfalls

- **Fixing the symptom at the crash site** — the null-check where it *threw*, not where the null was *born*. Recovery: walk upstream — why was the value null? Fix the source; add the guard as defense, not as the fix.
- **Can't reproduce, "fixed" it anyway** — the classic. The change either does nothing or breaks something, and you've lost the trail. Recovery: revert the speculative fix, add targeted logging at the suspect site, redeploy, and wait for real evidence.
- **Shotgun debugging** — five changes at once, bug gone, no idea which change did it (or which broke something else). Recovery: `git stash`, re-confirm the repro, reapply one change at a time, re-running the repro after each.
- **Flaky bug declared fixed after one green run** — it was always intermittent. Recovery: run the repro 10 times (or loop the curl); "fixed" means 10/10, or means you understand exactly why the failing condition can no longer occur.
- **Bisect left half-finished** — repo stuck on an old commit, everything looks broken. Recovery: `git bisect reset` returns to where you started; nothing was lost.

## Verification

- [ ] Bug reproduced on demand before any code changed (or explicitly instrumented-and-waiting, with no fix shipped)
- [ ] Root cause stated in one sentence with evidence
- [ ] Diff is minimal — every changed line maps to the root-cause sentence
- [ ] Original repro steps now pass; adjacent flows re-checked
- [ ] Regression note written and saved to repro/ + PR body
- [ ] `git bisect reset` ran if bisect was used
