---
name: entitlement-overprivilege-analyzer
description: >-
  Analyse entitlement and identity registries to find over-privileged access
  held by a deployment's identities. Use to check granted entitlements
  against what the declared tools actually need, to find over-broad OAuth
  scopes on credential providers, or to find standing privilege.
allowed-tools: Bash, Read
---

# Entitlement Overprivilege Analyzer

**Controls:** Controls 1 and 3 — over-privileged access

## What this adds beyond the IAM verifier

The IAM verifier measures cloud permissions against cloud usage. This skill
measures **application-level entitlements** — relationship-graph authorisation,
OAuth scopes on stored credential providers, and identity-registry
relationships — against what the declared tool surface actually requires.

An agent can hold a minimal cloud role and an OAuth token with full mailbox
access.

## When to use this
After the IAM baseline is verified, not instead of it. The IAM verifier asks
whether the role is default-deny; this asks whether the entitlements actually
granted exceed what the declared tools need. Reach for it when scopes were
granted at integration time, when a credential provider holds OAuth scopes
nobody has reviewed, or when looking for standing privilege.

## Procedure

1. **Take the required capability set** from the code-surface analyzer. This is
   the denominator: what the declared tools genuinely need.
2. **Enumerate granted entitlements** from the authorisation graph for every
   identity in the deployment manifest.
3. **Enumerate credential-provider scopes.** Stored OAuth scopes are frequently
   far wider than the tool needs, because the consent screen offered a bundle.
4. **Diff.** Every grant with no corresponding requirement is an over-privilege
   finding, and each needs a justification gap recorded — the grant, the
   requirement it was presumably for, and the absence.
5. **Flag standing privilege.** Any grant that is permanent rather than issued
   per task.

## Example

**Input** — the fixture committed at the top of [`scripts/entitlement_overprivilege_analyzer.py`](scripts/entitlement_overprivilege_analyzer.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   the task's own write      ok      permitted
   a different report        REFUSED bound to report/8812
   a different scope         REFUSED scoped to reports:write
   after the task completes  REFUSED task closed
   after the TTL expires     REFUSED expired

An injection landing at 09:14 needs a task to be open, on the resource
it wants, holding the scope it wants. Standing authority required none
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
  "identities": [
    {"id": "str",
     "granted": ["str"],
     "required_by_tools": ["str"],
     "excess": [{"grant": "str", "justification_gap": "str"}]}
  ],
  "oauth_scope_excess": [{"provider": "str", "granted_scope": "str", "needed_scope": "str"}],
  "standing_privilege": ["str"],
  "verdict": "PASS|PARTIAL|FAIL"
}
```

## Failure modes

- **Comparing grants against other grants.** The denominator is the tool
  surface, not a peer deployment.
- **Accepting a bundled OAuth scope** because it was what the provider offered.
- **Missing standing privilege** because the scope itself looked narrow.
