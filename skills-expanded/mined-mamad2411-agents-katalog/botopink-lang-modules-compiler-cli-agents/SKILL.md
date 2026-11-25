# compiler-cli

> Path: `modules/compiler-cli/`
> Parent: [`../AGENTS.md`](../AGENTS.md)
> Docs: [`./docs.md`](docs.md) · Examples: [`src/cli/examples.md`](src/cli/examples.md)

Package that builds the `botopink` CLI executable. Depends on `compiler-core`.

## Tree

```text
compiler-cli/
├── AGENTS.md            ← you are here
├── build.zig            ← package build graph + `run` + `test` steps
├── build.zig.zon        ← dependency manifest (compiler-core)
├── tests/               ← end-to-end CLI scripts (NOT in `zig build test`)
│   ├── std_erlang.sh        ← `bp test --target erlang` over libs/std
│   ├── mutual_recursion.sh  ← forward-ref + mutual recursion runs on every backend
│   ├── mutual_recursion/    ← fixture project for the script above
│   ├── backend_exec.sh      ← backend EXECUTION parity (numeric/records/modules
│   │                          on node/erlang/beam/wasm); `zig build test-backends`
│   ├── backend_exec/         ← numeric + records fixture projects
│   ├── test_tooling.sh      ← `botopink test` behaviours: empty test, --filter
│   │                          (multi / none), assert-message, mixed pass/fail exit
│   └── test_tooling/         ← pass + fail fixture projects
└── src/
    ├── AGENTS.md
    ├── docs.md          ← argv parser layout, dispatch flow
    ├── main.zig         ← argv parser, subcommand dispatcher
    └── cli/             ← one file per subcommand + shared helpers
        ├── AGENTS.md
        ├── docs.md      ← subcommand pipeline + shared helpers
        └── examples.md  ← `botopink` command recipes
```

## Commands

```bash
zig build               # produce ./zig-out/bin/botopink
zig build run -- help
zig build run -- version
zig build test          # CLI unit tests (e.g. the generic lib loader)

# End-to-end scripts under tests/ build the CLI + spawn runtimes, so they are
# NOT part of `zig build test` — run them directly:
bash modules/compiler-cli/tests/std_erlang.sh        # stdlib suite on erlang
bash modules/compiler-cli/tests/mutual_recursion.sh  # mutual recursion on every backend
bash modules/compiler-cli/tests/backend_exec.sh      # numeric/records/modules per backend
bash modules/compiler-cli/tests/test_tooling.sh      # `botopink test` behaviours

# backend_exec.sh is also reachable from the repo root as a single build step
# (skips any absent runtime; sets BOTOPINK_SKIP_BUILD so it reuses the install):
zig build test-backends
```

> **Pinned backend reds** (recorded, not regressions — Front-A codegen gaps that
> `backend_exec.sh` surfaces and keeps visible): BEAM mis-codegens integer
> arithmetic combined with calls (`f(n-1) + …` / 2-arg arithmetic calls trip
> `beam_validator`), `case…of` enum dispatch (returns the wrong arm), and lambdas
> (a `#Fun` mis-applied to `*`); the erlang backend emits cross-module package
> calls unqualified (`area` vs `geometry:area`). The harness builds these (erlc
> must accept the asm) but treats the run as informational, flagging loudly if a
> red ever starts passing so the pin can be promoted to a hard assert.

## External libs (generic loader)

`cli/libs.zig` is the driver-side half of the lib-agnostic package mechanism. A
project's `botopink.json` `dependencies: ["<name>", …]` are resolved from disk
against an ordered **root list** (`resolveLibRoots`): walking up from cwd, each
ancestor `D` contributes — when present — `D/repository/botopink-lang/libs`
(bundled libs), `D/repository` (sibling projects), and `D/libs` (legacy flat
tree), de-duplicated nearest-first. `<name>` resolves to the **first root**
holding `<name>/botopink.json`; the loader reads its `{src, files}` and feeds the
lib's modules into compilation prefixed by name (`<name>/<module>`). On today's
flat tree only the `D/libs` branch fires, so the list is `[<ancestor>/libs]` —
byte-identical to the former single-root walk. The compiler core never names a
lib — it just sees ordinary `Module[]` and resolves `from "<name>"` through the
shared import registry. `std` is the one embedded exception and is not loaded
here. `shipMjsSidecars` resolves an owning lib's `.mjs` through the same root
list.

**Unknown `botopink.json` fields are ignored.** `LibManifest` reads only `src`
and `files`; the project loader (`config.zig`) reads `dependencies`/`entry`/etc.
Anything else — including the bpmp-facing `botopink` (compiler version
constraint) and `requires` (per-dep version constraint) added in v0.beta.18 —
passes through untouched. Adding a new optional field to `botopink.json`
requires no change here. Full schema lives in
[`docs/botopink-json.md`](../../docs/botopink-json.md).

## Env

| Variable              | Read by                                  | Effect                                                                 |
| --------------------- | ---------------------------------------- | ---------------------------------------------------------------------- |
| `BOTOPINK_LIB_ROOTS`  | `cli/libs.zig:resolveLibRoots`           | Prepends extra lib roots before the walk-up roots.                     |

**`BOTOPINK_LIB_ROOTS` contract:**

- Path separator: `:` on POSIX, `;` on Windows (matches `PATH`; via
  `std.fs.path.delimiter`).
- Entries are prepended to the walk-up result, then the combined list is
  de-duplicated first-occurrence-wins (so an env entry always shadows a
  duplicate walk-up root).
- Non-existent entries are **silently dropped** — a typo must not break a
  build that does not need the missing root.
- Empty entries (`a::b`, trailing `:`) are dropped.
- Relative entries are resolved against the process cwd.
- Unset or empty value → byte-identical to the legacy resolver
  (`zig build test` on `BOTOPINK_LIB_ROOTS=` matches the unset baseline).

The same hook is mirrored in
[`language-server/src/project_graph.zig:resolveRoots`](../language-server/AGENTS.md#env)
and
[`lib-test-runner/src/discovery.zig:resolveRoots`](../lib-test-runner/AGENTS.md#env)
so the CLI, the LSP, and the lib-test runner always see the same root list.
bpmp uses it to point spawned compilers at its package store
(`$BPMP_HOME/packages/<name>/versions/<v>`).

## CLI behavior contract

- Exit `0` on success, non-zero on command failure.
- All user-facing status/errors must go through `src/cli/reporter.zig`.
- Keep command options aligned with help text in `src/main.zig` and the
  `cli/<cmd>.zig` implementation.

### `botopink test` output format (§T)

Each `test "name" { … }` block emits a fixed envelope so downstream
tooling (lib-test-runner, IDE test panels, future `--json` consumers)
can parse per-test outcomes without scanning ad-hoc prose:

```
TEST <file>:<line> <name>
----- RUN LOG -----
\`\`\`logs
<captured stdout>
\`\`\`
  duration <ms>ms
  ok   <name>          | (or)
  FAIL <name>  (<err>)  at <file>:<line>
```

`  duration <ms>ms` lands between the fence-close and the ok/FAIL line
(monotonic clock around the test body). Older parsers that don't
recognise the line skip it — forward-compatible by construction.

The runner closes with a single summary line: `<P> passed, <F> failed`.
Exit code is non-zero when any test fails.

**Backend status**:
- commonJS — emits the envelope; stdout is captured per-test via a
  `process.stdout.write` override restored after each `t.fn()`.
- erlang — emits the envelope; the body's `io:format` calls land
  inside the fence via the synchronous group-leader path (no explicit
  capture).
- beam_asm — follow-up; needs `call_ext_only` to `io:put_chars/1`
  for the envelope markers around each test invocation.
- wat — gated on `botopink test --target wasm` wiring (Frente A §C2).

**`--json` / JSONL mode**: shipping. `botopink test --json` captures each
child runner's stdout, parses the §T envelope above, and re-emits one
JSON object per line to its own stdout (stderr passes through). Schema:

- per test: `{"event":"test","module":"<src-name>","file":"<path>",
  "line":<u32>,"name":"<test name>","status":"ok"|"fail",
  "run_log":"<captured stdout>","duration_ms":<u32>,
  "error_message":"…","error_file":"…","error_line":<u32>}` — the
  three `error_*` keys appear only on `"status":"fail"`;
  `duration_ms` appears only when the envelope carries a `  duration
  <ms>ms` line (always on current commonJS + erlang runners, omitted
  by older builds). Strings are RFC 8259 §7 escaped (embedded
  newlines surface as `\n`).
- end of run: `{"event":"summary","passed":<P>,"failed":<F>}` — a
  single record aggregated across every module the run touched (not
  per child), so consumers see exactly one terminal record per
  invocation.

The sentinel parser lives in `cli/test_cmd.zig` (`emitJsonl` +
`parseFailLine` + `parseDurationMs`). Forward-compatible: unknown
envelope lines are skipped.

Text mode (no flag) is unchanged: stdio is inherited so the runner
streams the §T envelope live to the user's terminal.

See [`src/AGENTS.md`](src/AGENTS.md) for the dispatch flow and
[`src/cli/AGENTS.md`](src/cli/AGENTS.md) for the per-command list.

## Tagging

`compiler-cli` is auto-tagged on push by
[`../../.github/workflows/tag.yml`](../../.github/workflows/tag.yml) (path
filter: `modules/compiler-cli/**`):

- `compiler-cli/<version>-feat` — moving; force-updated on each feat push.
- `compiler-cli/<version>` — immutable; created once per master/main push.
  Re-push without bumping `botopink.json.version` → red gate.

`<version>` is `botopink.json.version` (this module's local manifest, NOT
the workspace `v*` release tags). Bumping the tag is a one-line edit to
`botopink.json` in the same PR that lands the changes you want tagged.
Spec: [`tasks/v0.beta.18/specs/module-auto-tag.md`](../../tasks/v0.beta.18/specs/module-auto-tag.md).
