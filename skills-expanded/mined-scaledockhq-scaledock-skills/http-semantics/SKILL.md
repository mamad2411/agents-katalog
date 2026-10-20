---
name: http-semantics
description: >-
  HTTP Semantics RFC 9110, Caching RFC 9111 and RFC 9112 HTTP/1.1: methods, status codes,
  conditional requests, caching and extension fields. Covers RFC 9110 and RFC
  9111, RFC 10008 QUERY, RFC 9651 Structured Fields, RFC 8288 Web Linking, RFC
  9745 Deprecation, RFC 8594 Sunset, RFC 9727 api-catalog, RFC 7240 Prefer,
  RFC 7838 Alt-Svc, RFC 8297 Early Hints, RFC 8942 Client Hints, RFC 9211
  Cache-Status, RFC 9209 Proxy-Status, RFC 9213 Targeted Cache-Control, RFC
  9218 Priority, RFC 5789 PATCH, RFC 7578 multipart/form-data, RFC 9652
  Link-Template and RFC 9842 Compression Dictionary Transport. Tracks
  Idempotency-Key draft-07 and Resumable Uploads draft-12. Use when designing
  or reviewing an HTTP API. Upgrades from RFC 7230-7235.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.2.0"
  kind: standard
---

# HTTP Semantics and Caching

RFC 9110 (HTTP Semantics) and RFC 9111 (HTTP Caching), published by the IETF as Internet Standards, define what HTTP methods, status codes, header fields, conditional requests, content negotiation, range requests and caches mean, independent of the HTTP version. With this skill the agent designs and reviews HTTP APIs and servers that use them correctly, together with the extension fields APIs commonly add: QUERY, Structured Fields, Link, Deprecation, Sunset, api-catalog and Prefer.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: origin server or API, client, intermediary or cache, or author of a new header field.
- Target version, per family (see [`references/versions.md`](references/versions.md)):
  - Core: RFC 9110 and RFC 9111 (current, default). RFC 9112 HTTP/1.1 is current for message syntax and connection management; it obsoletes portions of RFC 7230. RFC 7230-7235 is legacy: read it and upgrade from it, never author against it. Idempotency-Key draft-07 is a preview (posture: track): do not add it to new APIs.
  - Query: RFC 10008 QUERY (current).
  - Structured fields: RFC 9651 Structured Fields (current). RFC 8941 Structured Fields is legacy, kept only for fields already defined against it.
  - Lifecycle and discovery: RFC 8288 Web Linking, RFC 9745 Deprecation, RFC 8594 Sunset, RFC 9727 api-catalog and RFC 7240 Prefer (each current, the only line of its family).
  - Extensions, each the current line of its family: RFC 7838 Alt-Svc, RFC 8297 Early Hints, RFC 8942 Client Hints, RFC 9211 Cache-Status, RFC 9209 Proxy-Status, RFC 9213 Targeted Cache-Control, RFC 9218 Priority, RFC 5789 PATCH, RFC 7578 multipart/form-data, RFC 9652 Link-Template and RFC 9842 Compression Dictionary Transport. Resumable Uploads draft-12 is current with posture track: do not emit it.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check each RFC's RFC Editor entry for errata and "obsoleted by" or "updated by", check the datatracker for a new Idempotency-Key revision or RFC, and update the pins.
- Caches in the path: browser only, or shared caches (CDN, reverse proxy) too. This decides `private`, `s-maxage` and Vary.
- Authentication: whether requests carry Authorization. This decides what shared caches may store.
- Resources and operations: the URIs, which operations change state, and which can be retried.

## Invariants

1. **Safe methods stay safe.** GET, HEAD, OPTIONS, TRACE and QUERY must not be used to trigger requested state changes; an unsafe action reachable through a safe method MUST be disabled (RFC 9110 § 9.2.1; RFC 10008 § 2).
2. **Only idempotent requests are retried automatically.** A client SHOULD NOT and a proxy MUST NOT automatically retry a non-idempotent request (RFC 9110 § 9.2.2).
3. **Status codes carry their required fields.** 405 MUST carry Allow; 401 MUST carry WWW-Authenticate; 426 MUST carry Upgrade; a PUT that creates MUST answer 201 and one that modifies MUST answer 200 or 204 (RFC 9110 § 15.5.6, § 15.5.2, § 15.5.22, § 9.3.4).
4. **Entity tags are marked and compared correctly.** A tag that is not strong MUST be marked `W/`; If-Match uses strong comparison and If-None-Match weak comparison (RFC 9110 § 8.8.3, § 13.1.1, § 13.1.2).
5. **A false precondition stops the method.** The server MUST NOT perform the method; it answers 412, or 304 for a false If-None-Match or If-Modified-Since on GET and HEAD, evaluated in the § 13.2.2 order, and only after the checks that would give a non-2xx, non-412 response (RFC 9110 § 13.1, § 13.2).
6. **304 and 206 repeat the 200's metadata.** They MUST include the Date, ETag, Vary, Content-Location, Cache-Control and Expires a 200 would have had; a single-part 206 MUST carry Content-Range, and a multipart one MUST NOT carry it at the top level (RFC 9110 § 15.4.5, § 15.3.7).
7. **Caches obey response directives.** `no-store` is never stored; `private` is not stored by shared caches; a shared cache reuses responses to Authorization requests only with `public`, `s-maxage` or `must-revalidate`; caches MUST ignore unknown directives (RFC 9111 § 3, § 3.5, § 5.2.2, § 5.2.3).
8. **Unsafe requests invalidate.** A cache MUST invalidate the target URI after a non-error response to an unsafe method, and MUST NOT invalidate Location or Content-Location URIs of another origin (RFC 9111 § 4.4).
9. **Directive arguments use the defined form.** `max-age`, `s-maxage`, `max-stale` and `min-fresh` MUST NOT be sent quoted (RFC 9111 § 5.2.1, § 5.2.2).
10. **QUERY content is typed and part of the cache key.** A server MUST fail a QUERY with a missing or inconsistent Content-Type; caches MUST include the request content in the cache key (RFC 10008 § 2, § 2.7).
11. **Structured Fields fail closed.** On a parse failure the whole field is ignored, or the message treated as malformed; a field defined against RFC 8941 never carries RFC 9651-only types (RFC 9651 § 4.2, § 2.4).
12. **Link has exactly one rel.** `rel` MUST be present once per link-value, and relative targets resolve against the link context, not a base in the content (RFC 8288 § 3.3, § 3.1).
13. **Deprecation precedes Sunset.** Deprecation is a Structured Date, and the Sunset time MUST NOT be earlier than it (RFC 9745 § 2.1, § 4).
14. **Preferences are optional.** A server MUST ignore preferences it does not support instead of failing, and MUST send `Vary: Prefer` when a preference can change a cacheable response (RFC 7240 § 2).

## Workflow

1. **Pick the version.** Use the current line of each family. If documentation or code cites RFC 7230-7235 or RFC 8941, plan the upgrade (step 10). Treat Idempotency-Key as track.
   -> [`references/versions.md`](references/versions.md)
   ✓ New documentation cites RFC 9110, RFC 9111 and the current extension RFCs; nothing legacy is authored; Idempotency-Key is only used where it already exists or the user requires it.
2. **Choose methods.** Map each operation to a method by safety and idempotency: GET for reads, QUERY for reads with a request body, PUT for client-addressed replacement, POST for server-addressed creation or processing, DELETE for removal.
   -> [`references/methods-and-status.md`](references/methods-and-status.md)
   ✓ No safe method changes state; no GET or DELETE relies on request content; every method a resource supports is listed in Allow.
3. **Map outcomes to status codes and fields.** Pick the status code for every success and failure, with Location, Content-Location, Allow and Retry-After where they apply. Use the `problem-details` skill for error bodies.
   -> [`references/methods-and-status.md`](references/methods-and-status.md)
   ✓ Each response meets its section's requirements (201 with Location, 405 with Allow, 401 with WWW-Authenticate), and 422 versus 400 versus 415 follows § 15.5.
4. **Add validators and conditional requests.** Send strong ETags and Last-Modified on representations, accept If-None-Match on GET, and require If-Match for updates that must not overwrite each other.
   -> [`references/conditional-and-range.md`](references/conditional-and-range.md)
   ✓ A stale If-Match gets 412 with no change applied; a matching If-None-Match on GET gets 304 with the 200's metadata; `If-None-Match: *` on PUT prevents overwrite.
5. **Add range support** (only for large or resumable representations). Advertise `Accept-Ranges: bytes`, answer 206 and 416 correctly, and honour If-Range.
   -> [`references/conditional-and-range.md`](references/conditional-and-range.md)
   ✓ Single and multipart 206 responses carry the right Content-Range; unsatisfiable ranges get 416 with `bytes */length`.
6. **Negotiate and set Vary.** Decide which request fields select the representation and list them in Vary.
   -> [`references/caching.md`](references/caching.md)
   ✓ Every cacheable negotiated response has Vary; 406 or a default is a deliberate choice; Accept-Charset is not relied on.
7. **Set the caching policy.** Give every response an explicit Cache-Control that matches who may store it and for how long.
   -> [`references/caching.md`](references/caching.md)
   ✓ Per-user responses are `private` or `no-store`; shared-cache lifetimes use `s-maxage`; no API response relies on heuristic freshness by accident.
8. **Define new header fields as Structured Fields.** Name them per RFC 9110 § 16.3.2 and define them as a List, Dictionary or Item per RFC 9651.
   -> [`references/structured-fields.md`](references/structured-fields.md)
   ✓ Each new field names RFC 9651, its top-level type, its constraints and its failure handling, and has no `X-` prefix.
9. **Add lifecycle and discovery fields.** Use Link for relations, Deprecation and Sunset for retirement, api-catalog for discovery, and Prefer for optional behaviour. Use the `ratelimit-headers` skill for quota fields.
   -> [`references/api-lifecycle-fields.md`](references/api-lifecycle-fields.md)
   ✓ Deprecation is a Structured Date, Sunset is an HTTP-date in GMT no earlier than it, `/.well-known/api-catalog` serves `application/linkset+json`, and Prefer-dependent responses carry `Vary: Prefer`.
10. **Upgrade** (only when asked). Follow the upgrade section for each family, from RFC 7230-7235 to RFC 9110 and RFC 9111, and from RFC 8941 to RFC 9651; for POST-based queries, follow the QUERY adoption steps.
    -> [`references/versions.md`](references/versions.md)
    ✓ The upgraded API cites the current RFCs, uses the renamed terms and status phrases, and behaves the same on the wire.

## Verify before done

- [ ] Every method's use matches its safety and idempotency (RFC 9110 § 9.2; RFC 10008 § 2).
- [ ] Every 201 has Location (or the target is the new resource), every 405 has Allow, every 401 has WWW-Authenticate (RFC 9110 § 15.3.2, § 15.5.6, § 15.5.2).
- [ ] ETags are quoted, weak ones carry `W/`, and successful PUT responses only carry validators for content stored unchanged (RFC 9110 § 8.8.3, § 9.3.4).
- [ ] Preconditions are evaluated in the § 13.2.2 order and answer 412 or 304 as § 13.1 requires.
- [ ] Every 304 and 206 repeats the 200's Date, ETag, Vary, Content-Location, Cache-Control and Expires (RFC 9110 § 15.4.5, § 15.3.7).
- [ ] Every response a shared cache could see has explicit Cache-Control, and responses to authenticated requests are not shared unless intended (RFC 9111 § 3.5, § 5.2.2).
- [ ] Directive arguments for `max-age` and `s-maxage` are unquoted; `no-cache` and `private` field lists are quoted (RFC 9111 § 5.2.2).
- [ ] New fields are Structured Fields with a documented type, and none is prefixed `X-` (RFC 9651 § 2; RFC 9110 § 16.3.2.1).
- [ ] Sunset is not earlier than Deprecation, and both are hints that do not change behaviour (RFC 9745 § 4, § 5).
- [ ] Nothing from the Idempotency-Key preview is added to a new API unless the user asked for it, and any use is labelled as an expired draft.

## Reference index

- **`references/versions.md`**: every version line per family with status and posture, which to use, what changed, upgrade steps (RFC 7230-7235, RFC 8941, POST to QUERY) and the Idempotency-Key preview. Load for steps 1 and 10.
- **`references/methods-and-status.md`**: method properties, GET to TRACE and QUERY, Allow, Location, Content-Location, Retry-After, status code rules, and new field naming. Load for steps 2, 3 and 8.
- **`references/conditional-and-range.md`**: validators, ETag comparison, If-Match to If-Range, evaluation order, lost updates, 304, 412, Range, 206, 416 and partial PUT. Load for steps 4 and 5.
- **`references/caching.md`**: content negotiation and Vary, storage and reuse, freshness and age, validation, invalidation, every Cache-Control directive, stale extensions, recipes and security. Load for steps 6 and 7.
- **`references/structured-fields.md`**: defining fields, every type with limits, parsing, serialising and security. Load for step 8.
- **`references/api-lifecycle-fields.md`**: Link, Deprecation, Sunset, api-catalog, Prefer and the Idempotency-Key preview. Load for step 9.

## Related skills

- `problem-details` for `application/problem+json` error bodies on 4xx and 5xx responses: `npx skills add ScaleDockHQ/scaledock-skills --skill problem-details`.
- `ratelimit-headers` for RateLimit and RateLimit-Policy fields with 429 and Retry-After: `npx skills add ScaleDockHQ/scaledock-skills --skill ratelimit-headers`.
- `openapi` for describing these methods, status codes and headers in an OpenAPI document: `npx skills add ScaleDockHQ/scaledock-skills --skill openapi`.
- `http-cookies`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill http-cookies`
- `hsts`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill hsts`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): RFC (Internet Standard, STD 97), RFC 9110, checked 2026-10-05.
- [RFC 9111: HTTP Caching](https://www.rfc-editor.org/rfc/rfc9111): RFC (Internet Standard, STD 98), RFC 9111, checked 2026-10-05.
- [RFC 9112: HTTP/1.1](https://www.rfc-editor.org/rfc/rfc9112): RFC (Internet Standard, STD 99, updated by RFC 9931), RFC 9112, checked 2026-10-06.
- [RFC 7230: Hypertext Transfer Protocol (HTTP/1.1): Message Syntax and Routing](https://www.rfc-editor.org/rfc/rfc7230): RFC (Proposed Standard, obsoleted by RFC 9110 and RFC 9112), RFC 7230, checked 2026-10-05.
- [RFC 7231: Hypertext Transfer Protocol (HTTP/1.1): Semantics and Content](https://www.rfc-editor.org/rfc/rfc7231): RFC (Proposed Standard, obsoleted by RFC 9110), RFC 7231, checked 2026-10-05.
- [RFC 7232: Hypertext Transfer Protocol (HTTP/1.1): Conditional Requests](https://www.rfc-editor.org/rfc/rfc7232): RFC (Proposed Standard, obsoleted by RFC 9110), RFC 7232, checked 2026-10-05.
- [RFC 7233: Hypertext Transfer Protocol (HTTP/1.1): Range Requests](https://www.rfc-editor.org/rfc/rfc7233): RFC (Proposed Standard, obsoleted by RFC 9110), RFC 7233, checked 2026-10-05.
- [RFC 7234: Hypertext Transfer Protocol (HTTP/1.1): Caching](https://www.rfc-editor.org/rfc/rfc7234): RFC (Proposed Standard, obsoleted by RFC 9111), RFC 7234, checked 2026-10-05.
- [RFC 7235: Hypertext Transfer Protocol (HTTP/1.1): Authentication](https://www.rfc-editor.org/rfc/rfc7235): RFC (Proposed Standard, obsoleted by RFC 9110), RFC 7235, checked 2026-10-05.
- [RFC 10008: The HTTP QUERY Method](https://www.rfc-editor.org/rfc/rfc10008): RFC (Proposed Standard), RFC 10008, checked 2026-10-05.
- [draft-ietf-httpbis-safe-method-w-body: The HTTP QUERY Method](https://datatracker.ietf.org/doc/draft-ietf-httpbis-safe-method-w-body/): RFC Published (became RFC 10008), -14, checked 2026-10-05.
- [RFC 5861: HTTP Cache-Control Extensions for Stale Content](https://www.rfc-editor.org/rfc/rfc5861): RFC (Informational), RFC 5861, checked 2026-10-05.
- [RFC 9651: Structured Field Values for HTTP](https://www.rfc-editor.org/rfc/rfc9651): RFC (Proposed Standard), RFC 9651, checked 2026-10-05.
- [RFC 8941: Structured Field Values for HTTP](https://www.rfc-editor.org/rfc/rfc8941): RFC (Proposed Standard, obsoleted by RFC 9651), RFC 8941, checked 2026-10-05.
- [RFC 8288: Web Linking](https://www.rfc-editor.org/rfc/rfc8288): RFC (Proposed Standard), RFC 8288, checked 2026-10-05.
- [RFC 9745: The Deprecation HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9745): RFC (Proposed Standard), RFC 9745, checked 2026-10-05.
- [RFC 8594: The Sunset HTTP Header Field](https://www.rfc-editor.org/rfc/rfc8594): RFC (Informational), RFC 8594, checked 2026-10-05.
- [RFC 9727: api-catalog: A Well-Known URI and Link Relation to Help Discovery of APIs](https://www.rfc-editor.org/rfc/rfc9727): RFC (Proposed Standard), RFC 9727, checked 2026-10-05.
- [RFC 7240: Prefer Header for HTTP](https://www.rfc-editor.org/rfc/rfc7240): RFC (Proposed Standard, updated by RFC 8144), RFC 7240, checked 2026-10-05.
- [RFC 8144: Use of the Prefer Header Field in Web Distributed Authoring and Versioning (WebDAV)](https://www.rfc-editor.org/rfc/rfc8144): RFC (Proposed Standard), RFC 8144, checked 2026-10-05.
- [draft-ietf-httpapi-idempotency-key-header-07: The Idempotency-Key HTTP Header Field](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-07): Internet-Draft (Expired, WG Document), -07, checked 2026-10-05.
- [RFC 7838: HTTP Alternative Services](https://www.rfc-editor.org/rfc/rfc7838): RFC (Standards Track), April 2016, checked 2026-10-06.
- [RFC 8297: An HTTP Status Code for Indicating Hints](https://www.rfc-editor.org/rfc/rfc8297): RFC (Experimental), December 2017, checked 2026-10-06.
- [RFC 8942: HTTP Client Hints](https://www.rfc-editor.org/rfc/rfc8942): RFC (Experimental), February 2021, checked 2026-10-06.
- [RFC 9211: The Cache-Status HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9211): RFC (Standards Track), June 2022, checked 2026-10-06.
- [RFC 9209: The Proxy-Status HTTP Response Header Field](https://www.rfc-editor.org/rfc/rfc9209): RFC (Standards Track), June 2022, checked 2026-10-06.
- [RFC 9213: Targeted HTTP Cache Control](https://www.rfc-editor.org/rfc/rfc9213): RFC (Standards Track), June 2022, checked 2026-10-06.
- [RFC 9218: Extensible Prioritization Scheme for HTTP](https://www.rfc-editor.org/rfc/rfc9218): RFC (Standards Track), June 2022, checked 2026-10-06.
- [RFC 5789: PATCH Method for HTTP](https://www.rfc-editor.org/rfc/rfc5789): RFC (Standards Track), March 2010, checked 2026-10-06.
- [RFC 7578: Returning Values from Forms: multipart/form-data](https://www.rfc-editor.org/rfc/rfc7578): RFC (Standards Track), July 2015, obsoletes RFC 2388, checked 2026-10-06.
- [RFC 9652: The Link-Template HTTP Header Field](https://www.rfc-editor.org/rfc/rfc9652): RFC (Standards Track), September 2024, checked 2026-10-06.
- [RFC 9842: Compression Dictionary Transport](https://www.rfc-editor.org/rfc/rfc9842): RFC (Standards Track), September 2025, checked 2026-10-06.
- [draft-ietf-httpbis-resumable-upload-12: Resumable Uploads for HTTP](https://www.ietf.org/archive/id/draft-ietf-httpbis-resumable-upload-12.html): Internet-Draft, 6 July 2026, expires 7 January 2027, intended status Standards Track, checked 2026-10-06. Posture: track.
