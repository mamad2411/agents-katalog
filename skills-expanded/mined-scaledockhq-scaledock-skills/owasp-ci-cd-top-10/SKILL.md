---
name: owasp-ci-cd-top-10
description: >-
  OWASP CI/CD Top 10: review build and deployment pipelines against the top CI/CD security risks. Covers OWASP CI/CD Top 10. Use when reviewing CI/CD security risks. Triggers: CI/CD Top 10.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OWASP CI/CD Top 10

The OWASP Top 10 CI/CD Security Risks (CICD-SEC-1 to CICD-SEC-10): each risk's definition and the recommended controls, read from the project's Markdown source at a pinned commit.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Reviewer or owner of an SCM, CI system, artifact repository or deployment pipeline.
- Target version: OWASP CI/CD Top 10 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **CICD-SEC-1.** "Establish pipeline flow control mechanisms to ensure that no single entity (human / programmatic) is able to ship sensitive code and artifacts through the pipeline without external verification or validation."
2. **CICD-SEC-4.** "Ensure that pipelines running unreviewed code are executed on isolated nodes, not exposed to secrets and sensitive environments."
3. **CICD-SEC-6.** "Ensure secrets that are used in CI/CD systems are scoped in a manner that allows each pipeline and step to have access to only the secrets it requires."
4. **CICD-SEC-9.** "Prior to consuming the resource in subsequent steps down the pipeline, the resource’s integrity should be validated against the signing authority."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Each of CICD-SEC-1 to CICD-SEC-10 is assessed, and every finding names its risk id.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `slsa`, `trusted-publishing`, `s2c2f`, `owasp-scvs`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [CICD-SEC-1: Insufficient Flow Control Mechanisms](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-01-Insufficient-Flow-Control-Mechanisms.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-2: Inadequate Identity and Access Management](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-02-Inadequate-Identity-And-Access-Management.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-3: Dependency Chain Abuse](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-03-Dependency-Chain-Abuse.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-4: Poisoned Pipeline Execution (PPE)](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-04-Poisoned-Pipeline-Execution.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-5: Insufficient PBAC (Pipeline-Based Access Controls)](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-05-Insufficient-PBAC.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-6: Insufficient Credential Hygiene](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-06-Insufficient-Credential-Hygiene.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-7: Insecure System Configuration](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-07-Insecure-System-Configuration.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-8: Ungoverned Usage of 3rd Party Services](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-08-Ungoverned-Usage-of-3rd-Party-Services.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-9: Improper Artifact Integrity Validation](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-09-Improper-Artifact-Integrity-Validation.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
- [CICD-SEC-10: Insufficient Logging and Visibility](https://raw.githubusercontent.com/OWASP/www-project-top-10-ci-cd-security-risks/74b2c790d5512998f232480dde61d4d42fa692ae/CICD-SEC-10-Insufficient-Logging-And-Visibility.md): OWASP Project document, Commit 74b2c790d551 (2025-11-03), checked 2026-10-06.
