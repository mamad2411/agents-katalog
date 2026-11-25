---

name: "dependency-lifecycle-orchestrator"

description: "Orchestrates dependency management, including security audits, version upgrades, and lifecycle management."

version: 1

created: "2026-07-31"

updated: "2026-07-31"

---

## When to Use

Use for any task involving project dependencies, including security audits, version upgrades, and general dependency health management.



## Procedure

0. **Pre-Flight Memory Recall & Fork Guardrail Gate**:
   - Query local memory for dependency standards and prior upgrade incident postmortems:
     ```bash
     python3 ~/memory_system/inspect_memory.py --preflight .
     ```
   - Verify repository origin:
     ```bash
     python3 ~/memory_system/check_fork_guardrail.py .
     ```
   - **Active Fork Gate**: If the target repository is a fork of an active upstream project, **HALT automated dependency updates**. Consider refreshing the fork from upstream (`gh repo sync`) instead of making unilateral changes.

1. Identify the dependency task: Security Audit, Version Upgrade, or General Management.

2. For Security Audits: Use `dependency-security-audit` to scan for vulnerabilities and license issues.

3. For Version Upgrades: Use `dependency-updater` for safe updates and `dependency-upgrade` for major version transitions.

4. For General Management: Use `dependency-security-audit` for ongoing dependency health checks.

5. Synthesize the results into a clear action plan for the engineering team.



## Pitfalls

- **NEVER** apply automated dependency updates to an active forked repository; refresh from upstream or propose an upstream PR.

- Never perform major version upgrades without a staged rollout and full test suite.

- Ensure security audits are performed on every release candidate.

- Do not ignore 'dependency-updater' warnings for critical production packages.



## Verification

1. Dependency audit reports are generated and reviewed.

2. Version upgrades are tested and documented.

3. Project dependencies remain healthy and secure.


