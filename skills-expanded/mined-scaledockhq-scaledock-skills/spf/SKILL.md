---
name: spf
description: >-
  RFC 7208 SPF: write, check and debug v=spf1 DNS records that authorize which
  hosts may send mail for a domain in the MAIL FROM and HELO identities. Use
  when publishing or reviewing an SPF record, adding a mail provider with
  include, hitting the 10 DNS lookup limit or the void lookup limit, chasing a
  permerror, temperror, softfail or fail, flattening a record, debugging
  forwarded mail that fails SPF, implementing check_host() in a receiver, or
  recording results in Received-SPF or Authentication-Results (RFC 8601).
  Covers the mechanisms all, include, a, mx, ptr, ip4, ip6 and exists, the
  qualifiers + - ~ ?, the redirect and exp modifiers, macros, record size, and
  the RFC 7372 enhanced status codes. RFC 7208 is the current line (updated by
  RFC 7372, RFC 8553 and RFC 8616); RFC 4408 is legacy, and the SPF RR type 99
  is obsolete. No preview exists. Triggers: SPF record, v=spf1, -all, ~all,
  too many DNS lookups, multiple SPF records, include:, redirect=, SPF
  flattening, SPF fail on forwarding.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Sender Policy Framework (SPF)

RFC 7208, an IETF Proposed Standard from the SPFbis working group, defines SPF version 1: a domain publishes a `v=spf1` record in a DNS TXT record listing the hosts allowed to use it in the SMTP `MAIL FROM` and `HELO` identities, and a receiver evaluates that record with the `check_host()` function. With this skill the agent writes and reviews SPF records, keeps them inside the DNS lookup and size limits, implements or audits a verifier, and records the result.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: publisher (a domain owner writing records), verifier (a receiving MTA or filter running `check_host()`), or mediator (a forwarder or mailing list).
- Target version: RFC 7208 (default). RFC 4408 is legacy: read it and upgrade from it, never author against it. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the RFC Editor entry for RFC 7208 for new errata, updating or obsoleting RFCs, check the IETF Datatracker for a draft revising SPF, and update the pins.
- Sending sources (publisher): every host, relay and third-party service that sends with the domain in `MAIL FROM` or `HELO`, and which domains send no mail at all.
- Identities (verifier): whether `HELO`, `MAIL FROM` or both are checked, and where in the mail flow.

## Invariants

1. **TXT only, `v=spf1` exactly.** Records are published as DNS TXT (type 16) only (§ 3.1); the SPF RR type 99 is not to be used (§ 14.1). Records that do not start with exactly `v=spf1` followed by a space or the end are discarded, so `v=spf10` is not a record (§ 4.5).
2. **One record per name.** A name MUST NOT have more than one record that selection would pick (§ 3.2). Two `v=spf1` records give `permerror` (§ 4.5).
3. **Strings concatenate without spaces.** A TXT record with several character-strings is read as one string joined with no added space (§ 3.3). Keep the DNS answer small enough for 512 octets; the guideline is under 450 octets of name plus record text (§ 3.4).
4. **At most 10 DNS-querying terms per evaluation.** `include`, `a`, `mx`, `ptr`, `exists` and `redirect` count; `all`, `ip4`, `ip6` and `exp` do not. Exceeding 10 MUST give `permerror` (§ 4.6.4), and the count is global across every `include` and `redirect` (§ 4.1).
5. **At most two void lookups.** Implementations SHOULD stop with `permerror` after more than two terms whose lookup returns NXDOMAIN or an empty answer (§ 4.6.4, § 11.1).
6. **End with `all` or `redirect`.** With no match and no `redirect`, the result is `neutral`, as if `?all` ended the record (§ 4.7). Negative determinations need `-all` or a `redirect` to a record that ends in it (§ 2.1). A `redirect` is ignored when the record has an `all` anywhere (§ 5.1, § 6.1), and terms after `all` are ignored (§ 5.1).
7. **Do not publish `ptr` or `%{p}`.** Both SHOULD NOT be published; verifiers MUST still support `ptr` (§ 5.5, § 7.3).
8. **Targets must have a record.** An `include` whose target returns `none` gives `permerror` (§ 5.2), and so does a `redirect` to a name with no record or a malformed name (§ 6.1).
9. **Modifiers once each; syntax errors are fatal.** `redirect` and `exp` appear at most once each, else `permerror`; unknown modifiers are ignored (§ 6). Any syntax error anywhere in the record gives `permerror` before evaluation (§ 4.6).
10. **Verifiers check `MAIL FROM` when `HELO` is not conclusive.** A verifier MUST check `MAIL FROM` if a `HELO` check was not done or not definitive (§ 2.4). With a null reverse-path, `MAIL FROM` is `postmaster@` plus the `HELO` domain (§ 2.4). Checking `HELO` first is RECOMMENDED (§ 2.3).
11. **`neutral` is `none`; `softfail` alone is not a reject.** `neutral` MUST be treated exactly like `none` (§ 8.2). Receivers SHOULD NOT reject on `softfail` alone (§ 8.5).
12. **SPF authorizes only `MAIL FROM` and `HELO`.** Checking other identities against `v=spf1` records is NOT RECOMMENDED without the publisher's approval (§ 2.2), and a `pass` says nothing about the `From:` header field (§ 11.2). Tie SPF to `From:` with DMARC.
13. **IDNs are A-labels.** Domain names, including those in macro expansions, are converted to A-labels before SPF uses them (§ 4.3; RFC 8616 § 4).

## Workflow

1. **Pick the version.** Use RFC 7208. If a record or implementation uses the SPF RR type or cites RFC 4408, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ New records are TXT only, and the code or documentation cites RFC 7208.
2. **Inventory senders.** List the border MTAs and services that send across the Internet with the domain in `MAIL FROM` or `HELO`; internal relays do not need listing (Appendix F). Services that use the customer's domain need authorizing in that domain's record (Appendix E). Give each sending host name its own record, and give every name that sends no mail `v=spf1 -all` (§ 10.1.2).
   -> [`references/record-syntax.md`](references/record-syntax.md)
   ✓ Every sending path maps to a mechanism, and every non-sending name has a `-all` record.
3. **Write the record.** Prefer `ip4` and `ip6` over `a`, and `a` over `mx`, unless hosts change often (§ 10.1.2). Use `include` across administrative boundaries and `redirect` within one (§ 5.2, § 6.1). End with `-all` (or `~all` while testing), and put any `redirect` last (§ 4.7, § 6.1).
   -> [`references/record-syntax.md`](references/record-syntax.md)
   ✓ The record parses against the § 12 ABNF and ends in `all` or `redirect`.
4. **Count lookups and bytes.** Walk every `include` and `redirect` and count DNS-querying terms, check that no name has two records, and size the TXT answer. Decide on flattening only with its trade-offs written down.
   -> [`references/limits-and-pitfalls.md`](references/limits-and-pitfalls.md)
   ✓ 10 or fewer DNS-querying terms in the whole tree, no void lookups from your own terms, and the answer under the § 3.4 guideline.
5. **Publish with a transition period.** Keep the old policy valid until mail sent under it has been checked (§ 2.1).
   ✓ Old and new records both authorize mail in flight during the change.
6. **Implement or audit the verifier** (verifier role). Follow `check_host()`: initial processing, TXT lookup, record selection, left-to-right evaluation, `include` and `redirect` recursion, the lookup, void and time limits, and macro expansion.
   -> [`references/evaluation.md`](references/evaluation.md)
   ✓ Each case in the § 4 and § 5 result tables gives the result the RFC specifies.
7. **Act on and record the result.** Choose local policy per result, use the SMTP reply codes RFC 7208 § 8 and RFC 7372 give, and record the result in `Received-SPF` or `Authentication-Results`.
   -> [`references/evaluation.md`](references/evaluation.md)
   ✓ Rejections use 550 or 451 with a matching enhanced code; accepted mail carries a results header that names the checked identity.
8. **Plan for mediators and DMARC.** Expect forwarded mail to fail SPF and choose a mitigation from Appendix D; hand `From:` alignment to the `dmarc` skill.
   -> [`references/limits-and-pitfalls.md`](references/limits-and-pitfalls.md)
   ✓ Forwarding paths are known, and the domain does not rely on SPF alone for `From:` protection.
9. **Upgrade** (only when asked). Follow the RFC 4408 to RFC 7208 checklist: drop the SPF RR type, apply the void lookup limit, replace `ptr` and `%{p}`, and remove `x-` key names.
   -> [`references/versions.md`](references/versions.md)
   ✓ The domain has exactly one TXT record per name, and the verifier passes the RFC 7208 limits.

## Verify before done

- [ ] Each mail-using name has exactly one TXT record that starts with `v=spf1` and no type 99 record is relied on (§ 3.1, § 3.2, § 4.5).
- [ ] The whole `include` and `redirect` tree uses 10 or fewer of `include`, `a`, `mx`, `ptr`, `exists` and `redirect` (§ 4.6.4).
- [ ] Every `include` and `redirect` target has its own SPF record (§ 5.2, § 6.1).
- [ ] The record ends in `-all`, `~all` or a `redirect`, and has no `redirect` next to an `all` (§ 4.7, § 5.1).
- [ ] No `ptr` mechanism and no `%{p}` macro is published (§ 5.5, § 7.3).
- [ ] The TXT answer stays under the § 3.4 size guideline, counting other TXT records at the same name.
- [ ] Names that send no mail publish `v=spf1 -all`; sending hosts used in `HELO` have their own record (§ 10.1.2).
- [ ] Verifiers treat `neutral` like `none`, return `permerror` on the limits, and `temperror` on DNS failures (§ 4.4, § 4.6.4, § 8.2).
- [ ] Results headers carry the identity that produced the result and no unauthenticated local-part (RFC 8601 § 2.7.2, § 4).

## Reference index

- **`references/versions.md`**: RFC 7208 and RFC 4408 with their status, updates and errata, what RFC 7208 changed, and the upgrade checklist. Load for steps 1 and 9.
- **`references/record-syntax.md`**: the record format, every mechanism, qualifier and modifier, CIDR lengths, macros, and annotated examples. Load for steps 2 and 3.
- **`references/evaluation.md`**: `check_host()` step by step, the identities, results, SMTP reply codes, `Received-SPF` and `Authentication-Results`. Load for steps 6 and 7.
- **`references/limits-and-pitfalls.md`**: the lookup, void, MX, PTR and time limits, counting a record tree, record size, flattening, forwarding and mediators, security considerations, and common mistakes. Load for steps 4 and 8.

## Related skills

- `dmarc` for tying the SPF-authenticated domain to the `From:` domain, with policies and reports: `npx skills add ScaleDockHQ/scaledock-skills --skill dmarc`.
- `dkim` for signing messages, the other authentication method DMARC builds on: `npx skills add ScaleDockHQ/scaledock-skills --skill dkim`.
- `list-unsubscribe` for the unsubscribe header fields on list and bulk mail: `npx skills add ScaleDockHQ/scaledock-skills --skill list-unsubscribe`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 7208: Sender Policy Framework (SPF) for Authorizing Use of Domains in Email, Version 1](https://www.rfc-editor.org/rfc/rfc7208): RFC (Proposed Standard, updated by RFC 7372, RFC 8553 and RFC 8616), RFC 7208, checked 2026-10-05.
- [RFC 7208 errata](https://www.rfc-editor.org/errata/rfc7208): RFC Editor errata list, 2 verified, 10 reported, 2 held for document update, 3 rejected, checked 2026-10-05.
- [RFC 4408: Sender Policy Framework (SPF) for Authorizing Use of Domains in E-Mail, Version 1](https://www.rfc-editor.org/rfc/rfc4408): RFC (Experimental, obsoleted by RFC 7208), RFC 4408, checked 2026-10-05.
- [RFC 7372: Email Authentication Status Codes](https://www.rfc-editor.org/rfc/rfc7372): RFC (Proposed Standard), RFC 7372, checked 2026-10-05.
- [RFC 8553: DNS AttrLeaf Changes: Fixing Specifications That Use Underscored Node Names](https://www.rfc-editor.org/rfc/rfc8553): RFC (Best Current Practice, BCP 222), RFC 8553, checked 2026-10-05.
- [RFC 8616: Email Authentication for Internationalized Mail](https://www.rfc-editor.org/rfc/rfc8616): RFC (Proposed Standard), RFC 8616, checked 2026-10-05.
- [RFC 8601: Message Header Field for Indicating Message Authentication Status](https://www.rfc-editor.org/rfc/rfc8601): RFC (Proposed Standard), RFC 8601, checked 2026-10-05.
