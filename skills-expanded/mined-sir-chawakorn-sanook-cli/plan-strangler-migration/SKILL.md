---
name: plan-strangler-migration
description: Plans and executes incremental legacy modernization with the strangler-fig pattern — pins current behavior with characterization/golden-master tests, carves the narrowest seam, routes traffic old↔new behind a flag (shadow then canary), compares parity on real traffic, migrates data via expand-contract, then flips the default and retires the old path against a tracked kill-list.
when_to_use: Replacing or rewriting a live legacy system/module slice by slice with rollback at every step — monolith→service, framework v-old→v-new, on-prem→cloud, rewriting an untested critical component, or peeling a god-class apart, when a big-bang cutover is too risky. Distinct from feature-flags-rollout (owns the flag/bucketing/ramp mechanics this skill drives), db-migration-safety (owns the DDL/lock safety of the expand-contract step), and diff-table-parity (diffs two static datasets; this diffs live request streams).
---

## When to Use

Reach for this when you must **swap an implementation while the system stays live**, with rollback at every step:

- "Move this endpoint/module off the monolith into a new service without a freeze"
- "Rewrite this untested payment/pricing component — I'm scared to touch it"
- "Migrate from <old framework/runtime> to <new> without a big-bang cutover"
- "Break this 4,000-line god-class apart safely"
- "Re-platform on-prem → cloud, one slice at a time, provably reversible"
- "We tried a rewrite-and-switch and it blew up — do it incrementally instead"

NOT this skill:
- Building the flag, hashed bucketing, and 1→10→50→100 ramp itself → feature-flags-rollout (this skill *drives* a flag; that skill *builds* it)
- Lock contention, blocking DDL, destructive ops in the expand-contract step → db-migration-safety
- Diffing two **static** tables/query results to prove a migration matched → diff-table-parity (this skill diffs **live shadowed request streams** in flight)
- Writing tests for code whose contract you *know and trust* (TDD a new feature) → write-tests (here you pin **observed** behavior, bugs included, not desired behavior)
- Behavior-preserving cleanup once the new path already works → refactor-cleanup
- Sequencing an already-decided plan into batched steps → write-plan

## Steps

1. **Characterize BEFORE you touch anything — pin observed behavior, not intended behavior.** Write golden-master/characterization tests that capture what the legacy path *actually does today, bugs included*. These are your regression witness; without them you cannot prove the new path is equivalent. If the unit is untestable in isolation, characterize at the next boundary out (HTTP, queue message, CLI stdout). Don't write the assertion by hand — record the real output and snapshot it:

   ```python
   # Pin CURRENT behavior. If legacy returns a wrong-but-shipped value, the snapshot
   # captures the wrong value on purpose — parity first, fix bugs in a LATER slice.
   @pytest.mark.parametrize("case", load_real_inputs("prod_samples.jsonl"))
   def test_golden_master(case, snapshot):
       assert snapshot == legacy.handle(case)   # `pytest --snapshot-update` once, then freeze
   ```
   Feed it **real recorded inputs** (sampled prod traffic / a replay log), not invented ones — invented inputs miss the quirks that break the rewrite.

2. **Find the seam — the narrowest interface where old and new can swap.** Pick the boundary by cost; narrowest viable wins.

   | Seam type | Swap point | Use when | Rollback granularity |
   |---|---|---|---|
   | **HTTP route / reverse proxy** | nginx/Envoy/API-gateway path rule | monolith→service, per-endpoint carve | per route, instant |
   | **Function/interface (facade)** | inject impl behind one interface | god-class split, in-process rewrite | per call, per deploy |
   | **Message/queue consumer** | new consumer group on same topic | async pipeline, event handler | per topic/partition |
   | **Branch-by-abstraction** | abstraction layer both impls satisfy | can't split a release; long-lived migration on `main` | per flag, no long branch |

   Default to **branch-by-abstraction behind a flag** for in-process work and a **proxy/gateway route split** for service extraction. Avoid long-lived feature branches — they rot; keep both impls on `main` behind the seam.

3. **Stand up the new impl behind the seam and route a thin slice via flag — start in shadow.** Do not send real users to unproven code first. Ramp the *mode*, then the *percentage*:
   - **Shadow (mirror):** run new alongside old on real traffic, **discard new's result, serve old**, log the diff. Zero user risk — this is how you earn trust.
   - **Parallel-run (canary):** serve new to 1% (sticky by user/key), keep old as the authority for everything else.
   - The flag/bucketing/ramp mechanics are **feature-flags-rollout's** job — wire to it; don't reinvent hashing here.

   ```
   result_old = legacy.handle(req)
   if flags.enabled("strangler.charges", req.user):     # sticky bucket
       result_new = newimpl.handle(req)
       compare.record(req, result_old, result_new)      # async, never blocks the response
   return result_old                                    # shadow phase: OLD is still the truth
   ```

4. **Compare old vs new on real traffic; widen only while parity holds.** Diff every shadowed request and alert on mismatch rate, not just errors. Normalize away legitimate noise — timestamps, map ordering, float epsilon — *before* diffing, or you'll drown in false diffs. Set a hard gate: **promote a slice only after ≥10k shadow requests at <0.1% semantic mismatch.** A persistent diff is a finding: either a real new-impl bug, or an undocumented legacy quirk you must replicate. Never widen past an unexplained diff.

5. **Migrate data/state with expand-contract — keep both readable until cutover.** Never rename/drop in place. Three phases, each independently deployable and reversible: **expand** (add new column/table/store, backfill, dual-write old+new) → **migrate** (reads shift to new, writes still hit both) → **contract** (stop writing old, drop it — only after the new path is the default and stable). Dual-write so a rollback at any moment still finds consistent data on the old side. The DDL safety of each phase (lock time, backfill batching, online index) belongs to **db-migration-safety** — route the schema change there.

6. **Flip the default, keep the rollback flag live, retire in two separate steps.** When a slice holds parity at 100%, flip its flag default to **new** but **leave the flag in place** so one toggle reverts. Bake in for one full business cycle (covers month-end/batch/cron paths). Only then: (a) delete the old code path, (b) **in a separate later commit**, remove the now-unused flag and dead branches. Collapsing flip + delete into one change throws away your rollback the moment you might need it.

7. **Track a kill-list so "done" is provable.** Maintain a checklist of every legacy unit (route, function, table, consumer) with its state: `characterized → shadowing → canary → default-new → old-deleted → flag-removed`. The migration is done when every row reaches `flag-removed` and zero callers reference the legacy module. No kill-list = no way to prove completion, and stranded half-migrated code lives forever.

## Common Errors

- **Rewriting before characterizing.** You have nothing to compare against, so "it works" is a guess. Always pin observed behavior (step 1) first — even ugly snapshot tests beat none.
- **Pinning intended behavior instead of actual.** You "fix" a legacy bug while characterizing, the snapshot now disagrees with prod, every shadow diff is noise. Capture reality; fix bugs as a *later, separate* slice with its own test change.
- **Big-bang seam — boundary too wide.** Carving a whole subsystem at once = no thin slice, no cheap rollback. Find a narrower interface (one route, one function) even if it means more iterations.
- **Going straight to canary, skipping shadow.** Real users hit unproven code before you've seen a single diff. Shadow first; users only after the mismatch rate is provably near-zero.
- **Comparison blocks the response / mutates state twice.** Synchronous diffing adds new-impl latency to every request, and a non-idempotent new path in shadow double-charges/double-sends. Record diffs async and keep shadow side-effect-free (no writes, no emails, no charges).
- **Diffing raw output without normalization.** Timestamps, map ordering, and float jitter flood you with fake mismatches and you stop trusting the signal. Canonicalize both sides before comparing.
- **Rename/drop-in-place migration.** Destroys the old read path, so rollback corrupts data. Use expand-contract with dual-write; drop only in the final contract phase.
- **Deleting the old path in the same change that flips the default.** The instant you need to roll back, there's nothing to roll back to. Flip, bake, then delete in a later commit; remove the flag in a third.
- **Long-lived rewrite branch.** It diverges from `main` for months and the merge is its own big-bang. Keep both impls on `main` behind the seam (branch-by-abstraction).
- **No kill-list / orphaned flags.** Half-migrated routes and permanent "temporary" flags accumulate; nobody can say what's done. Track every unit to `flag-removed`.

## Verify

1. **Characterization exists and is green on legacy:** the golden-master suite runs against the *unmodified* old path and passes from real recorded inputs (not hand-written cases).
2. **Seam is reversible by config:** a single flag/route toggle (no redeploy) flips a slice old↔new and back; demonstrate the round-trip live.
3. **Shadow parity gate met:** the promoted slice logged ≥10k shadowed requests at <0.1% semantic mismatch, and every residual diff is explained (real bug filed, or quirk now replicated).
4. **Shadow is side-effect-free:** with the new path shadowed at 100%, downstream effects (writes, charges, emails) occur exactly once — proven by counts, not inspection.
5. **Data is dual-readable mid-migration:** after cutover-to-new-reads but before contract, force the rollback flag → the old read path still returns consistent data (dual-write working).
6. **Rollback works after flip:** with default=new in prod, toggle the flag → traffic returns to old with no errors and no data divergence.
7. **Old path retired separately and fully:** dead legacy code is deleted in its own commit, the flag removed in another, and a code search shows zero remaining references to the legacy module.
8. **Kill-list closed:** every unit on the list is at `flag-removed`.

Done = the golden-master suite passes on the new path, every kill-list unit reached `flag-removed`, no live caller references the legacy module, and a single toggle could have reverted each slice up until its flag was removed.
