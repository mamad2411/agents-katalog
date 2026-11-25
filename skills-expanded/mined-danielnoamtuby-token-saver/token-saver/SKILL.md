---
name: token-saver
description: Cost-and-context discipline for any session: reach the same verified result with fewer input tokens, fewer tool round-trips and fewer messages. Use when the user says "save tokens", "be cost effective", "keep it cheap", or starts a long multi-step session where cost compounds.
---

# Token saver

Two goals, in this order:

1. **Spend the fewest tokens that still gets the job actually done and
   verified.**
2. **Make the output worth reading** — a cheap session that hands back a vague
   summary just moves the cost onto the human, who now has to re-derive what
   happened. Keep the final report specific: what changed, what was verified, what is left.

Cheapness is never an excuse to skip verification the task genuinely requires,
to guess at a file's contents, or to hedge instead of answering. **If cutting
cost would make the work wrong, spend the tokens and say why.**

## Where the tokens actually go

Cost is dominated by **input re-sent on every turn**, not by what you write.
Every file you read stays in context for the rest of the session and is
re-billed each turn. The expensive mistakes, in order:

| Mistake | Why it's expensive |
| --- | --- |
| Reading a whole file to use 10 lines | The full file is re-billed every subsequent turn |
| Re-reading a file you just read or edited | Pure duplicate — the edit already succeeded or it would have errored |
| Screenshots / `read_page` when text would do | Images and DOM trees are huge and mostly noise |
| Polling a slow job in a tight loop | Each poll is a full turn: system prompt + all context + result |
| Narrating a plan, doing it, then re-summarizing | Three payloads for one unit of work |
| Dumping raw command output into the reply | The user re-reads what you already read |

## The cheap path, in order

**1. Locate before you read.** Grep with `-n` and a small `-C`, or glob for
names. Get line numbers first, then read only those ranges (`sed -n '120,180p'`,
or Read with `offset`/`limit`). Reading a 2000-line file to change one function
is the single most common waste.

**2. Prefer the cheapest surface that answers the question.**

```
CLI / API / JSON endpoint  ->  filesystem (grep, git)  ->  rendered UI / browser
cheapest ─────────────────────────────────────────────────────► most expensive
```

`git diff --stat` before `git diff`. `git log --oneline -10`, never bare
`git log`. `curl` piped through a `node -e` projection of the three fields you
need, not the whole object. **Shape the output in the command** — `head`,
`wc -l`, `--name-only` — rather than reading it all and ignoring most.

**3. One tool call per message, but make each call carry more.** The user
wants work done one by one, never as parallel tool calls. Save the round trips
inside the call instead: `cmd1; cmd2; cmd3` in one shell call beats three
calls, and one grep with an alternation (`a|b|c`) beats three greps.

**4. Don't re-verify what the tool already told you.** An Edit that returned
success wrote the change. A CI/checks pass that reports green *is* green — if
you don't trust it, fix the check rather than hand-verifying forever. Re-read a
file only when something *else* may have changed it.

**5. Don't poll.** Use a blocking wait if one exists, a background task, or a
scheduled wakeup with **one** status check per wake. A 10-minute job checked
every 30s costs 20 full turns to learn one boolean.

**6. Delegate only when it actually saves.** A subagent (or any delegated sub-task) is worth it when the
work would otherwise dump a lot of junk into *your* context and you only need
the conclusion — broad searches, "which of these 40 files does X", sweeping
audits. It's a loss for a single known lookup, or when you'd re-read the same
files afterwards anyway. **Never spawn a subagent and also do the search
yourself.** Don't launch subagents or workflows unless the task warrants it or
the user asked.

**One subagent at a time.** Parallel subagents each start a fresh context and
bill their own input, so a fan-out spends several sessions' worth of tokens in
one burst. Run delegated tasks one after another, and fan out only when the
user explicitly asks for parallel work or a workflow.

**Give the subagent the cheapest model that can do the job.** Default to a
model below the session's own, and step up only when the task needs it:

| Delegated task | Model |
| --- | --- |
| Search, lookup, "which files do X", collecting facts | smallest / fastest tier |
| Routine, well-specified edits, tests or summaries | mid tier |
| Hard reasoning, design trade-offs, subtle debugging | one tier below the session |
| Judgment that genuinely needs the session's own level | same model, with the reason stated in a clause |

Never pick a model *above* the session's. If a cheaper model returns a wrong
or thin result, redo it one tier up rather than retrying at the same tier: a
failed cheap run costs more than it saved. A named agent type that fixes its
own model keeps it.

**7. Stop when the answer is reached.** Extra confirmation passes, extra "let me
also check", and speculative refactors are pure spend. Scope creep is a token
cost as well as a review cost.

## Fewer, denser messages

- **No preambles.** Don't announce what you're about to do and then do it.
- **No progress narration** between tool calls, unless the user is waiting on a
  long operation and needs to know it's alive.
- **No restating the plan** after executing it — the final report covers it.
- **No pasted tool output.** Quote the one to three lines carrying the finding.
- **One batched round of questions, or none.** If a sensible default exists,
  take it and say so in a clause. Blocking on something you could answer from
  the repo costs a round-trip *and* the user's attention.
- **One correction, once.** Don't re-audit your own earlier phrasing.

## When not to optimize

Spend freely on:

- reading the code you are about to change;
- the manual or visual verification a task explicitly requires;
- understanding an unfamiliar system before editing its hot core;
- reading a diff before merging it.

Skimping there produces rework, which costs far more than the read would have.
