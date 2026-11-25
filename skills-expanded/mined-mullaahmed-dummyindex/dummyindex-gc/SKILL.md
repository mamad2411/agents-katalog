---
name: dummyindex-gc
description: "Run context-hygiene garbage collection for stale, superseded, or dead generated proposals and audits, with carefully bounded routing for trivially dead or broader dead code. Combines deterministic candidate signals and commit-throttle state with parallel agents that inspect `.context/` and current work, classify each candidate as keep, stale, superseded, or dead, and distinguish disposable docs from code requiring tests or a proposal. Requires explicit user confirmation before every deletion; docs are deleted through guarded CLI operations, trivial private code only when implementer and tester keep the suite green, and broader code goes to planning. Use for `/dummyindex-gc`, `$dummyindex-gc`, garbage-collect context, sweep stale docs, clean up dead context, or a hygiene-sweep nudge."
---

# /dummyindex-gc / $dummyindex-gc — context-hygiene GC council sweep

> **Installed from dummyindex `__VERSION__`.** Run `dummyindex --version` to confirm the CLI matches. If they diverge, diagnose with `dummyindex context check --versions` (it reports which layer is stale), then run `/dummyindex-update` on Claude or `$dummyindex-update` on Codex to bring the CLI, skills, and this repo's wiring back into sync — the update skill is non-destructive on a curated `.context/`. Don't reach for a blunt `dummyindex install` to "fix" a version skew.

You are the **GC conductor**. Retire disposable proposals/audits. Keep their accepted knowledge in durable homes. Delete obsolete workspaces only after confirmation. Never archive transcripts or whole proposals.

## The deterministic / LLM split (read this first)

Same idiom as `audit-panel` (plumbing) + `/dummyindex-audit` (council).

- **`dummyindex context gc` is plumbing.** Lists candidate docs, gathers objective signals, computes commit-throttle state. Runs one guarded delete on explicit `--yes`. Never decides what is dead. Never confirms. Never touches source code.
- **This skill is judgment + gate.** "Stale / superseded / dead" is an LLM call: does the artifact still match the code and work in flight? Not an age rule. Confirm with the user. Only then run the CLI delete, or route code.

## The orchestration contract (run it in THIS order)

Seven steps, **in order**. Do not reorder. Do not skip the confirm gate. Never delete before the user confirms.

> **`gc status` → PageIndex walk → user-confirm → `gc delete` (docs) / implementer+tester (trivial code) / new proposal (broad code) → `gc stamp` → reconcile-if-code.**

### 1. `gc status` — the deterministic candidate report

```bash
dummyindex context gc status --json
```

Per candidate: `{kind, slug, rel_path, status, signals, tracked, age_days, recommendation, reason}`. Top level: `summary` (counts per recommendation) and commit-throttle state (`anchor`, `commits_since`, `threshold`, `should_signal`, `anchor_orphaned`).

- `recommendation`: `delete` / `close` / `review` / `keep`. A pre-council hint, not a verdict.
- `reason`: why the hint was given.
- `signals`: objective tags only (`orphan-empty`, `status:done`, `checklist-partial`, `report-written`, `untracked`, `age-<n>d`, `ARCHIVED`). Not verdicts.
- `anchor_orphaned` true: anchor unknown after history rewrite. Note it. Re-baseline in step 6.

On Claude this report also drives the SessionStart "N commits since last hygiene sweep" nudge. Codex installs no GC hook.

### 2. Fan out the PARALLEL council walk (dispatchable subagents)

Walk only `close`, `review`, `delete` candidates. `keep` candidates get no walk. Dispatch **one host-native subagent per candidate (or small cluster), all in one message**, so they run concurrently. Claude: `Task`. Portable host path (e.g. Codex): `explorer`, falling back to `default`. Each subagent:

- Grounds in `.context/HOW_TO_USE.md`, then reads the candidate's files (`spec.md`/`plan.md`/`checklist.md` for a proposal; `report.md`/`findings/` for an audit).
- Walks PageIndex-style to find what supersedes or depends on the candidate:
  ```bash
  dummyindex context query "<the candidate's topic / feature area>" --top-k 8 --json
  ```
- Reads the current session's work. "Superseded" is session-contextual: a plan the work in flight replaced is superseded now.
- Returns one verdict, `keep` / `stale` / `superseded` / `dead`, with evidence: `path:range`, superseding slug, or fixed-findings citation. "Looks old" is noise. Drop it.

These walks are read-only. Dispatch them.

### 3. Synthesize the delete-list — three categories, then closeout

Consolidate verdicts into three dispositions. Each takes a different path in step 5:

- **Dead docs.** Council verdict `stale` / `superseded` / `dead`: orphan scaffold, superseded `plan.md`, done audit with fixed findings, `_archive/*` child. Deleted through the CLI after confirm.
- **Trivially-dead code.** A 0-caller leading-`_` PRIVATE symbol that passes EVERY guard below. Cite the 0-caller claim from `.context/features/symbol-graph.json` (`calls` edges). Route to a proposal instead if it is any of:
  1. a CLI verb handler / `run(args)` reachable from the `cli/__init__.py` dispatch table;
  2. a hook entry point in the `hooks.py` / `claude_settings.py` command set (e.g. `signal`, `decide_nudge`);
  3. named in any `__all__` / re-exported public surface;
  4. a serialization round-trip member (`to_dict` / `from_dict` / `__init__`);
  5. referenced anywhere under `tests/`. First confirm `symbol-graph.json` includes `tests/`. If not, "0 callers" is blind to tests, so the graph alone never suffices;
  6. reachable by dynamic dispatch.
  Even then, removal must be **proven**, not asserted from the graph.
- **Broader / riskier dead code.** Anything not guard-passing: public symbol, multi-caller cluster that is all dead, anything unsure. Never auto-removed. Routed to a new proposal.

**Closeout and dry-run.**

- **`close` candidates and accepted `review` candidates:** run closeout.
  1. Draft: `dummyindex context gc closeout --draft --kind proposal --slug <slug>`. Existing draft is never overwritten; delete it to redraft.
  2. Fill transfers or discard reasons from council evidence. Empty discard reason is refused.
  3. Close: `dummyindex context gc closeout --kind proposal --slug <slug> --manifest .context/cache/gc/closeout-proposal-<slug>.json`

  Explicitly classify accepted lessons/decisions/evidence/fixtures and discarded material. The receipt must stay valid. Missing accepted units, changed fixtures, unreviewed files, or inbound durable references block deletion, even with `--force-partial`. Empty scaffolds keep their existing path. See `docs/guide/closeout.md` in the source distribution. After an accepted closeout, process at most one queued learning event through the evolve skill's ordinary gate, or record `NO_ENTRY`. Never learn recursively from evolve/experiment output.
- **`delete` candidates:** skip closeout.
- **All candidates headed for deletion:** run the dry-run. It runs every guard and removes nothing:
  ```bash
  dummyindex context gc delete --kind proposal --slug <slug>   # dry-run: no --yes, removes nothing
  ```
  Record the verdict. A `delete` recommendation can still fail the dry-run. The table shows that verdict.

Audits follow the same flow with `--kind audit`.

### 4. CONFIRM WITH THE USER — **non-dispatchable / human-decision**

> **This step is NOT dispatchable to a subagent.** The conductor (you, in this session) presents the batch and STOPS for an explicit "yes". A subagent never decides or confirms a deletion. Confirmation is a human decision the conductor/user owns. The CLI `--yes` flag enforces this gate; this skill enforces it above.

Present **one batch table** with one row per candidate:

| slug | recommendation | evidence | closeout result | dry-run verdict |
|---|---|---|---|---|

Ask for **one explicit confirmation**. The user may strike rows. Only listed rows are covered.

Rows that need `--allow-untracked` or `--force-partial` are **excluded from the batch**. Confirm each one alone. For each, spell out what it is, why it is dead, how it is removed, and the irreversible risk. An `untracked` deletion is **permanent** (not in git, no recovery). It needs the user's explicit okay on *that specific risk* before `--allow-untracked`. An `in_progress` / `checklist-partial` proposal is delete-blocked unless the user explicitly okays `--force-partial`. Confirmation always gates deletion. No doc or code is removed without the explicit go-ahead surfaced here.

### 5. Execute, per category (only user-confirmed items)

- **Dead docs → CLI delete, one row at a time.** For each confirmed row:
  ```bash
  dummyindex context gc delete --kind proposal --slug <slug> --yes
  dummyindex context gc delete --kind audit    --slug <slug> --yes
  ```
  One failure does not stop the others. A row refused at `--yes` is reported `blocked at delete`, with its reason. Add `--allow-untracked` only when the user explicitly okayed permanent deletion of that workspace. Add `--force-partial` only when the user explicitly okayed deleting that `in_progress` / `checklist-partial` proposal. Never add either speculatively. Re-deleting a gone target is an idempotent no-op (exit 0).
- **Trivially-dead code → implementer+tester (PROVE it green).** Dispatch the implementer to remove the symbol. Dispatch the tester to prove the full suite stays green. Keep the removal only if green. If anything goes red, the symbol was not dead: revert, route to a proposal. The graph proposes; the green suite disposes. GC never edits source directly; this path does.
- **Broader dead code → new proposal (never auto-removed).** Invoke `/dummyindex-plan "remove dead code: <short description>"` on Claude, or `$dummyindex-plan "remove dead code: <short description>"` on Codex.

### 6. `gc stamp` — advance the GC anchor

After the sweep report, every run, even when nothing was retired:

```bash
dummyindex context gc stamp
```

Advances the committed anchor to HEAD (or `--to <sha>`) and resets the commit-throttle counter. On Claude, the SessionStart nudge stays quiet until `threshold` new commits land. On Codex, it resets the same state. If step 1 flagged `anchor_orphaned`, re-baseline with `dummyindex context gc stamp --to HEAD`. Off-git, `stamp` is a no-op.

### 7. Reconcile `.context/` if code changed

If step 5's trivially-dead path changed source, reconcile per this repo's host guidance (`.claude/CLAUDE.md` or the active Codex project instruction file). **Do not** stop at a deterministic rebuild:

```bash
dummyindex context reconcile          # read-only — reports the delta, writes nothing
```

`reconcile` is read-only. It reports drift and unassigned files. Then follow the reconcile procedure (place / enrich each touched feature doc) and advance the anchor:

```bash
dummyindex context reconcile-stamp
```

Docs-only sweep: nothing to reconcile. `gc delete` already updated the on-disk docs, and step 6 stamped. Skip this step.

### Sweep report (chat output only, no file)

Final chat output of every run:

- counts per recommendation: `delete` / `close` / `review` / `keep`;
- closed: proposals closed out;
- deleted: rows removed;
- blocked: refused rows, each with its reason (`blocked at delete` or dry-run verdict);
- kept: rows left in place, including `keep` candidates.

Nothing to retire: write `ran, found nothing to retire`.

## Dogfooding this repo (GATE) — **non-dispatchable / human-decision**

> Running `/dummyindex-gc` against **this** repo to delete its own orphan / superseded docs is a **user-confirmed GATE, never automatic**. Read live candidates from a fresh `gc status` run, never a hard-coded slug list. Present them. STOP for the user's explicit confirm, as in step 4. This GATE is **not dispatchable to a subagent**: deleting this repo's docs is the conductor's/user's decision.

## Discipline (non-negotiable)

- **Confirmation always gates deletion.** No doc or code is removed without explicit user confirmation from step 4. The CLI refuses without an explicit target and `--yes`. Untracked workspaces need a second flag, `--allow-untracked`. This skill gates above that.
- **Step 4 (user-confirm) and the dogfood GATE are NOT dispatchable.** Human decisions. Only the read-only PageIndex walks (step 2) and trivially-dead implementer+tester (step 5) are dispatched.
- **Never show a bare `gc delete`.** Every shown `gc delete` carries `--yes` and sits behind the confirm step. Without `--yes` it is a dry-run, never an auto-action.
- **Delete only the genuinely dead.** Stale / superseded / dead / no-longer-useful. Not every `done` proposal. A `close` recommendation is only a hint; council and user decide.
- **Evidence over assertion.** Every verdict cites `path:range`, a superseding slug, or a fixed-findings reference. "Looks old" is not evidence.
- **GC never edits source directly.** Trivially-dead code goes through implementer+tester and is removed only if the full suite stays green. Broader dead code goes to a proposal. The CLI never touches code.
- **The code wins.** Conventions and feature docs are context, not authority. When a doc and the code disagree, cite the code. The doc is itself a GC candidate.

## CLI reference (deterministic state only)

```
dummyindex context gc status [--json] [--root DIR]
    → read-only sweep report: candidates, signals, recommendation + reason,
      summary, commit-throttle state (anchor, commits_since, threshold,
      should_signal, anchor_orphaned). Exit 0. Skill and Claude's SessionStart
      hook consume this.
dummyindex context gc delete --kind proposal|audit (--slug S | --path P) --yes \
    [--allow-untracked] [--force-partial] [--root DIR]
    → delete ONE generated-doc workspace dir, atomically, after user confirm.
      Guards (in order): slug-charset → sentinel-reject (_archive / leading-_ /
      . / .. / empty) → realpath containment → liveness (refuse in_progress /
      checklist-partial without --force-partial) → recoverability (refuse
      untracked without --allow-untracked). Re-delete of gone dir = no-op.
      NEVER deletes source code.
dummyindex context gc delete --kind proposal|audit (--slug S | --path P) [--root DIR]   # dry-run: no --yes
    → same guards, prints verdict, removes NOTHING. Guard error exit 2;
      untracked refusal exit 0 (`refused`). Advisory: --yes re-runs every guard.
dummyindex context gc closeout --kind proposal|audit --slug S (--manifest FILE | --draft) [--root DIR]
    → --draft writes .context/cache/gc/closeout-<kind>-<slug>.json. Never
      overwrites (exit 2 if it exists). A draft with an empty discard reason
      is refused by closeout until filled.
    → --manifest FILE closes the workspace from a reviewed manifest.
dummyindex context gc stamp [--to SHA] [--root DIR]
    → advance the committed GC anchor to HEAD (or --to SHA); resets the
      commit-throttle counter. Off-git = no-op.
dummyindex context gc signal [--json] [--root DIR]
    → Claude's SessionStart throttle probe: prints the one-line nudge iff over
      threshold or anchor orphaned, and not already signalled this session.
      Always exit 0. (The Claude hook runs this; on either host, run `gc status`.)

dummyindex context query "<topic>" [--top-k N] [--json]
    → PageIndex-style retrieval the council walk uses to find what supersedes or
      still depends on a candidate. No LLM in the loop.
```
