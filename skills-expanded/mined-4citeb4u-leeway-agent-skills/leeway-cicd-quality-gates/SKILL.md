---
name: leeway-cicd-quality-gates
description: Designs and reviews CI/CD quality gates for source, dependencies, tests, artifacts, supply chain, environments, deployment, and rollback. Use when creating or changing pipelines or deciding whether a build may advance.
license: MIT
metadata:
  authority: Creator/Human Authority > LeeWay Standards
  source-class: normalized-drive-candidate
---

# LeeWay CI/CD Quality Gates

Make gates deterministic, reproducible, least-privileged, and tied to protected artifacts. Cover lint/type/build, unit/integration/security tests, dependency and secret scanning, provenance/SBOM where required, environment promotion, smoke checks, and rollback. Separate runner failure from code failure and preserve logs, commit, artifact identity, and gate outcome.
