# tests/factorio/

## Purpose

Disposable Factorio test mod used to exercise LilEinstein's production runtime in an isolated save.

## Ownership

- `lil-einstein-test_0.1.0/data.lua` — test-only void-powered lab plus starved/supplied technology prototypes.
- `lil-einstein-test_0.1.0/control.lua` — delayed runtime assertions, including the authoritative live-research switch from a singleton queue after a 275-lab staggered pass with only 5 labs able to consume the current technology's unique pack.

## Local Contracts

- This mod is never copied into a player's normal mod directory.
- Runtime output is written only through Factorio's `helpers.write_file` into the runner-owned `script-output` directory.
- Assertions must observe public LilEinstein module behavior or initialized storage.
- Research-switch acceptance observes Factorio's read-only `LuaForce.current_research`; internal temporary-queue state alone is not sufficient.
- Research-switch acceptance keeps the alternate out of the explicit queue and proves the starved technology made low but nonzero progress before the switch.
- The scenario continues beyond the minimum temporary-research dwell and asserts the low-stock target is not restored during recovery checks; production elsewhere or packs still in transit are not recovery evidence until enough lab/network-reachable stock exists for the recovery window.
- A production test bridge is permitted only when gated on the active test mod; it may seed LilEinstein's stored queue for scenario setup and expose read-only snapshots, and it must be absent from normal saves.

## Work Guidance

- Keep the test save disposable and bounded.
- Use Factorio 2.0.77+ runtime APIs and guard optional module-load paths with assertions that produce useful output.

## Verification

- Run `powershell -ExecutionPolicy Bypass -File .\scripts\run_tests.ps1 -RequireInGame` from the repository root.

## Child DOX Index

None.
