---
name: security-txt
description: >-
  RFC 9116 security.txt: write, serve, sign, parse and audit the
  /.well-known/security.txt file that tells researchers how to report
  vulnerabilities, with every field in the IANA security.txt Fields registry
  (Contact, Expires, Encryption, Acknowledgments, Preferred-Languages,
  Canonical, Policy, Hiring, CSAF, Bug-Bounty). Use when publishing a
  vulnerability disclosure contact for a domain or IP address, reviewing or
  renewing an existing security.txt, building a scanner or parser for it,
  adding an OpenPGP cleartext signature, advertising a CSAF provider-metadata.json,
  or upgrading a file written against draft-foudil-securitytxt (legacy, for
  example files without Expires). Triggers: security.txt, .well-known/security.txt,
  RFC 9116, vulnerability disclosure contact, Expires field, Canonical field,
  PGP signed security.txt, text/plain charset=utf-8, security.txt scanner,
  security.txt expired.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# security.txt

RFC 9116, an Informational RFC from the IETF, defines `security.txt`: a machine-parsable text file at `/.well-known/security.txt` that tells security researchers how to report vulnerabilities to the organization behind a domain or IP address. With this skill the agent writes, serves, signs, parses and audits that file, and upgrades files written against the pre-RFC drafts.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: publisher (an organization serving the file), researcher or tool (a consumer that fetches and parses it), or both.
- Target version: RFC 9116 (default). draft-foudil-securitytxt is legacy: read files written against it and upgrade them, never author against it. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the RFC Editor entry for RFC 9116 for errata or an updating RFC, check the IANA security.txt Fields registry for new fields, search the datatracker for drafts that update RFC 9116, and update the pins.
- Hosts: every domain, subdomain and IP address that needs a file. One file covers only the host it is fetched from (§ 3.1).
- Contacts: the reporting channels in order of preference (email, phone, web form), and whether an OpenPGP key exists for encrypted reports.
- Disclosure policy: the URL of the vulnerability disclosure policy, if there is one.
- Signing: whether the file will carry an OpenPGP cleartext signature, and with which key.

## Invariants

1. **Location.** Web services place the file at `/.well-known/security.txt` (§ 3). A legacy `/security.txt` may exist or redirect there; when both exist, the `/.well-known/` file MUST be used (§ 3).
2. **Transport.** The file is fetched over HTTP 1.0 or later with the `https` scheme, and served as `text/plain` with `charset=utf-8` (§ 3, § 5.7).
3. **Format.** Plain text, UTF-8 in Net-Unicode form, and it MUST follow the § 4 ABNF (§ 2, § 4). Every line ends in CRLF or LF (§ 2.2).
4. **Fields.** Each field has a name, a colon, a space and a value, on its own line; names are case-insensitive; values are not chained unless the field definition allows it (§ 2, § 4).
5. **Contact is required** and may repeat, in order of preference; its value is a URI, so email and phone use `mailto:` and `tel:` (§ 2.5.3).
6. **Expires is required exactly once**, as an RFC 3339 date-time, and SHOULD be less than a year away (§ 2.5.5). Generators SHOULD write an upper-case `T` and `Z` (RFC 3339 § 5.6).
7. **Preferred-Languages appears at most once** and lists at least one language tag (§ 2.5.8).
8. **Every web URI value starts with `https://`** (§ 2.5.1 to § 2.5.7). Encryption points to a key; it never contains the key (§ 2.5.4).
9. **Scope.** A file applies only to the domain or IP address in the URI used to fetch it, not to subdomains or parent domains (§ 3.1).
10. **Consumers ignore fields they do not support** (§ 2.4), and treat every registered extension field as optional (§ 2.4, § 6.2).
11. **Canonical is binding when present.** If the retrieval URI is not listed in any Canonical field, the contents SHOULD NOT be trusted (§ 2.5.2).
12. **No implied permission.** Neither the presence nor the absence of the file grants or denies permission to test (§ 5.5).

## Workflow

1. **Pick the version.** Use RFC 9116. If an existing file has no Expires, uses a `Signature:` or `Permission:` field, or uses an RFC 5322 date, it was written against a draft: plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is RFC 9116, and any draft-era file is listed for upgrade.
2. **Choose the fields.** Write one or more Contact fields in preference order, one Expires, and the optional fields that apply: Encryption, Policy, Acknowledgments, Preferred-Languages, Canonical, Hiring, and registry fields such as CSAF.
   -> [`references/fields.md`](references/fields.md)
   ✓ Every value matches its field's syntax, and only Contact, Encryption, Canonical, Policy, Acknowledgments, Hiring and CSAF repeat.
3. **Set Expires and an owner.** Pick a date under a year away and record who renews the file before it.
   -> [`references/fields.md`](references/fields.md)
   ✓ Expires is in the future, under a year away, and a renewal is scheduled.
4. **Sign** (recommended). Add Canonical lines for every URI the file is served from, then make an OpenPGP cleartext signature over the final text.
   -> [`references/serving-and-signing.md`](references/serving-and-signing.md)
   ✓ The signature verifies, and the file still matches the § 4 `signed` production.
5. **Serve it.** Publish at `/.well-known/security.txt` on every in-scope host over HTTPS with `Content-Type: text/plain; charset=utf-8`; optionally redirect `/security.txt` to it. Reserve both names on multi-tenant hosts.
   -> [`references/serving-and-signing.md`](references/serving-and-signing.md)
   ✓ A plain HTTPS GET on each host returns 200 and the right media type, and every Canonical URI resolves to the same file.
6. **Parse and consume** (researcher or tool role). Fetch, record redirects, apply size limits, parse against the ABNF, check Expires and Canonical, verify any signature, then pick the first usable Contact.
   -> [`references/parsing-and-security.md`](references/parsing-and-security.md)
   ✓ The parser rejects stale, oversized and malformed files and ignores unknown fields.
7. **Review security.** Walk the § 5 considerations: compromise, redirects, stale data, malformed input, testing permission, multi-tenant hosts, transport and spam.
   -> [`references/parsing-and-security.md`](references/parsing-and-security.md)
   ✓ Every referenced resource is controlled by the organization, monitored, and reachable over HTTPS.
8. **Upgrade** (only when asked). Follow the draft to RFC 9116 checklist: add or reformat Expires, convert contacts to URIs, drop `Signature:`, `Permission:` and `Disclosure:`, move the file under `/.well-known/`, and re-sign.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded file parses against the RFC 9116 ABNF and reaches the same contacts.

## Verify before done

- [ ] `https://<host>/.well-known/security.txt` returns 200 with `Content-Type: text/plain; charset=utf-8` on every in-scope host (§ 3).
- [ ] At least one Contact, each a URI (`mailto:`, `tel:` or `https://`), listed in preference order (§ 2.5.3).
- [ ] Exactly one Expires, in RFC 3339 form, in the future and under a year away (§ 2.5.5).
- [ ] Preferred-Languages appears at most once (§ 2.5.8).
- [ ] Every web URI value starts with `https://` and every referenced page, mailbox and key is controlled by the organization (§ 5.3).
- [ ] If Canonical is present, the URI the file is served from is one of its values (§ 2.5.2).
- [ ] If signed, the signature verifies and the file matches the § 4 `signed` production (§ 2.3, § 4).
- [ ] The file is under 32 KB, every field under 2,048 characters, and fewer than 1,000 lines, so cautious parsers accept it (§ 5.4).
- [ ] Nothing in the file or its documentation says it grants permission to test (§ 5.5).

## Reference index

- **`references/versions.md`**: RFC 9116 and draft-foudil-securitytxt with their status, what changed across the drafts, the errata, the upgrade checklist, and why no preview is listed. Load for steps 1 and 8.
- **`references/fields.md`**: every field in the IANA registry with its syntax, cardinality, URI rules and examples, plus a complete example file. Load for steps 2 and 3.
- **`references/serving-and-signing.md`**: location, the legacy path, HTTPS and media type, scope, multi-tenant hosts, and OpenPGP cleartext signing with Canonical. Load for steps 4 and 5.
- **`references/parsing-and-security.md`**: the § 4 ABNF, parsing rules and limits, consumer checks, and every § 5 security consideration. Load for steps 6 and 7.

## Related skills

- `csaf` for the `provider-metadata.json` that the CSAF field points to: `npx skills add ScaleDockHQ/scaledock-skills --skill csaf`.
- `openssf-baseline` for the project-level vulnerability reporting controls a security.txt helps meet: `npx skills add ScaleDockHQ/scaledock-skills --skill openssf-baseline`.
- `eu-cra` for the manufacturer duty to publish a vulnerability reporting contact: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-cra`.
- `http-semantics` for redirects, media types and the `https` scheme in RFC 9110: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9116: A File Format to Aid in Security Vulnerability Disclosure](https://www.rfc-editor.org/rfc/rfc9116.html): RFC (Informational), RFC 9116 (April 2022), checked 2026-10-05.
- [RFC 9116 errata](https://www.rfc-editor.org/errata/rfc9116): RFC Editor errata, 1 verified (6946) and 2 reported (7264, 7743), checked 2026-10-05.
- [IANA security.txt Fields registry](https://www.iana.org/assignments/security-txt-fields/): IANA registry, last updated 2026-03-07, checked 2026-10-05.
- [securitytxt.org](https://securitytxt.org): project website by the RFC authors, checked 2026-10-05.
- [draft-foudil-securitytxt](https://datatracker.ietf.org/doc/draft-foudil-securitytxt/): Internet-Draft, revisions -00 to -12 (2017-09-10 to 2021-05-24), became RFC 9116, checked 2026-10-05.
- [draft-bruhns-securitytxt-product-security](https://datatracker.ietf.org/doc/draft-bruhns-securitytxt-product-security/): Internet-Draft (individual submission), -00 (2026-09-10), checked 2026-10-05.
- [RFC 9580: OpenPGP](https://www.rfc-editor.org/rfc/rfc9580): RFC (Proposed Standard), obsoletes RFC 4880, checked 2026-10-05.
- [RFC 3339: Date and Time on the Internet: Timestamps](https://www.rfc-editor.org/rfc/rfc3339): RFC (Proposed Standard), updated by RFC 9557, checked 2026-10-05.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): RFC (Internet Standard, STD 97), obsoletes RFC 7230 and RFC 7231, checked 2026-10-05.
- [CSAF Version 2.0](https://docs.oasis-open.org/csaf/csaf/v2.0/os/csaf-v2.0-os.html): OASIS Standard, requirement 8 (security.txt), checked 2026-10-05.
