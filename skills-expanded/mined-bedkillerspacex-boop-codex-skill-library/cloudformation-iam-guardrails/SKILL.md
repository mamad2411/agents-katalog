---
name: cloudformation-iam-guardrails
description: >
  CloudFormation IAM guardrails for owned AWS accounts: roles and policies in templates,
  CAPABILITY_IAM / CAPABILITY_NAMED_IAM deploy gates, permissions boundaries, CloudFormation
  service roles, stack policies, and least-privilege policies. Use when hardening or reviewing
  CloudFormation YAML/JSON that creates IAM, pipelines that pass capabilities, or stack-update
  protection — not for abusing third-party AWS accounts.
---

# CloudFormation IAM Guardrails

## Scope And Authorization

- **In scope:** AWS accounts and templates you own or are authorized to review.
- **Out of scope:** privilege escalation against accounts outside engagement scope.
- Prefer policy changes in non-prod; keep break-glass admin path documented.
- Redact account IDs and policy ARNs in public notes when required.
- Pair with `cloudformation-hooks` for proactive enforcement and `code-quality-standards`.

## When To Use

- Templates create `AWS::IAM::Role`, policies, instance profiles, users (avoid users).
- CI passes `--capabilities CAPABILITY_IAM` / `CAPABILITY_NAMED_IAM`.
- Need CFN **service role**, **permissions boundaries**, or **stack policies** for update protection.
- Tokens: CAPABILITY_IAM, permissions boundary, stack policy, CFN service role, IAM policy in YAML.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| CFN Hooks for general resources | `cloudformation-hooks` |
| Org SCPs | org/SCP skill |
| App runtime IAM (IRSA etc.) | workload identity skill |
| Secrets in templates | `secrets-management-hygiene` |
| Human IdP access reviews | IAM identity center skill |

## Risk Surface

| Risk | Why it matters |
| --- | --- |
| Wildcards in Action/Resource | Easy privilege explosion via stack update |
| Named IAM with CAPABILITY_NAMED_IAM | Overwrites/creates powerful named roles |
| Pipeline uses admin credentials | Any template becomes account admin |
| No stack policy | Critical IAM resources freely replaceable |
| Inline * policies | Hard to review; drifts |

## Workflow

### 1. Confirm scope and success criteria

1. Stacks/pipelines, who can deploy, whether service roles used.
2. Success: least-privilege roles deploy; unauthorized capability use blocked; critical resources protected.
3. Rollback: previous template version + known-good role policies.

### 2. Inventory IAM in templates

```bash
rg -n "AWS::IAM::|CAPABILITY_IAM|CAPABILITY_NAMED_IAM|PermissionsBoundary|ManagedPolicyArns" -g '*.yaml' -g '*.yml' -g '*.json' -g '*.template'
aws cloudformation get-template --stack-name my-stack --query TemplateBody --output text | head
```

1. List roles created and attached policies.
2. Check deploy role / pipeline role permissions.

### 3. Template guardrails

**Prefer:**

```yaml
Resources:
  AppRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${AWS::StackName}-app"   # careful with named IAM
      PermissionsBoundary: !Sub "arn:aws:iam::${AWS::AccountId}:policy/OrgBoundary"
      AssumeRolePolicyDocument:
        Version: "2012-10-17"
        Statement:
          - Effect: Allow
            Principal: { Service: lambda.amazonaws.com }
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
      Policies:
        - PolicyName: app-data
          PolicyDocument:
            Version: "2012-10-17"
            Statement:
              - Effect: Allow
                Action: ["s3:GetObject"]
                Resource: !Sub "arn:aws:s3:::${DataBucket}/*"
```

1. **No** `Action: "*"` / `Resource: "*"` unless break-glass and reviewed.
2. Prefer customer-managed policies with tight resources over AdministratorAccess.
3. Avoid creating IAM **users** / long-lived access keys in CFN.
4. Always attach **permissions boundary** for roles created by app pipelines if org standard.

### 4. Deploy-time gates

| Gate | Practice |
| --- | --- |
| Capabilities | Grant `CAPABILITY_IAM` only to pipelines that need it; separate from app deploy roles when possible |
| CFN service role | Stack operations assume limited service role; humans don’t use root |
| Change sets | Review IAM diffs before execute |
| Stack policy | Deny updates/deletes on critical IAM roles without explicit allow |
| Hooks / SCP | Block `iam:CreateUser` etc. at org level if policy requires |

```bash
aws cloudformation deploy \
  --template-file tpl.yaml \
  --stack-name app \
  --capabilities CAPABILITY_NAMED_IAM \
  --role-arn arn:aws:iam::123456789012:role/cfn-service-role
```

**Stack policy sketch:**

```json
{
  "Statement": [{
    "Effect": "Deny",
    "Principal": "*",
    "Action": ["Update:Replace", "Update:Delete"],
    "Resource": "LogicalResourceId/AppRole"
  }]
}
```

### 5. Verify

1. Access Analyzer / IAM Access Advisor on created roles after traffic.
2. Deploy template with overly broad policy → blocked by boundary/hook/SCP if configured.
3. Change set shows IAM resource changes; require security review label.
4. Confirm pipeline role cannot attach AdministratorAccess to new roles.

### 6. Operate

1. Periodic scan of stacks for IAM resources without boundaries.
2. Alert on `CAPABILITY_NAMED_IAM` deploys from unusual principals.
3. Quarterly removal of unused managed policies created by stacks.

### 7. Hand off

1. Standard role modules (CDK constructs / CFN macros) for app teams.
2. Runbook: exception for elevated policy with expiry.
3. Link hooks for automated property checks.

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Policy | Resource-scoped actions | `*` on `*` |
| Deploy identity | CFN service role least privilege | Long-lived admin access keys in CI |
| Boundaries | Org boundary on app-created roles | Unbounded CreateRole |
| Review | Change set IAM focus | Blind execute |
| Stack policy | Protects prod IAM logical IDs | Fully mutable prod identity |

## Output Checklist

- [ ] IAM resources in templates inventoried
- [ ] Least-privilege policies + boundaries applied
- [ ] Pipeline capabilities and service roles tightened
- [ ] Stack policies on critical resources
- [ ] Change set / analyzer verification done
- [ ] No unnecessary users/keys in templates
- [ ] Exceptions documented with expiry
- [ ] Residual privilege risks accepted explicitly

## Rules

- Owned accounts only; treat IAM template changes as high risk.
- Prefer reversible stack updates and change sets.
- Evidence from analyzer and denied deploys.
- Focus on **CFN IAM guardrails**; general org SCPs and hooks are companions.
