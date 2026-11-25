---
name: dns-over-https
description: >-
  DNS over HTTPS (RFC 8484): resolve DNS queries over HTTPS, with SVCB and HTTPS records for discovery. Covers RFC 8484 DNS Queries over HTTPS (DoH), RFC 9460 Service Binding and Parameter Specification via the DNS (SVCB and HTTPS Resource Records). Use when resolving DNS over HTTPS. Triggers: DoH, RFC 8484, SVCB.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# DNS Queries over HTTPS (DoH)

DNS Queries over HTTPS (DoH)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when resolving DNS over HTTPS.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 8484 DNS Queries over HTTPS (DoH) (default); RFC 9460 Service Binding and Parameter Specification via the DNS (SVCB and HTTPS Resource Records) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 8484 § 4.1.** "DoH servers MUST implement both the POST and GET methods."
2. **RFC 8484 § 5.** "This protocol MUST be used with the https URI scheme [RFC7230]."
3. **RFC 8484 § 5.1.** "The assigned freshness lifetime of a DoH HTTP response MUST be less than or equal to the smallest TTL in the Answer section of the DNS response."
4. **RFC 8484 § 5.3.** "Before using DoH response data for DNS resolution, the client MUST establish that the HTTP request URI can be used for the DoH query."
5. **RFC 8484 § 5.4.** "In order to maximize interoperability, DoH clients and DoH servers MUST support the "application/dns-message" media type."
6. **RFC 8484 § 6.** "When using the GET method, the data payload for this media type MUST be encoded with base64url [RFC4648] and then provided as a variable named "dns" to the URI Template expansion."
7. **RFC 8484 § 6.** "Padding characters for base64url MUST NOT be included."
8. **RFC 9460 § 2.2.** "If any RRs are malformed, the client MUST reject the entire RRset and fall back to non-SVCB connection establishment."
9. **RFC 9460 § 2.4.2.** "To avoid unbounded alias chains, clients and recursive resolvers MUST impose a limit on the total number of SVCB aliases they will follow for each resolution request."
10. **RFC 9460 § 9.4.** "Clients MUST NOT use an HTTPS RR response unless the client supports the TLS Server Name Indication (SNI) extension and indicates the origin name in the TLS ClientHello (which might be encrypted via a future specification such as [ECH])."
11. **RFC 9460 § 12.** "SVCB/HTTPS RRs permit distribution over untrusted channels, and clients are REQUIRED to verify that the alternative endpoint is authoritative for the service (similar to Section 2.1 of [AltSvc])."

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

- [RFC 8484 DNS Queries over HTTPS (DoH)](https://www.rfc-editor.org/rfc/rfc8484.html): PROPOSED STANDARD, RFC 8484 (PROPOSED STANDARD, October 20), checked 2026-10-06.
- [RFC 9460 Service Binding and Parameter Specification via the DNS (SVCB and HTTPS Resource Records)](https://www.rfc-editor.org/rfc/rfc9460.html): PROPOSED STANDARD, RFC 9460 (PROPOSED STANDARD, November 2), checked 2026-10-06.
