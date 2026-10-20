---
name: rsl
description: >-
  RSL 1.0 Really Simple Licensing: write, publish and read machine-readable AI licensing terms for web
  content, following RSL-SPEC-1.0 (Recommendation, 2025-12-10, errata to 2026-08-07), with upgrades
  from the RSL 0.9 draft. Use when a publisher, CDN or platform declares which automated and AI uses
  are permitted or prohibited (all, ai-all, ai-train, ai-input, ai-index, search), for which users and
  regions, and under which payment terms (free, attribution, purchase, subscription, training, crawl,
  use, contribution), or when a crawler, AI agent or training pipeline must discover, evaluate and honor
  those terms: the rsl XML document, application/rsl+xml, the robots.txt License directive, Link
  rel="license", HTML, RSS and file associations, max-age revalidation, conflict resolution,
  reporting, and the optional OLP, CAP (License auth scheme) and EMS protocols. Triggers: RSL, Really
  Simple Licensing, rslstandard.org, pay-per-crawl, pay-per-inference, AI content licensing.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Really Simple Licensing (RSL)

RSL is an XML vocabulary, published by the RSL Technical Steering Committee (RSL Collective), for machine-readable usage, licensing, payment and legal terms that govern how AI systems and automated agents may access or use digital assets, plus the ways to associate those terms with content. With this skill the agent writes and publishes RSL licenses for a site, or discovers and evaluates them in a crawler or agent.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. "§" refers to RSL-SPEC-1.0 as amended by its errata. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: publisher (origin, platform or CDN that declares terms), client (crawler, agent or pipeline that reads and honors them), or license server operator (OLP, CAP, EMS).
- Scope: which assets (site, path, page, element, feed item or file) the terms govern.
- Intent: which uses to permit or prohibit, for which user classes and regions, and the payment, reporting and legal terms.
- Association: robots.txt `License`, HTTP `Link`, HTML `<link>` or inline `<script>`, RSS, or embedded file metadata (§ 4.2).
- Target version: RSL 1.0 (default). RSL 0.9 is legacy: read it and upgrade from it, never author it. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), check the errata page and `https://rslstandard.org/rsl/latest/` for a newer version or namespace, and update the pins.

## Invariants

1. **The namespace identifies RSL.** Every document declares `https://rslstandard.org/rsl` as the default namespace on `<rsl>`, unprefixed; processors identify RSL by namespace, not media type, and serve it as `application/rsl+xml` (§ 2.2).
2. **Unknown RSL-namespace elements break conformance; foreign ones are ignored.** Unknown elements or attributes in the RSL namespace make the document non-conformant, and unrecognized extensions from other namespaces are ignored with their contents (§ 1.2, § 3).
3. **Structure:** `<rsl>` holds `<content url="...">` elements, each with at least one `<license>` (§ 3.1, § 3.3). The `url` is an RFC 9309 path (with `*` and `$`) unless the association is HTML, RSS or an embedded file (§ 3.3).
4. **Order never matters; specific beats general; prohibition beats permission.** All applicable terms are evaluated together, the narrower scope wins, a usage both permitted and prohibited is not licensed, and terms are read conservatively (§ 3.1.1).
5. **`<permits>` enumerates; `<prohibits>` excludes.** At most one of each per `type` (`usage`, `user`, `geo`) per license; values are space-separated tokens from the normative vocabularies (§ 3.4.1, § 3.5, § 3.6).
6. **No `<payment>` means free**; a `server` attribute means the client must obtain a license from that License Server even when the payment type is `free` or `attribution` (§ 3.3, § 3.7).
7. **Revalidate.** `max-age` is a positive number of days, defaulting to 30; the document and the association that pointed to it must both be revalidated within it (§ 3.2, § 3.2.1).
8. **Clients must locate, parse and comply before access.** A client that cannot obtain a valid RSL document treats the asset as unlicensed (§ 4, § 4.3).
9. **robots.txt `License` is an absolute URI**; group-scoped directives replace global ones for that group; `License` does not change `Allow` or `Disallow` (§ 4.4.1, § 4.4.2).
10. **`Link` and HTML `<link>` use `rel="license"` and `type="application/rsl+xml"`** with an absolute URL (§ 4.5, § 4.6.1).
11. **Across channels, most specific wins and conflicts resolve most-restrictively** (§ 4.9).
12. **Unmet reporting means unlicensed.** A client that cannot satisfy a `<reporting>` profile treats the activity as not licensed (§ 3.12).
13. **HTTPS only.** RSL files, license metadata and all OLP traffic are fetched over HTTPS (§ 5.1, § 8).

## Workflow

1. **Pick the version.** Use RSL 1.0. If an existing document uses comma-separated lists or `type="inference"`, it is 0.9: plan the upgrade (step 7).
   -> [`references/versions.md`](references/versions.md)
   ✓ The document targets the `https://rslstandard.org/rsl` namespace under RSL 1.0 rules.
2. **Model the terms** (publisher). Choose `<content>` scopes, then `<permits>`/`<prohibits>` by usage, user and geo, then `<payment>` with `<standard>`, `<custom>`, `<amount>` or `<accepts>`, then any `<reporting>`, `<legal>`, `<alternate>`, `<schema>`, `<copyright>` and `<terms>` (§ 3.3 to § 3.17).
   -> [`references/document.md`](references/document.md)
   ✓ Each intended use maps to one effective outcome under § 3.1.1, and the document validates against the Appendix A schema.
3. **Associate the license** (publisher). Add a robots.txt `License:` line, `Link` headers, HTML associations, RSS `rsl:` elements or embedded metadata, and keep them consistent (§ 4.2, § 4.9).
   -> [`references/discovery.md`](references/discovery.md)
   ✓ Every licensed asset has at least one association, and all associations point to documents with the same terms.
4. **Discover and evaluate** (client). Check every association point, select the robots.txt group, fetch the documents, validate them, and compute the effective license (§ 4.2 to § 4.4, § 4.9).
   -> [`references/discovery.md`](references/discovery.md)
   ✓ For each fetched asset the client records the documents used, their `max-age` and the effective permits, prohibitions, payment and reporting.
5. **Enforce or acquire** (only with a `server`, CAP or EMS). Implement OLP `/token`, `/introspect` and `/key`, the `License` authentication scheme and the 401/402/403 responses (§ 4.10, § 5, § 6, § 7).
   -> [`references/protocols.md`](references/protocols.md)
   ✓ Protected requests carry `Authorization: License <token>`, and failures return `WWW-Authenticate: License` plus a license reference.
6. **Review security and privacy.** HTTPS, client authentication, rate limits, opaque tokens and data minimization (§ 8, § 9).
   -> [`references/protocols.md`](references/protocols.md)
   ✓ No license metadata carries personal data, and no endpoint accepts unauthenticated clients.
7. **Upgrade** (only when asked). Rewrite 0.9 documents to 1.0 tokens and lists.
   -> [`references/versions.md`](references/versions.md)
   ✓ The upgraded document validates under RSL 1.0 and grants no right the 0.9 document did not.

## Verify before done

- [ ] `<rsl xmlns="https://rslstandard.org/rsl">` is the root, unprefixed, and every `<content>` has a `url` and at least one `<license>` (§ 2.2, § 3.3).
- [ ] Every token is in the § 3.4.1 vocabularies or a namespaced extension; lists are space-separated (§ 3.5, Appendix A).
- [ ] Every `server` attribute has a non-empty `url`, and `encrypted="true"` has a `server` (§ 3.3, § 7.1).
- [ ] robots.txt `License` values are absolute URIs, and `Link`/`<link>` carry `rel="license"` and `type="application/rsl+xml"` (§ 4.4.1, § 4.5, § 4.6.1).
- [ ] The client treats a missing or invalid document as unlicensed and revalidates within `max-age` (default 30 days) (§ 3.2.1, § 4.3).
- [ ] Documentation does not claim RSL enforces itself: enforcement is a server choice (§ 4.10).

## Reference index

- **`references/versions.md`**: RSL 1.0 and the 0.9 draft, the errata history, and the upgrade checklist. Load for steps 1 and 7.
- **`references/document.md`**: every element and attribute, the usage, user, payment, reporting, warranty and disclaimer vocabularies, conflict resolution and worked examples. Load for step 2.
- **`references/discovery.md`**: robots.txt, `Link`, HTML, RSS and embedded associations, precedence and the client evaluation algorithm. Load for steps 3 and 4.
- **`references/protocols.md`**: OLP endpoints, the CAP `License` scheme and error codes, EMS key retrieval, and security and privacy. Load for steps 5 and 6.

## Related skills

- `robots-txt` for RFC 9309 groups and path matching that RSL reuses: `npx skills add ScaleDockHQ/scaledock-skills --skill robots-txt`.
- `content-signals` for the robots.txt usage vocabulary RSL's usage tokens include: `npx skills add ScaleDockHQ/scaledock-skills --skill content-signals`.
- `aipref` for IETF AI usage preferences: `npx skills add ScaleDockHQ/scaledock-skills --skill aipref`.
- `tdmrep` for the W3C text and data mining reservation: `npx skills add ScaleDockHQ/scaledock-skills --skill tdmrep`.
- `x402` for the payment protocol `<accepts type="application/x402+json">` names: `npx skills add ScaleDockHQ/scaledock-skills --skill x402`.
- `web-bot-auth` for crawler identity that CAP should be paired with: `npx skills add ScaleDockHQ/scaledock-skills --skill web-bot-auth`.
- `oauth` for the OAuth 2.0 client credentials and introspection OLP builds on: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Really Simple Licensing (RSL) 1.0 Specification](https://rslstandard.org/rsl): Recommendation (RSL TSC), RSL-SPEC-1.0 published 2025-12-10, checked 2026-10-09.
- [RSL 1.0 Specification: Errata and Change History](https://rslstandard.org/rsl/errata): errata log, latest entry 2026-08-07, checked 2026-10-09.
- [RSL latest version pointer](https://rslstandard.org/rsl/latest/): version index, points to 1.0, checked 2026-10-09.
- [RSL Default Access Terms](https://rslstandard.org/rsl/default-terms): referenced terms document (§ 3.17.1), checked 2026-10-09.
- [Really Simple Licensing (RSL) 0.9 Specification](https://rslstandard.org/rsl/0.9/): Draft, version 0.9 last updated 2025-09-16, superseded, checked 2026-10-09.
- [RFC 9309: Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309): RFC (Proposed Standard), RFC 9309, checked 2026-10-09.
