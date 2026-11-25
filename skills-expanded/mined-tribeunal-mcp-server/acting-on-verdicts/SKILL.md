---
name: acting-on-verdicts
description: Use when an outcome is being waited on or has just landed — monitoring a running case, collecting what a jury decided, or driving an action from a ruling. Covers choosing between the waiting tools, reading a verdict correctly including the outcomes that are not decisions, and recording what was done about it exactly once.
---

# Acting on verdicts

Closing a case does not return its verdict; the ruling is attached afterwards. So every flow here is
wait, read, act, record — and the recording is the part that goes wrong, because it goes wrong
invisibly.

## When to use

Once a case exists and its outcome matters. Creating the case is `deciding-with-a-jury`; voting on
someone else's is `serving-jury-duty`.

## Checklist

- [ ] Pick the waiting tool from the table below — they are not interchangeable
- [ ] Read the verdict as a decision tree, not as a winner
- [ ] Act on the ruling
- [ ] **Before recording anything: read the existing comments**
- [ ] Record what was done, once, naming the decision it answers

## Which waiting tool

| You want | Tool | Shape |
| --- | --- | --- |
| The final ruling | `tribeunal_await_verdict` | State-based. Returns immediately if the case is already settled |
| To follow a case as it runs | `tribeunal_await_case_activity` | Cursor-based feed of comments, votes and marks |
| A snapshot now, no waiting | `tribeunal_get_case` | One read — it already carries `totalVotes` and each side's `votePercentage`, no separate stats tool |
| A dispute's ruling across appeal rounds | `tribeunal_await_ruling` | State-based on the dispute document, not a case cursor; honours `nextCheckAfter` |
| To recompute a ruling instead of trusting it | `tribeunal_verify_ruling` | One read against the published signer and log; always `independent:false` |
| To be told, without asking | Webhooks | See `wiring-webhooks` |

Long polls have a server-side ceiling and return before it if something happens. A return is not a
failure.

## Re-arm

`tribeunal_await_case_activity` hands back a `latestCursor` on every response, including empty ones.
Pass it to the next call and the feed is gapless. Stop when the case is past its end — a closed case
produces no further activity and waiting on one waits forever.

`tribeunal_await_verdict` re-arms only while the case is genuinely still running. Two answers are
terminal and mean stop, not retry: a verdict, and the notice that the case has not opened yet
because its jury is still filling. That notice will not change on its own.

`tribeunal_await_ruling` re-arms the same way: `final` is terminal, and so is `provisional` under
the default `until` — re-arm on `nextCheckAfter`, never before it.

## Reading a verdict

Work down, and do not skip to the winner.

1. **Is it decided?** If not, it is one of two different things.
2. **Is there a void reason?** A void case failed a rule — it did not reach the required turnout, or
   it did not reach the required level of agreement. That is not a tie and not a narrow result. It
   is no ruling at all, and reporting it as one is the worst failure available here.
3. **Undecided with no void reason** is a genuine tie or an empty case.
4. **Decided** — read the winning side, and the breakdown if who voted matters.
5. **Check the version** if the case may have been re-run. A superseded verdict is not current.

Never present a percentage from a void case as a result. "100%" of one vote when five were required
is not a mandate; it is a case that failed.

## Receipt

Acting on a ruling and leaving no trace on the case means the next process cannot tell the work was
done — and something else acting on the same verdict is the normal case here, not the exotic one. A
webhook and a poller both firing is exactly what these tools are for.

So the record is idempotent by construction:

**Read the case's comments first. If one already answers this decision, stop — do not post a second.**

Comments are accepted on a case in any state, including after it closes, so there is never a reason
to skip this.

### Worked example

The verdict comes back decided, winning side "Refactor", decision `01a066b1-ce82-763a-838e-…`, on
case `03389f81-…`. `tribeunal_list_comments` shows no comment mentioning that decision. You have
already scheduled the refactor. Post exactly this:

> **Acted on decision `01a066b1-ce82-763a-838e-…`** — jury ruled **Refactor** (7 of 9).
> Scheduled as PLAT-412, starting the sprint of 15 September. No rewrite work will be commissioned.
> Recorded automatically by the integration that requested this ruling.

The parts that matter: the decision identifier, so a later reader can tell *which* ruling this
answers; the outcome as the jury stated it; what was actually done; and who wrote it. A comment
saying "done" satisfies nobody and cannot be recognised as already-present on a second pass.

## Closing early

`tribeunal_close_case` ends a case before its deadline, for the owner or an admin. It reports that a
decision is pending, not the decision. Wait for the verdict afterwards like any other case. On a
case bound to arbitration rules the owner cannot close early at all — see `arbitrating-a-dispute`.

## Gotchas

| Trap | What is true |
| --- | --- |
| A case reported `open`, so it is still running | It stays `open` past its deadline until the close job runs |
| No verdict means the jury tied | It may instead have failed quorum or a requirement |
| The close response carries the ruling | It carries "pending" |
| Waiting on a case that has not opened will eventually work | It will not. The jury has to fill first |
| One process, one action, so recording is safe | Recording without reading first is how two receipts happen |
