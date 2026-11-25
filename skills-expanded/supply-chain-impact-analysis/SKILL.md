---
name: supply-chain-impact-analysis
description: Trace a supplier or evidence risk across governed products, plants, orders, customers, contracts, controls, policies, and remediation without inventing relationships.
tools: [ontology_search, trace_business_impact, inspect_ontology_term, count_affected_entities]
---

# Supply-chain impact analysis

## When to use

Use this procedure when the correct answer depends on relationships across systems of record rather than on one semantically similar document.

## Parameters

- `question`: the operator's impact question.
- `seed_limit`: maximum number of semantically retrieved seed entities; default `4`.
- `max_hops`: maximum stored-edge traversal depth; default `4`.
- `required_classes`: optional business-object classes that must be checked.

## Steps

1. Call `ontology_search` with the operator's exact question. Treat similarity as seed selection only.
2. Preserve each returned `node_id`, class, status, source system, and vector distance.
3. Call `trace_business_impact` using the same question and bounded `max_hops`.
4. Accept only relationships stored in the ontology edge table. Preserve edge IDs and evidence references.
5. Group affected instances by governed class: supplier, component, product, plant, order, customer, contract, evidence, control, policy, risk, and remediation.
6. Use `inspect_ontology_term` when a class or property definition is ambiguous.
7. Send only the returned node IDs to `count_affected_entities`; preserve its sandbox input, execution, and output envelope.
8. Cite every conclusion with `KG:NODE:<id>` or `KG:PATH:<id>`.
9. Escalate missing or invalid edges to ontology stewardship; do not repair the graph in generated prose.

## Guardrails

- Vector proximity never proves that two entities are related.
- Do not create new edges or change source status during a read-only impact query.
- Do not omit effective dates, source systems, validation status, or evidence references.
- Keep private reasoning out of the trace; persist inputs, selected context, actions, and evidence instead.

## Success criteria

- At least one governed seed entity and one valid stored path were returned.
- Every affected object retains a stable identifier and class.
- The answer distinguishes direct evidence from inferred operational impact.
- Host verification confirms all cited paths exist in the stored graph.
- The sandbox count matches independent host recomputation and the session is closed.
