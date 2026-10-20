---
name: devops-and-platform
description: >
  Build delivery and platform practices. Use for CI/CD pipelines, Docker and
  containers, Kubernetes, Terraform/IaC, DevOps vs SRE vs platform engineering,
  Nginx, config management, build systems, and developer platform design.
  Triggers: "CI/CD", "Docker", "Kubernetes", "k8s", "pipeline", "SRE",
  "platform engineering", "Nginx", "build system".
---

# DevOps and Platform

Shorten the path from commit to production, safely and repeatably.

## When to use
- Setting up or improving CI/CD.
- Containerizing and orchestrating services.
- Defining team operating models (DevOps/SRE/Platform).
- Building internal developer platforms.

## CI/CD
- **CI:** build, lint, test, scan, package on every commit. Fast, blocking,
  reproducible.
- **CD:** automated deploy to staging/prod; progressive delivery for rollout.
- Pipeline stages: source → build → test → scan → artifact → deploy → verify →
  monitor → rollback.
- Trunk-based development + short-lived branches enable continuous delivery.

## Containers & orchestration
- Docker: images, layers, multi-stage builds, small base images, non-root,
  `.dockerignore`, one process per container.
- Kubernetes: pods, deployments, services, ingress, configmaps/secrets, HPA,
  probes, namespaces; deployment strategies; service types (ClusterIP,
  NodePort, LoadBalancer, ExternalName).
- Don't run state on K8s without a story (StatefulSets, operators, volumes).

## Infrastructure & config
- IaC for all infra (Terraform); config management vs IaC.
- Nginx as reverse proxy/LB: TLS termination, caching, rate limit, static.
- Build systems at scale: caching, remote build, monorepo tooling (Amazons
  Brazil, Bazel-style).

## Operating model
- DevOps = culture + automation; SRE = reliability engineering with SLOs/error
  budgets; Platform engineering = internal product for developers.
- Golden paths/paved roads to reduce cognitive load.

## Checklist
- [ ] CI fast, blocking, reproducible; tests + scans.
- [ ] Artifacts immutable + versioned.
- [ ] CD with progressive rollout + rollback.
- [ ] Containers minimal, non-root, scanned.
- [ ] K8s probes, limits, autoscaling configured.
- [ ] All infra in IaC.
- [ ] SLOs + on-call + runbooks (SRE).
- [ ] Developer golden path documented.

## Common pitfalls
- Flaky/slow CI nobody trusts.
- Snowflake servers; manual infra changes.
- Latest tags instead of immutable versions.
- No resource limits → noisy neighbor eviction.
- Running stateful workloads on K8s without operators.

## References
- `...\cicd-pipeline-explained-in-simple-terms.md`, `...\cicd-simplified-visual-guide.md`, `...\how-do-companies-ship-code-to-production.md`
- `...\9-docker-best-practices-you-must-know.md`, `...\top-8-must-know-docker-concepts.md`, `...\how-does-docker-work.md`
- `...\what-is-k8s-kubernetes.md`, `...\kubernetes-periodic-table.md`, `...\top-10-k8s-design-patterns.md`, `...\the-ultimate-kubernetes-command-cheatsheet.md`, `...\top-4-kubernetes-service-types-in-one-diagram.md`
- `...\a-cheatsheet-on-infrastructure-as-code-landscape.md`, `...\how-does-terraform-turn-code-into-cloud.md`
- `...\devops-vs-sre-vs-paltform-engg.md`, `...\devops-vs-noops.md`
- `...\why-is-nginx-so-popular.md`
- `...\how-does-amazon-build-system-work.md`
- `...\cloud-native-anti-patterns.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`deployment-strategies`, `observability`, `cloud-and-infrastructure`,
`security-and-auth`.
