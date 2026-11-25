---
name: cisa-secure-by-design
description: >-
  CISA Secure by Design: apply the secure-by-design principles to software products and their defaults. Covers Secure by Design. Use when applying CISA Secure by Design. Triggers: Secure by Design.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Secure by Design

CISA Secure by Design: the three software product security principles and the secure-by-default approach from the joint guide "Shifting the Balance of Cybersecurity Risk: Principles and Approaches for Secure by Design Software" (October 2023), and the seven goals of the Secure by Design Pledge for enterprise software manufacturers.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Software manufacturer: product owner, security lead or engineer deciding product defaults, vulnerability handling and transparency.
- Target version: Secure by Design (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Principle 1.** "Take ownership of customer security outcomes and evolve products accordingly. The burden of security should not fall solely on the customer."
2. **Secure by Default.** "A secure configuration should be the default baseline."
3. **Default passwords.** "At the end of provisioning, only the customer should possess their authentication credentials."
4. **Vulnerability disclosure policy.** "Within one year of signing the pledge, publish a vulnerability disclosure policy (VDP) that authorizes testing by members of the public on products offered by the manufacturer, commits to not recommending or pursuing legal action against anyone engaging in good faith efforts to follow the VDP, provides a clear channel to report vulnerabilities, and allows for public disclosure of vulnerabilities in line with coordinated vulnerability disclosure best practices and international standards."
5. **CVEs.** "Demonstrate transparency in vulnerability reporting by including accurate Common Weakness Enumeration (CWE) and Common Platform Enumeration (CPE) fields in every Common Vulnerabilities and Exposures (CVE) record for the manufacturer’s products."

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
- [ ] The product ships with a secure default configuration and no default passwords, and the manufacturer publishes a vulnerability disclosure policy and complete CVE records with CWE and CPE fields.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `nist-ssdf`, `owasp-proactive-controls`, `security-txt`, `cve-json`, `cwe`, `cisa-kev`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Shifting the Balance of Cybersecurity Risk: Principles and Approaches for Secure by Design Software](https://www.cisa.gov/sites/default/files/2023-10/SecureByDesign_1025_508c.pdf): CISA joint guidance, October 2023 update (TLP:CLEAR), checked 2026-10-06.
- [Secure by Design Pledge](https://www.cisa.gov/securebydesign/pledge): CISA voluntary pledge, Pledge launched May 2024, page read 2026-10-06, checked 2026-10-06.
