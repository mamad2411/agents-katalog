# Backend scripts

The user owns the running dev console. Agents must not start, stop or restart
dev servers; follow the task's verification policy.

## Script index

- [dev.mjs](dev.mjs) is the backend dev-runner entrypoint: self-heal dependencies,
  initial compile/assets, start the compiled backend, supervise compilation and
  `dist/` changes, then shut down. Keep it as readable lifecycle wiring.
  Helper navigation and operational invariants live in [dev/CLAUDE.md](dev/CLAUDE.md).
- [copy-assets.mjs](copy-assets.mjs) copies the explicit non-TypeScript runtime
  assets from `src/` to `dist/`. Keep the list aligned with runtime readers;
  TypeScript does not emit these files. Both build and dev paths use this script.
  Equal destination bytes skip the write, preventing asset-copy restart loops.
  Its regression owner is [devCopyAssets.test.ts](../src/__tests__/devCopyAssets.test.ts).

## Runner boundaries

Run compiled `dist/index.js` with plain Node. Loader injection can propagate
through child environments into native PTY helpers; preserve startup behavior,
exported helper contracts and exact log messages.

Keep long-lived child, watcher and timer ownership in `dev/` helpers. The local
guide owns compiler repair, backend respawn, output baselines, lock deferral,
drain handshakes, soft/full shutdown and exit-log retention. Existing `.d.mts`
files mirror the helper contracts consumed by TypeScript, including regressions.

Backend restarts preserve the detached terminal-server and agent PTYs. Only a
real shutdown requests terminal-server termination; soft console stops preserve
sessions for re-adoption. Control-pipe wiring is covered by
[devControl.test.ts](../src/__tests__/devControl.test.ts).

## Related owners

- [Root scripts](../../scripts/CLAUDE.md): preflight, orchestration, console
  commands, shared dependency checks/watches; the outer supervisor's logs are in
  [scripts/orchestrate](../../scripts/orchestrate/CLAUDE.md).
- [Backend source](../src/CLAUDE.md): application boot and subsystem navigation.
- [Restart drain](../src/restartDrain/CLAUDE.md): backend admissions and state flush.
- [Project run locks](../src/projectRunLock/CLAUDE.md): lock ownership and liveness.
- [Terminal-server](../src/terminalServer/CLAUDE.md): detached PTY process ownership.
- [Crash logging](../src/crashLog/CLAUDE.md): backend live mirrors and crash adoption.
