---
name: orchestra
description: Routing policy for a coding agent that can hand work to other models: Claude tiers (Opus, Sonnet, Haiku), OpenAI GPT through the Codex CLI, Kimi and DeepSeek through the Kimi Code CLI. Decides who does a job, how to brief it, how to run it safely (one runner, hard status gates, worktree per writing lane) and how to check the answer before using it. Load before spawning any sub-agent or external model lane.
---

# Orchestra

You are the conductor. You plan, write briefs, review and merge. Other models play the parts.
The conductor's time is the most expensive in the room, so it should not play the long, plain parts itself,
and it should never pass on an answer it has not checked.

## 1. Should this be delegated at all?

Do it yourself when any of these hold:
- It takes fewer steps than writing the brief would.
- It needs the conversation's context that you cannot write down in a page.
- It touches secrets, credentials, production systems, or anything irreversible.
- The user is waiting on a quick answer.

Delegate when the job can be described in one self-contained brief and checked from the outside
(tests, a diff, an exact answer, a schema).

## 2. Who plays what

Pick the cheapest lane that will pass the check. Move up only when a lane fails the check, not on a hunch.

| Job | First choice | Brief style | Fallback |
|---|---|---|---|
| Hard design, tricky bug, unfamiliar code | Claude Opus (sub-agent) | Goal + constraints, let it plan | gpt-6.1-sol, effort high |
| Routine feature, clear bug, refactor with tests | Claude Sonnet (sub-agent) or gpt-6.1-sol | Steps, files, done-check | Kimi k3.1-pro |
| Well-specified execution on the GPT side | gpt-6.1-sol | Numbered steps, exact files, exact check | Kimi, DeepSeek v4-pro |
| Second opinion, "what are we missing" | gpt-6-astra (read-only) | The question + the evidence, ask for disagreement | DeepSeek v4-pro |
| Third opinion from another family | DeepSeek v4-pro (read-only) | Same as above | Kimi |
| Cheap execution of easy, testable work | Kimi k3.1-pro or DeepSeek v4-pro | Very explicit steps | gpt-6-luna |
| Bulk mechanical work (labeling, renames, data cleanup) | Claude Haiku, gpt-6-luna or deepseek-flash | Rules + format + examples | Next bulk lane |
| A decision with no single right answer | Council (3 lanes, blind) | Same question to all | Ask the user |

Measure your own stack: `bench/run.sh` scores each lane on a write task with hidden tests,
an exact-answer reasoning task and a bulk labeling task. Re-route when the numbers say so.

## 3. Brief rules

A lane sees only the brief. Write it so a stranger could do the job.
- First line: the outcome, in one sentence.
- The files it may touch, and the ones it must not.
- The exact check it must run and pass (a command, not "make sure it works").
- Out of scope: commits, pushes, new dependencies, edits to tests, anything you would not accept in review.
- The last line it must print: `DONE` or `FAILED: <reason>`.
- Never put secrets, tokens or personal data into a brief. Briefs go to other vendors.

Templates: `templates/execute.md`, `templates/opinion.md`, `templates/bulk.md`.

## 4. Running a lane

Always go through `scripts/mmo-run`. It is the one place where the safety rules live:

```bash
scripts/mmo-preflight                       # offline: which lanes are installed
scripts/mmo-run codex   -m gpt-6.1-sol -e high --mode rw -C ../wt-auth --brief brief.md --out out/auth.md
scripts/mmo-run deepseek -m deepseek/deepseek-v4-pro --mode ro --brief q.md --out out/ds.md
```

- `--mode ro` for anything that only reads. `--mode rw` refuses to run outside a linked git worktree,
  so a writing lane never edits your main checkout. Make one worktree per writing lane.
- Every run has a timeout, no stdin, and an output file whose first line is a status header:
  `<!-- mmo provider=… model=… mode=… status=ok|failed|timeout|empty|limit|auth|model exit=… seconds=… -->`
- Exit codes: 0 ok, 2 usage, 3 failed, 4 timeout, 5 empty, 6 limit/balance, 7 auth, 8 model (id rejected).
- Run independent lanes in parallel. Wait for all of them before you judge any.

## 5. Gates before you use an answer

1. Status header says `ok`. Anything else is not an answer. Do not read meaning into a failed lane.
2. The lane's own check passed, and you re-ran it yourself. A lane saying DONE proves nothing.
3. For writing lanes: read the whole diff. Reject edits outside the allowed files, deleted or weakened tests,
   new dependencies, and silenced warnings.
4. For opinions: weigh arguments, not votes. Two models agreeing is a hint, not proof.
5. Merge one lane at a time; run the full test suite once after the last merge.

## 6. When a lane fails

- `limit` (quota, balance, 429): switch to the fallback column. Do not retry the same lane in a loop.
- `model` (unknown or unsupported model id, e.g. model_not_found): switch to a model id the CLI accepts, or the fallback lane. Waiting for a reset will not help.
- `auth`: tell the user which CLI needs a fresh login. Do not try to log in for them.
- `timeout` or `empty`: shrink the brief or split the job, then retry once.
- Same lane fails twice on the same check: move one step up the table, with the failure output in the new brief.
- Never hide a failure in the final report. Say which lane failed, why, and what replaced it.

## 7. Council

For decisions where reasonable models disagree, use the `council` skill: the same question to three lanes
from different families, read-only, answers shuffled and anonymized before you judge them.
