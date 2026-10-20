---
name: nist-800-207
description: >-
  NIST SP 800-207: design a zero trust architecture with policy decision and enforcement points. Covers SP 800-207, SP 800-207A. Use when applying zero trust architecture. Triggers: zero trust, SP 800-207.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# NIST SP 800-207

NIST Special Publication 800-207, Zero Trust Architecture: the seven tenets of zero trust, the logical components (policy engine, policy administrator, policy enforcement point) and deployment models, plus SP 800-207A on identity-tier and network-tier policies for cloud-native applications.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when applying zero trust architecture.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: architect or security team designing, migrating to or reviewing a zero trust architecture.
- Target version: SP 800-207 (default); SP 800-207A (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **§ 1.** "In this new paradigm, an enterprise must assume no implicit trust and continually analyze and evaluate the risks to its assets and business functions and then enact protections to mitigate these risks."
2. **§ 2.1 tenet 2.** "Access requests from assets located on enterprise-owned network infrastructure (e.g., inside a legacy network perimeter) must meet the same security requirements as access requests and communication from any other nonenterprise-owned network."
3. **§ 2.1 tenet 3.** "Access to individual enterprise resources is granted on a per-session basis."
4. **§ 2.1 tenet 6.** "All resource authentication and authorization are dynamic and strictly enforced before access is allowed."

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

- [SP 800-207](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207.pdf): NIST SP, SP 800-207, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
- [SP 800-207A](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-207A.pdf): NIST SP, SP 800-207A, fetched 2026-10-06 (NIST SP, 2026-10-06), checked 2026-10-06.
