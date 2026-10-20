---
name: mta-sts
description: >-
  MTA-STS (RFC 8461) and TLS-RPT (RFC 8460): enforce TLS for inbound SMTP and receive TLS failure reports. Covers RFC 8461 SMTP MTA Strict Transport Security (MTA-STS), RFC 8460 SMTP TLS Reporting. Use when publishing an MTA-STS policy. Triggers: MTA-STS, TLS-RPT, RFC 8461.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# SMTP MTA Strict Transport Security (MTA-STS)

SMTP MTA Strict Transport Security (MTA-STS)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing an MTA-STS policy.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 8461 SMTP MTA Strict Transport Security (MTA-STS) (default); RFC 8460 SMTP TLS Reporting (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 8461 § 2.** "However, MTA-STS is designed not to interfere with DANE deployments when the two overlap; in particular, senders who implement MTA-STS validation MUST NOT allow MTA-STS Policy validation to override a failing DANE validation."
2. **RFC 8461 § 3.1.** "If the number of resulting records is not one, or if the resulting record is syntactically invalid, senders MUST assume the recipient domain does not have an available MTA-STS Policy and skip the remaining steps of policy discovery."
3. **RFC 8461 § 3.3.** "HTTP 3xx redirects MUST NOT be followed, and HTTP caching (as specified in [RFC7234]) MUST NOT be used."
4. **RFC 8461 § 3.3.** "If a valid TXT record is found but no policy can be fetched via HTTPS (for any reason), and there is no valid (non-expired) previously cached policy, senders MUST continue with delivery as though the domain has not implemented MTA-STS."
5. **RFC 8461 § 3.3.** "Conversely, if no "live" policy can be discovered via DNS or fetched via HTTPS, but a valid (non-expired) policy exists in the sender's cache, the sender MUST apply that cached policy."
6. **RFC 8461 § 4.2.** "The certificate MUST have a subject alternative name (SAN) [RFC5280] with a DNS-ID [RFC6125] matching the hostname, per the rules given in [RFC6125]."
7. **RFC 8461 § 5.1.** "A message delivery attempt MUST NOT be permanently failed until the sender has first checked for the presence of a new policy (as indicated by the "id" field in the "_mta-sts" TXT record)."
8. **RFC 8461 § 7.2.** "MTAs supporting MTA-STS MUST have support for TLS 1.2 [RFC5246] or TLS 1.3 [RFC8446] or higher."
9. **RFC 8460 § 3.** "Reports sent via SMTP MUST contain a valid DomainKeys Identified Mail (DKIM) [RFC6376] signature by the reporting domain."
10. **RFC 8460 § 5.3.1.** "Note that, when sending failure reports via SMTP, Sending MTAs MUST NOT honor MTA-STS or DANE TLSA failures."

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
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 8461 SMTP MTA Strict Transport Security (MTA-STS)](https://www.rfc-editor.org/rfc/rfc8461.html): PROPOSED STANDARD, RFC 8461 (PROPOSED STANDARD, September ), checked 2026-10-06.
- [RFC 8460 SMTP TLS Reporting](https://www.rfc-editor.org/rfc/rfc8460.html): PROPOSED STANDARD, RFC 8460 (PROPOSED STANDARD, September ), checked 2026-10-06.
