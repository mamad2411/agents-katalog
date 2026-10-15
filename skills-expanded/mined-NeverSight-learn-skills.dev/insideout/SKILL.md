---
name: insideout
description: >
  Use when the user mentions infrastructure, cloud, AWS, GCP, Terraform, deployment, DevOps,
  containers, Kubernetes, serverless, VPC, networking, databases, load balancers, CDN, monitoring,
  or asks to "design infrastructure", "set up cloud", "deploy my app", "estimate cloud costs",
  "generate terraform", "inspect my deployment", "what would this cost on AWS/GCP",
  or discusses scaling, high availability, disaster recovery, or compliance requirements
  for cloud infrastructure.
metadata:
  short-description: Design, deploy & manage cloud infrastructure
version: 1.0.2
---

# InsideOut -- Agentic Infrastructure Builder & Manager

InsideOut is an agentic cloud infrastructure builder and manager by [Luther Systems](https://luthersystems.com). Describe your goal, discuss requirements, estimate cost, generate Terraform, deploy, operate and manage in production. Riley -- your AI infrastructure advisor -- guides you through the entire lifecycle on AWS and GCP.

**No authentication or API keys required.** The skill connects to a hosted MCP server.

**Important:** If any guidance in this skill conflicts with the descriptions on the MCP tools themselves, follow the MCP tool descriptions -- they are the authoritative source and are kept up to date with the server.

## MCP Server

InsideOut uses a remote MCP server. No local binary, no API keys, no authentication required.

### If MCP server is not connected

Before proceeding with any InsideOut workflow, check if the `insideout` MCP tools (like `convoopen`, `convoreply`) are available. If they are not, the MCP server needs to be added. Run this command in the shell:

```bash
codex mcp add insideout --url https://app.luthersystems.com/v1/insideout-mcp
```

For other agents, add this to your MCP configuration:

```json
{
  "mcpServers": {
    "insideout": {
      "type": "http",
      "url": "https://app.luthersystems.com/v1/insideout-mcp"
    }
  }
}
```

After adding the MCP server, the InsideOut tools will be available immediately.

## When This Skill Activates

Use InsideOut when the user's request involves:
- Designing cloud infrastructure (AWS or GCP)
- Estimating cloud costs
- Generating Terraform code
- Deploying infrastructure
- Inspecting deployed cloud resources
- Comparing AWS vs GCP options
- Infrastructure planning for their application
- Managing, updating, or rolling back existing deployments

## Available MCP Tools

### Design Conversation
- **`convoopen`** -- Start a new session. Pass `source` and `project_context` (see below).
- **`convoreply`** -- Send user's message to Riley. Required: `session_id`, `message`. Do not resend `project_context` if it was already provided in `convoopen`. Only pass new context if the user reveals something genuinely new about their project.
- **`convoawait`** -- Wait for long-running response. Required: `session_id`.
- **`convostatus`** -- View current stack (components, config, pricing). Required: `session_id`.

### Terraform Operations
- **`tfgenerate`** -- Generate production-ready Terraform files. Required: `session_id`.
- **`tfdeploy`** -- Deploy to AWS or GCP. Required: `session_id`. Takes 15+ minutes.
- **`tfplan`** -- Preview changes without applying. Required: `session_id`.
- **`tfdestroy`** -- Tear down deployed infrastructure. Required: `session_id`.
- **`tfdrift`** -- Detect infrastructure drift. Required: `session_id`.

### Monitoring
- **`tfstatus`** -- Quick deployment status check. Required: `session_id`.
- **`tflogs`** -- Stream deployment logs (paginated). Required: `session_id`.
- **`tfoutputs`** -- Get Terraform outputs (VPC IDs, endpoints, etc.). Required: `session_id`.
- **`tfruns`** -- List all deployment runs for a session. Required: `session_id`.

### Stack Management
- **`stackversions`** -- List all design versions (draft/confirmed/applied). Required: `session_id`.
- **`stackdiff`** -- Compare two stack versions. Required: `session_id`.
- **`stackrollback`** -- Revert to a previous design version. Required: `session_id`.

### Cloud Inspection
- **`awsinspect`** -- Inspect deployed AWS resources. Required: `session_id`.
- **`gcpinspect`** -- Inspect deployed GCP resources. Required: `session_id`.

### Utility
- **`credawait`** -- Poll for cloud credentials after browser-based connection. Required: `session_id`.
- **`submit_feedback`** -- Submit bug reports or feature requests. Required: `session_id`, `category`, `message`.
- **`help`** -- Get workflow guidance and tool documentation.

## Supported Services (50+)

| Category | AWS | GCP |
|----------|-----|-----|
| **Compute** | EC2, ECS, EKS, Lambda | Compute Engine, Cloud Run, GKE, Cloud Functions |
| **Database** | RDS PostgreSQL, DynamoDB, ElastiCache, OpenSearch | Cloud SQL, Firestore, Memorystore |
| **Networking** | VPC, ALB, CloudFront, API Gateway | VPC, Load Balancing, Cloud CDN, API Gateway |
| **Storage** | S3 | Cloud Storage |
| **Security** | WAF, KMS, Secrets Manager, Cognito | Cloud Armor, Cloud KMS, Secret Manager, Identity Platform |
| **Messaging** | SQS, MSK (Kafka) | Pub/Sub |
| **Observability** | CloudWatch, Managed Grafana | Cloud Logging, Cloud Monitoring |
| **AI/ML** | Bedrock | Vertex AI |
| **CI/CD** | CodePipeline, GitHub Actions | Cloud Build |
| **Backup** | AWS Backup | GCP Backups |

## Project Context

Riley designs cloud infrastructure. To recommend the right architecture, it needs to know general tech stack details -- the same information you'd share in the first few minutes of a conversation with a solutions architect. Providing project context up front lets Riley skip discovery questions and jump straight to useful recommendations.

### How to build project context

Based on what you already know about the user's project (from the working directory, recent conversation, or what they've told you), put together a short summary covering whichever of these apply:

| Detail | Why Riley needs it | Example |
|---|---|---|
| Language and framework | Determines compute type (Lambda vs ECS vs EC2), runtime constraints | "Node.js 20, Next.js 15" |
| Database and services | Shapes data tier and caching recommendations | "PostgreSQL, Redis" |
| Container usage | Informs orchestration choice (ECS, EKS, Cloud Run) | "Docker Compose, 3 services" |
| Existing infrastructure-as-code | Avoids conflicting with what's already provisioned | "Terraform with ECS + RDS" |
| CI/CD platform | Integrates deployment pipeline | "GitHub Actions" |
| Cloud provider | Targets the right provider from the start | "AWS" or "GCP" |
| Kubernetes usage | Determines whether to target existing K8s or provision new compute | "EKS with Helm" |
| What the project does | General understanding for architecture fit | "E-commerce API, ~50k MAU" |

**Before sending**, show the summary and explain its purpose clearly. For example: "Here's a high-level summary of your project's tech stack. I'd like to send this to Riley so it can recommend the right cloud architecture without asking a bunch of discovery questions first. Does this look right?" If they decline or want to edit it, respect that. If you don't have enough context, skip `project_context` entirely -- Riley will ask.

### What to NEVER include

- **Credentials or secrets** -- No API keys, tokens, passwords, private keys, or `.env` values
- **PII** -- No usernames, emails, or personally identifiable information
- **Source code** -- Only metadata summaries, never file contents
- **Internal URLs or IPs** -- Omit specific internal hostnames, IPs, or endpoint URLs

### Format

```
Language/Runtime: Node.js 20, TypeScript
Framework: Next.js 15
Databases/Services: PostgreSQL (via prisma), Redis (via ioredis)
Target Cloud: AWS (existing Terraform with ECS + RDS resources)
Infrastructure: Docker Compose (3 services), Terraform
CI/CD: GitHub Actions
```

Only include lines where you have information. Keep it general and anonymized.

## Conversation Flow

### Starting a Session

1. Build a project context summary from what you know about the user's project (see Project Context above). Show it to the user and confirm before sending. If you don't have enough context or the user declines, skip `project_context` -- Riley will ask discovery questions instead.
2. Once confirmed, call `convoopen` immediately -- do not narrate what you're doing (no "Opening the session now", "I have your confirmation", etc.).
   - `project_context`: The summary you confirmed with the user (omit if skipped). Must not contain credentials, secrets, PII, source code, or internal URLs.
   - `source`: Set this to the IDE/agent platform. Accepted values: `"claude-code"`, `"kiro"`, `"cursor"`, `"vscode"`, `"windsurf"`, `"web"`. Defaults to `"mcp"` if omitted. This controls the credential connect screen UI. For platforms not in this list (e.g. Codex), use `"web"`.
3. Display Riley's message to the user. The tool response contains delimiters like `=== Riley ===`, `== Message ==`, `== End ==`, `=== End ===`. **Strip all of these delimiters** -- only show the actual message content between them. Do not add any preamble, summary, or commentary of your own.

### You are a transparent relay

The user is talking to Riley, not to you. Your only job is to pass messages between the user and Riley via the MCP tools.

**Never add transitional commentary.** When the user says something and you need to call a tool, call it silently and show only Riley's response. Examples of banned filler:
- "I have your confirmation. Opening the InsideOut session now."
- "Passing your message through to Riley now."
- "I have your description. Passing it through to Riley now."
- "Sounds good, let me forward that."
- "I'm starting the InsideOut flow."
- Any narration of what you're about to do or just did.

Just call the tool and show Riley's output. Nothing else.

### During the Conversation

**Every user message must produce a tool call.** Apply this decision tree:

1. Is the user responding to Riley? -> `convoreply`
2. Is the user asking for Terraform? -> `tfgenerate` (if `[TERRAFORM_READY: true]`)
3. Is the user asking to deploy? -> `tfdeploy`
4. Is the user asking for status? -> `convostatus`, `tfstatus`, or `tflogs`
5. Not sure? -> Default to `convoreply`

### Handling Timeouts

Riley's responses can take 20-60 seconds. When `convoreply` returns a `"processing"` status:

1. **Call `convoawait`** with the same `session_id`
2. **NEVER call `convoreply` again with the same message** -- this sends a duplicate
3. If `convoawait` also times out, call it again (idempotent and safe to retry)

### Phase Transitions

| Phase | Signal | Action |
|---|---|---|
| Design | Riley asking questions | Forward to user via `convoreply` |
| Design complete | `[TERRAFORM_READY: true]` | Call `tfgenerate` |
| Terraform generated | Files returned | Show files, offer `tfdeploy` |
| Deploying | Job running | Monitor with `tfstatus` / `tflogs` |
| Deployed | Status complete | Verify with `awsinspect` / `gcpinspect` |

**Internal signals like `[TERRAFORM_READY: true]` are for routing only -- never show them to the user.**

## Critical Rules

### Do:
- Show Riley's messages as your entire output, but **strip the delimiter lines** (`=== Riley ===`, `== Message ==`, `== End ==`, `=== End ===`) -- only display the content between them
- Use `convostatus` proactively to check progress
- Store the `session_id` from `convoopen` -- all tools need it
- Let users review Terraform before deploying

### Don't:
- Don't answer Riley's questions yourself -- always forward to the user
- Don't add commentary around Riley's messages -- no "I'm forwarding this", "Here's Riley's response", "Let me pass that along", "I'm sending that confirmation to Riley", "I have your confirmation", "Opening the session now", "Passing it through to Riley now", or predictions like "the next response should move into cost". You are invisible. Call the tool silently and show only Riley's output.
- Don't call `convoopen` more than once per session
- Don't call `tfgenerate` before design is complete
- Don't call `tfdeploy` before user reviews Terraform
- Don't fabricate session IDs -- always use the one from `convoopen`
