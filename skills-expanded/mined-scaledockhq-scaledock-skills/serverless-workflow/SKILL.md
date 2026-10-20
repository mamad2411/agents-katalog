---
name: serverless-workflow
description: >-
  Serverless Workflow: This document proposes the creation of a Domain Specific Language (DSL) for the Open Workflow Specification, designed for building platform agnostic workflows. Covers Serverless Workflow DSL. Use when writing a serverless workflow. Triggers: Serverless Workflow, DSL.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Serverless Workflow

The Serverless Workflow DSL 1.0.3 from the Serverless Workflow project (CNCF): the DSL concepts document and the DSL reference, read from the serverlessworkflow/specification repository at the v1.0.3 release.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Workflow author, or a runtime that executes Serverless Workflow definitions.
- Target version: Serverless Workflow DSL (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Priority of Constituencies.** "If a trade-off needs to be made, always put author's needs above all."
2. **Secret.** "If a workflow attempts to access a secret to which it does not have access rights or which does not exist, runtimes **must** raise an error with type `https://serverlessworkflow.io/spec/1.0.0/errors/authorization` and status `403`."
3. **Task Flow.** "Flow directives may only redirect to tasks declared within their own scope. In other words, they cannot target tasks at a different depth."
4. **Runtime Expressions.** "In `strict` mode, all expressions must be properly identified with `${}` syntax."
5. **Runtime Expressions.** "All runtimes **must** support the default runtime expression language, which is [`jq`](https://jqlang.github.io/jq/)."
6. **Runtime Expressions.** "When the evaluation of an expression fails, runtimes **must** raise an error with type `https://serverlessworkflow.io/spec/1.0.0/errors/expression` and status `400`."
7. **Timeouts.** "A timeout error **must** have its `type` set to `https://serverlessworkflow.io/spec/1.0.0/errors/timeout` and **should** have its `status` set to `408`."
8. **Interoperability, Supported Protocols.** "Runtimes **must** raise an error with type `https://serverlessworkflow.io/spec/1.0.0/errors/communication` if and when a problem occurs during a call."
9. **Events.** "Events in Serverless Workflow adhere to the [Cloud Events specification](https://cloudevents.io/), ensuring interoperability and compatibility with event-driven systems."
10. **Input.** "When set, runtimes must validate raw input data against the defined schema before applying transformations, unless defined otherwise."
11. **Output.** "When set, runtimes must validate output data against the defined schema after applying transformations, unless defined otherwise."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `cloudevents`, `json-schema`, `asyncapi`, `openapi`, `grpc`, `json-pointer`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Serverless Workflow DSL](https://raw.githubusercontent.com/serverlessworkflow/specification/9b5b1da29e9d4fff2358580241e11aab22704a16/dsl.md): Specification, DSL 1.0.3 (v1.0.3, commit 9b5b1da, 2026-07-31), checked 2026-10-06.
- [Serverless Workflow DSL reference](https://raw.githubusercontent.com/serverlessworkflow/specification/9b5b1da29e9d4fff2358580241e11aab22704a16/dsl-reference.md): Specification, DSL 1.0.3 (v1.0.3, commit 9b5b1da, 2026-07-31), checked 2026-10-06.
