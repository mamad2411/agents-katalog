---
name: risk-registry-integrator
description: >-
  Pull open risks and exceptions for the downstream services an agent or its
  MCP tools connect to, and map them to the deployment. Use to roll up
  inherited risk, to find expired exceptions on a dependency, or when asked
  what a deployment inherits from the systems it calls.
allowed-tools: Bash, Read
---

# Risk Registry Integrator

**Controls:** Cross-cutting — inherited risk

## What this adds

A deployment's own controls can be clean while every system it calls is
carrying an accepted risk. Inherited risk is invisible unless something joins
the downstream inventory to the register, and this skill is that join.

## When to use this
When assembling a deployment's risk position, and every time a downstream it
depends on changes. An agent's risk is the union of its own and every
downstream its tools reach, and that union is built by pulling each downstream
register rather than by asking each team.

## Procedure

1. **Take the downstream inventory** from the inventory resolver. Do not build
   a second list — a divergence between the two is itself the finding.
2. **Query the register per downstream.** Open risks with severity and status,
   plus any accepted exceptions.
3. **Check exception expiry.** Expired and approaching-expiry exceptions are
   separate categories and are treated differently.
4. **Find unmapped downstreams.** A dependency with no register entry is not a
   dependency with no risk; it is one nobody has assessed.
5. **Roll up.** The deployment inherits the highest open severity among its
   dependencies, and that number belongs in the attestation.

## Example

**Input** — the fixture committed at the top of [`scripts/risk_registry_integrator.py`](scripts/risk_registry_integrator.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
family                                       risks  ids
identity and authorisation                       3  R1, R5, R11
code and CI/CD pipeline                          2  R7, R8
lateral movement and logging                     2  R9, R10
RAG misconfiguration and data exposure           1  R12
guardrail tampering                              1  R2
local filesystem manipulation                    1  R6
prompt injection and instruction hijacking       1  R3
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
  "deployment_id": "str",
  "downstreams": [
    {"service": "str",
     "open_risks": [{"id": "str", "severity": "critical|high|medium|low", "status": "str"}],
     "exceptions": [{"id": "str", "expires": "str", "state": "active|expiring|expired"}],
     "in_register": true}
  ],
  "unmapped_downstreams": ["str"],
  "inherited_severity": "critical|high|medium|low|none",
  "verdict": "PASS|PARTIAL|FAIL"
}
```

## Failure modes

- **Treating an unmapped downstream as clean.** Absence of a record is absence
  of assessment.
- **Ignoring expired exceptions** because the risk is still recorded as
  accepted. An expired exception is an open risk with a date on it.
