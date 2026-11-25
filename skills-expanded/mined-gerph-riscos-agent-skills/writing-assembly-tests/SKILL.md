---
name: writing-assembly-tests
description: Write and test small ObjAsm command-line exercisers under `testcode/s`, including optional reuse of Pyromaniac suites through a build-service runner when a repository needs to ship module tests outside the main Pyromaniac tree.
metadata:
  author: gerph@gerph.org
license: MIT
allowed-tools: Bash(riscos-run:*)
---

# Writing tests in assembly

Use this skill when adding or updating a small ARM assembly test program in
`testcode/s/` which exercises SWIs, commands, or module entry points through a
simple command-line interface.

## Workflow

1. Create `testcode/s/<toolname>` as an ObjAsm source.
2. Include the standard helper headers:
   - `GET hdr.swis`
   - `GET hdr.printmacros`
   - `GET hdr.macros`
3. If the tool needs argument parsing beyond a single character dispatch, reuse
   the helper routines from `assets/testcode/s/_args_common`.
4. Build the tool with `make testcode` or `make -C testcode bin/<toolname>`.
5. Run it manually with:

   ```bash
   ./pyro.py --load-internal-modules testcode/bin/<toolname> <args>
   ```

6. Add a suite `testcode/tests-<name>.txt` and expectation files under
   `testcode/expect/...`.
7. Run the suite with:

   ```bash
   make tests TEST=<name>
   ```
8. When committing the test, include the built binary in
   `testcode/bin/<toolname>` as well as the source and expectations. In this
   environment CI runs the tests but does not build the test binaries first, so
   the checked-in binary is part of the test asset.

When extending an existing suite with another assembly exerciser, prefer adding
another `Test:` entry alongside the existing one rather than creating a fresh
group unless the public interface being exercised is genuinely separate.

## Optional build-service reuse pattern

Some component repositories do not run the tests inside a full Pyromaniac
checkout. Instead they:

1. Keep the assembly exercisers and expectations in a local `testcode/` tree.
2. Treat `tests-<name>-pyro.txt` as the source suite lifted from Pyromaniac.
3. Generate a local `tests-<name>.txt` by rewriting the Pyromaniac-specific
   `Command:`, `Expect:`, `Replace:`, and path forms.
4. Bundle the module under test, the test binaries, and the harness scripts.
5. Run the resulting suite through a local copy of `test.pl` using a runner
   such as `run-on-build-service.sh`.
6. Have that runner translate Pyromaniac-style options into a `.robuild.yaml`
   script and submit the archive with `riscos-build-online`.

Use this only when the repository needs Pyromaniac-compatible tests without
depending on the whole Pyromaniac tree. Not every assembly-test repository
needs this extra layer.

## Reliable setup sequence for the build-service pattern

When restoring the bundled build-service example into a repository, do the
setup in this order so the generated suites and `make tests` target work
first time:

1. Copy the bundled `assets/buildservice-example/testcode/` tree into the
   repository `testcode/` directory.
2. Copy in any additional helper headers and helper sources your specific
   tests need, such as `hdr/vdu`, `hdr/osplot`, `hdr/osspriteop`, or local
   `s/_*.common` helpers that are not part of this skill bundle.
3. Update `testcode/Makefile`:
   - set `MODULE = <module-under-test>`
   - update the `tests:` prerequisite list to name the generated suites your
     repository uses
   - add any extra copied module binaries required by the tests
4. Update `testcode/run-on-build-service.sh`:
   - set `files=(...)` to include the built test binaries and any data
     directories needed at runtime
   - set `modules=(...)` to the modules that must be `RMLoad`ed before the
     test command runs
5. Add `tests-<area>-pyro.txt` files as the source suites lifted from
   Pyromaniac or written in the same style.
6. Keep any non-Pyromaniac tests, such as ad hoc BASIC smoke tests, in plain
   `tests-<name>.txt` files. Do not route those through the Pyromaniac
   transform rule.
7. Put the simpler assembly-based suites first in `tests.txt`. Place heavier
   smoke tests such as BASIC runners later, because the assembly tools usually
   provide the more fundamental interface coverage with fewer dependencies.
8. Build the assembly tools with `make` in `testcode/`.
9. Regenerate any transformed local suites with commands such as
   `make tests-<area>.txt` after editing `tests-<area>-pyro.txt`.
10. Run the suites with `make tests`.

If `make tests-<name>.txt` reports no rule for a generated suite, check that:

- `tests-<name>-pyro.txt` exists with the exact matching stem
- `transform-pyro-tests-to-buildservice.sh` is present and executable
- the suite is intended to be generated, rather than being a hand-written
  non-Pyromaniac test file

If the generated suite exists but still appears to run stale commands or
expectations, rebuild it explicitly before debugging anything deeper.

## Asset layout

This skill stores non-documentation files under `assets/` using the same names
and relative paths they would have in a `testcode/` source tree.

That is intentional. If you reuse one of these bundled files, copy it back into
the matching location in the target tree:

- `assets/testcode/s/_args_common` -> `testcode/s/_args_common`
- `assets/testcode/s/urlfetcher` -> `testcode/s/urlfetcher`
- `assets/testcode/hdr/macros` -> `testcode/hdr/macros`
- `assets/testcode/hdr/printmacros` -> `testcode/hdr/printmacros`
- `assets/testcode/hdr/swis` -> `testcode/hdr/swis`
- `assets/testcode/Makefile` -> `testcode/Makefile`
- `assets/testcode/tests-pymodules-urlfetcher.txt` -> `testcode/tests-pymodules-urlfetcher.txt`
- `assets/buildservice-example/testcode/...` -> copy the contents of that
  bundled example tree back into a real repository `testcode/` directory

The build-service example bundle also includes optional common files that may
be useful when the copied test sources depend on them:

- `assets/buildservice-example/testcode/hdr/vdu` -> `testcode/hdr/vdu`
- `assets/buildservice-example/testcode/hdr/osplot` -> `testcode/hdr/osplot`
- `assets/buildservice-example/testcode/hdr/osspriteop` -> `testcode/hdr/osspriteop`
- `assets/buildservice-example/testcode/s/_args_common` -> `testcode/s/_args_common`
- `assets/buildservice-example/testcode/s/_dump_common` -> `testcode/s/_dump_common`
- `assets/buildservice-example/testcode/s/_colourtrans_common` -> `testcode/s/_colourtrans_common`
- `assets/buildservice-example/testcode/s/_screenmode_common` -> `testcode/s/_screenmode_common`
- `assets/buildservice-example/testcode/.gitignore` -> `testcode/.gitignore`

Do not drop them into the destination with their skill-bundle path unchanged.
The assembler expects names such as `s/<toolname>` and `hdr/<header>` inside
the real source tree.

## What to read

Read the documentation in `references/` and use the concrete files in
`assets/testcode/` as copyable examples:

- `workflow.md` for the expected repository pattern
- `assets/testcode/s/_args_common` for the shared argument parsers
- `assets/testcode/hdr/macros` for `Push`, `Pull`, `XSWI`, `XBL`, and `SIGNATURE`
- `assets/testcode/hdr/printmacros` for `PrintMessage`, `PrintInteger`, `PrintHex`, and string helpers
- `assets/testcode/hdr/swis` for the shared SWI symbol definitions
- `assets/testcode/Makefile` for the exact build rules
- `assets/testcode/s/urlfetcher` for a full command-line exerciser
- `assets/testcode/tests-pymodules-urlfetcher.txt` for a parameterised suite example
- `references/build-service-pyromaniac-reuse.md` for the optional
  build-service bridge pattern
- `assets/buildservice-example/testcode/` for a complete example tree that
  keeps Pyromaniac-style suites, transforms them, and runs them remotely

## Style that matches this tree

- Keep the entry point small: move `R1` to `R8`, then dispatch on short option
  letters.
- When an operation needs a filename, URL, sprite name, or other string
  argument, prefer a small local `read_string` routine in the style of
  `testcode/s/sprite_plot` so the value can be supplied at runtime.
- Print plain text results that are easy to compare in expectation files.
- Use one-letter actions when that keeps the command line compact and makes
  grouped tests easy to write.
- Prefer exercising one interface per verb, then compose verbs in the test
  `Args:` string.
- If the tool already has a built-in table-validation or self-checking mode,
  prefer driving that single mode from the suite and comparing its full output.
  This keeps the assembly binary as the canonical source of the case table.
- Keep helper state in static storage near the end of the file, following the
  existing `testcode/s/*` pattern.
- Avoid compiling host-specific test data paths into the binary when the value
  can be passed in from the test harness. This matters especially for
  cwd-sensitive `file:` URLs.
- If the assembly source changes, rebuild and commit the matching
  `testcode/bin/<toolname>` binary in the same change so the repository remains
  runnable by CI and by other developers.

## Test suite pattern

A common group-level pattern is:

```text
Group: Module: Operations
Command: $TOOL --load-internal-modules bin/<toolname> $ARG1
Expect: expect/<area>/<toolname>/<toolname>_$ARG1

Test: Do one scenario
Args: abc
```

That lets each `Args:` string describe a whole scenario while keeping the suite
file short.

If a scenario needs setup parameters, put them directly into the argument
string. For example, a fetch test may prepend `f<url>,` before the operation
verbs so the same tool can be reused with different URLs.

For build-service runners and transformed local suites, remember that the
invoked RISC OS command path will usually use dotted form such as
`bin.<toolname>`, even though the host-side Pyromaniac source suite may mention
`bin/<toolname>`. If you invoke the bridge script manually, use the same dotted
form that the transformed local suite would pass.

## Build-service example assets

The bundled example under `assets/buildservice-example/testcode/` captures a
component-repository pattern for reusing Pyromaniac assembly tests elsewhere.
The important files are:

- `Makefile` to build `s/*`, copy in the module under test, transform
  `tests-*-pyro.txt`, and invoke `test.pl`
- `transform-pyro-tests-to-buildservice.sh` to normalise Pyromaniac suites for
  non-Pyromaniac execution
- `run-on-build-service.sh` to turn Pyromaniac-style command-line switches into
  `.robuild.yaml` commands and submit them with `riscos-build-online`
- `test.pl` as the repository-local copy of the tooltester harness
- `tests.txt`, `tests-sysvars-pyro.txt`, and `tests-sysvars.txt` as a source
  suite plus generated output
- `s/var_read`, `s/var_set`, `hdr/*`, and `expect/var/*` as a complete sample
  test tree
- optional extra headers such as `hdr/vdu`, `hdr/osplot`, and
  `hdr/osspriteop`
- optional shared helper sources such as `s/_args_common`,
  `s/_dump_common`, `s/_colourtrans_common`, and `s/_screenmode_common`
- a sample `.gitignore`

That example is intentionally concrete. Reuse the structure and scripts, then
replace the module names, uploaded files, assembly exercisers, and expectation
files for the target repository.

For repositories that mix transformed Pyromaniac suites with local smoke tests,
keep the generated `tests-*-pyro.txt` source files alongside any hand-written
plain `tests-*.txt` files. Only the Pyromaniac-derived suites should use the
automatic `tests-%.txt: tests-%-pyro.txt ...` conversion rule.

Do not run multiple copies of the bundled build-service runner in parallel from
the same `testcode/` directory unless you have first made its temporary file
handling unique. The simple example runner writes a shared `.robuild.yaml`, so
parallel invocations can interfere with each other.
