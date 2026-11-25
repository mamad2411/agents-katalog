---
name: clean-core-check
description: Check an ABAP object or package for clean core compliance — unreleased APIs, direct SELECT on SAP-owned tables, classic constructs disallowed in ABAP Cloud, modifications to SAP standard. Use when the user asks to audit, verify, or check clean core compliance, ABAP Cloud compatibility, released API usage, or extension point usage. Produces a categorised report with hard violations and soft warnings. Read-only — never writes back. Targets BTP ABAP Environment and S/4HANA on-prem in the ABAP Cloud development model.
license: Apache-2.0
---

# abap-cloud-rap:clean-core-check

Check an ABAP object or package for clean core compliance. Pulls the source from the connected system and produces a categorised compliance report with concrete remediation steps.

## What this command does

You are auditing one or more ABAP objects for compliance with the **clean core** principles enforced by ABAP Cloud development model. The rules in `../CLAUDE.md` define what is allowed; this command finds what is not. Output is a structured report — **read-only**, no writes back.

**Tool routing.** Read the `## Tooling` section in `../CLAUDE.md` before the first tool call. This skill is read-heavy, so most of its work lands on `arc-1`:

| Step | Primary | Fallback |
|---|---|---|
| List the objects in scope | `arc-1` `SAPRead type=DEVC` (package) or `SAPSearch` | ask the user for the object list |
| Read each object's source | `arc-1` `SAPRead` | ask the user to paste it |
| Decide whether a consumed SAP API is released | `arc-1` `SAPRead type=API_STATE` — the authoritative C0–C4 contract state | ATC evidence below, else flag as *unverified* |
| Corroborate with tool findings | `abap-adt` `abap_atc_run` + `abap_atc_get_result`, variant `ABAP_CLOUD_DEVELOPMENT_DEFAULT` | `arc-1` `SAPDiagnose action="atc"` |
| Trace what a custom CDS view sits on | `arc-1` `SAPContext action="deps"` / `action="impact"` | read the source and follow `select from` by hand |

`SAPRead type=API_STATE` replaces guesswork: **never assert that an SAP object is or is not released from memory** — check it, or mark the finding *unverified* and say so.

## Inputs

If not provided, ask. Defaults to the narrowest scope.

- An ABAP object name (class, function group, program, include, CDS entity, BDEF)
- A package name
- A transport request — check every object in the transport

## What to check

For each object in scope, look for the following. Each maps to a rule in `CLAUDE.md`.

### Hard violations — never allowed in either BTP or S/4HANA on-prem Cloud development

| Check                                                | Source rule                              |
|------------------------------------------------------|------------------------------------------|
| Use of an SAP class/interface/FM with no C1 release  | `released-apis-only`                     |
| Direct `SELECT` from a SAP-owned database table      | `no-direct-select-on-sap-owned-tables`   |
| Classic dynpro (`CALL SCREEN`, screen exits)         | `abap-cloud-language-scope-only`         |
| `SUBMIT`, `CALL TRANSACTION`, `LEAVE TO`             | `abap-cloud-language-scope-only`         |
| `FORM` / `PERFORM`                                   | `abap-cloud-language-scope-only`         |
| `CALL FUNCTION ... DESTINATION 'NONE'` for internal logic | `abap-cloud-language-scope-only`    |
| Modification of SAP standard objects                  | `no-modification-of-sap-standard`        |
| Use of an SAP enhancement point that is not released | `no-modification-of-sap-standard`        |
| `define view` (legacy DDL view) instead of `define view entity` | `interface-entity-required-annotations` |

### Soft warnings — allowed in S/4HANA on-prem Cloud development for transitional reasons, never allowed in BTP

| Check                                                | Note                                                        |
|------------------------------------------------------|-------------------------------------------------------------|
| Use of a SAP API released only with `Use System-Internally` contract | Allowed on-prem during migration, hard-blocked on BTP |
| Released-API use that is deprecated and slated for removal | Will become a hard violation in a future release |
| Custom CDS view selecting from another *unreleased* custom view | Allowed today, but introduces a chain that will break |

## Procedure

1. **Get the source.** Resolve the scope and read every object per the tool-routing table above. The official `abap-adt` server has no source-read tool, so this step runs on `arc-1` `SAPRead`; if `arc-1` is not connected, ask the user to paste the source from ADT. Do not paraphrase or imagine source code.
2. **For each object, walk the hard checks.** Record every hit with: object, line/element, check name, root-cause rule, and a concrete remediation.
3. **Then walk the soft checks** for objects targeting S/4HANA on-prem. Skip soft checks if the target is BTP — every soft finding is hard there.
4. **For every finding, propose a concrete fix.** Examples:
   - Direct `SELECT vbak` → "use released `I_SalesOrder`; field `VBELN` becomes `SalesOrder`, `NETWR` becomes `TotalNetAmount`"
   - Unreleased FM call → "use released class `<X>` instead; signature: `<methods>`"
   - `define view ZX_...` → "migrate to `define view entity ZX_...`; remove `@AbapCatalog.sqlViewName`"
   - `PERFORM process_order` → "move logic to a method on a `FINAL` class; declare per Clean ABAP `methods-do-one-thing-and-stay-small`"
5. **Do not write changes.** This command is read-only. The user runs `/abap-cloud-rap:atc-remediation` or fixes by hand.

## Output format

```
# Clean Core Compliance Report — <SCOPE>

Target system: BTP | S/4HANA on-prem
Objects audited: <N>
Hard violations: <N>
Soft warnings: <N>

## Hard violations
(Listed by object, then by check.)

### Object: <name>
#### HV-001 — <one-line violation>
- **Where:** <file> line <N>
- **Check:** <check name from the hard table above>
- **Rule:** <rule-name from CLAUDE.md>
- **Found:**
` ` `abap
<offending code>
` ` `
- **Fix:**
` ` `abap
<concrete replacement, ready to paste>
` ` `
- **Notes:** <e.g. field-name mapping when migrating from a table to a released CDS view>

(repeat per finding)

## Soft warnings (S/4HANA on-prem only)
(Same structure as hard violations; only emitted when target is S/4HANA on-prem.)

## Summary
| Object                | Hard | Soft | Clean core compliant? |
|-----------------------|------|------|-----------------------|
| <name>                | N    | N    | yes / no              |
...

## Recommended next actions
1. Fix the hard violations first — they prevent activation on BTP.
2. For ATC-checkable findings, run `/abap-cloud-rap:atc-remediation` to apply mechanical fixes in batches.
3. For semantic migrations (e.g. `vbak → I_SalesOrder` with field renames), do them by hand and re-run this command to confirm.
4. Re-run this command after fixes to confirm.
```

## Hard rules for this command

- **Read-only.** No writes back. Ever. Only read/diagnose tools from either server.
- **Always state the target system.** Hard vs soft violation depends on it.
- **Verify release state, never recall it.** A `released-apis-only` finding must cite `SAPRead type=API_STATE` output or an ATC finding. Otherwise mark it *unverified*.
- **Always cite the check name and the source rule.** Never present a finding without both.
- **Always show a concrete remediation.** A finding without a fix is not useful.
- **For field-name migrations (e.g. `vbak.vbeln → I_SalesOrder.SalesOrder`), list every renamed field used in the surrounding code** — not just the table swap. Half a migration is worse than none.
- **Pseudo-comment suppression is not a remediation.** If the user wants to ignore a finding, they should justify it through `/abap-cloud-rap:atc-remediation`, not here.
- **Do not include findings that have no rule in `CLAUDE.md`.** This is a compliance check against the library, not a free-form code review.
