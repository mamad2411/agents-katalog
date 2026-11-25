---
name: tdmrep
description: >-
  W3C TDMRep (TDM Reservation Protocol): declare and read text and data mining rights reservations and
  TDM licensing policies for web content, following the W3C Community Group Final Report of 10 May 2024.
  Use when a publisher or rightsholder opts content out of text and data mining under Article 4(3) of
  the EU CDSM Directive 2019/790 (the opt-out general-purpose AI providers must honor under EU AI Act
  Article 53(1)(c)), or when a crawler, AI training pipeline or TDM agent must detect and apply those
  reservations: tdm-reservation and tdm-policy in /.well-known/tdmrep.json, HTTP response headers, HTML
  meta tags, EPUB 2, EPUB 3 and PDF XMP metadata, path patterns with * and $, processing priority, and
  ODRL 2.2 TDM Policies (Offer, assigner vCard, tdm:mine, obtainConsent, compensate, tdm:research).
  Triggers: TDMRep, TDM reservation, text and data mining opt-out, tdmrep.json, tdm-reservation header,
  CDSM Article 4, AI training opt-out.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# TDM Reservation Protocol (TDMRep)

TDMRep is a W3C Community Group specification for stating, in machine-readable form, whether text and data mining (TDM) rights over a web resource are reserved, and where a TDM licensing policy can be found. It answers the "appropriate manner, such as machine-readable means" condition of Article 4 of the EU CDSM Directive. With this skill the agent publishes reservations for a site or files, or detects and applies them in a crawler or AI pipeline.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Section names refer to the Final Community Group Report of 10 May 2024. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

TDMRep is a Community Group report, "not a W3C Standard nor ... on the W3C Standards Track" (Status of This Document). It states a rights reservation; it does not block retrieval. This skill describes the protocol, not the law.

## Inputs (fill in, or ask before starting)

- Role: publisher or rightsholder (declares), TDM agent (crawler or pipeline that reads and applies), or both.
- Technique: the well-known file, HTTP headers, HTML meta, or EPUB/PDF metadata (Protocol).
- Policy: whether to offer a TDM Policy, and its terms (contact, consent, compensation, purpose).
- Target version: TDMRep Final Report 2024 (default). No legacy line or preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources), compare the editor's draft with the Final Report, check the Community Group for a newer report, and update the pins.

## Invariants

1. **Two properties.** `tdm-reservation` (`1` reserved, `0` not reserved) and optional `tdm-policy` (a URL) (Declaring the reservation of TDM Rights).
2. **Anything other than `1` or `0` is a protocol error and means unset** (tdm-reservation).
3. **The Article 4 opt-out is `tdm-reservation: 1`** (tdm-reservation).
4. **A policy beside `0` is not an error, but agents SHOULD NOT process it** (tdm-policy).
5. **Unreachable or unparsable policies are not errors;** the agent then has no way to know the conditions for processing (tdm-policy).
6. **The well-known file is `/.well-known/tdmrep.json`, a JSON array of rules** with required `location` and `tdm-reservation` and optional `tdm-policy`; the brackets are mandatory even for one rule (TDM File on the Origin Server).
7. **The first matching rule wins;** matching is case-sensitive with `*` and `$` as in robots.txt; no match means unset (TDM File on the Origin Server).
8. **Agents check the well-known file before scraping a server, then headers on every response, then HTML meta, then EPUB/PDF metadata,** each later value superseding earlier ones, and an absent property never resets a value (Processing priority).
9. **Publishers SHOULD use only one technique** (Processing priority).
10. **Policies are ODRL 2.2 Offers** with the two-value `@context`, a `uid`, `profile` `http://www.w3.org/ns/tdmrep`, one `assigner` and a `permission` array whose action is `tdm:mine` (Expressing a TDM Policy).

## Workflow

1. **Pick the version.** Use the 2024 Final Report.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded.
2. **Decide the reservation** (publisher). Choose `1` or `0` per path or file, and whether to offer a policy.
   -> [`references/declaring.md`](references/declaring.md)
   ✓ Every path the rightsholder cares about has an explicit value.
3. **Publish it** (publisher). Write `tdmrep.json` rules most-specific first, or send headers, or add HTML meta or EPUB/PDF metadata, using one technique where possible.
   -> [`references/declaring.md`](references/declaring.md)
   ✓ For sample URLs the first matching rule, header or meta tag yields the intended value.
4. **Write the policy** (optional). Build an ODRL Offer with assigner contact details and permissions with duties or constraints.
   -> [`references/policies.md`](references/policies.md)
   ✓ The policy is served as `application/json` or `application/ld+json` and has every MUST property.
5. **Apply reservations** (agent). Fetch and cache the well-known file, match the URL, then let headers, HTML meta and file metadata supersede in order, and treat unset as unknown, not permission.
   -> [`references/declaring.md`](references/declaring.md)
   ✓ Each mined resource has a recorded value and the technique it came from.

## Verify before done

- [ ] `/.well-known/tdmrep.json` is a JSON array, each rule has `location` and `tdm-reservation`, and specific rules come before general ones (TDM File on the Origin Server).
- [ ] Every `tdm-reservation` value is the integer `1` or `0` (tdm-reservation).
- [ ] Header names are `tdm-reservation` and `tdm-policy`; HTML meta names match; EPUB and PDF use `tdm:reservation` and `tdm:policy` (Protocol).
- [ ] The agent never treats unset as "not reserved" and never lets a missing property reset a value (Processing priority).
- [ ] Policies have `@type` `Offer`, the tdmrep `profile`, one `assigner` and `tdm:mine` permissions (Expressing a TDM Policy).
- [ ] PDF/A files do not carry TDMRep XMP properties, which a PDF/A validator rejects (TDM Metadata in PDF files).
- [ ] Documentation does not present TDMRep as access control.

## Reference index

- **`references/versions.md`**: the single line, the editor's draft relationship and what to watch. Load for step 1.
- **`references/declaring.md`**: the two properties, every technique with examples, pattern matching, processing priority and the legal context. Load for steps 2, 3 and 5.
- **`references/policies.md`**: the ODRL TDM Policy profile: context, type, profile, assigner, permissions, duties and constraints. Load for step 4.

## Related skills

- `robots-txt` for crawl access, which TDMRep does not control: `npx skills add ScaleDockHQ/scaledock-skills --skill robots-txt`.
- `aipref`, `content-signals` and `rsl` for other AI usage and licensing signals: `npx skills add ScaleDockHQ/scaledock-skills --skill aipref`, `--skill content-signals`, `--skill rsl`.
- `odrl` for the ODRL 2.2 model TDM Policies profile: `npx skills add ScaleDockHQ/scaledock-skills --skill odrl`.
- `eu-ai-act` for general-purpose AI provider obligations: `npx skills add ScaleDockHQ/scaledock-skills --skill eu-ai-act`.
- `well-known-uris` for the `/.well-known/` namespace: `npx skills add ScaleDockHQ/scaledock-skills --skill well-known-uris`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [TDM Reservation Protocol (TDMRep), Final Community Group Report](https://www.w3.org/community/reports/tdmrep/CG-FINAL-tdmrep-20240510/): Final Community Group Report (W3C TDMRep CG), 10 May 2024, checked 2026-10-09.
- [TDM Reservation Protocol (TDMRep), editor's draft](https://w3c-cg.github.io/tdm-reservation-protocol/spec/): Editor's Draft, unchanged in substance from the Final Report, checked 2026-10-09.
- [Directive (EU) 2019/790 (CDSM Directive)](https://eur-lex.europa.eu/eli/dir/2019/790/oj): EU Directive, OJ L 130 of 17.5.2019, Article 4, checked 2026-10-09.
- [AI Act Article 53: Obligations for providers of general-purpose AI models](https://ai-act-service-desk.ec.europa.eu/en/ai-act/article-53): European Commission AI Act Service Desk, Regulation (EU) 2024/1689 Article 53(1)(c), checked 2026-10-09.
