---
name: http-cookies
description: >-
  HTTP cookies (RFC 6265, State Management): set and read cookies safely from a server with Set-Cookie and Cookie, choosing Expires, Max-Age, Domain, Path, Secure, HttpOnly and SameSite, the __Secure- and __Host- name prefixes, sizes and lifetimes. RFC 6265 is the current line; RFC 6265bis (draft-ietf-httpbis-rfc6265bis-22, in the RFC Editor queue) is a preview to build on now, because it defines SameSite=Strict/Lax/None, Lax-by-default, the prefixes, the 400-day lifetime cap and the 4096-octet limit. RFC 2965 and RFC 2109 (Set-Cookie2, Cookie2, $Version) are legacy. Use when designing session cookies, writing or reviewing Set-Cookie headers, parsing a Cookie header, deleting a cookie, scoping a cookie to a subdomain, debugging a cookie that is not sent or not stored, or hardening cookies against CSRF, session fixation, cookie tossing and subdomain attacks. Triggers: Set-Cookie, SameSite, cross-site cookie, third-party cookie, HttpOnly, Secure flag, __Host-, cookie prefix, cookie size limit, cookie expiry.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# HTTP cookies

The IETF HTTP State Management Mechanism defines the `Set-Cookie` response header field, which stores a name-value pair at the user agent, and the `Cookie` request header field, which returns it. RFC 6265 is the published standard; draft-ietf-httpbis-rfc6265bis will obsolete it and adds SameSite, the cookie name prefixes and stricter limits. With this skill the agent writes and reviews server-side cookie handling: the exact `Set-Cookie` strings, how to read `Cookie`, and the security posture of each cookie.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Section numbers without a prefix are RFC 6265bis-22. "6265 §" marks RFC 6265.

## Inputs (fill in, or ask before starting)

- Role: cookie producer (a server, framework or API that sends `Set-Cookie`), cookie reader (a server that parses `Cookie`), or both. User agent implementers follow § 5 of the draft directly; this skill targets servers (§ 3.2.1).
- Target version: RFC 6265 is current, and every cookie must stay valid under it. RFC 6265bis is a preview (posture: build): emit its SameSite attribute and name prefixes now, because browsers implement them and RFC 6265 user agents ignore unrecognized attributes (6265 § 4.1.2). RFC 2965 and RFC 2109 are legacy: read and upgrade from them, never emit `Set-Cookie2` or `$Version`. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Deployment: the hosts that set and read each cookie, whether every one of them is HTTPS-only, and whether any sibling subdomain is run by a less trusted party.
- Cross-site needs: does any cookie have to be sent in an iframe, a cross-site `fetch`, or a cross-site `POST` (single sign-on, embedded widgets)?
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the datatracker for a new draft revision or a `became_rfc` relation, and update the pins.

## Invariants

1. **One cookie per `Set-Cookie` field.** Never fold several `Set-Cookie` fields into one with commas (6265 § 3: SHOULD NOT; § 3: MUST NOT), and send at most one `Set-Cookie` per cookie-name in a response (6265 § 4.1.1; § 4.1.1).
2. **Follow the server grammar.** `cookie-name` is a non-empty token and `cookie-value` uses only `cookie-octet` (no whitespace, `"`, `,`, `;` or `\`), optionally inside double quotes that stay part of the value (6265 § 4.1.1; § 4.1.1). Encode arbitrary data, for example with Base64 (6265 § 4.1.1).
3. **No duplicate attributes** in one `set-cookie-string` (6265 § 4.1.1: SHOULD NOT; § 4.1.1: MUST NOT).
4. **Dates are `IMF-fixdate`** with a four-digit year, such as `Wed, 09 Jun 2027 10:18:14 GMT` (6265 § 4.1.1 `rfc1123-date`; § 4.1.1). `Max-Age` wins over `Expires` (6265 § 4.1.2.2).
5. **`Secure` on every cookie served over HTTPS** (6265 § 8.3; § 8.3). Without it the secure channel's protection is "largely moot".
6. **`SameSite=None` requires `Secure`.** User agents drop a `SameSite=None` cookie without it (§ 5.7 step 19).
7. **Prefixes carry their conditions.** `__Secure-` needs `Secure`; `__Host-` needs `Secure`, `Path=/` and no `Domain`, and is set from a secure origin (§ 4.1.3, § 5.7 steps 20 and 21).
8. **Size.** The name plus the value must be at most 4096 octets, and each attribute value at most 1024 octets, or the user agent drops it (§ 5.6, § 5.7 step 4). Keep the whole `Cookie` header under the server's field limit, often 8192 octets (§ 4.2.1).
9. **Delete with the same scope.** A deletion `Set-Cookie` repeats the original name, `Path` and `Domain` and sets `Expires` to a date in the past (§ 3.1, § 4.1.2). `Max-Age=0` also expires the cookie at the user agent (§ 5.6.2), but the server grammar only allows a `Max-Age` that starts with 1 to 9 (§ 4.1.1).
10. **The `Cookie` header carries names and values only.** Do not infer attributes, expiry or origin from it, and do not rely on the order of cookies, even two with the same name (6265 § 4.2.2; § 4.2.2). Tolerate several `Cookie` fields in one request (§ 4.2.1: MUST).
11. **Cookies can disappear.** Degrade gracefully when one is missing, because user agents evict at any time (6265 § 6.1, § 8.6; § 6.1, § 8.6).
12. **Cookies are not an isolation boundary** between ports, schemes, paths or sibling subdomains (6265 § 8.5, § 8.6; § 8.5, § 8.6). Do not share a host, or a parent domain cookie, with a mutually distrusting service.
13. **Store a session identifier, not session data,** and avoid session fixation (6265 § 8.4; § 8.4).

## Workflow

1. **Pick the version.** Target RFC 6265 plus the RFC 6265bis server profile, which is a strict subset of what RFC 6265 user agents accept. Upgrade any `Set-Cookie2` or `$Version` code.
   -> [`references/versions.md`](references/versions.md)
   ✓ No legacy header is emitted, and every cookie parses under both RFC 6265 and RFC 6265bis.
2. **Inventory cookies.** For each cookie, record its purpose, the hosts and paths that need it, whether script needs to read it, whether it must travel cross-site, and how long it must live.
   -> [`references/storage-and-limits.md`](references/storage-and-limits.md)
   ✓ Every cookie has an owner, a scope and a lifetime, and the set is as few and as small as possible (§ 6.1).
3. **Choose the scope.** Prefer host-only (no `Domain`) and `Path=/`; add `Domain` only when sibling hosts must receive the cookie, knowing every subdomain can then read and overwrite it (§ 4.1.2.3, § 8.6). `Path` is not a security boundary (§ 4.1.2.4).
   -> [`references/set-cookie-attributes.md`](references/set-cookie-attributes.md)
   ✓ Every `Domain` is justified, and no security cookie depends on `Path` for isolation.
4. **Choose the protections.** `Secure` on all HTTPS cookies; `HttpOnly` unless script must read the value; an explicit `SameSite` (`Strict` or `Lax` by default, `None` with `Secure` only for cross-site use); `__Host-` for session cookies, or `__Secure-` when `Domain` is needed.
   -> [`references/same-site-and-prefixes.md`](references/same-site-and-prefixes.md)
   ✓ Each cookie's flags match its inventory row, and every prefixed cookie meets its prefix rules.
5. **Choose the lifetime.** Session cookie (no `Expires` or `Max-Age`) or a purpose-based `Max-Age`; nothing past 400 days, which user agents cap anyway (§ 5.5, § 7.4).
   -> [`references/storage-and-limits.md`](references/storage-and-limits.md)
   ✓ No cookie asks for more than 400 days, and none relies on being kept until expiry.
6. **Serialize `Set-Cookie`.** Build the string with a structured API rather than string concatenation (§ 6.2), one field per cookie.
   -> [`references/set-cookie-attributes.md`](references/set-cookie-attributes.md)
   ✓ Each header matches the § 4.1.1 grammar, with no repeated attribute and no repeated name in one response.
7. **Read `Cookie`.** Split on `"; "`, accept several `Cookie` fields, treat names case-sensitively, and handle duplicate names without relying on order.
   -> [`references/set-cookie-attributes.md`](references/set-cookie-attributes.md)
   ✓ The parser handles a missing cookie, a duplicate name and a split header.
8. **Harden.** Check sessions against fixation, state-changing endpoints against CSRF with a defense beyond SameSite, and sibling subdomains against cookie tossing.
   -> [`references/security.md`](references/security.md)
   ✓ Every item in the security checklist is answered.
9. **Upgrade** (only when asked). Follow the path in versions.md: RFC 2109 or RFC 2965 to RFC 6265, then RFC 6265 to the RFC 6265bis profile.
   -> [`references/versions.md`](references/versions.md)
   ✓ The same cookies reach the same hosts and paths, and no new cookie is rejected by a user agent.

## Verify before done

- [ ] Every `Set-Cookie` matches the § 4.1.1 grammar: non-empty token name, `cookie-octet` value, no repeated attribute, one field per cookie.
- [ ] Every cookie set over HTTPS has `Secure`; every `SameSite=None` cookie has `Secure`.
- [ ] Every cookie has an explicit `SameSite` value chosen for its cross-site needs, not the user agent default.
- [ ] Every `__Host-` cookie has `Secure; Path=/` and no `Domain`; every `__Secure-` cookie has `Secure`.
- [ ] Session and authentication cookies are `HttpOnly`, hold an opaque identifier, and are re-issued when the session's privilege changes.
- [ ] No cookie requests a lifetime above 400 days; name plus value stay under 4096 octets; attribute values under 1024.
- [ ] Deletions repeat the original `Domain` and `Path`.
- [ ] The `Cookie` parser tolerates several fields, duplicate names and missing cookies.
- [ ] Nothing emits `Set-Cookie2`, `Cookie2`, `$Version`, `Comment`, `CommentURL`, `Discard` or `Port`.

## Reference index

- **`references/versions.md`**: RFC 6265, RFC 6265bis, RFC 2965 and RFC 2109 with status, what changed, the upgrade steps and the preview's posture. Load for steps 1 and 9.
- **`references/set-cookie-attributes.md`**: the `Set-Cookie` and `Cookie` grammars, each attribute with server rules and user agent handling, deletion and examples. Load for steps 3, 6 and 7.
- **`references/same-site-and-prefixes.md`**: same-site and cross-site requests, `Strict`, `Lax`, `None`, Lax-by-default and Lax-allowing-unsafe, and the `__Secure-` and `__Host-` prefixes. Load for step 4.
- **`references/storage-and-limits.md`**: the user agent's storage model, replacement and eviction, size and count limits, the 400-day cap, session cookies and the public suffix list. Load for steps 2 and 5.
- **`references/security.md`**: ambient authority and CSRF, clear text, session identifiers and fixation, weak confidentiality and integrity, subdomain attacks, SameSite caveats and privacy. Load for step 8.

## Related skills

- `http-semantics` for header field syntax, `IMF-fixdate` and safe methods: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.
- `hsts` to stop the HTTP downgrade that lets an active attacker read or inject cookies: `npx skills add ScaleDockHQ/scaledock-skills --skill hsts`.
- `content-security-policy` to reduce the cross-site scripting that defeats SameSite and reads non-`HttpOnly` cookies: `npx skills add ScaleDockHQ/scaledock-skills --skill content-security-policy`.
- `owasp-asvs` for session management and CSRF verification requirements: `npx skills add ScaleDockHQ/scaledock-skills --skill owasp-asvs`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 6265: HTTP State Management Mechanism](https://www.rfc-editor.org/rfc/rfc6265.html): RFC (Proposed Standard), RFC 6265 (April 2011), checked 2026-10-05.
- [draft-ietf-httpbis-rfc6265bis-22: Cookies: HTTP State Management Mechanism](https://www.ietf.org/archive/id/draft-ietf-httpbis-rfc6265bis-22.txt): Internet-Draft (HTTPBIS WG, intended Proposed Standard), revision 22 (1 December 2025), checked 2026-10-05.
- [draft-ietf-httpbis-rfc6265bis datatracker entry](https://datatracker.ietf.org/doc/draft-ietf-httpbis-rfc6265bis/): IESG state RFC Ed Queue, no `became_rfc` relation, latest revision 22, checked 2026-10-05.
- [RFC 2965: HTTP State Management Mechanism](https://www.rfc-editor.org/rfc/rfc2965.txt): RFC (Historic, obsoleted by RFC 6265), RFC 2965 (October 2000), checked 2026-10-05.
- [RFC 2109: HTTP State Management Mechanism](https://www.rfc-editor.org/rfc/rfc2109.txt): RFC (Historic, obsoleted by RFC 2965), RFC 2109 (February 1997), checked 2026-10-05.
- [HTML Living Standard: sites and same site](https://html.spec.whatwg.org/multipage/browsers.html#same-site): WHATWG Living Standard, the `[SAMESITE]` reference of RFC 6265bis, checked 2026-10-05.
