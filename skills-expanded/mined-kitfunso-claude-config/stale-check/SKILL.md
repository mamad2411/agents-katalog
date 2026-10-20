---
name: stale-check
description: Verify a memory file's claims against the repo, git, npm and the live service, and propose the edit. Use for "is this memory still true", "audit my memory", "stale check <project>".
disable-model-invocation: true
---

# Stale check

Memory records what was true when it was written and rots without saying so. The global rule already says to treat any pending-or-broken memory claim older than about a week as unverified. Nothing did the verifying. This is the verifier.

Takes one memory file (or one project), checks every claim that can be checked, and proposes the edit. It never applies it.

## 1. Split the file into claims

Read the file and list every load-bearing claim: a version, a commit sha, a branch, a file path, a function name, a URL, a count, a state word (`SHIPPED`, `BLOCKED`, `LIVE`, `PENDING`, `NOT yet`), a date-relative statement.

Sort each into one of three buckets before checking anything:

- **Checkable now** — something in this session can settle it.
- **Checkable, but not from here** — needs a login, a phone, a paid console. These go to `/human-blockers`, not to a guess.
- **Not checkable** — a preference, a decision, a lesson. Leave these alone. A rule about how to work is not stale because it is old.

## 2. Check the checkable ones

One command per claim, and the command goes in the report so Keith can re-run it.

| Claim shape | How it settles |
|---|---|
| version published | `npm view <pkg> version`, `pip index versions <pkg>` |
| commit / branch / head | `git -C <repo> log -1 --format=%h`, `git -C <repo> branch --show-current` |
| file or function exists | `Read` the path, `Grep` the symbol |
| a service is live | one `curl -s -o /dev/null -w '%{http_code}'` against the URL |
| a count | the query or `wc` that produced it |
| open PR, CI state | `gh pr list`, `gh pr checks` |
| a gate is open | read the `docs/LAUNCH.md` row, not the memory line |

Never settle a claim by reasoning about it. If no command settles it, it is unverifiable, which is a verdict, not a failure.

## 3. Verdict per claim

- **VERIFIED** — the source agrees. Say so and move on; no edit.
- **STALE** — the source disagrees. Give the old text, the new fact, and the command that shows it.
- **UNVERIFIABLE** — nothing here settles it. Say what would.

A memory file where every claim comes back VERIFIED is a good result and takes one line to report. Do not manufacture findings to justify the run.

## 4. Correct and report

Memory files are hand-maintained. Output one block per stale claim:

```
<file>:<line>
  was:  <the current text>
  now:  <the corrected text>
  why:  <command and its output>
```

Then apply each verified correction as a targeted edit and report what changed. Never rewrite the whole file, and do not delete a claim you could not verify: unverified is not the same as wrong.

Update the memory file and `hippo remember` the correction in the same session, per the writeback rule.

## Scope

One file, or one project's files, per run. A sweep over every memory file produces a report nobody reads and burns a session doing it. Run it on the project you are about to work on, at the start, which is also where a stale claim would have cost the most.
