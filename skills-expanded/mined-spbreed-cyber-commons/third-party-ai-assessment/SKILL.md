---
name: third-party-ai-assessment
description: >-
  Assess the AI components of a supply chain for the two properties that make
  them different — silent change, and running with agent authority — and
  invalidate the control tests that predate a model change. Use when a model
  provider changed the model and you need to know what that invalidates, and at
  vendor assessment or renewal.
allowed-tools: Read, Grep, Glob
---

# The vendor changed the model and your control tests expired

Third-party AI differs from ordinary third-party software in two ways. A hosted
model can change underneath you with no change record on your side, which
invalidates every control test taken before it. And a tool package or MCP
connector runs **with your agent's authority**, so its risk is not the
vendor's — it is yours.

## When to use this

Vendor assessment, renewal, and any time a provider announces a model update.

## Procedure

**1 — Enumerate the AI components.** Hosted models, tool packages, MCP servers,
embedded features in products you already bought. The last category is the one
nobody lists.

**2 — Score each on the two properties.** Can it change without telling you, and
does it execute with your agent's authority? Either one alone justifies a higher
tier than the ordinary assessment would give.

**3 — Record the last known model version, with a date.** Without it you cannot
tell whether a control test predates a change, which makes the next step
impossible.

**4 — Invalidate control tests taken before the change.** Not "review" — mark
them unevidenced. A test performed against a different model is not weak
evidence, it is evidence about something else.

**5 — Ask the questions a contract can answer.** Notice period for model change,
whether the version is pinnable, what telemetry you get, and exit. Then record
which ones the vendor declined; that list is the assessment.

## Example

**Input** — the fixture committed at the top of [`scripts/third_party_ai_assessment.py`](scripts/third_party_ai_assessment.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
component                               kind          tier    flags
------------------------------------------------------------------------------------------------
cryptography==42.0.5                    library       low     —
langchain==0.2.1                        library       medium  unsigned
hosted GLM-4.6 endpoint                 hosted model  high    unsigned, not version-pinned, CAN CHANGE WITHOUT NOTICE
local glm-4.6 weights (pinned digest)   weights       low     —
mcp-jira-connector==0.0.3               tool package  high    unsigned, runs with agent authority
your controls were tested against a model that changed 5 days ago:
```

The run continues past this. `test_skills.py` executes the script on every
build, **with no model configured** — so what CI proves is that it runs and
refuses legibly, not that it prints these lines. The output above is a recorded
run against a real model, and nothing re-diffs it: a model's answer is not
reproducible, and this repository does not claim otherwise anywhere it can be
checked.

## Output contract

```json
{
  "components": [{"name": "str", "kind": "model|tool|mcp|embedded",
                  "silent_change": true, "runs_with_agent_authority": false, "tier": "str"}],
  "versions": [{"component": "str", "version": "str", "as_of": "str", "changed_at": "str|null"}],
  "control_tests": [{"id": "str", "tested_at": "str", "status": "valid|unevidenced", "why": "str"}],
  "contract_questions": [{"question": "str", "answered": false}]
}
```

## Failure modes

- **Assessing the vendor and not the authority.** The connector runs as your
  agent.
- **Keeping a control test that predates a model change.** It evidences the old
  model.
- **Missing embedded AI features.** They arrived with a product you already
  own.
