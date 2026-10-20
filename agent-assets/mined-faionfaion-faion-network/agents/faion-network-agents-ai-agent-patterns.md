# AI Agent Patterns

## Summary

**One-sentence:** Six agentic AI patterns (ReAct, CoT, Tool Use, Plan-Execute, Reflection, Tree-of-Thoughts) + four multi-agent topologies. Decision record picking the right pattern.

**One-paragraph:** Catalogues six structured patterns for agentic AI systems plus multi-agent coordination topologies (Sequential, Parallel, Supervisor, Hierarchical). The methodology output is a decision record naming the chosen pattern + the 2 axes that drove the choice (loop shape, multi-agent need) + the rejected alternatives.

**Ефективно для:** Architects + tech leads, що уникають «давайте візьмемо ReAct, тому що всі беруть» через структурний вибір по двох осях.

## Applies If (ALL must hold)

- new agent project at scoping stage
- task shape is at least partially known (single vs multi-step, single vs multi-agent)
- you have ≥1 candidate framework selected
- decision-record discipline is in scope
- team can revisit the choice in 3 months

## Skip If (ANY kills it)

- task is trivially single-shot — no agent pattern needed
- framework mandates a single pattern (e.g., CrewAI = role-based) — work within it
- research / exploratory phase — try patterns; decision record later
- patterns already decided by org policy

## Prerequisites

| Input artifact | Format | Source |
|---|---|---|
| Use-case brief | text | Author / owner |
| Tier-manifest entry | JSON | `skills/tier-manifest.json` |
| Eval / fixture data (when applicable) | jsonl | Repo `tests/fixtures/` |
| Named approver | role:person | Org RACI |

## Assumes Loaded

| Methodology | Why |
|-------------|-----|
| `geek/ai/llm-integration/semantic-xml-content` | Authoring shape for `content/*.xml`. |
| `geek/ai/ml-engineer/ai-agent-patterns` | Pattern catalogue for agent loops referenced from this methodology. |

## Content (load on demand)

| File | Depth | What's inside | Est. tokens |
|------|-------|---------------|-------------|
| `content/01-core-rules.xml` | essential | 5 testable rules with statement + rationale + source | ~800 |
| `content/02-output-contract.xml` | essential | JSON Schema for produces=decision-record + valid/invalid examples + forbidden patterns | ~900 |
| `content/03-failure-modes.xml` | essential | 5 antipatterns with symptom / root-cause / fix | ~900 |
| `content/04-procedure.xml` | medium | 5-step procedure with input / action / output / decision-gate | ~700 |
| `content/05-examples.xml` | medium | End-to-end worked example | ~500 |
| `content/06-decision-tree.xml` | essential | Root question + branches with `when` observables → conclusion(ref=rule-id) | ~400 |

## Task Routing

| Sub-task | Model | Rationale |
|----------|-------|-----------|
| `plan-step` | sonnet | Standard reasoning over the procedure / scoring axes. |
| `author-output` | sonnet | Produces the artefact in the shape `produces=decision-record`. |
| `audit-validate` | haiku | Mechanical schema check via `scripts/validate-ai-agent-patterns.py`. |
| `senior-review` | opus | Cross-artefact judgement on rejection / approval. |

## Templates

| File | Purpose |
|------|---------|
| `templates/plan-execute-skeleton.py` | Plan-Execute pattern skeleton |
| `templates/react-system-prompt.txt` | ReAct system prompt template |
| `templates/reflection-critic-prompt.txt` | Reflection critic prompt template |
| `templates/tool-definition.json` | Tool definition reused across patterns |
| `templates/patterns-decision-record.md` | Decision record skeleton |

Files the packer does not ship standalone have their bodies inlined under `## Template Contents` at the end of this file - read them there, do not fetch the path.

## Scripts

| File | Purpose | When to call |
|------|---------|--------------|
| `scripts/validate-ai-agent-patterns.py` | Validate an output artefact against the JSON schema from `content/02-output-contract.xml`. | Pre-merge on the artefact PR + `--self-test` in CI. |

## Related

- [[ai-agent-patterns]] — pattern catalogue this methodology routes through.
- [[agents-production-deployment]] — production gates this methodology feeds into.
- external: rule rationales cite the sources in `content/01-core-rules.xml`.

## Decision tree

The mandatory tree at `content/06-decision-tree.xml` picks the right rule branch for the current task. Branches use observable inputs (numeric / boolean / categorical) and every leaf cites one of `r1-two-axes`, `r2-default-react`, `r3-plan-execute-when-long`, `r4-reflection-when-self-correct`, `r5-multi-agent-when-roles` from `content/01-core-rules.xml`.

## Template Contents

Bodies of the templates above that the packer does not ship as standalone files, inlined here so they are deliverable.

### `templates/plan-execute-skeleton.py`

```python
"""Skeleton for the `ai-agent-patterns` template `plan-execute-skeleton.py` — fill the placeholders."""
from __future__ import annotations
from dataclasses import dataclass


@dataclass
class Skeleton:
    slug: str = "ai-agent-patterns"
    version: str = "1.1.0"
    owner: str = "role:person"
    approver: str = "role:person"

    def render(self) -> dict:
        return {
            "slug": self.slug,
            "version": self.version,
            "owner": self.owner,
            "approver": self.approver,
        }


if __name__ == "__main__":
    import json
    import sys
    sys.stdout.write(json.dumps(Skeleton().render(), indent=2) + "\n")
```

### `templates/react-system-prompt.txt`

```text
# React System Prompt
# Prompt skeleton for ai-agent-patterns.

SYSTEM: You are applying methodology `ai-agent-patterns`. Honour every rule in content/01-core-rules.xml.
USER: <task input>
ASSISTANT (expected shape): <see content/02-output-contract.xml>
```

### `templates/reflection-critic-prompt.txt`

```text
# Reflection Critic Prompt
# Prompt skeleton for ai-agent-patterns.

SYSTEM: You are applying methodology `ai-agent-patterns`. Honour every rule in content/01-core-rules.xml.
USER: <task input>
ASSISTANT (expected shape): <see content/02-output-contract.xml>
```

### `templates/tool-definition.json`

```json
{
  "_header": "purpose: Tool definition reused across patterns | consumes: Inputs declared in AGENTS.md Prerequisites. | produces: Filled artefact for ai-agent-patterns matching content/02-output-contract.xml. | depends-on: content/01-core-rules.xml, scripts/validate-ai-agent-patterns.py | token-budget-impact: small",
  "purpose": "Tool definition reused across patterns",
  "consumes": "Inputs declared in AGENTS.md Prerequisites.",
  "produces": "Filled artefact for ai-agent-patterns matching content/02-output-contract.xml.",
  "depends-on": [
    "content/01-core-rules.xml",
    "scripts/validate-ai-agent-patterns.py"
  ],
  "token-budget-impact": "small",
  "_": "real fields below (this is a template; fill or remove the metadata header)",
  "name": "<tool_name>",
  "description": "<short description>",
  "input_schema": {
    "type": "object",
    "properties": {},
    "required": []
  }
}
```
