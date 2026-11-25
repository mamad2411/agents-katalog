---
name: cloudformation-hooks
description: >
  Deploy CloudFormation Hooks for proactive control of stack operations: guard
  resource configurations before create/update, activate hooks in accounts, write
  Lambda/Guard hook handlers, and fail noncompliant templates early. Use on owned
  AWS accounts/orgs — complements cloudformation-iam-guardrails and SCPs; not for
  attacking other accounts’ stacks.
---

# CloudFormation Hooks

## Scope And Authorization

- **In scope:** AWS accounts/organizations you administer; authorized landing-zone work.
- **Out of scope:** enabling hooks that disrupt accounts without owner approval; reading other tenants’ templates.
- Stage hooks in non-prod OUs first; document break-glass bypass if used.
- Redact account IDs and hook payload samples containing secrets.
- Pair hook handler code with `code-quality-standards`.

## When To Use

- Blocking noncompliant resources at **CloudFormation** provision time (not only Config after-the-fact).
- Enforcing encryption, public access blocks, required tags, approved AMIs, etc. via hooks.
- Tokens: CloudFormation Hooks, Hook targets, activation, Guard hook, Lambda hook, FAIL/WARN.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| IAM in templates / CAPABILITY_* | `cloudformation-iam-guardrails` |
| Org SCPs / Control Tower | landing-zone / org policy skills |
| Terraform policy-as-code | OPA/Sentinel / Terraform skills |
| Runtime Config rules only | AWS Config skill |
| Secrets hygiene | `secrets-management-hygiene` |

## Concepts

| Term | Meaning |
| --- | --- |
| Hook | Proactive validation invoked during stack operations |
| Target | Resource types / stack-level operations the hook evaluates |
| Activation | Account/region enablement and target filters |
| Result | `SUCCESS`, `FAILURE` (block), or warning-style behaviors per design |
| Handler | Lambda or Guard rules evaluating request properties |

## Workflow

### 1. Confirm scope and success criteria

1. Accounts/OUs, regions, resource types in scope, enforcement mode (warn → fail).
2. Success: noncompliant create/update fails with clear message; compliant stacks still deploy; operators know how to fix.
3. Rollback: deactivate hook or set filter to empty targets temporarily with ticket.

### 2. Inventory provisioning paths

```bash
aws cloudformation list-stacks --stack-status-filter CREATE_COMPLETE UPDATE_COMPLETE
aws cloudformation list-types --type HOOK --visibility PUBLIC
# Also note CDK/SAM/Service Catalog that compile to CFN
```

1. Map who can `cloudformation:CreateStack` and whether service roles are used.
2. Existing Config rules / SCPs overlapping hooks (avoid contradictory messages).

### 3. Choose control content

| Control example | Hook checks |
| --- | --- |
| S3 | Public access block on, encryption SSE-S3/KMS |
| Security Group | No `0.0.0.0/0` on admin ports |
| IAM Role | No `*` on sensitive actions without boundary |
| Tags | `Owner`, `CostCenter` present |
| RDS | Storage encrypted, not publicly accessible |

Prefer few high-value hooks over dozens of noisy ones.

### 4. Implement and activate

**Guard-oriented pattern (conceptual):** write rules that assert properties on `AWS::S3::Bucket` etc., package as hook, register type, activate for account/region.

**Lambda hook pattern:** handler receives resource properties; return failure with remediation text.

```bash
# After packaging (org-specific pipeline)
aws cloudformation set-type-configuration \
  --type HOOK \
  --type-name MyOrg::Security::ComplianceHook \
  --configuration '{"CloudFormationConfiguration":{"HookConfiguration":{"TargetStacks":"ALL","FailureMode":"FAIL","Properties":{}}}}'
```

1. Start with `TargetStacks` limited or FailureMode warn-equivalent during pilot if available in your setup; then FAIL.
2. Grant hook execution role least privilege to evaluate only needed APIs.
3. Version hooks; pin activations.

### 5. Verify

```bash
# Deploy intentional noncompliant template → expect hook failure
aws cloudformation deploy --template-file bad-s3.yaml --stack-name hook-test-bad
# Deploy compliant template → success
aws cloudformation deploy --template-file good-s3.yaml --stack-name hook-test-good
```

1. Capture error message quality for operators.
2. Ensure CDK/SAM paths also hit hooks (they use CFN).
3. Measure false positive rate with app teams.

### 6. Operate

1. Dashboard: hook failure counts by type and stack.
2. Change process for new exceptions (temporary filter + ticket + expiry).
3. Align with `cloudformation-iam-guardrails` for IAM-specific template reviews.

### 7. Hand off

1. Catalog of hooks, owners, failure modes, OUs.
2. Runbook: interpret hook error, fix template, request exception.
3. IaC examples of compliant patterns in platform docs.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rollout | Pilot OU then expand | Global FAIL day-one untested |
| Messages | Actionable remediation | Opaque Lambda timeout |
| Scope | Critical resource types | Hook on every type with flaky logic |
| Exceptions | Time-boxed | Permanent silent disable |
| Overlap | Document vs SCP/Config | Triple-fail confusing |

## Output Checklist

- [ ] Scope accounts/regions/types defined
- [ ] Controls prioritized with owners
- [ ] Hook packaged, registered, activated
- [ ] Noncompliant stack blocked with clear error
- [ ] Compliant path verified (incl. CDK/SAM if used)
- [ ] Monitoring and exception process live
- [ ] Docs/examples for app teams
- [ ] Residual gaps (non-CFN provisioners) noted

## Rules

- Owned AWS only; coordinate before account-wide FAIL mode.
- Prefer reversible activation changes.
- Evidence from failed/succeeded deploys.
- Focus on **CFN Hooks**; IAM template guardrails and SCPs are related but separate.
