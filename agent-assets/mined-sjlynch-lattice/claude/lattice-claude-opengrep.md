# backend/src/opengrep

Opengrep (the LGPL-2.1 community fork of Semgrep CE — a local, offline SAST
engine) as a Lattice **tool**: installed at the user's click, run as a child
process, its findings handed to agents as a size-bounded markdown **digest**
(never raw JSON). Facade: `../opengrep.ts`. Owned elsewhere: MCP tools
(`../latticeMcp/CLAUDE.md`), routes (`../routes/ROUTES.md`), Settings → Tools
(`frontend/src/components/settings/tools/CLAUDE.md`), the graph Security chip
(`useSecurityOverlay`, `frontend/src/components/forceGraph/hooks/CLAUDE.md`).

## Licence boundary (read before adding anything here)

Lattice is MIT; the engine is LGPL-2.1; pack `qodana-mit` is MIT; pack
`opengrep-archived` is LGPL-2.1 + Commons Clause. Two enforced rules keep
Lattice's licence unaffected:

1. **No third-party binary or rule file is ever committed or bundled into a
   Lattice package.** The repo holds only URLs, a pinned version, pinned
   commits and SHA-256 digests (`versions.ts`); every download lands under
   `~/.lattice/opengrep/` at the user's explicit click. Pinned by
   `__tests__/opengrepNoVendoredAssets.test.ts` (walks `git ls-files`).
   Lattice-authored (MIT) rules may live in the repo; third-party ones may not.
2. **Opengrep runs only as a separate process** (`spawnWithTimeout`, JSON over
   a file) — never linked, loaded in-process or modified. Process separation
   isn't a derivative work, and LGPL duties fall on the distributor (GitHub
   releases). **Never ship an installer bundling `opengrep.exe`** (Lattice would
   then owe LGPL licence text + a source pointer).

The Commons Clause bars *selling* a product whose value derives substantially
from those rules (a hosted-Lattice concern, not the source). So
`opengrep-archived` is `defaultEnabled: true` once installed (the only real
TypeScript/Node/Express coverage) while its DOWNLOAD stays a click with the
licence named on the Settings row and a no-resale confirmation. Never change:
nothing fetched without a click, nothing committed.

## Map

- `types.ts` — the wire types (status, packs, scan records + envelope, graph
  result, findings, triage, reviews, global + project settings), type-only and
  node-free: the frontend re-exports them via `../shared/wireTypes.ts`. Each
  original module re-exports its own, so import from there as before. Change
  a payload shape HERE; never import a runtime module from it.
- `versions.ts` — `OPENGREP_VERSION`, per-asset `{sha256, bytes}`,
  `OPENGREP_RULE_PACKS` (full-commit pins). The digest block is written ONLY by
  `scripts/opengrep-pin.mjs` (repo root), which Sigstore-verifies every asset
  (`cosign verify-blob` vs `OPENGREP_SIGNING_IDENTITY`) and refuses
  unverified digests — never hand-edit.
- `paths.ts` — engine/packs/state under `~/.lattice/opengrep/`, scans under
  `per-project/<hash>/opengrep/`, optional read-only `<project>/.opengrep/rules/`.
- `state.ts` — `state.json`. Display/scan reads are lenient;
  `updateOpengrepState` reads strictly and never writes over an unreadable
  file (it would drop `binary` + the other packs).
- `platform.ts` / `detect.ts` — the asset is picked automatically (never by the
  user); `resolveOpengrep()` prefers a PATH install (never override a
  package-manager copy); the `--version` probe doubles as the
  antivirus-quarantine check.
- `install.ts` — stream + hash → size vs pin → digest vs pin → atomic rename →
  `--version` → state. Single-flight, with the pending start cached
  SYNCHRONOUSLY before the `chooseAsset` await (else two POSTs race
  `rm`/`rename` and report a bogus quarantine). Leftover `.part` files are
  removed/swept. **Never at boot.**
- `rules.ts` — pack install/remove facade (`fetchPackCommit` → `prunePackTree`
  → swap → state, under `withRulesMutation`). The swap puts the old install
  BACK if the new tree can't be renamed in. Per-pack single-flight (DELETE
  mid-install → 409 `installing`); removal cancels that pack's running install,
  which discards its tree — a removal is never silently undone.
- `rulePackFetch.ts` — shallow fetch of the pinned commit, verify HEAD == pin,
  drop `.git` (content-addressed: tarball bytes aren't stable). Git runs with a
  timeout and credential prompts disabled, so it fails fast.
- `rulePackTree.ts` — `prunePackTree` keeps only rule YAML (top-level `rules:`,
  not `*.test.yaml`) + root LICENSE/README and drops the pack's `prune`
  folders (`qodana-mit`: `jetbrains/`, `rules/lgpl/` — the licence boundary).
  `sweepStalePackDirs` touches only THE SAME pack's `.tmp-`/`.old-` siblings:
  installs of different packs may overlap. `rulePackError.ts` breaks a cycle.
- `rulesGate.ts` — reader/writer exclusion: a scan holds a read slot from
  resolving packs until its record is stored; `withRulesMutation` blocks NEW
  reads, then waits (install swap, bounded) or throws `OpengrepRulesBusyError`
  (removal). Writer-preferring. The routes' `isAnyOpengrepScanRunning()` is only
  a fast path — the gate also covers late swaps and workflow/MCP scans.
- `settings.ts` — machine-global `globalSettings.opengrep.packs` + per-project
  `userSettings.opengrep` (floor, budget, ignores, excludes); sanitized on READ.
- `scan.ts` — single-flight execution, error classes, run state (recent
  failures for the poll route), cancel/abort (cancelled workflow runs abort via
  the request `signal`). `scanArgs.ts`: targets, jobs, engine args.
  `scanRecords.ts`: last 10 scans (`<id>.json` + `.snapshot`/`.cache`/`.meta`
  sidecars). `scanCache.ts`: incremental-reuse identities.
- `digest.ts` — `buildDigest`; re-exports `parseOutput.ts` (parse, matchers)
  and `renderDigest.ts` (budgeted markdown). Import `digest.ts`.
- `graph.ts` — complete per-file findings for the Security overlay (no caps).
- `service.ts` — THE facade routes, MCP tools and the workflow hook call.
- `triage.ts`, `review*.ts` — finding dispositions and interactive security-
  review conversations (routes: `../routes/opengrepReview.ts`; scratch:
  `../homeScratch/CLAUDE.md`).

## Invariants

**Triggering.** Never scan on graph load, file change, project switch or a
timer — only on an explicit click/request. Nothing installs at boot.

**Scans.**
- Engine **cwd = the rules root, packs as RELATIVE ids**: `check_id` derives
  from the config path relative to cwd and fingerprints hash it, so any other
  cwd makes them machine-specific. Local rules go as absolute `-f` paths
  (stable per machine only).
- Targets are CONFINED to the project (`OpengrepBadTargetError` → 400).
- One scan per project (409 `busy`); a hard wall-clock timeout kills it.
- `.meta.json` is promoted LAST, so incomplete snapshots never enter history.
- Cancel/abort kills the engine, stores nothing, frees the slot at once (409
  `scan-cancelled`); cancel matches the exact id, so a stale chip can't cancel
  a newer scan. A `process` `exit` handler aborts running scans — no orphaned
  engine writing an unrecorded `-o` file after a restart.
- `startProjectScanWithDigest` callers MUST observe `done` (else an unhandled
  rejection).

**Incremental reuse** — explicit `mode: incremental` only; default `full`
always runs the engine. When unsure, rescan: any missing/unsupported cache,
engine/rule/context change or unrepresentable include falls back to full with
`record.update.reason`. Never follow symlinks/reparse points; keep path casing
in CLI includes. Reuse is validated for Opengrep 1.30.0 only; git index/ignore
changes, external git config, linked git dirs and linked rules disable it.
Partial/error paths, skipped rules and files edited mid-analysis are never
reused as clean; zero-finding coverage comes only from engine `paths.scanned`;
deleted/renamed paths drop out. Corrupt cache metadata disables reuse without
hiding saved findings; severity/ignore changes re-filter, never invalidate.

**Digest** (what agents see):
- Filter FIRST (severity floor, ignore lists), then dedupe by fingerprint.
- Hard byte budget. "Scan caveats" render first and are reserved from it. An
  oversized group is re-rendered TRIMMED before being cut, so a huge ERROR rule
  never drops while small INFO groups stay; the tail names what was omitted.
- Short fingerprint (first 16 hex + `_N`) is what the digest prints and agents
  put in tasks as `opengrep:<fp>`; every matcher accepts full or short,
  case-insensitively, with or without `opengrep:`.
- Native `extra.is_ignored` findings stay in the raw inventory but never in
  digests or graph colors.

**Graph.** Unvisited files never read as clean; partial parses/errors keep
coverage uncertain. Only open shown findings color the graph, but below-floor
and ignored/deferred ones are kept — presentation never destroys evidence.

**Triage and review.**
- Triage is presentation only (never a scanner-input or CI exclusion); ignore
  needs a reason, defer an owner + future date; expired exceptions read open; a
  local reopen can't override source suppressions or Settings ignores; corrupt
  state is never replaced.
- One active review per project. Its store holds metadata only. The brief makes
  the agent WAIT for the user's explicit choice and create only agreed tasks
  (Open, never run/merged).
- Session metadata is persisted BEFORE spawn. Stop (Pi: `agent_settled`) only
  marks awaiting-decision — never collects a report, kills the PTY or deletes
  scratch. Cancel blocks terminal restore durably before guarded cleanup.
- An unreachable terminal server is never evidence of death; only an absent,
  unregistered PTY past a grace period is closed.

## Consumers

- `../routes/opengrep.ts` — `POST /scan` `async: true` waits ≤ 15 s then
  answers `202 {scanId}` (`acceptImmediately`: at once, so early cancel can
  target it). `GET /scans/:id`: 202 while running, the POST's error once
  failed, 404 after a restart.
- `../latticeMcp/` — `opengrep_scan` polls the async form (Node's fetch drops a
  response after 300 s, under the 10 min scan cap). `opengrep_ignore` →
  `addOpengrepIgnores` exists **outside task worktrees only** (an untrusted
  worktree brief must not silence findings its own change introduced). It is
  the ONE Lattice-settings write a planning agent may make: additive, deduped,
  merged under the settings lock on a strict read (`updateUserSettings`) so
  bursts and Settings saves aren't clobbered; removal is in Settings → Tools.
- `../workflowRuns/stepTools.ts` — agent step with `tools: [opengrep]`: scan →
  `OPENGREP_FINDINGS.md` beside `WORKFLOW_STEP.md` → `{{tool_reports}}`. A
  missing engine / no rules / busy / failed scan never fails the step.

## Tests

Named after the module — grep `opengrep` in `backend/src/__tests__/`.
`opengrepRealCache` is opt-in: set `LATTICE_TEST_OPENGREP_BINARY` (Windows
also `LATTICE_TEST_OPENGREP_USERPROFILE`, for the engine child only).
