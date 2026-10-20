---
name: gpc
description: >-
  Global Privacy Control (GPC) WD 2026-09-24: honor, send and detect the W3C
  Sec-GPC: 1 do-not-sell-or-share signal, navigator.globalPrivacyControl and the
  /.well-known/gpc.json support resource. Targets GPC Working Draft 2026-09-24 (posture
  build; the Editor's Draft has the same text); the pre-W3C community draft (2020 to 2024)
  is legacy. Use when a site, server, CDN, proxy or analytics or ad tag must read GPC,
  when a browser, extension or test harness must send it, when publishing or validating
  gpc.json (gpc, lastUpdate), when wiring opt-out of sale, sharing or cross-context targeted
  advertising to the signal, or when testing with the WebDriver privacy commands. Covers the
  spec's own legal-effects text (CCPA, Colorado and other US state universal opt-out
  mechanisms, GDPR Articles 7 and 21) without legal advice. Triggers: GPC, Sec-GPC,
  globalPrivacyControl, gpcAtNavigation, gpc.json, global privacy control, opt-out
  preference signal, universal opt-out mechanism, do not sell or share, DNT successor.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Global Privacy Control

Global Privacy Control (GPC), published by the W3C Privacy Working Group, defines a signal that conveys a person's request that websites not sell or share their personal information with third parties or use it for cross-context targeted advertising (Abstract, § 2). The signal travels as the `Sec-GPC: 1` request header and as `navigator.globalPrivacyControl`, and an origin can state its support at `/.well-known/gpc.json`. With this skill the agent reads and honors the signal on servers and in page scripts, sends it from a user agent or test harness, and publishes or validates the support resource.

Draft posture: build (GPC Working Draft 2026-09-24, `WD-gpc-20260924`). The specification is a Working Draft on the Recommendation track; implement the pinned revision's shapes.

The legal-effects section (§ 5) is non-normative. Whether a GPC signal is legally binding, and what a recipient must do, depends on the jurisdiction, the applicable law and any agreement with the person (§ 5). This skill reports what the spec says and gives no legal advice; send legal questions to counsel.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Bare section numbers (§ 3.3) refer to the pinned Working Draft. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: server or site (reads the header or property and honors it), user agent or extension (sends it), intermediary (CDN or proxy that forwards it), support-resource publisher, or tester.
- Target version: GPC Working Draft 2026-09-24 (default, posture build: implement it). GPC community draft (2020 to 2024) is legacy: read it and upgrade from it, never author against it. No preview exists, because the Editor's Draft has the same text. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- What the signal controls in this system: the sale or sharing of personal data with third parties and cross-context ad targeting (§ 2). List the processing and the third parties (tags, pixels, data feeds) it touches.
- Jurisdictions served: needed only to decide, with counsel, what honoring requires; the spec does not decide it (§ 5).
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the W3C history page for a newer Working Draft, Candidate Recommendation or Recommendation, compare the Editor's Draft with the latest Working Draft, and update the pins.

## Invariants

1. **The header is exactly `Sec-GPC: 1`.** The field value grammar is the single character `"1"`, with no extension mechanism (§ 3.3, § 3.3.1). Compare the value for string equality; do not parse it.
2. **A user agent sends it only when the cached preference is on.** It MUST NOT send `Sec-GPC` when the top-level browsing context's `gpcAtNavigation` is false, MUST send exactly `1` when it is true, MUST NOT send more than one, and MUST NOT put it in a trailer (§ 3.3).
3. **The preference is cached per top-level navigation.** `gpcAtNavigation` MUST reflect the preference when the top-level browsing context's active document began loading; a change takes effect at the next navigation (§ 3.2). The user agent SHOULD offer to reload inconsistent tabs (§ 3.2).
4. **Servers ignore anything but `1`.** A server MUST process a request as if `Sec-GPC` were absent unless the value is exactly `1`; with several `Sec-GPC` fields, it MUST treat the request as carrying `1` if at least one is exactly `1`, and as carrying none otherwise (§ 3.3).
5. **Intermediaries never strip a `1`.** They MUST NOT remove `Sec-GPC: 1`, MAY remove other values, and MAY insert `Sec-GPC: 1` when they have reason to believe the person has the preference (§ 3.3).
6. **The script property mirrors the header.** `globalPrivacyControl` is a read-only boolean on `Navigator` and `WorkerNavigator`; its value MUST be the top-level browsing context's `gpcAtNavigation`, so it is true exactly when the header would be sent (§ 3.4).
7. **`/.well-known/gpc.json` is an `application/json` object.** Otherwise the origin's support is unknown (§ 4, § 4.1). Unknown members MUST be ignored (§ 4.1).
8. **`gpc` is a boolean.** `true` means the server intends to abide by GPC requests at least to the extent legally obligated, `false` means it does not, and any other value means support is unknown (§ 4.1).
9. **`lastUpdate` is an RFC 3339 full-date or date-time.** It records when the statement was made; an invalid value makes the date unknown (§ 4.1).
10. **The support resource does not report per-visitor handling.** It conveys the origin's awareness of and support for GPC, not whether this user agent's requests are honored (§ 4).
11. **The signal is narrow.** It is not meant to invoke every privacy right: not deletion, and not data collection or ad targeting within the same context (§ 1, § 5.2).

## Workflow

1. **Pick the version.** Use GPC Working Draft 2026-09-24. If code or a `gpc.json` follows the community draft (a `version` member, a `Navigator`-only property, no navigation cache), plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target is recorded as `WD-gpc-20260924`, and nothing emits the legacy `version` member.
2. **Map the signal to processing.** Decide which sale, sharing and cross-context ad targeting the signal stops in this system, and which processing stays out of scope (§ 2, § 5.2). Record how the site handles conflicts with choices the person made directly (§ 5.2).
   -> [`references/signal.md`](references/signal.md)
   ✓ Every third-party flow is marked as stopped by GPC or out of scope, and the disclosure the spec recommends is drafted for counsel.
3. **Read the signal on the server.** Apply the exact-match and multiple-field rules, and treat the signal as a standing preference rather than a fresh opt-out per request (§ 3.3, Appendix A).
   -> [`references/implementation.md`](references/implementation.md)
   ✓ `Sec-GPC: 1` turns the preference on; `Sec-GPC: 0`, `Sec-GPC: true` and an absent field do not; repeated fields count as `1` when at least one is exactly `1`.
4. **Read the signal in the client.** Check `navigator.globalPrivacyControl` in pages and workers before loading or configuring third-party tags (§ 3.4).
   -> [`references/implementation.md`](references/implementation.md)
   ✓ Tags that sell or share data are gated on the property, and code treats `undefined` (an older user agent) as "not set".
5. **Keep intermediaries transparent.** Configure CDNs, proxies and edge functions to forward `Sec-GPC: 1` (§ 3.3).
   -> [`references/implementation.md`](references/implementation.md)
   ✓ A request sent with `Sec-GPC: 1` reaches the origin with the field intact.
6. **Publish the support resource** (optional, § 4). Serve `/.well-known/gpc.json` as `application/json` with `gpc` and `lastUpdate`, or redirect to it.
   -> [`references/well-known-resource.md`](references/well-known-resource.md)
   ✓ The response parses as a JSON object, `gpc` is a boolean, `lastUpdate` is a valid RFC 3339 date, and the statement matches what the origin actually does.
7. **Send and test the signal** (user agents, extensions, test suites). Cache the preference per top-level navigation, send the header and property consistently, and drive tests with the WebDriver commands (§ 3.2 to § 3.4, § 8).
   -> [`references/implementation.md`](references/implementation.md)
   ✓ After `POST /session/{session id}/privacy` with `{"gpc": true}` and a navigation, the server sees `Sec-GPC: 1` and the page sees `true`.
8. **Upgrade** (only when asked). Follow the community-draft checklist: replace `version` with `lastUpdate`, read the property from workers too, and apply the navigation cache and server rules.
   -> [`references/versions.md`](references/versions.md)
   ✓ `gpc.json` and the header handling pass the checks in [Verify before done](#verify-before-done).

## Verify before done

- [ ] Header checks compare the value to the exact string `1` and follow the repeated-field rule (§ 3.3).
- [ ] No user-agent code emits `Sec-GPC` with any other value, twice, or in a trailer (§ 3.3).
- [ ] `navigator.globalPrivacyControl` and the header agree for the same navigation (§ 3.4).
- [ ] Intermediaries forward `Sec-GPC: 1` unchanged (§ 3.3).
- [ ] `/.well-known/gpc.json`, if served, is `application/json`, a JSON object, with boolean `gpc` and RFC 3339 `lastUpdate` (§ 4.1).
- [ ] The handling does not claim GPC covers deletion or same-context processing (§ 1, § 5.2).
- [ ] Legal conclusions are labelled as jurisdiction-dependent and not taken from this skill (§ 5).
- [ ] Nothing emits the community draft's `version` member.

## Reference index

- **`references/versions.md`**: the Working Draft and the legacy community draft, the W3C publication history, what changed, the upgrade checklist, and why there is no preview. Load for steps 1 and 8.
- **`references/signal.md`**: definitions, the header grammar and rules, preference caching, the JavaScript property and its worker and iframe exposure, privacy considerations, and the spec's legal-effects text. Load for steps 2 to 4.
- **`references/well-known-resource.md`**: `/.well-known/gpc.json`, its members, how a consumer decides "unknown", and examples. Load for step 6.
- **`references/implementation.md`**: server, client, intermediary and user-agent patterns with TypeScript, the WebDriver commands, and common mistakes. Load for steps 3 to 5 and 7.

## Related skills

- `http-cookies` for the cookies that GPC-aware consent and ad tags set or skip: `npx skills add ScaleDockHQ/scaledock-skills --skill http-cookies`.
- `content-security-policy` for restricting which third-party scripts a page may load once the signal is honored: `npx skills add ScaleDockHQ/scaledock-skills --skill content-security-policy`.
- `aipref` for expressing a site's preferences about AI use of its content, a separate signal from GPC: `npx skills add ScaleDockHQ/scaledock-skills --skill aipref`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Global Privacy Control (GPC), latest published version](https://www.w3.org/TR/gpc/): W3C Working Draft (Privacy WG, Recommendation track), WD-gpc-20260924, checked 2026-10-05.
- [Global Privacy Control (GPC), W3C Working Draft 24 September 2026](https://www.w3.org/TR/2026/WD-gpc-20260924/): W3C Working Draft, WD-gpc-20260924, checked 2026-10-05.
- [Global Privacy Control (GPC), Editor's Draft](https://w3c.github.io/gpc/): Editor's Draft, commit 09013ac (2026-09-24), same text as the Working Draft, checked 2026-10-05.
- [W3C history of the GPC specification](https://www.w3.org/standards/history/gpc/): publication history, Working Drafts WD-gpc-20241121 to WD-gpc-20260924, checked 2026-10-05.
- [w3c/gpc GitHub repository](https://github.com/w3c/gpc): specification repository, main at 09013ac, checked 2026-10-05.
- [GPC community draft, last pre-W3C revision](https://github.com/w3c/gpc/blob/90272664a01b925041eea0222a9f7c2ea194954f/index.html): unofficial draft, superseded, commit 9027266 (2024-03-21), checked 2026-10-05.
- [GPC community draft, 2020 revision](https://github.com/w3c/gpc/blob/e60ad1cbc4aad738e8630c0d97fbecf392b453cc/index.html): unofficial draft, superseded, commit e60ad1c (2020-11-14), checked 2026-10-05.
- [Global Privacy Control project page](https://globalprivacycontrol.org/): project website (non-normative), checked 2026-10-05.
