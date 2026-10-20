---
name: infra-aws
description: >
  AWS for AI platforms — acting through a least-privilege IAM role, across the six surfaces a
  platform uses. Carries: the role model (project-prefixed ARNs, read-heavy defaults, explicit
  denies on deletion and all IAM mutation), credential hygiene (SSO/profiles — keys never in the
  repo or transcript), **workload identity so no static access key exists** (EKS Pod Identity/IRSA,
  task vs execution roles, GitHub OIDC with the trust policy scoped to repo AND branch), EKS
  (private endpoint, IMDSv2, GPU node groups), serverless (Lambda's 15-minute ceiling, Fargate),
  managed databases (RDS/Aurora/DynamoDB — private subnets, IAM auth), CodePipeline + ECR, Bedrock
  (data terms, model pinning, per-region quota), plus S3 plumbing (DVC remotes, versioning,
  lifecycle), Redshift access, and cost awareness. Load when provisioning or touching AWS, or when
  `aws` isn't installed yet. Triggers: AWS, S3, bucket, boto3, aws cli, IAM, role, IRSA, Pod
  Identity, EKS, Lambda, Fargate, ECS, RDS, Aurora, DynamoDB, Bedrock, ECR, CodePipeline, Redshift,
  presigned URL, DVC remote s3, aws profile, SSO, sts get-caller-identity, OIDC federation, IMDSv2,
  set up the role, connect to AWS.
---

# infra-aws — AWS through a role that can't hurt you much

**Pinned:** awscli, boto3 — unpinned · authored 2026-07-18 · run `/skill-update infra-aws` once
the deps are installed (`uv add boto3`; the CLI installs system-side)
**Verified:** 2026-07-25 — Lambda's 900s/15-minute maximum and the EKS Pod Identity vs IRSA
guidance confirmed against AWS documentation. Bedrock quota and data-handling specifics are
region- and account-dependent: **confirm those for your own account rather than relying on this
file.**

> On-demand: load this when the project's infrastructure is AWS. The **boundary is the IAM
> policy, not this skill's judgment** — same philosophy as the repo's security model (hooks are
> guardrails; permissions are the boundary), extended to the cloud. Credential *policy* lives in the
> security canon (`governance` → `security.md` `S8`); warehouse query discipline is `sql`.
> **SageMaker remains out of scope** — it is a large surface with its own opinions, and nothing here
> needs it yet; use `serving` + `kubernetes` instead, or open it as a decision when a project does.
>
> **Neighbours:** provisioning AWS resources declaratively is `iac-terraform` (do not click in the
> console — a resource created by hand is drift by definition). Workload access to AWS APIs should
> use **IRSA / EKS Pod Identity**, not stored keys — that's `authn-authz` `I3`, and it is the
> preferred answer whenever a pod needs S3 or Redshift. EKS cluster configuration and workloads are
> `kubernetes`; secret storage in Secrets Manager/SSM is `secrets-management`; CI reaching AWS uses
> **OIDC federation, never a stored access key** (`supply-chain.md` `C6`).

## The role model — set up once, by the human
Claude acts through a dedicated **`claude-for-ai-platforms`** IAM identity whose policy is the
blast radius. Starter policy: `.claude/templates/aws-iam-policy.json` — copy it, replace
`PROJECT-PREFIX` (S3 bucket prefix), `ACCOUNT-ID`, `REGION`, `CLUSTER-NAME`, `DB-NAME`, and `DB-USER`, review it
yourself, then attach it. Its shape, which the human should verify survives their edits:
- **Project-prefixed ARNs only** — `arn:aws:s3:::PROJECT-PREFIX-*`; the role cannot see other
  buckets' contents.
- **Explicit `Deny` on the catastrophic tier** — `s3:DeleteBucket`, `redshift:DeleteCluster`,
  and **all `iam:*`** (the role must never be able to widen itself). Deny beats any Allow,
  including ones added later by mistake.
- Turn **CloudTrail on** for the account and enable **S3 versioning** on project buckets —
  auditability and undo are part of least privilege.
- Prefer an assumable **role** (SSO / `aws configure sso`) over long-lived user keys; either
  way the credentials live in `~/.aws/` or the environment — **never** in the repo, `.env`
  included (`.env` holds app config; AWS credentials have their own store).

Sanity check before any work: `aws sts get-caller-identity` — confirm you are the scoped role,
not someone's admin profile.

**Every bucket/cluster provisioned gets a row in the resource matrix**
(`.claude/memory/process/resources.md`) + its env keys in `.env.example`, same commit — the
matrix is how the rest of the stack knows where everything is accessed and where each
credential lives (by reference).

## First-time setup — the walkthrough (agent and human each have a part)
Run this top to bottom when AWS work starts on a fresh box. Steps are split deliberately:
the agent does the mechanical parts; the human does everything that touches admin power or a
secret.

**1. CLI present?** `command -v aws || aws --version`. If missing, two install paths:
- **Agent-runnable, no sudo:** download the official v2 bundle and install user-local —
  `curl -o /tmp/awscliv2.zip "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip"`,
  `unzip`, then `./aws/install -i ~/.local/aws-cli -b ~/.local/bin` (ensure `~/.local/bin` is
  on PATH). Never pipe the download into a shell (the bash hook blocks it anyway); the
  system-wide install needs sudo, which this agent deliberately cannot run — that variant is
  the human's, via the `!` prefix in their prompt.
- `uv add boto3` for the Python side (per `env-uv`; it shares the CLI's credential chain).

**2. Authenticate — on the human's side, always.** Access keys and SSO logins must never pass
through the chat (a pasted secret lives in the transcript forever — security canon). Ask the
user to run, in their own terminal or via the `!` prefix:
- **Preferred:** `aws configure sso` (short-lived credentials; needs the org's SSO start URL),
  then `aws sso login --profile <profile>` when sessions expire.
- **Fallback:** `aws configure --profile claude-ds` with an access key **they** created for the
  scoped identity (console → IAM → the user → security credentials). The agent's job is to say
  *which identity* the key must belong to — never to receive the key.
Set the project to the profile via config/env (`AWS_PROFILE=claude-ds` in `.env` is fine —
it's a *name*, not a secret).

**3. Create the identity + attach the policy — human, with their admin profile.** The agent
prepares; the human executes (the agent's own role has `iam:*` denied, and the hook asks on
any `aws iam` mutation — both by design). Prepare for them: the filled-in policy JSON (from
the template, placeholders replaced), and this sequence —
```bash
aws iam create-policy --policy-name claude-for-ai-platforms \
    --policy-document file://aws-iam-policy.filled.json
aws iam create-user --user-name claude-for-ai-platforms        # or create-role + trust policy for SSO/assume
aws iam attach-user-policy --user-name claude-for-ai-platforms \
    --policy-arn arn:aws:iam::ACCOUNT-ID:policy/claude-for-ai-platforms
```
Console clicking works identically (IAM → Policies → Create from JSON → attach). Either way,
**the human reads the policy before attaching** — the review is the point, not a formality.

**4. Verify the boundary, both directions.** As the new profile:
`aws sts get-caller-identity` (the scoped identity, not admin) ·
`aws s3 ls s3://PROJECT-PREFIX-data` (allowed path works) · and one **expected failure**, e.g.
`aws iam list-users` — it must be denied. A boundary you never saw refuse anything is a
boundary you haven't tested.

## S3 — the project's durable data layer
- **Bucket convention:** `PROJECT-PREFIX-data` (raw + processed, versioned, lifecycle to IA/
  Glacier for old raw), `PROJECT-PREFIX-artifacts` (checkpoints, exports — the DVC remote).
- **DVC remote:** `dvc remote add -d storage s3://PROJECT-PREFIX-artifacts/dvc` — then the
  existing `data-dvc` flow (push/pull, pin-to-commit) works unchanged; boto3/awscli creds are
  picked up automatically.
- **Moving data:** `aws s3 sync` (idempotent, resumable) over `cp` for trees; `--dryrun` first
  when the direction is `local → bucket` onto existing keys. Presigned URLs
  (`aws s3 presign`, expiry short) to hand a file to someone — never make a bucket public.
- **Raw immutability in the cloud:** versioning on + a lifecycle rule, and the deny on
  `DeleteBucket`; recursive `aws s3 rm` is confirm-gated by the bash hook.

## Redshift — the warehouse door (the queries themselves are `sql`)
- **Access:** the Data API (`aws redshift-data execute-statement` / boto3
  `redshift-data`) — no long-lived connections or passwords in code; auth rides the IAM role.
- **Bulk in/out goes through S3, always:** `UNLOAD ('SELECT ...') TO 's3://PROJECT-PREFIX-...'`
  for extracts (then the snapshot-what-training-eats rule from `sql` applies to the landed
  files), `COPY` from S3 for loads. Row-by-row inserts and `SELECT *` over the wire are the
  anti-pattern at warehouse scale.
- Training extracts landed from UNLOAD get versioned (`data-dvc`) and recorded in the dataset
  manifest with the query file + extract time.

## The platform surfaces — EKS, serverless, managed DBs, native CI/CD, Bedrock

Beyond S3 + Redshift, these are the five surfaces an AI platform on AWS actually uses. Each is
treated the same way as everything above: the boundary is the IAM policy, and the identity is
short-lived.

### Workload identity — the rule that removes the keys (`I3`)

**No static access keys for workloads. Ever.** The mechanisms, in order of preference:

| Workload | Mechanism |
|---|---|
| Pod on EKS (EC2 nodes) | **EKS Pod Identity** — the current default for new clusters. No OIDC provider to wire, roles reuse across clusters without editing trust policies, and session tags come free |
| Pod on **Fargate**, Windows nodes, or EKS Anywhere | **IRSA** — Pod Identity does not cover these, so IRSA remains the answer rather than the legacy option |
| Lambda / ECS task | The function's or task's **execution role** |
| EC2 | **Instance profile** |
| GitHub Actions → AWS | **OIDC federation** — scope the trust policy to the repo **and the branch** |

```bash
aws sts get-caller-identity        # S8 — the wrong identity means stop
aws eks describe-cluster --name CLUSTER --query cluster.identity.oidc.issuer
```

The trust-policy condition is the part that gets written too loosely:

```json
"Condition": {
  "StringEquals": {"token.actions.githubusercontent.com:aud": "sts.amazonaws.com"},
  "StringLike":   {"token.actions.githubusercontent.com:sub": "repo:ORG/REPO:ref:refs/heads/main"}
}
```
A `sub` of `repo:ORG/REPO:*` trusts **any** branch — including one a contributor pushed. That is the
difference between OIDC federation and a shared credential with extra steps.

### EKS

- **Pod Identity on EC2 node groups, IRSA on Fargate** (above), and
  `automountServiceAccountToken: false` for pods that don't call the Kubernetes API (`P6`). The two
  coexist, so a migration is incremental rather than a cutover.
- **Private API endpoint** with public access restricted to known CIDRs.
- **Managed node groups** with a launch template enforcing IMDSv2 and hop limit 1 — IMDSv1 lets any
  pod that can reach the metadata endpoint assume the *node's* role, which is a well-worn escalation
  path.
- **GPU node groups** with taints plus the NVIDIA device plugin; separate from general workloads.
- **Security groups for pods** where you need per-pod network policy at the VPC layer, alongside
  Kubernetes NetworkPolicy (`P5`).
- What AWS owns vs you → record it in `memory/process/control-coverage.md` (`P8`). On EKS the
  control plane is theirs; the nodes, the CNI configuration, and everything in §5 of the CIS
  Kubernetes Benchmark are yours.

### Serverless

- **Lambda:** a 15-minute maximum timeout, which a long generation can exceed — use a queue
  (`caching-and-queues`) or Step Functions rather than fighting it. Cold start plus model load makes
  Lambda a poor fit for inference; it is a good fit for the glue around it. One execution role per
  function, least-privilege. Enable **SnapStart** where the runtime supports it.
- **ECS on Fargate:** the better fit for containerised inference that doesn't need Kubernetes.
  Task role (what the app uses) and execution role (what pulls the image) are **different roles** —
  conflating them is a common over-grant.
- **Step Functions** for orchestration inside AWS; see `workflow-orchestration` before adding it
  alongside another engine.

### Managed databases

| Service | For |
|---|---|
| **RDS PostgreSQL / Aurora** | Default OLTP. Supports `pgvector` (`vector-stores`) |
| **DynamoDB** | Key-value at scale. Design around the access pattern; it is not a relational store |
| **ElastiCache** | Redis (`caching-and-queues`) |
| **OpenSearch** | Search + vector, if you already run it |

Non-negotiables (`P11`, `D9`): **private subnets, `publicly_accessible = false`** — `guard-iac.py`
blocks the manifest that sets it true; security group scoped to the app's SG, never `0.0.0.0/0` on
5432; **IAM database authentication** rather than a stored password where supported; encryption at
rest with a CMK; automated backups with **a tested restore** (`D10`).

### CodePipeline / CodeBuild

Held to the same bar as `secure-cicd`: a least-privilege service role **per pipeline**, no long-lived
credentials inside builds, untrusted-contributor builds receive no secrets (`CICD-SEC-4`), and
artifacts signed and verified between stages (`C3`). **ECR** with scan-on-push, immutable tags, and a
lifecycle policy so old images expire.

### Bedrock

- **Data handling:** prompts and completions are not used to train the base models, but confirm the
  current terms and your region's data-residency guarantees rather than assuming — sending a prompt
  is egress (`S7`), and the answer belongs in the record.
- **Pin the model id including its version** (`M14`). Model deprecations are announced on a schedule;
  track them.
- **VPC endpoints** so traffic doesn't traverse the public internet, and **Guardrails** as a
  `guardrails`-layer control — not a substitute for your own.
- **Quotas are per-region, per-model, in tokens per minute** — an availability constraint as much as
  a cost one. Handle throttling with backoff (`R4`) and plan a fallback (`R5`).

## Cost awareness (cost bugs are silent like leakage bugs)
Know the pricing dimension before running: S3 = storage + requests + **egress** (a `sync` down
of a TB is a bill), Redshift = cluster-hours (or RPU-hours serverless) — don't leave clusters
running for a weekly query; lifecycle rules are the cheapest habit. Anything projected to cost
real money is a decision for the user, stated in dollars, before the command — and new
recurring costs get a decision-log line.

## Gotchas
- **Region mismatch** is the classic silent failure — bucket and cluster region pinned in
  config (`${oc.env:AWS_REGION}` via the config system), not defaulted per-shell.
- The hook confirm-gates `aws s3 rb`, recursive `s3 rm`, `redshift delete-*`, and any
  `aws iam` mutation — if the dialog surprises you, stop and re-read what you were about to do.
- boto3 pagination: list operations truncate at 1,000 — use paginators, or counts lie.
