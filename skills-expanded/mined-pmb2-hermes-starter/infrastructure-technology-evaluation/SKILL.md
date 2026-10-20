---
name: infrastructure-technology-evaluation
description: "Systematic methodology for evaluating a technology (K8s, service mesh, database, etc.) for adoption across a user's full infrastructure stack — discover services, assess readiness workload-by-workload, produce a phased migration roadmap with decision matrix."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [infrastructure, evaluation, migration, assessment, technology-adoption, roadmap, audit]
    triggers: [evaluate-technology, migration-assessment, infrastructure-audit, technology-readiness, adoption-roadmap, should-i-adopt, kubernetes-assessment, k8s-evaluation, stack-evaluation]
    related_skills: [vps-application-deployment, plan, writing-plans, spike]
    triggers_extended:
      - "authenticate users"
      - "auth system"
      - "FOSS authentication solution"
      - "evaluate auth options"
      - "login with google"
      - "OAuth provider"
      - "social login"
      - "SSO for apps"
      - "user management system"
---

# Infrastructure Technology Evaluation

Systematic methodology for evaluating whether a specific technology (Kubernetes, service mesh, database, CI/CD platform, observability stack) is right for a user's infrastructure — based on comprehensive document analysis, workload-by-workload assessment, and phased migration planning.

## When to Use

Trigger conditions — any of:
- User asks to evaluate a technology for their stack ("evaluate K8s", "should I use X")
- User asks for a migration assessment ("is it time to move to X")
- User asks for an infrastructure audit or readiness check
- User wants a structured report with findings and recommendations
- User wants to understand the cost/benefit of adopting a new technology

## Workflow

### Phase 1: Document & Infrastructure Discovery

The first step is always understanding *what exists*. Do not jump to evaluation until the full picture is mapped.

**1a. Locate document sources:**
- Check home directory for overview files (`*CENSUS*`, `*ECOSYSTEM*`, `*INVENTORY*`, `*MAP*`)
- Check primary Documents directory
- Check secondary drives (D:, E: mounts for user data)
- Check Obsidian vault if configured
- Check GitHub repos folder for architecture docs

**1b. Read overview documents first:**
```bash
# Find census/ecosystem/summary docs first — they give you the lay of the land
find /docs -name "*CENSUS*" -o -name "*ECOSYSTEM*" -o -name "*INVENTORY*" | head -10
# Then read them to understand the full stack before diving into specifics
```

**1c. Map the current infrastructure across these dimensions:**
- Host environment (OS, Docker, GPU, CPU, RAM)
- Running containers/services (count, categorization)
- Tech stacks and their dependencies
- Databases and storage (count, types, port mappings)
- Networks and proxy layers
- Deployment patterns (Docker Compose, VPS, hybrid)
- Backup/DR strategy
- Key operational constraints (solo operator? team? budget?)

### Phase 2: Technology Readiness Assessment

For each major workload or subsystem, assess readiness against the target technology:

**Assessment criteria:**
- **Stateless vs Stateful**: Can it be ephemeral? (Stateless = easier, Stateful = harder)
- **GPU dependency**: Does it need GPU? (GPU = harder in most orchestration systems)
- **Data gravity**: How much persistent data? (More data = harder migration)
- **Scaling need**: Does it benefit from horizontal scaling?
- **Dependency tree**: What other services depend on it?
- **Migration complexity**: Simple container move vs complex re-architecture
- **Business criticality**: Can it have downtime?

**Categorize workloads into tiers:**

| Tier | Label | Action |
|------|-------|--------|
| **Tier 1** | Best candidates | Stateless, scalable, no GPU, low data gravity |
| **Tier 2** | Conditional | Stateful but migratable with PVC/CSI |
| **Tier 3** | Stay put | GPU-bound, too complex, low ROI for migration |
| **Tier 4** | Already fine | On VPS or lightweight, no migration needed |

### Phase 3: Operational Impact Analysis

Assess the non-technical factors that often matter more:

- **Solo operator overhead**: How much maintenance time does the new tech add? (5-10 hrs/week for K8s, ~0 for Docker Compose)
- **Learning curve**: Is the technology familiar to the user?
- **Cost**: Additional hardware, cloud services, operational time
- **Developer experience regression**: Will iteration speed slow down?
- **Portability gains**: Does the new tech make the stack cloud-neutral?
- **Hardware requirements**: Does it require a second machine? GPU? More RAM?

### Phase 4: Decision Matrix & Verdict

Build a comparison table across the key criteria:

| Criteria | Current State | Improved State | New Tech |
|----------|--------------|----------------|----------|
| Iteration speed | ✅ Fast | ✅ Fast | ⚠️ Slower |
| Auto-healing | ❌ None | ⚠️ Partial | ✅ Full |
| Zero-downtime | ❌ None | ❌ None | ✅ RollingUpdate |
| H. scaling | ❌ None | ❌ None | ✅ HPA |
| Resource mgmt | ❌ None | ✅ Limits | ✅ QoS |
| Operator burden | 🟢 Low | 🟢 Low | 🟠 Medium |

Use a clear verdict label:
- ✅ **Ready** — Adopt now, clear benefits
- ⏳ **Not Ready But High Potential** — Fix precursor issues first, then adopt
- ❌ **Not Worth It** — Costs/overhead outweigh benefits for this user

### Verdict Sensitivity: Single-Node vs Multi-Node

**The verdict for distributed technologies (K8s, service mesh, etc.) depends critically on node count.** A single-node eval and a multi-node eval of the same user's stack can reach opposite conclusions:

| Scenario | Node Count | Typical Verdict | Reason |
|----------|-----------|-----------------|--------|
| Single desktop, all workloads local | 1 | ❌ Not Ready | K8s on 1 node loses HA, scheduling choice, spread. Docker Compose + Phase 0 is cheaper and faster. |
| Single desktop + 1 VPS with client services | 2+ | ✅ Ready for client workloads | Multi-node unlocks real value: pod spread, node failure tolerance, unified control plane across providers. Internal/GPU workloads stay on Docker. |
| Multi-VPS, multi-provider, serving clients | 3+ | ✅ Strongly Ready | K8s provides the unified control plane that makes multi-provider, multi-tenant operations feasible. Without it, each VPS is an SSH snowflake. |

**Always ask:** "How many machines / VPS nodes are involved?" If the answer is 1, the bar for K8s adoption is much higher. If it's 2+, the calculus flips.

### Verdict Branch for Client/Service Providers

When the user serves external clients or runs multi-tenant workloads, add this dimension:

```
User serves clients?
├── No → Standard evaluation (current stack focus)
├── Yes, 1-2 clients → Adopt K8s specifically for client workloads
│     Internal stack stays on existing tooling
│     Client apps get K8s benefits (auto-healing, GitOps, zero-downtime)
│
└── Yes, 3+ clients → Strong K8s adoption signal
      Client isolation via namespaces + network policies
      Standardized deployment pipeline (Helm charts + ArgoCD)
      Per-client resource quotas and cost tracking
      Without K8s: SSH hell × N servers
```

The key insight: **separate "internal stack" from "client workloads."** Internal stack (GPU models, complex compose apps, high-data-gravity DBs) can stay on Docker Compose indefinitely. Client workloads (new Next.js apps, APIs, Postgres instances) benefit enormously from K8s — even on a 2-node cluster.

### Phase 5: Phased Migration Roadmap

Always produce phased recommendations — never propose a big-bang migration:

**Phase 0 — Current Stack Improvements (Fix What You Have First)**
- Resource limits, health checks, compose profiles
- Backup/restore pipeline
- Consolidation and monitoring
- Zero-cost, immediate improvements

For the exact YAML patterns (per-service limits, healthchecks, profiles, logging blocks), see `references/docker-compose-hardening-patterns.md`.

**Phase 1 — First Footprint (3-6 Months)**
- Prerequisite: second machine if needed
- Migrate lowest-risk workloads (stateless, Tier 1)
- Set up GitOps and CI/CD
- Keep hardest workloads (GPU, stateful) on current stack

**Phase 2 — Full Value (6-12 Months)**
- Split into specialized clusters/environments
- Add service mesh, observability, advanced scheduling
- Migrate stateful workloads with proven backup/restore

Include a **prerequisites checklist** for each phase and a clear **decision flowchart** based on hardware availability.

**For multi-node / client-service scenarios**, see `references/verdict-flip-multi-vps-case.md` for how the verdict can change from single-node to multi-node analysis.

### Phase 6: Report Deliverable

Write the report to `_docs/` or a project directory with:
- Executive summary with clear verdict
- Current infrastructure assessment (table + diagram)
- Pain points the new technology would solve
- Red flags / why it's premature
- Workload-by-workload analysis (4 tiers)
- Recommended architecture diagram
- Phased migration roadmap
- Infrastructure requirements and budget
- Decision matrix
- Immediate actions checklist

## Pitfalls

- **Skipping Phase 1**: Jumping to evaluation without mapping the full stack leads to wrong recommendations. Always read the census/ecosystem docs first.
- **Ignoring operator burden**: A solo developer managing 101 containers needs different advice than a team of 5 SREs. Always factor in who operates the stack.
- **Single-GPU ceiling**: Workloads that share one GPU cannot benefit from orchestration-level scaling. Until there are 2+ GPU machines, K8s provides no GPU benefit over Docker.
- **Data gravity is the hardest problem**: Volume migration (Docker volumes → PV/PVC) is the most complex and risky part of any Docker→K8s migration. Don't underestimate it.
- **DevEx regression**: For a solo developer, `docker compose up -d --build` is dramatically faster than the K8s build→push→apply→wait loop. Account for this in recommendations.
- **Phase 0 before Phase 1**: Always fix Docker-native issues (resource limits, health checks, profiles) before even planning K8s migration. Most pain points can be addressed at the Docker level.
- **Don't recommend K8s on single node**: K8s on one machine removes most of its value proposition (no multi-node scheduling, no HA, no spread). If there's only one machine, recommend thorough Docker improvements instead.
- **Avoid "you should migrate everything"**: Always tier workloads. A phased approach with clear criteria for what stays and what moves is more credible and actionable.

## Verification Steps

After the evaluation:
- [ ] All workloads categorized into tiers
- [ ] Decision matrix has all key criteria compared
- [ ] Phase 0 improvements are actionable and zero-cost
- [ ] Each phase has prerequisites listed
- [ ] Verdict is clearly stated with reasoning
- [ ] Report includes both current architecture and target architecture visuals
- [ ] Hardware requirements and costs are estimated
- [ ] Solo operator overhead is explicitly addressed
