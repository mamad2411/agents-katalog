---
name: deploy-target
description: Set or switch the deployment target platform (aws/gcp/azure/cloudflare/vercel/kubernetes/vps) and load its service landscape into the working context.
---

# /deploy-target [target]

Owner: **platform-lead**; architecture impact assessed by **lead-architect**.

1. No argument: show current target and the available catalogs under `constraints/platforms/`.
2. With argument: read `constraints/platforms/<target>.yaml`; summarize the landscape in one
   table — compute, data, messaging, storage, edge, observability, IaC preference, notable limits.
3. If an architecture already exists (post-ARB), this is a re-platform: lead-architect produces
   an impact note (which mappings break, migration cost class) BEFORE the switch is confirmed —
   switching targets after ARB re-opens the ARB gate.
4. Update CLAUDE.md `deployment_target`; log an ADR if this changes a prior decision.

## Output
Updated config; landscape summary; impact note + reopened gate status if applicable.
