---
name: pr-feedback
description: Work the reviewer's comments on a pull request — list what is still unaddressed, act on each item (fix it, answer it, or argue with it), and post the replies back so nothing is silently dropped. Use when the user says to address / answer / go through the PR comments or review feedback, when you are about to add to a branch that has an open PR, and as the collect/answer steps of the `ship` skill. Works standalone on any repo with `gh`.
---

# PR feedback — the reviewer's comments are work items

A comment on the PR is a work item exactly like the user's chat prompt. This
skill owns both halves: **collect** before you implement, **answer** after you
push. It never decides *what* the code should do — it makes sure no item is lost.

## Two modes — say which one you are in

Invoked as `/feature:pr-feedback collect` or `/feature:pr-feedback answer`; with
no argument, `collect`. The modes are separated because they belong to opposite
ends of a pass, and running the wrong one is a real failure: `answer` before the
push cites no commit, and a second `collect` after the work re-opens items you
just handled.

| Mode | When | What it does |
|---|---|---|
| `collect` | **before** any code is written — `workspace` Phase 2, or `ship` step 0 standalone | list unaddressed items, decide per item, hand the list back |
| `answer` | **after** the push — `ship` step 4b | one reply per item picked up, each citing the fixing commit |

All plumbing is one script; never hand-roll it with `gh api`:

```bash
SC="${CLAUDE_PLUGIN_ROOT}/scripts/pr_feedback.py"
```

Behaviour is driven by the `pr_feedback` block of the config (`enabled`, `reply`,
`resolve`, `include_outdated`, `include_bots`, `marker`); with no config at all
the shipped defaults apply, so this works outside a workspace too.

## `collect` — before implementing

```bash
python3 "$SC" list --cwd "$WT" [--pr <url>]
```

`--pr` when you know it (a workspace's `.feature.json` records it); omit it and
the current branch's own PR is used. `pr_feedback.enabled: false`, no PR yet, or
nothing unaddressed ⇒ one line of output and **stop here, silently**. A
`gh`/network failure (exit 2) is one line in the report, never a blocker.

A thread is unaddressed when it is unresolved **and its last comment isn't
yours**. Two traps the script already handles — don't reintroduce them by hand:

- `gh` posts as the human's own account, so **the author tells you nothing**;
  the marker in your own replies is the only discriminator.
- **`isOutdated` does not mean handled** — a comment goes outdated the moment you
  push a fix touching that file, so outdated threads are usually the ones just
  worked on. The digest carries the diff hunk for exactly that reason.

On a PR whose earlier replies predate the marker you may see a thread you already
answered; the digest prints the whole thread, so just don't answer it twice.

Then act per item — do what's clear, ask only what genuinely isn't:

| Item | What you do |
|---|---|
| a concrete fix ("extract this into a helper") | implement it in this pass |
| a question ("why like this?") | answer it in the thread; no code change |
| you disagree, or you see a better option | say so **with the argument** — never silently comply |
| out of scope for this task | don't widen the scope silently: answer where it belongs instead |
| genuinely ambiguous | ask it as a numbered question before implementing |

The user's prompt and the PR comments are **one** work list — deliver both. Never
make the user repeat a comment in chat because you didn't look.

## `answer` — after the push

Only **after** the push, so a reply can cite the commit that settles it. Reply in
the user's language (`output_language`), and be honest: agreement is a verdict,
not a courtesy.

```bash
python3 "$SC" reply --thread <thread-id> --body "<verdict + what you did + <sha>>"
python3 "$SC" reply --issue --cwd "$WT" --to <item-url> --body "<answer>"   # review body / general comment
```

The script appends the agent marker — that is what makes the item count as
answered next time — so never hand-roll a reply. A **thread** reply is
self-addressing. A **general** reply is not: it lands in the PR conversation with
nothing tying it to what it answers, so pass `--to <url>` (the `url` field of the
item in the digest). Two review bodies ⇒ two `--to` replies. One unaddressed
`--to` means that item comes back next time, which is the safe direction to fail.

`pr_feedback.reply: on_fix` ⇒ answer only where code changed; `never` ⇒ act on
the comments but post nothing. Resolving follows `pr_feedback.resolve` (default
`never`: you answer, the reviewer resolves); under `on_fix` / `always`:

```bash
python3 "$SC" resolve --thread <id>
```

If `list` printed a `!! GitHub capped …` line, the list was truncated by the API —
say so in the report and open the PR to check the remainder by hand rather than
claiming all feedback is addressed.

## Report back

Whoever invoked you (the `ship` skill, or the user directly) needs two things:

- the counters — `feedback: 5 · fixed 3 · answered 1 · deferred 1`;
- one bullet per item: **where** (`path:line` + a short quote), **your honest
  verdict**, **what you actually did**. Verdicts: agreed · disagreed, with the
  argument · there's a better option, namely … · what's there is justified,
  because … Agreeing with everything is a smell, not politeness.

## Red flags
- Implementing while unaddressed comments sit on the PR → no. Same work list.
- Deciding a comment is handled because it's `isOutdated`, or because "the last
  comment is the author's" → no.
- Answering before the push → no. The reply has to cite the commit.
- Writing "agreed" while leaving the code unchanged, or quietly fixing what you
  told the reviewer was fine → no. Verdict and code must match.
- Posting a general reply without `--to` → no. It answers nothing traceable.
- Reporting "all feedback addressed" after a capped list → no.
