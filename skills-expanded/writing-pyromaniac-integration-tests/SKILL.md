---
name: writing-pyromaniac-integration-tests
description: Create or update integration tests in the Pyromaniac repository, especially `testcode/tests-*.txt` suites, expectation files under `testcode/expect/`, BASIC smoke tests in `testcode/basic/`, and assembly exercisers in `testcode/s/`.
metadata:
  author: gerph@gerph.org
license: MIT
---
# writing-pyromaniac-integration-tests

Use this skill when wiring a feature into the Pyromaniac integration test
harness.

## Choose the smallest useful test surface

Use `--command` only when a simple OSCLI command is enough.

Use BASIC in `testcode/basic/` when you need:

- `SYS` calls with multiple returned registers
- XSWI error inspection
- loops or a few sequential checks
- simple smoke coverage without building an assembly helper

Use assembly in `testcode/s/` when you need:

- a compact command-line front end for many SWI scenarios
- explicit register-level control
- grouped scenario strings such as `rgsdx`
- reusable exercisers that are easier to drive from `tests-*.txt`

Use the `writing-assembly-tests` skill for the assembly pattern and
`using-bbcbasic` for BASIC specifics.

## Repository workflow

Build assembly helpers:

```bash
make testcode
```

Run one suite:

```bash
make tests TEST=<name>
```

Manual runs:

```bash
./pyro.py --load-internal-modules --command '*Command'
./pyro.py --load-internal-modules testcode/bin/<tool> <args>
./pyro.py --load-internal-modules --load-module "$ROSYSMODULES/BASIC,ffa" \
          --command 'Run TestThing' testcode/basic/TestThing,fd1
```

## Suite structure

Suites live in `testcode/tests-<name>.txt`.

- `make tests TEST=<name>` runs that file directly
- `make tests` needs `testcode/tests.txt` to include it
- `testcode/tests.txt` is the full suite list for normal runs; add new
  `Include: tests-<name>.txt` lines in the appropriate section so the suite is
  part of the standard test set
- expectations live under `testcode/expect/...`
- on mismatch, `testcode/test.pl` writes `<expect-file>-actual`

A common parameterised pattern is:

```text
Group: Module: Operations
Command: $TOOL --load-internal-modules bin/<tool> $ARG1
Expect: expect/<area>/<tool>/<tool>_$ARG1

Test: Do one scenario
Args: abc
```

Scenario arguments can include setup parameters as well as verbs. For example:

```text
Command: $TOOL --load-internal-modules bin/urlfetcher $ARG1

Test: Fetch via file URL
Args: ffile:testdata/urlfetcher.txt,rgsdx
```

That pattern is useful when the tool must accept a runtime URL, filename, or
other string parameter.

Be explicit about cwd-sensitive cases. In particular, relative `file:` URLs in
the Pyromaniac URL fetcher resolve against the process current working
directory:

- under `make tests`, `testcode/test.pl` runs from `testcode`
- manual `./pyro.py ...` runs from the repository root use a different base

So a relative `file:` URL that works in the harness may need a different path
when run manually.

## Updating expectations

When a test fails:

1. read the `-actual` file first
2. compare it with the checked-in expectation
3. decide whether the code regressed or the output intentionally changed

Do not blindly replace expectations without checking whether the interface
change was deliberate.

## Good coverage choices

Prefer a few scenario-driven tests that cover the public contract end to end:

- success path
- expected error path
- edge case or length-only path
- cleanup/deregister/finalise path
- one test that confirms user-visible text or formatting when that output is
  part of the contract
