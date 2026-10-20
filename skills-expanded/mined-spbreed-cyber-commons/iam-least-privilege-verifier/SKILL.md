---
name: iam-least-privilege-verifier
description: >-
  Prove a deployment's role baseline is default-deny and quantify granted-
  but-unused permissions against observed usage. Use to evidence least
  privilege, to find excess permissions on an agent role, or when asked
  whether a deployment's IAM posture supports a default-deny claim.
allowed-tools: Bash, Read
---

# Iam Least Privilege Verifier

**Controls:** Control 1 — default-deny and least privilege

## Confidence: HIGH

This is one of the controls that is genuinely provable at runtime. Policy
documents are readable, and usage data turns "least privilege" from an
assertion into a measured delta.

## When to use this
Whenever a default-deny or least-privilege claim is about to be made, and again
whenever the role changes. It needs observed usage as well as the policy, so it
runs against a deployment that has been live long enough to have a usage
window — a fresh deployment shows every permission as unused and the result
means nothing.

## Procedure

1. **Establish the default-deny baseline.** Read every inline and attached
   policy. The baseline fails if any of these are present:
   - `Action: "*"` or `Resource: "*"` in an Allow statement
   - broad managed policies such as administrator or power-user equivalents
   - a wildcard principal on a trust policy

2. **Measure excess.** Compare granted permissions against observed usage from
   the access-analysis and last-accessed data. Count actions, roles, keys and
   passwords idle for at least the tracking period (configurable 1–180 days;
   default 90).

3. **Generate the least-privilege diff.** Policy generation derived from actual
   activity produces a candidate policy; the diff against what is granted is
   the excess-permission finding, expressed concretely rather than as a score.

4. **Check external access.** External-access findings must be zero, or each
   one must map to an approved exception.

## Example

**Input** — the fixture committed at the top of [`scripts/iam_least_privilege_verifier.py`](scripts/iam_least_privilege_verifier.py). Edit it and re-run: the buckets, counts and verdicts below are derived from it, not hard-coded.

**Output** — the opening lines of a real run:

```
   charge_card payments:booking          ['CHARGE']
   run_query   table:bookings            ['SELECT', 'UPDATE']
   send_email  domain:cybertravels.com   ['*']
allow-by-default:
   run_query   table:bookings                SELECT ALLOW run_query on table:bookings permits SELECT
   run_query   table:customer_pii            SELECT ALLOW allowed by default
   charge_card payments:booking              REFUND deny  REFUND not permitted on payments:booking (only ['CHARGE'])
   send_email  domain:archive.evil.example   *      ALLOW allowed by default
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
  "role_arn": "str",
  "default_deny_verified": true,
  "wildcard_findings": [{"policy": "str", "statement": "str"}],
  "excess_permission_count": 0,
  "unused": [{"type": "action|role|key|password", "name": "str", "idle_days": 0}],
  "generated_policy_diff": "str",
  "external_access_findings": 0,
  "tracking_period_days": 90,
  "verdict": "PASS|PARTIAL|FAIL"
}
```

## Failure modes

- **Incomplete audit-trail coverage.** If the trail is not intact, "unused" is
  unreliable and the verdict must be `PARTIAL`. Policy generation can miss
  legitimately-used-but-rare actions — an annual disaster-recovery permission
  looks identical to dead permission over a 90-day window.
- **Counting managed-policy names instead of effective actions.** Two policies
  can grant the same action; the union is what matters.
- **Treating a low excess count as a pass** while a wildcard is present. The
  baseline check is a gate, not a contributor to a score.
