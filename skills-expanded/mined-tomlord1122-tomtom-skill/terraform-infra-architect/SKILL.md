---
name: terraform-infra-architect
description: Scaffold and evolve multi-environment, multi-stack Terraform repositories with S3 remote state, Makefile automation, and GitHub Actions CI. Use when the user asks to "create a terraform repo", "scaffold infrastructure", "build a new terraform stack", "set up IaC project", "design multi-stack terraform architecture", "help me create EKS infrastructure", or "set up foundation AWS resources with Terraform".
---

# Terraform Infrastructure Architect

Guides users through scaffolding production-ready Terraform repositories by asking
detailed questions about their needs. Follows the layered stack pattern:
**Foundation (aws/) → Platform (service/eks) → Workload (service/<app>)**.

Emphasizes remote state composition, environment isolation via `.tfvars`, Makefile-driven execution,
and GitHub Actions safe delivery.

## Thinking Process

When activated, follow this structured thinking approach. **NEVER assume defaults**.
Always ask the user questions and wait for answers before proceeding.

### Step 1: Project Identity & Scope Discovery (ALWAYS ASK FIRST)

**Goal:** Understand what the user is building before writing a single line of code.

**Key Questions to Ask (ask ALL of these):**

1. **Project name / prefix?**
   - "What is the project or team prefix for resource naming? (e.g., `acme`, `platform`, `data-team`)"
   - This becomes: S3 bucket prefix, resource Name tags, state file paths

2. **Environments?**
   - "Which environments do you need? Common: `int`, `stg`, `prod`. Do you need all three or fewer?"
   - "Or do you have custom environment names?"

3. **Regions per environment?**
   - "Which AWS region for dev/staging? (e.g., `us-west-2`, `eu-central-1`)"
   - "Which AWS region for production? (same or different?)"
   - "Do you need multi-region in a single environment?"

4. **Do you need plumbing/foundation resources?**
   - "Do you need me to create foundation stacks? These are: VPC, Route53 (DNS), Secrets Manager, SNS (alerts)."
   - "Which ones do you already have vs which should I scaffold?"
   - **Critical:** If they already have a VPC, you must not create a new one. Ask for the VPC ID or tell them to use `terraform_remote_state`.

5. **Do you need an EKS (Kubernetes) cluster?**
   - "Do you need a Kubernetes platform? If yes, I will scaffold the EKS stack."
   - "If you already have EKS, tell me the cluster name and OIDC provider URL."

6. **Do you need workload/application stacks?**
   - "After foundation + platform, do you have services that need databases, caches, IAM roles, DNS records?"
   - "What is the service name? (e.g., `api`, `backend`, `analytics`)"

7. **Who is the owner / team?**
   - "What team name should I use for resource tags and ownership?"

8. **Where should I scaffold this?**
   - "What directory path should I create the repository in? (default: current directory)"

**Thinking Framework:**
- "If I don't ask about existing resources, I might create duplicates"
- "Foundation stacks are the city's plumbing -- pipes, power, addresses. Nothing else works without them."
- "Every answer changes the scaffold output. No one-size-fits-all."

**Decision Point:** Do NOT proceed until user has answered at minimum:
- Project prefix
- Environments and regions
- Which stacks they need (VPC? EKS? Service?)
- Whether resources already exist in AWS

**Articulation Template:**
- "I understand you are building `[project]` with environments `[envs]` in regions `[regions]`"
- "You need foundation stacks: `[list]`, platform: `[yes/no]`, workload: `[name or none]`"

### Step 2: Foundation / Plumbing Stack Deep Dive

**Goal:** If user needs foundation resources, ask detailed questions about each.

**Ask about VPC:**
- "What CIDR block should the VPC use? (e.g., `10.0.0.0/24`, `172.16.0.0/20`)"
- "How many availability zones? (2 or 3?)"
- "Do you need public subnets? (for load balancers, bastion hosts)"
- "Do you need dedicated pod networking CIDR for EKS? (e.g., `100.64.0.0/16`)"
- "Do you have a Transit Gateway to connect to? If yes, what is the TGW ID?"
- "Do you need VPC endpoints for S3, DynamoDB, ECR?"

**Ask about Route53:**
- "What is your external domain? (e.g., `int.acme.example.com`)"
- "What is your internal domain? (e.g., `int.acme.internal`)"
- "Or should I use placeholder domains for now?"

**Ask about Secret Manager:**
- "What secrets do you need containers for?"
- "Format: `name = { description, owner, sys }`"
- "Example: database master password, API auth tokens, cache auth tokens"
- "Do you want me to create a dummy example secret to show the pattern?"

**Ask about SNS:**
- "Do you need alarm topics? Standard set: P0, P1, P2, Report, Notification?"
- "Or custom topic names?"

**Thinking Framework:**
```text
Foundation Stack = Plumbing
  VPC     = streets + power grid
  Route53 = address book
  Secrets = safe deposit boxes (empty until you add contents)
  SNS     = fire alarm system
```

**Decision Point:** Confirm:
- "VPC will use CIDR `[X]` across `[N]` AZs in `[region]`"
- "DNS domains will be `[external]` and `[internal]`"
- "Secrets containers: `[list of names]`"
- "SNS topics: `[list of names]`"

### Step 3: EKS Platform Deep Dive (If Requested)

**Goal:** Understand Kubernetes platform requirements in detail.

**Key Questions to Ask:**

1. **Cluster version?**
   - "Which EKS Kubernetes version? (e.g., `1.32`, `1.35`)"

2. **Access model?**
   - "Who needs cluster admin access? (IAM roles, SSO groups)"
   - "Do you use AAD/Entra ID, Okta, or AWS IAM for authentication?"

3. **Node groups -- ask about EACH node group:**
   - "How many node groups do you need?"
   - For each:
     - "Purpose? (e.g., `infra`, `app`, `database`, `gpu`)"
     - "Subnet type? (`public` or `private`)"
     - "Instance type? (e.g., `m6a.xlarge`, `c6a.2xlarge`)"
     - "Desired / min / max capacity?"
     - "Does it need Kubernetes labels? (for pod scheduling)"
     - "Does it need taints? (to prevent unwanted pods from scheduling)"
   
4. **Add-ons:**
   - "Which EKS add-ons do you need?"
   - "Standard: CoreDNS, kube-proxy, VPC CNI, metrics-server. Any others?"

5. **IRSA (IAM Roles for Service Accounts):**
   - "Do you have Kubernetes services that need AWS permissions? (S3, RDS, Bedrock, etc.)"
   - "What service accounts and what AWS permissions do they need?"

6. **Networking:**
   - "Should the EKS API endpoint be public, private, or both?"
   - "Do you need a bastion host or VPN to access private clusters?"

**Thinking Framework:**
```text
EKS Stack = Apartment Building
  Control Plane   = Building management office (AWS-managed)
  Node Groups     = Different apartment wings (CPU-focused, memory-focused, GPU)
  IRSA            = Key cards that only open specific doors
  OIDC Provider   = The key card validation machine
```

**Decision Point:** Confirm node group plan:
```
Node Group: [name]
  - Subnet: [public/private]
  - Instance: [type]
  - Capacity: [desired]/[min]/[max]
  - Labels: [map]
  - Taints: [list or none]
```

### Step 4: Workload / Service Stack Deep Dive (If Requested)

**Goal:** Understand what application infrastructure sits on top of EKS.

**Key Questions to Ask:**

1. **Service identity:**
   - "What is the service name? (used in resource naming and tags)"
   - "Who is the owning team?"

2. **Database:**
   - "Do you need a database? (Aurora PostgreSQL, RDS MySQL, DynamoDB?)"
   - "Instance class for dev? (e.g., `db.t4g.medium`)"
   - "Instance class for prod?"
   - "Do you need read replicas?"
   - "Backup retention? (dev=7 days, prod=30 days?)"

3. **Cache:**
   - "Do you need a cache? (ElastiCache Valkey/Redis, Memcached?)"
   - "Node type? (e.g., `cache.t4g.micro`)"
   - "How many nodes?"

4. **Storage:**
   - "Do you need S3 buckets?"
   - "What access patterns? (read-only, read-write, cross-account?)"

5. **IAM / IRSA:**
   - "What AWS services does your app need to access?"
   - "S3, DynamoDB, Bedrock, Secrets Manager, SQS, SNS?"
   - "What is the Kubernetes namespace and service account name?"

6. **DNS:**
   - "Do you need DNS records for the service? (database endpoint, API endpoint)"

7. **Alarms:**
   - "Do you need CloudWatch alarms? (CPU, memory, disk, connection count)"
   - "Which SNS topics should they publish to?"

**Thinking Framework:**
```text
Workload Stack = Apartment Furniture
  RDS/Cache  = Furniture inside the apartment
  IAM/IRSA   = Who can use which appliance
  DNS        = Address label on your door
  Alarms     = Smoke detector inside your unit
```

**Decision Point:** Confirm service infrastructure bundle:
- "Service `[name]` will have: `[DB yes/no]`, `[Cache yes/no]`, `[S3 yes/no]`, `[IRSA yes/no]`"
- "It will consume remote state from: `[list of foundation stacks]`"

### Step 5: Repository Structure Design

**Goal:** Define the directory layout based on answers from Steps 1-4.

**Actions:**
1. Create `terraform/deployments/aws/` and `terraform/deployments/service/`
2. Create matching `terraform/config/aws/` and `terraform/config/service/`
3. Create `.github/workflows/`

**Thinking Framework:**
```text
{project}/
├── terraform/
│   ├── makefile              # Human-friendly execution
│   ├── deployments/
│   │   ├── aws/{stack}/      # Foundation blueprints
│   │   └── service/{stack}/  # Platform + workload blueprints
│   └── config/
│       ├── aws/{stack}/      # Site-specific values (CIDRs, domains)
│       └── service/{stack}/  # Site-specific values (instance sizes, counts)
├── .github/workflows/        # Safe CI/CD delivery
└── README.md
```

**Decision Point:** Show user the planned directory tree and get confirmation.

### Step 6: Scaffold & Generate

**Goal:** Run the scaffold script with the user's specific answers.

**Actions:**
1. Call `scripts/scaffold-repo.sh` with the collected parameters
2. After generation, read the key generated files to verify correctness
3. Show the user the generated structure

**Decision Point:** Confirm the script output:
- Correct number of stacks created
- Correct project prefix applied
- Correct environments/regions reflected

### Step 7: Validate & Handoff

**Goal:** Ensure the user knows what to do next.

**Actions:**
1. Show the exact apply order (foundation first, then platform, then workload)
2. Remind about prerequisites:
   - S3 backend buckets must exist before first apply
   - AWS credentials must be configured
   - GitHub OIDC trust policy must be set up for CI
3. Explain the `config/` vs `deployments/` separation one more time
4. Offer to generate a TUTORIAL.md walkthrough if they want

**Critical Safety Reminders (ALWAYS SAY THESE):**
- "Never run `make tf_apply` without running `make tf_plan` first"
- "Never commit real secret values to `.tfvars` files"
- "Always apply foundation stacks before service stacks"
- "Check the plan output carefully for unexpected `destroy` or `replace` actions"

**Decision Point:** User can answer:
- "Which stack do I apply first and why?"
- "Where do I put environment-specific values?"
- "How do I run a plan?"
- "What do I need to create in AWS before the first terraform apply?"

## Usage

```bash
# Scaffold a complete terraform infra repo
bash /mnt/skills/user/terraform-infra-architect/scripts/scaffold-repo.sh [options]
```

**Arguments:**
- `--project-name` - Project prefix for resource naming (required)
- `--environments` - Comma-separated envs (default: `int,stg,prod`)
- `--main-region` - Primary region for dev/staging (default: `us-west-2`)
- `--prod-region` - Production region (default: `ap-south-1`)
- `--stacks` - Comma-separated foundation stack list (default: `vpc,route53,secret-manager,sns`)
- `--with-eks` - Include EKS platform stack (flag)
- `--with-service` - Include a sample workload stack (flag)
- `--service-name` - Name of the workload service (default: `app`)

**Examples:**

```bash
# Minimal foundation-only repo
bash /mnt/skills/user/terraform-infra-architect/scripts/scaffold-repo.sh \
  --project-name acme \
  --environments int,stg,prod \
  --stacks vpc,route53

# Full platform + workload repo
bash /mnt/skills/user/terraform-infra-architect/scripts/scaffold-repo.sh \
  --project-name acme \
  --environments int,stg,prod \
  --with-eks \
  --with-service \
  --service-name api
```

## Output

The script creates the following structure:

```text
{project}-infra/
├── terraform/
│   ├── makefile
│   ├── deployments/
│   │   ├── aws/vpc/
│   │   ├── aws/route53/
│   │   ├── aws/secret-manager/
│   │   ├── aws/sns/
│   │   ├── service/eks/        # if --with-eks
│   │   └── service/{app}/      # if --with-service
│   └── config/
│       ├── aws/vpc/
│       ├── aws/route53/
│       ├── aws/secret-manager/
│       ├── aws/sns/
│       ├── service/eks/        # if --with-eks
│       └── service/{app}/      # if --with-service
├── .github/workflows/
│   ├── plan.yaml
│   ├── apply.yaml
│   └── parameter_check.yaml
└── README.md
```

## Present Results to User

When presenting a scaffolded repo, use this format:

```
Scaffolded: {project-name}-infrastructure

Foundation Stacks (Plumbing):
- vpc             (network: CIDR [X], [N] AZs, [public/private] subnets)
- route53         (DNS: [external_domain], [internal_domain])
- secret-manager  ([N] secret containers: [list names])
- sns             (topics: [list names])

Platform Stacks:
- eks             (Kubernetes [version], [N] node groups)
  Node Groups:
  - [name1]: [instance] x[desired] in [subnet]
  - [name2]: [instance] x[desired] in [subnet]

Workload Stacks:
- {app}           ([DB yes/no], [Cache yes/no], [IRSA yes/no])

Apply Order (CRITICAL - never skip):
1. make tf_apply ENV=int AWS_REGION=[region] MODULE_TYPE=aws COMPONENT=vpc
2. make tf_apply ENV=int AWS_REGION=[region] MODULE_TYPE=aws COMPONENT=route53
3. make tf_apply ENV=int AWS_REGION=[region] MODULE_TYPE=aws COMPONENT=secret-manager
4. make tf_apply ENV=int AWS_REGION=[region] MODULE_TYPE=aws COMPONENT=sns
5. make tf_apply ENV=int AWS_REGION=[region] MODULE_TYPE=service COMPONENT=eks
6. make tf_apply ENV=int AWS_REGION=[region] MODULE_TYPE=service COMPONENT={app}

Pre-Requisites Before First Apply:
1. Create S3 buckets: {prefix}-int-{region}-tf-backend
2. Configure AWS credentials: aws configure or env vars
3. (For CI) Set up GitHub OIDC trust policy in AWS IAM
4. (For secrets) Update dummy secret values after secret-manager apply

Next Steps:
1. Review all .tfvars files in terraform/config/
2. Run terraform fmt to standardize formatting
3. Run make tf_plan on the VPC stack first
4. Inspect the plan output before applying
```

## Troubleshooting

**Error: `No valid credential sources found for AWS Provider`**
- Ensure `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` are exported, or use `aws configure`

**Error: `Backend bucket does not exist`**
- The S3 backend bucket must be created manually first
- Bucket naming: `{prefix}-{env}-{region}-tf-backend`
- Example: `acme-int-us-west-2-tf-backend`

**Error: `terraform_remote_state` read fails**
- The upstream stack (e.g., VPC) must be applied first so its state file exists in S3
- Verify the `key` path in `data-sources.tf` matches the actual state file path
- Example: `int/us-west-2/aws/vpc/terraform.tfstate`

**Error: `Error acquiring the state lock`**
- Another process is holding the state lock
- Use `make tf_force_unlock ENV=... AWS_REGION=... MODULE_TYPE=... COMPONENT=... ID=<lock-id>`
- Or wait for the other process to finish

**Security Warning: Never commit `.tfvars` with secrets**
- Secret Manager stack creates containers only; values should be injected via CI workflow or AWS Console
- Always use `git status` to double-check what you are committing
