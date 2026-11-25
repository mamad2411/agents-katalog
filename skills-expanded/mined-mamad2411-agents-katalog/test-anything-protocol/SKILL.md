---
name: test-anything-protocol
description: >-
  Test Anything Protocol (TAP 14): emit and parse TAP test output. Covers TAP 14. Use when emitting TAP output. Triggers: TAP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Test Anything Protocol

TestPoint := ("not ")? "ok" (" " Number)? ((" -")? (" " Description) )? (" " Directive)? "\n" (YAMLBlock)?

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when emitting TAP output.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: TAP 14 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **Whitespace Around Directive Delimiter.** "For example: TAP version 14 # MUST be treated as a SKIP test ok 1 - must be skipped test # SKIP # MUST NOT be treated as a SKIP test ok 2 - must not be skipped test \# SKIP # MAY be treated as a SKIP test, but SHOULD warn about it ok 3 - may skip, but should warn# skip ok 4 - may skip, but should warn # skip ok 5 - may skip, but should warn#skip"
2. **Synopsis.** "The key words must , must not , required , shall , shall not , should , should not , recommended , may , and optional in this document are to be interpreted as described in RFC 2119 ."
3. **Changes From TAP13 Format.** "That is, TAP14 is designed to be reasonably parseable by any compliant TAP13 Harness, and TAP14 Harnesses should be able to reasonably interpret the output of TAP13 Producers."
4. **Harness Behavior.** "A harness that is collecting output from a test program should read and interpret TAP from the process’s standard output, not standard error."
5. **Harness Behavior.** "(Handling of test standard error is implementation-specific.) A Harness should normalize line endings by replacing any instances of \r\n or \r in the TAP document with \n ."
6. **Harness Behavior.** "A harness should treat a test program as a failed test if: The TAP output lines indicate test failure, or The TAP output of the process is invalid in a way that is not recoverable, or The exit code of the test program is not 0 (including test programs killed by a fatal Unix signal)."
7. **Harness Behavior.** "If one or more test programs are considered failures, then a TAP Harness should indicate failure to the user in whatever means are appropriate."
8. **Document Structure.** "TAP14 producers must encode TAP data using the UTF-8 encoding."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [TAP 14](https://testanything.org/tap-version-14-specification.html): Specification, TAP version 14, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
