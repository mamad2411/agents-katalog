---
name: deployment-inventory-resolver
description: >-
  Resolve a deployment_id into the artifacts that make up one agentic
  deployment and build the evidence graph every other attestation skill
  consumes. Use first, before any control is evaluated, or when asked which
  repo, image, role, workload identity, gateway or guardrail a deployment
  actually consists of.
allowed-tools: Bash, Read, Grep, Glob
---

# Deployment Inventory Resolver

**Controls:** All — this skill produces the join key

## Why this runs first

`deployment_id` is the primary key for every other skill in this set. Without
it, an IAM finding, a SPIFFE entry and a gateway policy are three unrelated
facts about three things that may or may not be the same system.

This skill turns that ID into a manifest of content-addressed artifacts, so
every later finding resolves to one evaluable unit and cannot be silently
confused with a neighbouring deployment.

## When to use this
**First, before any control is evaluated.** Nothing else in this chain can run
without a resolved `deployment_id`: an IAM finding, an identity entry and a
gateway policy are three unrelated facts until something establishes they
describe the same system. Also run it whenever anyone asks which repo, image,
role, workload identity, gateway or guardrail a deployment actually consists
of — that question is usually answered from memory and usually wrongly.

## Procedure

1. **Resolve the code.** Repository URL plus the exact commit SHA that was
   built. Not a branch — a branch moves.
2. **Resolve the image.** Registry digest (`sha256:…`), not a tag. Confirm the
   digest matches the revision actually deployed, not the newest build.
3. **Resolve the runtime identity.** The IAM role ARN, the SPIFFE ID, and —
   on platforms that auto-create one — the workload identity ARN exposed by the
   runtime/gateway description API.
4. **Resolve the traffic path.** Gateway or route ARN, and the guardrail ID
   attached to it.
5. **Resolve the downstreams.** Every service the deployment's tools call.
   These become the input to the risk-registry skill.
6. **Cross-link and check completeness.** Every artifact must reference the
   others. Report orphans rather than omitting them.

## Example

**Input** — the fixture committed at the top of [`scripts/deployment_inventory_resolver.py`](scripts/deployment_inventory_resolver.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
asset                             kind              autonomy  owner         found via
--------------------------------------------------------------------------------------------
fraud-scoring-model               model             L1        risk-eng      registry
support-summariser                copilot           L1        support-eng   registry
vendor-contract-analyser          embedded-feature  L1        —             expense report
unknown-openai-usage-marketing    copilot           L1        —             egress logs
pr-remediation-agent              agent             L2.5      —             egress logs
agent-worker-7f3c                 agent             L2.5      —             egress logs
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
  "resolved_at": "str",
  "artifacts": {
    "repo": {"url": "str", "commit": "str"},
    "image": {"registry": "str", "digest": "str", "matches_deployed": true},
    "identity": {"role_arn": "str", "spiffe_id": "str", "workload_identity_arn": "str"},
    "traffic": {"gateway_arn": "str", "guardrail_id": "str"},
    "downstreams": ["str"]
  },
  "missing": ["str"],
  "orphans": ["str"],
  "verdict": "PASS|PARTIAL|FAIL"
}
```

A manifest with entries in `missing` is `PARTIAL` at best. Every downstream
skill inherits that ceiling — you cannot attest a control on an artifact you
could not resolve.

## Failure modes

- **Resolving a tag instead of a digest.** Tags are mutable; the thing you
  attested is not necessarily the thing running.
- **Treating an unresolvable artifact as absent.** "No gateway configured" and
  "I could not read the gateway API" are different findings.
- **Reusing a manifest across runs.** Re-resolve. Drift is the point.
