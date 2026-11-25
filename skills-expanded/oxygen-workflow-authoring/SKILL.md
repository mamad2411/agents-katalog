---
name: oxygen-workflow-authoring
description: Author, validate and operate deterministic OXYGEN Workflows with explicit inputs, hosted runs, current schemas and inspectable effects.
---

# Compose the hosted workflow

Read [composition](../../../docs/composition.md), [the runtime contract](../../../docs/runtime-contract.md) and the relevant function definitions. This kit already contains six disabled workflow graphs.

Use Workflows for deterministic control flow, Tables for row dependencies, Sequences for outreach cadence and Agents for adaptive goals. Local files author definitions; OXYGEN executes production runs.

```sh
oxygen commands get "workflows schema" --json
oxygen workflows schema --subject graph --json
oxygen capabilities search "workflow trigger from a qualified account" --json
```

1. Search existing definitions/templates and resolve resource IDs from the chosen workspace.
2. Inspect the selected trigger's current event schema, including source, event and filters. Do not equate a human event label with an exact trigger.
3. Author typed inputs, closed output schemas, explicit dependencies and error/hold paths. Avoid `#` in node IDs; it is reserved for iteration IDs.
4. Lint for the intended draft/publish phase, then apply within the requested scope. Inspect the saved version and trigger status.
5. Discover the current call preview and dry-run grammar. A call preview describes effects; a dry run may perform internal reads or permitted GETs. Inspect both before live scope.
6. Execute or enable only the authorized rows/events, effects and credit ceiling. Tail the durable run and inspect outputs, retries and costs.

Code nodes use declared inputs. For this kit, edit the pure source/contract and run `npm run build`; the generated `(inputs) => ...` expression is the deployed source. Do not insert ambient credentials, clocks or network calls.

An outbound graph enrolls through the native Sequence action. Inspect its current state and enrollment semantics; pending enrollment and active delivery differ. It must not bypass sender, suppression or reply-stop controls with raw provider sends.

Return definition/version, lint results, previewed effects, run link and verified state. Reconcile ambiguous external effects before retrying; replay and one-node tests must use the current server-supported semantics.
