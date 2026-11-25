---
name: signed-policy
description: Formally verify Lodeline's signed policy apply path with a TLA+ model of apply, verify_envelope, atomic_write, settle_pending, the file in force, boot, and reload. Use before you change those functions, the policy watermark, the pending envelope row, PolicyPaths or SignedFile::in_force, policy.yaml writes, or control-socket concurrency, or to check whether an older or unsigned envelope can replace the file in force across a crash, a power cut, or a restart.
---

# Verify the signed policy apply path

`spec/SignedPolicy.tla` models how the agent takes a signed envelope from the control socket to the applied file, `state.db`, and the live evaluator, and how it chooses between the applied file and the operator's local file. TLC checks every order of those steps within the bounds below. Any party can deliver any envelope any number of times, because the agent's only defense is `verify_envelope`.

## Run the check

```sh
python3 .claude/skills/signed-policy/check.py
```

The command exits 0 only if all three parts pass. Each part runs even when an earlier one fails. The run takes 60 to 70 seconds on a 12-core Mac, and the last line is `OK in <seconds>` or `FAILED in <seconds>`.

1. It compares each function and block in the coverage table with its text at the sync commit. It prints `DRIFT <file> <function> changed since the sync commit. Model element: <elements>` for each difference, or `Drift check clean.`
2. It runs TLC on `spec/policy.cfg`, `spec/rule_packs.cfg`, and `spec/local_edits.cfg`. It prints `PASS <config>: <n> distinct states in <s>s`, or `FAIL <config>` followed by TLC's output.
3. It breaks the model 24 ways. Each break is a text edit to the model, and TLC checks it against one property on one thread. It prints `<verdict> <break> (<code it stands for>): <property>, <s>s`, with one of three verdicts.
   - `KILLED` means that TLC reported the property violated, the trace took the expected actions in order, and for some breaks the last state of the trace shows the expected text.
   - `OFF-TARGET` means that TLC reported the property violated, but the trace missed the expected actions or the expected text. The next line shows `wanted [...], trace took [...]`, where `wanted` lists the expected actions and then the expected text.
   - `SURVIVED` means that TLC did not report the property violated.

Use `--drift` for part 1 alone. Use `--model` for part 2 alone while you edit the model.

### Install the tools once

`check.py` downloads TLC 1.7.4 from the official tlaplus GitHub release on its first run and verifies the pinned SHA-256. The jar stays in `~/.cache/lodeline-formal/`, or under `$XDG_CACHE_HOME` when that is set.

TLC needs Java 11 or later, and `/usr/bin/java` on macOS is a stub. `check.py` tries `$JAVA_HOME`, then Homebrew's `openjdk@21`, then `java` on `PATH`.

```sh
# macOS. A plain install also upgrades shared libraries that headless Java does not use.
HOMEBREW_NO_AUTO_UPDATE=1 brew install --ignore-dependencies openjdk@21

# Debian or Ubuntu
sudo apt-get install openjdk-21-jre-headless
```

## What the check proves

Below, the applied file is `SignedFile.applied`, the local file is `SignedFile.local`, and the file in force is what `SignedFile::in_force` returns, the applied file if it exists, else the local file. Each property covers one file, `policy.yaml` or `rule-packs.yaml`, and its own version. A broken variant is checked against its own property alone.

| Property | Claim | Harm if it breaks | Broken variants that TLC catches | Configs |
|---|---|---|---|---|
| `OnlySignedAccepted` | The applied target is absent, or holds the operator's unsigned file, or holds an envelope that passed checks 1 and 2 of `verify_envelope`. The operator's file at the target comes only from `Starts`. The property says nothing about the local file. | Anyone who reaches the sender or the socket can install a policy. | No signature check. | `policy`, `rule_packs`, `local_edits` |
| `NoExpiredApplied` | On the step from verification to `record_pending`, `now < valid_until`. It says nothing about a later tick or a settle. Boot finishes a pending row even when its envelope expired after verification. The host then reports the policy as expired (`policy_expired_active`), the same end state as an envelope that expires right after a completed apply, because expiry flags an active policy and never removes it. | A long-expired policy replaces the current one. | No expiry check. | `policy`, `rule_packs`, `local_edits` |
| `VersionCheckHolds` | While an apply is between verification and its rename, its envelope is newer than the file in force. | An older envelope is written over a newer one. | No version check. No `apply_lock`. No settle in `apply`. | `policy`, `rule_packs`, `local_edits` |
| `WatermarkNeverAhead` | The applied version never exceeds the version of the file in force. | A retry fails as a regression, and the host reports a version that it does not hold. | Promote before the rename. The rename keeps the operator's file. No directory fsync in `write_file_durably`. No directory sync in `settle_pending`. | `policy`, `rule_packs` |
| `NoRollback` | The version of the file in force falls only on a step that leaves the agent down with a pending row present. It is about the file, and is not a claim about acceptance, which is `VersionCheckHolds`. | A host that took a newer policy runs an older one. | No version check and no `record_pending` guard together. Either one alone does not break it. | `policy`, `rule_packs` |
| `WatermarkMonotonic` | The applied version falls only on a step that leaves the agent down, with the pending row equal to the file in force and that file at or above the old applied version. | Envelopes older than the last applied one become acceptable again. | No guard on the version at any step, which removes check 4 and the `record_pending` and `promote_pending` guards. | `policy`, `rule_packs`, `local_edits` |
| `BootSettles` | On the boot step no row is left pending, and the applied record equals the envelope behind the file in force, or is empty when that file is the operator's. | An apply checked against a stale record replaces a newer policy. | No settle at boot. Boot settles the apply target. `record_pending` at `synchronous=NORMAL`, where a power cut keeps the rename and loses the row. | `policy`, `rule_packs` |
| `LiveMatchesDisk` | With the agent up, no apply in flight, no row pending, no change unseen, no hand edit that no reload has looked at, no reload between its check and its read, and no reload that kept the live policy behind a retry, the live policy is the applied file if it exists, else the local file. | The agent acknowledges a policy and keeps enforcing the old one. | The local file read first. No reload notification. No notification after a settled apply. The change consumed after the read. No retry after a failed reload. A bad bundle holds back the policy. A retry for the bundle skips a changed file. | `policy`, `rule_packs`, `local_edits` |
| `ExpiryMatchesDisk` | For `policy` only. With the agent up, no apply in flight, and no row pending, `active_valid_until` is the expiry of the file in force, so the reported expiry matches the file on disk. An unseen change or a running reload does not exempt it. | The host reports an expiry for a policy it does not run. | No expiry seeded at boot. A settled apply not published. | `policy` |
| `LoadedPolicyKept` | For `policy` only. While the agent stays up, a policy file that was loaded never becomes no file loaded. | A save that unlinks before it writes drops every deny rule. | No missing-file rule in `reload`. | `local_edits` |

Each config checks only the properties that list it in the last column. A property says nothing about a config that does not list it.

| Config | Kind | Connections | Failed steps | Power cuts | Hand edits | Distinct states |
|---|---|---|---|---|---|---|
| `policy` | policy | 2 | yes | yes | no | 2,075,700 |
| `rule_packs` | bundle | 2 | yes | yes | no | 1,438,404 |
| `local_edits` | policy | 2 | yes | no | yes | 7,121,540 |

- `policy` checks every property except `LoadedPolicyKept`. `rule_packs` checks the same less `ExpiryMatchesDisk`, which covers `policy` only.
- A failed step is an error from `record_pending`, the rename, the directory fsync, or `promote_pending`, or a reload that fails and keeps what is live (`ReloadReadFails`).
- Every config allows a process crash whenever the agent is up, and starts from all six hosts in `Starts`. Crashes and power cuts share a cap of three stops.
- `local_edits` has no power cuts. A stop there is a crash, which keeps every write the agent made, so that config says nothing about what a power cut loses. It adds the hand edits `DeleteApplied` and `EditLocal`.
- `WatermarkNeverAhead`, `ExpiryMatchesDisk`, `NoRollback`, and `BootSettles` are left out of `local_edits` because each fails when added there, and the first failing step is the hand edit `EditLocal`. The documented way back to the local file keeps the signed version and its expiry while the local file runs.

## Decide if your change touches verified code

Read the coverage table. If your change touches a listed function or block, `check.py` prints `DRIFT` until you confirm the model at a new sync commit. A row such as `first..last` tracks the lines from the first line that contains `first` to the next line, from there on, that contains `last`, for a block of a function too large to track whole. A row prints `DRIFT` too when its function or block is gone from the current file.

`check.py` reads the lines under the `Sync commit:` line up to the next heading. Any line there with a pipe character must be a row of the table, and the table needs the three columns Model element, File, and Function. A line that is not a row stops the run with ``check.py: SKILL.md has a coverage row that cannot be parsed: '<line>'``, because a row left out would leave a function untracked. A missing or wrong header stops it with ``check.py: SKILL.md has no coverage table under the `Sync commit:` line``.

Sync commit: `099fddf2aaff4612e2f02a034e949d4c16e6c1e3`

| Model element | File | Function |
|---|---|---|
| `Settle, Verify, Reject, Finish, cacheLock` | `crates/lodeline-agent/src/policy_apply.rs` | `apply` |
| `Settle, Verify, Reject, Finish, cacheLock` | `crates/lodeline-agent/src/policy_apply.rs` | `apply_rule_packs` |
| `Settle, applyLock` | `crates/lodeline-agent/src/policy_apply.rs` | `settle_earlier_apply` |
| `Publish, Notify, NotifySettled` | `crates/lodeline-agent/src/policy_apply.rs` | `publish_policy` |
| `Notify, NotifySettled` | `crates/lodeline-agent/src/policy_apply.rs` | `publish_rule_packs` |
| `Verify` | `crates/lodeline-core/src/policy/verify.rs` | `verify_envelope` |
| `Verify` | `crates/lodeline-core/src/policy/pubkeys.rs` | `active_pubkey` |
| `Record, Rename, Fsync, Promote` | `crates/lodeline-core/src/policy/atomic_writer.rs` | `atomic_write` |
| `SettleRow, Matches, Finished` | `crates/lodeline-core/src/policy/atomic_writer.rs` | `settle_pending` |
| `Rename, RenameFails, Fsync, FsyncFails` | `crates/lodeline-core/src/policy/atomic_writer.rs` | `write_file_durably` |
| `RenameFails` | `crates/lodeline-core/src/policy/atomic_writer.rs` | `create_dir_durably` |
| `Fsync, SettleRow` | `crates/lodeline-core/src/policy/atomic_writer.rs` | `sync_dir` |
| `Record, RecordFails` | `crates/lodeline-core/src/host_meta.rs` | `record_pending` |
| `Matches` | `crates/lodeline-core/src/host_meta.rs` | `pending` |
| `Promote, PromoteFails, SettleRow` | `crates/lodeline-core/src/host_meta.rs` | `promote_pending` |
| `SettleRow` | `crates/lodeline-core/src/host_meta.rs` | `clear_pending` |
| `Record, RecordFails, Promote, PromoteFails` | `crates/lodeline-core/src/host_meta.rs` | `require_advanced` |
| `Record, RecordFails, WriteBackDb, PowerCut` | `crates/lodeline-core/src/state.rs` | `open` |
| `Verify, Boot` | `crates/lodeline-core/src/host_meta.rs` | `host_meta_get` |
| `InForce, ReloadCheck` | `crates/lodeline-agent/src/runtime.rs` | `in_force` |
| `target, local` | `crates/lodeline-agent/src/runtime.rs` | `at` |
| `target, local` | `crates/lodeline-agent/src/runtime.rs` | `policy_paths` |
| `target, local` | `crates/lodeline-agent/src/runtime.rs` | `system_policy_paths` |
| `target, local` | `crates/lodeline-agent/src/runtime.rs` | `default_policy_paths` |
| `target, local` | `crates/lodeline-agent/src/runtime.rs` | `resolve_policy_paths_unix` |
| `InForce` | `crates/lodeline-agent/src/runtime.rs` | `policy_path_for_command` |
| `Boot` | `crates/lodeline-agent/src/runtime.rs` | `let policy_path_for_apply = cfg..let bundle_doc_for_ctx` |
| `Settle, Rename` | `crates/lodeline-agent/src/runtime.rs` | `let apply_ctx = Arc::new..apply_lock: Default::default()` |
| `ReloadCheck, ReloadRead, loaded, retry` | `crates/lodeline-agent/src/runtime.rs` | `paths: cfg.policy_paths.clone()..rule_packs_read,` |
| `ReloadCheck, ReloadRetry, ReloadRead, ReloadReadFails` | `crates/lodeline-agent/src/policy_reload_task.rs` | `reload` |
| `ReloadCheck, ReloadRetry` | `crates/lodeline-agent/src/policy_reload_task.rs` | `run` |
| `ReloadRead, ReloadReadFails` | `crates/lodeline-agent/src/policy_reload_task.rs` | `read_bundle_state` |
| `ReloadRead, ReloadReadFails` | `crates/lodeline-agent/src/policy_reload_task.rs` | `note_unfinished` |
| `ReloadCheck` | `crates/lodeline-agent/src/control.rs` | `Request::ReloadPolicy => {..policy_version_tx.send_modify(` |
| `Workers` | `crates/lodeline-agent/src/control.rs` | `serve_until` |

The check cannot read Rust. A `PASS` covers the model, and `DRIFT` is the only link from the model to the code. `Boot` stands for the block above and for its order in `runtime::run`, which no row can see: settle, load the file, then start the control socket. If you change that order, update `Boot` by hand.

## Resolve a DRIFT line

1. Run `git diff <sync commit> -- <file>` and read the change to the function or block on the `DRIFT` line.
2. If the change alters no step, order, guard, or lock, go to step 5.
3. Edit the actions named after `Model element` in `spec/SignedPolicy.tla` so that they do what the code now does. Keep one action per indivisible step in the code. If the function or block was renamed or moved, fix its row in the coverage table.
4. Run `check.py --model`. Then resolve each `FAIL`.
5. Move the sync commit in this file to a commit on `main`. A squash merge drops branch commits. Move it only after you confirm that the model describes the code at that commit.
6. Run `check.py`. All three parts must pass.

If the run stops with `check.py: cannot read <file> at <sync commit>` or `<function> is not in <file> at <sync commit>`, the sync commit is missing from your clone, or the row names text that was not there. Fetch the commit, or fix the row.

## Resolve a FAIL line

`FAIL <config>` is followed by TLC's output. A violation comes with a trace. Each state names the action that produced it and the variables that changed. If the output is an error with no trace, such as a syntax error in the model, fix the model text first.

1. Find each action in the coverage table and read its code.
2. If the code cannot take those steps in that order, the model is wrong. Fix the action, and keep the property and the bounds.
3. If the code can take those steps, compare the last state with the harm in the property table. If the harm cannot follow, the property claims too much. Restate the same claim more exactly, and add a mutant that proves the new form can fail.
4. Otherwise you found a bug. Report the trace as a short list of steps in the code's words. Then fix the code or report the bug. Do not weaken a property, lower a bound, or remove an action to get a pass.

## Resolve a SURVIVED or OFF-TARGET line

A property that cannot fail proves nothing. Find out why the break no longer reaches the property, and correct the model or the mutant in `check.py`. A mutant edit must match the model text exactly once, so a rename in the model stops the run with `check.py: mutant edit must match once`.

`SURVIVED` means that TLC did not report the property violated. Read the edit in `MUTANTS` and the action it changes. Find the other step or guard that now blocks the harm, and correct the edit or the model.

`OFF-TARGET` means that the property failed without the expected actions in order, or without the expected text in the last state. The next line, `wanted [...], trace took [...]`, lists the expected actions and text, then the actions of the trace that TLC found on one thread. Compare the two lists.

1. If the trace shows the harm the mutant stands for by a shorter way, correct the expected steps or text in `MUTANTS`.
2. If it shows some other failure, tune the edit until the mutant fails for its own reason. A mutant that fails for the wrong reason says nothing about the code it stands for.

A property written as `[][...]_vars` skips any step that changes no variable. If the failure you want to catch leaves a value unchanged, write the property as an invariant.

## Know what a pass covers

The bounds are `MaxVersion = 4`, `MaxClock = 3` (`valid_until` is 1 to 3, and the clock runs 0 to 3), `MaxCrashes = 3` (crashes and power cuts share it), and two connections in every config.

Every break runs on `policy`, except `no missing-file rule` and `a retry for the bundle skips a changed file`, which run on `local_edits`. No break runs on `rule_packs`. The checks under `apply_lock` make the `record_pending` and `promote_pending` guards unreachable, so removing either guard alone passes every property of `policy` and `rule_packs`. The breaks that need those guards removed remove several at once.

The model assumes these facts:

- ed25519 and the canonical bytes work. `auth` stands for checks 1 and 2 of `verify_envelope`.
- `rename` plus the directory fsync is durable, one SQLite transaction is atomic, and WAL commits reach the disk in order.
- The state directory is not lost. `create_dir_durably` keeps a new directory, and the model treats the directory as there.
- The wall clock only moves forward. A tick after verification does not count against `NoExpiredApplied`.
- A host starts in one of the six `Starts`: nothing, the operator's unsigned file at the apply target and nothing else (the `--policy`, non-root, and Windows host), the operator's file in the local path, an older agent's file, or an older agent stopped just after or just before its rename. An older agent's rename has reached the disk, and its record has an expiry.
- A retry is no, behind, or bundle. Behind is a reload that kept the live file. Bundle is a load of the policy over a bundle that `read_bundle_state` reports as Corrupt or Empty, and only the policy kind models it. A retry for the bundle that finds the policy text it applied has nothing to apply, and a retry compares nothing else.
- `policy.yaml` and `rule-packs.yaml` do not affect each other. They share `apply_lock` and a `state.db` connection, and the model checks each alone.
- Two envelopes never hold the same bytes, so `pending = file` stands for the blake3 comparison in `settle_pending`.
- Every envelope that passes `Verify` loads at `ReloadRead` and at `Boot`, the operator's file also loads.
- The only writers other than an apply are the hand edits in `local_edits`: deleting the applied file, and adding or removing the local one. Nobody else writes these files or `state.db`.

The model leaves out these parts:

- The other hand edits, and power cuts in `local_edits`.
- `lodeline-sender`, `lodeline-server`, and `lodeline-sign`.
- Document content: check 5 of `verify_envelope`, `merge`, and deny-rule compilation. A failure of `merge` counts as `ReloadReadFails`. A deny-rule failure keeps the previous evaluator, finishes the reload, and does not retry.
- A `rule-packs.yaml` that does not parse at boot. Boot ignores it with a warning, so it is document content, and the `Boot` row ends at the bundle read.
- `policy_expiry_task`, the wake-ups of `rule_packs_watch`, and the root tick that reloads when the rule-pack file in force no longer matches the last load's read. `ReloadCheck` only stands for these as a reload at any time. The model has no liveness property, so it does not show that a hand edit is ever looked at. The root tick is what makes that true for `rule-packs.yaml` when a poll watcher misses a change.
- Commands that only read the files: `assess`, `show`, `doctor`, and `status`.
- `host_meta_get` reading version 1 with no expiry as no envelope, and a recorded version with no expiry.
- `DeploymentStore` and `DeploymentCoordinator`, which `runtime::run` does not use yet.
- Windows rename semantics and its `sync_dir`, which does nothing.

To bring this skill back in line after changes that skipped it, run `/maintain-formal-verification-skill`.
