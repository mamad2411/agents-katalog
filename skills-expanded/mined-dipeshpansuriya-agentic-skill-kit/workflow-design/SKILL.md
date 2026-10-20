---
name: workflow-design
description: Design business process flows, state machines with transition tables, CI/CD pipelines and orchestration flows as Mermaid plus tables. Use when the user asks to map a process, draw a state machine, design a pipeline, or plan retries and compensation.
---

# Workflow Design

Design workflows for logistics platforms: business processes across parties (forwarder, airline, ground handler, customs), entity lifecycles (AWB, booking, ULD), CI/CD pipelines, and distributed service flows. Tables are the source of truth; Mermaid diagrams are drawn from them.

## Inputs
- Process description, SOP, meeting notes, ticket, or an existing diagram
- Entity and its statuses / message codes (e.g., FSU: RCS, MAN, DEP, ARR, DLV)
- Pipeline needs: repo, stack, environments, approval rules, hosting
- Existing workflow to review or fix

## Defaults (ask vs assume)
| Setting | Default if not stated | Ask only if |
|---|---|---|
| Diagram format | Mermaid (`flowchart` for processes, `stateDiagram-v2` for states, `sequenceDiagram` for service flows) | User needs BPMN XML / Visio |
| CI/CD platform | GitHub Actions | They use Azure DevOps / Jenkins and it is not stated |
| Environments | dev (PR) → staging (auto) → production (approval) | Regulated change windows apply |
| Messaging | At-least-once delivery | Never |
| Coordination | Orchestration for transactions with compensation/SLAs; choreography for notifications | Never |
| SLAs | Marked "TBD" | SLAs are the point of the request |

Ask at most 3 questions, only when the answer changes the design. State assumptions at the top.

## Steps
1. Classify the request with the routing table below and open the matching reference.
2. Name the trigger, the outcome ("done" definition), actors/systems, and scope boundaries.
3. Build the table first (step table, transition table, stage table, or saga table).
4. Add the unhappy paths: rejects, timeouts, duplicates, holds, partial failures, rollback.
5. For state machines, save the transition table to a `.md` file and run `python3 scripts/validate_state_machine.py FILE.md` (add `--initial` / `--terminal` if not declared); fix every ERROR.
6. For pipelines, start from `templates/github-actions-template.yml` and replace every `TODO`; map to Azure DevOps / Jenkins with `references/cicd-pipelines.md` if needed.
7. Draw the Mermaid diagram from the table; names must match exactly.
8. Run the self-check and fix before returning.

## Routing
| Request | Reference / template | Output |
|---|---|---|
| (a) Business process, SOP, swimlanes, "as-is / to-be" flow | `references/business-process.md` | Mermaid swimlane flowchart + step table (actor, SLA, exception handling) |
| (b) Lifecycle, statuses, "state machine" | `references/state-machines.md` + `templates/state-machine-template.md` | States table, transition table (From, Event, Guard, To, Action), validator result, `stateDiagram-v2` |
| (c) CI/CD pipeline, release flow, deployment gates | `references/cicd-pipelines.md` + `templates/github-actions-template.yml` | Stage/gate table, pipeline YAML, rollback plan |
| (d) Service coordination, retries, idempotency, saga, compensation | `references/orchestration-reliability.md` | Orchestration vs choreography decision, retry policy table, idempotency keys, saga table + sequence diagram |

Mixed requests: one section per sub-part, in order a → d, with shared names.

## Rules
- **Branding only on request:** use plain, neutral formatting by default. Apply a company or brand design skill (colours, fonts, logo, templates) only when the user names that skill or brand in the request; never pick one automatically.
- Tables first, diagrams second; the diagram must not contain anything the table lacks.
- Every decision has labelled outcomes; every path ends in an end/terminal state.
- Every exception has an owner and handling (retry, park, escalate, compensate).
- Every human task and exception state has an SLA or "TBD".
- State names are facts ("Manifested"); events are things that happened ("MAN received").
- Never ship a state machine with validator ERRORs; report the validator result line.
- Treat every message as possibly duplicated, late or out of order; define the idempotency key.
- Retries only for transient errors, with exponential backoff + jitter and a cap, then DLQ.
- Pipelines: build once, deploy the same artifact; production behind approval; tested rollback; least-privilege `permissions:`; OIDC over stored secrets.
- Never invent partner message codes, SLAs or approval rules; use "TBD" and list them.
- For architecture choices (e.g., which broker), point to the software-architecture skill; for reviewing pipeline code quality, the code-review skill.

## Self-check
- [ ] Trigger, outcome, actors stated
- [ ] Happy path and at least the relevant exceptions from the reference covered
- [ ] State machines: validator PASS (0 errors) and result line included
- [ ] Pipelines: stages, gates, environments and rollback all present; YAML valid
- [ ] Idempotency key and retry policy defined for async steps
- [ ] Mermaid is valid and names match the tables
- [ ] TBDs listed; nothing invented

## Output
Return the routed deliverable (tables, then Mermaid, then YAML if any), then an **"Assumptions & Needs input"** block (defaults used, TBD SLAs, open questions).

Test cases for this skill: `evals/test-cases.md` (rerun after every edit).
