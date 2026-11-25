---
name: architecture-variants
description: Produce 2-4 architecture variants designed against the deployment target's service landscape, with quantitative comparison and a recommendation. The core Phase 1 skill.
---

# /architecture-variants

Owner: **lead-architect**; platform mapping by **platform-lead**, data by **data-lead**,
costs by **cost-analyst**, SLO feasibility by **sre-lead**.

## Sequence
1. Inputs: product brief + requirements (load profile, latency class, availability tier, team
   skills, budget ceiling). Missing quantified load profile → stop, request via /product-brief.
2. Variant count from CLAUDE.md `architecture_variants` (default 3). Candidate shapes from
   `constraints/architecture-patterns.yaml` — e.g. serverless event-driven, modular monolith
   in containers, edge-first. If `deployment_target` is "compare", vary the target across
   variants instead of the shape.
3. Per variant, fill `.claude/docs/templates/architecture-variant.md`:
   - Component diagram (Mermaid) and rendering strategy.
   - **Component-to-service mapping table**: every logical component → concrete service from
     `constraints/platforms/<target>.yaml`, with its limits and pricing dimension. Native
     services first (AWS: Lambda/EventBridge/SQS/DynamoDB/CloudFront; Cloudflare: Workers/KV/
     D1/Queues; VPS: compose/nginx/systemd) — portability deviations recorded inline.
   - Data topology, async/eventing shape, auth approach.
   - Cost at launch / expected / 10x load (cost-analyst), operational burden class,
     lock-in assessment, scaling ceiling, SLO feasibility verdict (sre-lead).
4. Comparison table across variants + anti-pattern check against the patterns catalog.
5. Recommend one variant with reasoning; the user decides (per operation_mode). Adopt mode:
   include migration cost from `audit/current-state-report.md` as a comparison column.
6. Record the choice as `architecture/ADR-001-architecture-selection.md`.

## Output
`architecture/variants/variant-<X>-<name>.md` per variant; comparison + recommendation;
ADR-001 after the decision; risks → risk register.
