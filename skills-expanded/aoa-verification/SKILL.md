---
name: aoa-verification
description: Turn one stable technical truth into bounded evidence through contract, coverage-audit, or property mode. Use to define a named consumer seam, audit what existing checks really constrain, or express a broad invariant after manual cases establish meaning. Compose with aoa-eval when an evaluation surface must first be found or applied. Do not use for undefined behavior, generic test plans, or green checks as whole-system proof.
---

# aoa-verification

## Intent

Start from owner meaning and observed behavior, then choose the smallest evidence
form whose green result has an explicit claim limit.

## Trigger boundary

Use this skill when:

- a stable producer-consumer seam, an important invariant, or a property across
  many inputs/states needs evidence that can reveal a meaningful break

Do not use this skill when:

- behavior or ownership is undefined, the change is private, the request is a
  generic test strategy, or automation would exist only to produce green status

## Inputs

- owner rule, system/boundary under review, named consumers where relevant
- manual cases or failures, current checks, and available oracle

## Outputs

- exactly one typed mode result: evidence package, gaps, smallest authorized
  durable check or no-check decision, claim limit, and termination

## Procedure

1. Read `references/contract.yaml` and choose exactly one mode:

   | Mode | Select when | Required procedure |
   |---|---|---|
   | `contract` | A named consumer relies on a stable ABI, receipt, schema, tool result, or handoff. | `references/contract.md` |
   | `coverage-audit` | Checks exist and the question is what stable invariant they truly constrain. | `references/coverage-audit.md` |
   | `property` | Correctness must hold across many inputs or states. | `references/property.md` |

2. Read the selected reference completely. Do not load unrelated mode
   procedures.
3. Read the authoritative owner rule before the subject implementation,
   checks, examples, or generated views. Use exact supplied paths directly;
   search only for a missing required input, not for ritual workspace
   orientation. Exercise expected, rejected, and motivating failure cases
   manually and state the oracle. Do not collect repository-wide inventories,
   hashes, or status unless the claim or effect boundary needs them.
4. When the exact evaluation surface is unknown or must be selected/applied,
   use a task-local DAG: `aoa-eval.select -> aoa-eval.apply ->` the chosen
   verification mode. A named check may be run directly as evidence inside a
   verification task; cross-surface discovery and application remain
   `aoa-eval` responsibilities.
5. Create durable automation only after manual evidence establishes a repeated
   or owner-declared long-lived rule and the active task authorizes the write.
   Remove session-only probes after learning.

## Contracts

- manual observation and owner meaning precede durable automation
- evaluation selection/application and interpretation of what evidence proves
  remain distinct, composable effects
- a check protects one claim and cannot certify the whole system
- generated/exported views remain subordinate to owner sources
- no-check is valid when recurrence, oracle, or stability is missing

## Risks and anti-patterns

- restating a fixture, snapshot, formatting, or field order as semantic law
- property tests with a self-fulfilling oracle
- adding validators after the fact to hide an unresolved manual failure
- silently using verification as a replacement for eval inventory selection or
  treating a selected eval as proof of invariant coverage

## Verification

- confirm selected mode, owner rule, manual cases, and oracle
- when an eval surface was discovered or applied, name the `aoa-eval` handoff
  and preserve its observation/proof limit
- if automation is proposed, show the motivating failure it catches
- make claim limit, evidence gap, consumer impact, and stop line explicit

## Adaptation points

Owners supply local commands, generators, schemas, fixtures, consumers, and
compatibility windows without duplicating this procedure.
