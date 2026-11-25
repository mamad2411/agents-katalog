---
name: aws-iam-policy-simulator
description: >
  AWS IAM Policy Simulator for owned accounts: simulate-principal-policy and
  simulate-custom-policy, resource/context keys, batch testing allow/deny matrices,
  and CI checks before policy deploys. Use when validating IAM changes safely —
  not as a substitute for runtime authorization testing of application logic.
---

# AWS IAM Policy Simulator

## Scope And Authorization

- **In scope:** Simulating IAM policies for principals and resources in authorized accounts.
- **Out of scope:** Using simulation to probe unauthorized third-party accounts.
- Simulator results can differ from real evaluation when context keys or service-specific conditions are incomplete — always follow with canaries.
- Do not treat “implicit deny” surprises as simulator bugs without checking SCP/boundaries/session policies.
- Pair with `aws-iam-least-privilege` for fixes; `code-quality-standards` for automation.

## When To Use

- Before attaching a new managed policy version.
- Building allow/deny matrices for roles (get/put/delete on specific ARNs).
- Debugging unexpected AccessDenied with simulated context keys.
- CI gate: required actions must return `allowed`; forbidden actions `implicitDeny`/`explicitDeny`.
- Comparing two policy documents without deploying.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| Designing policies | `aws-iam-least-privilege` |
| Unused permission cleanup | `aws-iam-access-analyzer-unused` |
| KMS grants evaluation | `aws-kms-grants` |
| App-level authz (ABAC in app) | application auth skills |
| Implementation quality baseline | `code-quality-standards` |

## Domain Focus

| API | Use |
| --- | --- |
| `simulate-principal-policy` | Effective identity policies for an existing principal |
| `simulate-custom-policy` | Trial policy documents without attach |
| Context entries | Supply `aws:SourceIp`, tags, MFA, etc. |
| Resource ARNs | Required for resource-level actions |
| Limitations | SCPs, resource policies, and some conditions need care |

## Evaluation Outcome Codes

| Result | Meaning |
| --- | --- |
| `allowed` | Explicit allow path matched |
| `explicitDeny` | Deny statement matched |
| `implicitDeny` | No allow matched |

## Workflow

### 1. Confirm scope and success criteria

1. Record principal ARN, candidate policy changes, actions/resources matrix.
2. Success: required cells allowed; cross-tenant cells denied; CI runs simulator on PR.
3. Note SCPs that might still deny in real accounts after allow in IAM.

### 2. Inventory principal policies

```bash
ROLE_ARN=arn:aws:iam::ACCT:role/app-role
aws iam list-attached-role-policies --role-name app-role
aws iam list-role-policies --role-name app-role
aws iam get-role --role-name app-role
```

1. Include permission boundary ARNs if present.
2. List resource policies on target (bucket policy, KMS) separately — simulator identity-only vs full request context nuances.

### 3. Baseline

1. Simulate **current** principal for matrix → store JSON results.
2. Capture real AccessDenied errors from CloudTrail for comparison.
3. Draft desired matrix table in ticket.

### 4. Run simulations

**Principal simulation:**

```bash
aws iam simulate-principal-policy \
  --policy-source-arn "$ROLE_ARN" \
  --action-names s3:GetObject s3:PutObject s3:DeleteObject \
  --resource-arns \
    arn:aws:s3:::team-a/data.txt \
    arn:aws:s3:::team-b/data.txt \
  --output json > sim-current.json
```

**Custom policy trial:**

```bash
aws iam simulate-custom-policy \
  --policy-input-list file://policy-vnext.json \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::team-a/data.txt
```

**Context keys example:**

```bash
aws iam simulate-principal-policy \
  --policy-source-arn "$ROLE_ARN" \
  --action-names s3:GetObject \
  --resource-arns arn:aws:s3:::team-a/data.txt \
  --context-entries \
    ContextKeyName=aws:RequestedRegion,ContextKeyValues=us-east-1,ContextKeyType=string \
    ContextKeyName=aws:MultiFactorAuthPresent,ContextKeyValues=true,ContextKeyType=boolean
```

**Matrix automation sketch**

1. YAML of `{action, resource, expect}`.
2. Script calls simulator; fails CI on mismatch.
3. Print only failed cells in PR comments.

### 5. Verify with evidence

1. Diff sim-current.json vs sim-next.json for unintended allows.
2. Deploy to non-prod and run real API canary with same identity.
3. Confirm SCP: if org denies Region, real call fails even if simulator allow — document.

```bash
jq '.EvaluationResults[] | {Action, ResourceName, Decision}' sim-next.json
```

### 6. Observe and harden

1. Re-run matrix when AWS managed policies update.
2. Include new actions in matrix when features ship.
3. Store simulation outputs as build artifacts (no secrets).

### 7. Hand off

1. Publish matrix + CI job name.
2. Onboarding: how to add a new required action test.
3. Link least-privilege skill for remediation patterns.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Matrix | require + forbid cells | only test happy path allows |
| Context | supply realistic keys | empty context when policy depends on tags |
| Scope | principal + canary | simulator alone as proof |
| CI | block bad allows | optional local-only sim |
| SCPs | document residual denies | assume IAM allow == org allow |
| Output | stored JSON evidence | “we clicked console once” |

## Output Checklist

- [ ] Principal and matrix defined
- [ ] Current simulation baselined
- [ ] Candidate policies simulated
- [ ] Context keys included where needed
- [ ] CI or scripted checks for matrix
- [ ] Real canary confirms critical allows
- [ ] SCP/resource-policy residual risks noted
- [ ] Artifacts attached to change ticket
- [ ] `aws-iam-least-privilege` applied for fixes

## Rules

- Authorized accounts only.
- Simulator is necessary but not always sufficient — canary in real env.
- Always test negative cases (should deny).
- Supply context keys used by conditions.
- Focus on simulation workflow; policy design and unused cleanup elsewhere.
