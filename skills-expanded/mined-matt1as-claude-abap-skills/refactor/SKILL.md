---
name: refactor
description: Refactor existing ABAP code to Clean ABAP style without changing behavior. Use when the user asks to refactor, clean up, modernize, or tidy ABAP code. Applies the rule set in ../CLAUDE.md in deterministic passes (naming, declaration, expression, method shape, error, class) and asks before writing back via MCP. Targets modern ABAP only — BTP ABAP Environment or S/4HANA on-prem in the ABAP Cloud development model.
license: Apache-2.0
---

# clean-abap:refactor

Refactor existing ABAP code to conform to the Clean ABAP rule set in `../CLAUDE.md` (relative to this skill's directory).

## What this command does

You are refactoring ABAP source code to bring it into compliance with the Clean ABAP rule set. **Style and structure only — business logic stays identical.** If a change would alter what the code does, you do not make it; you flag it instead.

## Inputs

Accept any of the following. If nothing is provided, ask which target the user wants.

- An ABAP object name — read it with `arc-1` `SAPRead`
- A package name — enumerate with `arc-1` `SAPRead type=DEVC`, then refactor object by object, never as a single bulk change
- A code block pasted into the conversation — always works, and is the only path when no read-capable server is connected

**Tool routing.** Read the `## Tooling` section in `../CLAUDE.md` before the first tool call. The two halves of this skill land on different servers:

| Step | Primary | Fallback |
|---|---|---|
| Read the source | `arc-1` `SAPRead` | ask the user to paste it |
| Find callers before touching a signature | `arc-1` `SAPNavigate action="references"` | ask the user; if unknown, skip the change |
| Dry-run the refactored source | `arc-1` `SAPDiagnose action="syntax"` with `source` — validates without writing | skip, and rely on activation |
| Write back and activate | `abap-adt` `abap_creation-create_object`, `abap_activate_objects` | `arc-1` `SAPWrite` + `SAPActivate` when write scope is enabled; otherwise hand the diff to the user to paste in ADT |
| Prove behaviour is preserved | `abap-adt` `abap_run_unit_tests` | `arc-1` `SAPDiagnose action="unittest"` |

If only `arc-1` is connected, check whether its write actions are actually enabled before promising a write-back — when write scope is off, the mutating actions are absent from the tool's `action` enum. If they are absent, the refactor is **read-only**: produce the diff and hand it to the user. If they are present, write through `arc-1`, then **read the object back with `SAPRead` and confirm it matches the diff you showed**, and run `SAPActivate`. A successful `SAPWrite` means abaplint passed, not that the object compiles — activation is the real gate.

## Procedure

1. **Load the rule set.** Read every `## RULE:` block in `../CLAUDE.md`. Those are the only refactoring targets.
2. **Get the source.** If pasted inline, use it. If an object name was given, read it with `arc-1` `SAPRead`. If no read-capable server is connected, ask the user to paste it from ADT.
3. **Run the review first.** Internally, perform the same analysis as `/clean-abap:review`. Use the prioritised list as your refactor plan.
4. **Refactor in passes**, in this order. Do not skip ahead:
   1. **Naming pass** — apply `use-problem-domain-names`, `no-magic-numbers-or-literals`
   2. **Declaration pass** — apply `prefer-inline-declarations`, `no-default-key-on-internal-tables`
   3. **Expression pass** — apply `use-string-templates-not-concatenate`, `prefer-is-not-initial-over-negation`, `prefer-case-over-long-if-elseif`, `use-table-expressions-not-read-table-plus-sy-subrc`
   4. **Method shape pass** — apply `methods-do-one-thing-and-stay-small`, `at-most-three-importing-parameters`, `prefer-returning-over-exporting`
   5. **Error pass** — apply `class-based-exceptions-not-sy-subrc`, `catch-specific-exceptions-not-cx-root`
   6. **Class shape pass** — apply `final-classes-and-private-members-by-default`, `prefer-new-over-create-object`
5. **Preserve behaviour.** After every pass, mentally diff the program logic. If you cannot prove a change is behaviour-preserving (e.g. a refactor would change exception types caught upstream, would change SELECT result order, would alter authority checks), **stop and ask** instead of guessing.
6. **Show the diff before writing back.** Produce a per-method or per-section before/after diff. Annotate every change with the rule name that motivated it. Syntax-check the result first with `arc-1` `SAPDiagnose action="syntax"` (passing `source`) — it validates the new source without writing anything, so a broken refactor never reaches the system.
7. **Ask for confirmation before writing back.** Explicit confirmation per object — not a blanket yes for a package. Write via the official `abap-adt` server (or `arc-1` `SAPWrite` if that is the only one enabled), then activate and confirm the object activated cleanly. When writing through `arc-1`, read the object back afterwards and confirm it matches the diff you showed.
8. **Re-run the object's ABAP Unit tests after activation** (`abap-adt` `abap_run_unit_tests`, fallback `arc-1` `SAPDiagnose action="unittest"`). A behaviour-preserving refactor with no test evidence is a claim, not a proof — if the object has no tests, say so in the report.

## Behaviour preservation — non-negotiable

These changes are out of scope for this command — they alter behaviour:

- Changing exception classes raised by a public method (callers catch them)
- Changing the order or set of database rows returned by a SELECT
- Removing authority checks, even if they look redundant
- Inlining or extracting code that crosses a `COMMIT WORK` / `ROLLBACK WORK`
- Changing the public signature of a method except `EXPORTING → RETURNING` for a single output where no caller relies on `IS SUPPLIED`

If a Clean ABAP rule appears to require one of the above, **flag it** in the report and skip the change. Behaviour change belongs in a separate task, not in a style refactor.

## Output format

```
# Clean ABAP Refactor — <OBJECT NAME>

## Plan
1. <rule-name> — <count> occurrences
2. <rule-name> — <count> occurrences
...

## Changes

### <method or section name>

**Rule:** <rule-name>
**Before:**
` ` `abap
<original>
` ` `
**After:**
` ` `abap
<refactored>
` ` `
**Rationale:** <one sentence, no longer>

(repeat per change)

## Behaviour-preserving check
- [ ] No public method signature changed (except EXPORTING→RETURNING for single output)
- [ ] No exception classes added or removed from public methods
- [ ] No SELECTs reordered or filtered differently
- [ ] No authority checks removed
- [ ] No statements moved across COMMIT/ROLLBACK boundaries

## Skipped
<rule-name> at <location> — <one-line reason it would have changed behaviour>

## Verification
- Syntax check (arc-1 SAPDiagnose): pass / fail / not run
- ABAP Unit after activation: N passed, N failed / object has no tests / not run

## Confirmation
Write these changes back to <OBJECT NAME> via <abap-adt | arc-1>? (yes / no / per-method)
```

## Hard rules for this command

- **Style and structure only.** Never change what the code does.
- **One object at a time.** No silent batching across a package.
- **Confirm before write-back.** Always. Even if the user said yes for a previous object.
- **Activate after writing.** If activation fails, report the error and revert the write. Do not patch through activation errors.
- **No rule-by-rule chatter.** Group changes by method or section; one diff per change.
- **If a Clean ABAP rule conflicts with the ABAP Cloud / RAP overlay, the overlay wins.** Apply the overlay version of the rule. Note the conflict in the report.
