---
name: s2c2f
description: >-
  S2C2F: secure how a project consumes open source dependencies, by practice and maturity level. Covers S2C2F. Use when assessing a secure supply chain. Triggers: S2C2F.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# S2C2F

The OpenSSF Secure Supply Chain Consumption Framework (S2C2F): eight practices (Ingest, Scan, Inventory, Update, Audit, Enforce, Rebuild, Fix and Upstream) and their 25 requirements ING-1 to FIX-1, each with a maturity level from L1 to L4, read from the framework's Markdown source at a pinned commit.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Engineering, security or compliance owner of how an organization ingests and uses open source software.
- Target version: S2C2F (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **ING-2 (L1).** "Use an OSS binary repository manager solution (i.e. JFrog Artifactory, Azure Artifacts, etc.)"
2. **SCA-1 (L1).** "Scan OSS for known vulnerabilities (i.e. CVEs, GitHub Advisories, etc.)"
3. **INV-1 (L1).** "Maintain an automated inventory of all OSS used in development"
4. **AUD-3 (L2).** "Validate integrity of the OSS that you consume into your build"
5. **ENF-1 (L2).** "Securely configure your package source files (i.e. nuget.config, .npmrc, pip.conf, pom.xml, etc.)"

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
- [ ] Each requirement from ING-1 to FIX-1 at or below the target maturity level is assessed, and every finding names its requirement id.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `slsa`, `owasp-scvs`, `openssf-baseline`, `owasp-ci-cd-top-10`, `in-toto`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Secure Supply Chain Consumption Framework (S2C2F) Simplified Requirements](https://raw.githubusercontent.com/ossf/s2c2f/d0f0a7fbbc6cc6cb6a248cbc9e98c3d8cf3b189a/specification/framework.md): OpenSSF Community Specification, Version 1.1, commit d0f0a7fbbc6c (2025-05-26), checked 2026-10-06.
