---
name: bimi
description: >-
  BIMI (Brand Indicators for Message Identification): publish BIMI DNS records and SVG logos, and have receivers show them only on DMARC-authenticated mail. Covers draft-brand-indicators-for-message-identification-14. Use when publishing a BIMI record, building BIMI support into a mail receiver or MUA, or debugging BIMI-Location, BIMI-Indicator and Authentication-Results bimi= headers. Triggers: BIMI, brand indicators, VMC, CMC, mark certificate, _bimi TXT record.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# BIMI

Brand Indicators for Message Identification (BIMI), the Internet-Draft draft-brand-indicators-for-message-identification-14 (1 May 2026, intended status Standards Track). Domain Owners publish a BIMI Assertion Record in DNS; receivers check DMARC, find the record, fetch and validate the Indicator, and add BIMI header fields.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Domain Owner (publishing records and Indicators), receiver or MTA (discovery, validation and headers), or MUA (display).
- Target version: BIMI draft-14 (current, posture: build). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **§ 1.** "To participate in BIMI, Domain Owners MUST have a strong [DMARC] policy (quarantine or reject) on both the Organizational Domain, and the RFC5322.From Domain of the message."
2. **§ 1.** "Quarantine policies MUST NOT have a pct less than pct=100."
3. **§ 4.3.** "It MUST have the value of "BIMI1" for implementations compliant with this version of BIMI."
4. **§ 4.3.** "The URI, if present, MUST contain a fully qualified domain name (FQDN) and MUST specify HTTPS as the URI scheme ("https")."
5. **§ 5.5.** "The BIMI-Location, BIMI-Indicator, and BIMI-Logo-Preference headers MUST NOT be DKIM signed."
6. **§ 6.4.** "The BIMI-Location header MUST NOT be set by email senders, and Protocol Clients MUST ignore it."
7. **§ 7.1.** "If more than 1 RFC5322.From header is present in the message, or any RFC5322.From header contains more than 1 email address then BIMI processing MUST NOT be performed for this message."
8. **§ 7.1.** "If the DMARC [RFC7489] policy for the Author Domain or Author Organizational Domain is p=none then BIMI processing MUST NOT be performed for this message."
9. **§ 7.2.** "Assertion Record Discovery MUST NOT be attempted if the message authentication fails per Receiver policy."
10. **§ 7.2.** "Clients MUST query the DNS for a BIMI TXT record at the DNS domain constructed by concatenating the selector, the string '_bimi', and the Author Domain."
11. **§ 7.8.** "Regardless of success of the BIMI lookup, if a BIMI-Location, BIMI-Indicator, or BIMI-Logo-Preference header is already present in a message it MUST be either removed or renamed."
12. **§ 7.9.** "This header MUST NOT be added if Discovery or Validation steps failed."

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
- [ ] The DMARC policy on the Author Domain and Organizational Domain is quarantine (pct=100) or reject before a BIMI record is published.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `dmarc`, `dkim`, `spf`, `svg`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Brand Indicators for Message Identification (BIMI), draft-14](https://www.ietf.org/archive/id/draft-brand-indicators-for-message-identification-14.txt): Internet-Draft, draft-brand-indicators-for-message-identification-14, 1 May 2026, checked 2026-10-06.
