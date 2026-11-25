---
name: squad-reviewing-as-disprove
description: When acting as a reviewer agent, attempt to empirically disprove each finding before reporting it. Run the test, read the file, check the assertion. False-positive findings poison the team's trust in the ledger.
allowed-tools:
  - Bash
  - Read
  - Task
disable-model-invocation: false
---

# Reviewing as disprove-before-report

You are a reviewer agent. The author has handed you a diff plus their claimed verification artifacts (attestations) and asked for a review. Your job is not to look for problems. Your job is to ATTEMPT TO DISPROVE EACH FINDING you would otherwise report — and only ship the findings that survive that attempt.

This is the Anthropic Code Review pattern. Internal data shows it cuts false-positive review findings to under 1% when applied honestly. False positives are not a free externality: they cost the author time, they erode the reviewer's signal, and they teach the team to ignore review output. The only review worth shipping is the review whose findings you could not disprove.

## When to use this skill

Invoke this skill any time you have been asked to:

- review a diff before `squad attest --kind review`
- approve or block a PR
- assess whether `evidence_required` for an item is genuinely satisfied
- adjudicate a disagreement between two agents on whether code is correct

You should also invoke this skill the moment you catch yourself drafting a finding that begins with "this might be a problem because..." That hedge is the signal that you have not done the disprove-loop yet.

## The disprove loop

For each finding you are tempted to write:

1. **State the finding as a falsifiable claim.** Not "the error handling looks weak." Say: "if input X is passed, function F will panic because branch B is missing." Findings that cannot be made falsifiable are not findings — they are aesthetics, and aesthetics belong in style guides not review reports.

2. **Construct the disproving evidence.** What would you need to observe to know the finding is wrong? A test that exercises X and does not panic. A read of branch B that shows the case is handled. A run of the existing test suite that shows the function does not panic on X.

3. **Go get the disproving evidence.** Read the file. Run the test. Inspect the attestation file under `.squad/attestations/<hash>.txt` if the author claimed they ran a verification. If the disproving evidence exists, the finding does not ship — drop it.

4. **If the disproving evidence does not exist, ship the finding** with the exact reproduction steps you tried, so the author can either run them and see the same failure or tell you why your reproduction is wrong. A finding without reproduction steps is uncheckable; it is overhead for the author and noise for the next reviewer.

## What "go get the evidence" means in practice

- **Read the relevant file.** Don't trust the diff context. The diff shows what changed, not what surrounds it. The bug you are about to report may be answered by code three lines outside the diff hunk.
- **Run the relevant test.** If the finding is "the new code breaks test X," go run test X. If you cannot run it (sandbox limit, missing dep), say so explicitly in the finding — "I could not run test X locally; would you confirm it still passes" — rather than asserting it breaks.
- **Verify the attestation hash.** If the author shipped an `attest --kind test` row, locate the file, re-hash it, and confirm it matches the recorded hash. A mismatch means tampering or stale evidence; both are blocking findings on their own.
- **Check the assertion against the spec.** If the finding is "this contradicts the spec section S," open `.squad/specs/<NAME>.md` and quote section S. If the spec is silent on the matter, the finding is not "contradicts the spec" — it is "spec is silent; author chose X; reviewer would have chosen Y." That is a discussion, not a blocking finding.

## Running reproductions without harming the host

Running tests is part of the review, but the review shares its host with every
other session. Load, timing or flake reproductions follow these limits:

- Run them in isolated temporary state, never against a shared server, ENV or
  another session's worktree.
- Start every background, stress or long-running reproduction through the
  `bounded_run.py` from the installed Squad skill package (`workspace/agent-loop/bounded_run.py`): `bounded_run.py --owner <your id> --timeout
  SECONDS --cpu-seconds SECONDS [--record FILE] -- COMMAND`. It keeps the whole
  tree in one owned process group and ends it on exit, timeout, interrupt or a
  crash of the runner; RLIMIT_CPU caps each process. Never start a CPU load
  generator (`yes`, busy loops, `stress`) or a `&`/`nohup` background job
  outside it, and never use more parallel burners than the reproduction needs.
- Keep the budget small (seconds to a few minutes) and prefer a deterministic
  reproduction (an injected delay, a fake clock, `-count`) over host pressure.
- Before reporting, confirm the runner's report shows the tree ended. Clean up
  only processes you started, by their recorded PID or process group; never by
  name, pattern or port.
- If the reproduction genuinely needs more CPU than a bounded run on the shared
  host, state that limit in the finding instead of loading the host.

## Recording the review

When the disprove loop concludes, record the review with `squad attest --kind review --reviewer-agent <your-id> --findings-file <path>`. The findings file must declare:

- `status: clean` (no blocking findings survived the disprove loop) or `status: blocking` (findings did survive)
- `disagreements: <N>` — number of times you and the author disagreed during the back-and-forth
- `resolution: <accepted|rejected|pending>`
- A `---` separator
- The finding bodies, each with reproduction steps

`status: blocking` records exit_code 1 in the ledger and the item cannot reach `done` until either the findings are resolved (re-review with `status: clean`) or the author overrides via `squad done --force` — the override is itself recorded as a manual attestation.

## Anti-patterns to avoid

- **Listing the diff back to the author.** "You added function F. F has these arguments." If you can't say something the diff doesn't already say, you have not reviewed.
- **Stylistic findings dressed as bugs.** "Variable name `x` is unclear" is not a bug. If you have style preferences, file them as suggestions, not blockers; mark them clearly.
- **Findings that begin with "consider."** Consider-style findings are reviewer wishes, not bugs. They cost the author cycles for zero correctness benefit.
- **Skipping the disprove loop because the finding "feels obvious."** The findings that feel obvious are the ones most likely to be wrong; you have not done the work to know whether the surrounding code already handles the case you are flagging.
- **Reporting "couldn't run the tests, so this might fail."** Running the tests is part of the review. If the sandbox prevents it, say so explicitly; do not promote your inability to test into a finding.

## Why this matters

The evidence ledger is squad's load-bearing primitive. Reviewer attestations sit in the ledger alongside test attestations. A reviewer attestation that ships unfalsifiable findings is a corrupted ledger entry — future agents reading the ledger to decide "is this item really done" cannot tell whether the review found a real problem or a phantom. Once that gap exists, the ledger is no better than a chat log: pleasantly suggestive, operationally useless.

The disprove loop is what makes review output as durable as test output. Tests pass or fail by re-running the bytes. Reviews pass or fail by re-running the disprove loop. Both leave evidence the next agent can verify. Without the loop, review is opinion; with the loop, review is evidence.
