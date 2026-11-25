---
name: atc-remediation
description: Walk through ATC (ABAP Test Cockpit) violations methodically, grouped by category, with concrete fixes per finding. Use when the user asks to fix, remediate, address, or triage ATC findings on an ABAP object, package, or transport. Refuses pseudo-comment suppressions by default. Applies the rule set in ../CLAUDE.md (loaded on invocation). Targets modern ABAP — BTP ABAP Environment and S/4HANA on-prem in the ABAP Cloud development model.
license: Apache-2.0
---

# abap-cloud-rap:atc-remediation

Walk through ATC violations from the connected ABAP system and fix them methodically, grouped by category, with an explanation per finding.

## What this command does

You are taking ATC (ABAP Test Cockpit) results, grouping them by check category, and proposing a concrete fix for each — applying the rules in `../CLAUDE.md`. Pseudo-comment suppressions are off-limits unless the user explicitly justifies and approves them.

**Tool routing (read carefully).** Read the `## Tooling` section in `../CLAUDE.md` before the first tool call and follow it. For this skill the routing is:

| Step | Primary | Fallback |
|---|---|---|
| Run the ATC check | `abap-adt` `abap_atc_run` → poll `abap_atc_get_result` | `arc-1` `SAPDiagnose action="atc"` |
| Discover check variants | `arc-1` `SAPDiagnose action="atc_variants"` | ask the user for the variant name |
| Read the offending source | `arc-1` `SAPRead` (use `grep=` to pull just the finding's lines) | ask the user to paste it |
| Mechanical fixes | `abap-adt` `abap_atc_execute_deterministic_quickfixes`; for the rest, `abap_atc_apply_ai_fix` + `abap_atc_get_ai_fix_result` | `arc-1` `SAPDiagnose action="quickfix"` → `"apply_quickfix"` (returns deltas, writes nothing) |
| Write the fix back and activate | `abap-adt` `abap_creation-create_object` / `abap_activate_objects` | `arc-1` `SAPWrite` + `SAPActivate` when write scope is enabled — syntax-check with `SAPDiagnose action="syntax"` first, read back after; otherwise hand the diff to the user |

If neither server exposes ATC, ask the user to paste ATC results from ADT. **Never invent ATC findings.**

An expired session shows up as an error like `Your user was logged off` — that is an auth failure on that server, not a missing capability. Fall back for this run and tell the user which server needs re-authentication.

## Inputs to collect

If not provided, ask which of these to target. Default to the narrowest scope.

- A single ABAP object name
- A package name (list its contents first with `arc-1` `SAPRead type=DEVC` so the user can confirm the scope)
- A transport request number
- An existing ATC run / result ID (`abap_atc_get_result` with the stored `worklistId`)

Also ask which check variant to run against, defaulting to **`ABAP_CLOUD_DEVELOPMENT_DEFAULT`** for ABAP Cloud development scope. Confirm it exists with `arc-1` `SAPDiagnose action="atc_variants"` rather than assuming.

## Procedure

1. **Get ATC results.** Run the check per the tool-routing table above — `abap-adt` `abap_atc_run` first, `arc-1` `SAPDiagnose action="atc"` on hard failure, pasted output only when neither works. `abap_atc_run` returns a `worklistId`; the run is asynchronous, so poll `abap_atc_get_result` until the counts stop changing before you start grouping.
2. **Group findings by check category.** Typical categories:
   - **Clean Core / Cloud compatibility** — unreleased API usage, direct SELECT on SAP-owned tables, language-version violations
   - **Security & Authorization** — missing authorization checks, unsafe SQL, hard-coded user IDs
   - **Performance** — `SELECT *`, missing indexes, table reads in loops
   - **Code quality / Clean ABAP** — magic numbers, method length, parameter count, `CREATE OBJECT`, chained declarations
   - **CDS / RAP modelling** — missing mandatory annotations, incorrect composition/association, missing draft setup
   - **Testing** — missing ABAP Unit, test classes that hit live data
3. **For each finding, in priority order (Cloud compatibility → Security → Performance → Code quality → CDS/RAP → Testing):**
   - State the violation in one sentence
   - Cite the ATC check name and severity
   - Identify the root cause — name the rule from `CLAUDE.md` that applies
   - Show the fix as a Before/After code snippet
   - Propose the action: **auto-apply**, **ask before applying**, or **manual only** (see severity ladder below)
4. **Severity ladder for auto-apply decisions:**
   - **Auto-apply candidates** — mechanical fixes that cannot change behavior: missing annotations (`@AccessControl.authorizationCheck`, `@AbapCatalog.preserveKey`), `CREATE OBJECT → NEW`, `READ TABLE + sy-subrc → line_exists`, chained `DATA:` declarations split. Even auto-apply candidates require batch confirmation, never silent application.
   - **Ask-before-applying** — fixes that touch logic shape but not semantics: `EXPORTING → RETURNING` (only if no caller depends on `IS SUPPLIED`), method extraction, magic-number → named constant.
   - **Manual only** — fixes that change interfaces, exceptions, or data access patterns: replacing `SELECT FROM vbak` with `SELECT FROM I_SalesOrder` (column names differ), replacing unreleased function modules, removing a missing `authorization` block.
5. **Never suppress with pseudo-comments unsolicited.** `"#EC NOTEXT`, `"#EC CI_USAGE_OK`, and friends are not fixes. Refuse to insert them by default. If the user requests suppression, demand: (a) the specific check name, (b) a one-sentence written justification, (c) a JIRA/issue link if one exists. Emit the pseudo-comment with the justification in a comment above it.
6. **After each batch of fixes, re-run ATC on the same scope and variant** — via the same server you used for the baseline, so the counts are comparable — and report the delta: violations resolved, violations remaining, new violations introduced (if any — back out the offending change).

## Output format

```
# ATC Remediation — <SCOPE>

Variant: <check variant>
Results from: abap-adt (worklistId <id>) | arc-1 SAPDiagnose | pasted by user
Total findings: <N>

## Category breakdown
| Category                       | Total | Auto-apply | Ask | Manual |
|--------------------------------|-------|------------|-----|--------|
| Clean Core / Cloud             | N     | N          | N   | N      |
| Security & Authorization       | N     | N          | N   | N      |
| Performance                    | N     | N          | N   | N      |
| Code quality / Clean ABAP      | N     | N          | N   | N      |
| CDS / RAP modelling            | N     | N          | N   | N      |
| Testing                        | N     | N          | N   | N      |

## Findings

### Category: Clean Core / Cloud
#### F-001 — <one-line violation>
- **Object:** <name> line <N>
- **ATC check:** <check name> — severity <error|warning|info>
- **Root cause rule:** <rule-name from CLAUDE.md>
- **Before:**
` ` `abap
<offending code>
` ` `
- **After:**
` ` `abap
<fixed code>
` ` `
- **Disposition:** auto-apply | ask | manual
- **Note:** <if any — e.g. "released CDS view I_SalesOrder used in place of VBAK; field name differs from VBELN to SalesOrder">

(repeat per finding, grouped by category)

## Apply plan
- Auto-apply batch: N changes across M objects — confirm before writing.
- Ask-before-applying: N changes — I will confirm each one.
- Manual: N changes — listed above with full context for you to do by hand.

## Suppressions requested by user
<empty by default; if user explicitly requested any, listed here with justification>
```

## Hard rules for this command

- **Follow the tool-routing table.** Official `abap-adt` ATC first, `arc-1` `SAPDiagnose` as fallback, pasted output last. Never invent ATC findings.
- **Name the server in the report.** The reader needs to know whether the counts came from `abap-adt` or `arc-1` to reproduce them.
- **Always group by category.** A flat list of 200 findings is unactionable.
- **Always cite the ATC check name.** "Fix this" is not a remediation.
- **Never apply a fix that changes semantics without asking.** EXPORTING→RETURNING is borderline — confirm.
- **Refuse pseudo-comment suppression by default.** Only emit with an explicit user-provided justification in a comment above the suppressed line.
- **Re-run ATC after each batch.** Report the delta. If new findings appear, roll back the change that introduced them and report.
- **One object = one transaction.** Do not write across many objects in a single irreversible batch.
