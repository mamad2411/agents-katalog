---
name: cloud-containers-scanning-container
description: "Cloud Containers Scanning Container."
domain: cybersecurity
---

|
| Multi-Stage Build | Docker build technique using multiple FROM stages to separate build and runtime, reducing final image size |
| Distroless | Google-maintained minimal container images containing only the application and runtime dependencies |
| Non-Root User | Running container processes as unprivileged user to limit impact of container escape exploits |
| Read-Only Root | Mounting the container root filesystem as read-only to prevent runtime modification |
| Image Digest | SHA256 hash uniquely identifying an exact image version, more precise than mutable tags |
| Scratch Image | Empty Docker base image used for statically compiled binaries requiring no OS |
| Security Context | Kubernetes pod/container-level security settings controlling privileges, filesystem, and capabilities |

## Tools & Systems

- **Docker BuildKit**: Advanced Docker build engine supporting multi-stage builds and build secrets
- **Distroless Images**: Google's minimal container base images (static, base, java, python, nodejs)
- **docker-bench-security**: Script checking CIS Docker Benchmark compliance
- **Trivy**: Container image vulnerability and misconfiguration scanner
- **Hadolint**: Dockerfile linter enforcing best practices

## Common Scenarios

### Scenario: Reducing a 1.2GB Python Image to Under 150MB

**Context**: A data science team uses `python:3.12` as base image (1.2GB) with scientific computing packages. The image has 200+ known CVEs from unnecessary system packages.

**Approach**:
1. Switch to `python:3.12-slim-bookworm` as base (150MB) and install only required system libraries
2. Use multi-stage build: compile C extensions in builder stage, copy wheels to production
3. Pin numpy, pandas, and scipy to pre-built wheels to avoid build dependencies in production
4. Remove pip, setuptools, and wheel from the final image
5. Create non-root user and set filesystem permissions
6. Validate with Trivy: expect CVE count to drop from 200+ to under 20

**Pitfalls**: Some Python packages require shared libraries at runtime (libgomp, libstdc++). Test the application thoroughly after removing system packages. Alpine-based images use musl libc which can cause compatibility issues with numpy and pandas.

## Output Format

```
Container Image Hardening Report
==================================
Image: app:hardened
Base: python:3.12-slim-bookworm
Date: 2026-02-23

SIZE COMPARISON:
  Before hardening: 1,247 MB (python:3.12)
  After hardening:  143 MB  (python:3.12-slim + multi-stage)
  Reduction: 88.5%

SECURITY CHECKS:
  [PASS] Non-root user configured (appuser:1000)
  [PASS] HEALTHCHECK instruction present
  [PASS] No setuid/setgid binaries found
  [PASS] Package manager removed
  [PASS] Base image pinned by digest
  [PASS] No shell access (/bin/sh removed)
  [WARN] /tmp writable (emptyDir mounted)

VULNERABILITY COMPARISON:
  Before: 234 CVEs (12 Critical, 45 High)
  After:  18 CVEs (0 Critical, 3 High)
  Reduction: 92.3%
```
