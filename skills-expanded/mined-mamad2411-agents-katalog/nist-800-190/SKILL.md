---
name: nist-800-190
description: >-
  NIST SP 800-190: secure container images, registries, orchestrators, containers and host operating systems. Covers SP 800-190. Use when securing application containers. Triggers: SP 800-190.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# NIST SP 800-190

NIST Special Publication 800-190, Application Container Security Guide: the major risks to images, registries, orchestrators, containers and host OSs (Section 3), and the countermeasures for each (Section 4).

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when securing application containers.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: team building, deploying or operating containerized apps, or reviewing a container platform.
- Target version: SP 800-190 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 4.1.4.** "Secrets should be stored outside of images and provided dynamically at runtime as needed."
2. **§ 4.1.5.** "Organizations should maintain a set of trusted images and registries and ensure that only images from this set are allowed to run in their environment, thus mitigating the risk of untrusted or malicious components being deployed."
3. **§ 4.4.3.** "Organizations should automate compliance with container runtime configuration standards."
4. **§ 4.4.4.** "Containers should also be run with their root filesystems in read-only mode."
5. **§ 4.5.5.** "In no case should containers be able to mount sensitive directories on a host's file system, especially those containing configuration settings for the operating system."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [SP 800-190](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-190.pdf): NIST SP, SP 800-190, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
