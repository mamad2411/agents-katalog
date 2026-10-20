# AGENTS.md -- scripts/

Repo-wide tooling: environment doctor, full-stack orchestrator, and supporting glue.
All files are TypeScript; executed directly by Bun (no compile step).

## What this is

| Tool | Purpose |
|------|---------|
| `doctor/` | Probes all apps + services and reports health in a matrix |
| `stack/` | Full-stack launcher: Docker, migrations, host apps, readiness polling, teardown |
| `doctor.ts` | Entrypoint that wires `doctor/apps.ts` into a runnable CLI |

Nothing in `scripts/` is published. It runs locally and in CI only.

## Layout

```
scripts/
├── doctor.ts                  # doctor CLI entrypoint
├── doctor/
│   ├── apps.ts                # APPS registry (data-driven: add/remove apps here)
│   ├── coverage-summary.ts    # Coverage report aggregator
│   ├── probe-http.ts          # HTTP probe utility (GET + timeout)
│   └── spawn-app.ts           # Spawn + readyMatcher logic; AppEntry / AppKind types
└── stack/
    ├── launch.ts              # stack:full entrypoint (all phases, all flags)
    ├── heartbeat.ts           # Elapsed-time ticker for long-running phases
    ├── health.ts              # pollUntilReady + pollUntilReadyWithProgress
    ├── stream.ts              # pipeWithPrefix — colored, line-buffered subprocess output
    ├── services.ts            # SERVICES registry (Docker service definitions)
    ├── open-url.ts            # Phase 5.5 browser/surface opener
    ├── cleanup.ts             # Docker volume + network cleanup helpers
    ├── run-cleanup.ts         # CLI shim for cleanup.ts (volumes / nuke)
    ├── teardown.ts            # Graceful teardown: kill procs + compose down
    ├── teardown-pids.ts       # PID-file-based teardown for stack:down
    ├── pid-file.ts            # PID file read/write helpers
    ├── package.json           # @t/stack-scripts workspace (vitest runner)
    ├── vitest.config.ts       # Vitest config for stack/ tests
    └── __tests__/
        └── stream.test.ts     # Unit tests for pipeWithPrefix
```

## Entry points

| Script target | Resolved file |
|---------------|--------------|
| `bun run doctor` | `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\scripts\doctor.ts` |
| `bun run up` / `bun run stack:full` | `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\scripts\stack\launch.ts` |
| `bun run stack:down` | `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\scripts\stack\teardown-pids.ts` |
| `bun run stack:clean` | `stack:down` then `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\scripts\stack\run-cleanup.ts volumes` |
| `bun run stack:nuke` | `stack:clean` then `run-cleanup.ts nuke --force` |

## Invocation patterns

```bash
# Full stack (Docker + migrations + all apps + auto-open browser)
bun run up

# Skip mobile / desktop host processes
bun run stack:full:apionly        # --no-mobile --no-desktop
bun run stack:full:nodocker       # --no-docker (infra already running)

# Launch flags for launch.ts
--no-mobile    Skip Expo host process
--no-desktop   Skip Electron host process
--no-docker    Skip docker compose phase
--no-open      Skip browser-open phase
--open=<csv>   Open only named surfaces (website,web,api,mobile,desktop)
--quiet        Suppress per-service log streaming
--no-matrix    Skip doctor matrix render at the end

# Teardown / cleanup
bun run stack:down                # Kill PID-tracked procs + compose down
bun run stack:clean               # stack:down + remove Docker volumes
bun run stack:nuke                # stack:clean + remove networks and images

# Doctor only
bun run doctor

# Stack tests (Vitest, run from repo root or scripts/stack/)
bun run test --filter=@t/stack-scripts
```

## Conventions

- **TypeScript everywhere.** No `.js` files; Bun runs `.ts` directly.
- **Tests alongside source.** Unit tests live in `__tests__/` inside the same package directory.
- **Test runner: Vitest** (not Bun test) inside `scripts/stack/`. Check `package.json` before running.
- **Adding an app to doctor:** edit `scripts/doctor/apps.ts` — the `APPS` array is the sole registry; all other logic is table-driven.
- **Adding a Docker service:** edit `scripts/stack/services.ts` — the `SERVICES` array drives Phase 2 and the idle status box.
- **LEFTHOOK_EXCLUDE and `--no-verify` are forbidden** — if a hook fails, fix the underlying issue.
- **No secrets in scripts.** Use `.env.docker` / Railway env vars; scripts read `process.env` only.

## Links

- Root AGENTS.md: `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\AGENTS.md`
- Root README: `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\README.md`
- Doctor apps registry: `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\scripts\doctor\apps.ts`
- Stack launch phases: `C:\Users\jager\OneDrive\Documents\GitHub\template-repo\scripts\stack\launch.ts` (lines 1-28, phase comments)
