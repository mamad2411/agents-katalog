---
name: sensorium
description: "Use when debugging a failing test or wrong output in Python, Rust, TypeScript, or C by recording a run and querying the trace, over the sensorium CLI or the sensorium MCP server."
---

# Sensorium

Record one run. Ask the trace. Branch on the exit status before trusting the prose. A run reference is a full id, a unique prefix, or `last`. Event ids (`eN`) and frame ids (`fN`) stay stable for that file, so one answer is the next argument. Traces go to `~/.sensorium/traces`, or `$SENSORIUM_DIR/traces`.

## Loop

1. Record from the project root. Only code under that working directory is traced.
2. `sensorium info last`, then the query that matches the question (`exceptions`, `failures`, `grep`, `flow`, `tree`, `frame`).
3. Exit 0 or 1 is the trace's answer. Exit 2 means fix the command. Exit 3 means the recording cannot settle it: re-record. Do not retry a 3 on the same run, and do not re-record on a 2.
4. Per-line state is opt-in. Re-record with `--focus` (or `sensorium refocus <run> --focus ...`, which re-runs and then says MATCH, DIVERGED, or REFUSED). Then `frame` or `watch`.

## Record

Python 3.12+. The command is a `.py` file, a `-m` module, or a console script. Never `python` itself.

    sensorium run -- <command>
    sensorium run --focus pkg.module:qualname -- pytest tests/test_fog.py
    sensorium run --window QUALNAME --focus pkg.module:qualname -- <command>

`--focus` is repeatable (`pkg.module` or `pkg.module:qualname`) and records per-line capture. `--window` is `QUALNAME` or `MODULE:QUALNAME` and limits that capture to one function. `--include` and `--exclude` are globs against paths relative to the working directory. `--no-children` (or `SENSORIUM_NO_CHILDREN=1`) records the parent only. Otherwise a Python child (`subprocess`, `multiprocessing`, pytest-xdist) joins the same run. A non-Python child is counted and not traced. `--max-events`, `--max-bytes` (for example `8M`), `--max-calls`, and `--no-cap` set the caps. `0` is unlimited.

`run` exits with the target's own status. Exit 2 and no `run:` line means recording was refused.

Rust, Linux, rustc 1.96+ (`cargo install cargo-sensorium`):

    cargo sensorium test [--tier off|call] [--focus <qualname>]... [--max-events N] [--max-bytes SIZE] [--max-calls N] [--no-cap] [cargo test args]
    cargo sensorium run  [--tier off|call] [--focus <qualname>]... [cargo run args]

`--refocus-of` is written by `sensorium refocus`. macOS and Windows refuse to compile the runtime.

TypeScript, Node 24. From a checkout, `npm ci --prefix typescript` first. vitest 4.1 or `node --test`:

    sensorium ts run [--tier off|call] [--focus <spec>]... -- vitest run ...
    sensorium ts run -- node --test ...

A `--focus` spec is `<qualname>` or `<file>:<qualname>`, as `tree` prints it. A shell-free `npm test` that runs vitest or `node --test` is expanded. jest, a shell script, and a vitest project named by a string or glob are refused. Top-level `await` is not recorded. `for await` inside a function is.

C, Linux x86-64, gcc or clang. `-O0` or `-Og` keeps arguments and return values. Other `-O` still records calls.

    sensorium c run -- <cmd>
    sensorium c run --strict -- make test

`--strict` refuses a translation unit whose effective `-O` is not `-O0` or `-Og`. `--no-retval` skips the return trampoline (`SENSORIUM_C_NO_RETVAL=1`).

Python, Rust, and TypeScript stop storing at 100000 events, 8 MiB, or 1024 calls of one function unless a flag, `SENSORIUM_MAX_EVENTS` / `SENSORIUM_MAX_BYTES` / `SENSORIUM_MAX_CALLS`, or `$SENSORIUM_DIR/config.json` says otherwise. Later calls are counted and marked elided. `info` labels INCOMPLETE and TRUNCATED. Neither is a zero.

## Query

    sensorium runs
    sensorium info last
    sensorium tree last --depth 3
    sensorium frame last --fn compute
    sensorium grep last compute --kind RETURN
    sensorium exceptions last
    sensorium failures last
    sensorium flow last --value 1800
    sensorium flow last --object qualname:argname
    sensorium diff RUN_A RUN_B
    sensorium watch last --at module:qualname --expr 'n > 0'
    sensorium refocus last --focus pkg.module:qualname --compact

`tree`: `--root fN`, `--around eN`, `--depth`, `--limit`. Parentage is the caller frame. `frame`: a frame ref, or `--fn` (exact qualname, else one substring; more than one name is exit 2) and `--nth` (1-based). `grep`: substring of the rendered line; `--kind` is `CALL`, `RETURN`, `RAISE`, `HANDLED`, or `LINE`; `--fn`, `--after eN`, `--limit`. `exceptions`: swallowed, uncaught, re-raised, propagated, or ambiguous. SWALLOWED is claimed only when the recording proves it. `failures`: each failed test and the frame it failed in, including a vitest `expect`, a Rust panic, and a C crash or assert in a `test_` frame. `flow`: exactly one of `--value` (equality over captured arguments, returns, and LINE locals; not dataflow) or `--object` (`e<id>:<name>`, `<qualname>:<name>`, or `<qualname>:return`). `diff`: shape `(file, qualname, kind)`, not values. `--context`, `--task NAME`, `--ignore-moves`. `watch`: required `--at` and `--expr`. `--misses` is how many near-misses to show.

## Refocus

`sensorium refocus <run> --focus SPEC` re-runs the recorded command with that focus added to the original focus, then compares the shape. `--window` defaults to the original's. `--compact` prints the verdict and the finding. MCP defaults compact on.

- **MATCH** (exit 0). `refocus verdict: MATCH -- every recorded thread produced the identical CALL/RETURN/RAISE/HANDLED sequence`. The licence lists only checks that ran. A check that could not run withholds it. Same path, not same values.
- **DIVERGED** (exit 1). `refocus verdict: DIVERGED -- ...`. The new trace is a different execution and is queryable. `diff` prints `verdict: DIVERGED at causal step N`.
- **REFUSED before any rerun** (exit 2). Nothing was re-run: the original is INCOMPLETE, consumed stdin, names no command or directory, that directory or target is gone, or `capabilities.refocus` is false. Fix the call or pick another run.
- **REFUSED after a rerun** (exit 3). `refocus verdict: REFUSED -- <new> was recorded and is queryable, but it could NOT be verified against <orig>: treat it as a separate, UNVERIFIED execution`. Query the new trace on its own.

`diff` with no verdict prints `verdict: REFUSED -- cannot issue a MATCH/DIVERGED verdict` (exit 3).

## Exit status

| exit | meaning | next |
|---|---|---|
| 0 | the trace said yes | use it (`grep` matched; `refocus` MATCH; `watch` SATISFIED) |
| 1 | the trace said no, or none | believe it (`matches: 0`; no exceptions; `refocus` DIVERGED) |
| 2 | the call is wrong | edit the command. Ambiguous `--fn`, `--nth` out of range, a run reference that names nothing, `refocus` before any rerun |
| 3 | the trace cannot settle it | change the recording and re-record |

`sensorium run`, `sensorium ts run`, and `sensorium c run` exit with the recorded command's status. They do not use this table. `cargo sensorium` exits with cargo's status.

Over MCP the first line is `exit N:` plus that meaning, or `no answer:` when there is no exit (timeout, cancel). `isError` is set on exit 2 or on no exit: repair the call. 1 and 3 are answers about the trace. `record` and `record_c` say the status is the command's own (`exit 2` there can mean the program exited 2, or recording was refused and there is no trace).

## REFUSED and NOTHING WAS CHECKED

**REFUSED.** `REFUSED: ...` means a capability is missing or this recording cannot answer. Exit 3: re-record with what `info` says the trace lacks. Exit 2: the call is wrong; fix the arguments. The `refocus` and `diff` verdict lines above are the same word for "no verdict".

**NOTHING WAS CHECKED.** Only `watch` prints this, at exit 3, when no recorded site had the names the predicate needs:

    verdict: NOTHING WAS CHECKED -- the predicate could not be evaluated at any of the N recorded site(s)
      'hits: 0' here means 'could not evaluate', NOT 'the invariant held'

That is not a pass. The following lines name the gap and print the re-record command for this recorder (`sensorium run`, `sensorium ts run`, or `cargo sensorium`). Re-record with `--focus` on the function `--at` names, or point `--expr` at names the trace captured. A redacted name has no comparable value. Re-record with `SENSORIUM_REDACT_ALLOW=<name>` only when that value is not a secret. The allow list wins over `SENSORIUM_REDACT_NAMES`.

## Redaction

Rule v1 writes `<redacted>` for a secret-named environment value, and for a secret-named or secret-shaped captured value, before disk. It is not a scanner. A secret in a name the rule has never heard of, or text matching none of its shapes, is stored as typed. Treat a trace as a core dump.

`SENSORIUM_REDACT_NAMES` adds names. `SENSORIUM_REDACT_ALLOW` exempts names. `SENSORIUM_NO_REDACT` set to anything other than `0` turns the rule off (`=0` leaves it on). The key file is `<store>/redaction.key`. `SENSORIUM_REDACT_KEY` is not kept in the recorded environment. `sensorium redact --all --dry-run` shows a rewrite of traces already stored. `redact` is not an MCP tool.

## Limits

Python sees code under the run root, not the stdlib, site-packages, files the program read, non-Python threads, the clock, or the network. A `multiprocessing` spawn is witnessed only on 3.14+ (`_posixsubprocess.fork_exec`). Below that, `refocus` withholds the "no child process witnessed" line. Rust sees the workspace's own crates, on Linux. TypeScript sees eligible ES modules under the invocation root, on Node 24. C sees a Linux x86-64 build. The browser, jest, and top-level `await` are outside the TypeScript recorder.

## Examples

Recorded from this repo on 2026-11-20. A new run renumbers events. `last` still names the trace.

Swallowed rows. `corpus/silent_swallow/main.py` printed `total: 35 from 3 rows` and nothing about the dropped ones.

    sensorium exceptions last
      e9 RAISE   parse_row raise ValueError("invalid literal for int() with base 10: 'x7'") L8
        SWALLOWED at e10 load_all L15 -- caught in f3, which returned normally; never re-raised
      e14 RAISE   parse_row raise ValueError("invalid literal for int() with base 10: '??'") L8
        SWALLOWED at e15 load_all L15 -- caught in f3, which returned normally; never re-raised
    dispositions: swallowed 2

    sensorium grep last carol --kind CALL
    e3 CALL    load_all(rows=list[5]=['alice,10', 'bob,20', 'carol,x7', 'dan,5', 'erin,??'])
    e8 CALL    parse_row(row='carol,x7')
    matches: 2

Grams billed as kilograms. `corpus/unit_mismatch/main.py` printed `total: 5569.0`.

    sensorium flow last --value 1800
      e3 CALL    order_total(items=list[2]=[dict[3]={'name': 'mug', 'price': 12.0, 'grams': 400}, dict[3]={'name': 'kettle', 'price': 49.0, 'grams': 1800}])   [arg items[1].grams]
      e17 CALL    item_weight(item=dict[3]={'name': 'kettle', 'price': 49.0, 'grams': 1800})   [arg item.grams]
      e18 RETURN  item_weight -> 1800   [return]
      e19 CALL    shipping_cost(weight_kg=1800)   [arg weight_kg]
    sightings: 4 event(s), 4 capture(s)

    sensorium refocus last --focus corpus.unit_mismatch.main:shipping_cost --compact
    refocus verdict: MATCH -- every recorded thread produced the identical CALL/RETURN/RAISE/HANDLED sequence
    licence: verified against 20261120-215900-f9cc87

`item_weight` returned grams and `shipping_cost` took that number as `weight_kg`. The MATCH says the rerun was the same path, so that capture describes it.

## MCP

`sensorium mcp --allow-run` offers `record`, `refocus`, and `record_c`. Without `--allow-run` those tools are absent. `--store DIR` is `SENSORIUM_DIR` for the server and its children. `record` takes `command` as an argv array, never a shell string and never `python` itself. Query tools default `run` to `last`. Start the server from the project venv. Tools and the result header: `docs/mcp.md`.
