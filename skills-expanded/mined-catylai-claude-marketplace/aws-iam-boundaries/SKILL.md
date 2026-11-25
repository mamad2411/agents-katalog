---
name: aws-iam-boundaries
description: "Designs and reviews AWS IAM roles, CI OIDC trust policies, permission boundaries and policy wildcards. Use when writing or reviewing an IAM role, trust policy or CI credential. Not for CI workflow YAML (use github-workflow:actions-authoring or gitlab-workflow:gitlab-ci-authoring)."
license: MIT
---

# AWS IAM Boundaries

Every ARN, account id and role name on this page is a placeholder —
`111111111111`, `222222222222`, `<role-name>`, `<org>`. Substitute your own.

Without a checkout or credentials (web), review the policy JSON or HCL the user pastes.

## Roles are for jobs, not for people

A role should answer one question: *what does this workload need in order to do its one
job?* Name it after the job, scope it to the job, and let people assume it rather than
holding a copy of its permissions.

| Anti-pattern | What it becomes | Instead |
| --- | --- | --- |
| A role per engineer | Permissions accrete and nothing is ever removed, because removing something might break "someone" | A small set of job roles, assumed by whoever is doing that job |
| One `deploy` role for every service | Any service's pipeline can act on any other service's resources | One deploy role per service, scoped by resource ARN prefix or tag |
| An IAM user with access keys for CI | A static credential in someone's secret store, valid until a human revokes it | Federated, short-lived credentials — see OIDC below |
| "Temporary" broad grant added during an incident | Permanent | A documented break-glass role with alerting on assumption |

Scope by resource, not only by action. `s3:GetObject` on `*` and `s3:GetObject` on
`arn:aws:s3:::<org>-app-dev-*/*` are different permissions that a policy-reading eye can
easily slide past.

## Assume-role chains

The pattern that removes standing permissions from compute:

```
CI compute identity                  target account role
(instance profile / OIDC principal)  (arn:aws:iam::111111111111:role/<deploy-role>)
        │                                     ▲
        │  policy: sts:AssumeRole only        │  trust policy: names the CI principal
        └─────────────────────────────────────┘  permission policy: what the job may do
```

Two properties make it worth the extra hop:

1. **The base identity can do nothing on its own.** Its only permission is
   `sts:AssumeRole` against an enumerated list of role ARNs. If that credential leaks, the
   attacker has the right to ask for roles they must also be trusted by.
2. **The trust relationship is the control, and it lives in the target account.** The team
   that owns the production account decides who may assume into it, and they can revoke it
   without coordinating with anyone.

The base identity's policy should list role ARNs explicitly:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "AssumeDeployRolesOnly",
    "Effect": "Allow",
    "Action": "sts:AssumeRole",
    "Resource": [
      "arn:aws:iam::111111111111:role/<deploy-role>",
      "arn:aws:iam::222222222222:role/<deploy-role>"
    ]
  }]
}
```

`"Resource": "*"` on `sts:AssumeRole` is one of the wildcards that matters. It converts
"this runner may reach these two accounts" into "this runner may reach any role in the
organization that trusts a principal in its account", and the set of such roles is not
something you can enumerate from where you are standing.

### Failure modes worth naming

- **Skipping the hop and using the compute identity directly.** Works on day one, and
  quietly gives every job on that runner every permission any job on it ever needed.
- **A chain the CLI cannot follow.** If the job never configures the profile that performs
  the assumption, the SDK falls back to ambient credentials and fails with an
  authorization error that reads like a permissions problem. The first diagnostic is
  always `aws sts get-caller-identity` — print the identity the job is actually using
  before debugging what it is allowed to do.
- **Different role paths for different account classes.** Network or shared-services
  accounts often use a different role path from workload accounts. Write the mapping down
  once, in one table, and reference it; a half-remembered path produces `AccessDenied` that
  looks like a policy problem and is a typo.

## OIDC federation instead of long-lived keys

An IAM user's access key for CI is a permanent credential stored outside AWS: it does not
expire, it gets copied, and rotating it is a change nobody schedules. With OIDC the CI platform
mints a short-lived signed token naming the project, ref and job, and
`sts:AssumeRoleWithWebIdentity` exchanges it for temporary credentials (one hour by default,
bounded by the role's maximum session duration).

Register the platform as an IAM OIDC provider once per account. GitHub and GitLab need no
certificate thumbprint: AWS validates them against its own trusted certificate authorities and
ignores any `thumbprint_list`, so leave it out of `aws_iam_openid_connect_provider` rather
than hardcoding a value that looks load-bearing.

The trust policy, with `<issuer>` being the provider host (`token.actions.githubusercontent.com`,
`gitlab.com`, or your self-managed GitLab host):

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {
      "Federated": "arn:aws:iam::111111111111:oidc-provider/<issuer>"
    },
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "<issuer>:aud": "sts.amazonaws.com",
        "<issuer>:sub": "<exact subject from the tables below>"
      }
    }
  }]
}
```

**The `sub` condition is the security boundary.** Without it, any job on that platform, in any
project anywhere, can assume the role.

Condition operators:

- **Pin `aud` with `StringEquals`.** It stops a token minted for another relying party being
  replayed at yours. Use `sts.amazonaws.com` (the value GitHub's AWS action requests; set it in
  GitLab's `id_tokens: <NAME>: aud:`), and make the provider's registered audience match.
- **Use `StringEquals` for `sub` unless the value contains a `*`.** Move only a deliberately
  wildcarded value into a `StringLike` block. A `StringLike` with no `*` invites someone to add
  one "just for a moment".

### GitHub Actions `sub`

| `sub` value | Who can assume | Verdict |
| --- | --- | --- |
| condition absent | Any workflow in any repository on GitHub | Broken |
| `repo:<org>/*` (StringLike) | Every workflow in every repository of the org, any branch or PR | Too broad for anything that can write |
| `repo:<org>/<repo>:*` (StringLike) | Every branch, tag, environment and PR of one repository | Too broad for anything that can read state: a PR branch can run a plan and read every secret in state |
| `repo:<org>/<repo>:pull_request` | Workflows triggered by PRs to the repository | Plan-only role, and only if you accept PR authors reading state |
| `repo:<org>/<repo>:ref:refs/heads/main` | Jobs on `main` that do **not** declare an environment | Deploy role without environments |
| `repo:<org>/<repo>:environment:production` | Jobs that declare `environment: production`, behind its protection rules | Deploy role; strongest |

A job that declares an environment gets the `environment:` subject **instead of** the `ref:`
subject, so the last two rows are alternatives, not a ranking: a deploy job that adds
`environment:` stops matching a `ref:` trust policy.

**Subject format varies by repository.** Newer repositories, repositories renamed or
transferred since GitHub's cutover, and those opted in to immutable subject claims use
`repo:<org>@<org-id>/<repo>@<repo-id>:ref:refs/heads/main` (not on GitHub Enterprise Server).
Older repositories keep `repo:<org>/<repo>:…`. Write the trust policy for the format the
repository actually emits; the cutover date is in
[references/oidc-claims.md](references/oidc-claims.md).

### GitLab CI `sub`

Default format: `project_path:<group>/<project>:ref_type:<branch|tag>:ref:<name>`.

| `sub` value | Who can assume | Verdict |
| --- | --- | --- |
| condition absent | Any job on that GitLab instance | Broken |
| `project_path:<group>/*` (StringLike) | Every project in the group, any ref | Too broad for anything that can write |
| `project_path:<group>/<project>:*` (StringLike) | Every branch and tag of one project, including unprotected branches anyone with Developer access can push | Too broad for anything that can read state |
| `project_path:<group>/<project>:ref_type:branch:ref:main` | Jobs on `main` | Deploy role; keep `main` protected |

- **Issuer and condition keys.** On gitlab.com the keys are `gitlab.com:sub`, `gitlab.com:aud`,
  and AWS also supports `gitlab.com:project_id`, `namespace_id` and `ref_protected`. Add
  `project_id` (stable across renames and transfers) and `ref_protected = "true"` next to `sub`.
  A self-managed or Dedicated instance supports only `<host>:sub` and `<host>:aud`, so `sub`
  carries the whole boundary there.
- A project can customise its `sub` claim through the projects API; if it has, the default
  format above no longer applies.

### Verify the claims before relying on the policy

Claim formats change and can be customised per repository or project. Before trusting a
condition, print the claims from a real token in a throwaway job (decode the JWT payload; do
not log the token itself) and compare `sub` and `aud` character for character. Then test both
directions: the intended job assumes the role, and a job on another branch gets `AccessDenied`.
A condition that never matches fails loudly; one that matches too much is silent.

## Permission boundaries and the other ceilings

A permission boundary is a **ceiling**, not a grant: the role needs an `Allow` in its identity
policy and in its boundary. AWS has four ceilings, and choosing the wrong one is a common
design error:

| Policy | Attached to | Limits | Use it for |
| --- | --- | --- | --- |
| Permission boundary | One IAM user or role | That principal's identity-policy permissions (and resource-policy grants to the role's ARN, but not grants naming a role *session* ARN directly) | Delegating role creation; capping a generated role |
| SCP | An org root, OU or account | Every principal in member accounts, root user included; not the management account, not service-linked roles | Org-wide guardrails: allowed regions, "never disable CloudTrail" |
| RCP | An org root, OU or account | What any principal, including other accounts, can do to resources in member accounts, for the services RCPs support | Data perimeter: "nothing outside the org reads our buckets" |
| Session policy | One assumed-role or federated session, passed at `AssumeRole*` time | That session only | Narrowing a shared role for one job run |

None of these grant anything, and an explicit `Deny` in any of them wins.

### Delegating role creation safely

To let application teams create their own roles without creating an admin, condition the
create and policy-attach actions on your boundary:

```json
{
  "Sid": "CreateRolesOnlyWithBoundary",
  "Effect": "Allow",
  "Action": ["iam:CreateRole", "iam:PutRolePolicy", "iam:AttachRolePolicy", "iam:PutRolePermissionsBoundary"],
  "Resource": "arn:aws:iam::111111111111:role/<team-path>/*",
  "Condition": {
    "StringEquals": {
      "iam:PermissionsBoundary": "arn:aws:iam::111111111111:policy/<boundary-name>"
    }
  }
}
```

That condition alone leaves three escalation paths. Close them in the same policy:

```json
{
  "Sid": "ProtectTheBoundary",
  "Effect": "Deny",
  "Action": [
    "iam:DeleteRolePermissionsBoundary",
    "iam:CreatePolicyVersion",
    "iam:DeletePolicy",
    "iam:DeletePolicyVersion",
    "iam:SetDefaultPolicyVersion"
  ],
  "Resource": [
    "arn:aws:iam::111111111111:role/<team-path>/*",
    "arn:aws:iam::111111111111:policy/<boundary-name>"
  ]
}
```

- **Removing the boundary** from a role (`DeleteRolePermissionsBoundary`) lifts the ceiling.
- **Editing the boundary policy itself** (a new default version) raises the ceiling for every
  role that carries it.
- **Swapping to a different boundary** is covered by conditioning `PutRolePermissionsBoundary`
  on the same `iam:PermissionsBoundary` value, as above.

Also scope `iam:PassRole` to the team's path, or the team can hand an existing, unbounded role
to a service it launches.

### Capping a broad role

A deploy role built from a module you did not write is easier to reason about with a boundary
that forbids IAM writes, regions outside your footprint, and changes to logging or billing.
A boundary sets a maximum; it does not make `Resource: "*"` acceptable, and a reviewer reading
only the identity policy will not see it.

## Reading a policy for the wildcard that matters

Not all wildcards are equal. Some are unavoidable — many `Describe`/`List` actions support
no resource-level permissions, so `Resource: "*"` is the only legal form. Triage in this
order:

| Pattern | Why it is serious |
| --- | --- |
| `"Action": "*"` with `"Resource": "*"` | Administrator, whatever the role is named |
| `"Action": "iam:*"`, or any `iam:Create*` / `iam:Put*` / `iam:Attach*` without a boundary condition | Self-escalation: the role can grant itself anything |
| `"Action": "iam:PassRole"` with `"Resource": "*"` | The role can hand *any* role to a service it can launch, and inherit those permissions indirectly. Always scope `PassRole` to the specific roles, and add an `iam:PassedToService` condition. |
| `"Action": "sts:AssumeRole"` with `"Resource": "*"` | Lateral movement across every trusting role |
| `"Action": "kms:*"` or `kms:Decrypt` on `"Resource": "*"` | Reads every encrypted artifact the account can see, state files included |
| `"Action": "s3:*"` on `"Resource": "*"` | Includes `DeleteObject` and bucket-policy writes, not just the reads someone was thinking of |
| `"Principal": "*"` in a **resource** policy without a tight `Condition` | Grants outside the account entirely — worse than any identity-policy wildcard |
| `"NotAction"` or `"NotResource"` in an `Allow` | Grants everything except a list, so every new AWS service is granted on launch |
| A wildcard in the middle of an ARN: `arn:aws:s3:::<org>-*` | Matches buckets that do not exist yet, including one another account can create with a matching name; add an `s3:ResourceAccount` condition |

Benign, in context: `Resource: "*"` on read-only actions that genuinely have no
resource-level support; `Action: ["s3:GetObject"]` with a wildcard confined to the object
key of one owned bucket; a `Deny` statement with wildcards, which only ever narrows.

The reviewer's question is never "is there a `*`" — that is a grep, and greps are for
detectors. It is: **if this role were fully compromised, what is the largest thing its
holder could do?** Answer that in one sentence. If you cannot, the policy is too broad to
review.

## Verify

Check, rather than assume:

```
aws sts get-caller-identity
aws iam simulate-principal-policy --policy-source-arn <role-arn> --action-names <action> --resource-arns <arn>
aws accessanalyzer list-findings-v2 --analyzer-arn <analyzer-arn>
```

- `get-caller-identity` first: an unexpected account or role explains most "permission"
  errors.
- The policy simulator evaluates identity policies and the permission boundary, and SCPs when
  the account is in an organization (not SCPs that use global condition keys). It does not
  replace a real call for trust policies or resource-based policies.
- Access Analyzer answers what is reachable from outside the account, which reading policies
  will not tell you.
- For a trust policy, the positive and negative test-job runs in the OIDC section are the
  verification.

Without shell access or credentials (web), review the policy JSON or HCL the user pastes, and
list the commands above for them to run instead of reporting the policy as verified.

This skill proposes and reviews. Creating, attaching or deleting a role is a change for the
pipeline, not for this session.
