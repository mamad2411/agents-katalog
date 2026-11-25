---
name: verify-approval-guard
description: Use when a change touches the approval guard (D27, D31): guard.rs, the batch loop and guard_* functions in actor.rs, guarded / guarded_batch / call_guarded / held_batch in mcp.rs, run_batch in commands.rs, or the rig in tests/support/guard_rig.rs. Runs a property test over generated batches, human answers, ask categories, protocol versions and Mrtr retries, and says whether a tap that spends money or deletes can reach the device without the human's answer.
---

# Verify the approval guard

**Promise.** A tap, or `type --submit`, on a button that spends money, deletes an account, or is in a category the human opted into (`PHONEDRIVER_ASK`) never reaches the device without the human's answer through MCP elicitation, unless `autonomous` or `PHONEDRIVER_GUARD=off`. `Allow` covers exactly the one held step. `Allow for this session` covers that category only. Decline or dismiss taps nothing. In a `batch`, the steps before a held step run once, the held step runs at most once and only after Allow, and the batch goes on from the held step. On protocol 2026-07-28 a stale or mismatched retry never taps a guarded step.

**Harm if it breaks.** An agent places an order, sends money or deletes an account on someone's phone without their word.

## Tool, and why

Property-based testing (proptest) of the real code, not a model of it. Everything under test is the real daemon, the real `Mcp` server and the real `FakeDevice` log: the question here is whether the code behaves for every generated input, not whether events can interleave badly in a design, so a TLA+ model of a hand-copied state machine would check the copy. The oracle (`Model` in `crates/cli/tests/guard_property.rs`) is a 30-line re-statement of the promise above and shares no code with `mcp.rs`. Nothing to install: `proptest` is a dev-dependency of `crates/cli`.

A TLA+ model of `held_batch` was considered and not written: the retry state is one slot keyed by the batch's arguments, and the second property drives the real slot with random interleavings (see Bounds).

## Coverage record

| Check | What it drives | Code it covers |
|---|---|---|
| `a_guarded_step_reaches_the_device_only_after_the_humans_answer` | 1 to 3 calls (`batch` of 1 to 5 steps, `tap`, `type --submit`, optionally `autonomous`) with a scripted human (allow, session, decline, cancel, bare accept, junk, none) and an ask set, on 2025-11-25 (human asked over the open connection) and 2026-07-28 (question returned, client calls again). Compares the fake device's input log and the prompts shown against the oracle. | `guard.rs`: `classify`, `guarded`, `asks`, `stance`, `submit_button`. `actor.rs`: `guard_tap`, `guard_submit`, `guard_button`, `batch` (the `i == 0` approval rule). `mcp.rs`: `guarded`, `guarded_batch`, `call_guarded`, `decision`, `commitment`. `commands.rs`: `run_batch`. |
| `a_stale_or_mismatched_retry_of_a_batch_never_taps_a_guarded_step` | 2026-07-28 only, raw `call_tool_once` with hand-built `input_responses`: a pool of 1 to 3 batches, then random calls, retries with any answer (also for the wrong batch, twice, or with no question open) and call-then-answer pairs. Checks no guarded step is tapped without a matching open question, and a retry that follows its own question resumes exactly at the held step. | `mcp.rs`: `held_batch`, the retry block at the top of `guarded_batch`, `held_step`. |
| `every_answer_to_every_kind_of_held_input_on_both_protocols` | Exhaustive in its bound, about 3 seconds: 5 held inputs (a payment tap, a send tap with send asked, `type --submit`, two batches) x 7 clients (each of the 6 answers, and one that cannot ask) x 2 protocols, each called twice. It exists because the random properties miss a rare answer on a rare path; the first scratch break of this skill was one. | Same as the first row. |
| `f1_*`, `f2_*` (ignored) | Deterministic reproductions of open findings, see below. | `mcp.rs`: `guarded` (retry with an answer), `guarded_batch` (`held_batch.take()`). |

Support code: `crates/cli/tests/support/guard_rig.rs` (screens `checkout()` and `composer()`, daemon and `FakeDevice` rig; `tests/guard.rs` uses it too). The 2026-07-28 client must be started with `ClientLifecycleMode::Discover`; `.serve(..)` always negotiates 2025-11-25, whatever version `get_info` names (see F3). The retry property fails with "finished without asking" if the Discover handshake is lost, so a silent downgrade to the old path cannot go unseen.

**Sync commit: `4fc2204`** (the head when this check was written; the covered files were unchanged by the commit that added it).

When you finish a change, run:

```
git diff --stat 4fc2204 -- crates/cli/src/daemon/guard.rs crates/cli/src/daemon/guard crates/cli/src/daemon/actor.rs crates/cli/src/daemon/session.rs crates/cli/src/mcp.rs crates/cli/src/commands.rs crates/cli/tests/support/guard_rig.rs
```

Empty output means the check still describes the code. Otherwise read the diff for anything that changes: which taps are held, what an answer covers, what a batch retry does, the wire shape of an answer, or which tools take part (a new tool that taps must be added to the oracle and to `item()`). Run the check below. When it passes and you have confirmed the model and the generators still describe the code at the new commit, move the sync commit above to the new hash. Do not move it just because the test passes: a new guarded path the generators never reach passes too.

## Run

```
cargo test -p phonedriver --test guard_property
```

About 50 seconds, and the exhaustive test 4 seconds (every tap waits 500 ms for a screen change on the fake). It prints `coverage:` lines with `--nocapture`; on a good run these are in the hundreds of calls, prompts and resumes. A deeper run: `PROPTEST_CASES=60 cargo test -p phonedriver --test guard_property` (about 4 minutes). If `blaze` is free, `blaze test -p phonedriver --test guard_property` runs the same thing. The property tests do not run `autonomous` on batch (the MCP `batch` has no such field) or `PHONEDRIVER_GUARD=off` (an environment switch would race the other tests in the process).

A failure prints the shrunk input and what the device saw against what the promise says, in the code's own words (`Tap(Place)` is the "Place order · $34.10" button, `Submit` is `type --submit`, `Batch([...])` are the steps, `Retry(i, Allow)` is a second call carrying the answer). Steps of the story are numbered from 0.

## Real bug or modelling error

A **real bug** shows a guarded input (`Tap(Place)`, `Tap(Send)` with send asked, `Submit`) in "device saw" that the promise does not list, or a step before the held one that runs twice, or an approval that carries over to a second step. Reproduce it by hand with `guard.rs`'s `rig`: send the same calls and look at `rig.gestures()`. If the three-line story reads wrong in the product's terms ("the human said Allow once and two payments were tapped"), it is a bug. Report it with the counterexample; do not change the oracle to make it pass.

A **modelling error** is when the code did what the product intends and the oracle says otherwise. Typical causes: a new category or label added to the screens (`Btn`) with no oracle entry; a deliberate change to what a session approval covers (`Model::run`, `Ans::Session`); a changed prompt text (the prompt parser in `the_session_of_calls` reads `Tap "<label>"` and `Category: <name>`). Check the decision log first: if D27 or D31 changed, update `docs/decisions.md`, then the oracle, in the same commit.

A failure that mentions "finished without asking" or "asked, but the promise says no hold" means the question flow itself is off (or the Discover handshake was lost); fix the harness first.

To see the check fail on purpose: `python3 .claude/skills/verify-approval-guard/breaks.py <name>` applies one break to the product code, runs the check, restores the file with `git checkout`, and writes the output under `target/verify-approval-guard/`. Run it with no argument for the names:

| Break | Caught by |
|---|---|
| B1 approval on every batch step (`actor.rs`) | both |
| B2 resume from step 0 on the open connection (`mcp.rs`) | first |
| B2b resume from step 0 on 2026-07-28 | both |
| B3 `held_batch` never cleared | second |
| B4 any retry resumes the held batch | second |
| B5 session approval covers every category (`guard.rs`) | both |
| B6 / B6b decline taps (open connection / 2026-07-28) | first / both |
| B7 `type --submit` not guarded | both |
| B8 opt-in categories ignored | both |
| B9 a dismissed prompt taps, single `tap` on the open connection | first and the exhaustive one |

Before a commit that touches the covered files, run at least one break whose area you changed and confirm it still fails. A check that cannot fail is dead.

## Findings, fixed

F1, F2 and F3 were found at sync commit `4fc2204` and fixed in the commit that follows `55741c4`. Their tests now run by default.
- **F1.** A 2026-07-28 retry of `tap` or `type` was approved by any answer it carried. Now the server keeps one open question (`Held` in `mcp.rs`), keyed by the tool name and its arguments. An answer counts only on a retry of that exact call. Any other answer is treated as dismissed, and nothing is tapped. An `autonomous: true` call ignores a stray answer. Tests: `f1_an_answer_with_no_question_taps_a_payment`, `f1_an_answer_to_one_tap_approves_another`, and the property `a_stale_or_mismatched_retry_of_a_tap_or_type_never_taps_a_guarded_step`.
- **F2.** A stray answer emptied another call's open question. Now `take_held` compares the key before it takes the question. Test: `f2_a_stray_answer_does_not_cancel_the_pending_question`. Limit: the server keeps one open question, so a second call that asks replaces the first one.
- **F3.** `tests/guard.rs` now starts its 2026-07-28 client with `ClientLifecycleMode::Discover`. A decline or a dismissal on a retry now quotes the held question, which names the button and the category.

Limit: the key binds the answer to the call's arguments, not to what the screen shows at retry time. If the same call finds a different guarded button on the retry, the daemon applies the Once approval to that button.

## Not covered

- The label classifier (which text is guarded in which language): `guard.rs` unit tests and `tests/guard.rs` cover labels; this check uses fixed English screens with five buttons.
- Concurrent calls (the harness sends one at a time); the daemon's own ordering.
- `PHONEDRIVER_GUARD=off`, `autonomous` on `batch`, the CLI (`--approval`, exit code 5), `act` called straight on the daemon.
- A tap that reaches the device by another route: `shell input tap`, a point tap on a button, a double tap or long press on a guarded button (point taps are in `tests/guard.rs`), deep links, a button the screen merges into a container.
- A real client: Claude Code's elicitation UI and what it sends on 2026-07-28 are only as modelled by `Scripted`.
- Bounds: scenarios of at most 3 calls, batches of at most 5 steps, 14 answers, five buttons, one screen that does not change, session categories as the daemon keeps them for one MCP session. A pass covers those, not every length.
