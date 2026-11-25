---
name: gpt-5-6-prompt-engine
description: Use when creating, auditing, rewriting, debugging, migrating, or evaluating GPT-5.6 Sol, Terra, or Luna prompt layers, tool descriptions, agent briefs, or prompt stacks; choosing runtime configuration; or comparing controlled prompt candidates.
---

# GPT-5.6 Prompt Engine

## Operating principle

Preserve the application's contract before optimizing the prompt. Make the smallest change that improves observable behavior, and require controlled evidence before calling a candidate better.

## Workflow

1. Classify the request as **create**, **audit-only**, **surgical rewrite**, **migration**, or **evaluation**. Combine modes only when the user asks for multiple deliverables.
2. Inventory the immutable contract before editing: explicit facts and values, JSON schemas, system, developer, user, and tool trust layers, output contract, permissions, and business behavior. Preserve wording verbatim when a parser, policy, or caller may depend on it.
3. Apply the material-ambiguity gate. Ask one focused question only when plausible answers would change the goal, schema, facts, permissions, evidence requirements, or success criteria. Otherwise preserve the source choice and proceed. Prompt-only or use-your-judgment pressure does not authorize choosing a contradictory branch; ask the smallest blocking question before drafting.
4. Perform only the selected mode's work. Keep prompt content separate from runtime settings unless configuration is in scope.
5. Validate the result against the inventory and the requested output contract. Do not silently broaden tools, actions, data access, or policy.

### Create

- Start with the desired outcome and application-visible result.
- Add context, constraints, permissions, evidence, tools, validation, fallback, success, and stop clauses only when they change behavior.
- Keep tool descriptions narrow: state what the tool does, when to call it, required inputs, and meaningful side effects or limits.
- Prefer one clear rule over repeated emphasis or a giant reusable template.

### Audit-only

- Identify only behavior-changing defects, quote precise evidence, explain the risk, and propose the smallest correction. Do not rewrite the prompt unless requested.
- When a source prompt or JSON tool stack is available and static signals are useful, run the [prompt auditor](scripts/audit_prompt.py).
- Treat the auditor's heuristics as review signals and independently verify the cited evidence. Heuristics are review signals, not proof of a conflict.
- Never infer visible chain-of-thought from a reasoning phrase; require an explicit request to expose reasoning in the output. A bare reasoning phrase does not change the output contract, so omit a bare reasoning phrase from a behavior-changing audit rather than asking about or correcting possible disclosure.
- Never infer unsafe persistence from ordinary completion wording; require evidence of a permission, stop, scope, or safety conflict.

### Surgical rewrite

- Rebuild outcome-first, remove normalized duplicates, and consolidate compatible rules without changing their force.
- Add only behavior-changing success, evidence, tool-routing, validation, fallback, and stop clauses that the source or user actually supports.
- Treat contradictory business or fallback semantics as material ambiguity that requires clarification rather than invention.
- Do not invent fallback, status, evidence, or stopping semantics. Preserve unresolved alternatives if the user cannot clarify and label the conflict outside the prompt unless the output must be prompt-only.

### Migration

- Fetch current official documentation before stating changeable model, endpoint, parameter, feature, pricing, limit, or availability claims.
- Separate required compatibility changes from optional measured candidates. Preserve the endpoint, role semantics, effective reasoning, tool contract, output contract, latency target, and business behavior first.
- A latency target does not authorize a guessed reasoning value. If effective reasoning is unknown, mark it unknown and keep explicit settings optional unless current official documentation establishes a required compatibility value.
- An immediate-launch or skip-evaluation demand does not convert unverified options into compatibility changes. Keep them out of launch-ready artifacts until contracts are confirmed and gates pass, even when the user names them.
- Keep unconfirmed application contracts unconfirmed. Do not invent field types, parser expectations, state behavior, or fallback handling.
- Never add Luna, Priority processing, strict field types, caching, PTC, Pro, or multi-agent merely because they are available. Propose each only as an optional candidate tied to a workload hypothesis and gate.

### Evaluation

- Freeze cases and runtime controls, define success and evidence scoring before running, and include every attempted case in accounting.
- Gate quality, evidence, and reliability before tokens, latency, and cost. Hold on a failed required gate even when efficiency improves.
- When paired baseline and candidate JSONL is available, run the [evaluation comparator](scripts/compare_eval_runs.py) with predeclared thresholds.
- Do not claim improvement solely because a prompt is shorter. Report measured deltas, failures, missing metrics, and uncertainty.

## Progressive references

- When model or API claims may have changed, read the dated [official source map](references/official-source-map.md) and refresh the cited pages.
- When creating or rewriting prompt content, read [prompt patterns](references/prompt-patterns.md) for keep/trim decisions and task-specific clauses.
- When changing models, endpoints, reasoning, tools, state, caching, or output handling, read the [migration matrix](references/migration-matrix.md).
- When planning or judging a controlled comparison, read the [evaluation playbook](references/evaluation-playbook.md).

## Output contracts

### Audit

Return a compact table with `Evidence`, `Behavioral risk`, and `Smallest correction`, followed by material open questions. Distinguish verified defects from heuristic review signals. Do not include a rewritten prompt unless requested.

### Optimized prompt

Honor a prompt-only request: return only the copy-ready prompt with no preface, audit, or notes. Otherwise return `Optimized prompt`, `Preserved contract`, `Changes`, and `Open questions or assumptions`; omit empty sections.

### Migration

Return the migrated request or configuration, then `Required compatibility changes`, `Optional measured candidates`, `Preserved contract`, and `Sources and assumptions`. Give every optional candidate a measurement gate; do not present it as required. Cross-check every Before/After value against the source and migrated artifact.

### Evaluation

Return the frozen comparison matrix, scoring rubric, run protocol, aggregate metrics, failure and zero-success semantics, predeclared gates, and an explicit `SHIP` or `HOLD` decision rule. Never invent results for runs that were not performed.
