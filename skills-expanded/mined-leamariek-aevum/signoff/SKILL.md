---
name: signoff
description: Summarise an Aevum block that is ready for sign-off and record the user's approve or reject decision.
disable-model-invocation: true
argument-hint: <BLOCK_ID> [approve | reject <reason>]
---

Sign-off is the founder's decision. You prepare the evidence and write the
file only when the user's own message carries the decision.

1. From `logs/blocks/<BLOCK_ID>/progress.jsonl`, find the latest
   `block_ready_for_signoff` and its `integration_sha`. Confirm
   `git rev-parse block/<BLOCK_ID>/integration` matches. If there is no
   such event, say what state the block is in and stop.

2. Summarise in a few lines: clusters closed, the block-close gate
   verdicts (`logs/gates/gate1-delta.json`, `gate2.json`, `gate3a.json`,
   `gate3b.json`), fix-loop iterations, open gate3b warnings, and
   `git diff --stat <base_sha>..<integration_sha>`.

3. If the arguments say `approve` or `reject`, write exactly one of
   `logs/blocks/<BLOCK_ID>/signoff/SIGNED.md` or `REJECTED.md` with the
   founder's name (ask; suggest `git config user.name`), the UTC date, the
   integration SHA, and either `approved` on its own line or the reason.
   Without a decision in the arguments, stop after the summary.

4. After an approval, give the human-only next step as commands for the
   user to run: fast-forward `main` to the integration branch. Never run
   it yourself, and never push.
