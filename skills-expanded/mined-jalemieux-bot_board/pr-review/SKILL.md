---
name: pr-review
description: Review one pull request on Forgejo like the lazy senior developer who gets paged when it breaks, post the verdict to the human who merges, and turn every correction from them into a written review standard.
---

# PR review

The review method here follows the `ponytail-review` skill (MIT), fitted
to the fleet's forge and board.

A review thread names one pull request. Your job ends when the forge holds
your review, the thread holds your one-line verdict, and the human who merges
has what they need to decide. Their corrections become rules in the knowledge
base, so the next review starts from what they taught you, not from scratch.

Order of importance: correct, safe, holds under load, tested, fast, lean.
Lean still matters: every extra line must be read, tested and fixed later.

The forge plumbing (the `fj` helper, `$FORGEJO`, `$REPO`, `$FORGEJO_TOKEN`,
how events reach threads) is in the `forgejo-lifecycle` skill. Use the same.

## 1. Understand first

1. Read the review standards: `GET $BOARD/api/knowledge/review-standards.md`.
   They are what the human who merges has already told the fleet. Apply them
   first; your own judgement comes after. A rule there that your finding
   would contradict wins, unless the case is one the rule did not foresee:
   then say so.
2. Read the pull request and its issue on the forge: title, body, `Closes #n`,
   and the board thread it came from (its `thread:<id>` label, or the link in
   the body). That thread holds the asks and the decisions behind the change.
   The question is "does this do what was asked, and nothing else", so know
   what was asked.
3. Check out the branch in a worktree of your own. Never push to it.
4. Read the diff, then the code it touches: callers of every changed function,
   the functions it calls, the tests, the docs it should have changed. Trace
   the real flow: where data comes in, what is stored, what goes out.
5. A change can break code it does not touch. When a signature, return value
   or behaviour changes, grep every caller.
6. Find the load this repo expects (README, deploy config, the knowledge base):
   one person running a script, or many bots and boxes at once. Judge scale
   against that, and say which load you assumed.
7. Run the full test suite the way CI runs it. For a user-facing change, try
   it for real. Note what you could not test.

You do not label the pull request. The receiver posts its events into the
author's thread, the one `thread:<id>` label it honours. A push after a
send-back reaches you as a new review job from the routine.

## 2. Look for

1. **Bug:** wrong result, crash, missed edge case (empty, zero, last item,
   rounding, time zones), a caller broken by the change, a fix applied in one
   caller while the shared function stays broken.
2. **Risk:** security holes (injection, weak randomness, secrets, missing
   checks on input from users or other bots), data loss (errors swallowed,
   writes in the wrong order, no transaction), two versions of the board or
   launcher running side by side and one not surviving the change.
3. **Scale:** fine for one bot, wrong for a fleet: check-then-write races,
   the same work done by every process, lists that only grow, a query per
   item, per-process state that must be shared.
4. **Missing test:** risky new logic (a branch, a parser, security, data
   writes, a bug fix) with no test that fails when it breaks. One good test,
   not coverage.
5. **Speed:** big slowdowns are problems. Small wins are suggestions.
6. **Lean:** code that should not exist or should be smaller: dead code,
   unused options, speculative features; a helper the repo already has (name
   the path); the standard library already does it; an abstraction with one
   implementation; config nobody sets; near-copies that must change together;
   one function doing several unrelated jobs.
7. **Scope:** the change does more than the issue asked, or less. Extra is a
   finding; missing is a finding.

## 3. Check before you report

- Every finding needs a concrete case: "this input or situation leads to this
  wrong result". No case, no finding.
- Re-read the lines and confirm: the caller exists, the value can really be
  empty, the code really is unused.
- A shortcut marked with a `shortcut:` comment that names its limit is a
  decision, not a finding, unless the expected load already crosses it.
- Propose the smallest fix that works. Prefer fixes that delete code. Never
  ask for layers, frameworks or config the problem does not need.
- No style taste, no "consider", no vague worries.

## 4. The review, on the forge

Very simple English: short sentences, everyday words. Explain a technical
term the first time you use it. The reader may never have seen this code.

The first line is your signature, `bot <handle>, board thread <id>`, on a line
of its own, then a blank line. Every bot is the same forge account, and the
board quotes a review's first line into the thread, so this line is how anyone
knows which bot reviewed. Then `What this change does:` in two or three
sentences.

Then the findings in three groups, skip empty groups:
- **Must fix:** bug, security, data loss, breaks at the expected load, does
  not do what the issue asked.
- **Should fix:** risky code without a test, real slowness, duplication, a
  function that mixes jobs, code that should not exist.
- **Nice to have:** small speed-ups, shorter forms.

Number findings across all groups, so the author can say "fixed 2 and 5".
Every finding has four parts, each one or two short sentences:

```
2. **Orders land on the wrong day** (`billing/close_day.py:L40-52`)
   - **What this is:** At midnight this job closes the day and bills all orders of that day.
   - **Problem:** It takes "today" from the server clock, which runs in UTC. An order placed
     at 00:30 in Berlin is billed on the day before.
   - **Fix:** Compute the day once in the shop's time zone. One line, nothing else changes.
   - **If we skip it:** Late orders show the wrong date, and accounting fixes them by hand.
```

End with:
- `Verdict: Ship.` or `Verdict: fix 1 and 3 first.`
- `Lean: -<N> lines possible.` when lean findings exist.
- `Tested:` one line on what you ran and tried.
- `Not checked:` one line, if something mattered and you could not check it.

Nothing found: `What this change does:`, then `Looks good. Ship.` and the
`Tested:` line.

Post it as a comment review, since the shared forge account cannot approve.
Inline comments on lines go through the same call with `comments`.

```bash
fj "/repos/$REPO/pulls/<pr>/reviews" -d "$(jq -n --arg b "$BODY" '{event:"COMMENT", body:$b}')"
```

## 5. The verdict, in the pull request's thread

The pull request has a board thread of its own: the one its `thread:<id>`
label names (or the link in its body). Its author works there, the board
posts the forge's events there, and the human who merges follows it. Your
verdict goes there too, as a reply, so one thread tells the pull request's
story in order, with a handle on every line. The job thread that woke you is
not that place.

One message: the verdict, the link to the review, the `Tested:` and `Not
checked:` lines, and how to reach you. Mention the human who merges (the
workspace's knowledge base says who) and hold the message in their inbox:

```json
{"reply_to": <the PR's thread id>,
 "body": "@<human> Ship: PR #<pr> <review url>. Tested: ... Not checked: ... (I am @<handle>: mention me to correct this.)",
 "meta": {"needs": "<human>", "ask": "merge PR #<pr>", "pr": <pr>}}
```

`pr` is the PR number as a number: when Forgejo reports that PR merged, the board clears the ask from the
human's inbox. For a send-back use `"ask": "send back PR #<pr>: fix 1 and 3 first"`. You are not that
thread's worker, so a plain reply there reaches its author, not you; a
mention of your handle does, which is why the verdict says so.

Then close the job: reply in the job thread with one line, the verdict and a
link to the verdict message, and `"meta": {"done": true}`. Complete the job
thread, so the routine can hand you the next pull request.

## 6. When the human answers

- **They merged, or agreed.** The merge reaches the pull request's thread as
  a forge line; you see it when you look, or when someone mentions you. Post
  `"meta": {"resolved": true}` there if your ask still stands, and add one line
  to the tally in the standards.
- **They corrected you.** This is the point of the skill. It reaches you as a
  mention in the pull request's thread. Say there, in one sentence, the rule
  you take from it. Then write it into the standards
  the same day, with their message id. Do not write a rule they did not give;
  ask one precise question when the correction is unclear. Add the tally line
  with `overruled` and what they said.
- **They sent it back to the author.** You need do nothing. A push to the
  branch fires a new review job, and the new review says which earlier
  findings are fixed, by number, in the same thread as the first verdict.

## 7. The standards document

`review-standards.md` in the workspace's knowledge base. Two parts:

1. **Rules.** One per line, each with its source: `- <rule> (from <message id>)`.
   Grouped by subject: scope, tests, docs, lean, the fleet's load. A rule that
   contradicts an older one is not overwritten: quote both in the thread and
   ask which holds.
2. **Tally.** One line per review: `- #<pr> <date>: <verdict> → <what the human
   did: merged as-is | merged after changes | sent back | overruled> (<thread id>)`.
   This is the human's evidence for when the reviewer may merge on its own.

Write with `base_revision` and a `reason`; on a 409, read again and merge.

## What not to do

- Do not push to the branch, fix the code, merge, approve, or close anything.
- Do not relay the forge's events into the thread; the board does that.
- Do not give a verdict without having run the tests.
- Do not write to the standards without a human's message to cite.
- Do not pad: a review with nothing to fix is three lines.
