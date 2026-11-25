---
name: dmarc
description: >-
  RFC 9989 DMARC (DMARCbis): publish, evaluate and report on _dmarc policy records, with RFC 9990 aggregate reports and RFC 9991 failure reports. Covers the record tags (v, p, sp, np, t, psd, adkim, aspf, rua, ruf, fo), relaxed and strict SPF and DKIM identifier alignment, Organizational Domain discovery with the DNS Tree Walk instead of the Public Suffix List, receiver policy evaluation and enforcement, the rollout from p=none to quarantine and reject with t=y test mode, external report destination verification (_report._dmarc), the aggregate report XML schema, failure reports, and privacy. Use when adding or reviewing a DMARC record, moving a domain to enforcement, implementing DMARC checks in a mail receiver, generating or parsing DMARC reports, or debugging why mail fails DMARC. Triggers: DMARC, DMARCbis, _dmarc, dmarc=fail, rua, ruf, p=reject, p=quarantine, pct, Organizational Domain, tree walk, PSD DMARC, aggregate report, forensic report. RFC 7489 and RFC 9091 are legacy: upgrade from them to RFC 9989.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# DMARC

DMARC (Domain-based Message Authentication, Reporting, and Conformance) lets the owner of the domain in a message's `From` header publish a DNS record that ties that domain to aligned SPF or DKIM results, states how to handle failures, and asks for reports. RFC 9989, published by the IETF in May 2026, defines it with RFC 9990 (aggregate reporting) and RFC 9991 (failure reporting); together they obsolete RFC 7489 and RFC 9091. With this skill the agent writes and reviews DMARC records, plans the rollout to enforcement, implements receiver evaluation, and produces or parses reports.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Bare section numbers are RFC 9989. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Domain Owner (publishes records for its domains), PSO (publishes for a public suffix), Mail Receiver (evaluates and reports), or Report Consumer (receives and parses reports).
- Target version: RFC 9989 with RFC 9990 and RFC 9991 (default). RFC 7489 and RFC 9091 are legacy: read records and implementations written for them and upgrade, never author against them. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, search the RFC Editor index for DMARC RFCs that update or obsolete RFC 9989, RFC 9990 or RFC 9991, check their errata, check the IANA DMARC registry for new tags, and update the pins.
- Domains: the Author Domains in use, their Organizational Domain, and any delegated subtrees or names with more than eight labels.
- Mail streams: every system and third party that sends as the domain, with its MAIL FROM domain and DKIM `d=`.
- Users: whether people at the domain post to mailing lists or rely on forwarding. This decides whether `p=reject` is appropriate.
- Reporting: who receives aggregate reports, whether failure reports are wanted, and whether any destination is outside the domain.

## Invariants

1. **Record location and version.** The record is a TXT record at `_dmarc.<domain>`, and `v=DMARC1` (case-sensitive) is the first tag, or the record is ignored (§ 4.5, § 4.7). Multiple strings are concatenated (§ 4.5); several DMARC records at one name are all discarded (§ 4.10).
2. **Tolerant parsing.** Unknown tags MUST be ignored and syntax errors fall back to defaults (§ 4.7, § 4.8). Without a valid `p`, a record with a valid `rua` is treated as `p=none`; otherwise no DMARC processing (§ 4.10.1).
3. **Pass means aligned.** A message passes only if SPF (MAIL FROM identity only) or DKIM (`d=` of a valid signature) passes for an identifier aligned with the Author Domain (§ 3.2.4, § 4.4, § 5.3.5).
4. **Alignment uses the DNS Tree Walk.** Strict is identical domains; relaxed is the same Organizational Domain, found by the tree walk of at most eight queries, not a Public Suffix List (§ 3.2.10, § 4.10, § 4.10.2).
5. **Historic tags are not published.** `pct`, `rf` and `ri` are historic; use `t=y` where `pct=0` was used (§ A.6, § C.5.2, § 9.3).
6. **PSO records carry `psd=y`** (§ 5.2), and multi-organizational PSDs MUST NOT publish `ruf` (§ 10.2).
7. **No request, no report.** Receivers MUST NOT send aggregate reports without `rua` or failure reports without `ruf`, and MUST support `mailto:` if they send them (§ 4.7).
8. **External destinations are verified** through a `v=DMARC1` TXT record at `<policy domain>._report._dmarc.<destination host>`; unverified URIs MUST be ignored (RFC 9990 § 4, RFC 9991 § 5).
9. **Fix before enforcing.** Legitimate unaligned streams MUST be fixed before an Enforcement policy is published (§ 5.1.6). A domain at `p=reject` MUST NOT rely solely on SPF and MUST DKIM-sign (§ 7.4, § 8).
10. **Receivers do not reject on policy alone.** They MUST NOT reject solely because of `p=reject`, and without other evidence MUST treat such failures as `p=quarantine` (§ 7.4, § 8). A discovered `p=none` MUST NOT change existing handling (§ 5.4).
11. **Reports are well-formed and authenticated.** Aggregate reports follow the RFC 9990 XML schema with one DMARC Policy Domain per report, and their mail stream MUST pass DMARC (RFC 9990 § 3.1, § 3.5.2). Failure report generators MUST rate-limit (RFC 9991 § 2).

## Workflow

1. **Pick the version.** Use RFC 9989 with RFC 9990 and RFC 9991. If a record has `pct`, `rf` or `ri`, or code uses a Public Suffix List, plan the upgrade (step 9).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is RFC 9989, and no legacy-only tag or algorithm is introduced.
2. **Inventory and align the mail streams** (Domain Owner). For each stream, set an aligned MAIL FROM domain for SPF and an aligned DKIM `d=` (§ 5.1.1, § 5.1.2).
   -> [`references/rollout.md`](references/rollout.md)
   ✓ Every stream is listed with both identifiers and their alignment with the Author Domain.
3. **Set up reporting.** Create the aggregate report mailbox and parser; for a third-party Report Consumer, have it publish the `_report._dmarc` authorization record (RFC 9990 § 4). Request failure reports only for targeted diagnostics (RFC 9991 § 7).
   -> [`references/reporting.md`](references/reporting.md)
   ✓ Every `rua` and `ruf` destination is inside the domain or has a verified authorization record.
4. **Write the record in Monitoring Mode.** Publish `p=none` with `rua` at each Author Domain and the Organizational Domain (§ 5.1.4); add `sp`, `np`, `psd` or alignment modes only when needed.
   -> [`references/record-and-tags.md`](references/record-and-tags.md)
   ✓ Exactly one record per name, it matches the § 4.8 ABNF, and `v=DMARC1` comes first.
5. **Analyse and remediate.** Read aggregate reports until every legitimate source passes with alignment (§ 5.1.5, § 5.1.6).
   -> [`references/reporting.md`](references/reporting.md), [`references/rollout.md`](references/rollout.md)
   ✓ No legitimate source fails DMARC in the reports.
6. **Move to Enforcement** (only when asked). Step through quarantine, using `t=y` to test each level, before any `reject`; decide on `reject` against § 7.4.
   -> [`references/rollout.md`](references/rollout.md)
   ✓ Each stage held until reports were clean; `p=reject` only with aligned DKIM on all mail and the mailing-list impact considered.
7. **Evaluate at a receiver** (Mail Receiver). Extract the Author Domain, discover the policy with the tree walk, collect SPF and DKIM results, check alignment, decide, and apply local policy informed by the assessment policy.
   -> [`references/alignment-and-tree-walk.md`](references/alignment-and-tree-walk.md)
   ✓ The tree walk issues at most eight queries; § B.4 examples give the expected Organizational Domains; `p=reject` alone never causes a rejection.
8. **Generate or consume reports.** Build RFC 9990 aggregate reports (and RFC 9991 failure reports if offered), or parse them defensively.
   -> [`references/reporting.md`](references/reporting.md)
   ✓ Reports validate against RFC 9990 Appendix A, use the required filename and Subject, and the parser survives malformed or compressed-bomb input.
9. **Upgrade** (only when asked). Follow the RFC 7489 or RFC 9091 to RFC 9989 steps: replace `pct` with `t`, drop `rf`, `ri` and URI size limits, switch PSL lookups to the tree walk, add `psd=y` for PSDs, and move reports to the RFC 9990 schema.
   -> [`references/versions.md`](references/versions.md)
   ✓ The record parses under RFC 9989 with the same intended policy, and Organizational Domains resolve as intended under the tree walk.

## Verify before done

- [ ] Each `_dmarc` name has exactly one record, starting with `v=DMARC1`, that matches the RFC 9989 § 4.8 ABNF.
- [ ] No `pct`, `rf`, `ri` or `!size` URI suffix in any record (§ 4.8, § C.5.2).
- [ ] Every sending stream produces at least one aligned pass, and preferably both SPF and DKIM (§ 5.1, § 8).
- [ ] Any `p=reject` domain DKIM-signs all mail with an aligned `d=`, and its users' mailing-list use has been considered (§ 7.4).
- [ ] PSO records have `psd=y`; multi-organizational PSD records have no `ruf` (§ 5.2, § 10.2).
- [ ] External `rua` and `ruf` hosts publish `<domain>._report._dmarc` authorization records (RFC 9990 § 4, RFC 9991 § 5).
- [ ] Author Domains with more than eight labels have their own record (§ 5.1.8).
- [ ] Receiver code caps the tree walk at eight queries, ignores unknown tags, and never rejects on `p=reject` alone (§ 4.10, § 4.7, § 7.4).
- [ ] Aggregate reports validate against RFC 9990 Appendix A with namespace `urn:ietf:params:xml:ns:dmarc-2.0`.

## Reference index

- **`references/versions.md`**: RFC 9989, RFC 7489 and RFC 9091 with their status, what DMARCbis changed, and upgrade steps for records, receivers and report consumers. Load for steps 1 and 9.
- **`references/record-and-tags.md`**: record location, ABNF, every tag with defaults, `t` and `fo` semantics, historic tags, who publishes what, examples and common mistakes. Load for step 4.
- **`references/alignment-and-tree-walk.md`**: identifiers, strict and relaxed alignment, the DNS Tree Walk, policy discovery, Organizational Domain selection, receiver evaluation, enforcement and security. Load for step 7.
- **`references/reporting.md`**: external destination verification, the aggregate report XML structure and delivery rules, failure reports, and privacy. Load for steps 3, 5 and 8.
- **`references/rollout.md`**: Monitoring Mode to Enforcement, the policy ladder with `t=y`, when `p=reject` fits, subdomains and delegated zones. Load for steps 2, 5 and 6.

## Related skills

- `spf` for publishing and evaluating the SPF records DMARC aligns with: `npx skills add ScaleDockHQ/scaledock-skills --skill spf`.
- `dkim` for signing with an aligned `d=` and verifying signatures: `npx skills add ScaleDockHQ/scaledock-skills --skill dkim`.
- `list-unsubscribe` for the unsubscribe headers on bulk and list mail: `npx skills add ScaleDockHQ/scaledock-skills --skill list-unsubscribe`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9989: Domain-Based Message Authentication, Reporting, and Conformance (DMARC)](https://www.rfc-editor.org/rfc/rfc9989): RFC (Proposed Standard), RFC 9989 (May 2026), two verified editorial errata, checked 2026-10-05.
- [RFC 9990: DMARC Aggregate Reporting](https://www.rfc-editor.org/rfc/rfc9990): RFC (Proposed Standard), RFC 9990 (May 2026), checked 2026-10-05.
- [RFC 9991: DMARC Failure Reporting](https://www.rfc-editor.org/rfc/rfc9991): RFC (Proposed Standard), RFC 9991 (May 2026), checked 2026-10-05.
- [RFC 7489: Domain-based Message Authentication, Reporting, and Conformance (DMARC)](https://www.rfc-editor.org/rfc/rfc7489): RFC (Informational, obsoleted by RFC 9989, RFC 9990 and RFC 9991), RFC 7489 (March 2015), checked 2026-10-05.
- [RFC 9091: Experimental DMARC Extension for Public Suffix Domains](https://www.rfc-editor.org/rfc/rfc9091): RFC (Experimental, obsoleted by RFC 9989), RFC 9091 (July 2021), checked 2026-10-05.
- [RFC 9989 errata](https://www.rfc-editor.org/errata/rfc9989): RFC Editor errata, errata IDs 9025 and 9150 (verified), checked 2026-10-05.
- [IANA DMARC parameters registry](https://www.iana.org/assignments/dmarc-parameters/): IANA registry, last updated 2026-05-22, checked 2026-10-05.
- [IETF dmarc WG documents](https://datatracker.ietf.org/wg/dmarc/documents/): IETF Datatracker, WG active, checked 2026-10-05.
- [RFC Editor index](https://www.rfc-editor.org/rfc-index.txt): RFC Editor, index searched for DMARC, checked 2026-10-05.
