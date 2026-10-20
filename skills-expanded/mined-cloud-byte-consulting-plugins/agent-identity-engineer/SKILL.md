---
name: agent-identity-engineer
description: >-
  Engineer identity, credentials, and authorization for AI-agent principals
  on Kubernetes and cloud platforms using workload identity, projected tokens,
  OIDC, SPIFFE/SPIRE, OAuth2 client credentials, and short-lived scoped access.
  Use for agent or non-human identity, service accounts, API keys versus
  OAuth2, secret sprawl, mTLS, JWT claims, confused deputies, over-permissive
  roles, zero trust, JIT automation, attribution, or unified audit policy.
---

# Agent Identity Engineer

## Purpose
Make every agent action attributable, scoped, and revocable — the prerequisite for any autonomy at all. An org cannot score past ASDLC Level 2 with unmeasurable agent attribution (per the sibling `asdlc-maturity-assessment` skill, platform-assessment plugin), and it cannot safely expose MCP tools (`mcp-platform-api-author`) or agent APIs (`agent-api-contract-designer`) to principals it can't name. This skill designs the identity substrate: ephemeral credentials rooted in real identity, machine authorization that neither over-permissions nor strangles automation, and one policy/audit plane for humans and machines.

## Core model to hold in your head

### The four pillars of access
Every access — human or agent — decomposes into **connectivity, authentication, authorization, audit**. Design and evaluate all four for agent principals; orgs habitually solve authn for machines and skip the other three. The end-state is a single source of truth defining policy for all four pillars across every protocol and resource — not one stack for humans (SSO, MFA, session recording) and a shadow stack for machines (static tokens, wildcard roles, no audit). The perimeter died a long time ago; identity is the control plane.

### No standing secrets
A secret (API key, static token, shared password) is authentication by *possession of a string* — copyable, leakable, phishable, and unattributable. The thesis: **secrets are a vulnerability class to be eliminated, not managed better.** Replace with true identity: credentials issued per-use, cryptographically bound to an attested identity, expiring in minutes-to-hours.
- Vault-style dynamic secrets and rotation are a transitional improvement (short-lived DB creds beat static ones), but the destination is certificate/token issuance from identity, not distribution of strings.
- Platform rule inherited from the reference architecture: secret *retrieval and injection* at runtime — never distribution into configs, repos, or agent prompts.
- An API key pasted into an agent's context window is the modern password-on-a-sticky-note — and agents echo their context into logs, PRs, and chats.

### Ephemeral identity and the DIE triad
Modern infrastructure follows **DIE — Distributed, Immutable, Ephemeral** — and identity must match: ephemeral workloads need ephemeral identities. A compromised short-lived credential self-expires; rotation is replaced by reissuance. The catch: ephemeral identities still need a **root of trust** to derive from — a hardware root (TPM/HSM/cloud attestation) or a platform root (the K8s API server attesting a pod). An ephemeral credential not chained to an attested root is just a fast-rotating secret.

Concrete K8s stack for agent principals:

| Layer | Mechanism | Notes |
|---|---|---|
| Workload identity | **K8s ServiceAccount + projected (bound) tokens** | Audience-bound, time-bound (TTL in minutes, not hours), pod-bound JWTs — never the legacy long-lived SA token Secrets |
| External federation | **OIDC federation** of the cluster issuer to cloud IAM / IdP | Agent pods assume cloud roles with zero stored cloud keys (IRSA / Workload Identity pattern) |
| Cross-platform standard | **SPIFFE/SPIRE** — flag as the standard to evaluate | SVIDs issued from attested node+workload selectors; adopt when identity must span clusters, clouds, or non-K8s runtimes; overkill for a single managed cluster with OIDC federation |
| Agent → platform API | **OAuth2 Client Credentials grant** | THE machine-to-machine grant: the agent authenticates as itself (prefer private_key_jwt or mTLS-bound over a client secret) and receives a short-lived scoped access token. Never authorization-code flows or borrowed human tokens |
| Service ↔ service | **mTLS** (mesh-issued short-lived certs) | Encryption + mutual identity in one move |
| In-request authz context | **JWT claims propagation** | Carry the original principal (human researcher AND acting agent) in verified claims so downstream services authorize on who's really asking — the defense against the **confused deputy** (a privileged platform service tricked into acting for an unauthorized caller) |

Identity model for agents: a **per-agent, per-task session identity** — "agent X, dispatched by researcher Y, for task Z, expiring at T" — not one blessed `platform-agent` service account shared by everything. Session identity is what makes the audit trail mean anything.

### Machine authorization: the three pitfalls
1. **Over-permissive service accounts.** Advanced authz (JIT requests, dual authorization) was built for humans; it breaks automated workflows, so teams respond by granting machines broad standing roles — trading attack surface for convenience. This is the default failure mode of agent deployments.
2. **Granularity explosion.** Least privilege at full granularity is combinatorially huge — a single cloud compute service can expose ~585 distinct IAM actions, across 200+ services, before you count in-instance permissions. Perfect hand-crafted granularity is unachievable. Resolution: define permissions at the level of **platform golden-path operations** (`jobs:submit`, `datasets:read`), not raw cloud actions, and let the platform API translate. This is why agent authorization belongs at the platform/MCP layer, where the vocabulary is small.
3. **JIT friction vs. automation.** Human-style JIT approval per action would stall every agent loop. Resolution: move approval **up a level** — humans approve the *policy* (which task classes get which scopes, per the four-class action taxonomy: read-only / reversible writes / external side effects / high-risk), agents receive per-task scoped credentials automatically within it, and only class-4 actions page a human. Per-invocation authorization stays, but it's fast automated policy evaluation, not human review.

Zero-trust operating rules for agent workloads:
- Least privilege scoped per task, not per agent lifetime.
- Authorization checked per invocation, not per session.
- Namespace micro-segmentation with default-deny NetworkPolicy.
- Immutable, sandboxed containers for agent execution.
- Audit trails on by default, no opt-out.

### The unified human+machine policy and audit plane
One policy engine, one audit stream, two principal types. Every audit event carries: acting identity (agent session), on-behalf-of identity (dispatching human or trigger), task/run ID, resource, decision, and policy version. Anti-patterns to reject:
- Separate "bot audit" logs nobody correlates with the human stream.
- Agents sharing a human's credentials — attribution destroyed at the source.
- Policy expressed twice (IdP rules for humans, YAML for machines) drifting apart silently.

The audit stream feeds directly into the attribution evidence `asdlc-maturity-assessment` demands and the metrics `platform-fitness-functions` instruments.

### The scored checklist
Score each 0 (absent) / 1 (partial) / 2 (enforced by default); report as n/20:

| # | Check |
|---|---|
| 1 | No standing secrets: zero static API keys/tokens in agent configs, repos, or prompts |
| 2 | All agent credentials TTL-bounded (target: minutes–hours, never days) |
| 3 | Credentials chained to an attested root of trust (platform or hardware) |
| 4 | Per-agent per-task session identities; no shared agent service account |
| 5 | OAuth2 client credentials (or equivalent asserted identity) for every agent→API call |
| 6 | Legacy long-lived K8s SA token Secrets eliminated; projected tokens only |
| 7 | Scopes defined in platform-operation vocabulary, least-privilege per task class |
| 8 | Per-invocation policy evaluation; class-4 actions human-gated |
| 9 | mTLS + claims propagation downstream; confused-deputy test passes |
| 10 | Unified audit plane: human + agent events, on-behalf-of chain, queryable |

## Workflow
1. **Inventory principals and secrets.** For [YOUR ORGANIZATION / CLIENT]: every agent/automation identity, what credential it holds, TTL, scope, where stored. Grep configs and repos for static keys; list K8s ServiceAccounts with their token types and RoleBindings.
2. **Score the checklist** with evidence per row; the n/20 is the headline and feeds the benchmark gap register (`platform-maturity-benchmark`).
3. **Design the identity stack** from the table above for the org's actual estate — single managed cluster → projected tokens + OIDC federation; multi-cluster/hybrid → evaluate SPIFFE/SPIRE — including the session-identity scheme and credential issuance flow.
4. **Design authorization:** platform-operation scope vocabulary, task-class→scope policy matrix, class-4 human gates, and the per-invocation evaluation point (gateway or policy engine).
5. **Design the audit plane:** event schema with on-behalf-of chain, retention, and the queries that must be answerable ("everything agent session X touched"; "every mutation on behalf of researcher Y last week").
6. **Sequence migration:** eliminate standing secrets first (highest risk, clearest win), then session identities, then scope narrowing, then unified audit — each phase locked in with a fitness function so regression is impossible (`platform-fitness-functions`: temporal checks on credential TTLs, CI scans failing on static keys).
7. **Output.** Identity architecture brief: current-state inventory, scored checklist, target stack table, scope matrix, audit event schema, and the migration sequence with owners.

## Guardrails
- Never accept "we store keys in Vault" as the end state — managed secrets beat sprawled secrets, but the target is no standing secrets.
- Never let an agent run under a human's credentials or a shared bot account; unattributable autonomy is a finding, not a convenience.
- Reject any design where MCP servers or agent gateways hold one broad credential and "filter internally" — scoping happens at credential issuance.
- Don't gold-plate: SPIFFE/SPIRE for a single-cluster estate is complexity without payoff; say so.
- JIT friction is real — never propose per-action human approval for agent loops; approve policy, automate within it.
- Identity engineering here; org-wide governance and compliance program design → sibling `platform-security-playbook` (platform-assessment plugin).

## Suggested effort
Medium-high — inventory plus scored checklist in a half day; the full identity architecture brief is a multi-day engagement artifact.
