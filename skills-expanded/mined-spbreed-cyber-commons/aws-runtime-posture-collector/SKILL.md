---
name: aws-runtime-posture-collector
description: >-
  Snapshot a deployment's cloud network, crypto and logging posture as
  evidence for default-deny and egress controls. Use to evidence network
  isolation, to check whether private endpoints and endpoint policies are in
  place, or to record the runtime configuration an attestation depends on.
allowed-tools: Bash, Read
---

# Aws Runtime Posture Collector

**Controls:** Controls 1 and 2 — runtime posture

## What this collects

Configuration state, at a point in time, for the network and crypto boundary
around one deployment. It is evidence for other skills' verdicts rather than a
verdict in itself.

## When to use this
When an attestation needs to say something about the network, and therefore
after the deployment is running. The claims it supports — default-deny egress,
private endpoints, log retention — are runtime facts that no static analysis
can reach, and re-collecting is what makes the attestation re-issuable when the
posture drifts.

## Procedure

1. **Security groups and network ACLs.** Enumerate egress rules. Any rule
   permitting `0.0.0.0/0` outbound is an egress-open finding regardless of what
   an application-layer policy says.
2. **Private endpoints.** Record whether a private endpoint exists for each
   model and gateway service in use, and read the endpoint policy — an
   unscoped endpoint policy is an endpoint that permits any principal.
3. **Route tables.** Identify NAT and internet gateways on the deployment's
   subnets. A private endpoint does not help if a default route to an internet
   gateway remains.
4. **Key policies.** Record key policies and condition keys that scope use to a
   specific service. Unconditioned key access is a finding.
5. **Logging.** Confirm the audit trail and log destinations are enabled and
   delivering, and record the retention.

## Example

**Input** — the fixture committed at the top of [`scripts/aws_runtime_posture_collector.py`](scripts/aws_runtime_posture_collector.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
control  state           age (days)
------------------------------------
AC-1     PASS                   2.0
AC-2     PASS                   9.0
SB-1     STALE                 31.0
SB-2     STALE                120.0
EV-1     PASS                   5.0
EV-2     PASS                  12.0
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
  "collected_at": "str",
  "network": {
    "egress_open_findings": [{"sg": "str", "rule": "str"}],
    "private_endpoints": [{"service": "str", "present": true, "policy_scoped": true}],
    "internet_route_present": false
  },
  "crypto": {"keys": [{"id": "str", "conditioned": true}]},
  "logging": {"audit_trail_enabled": true, "log_destinations": ["str"], "retention_days": 0},
  "verdict": "PASS|PARTIAL|FAIL"
}
```

## Failure modes

- **Reading configuration and calling it enforcement.** This skill records what
  is configured. Whether traffic actually obeys it is the egress verifier's job.
- **Ignoring the route table** because a private endpoint exists.
- **Recording that logging is enabled** without checking that it is delivering.
