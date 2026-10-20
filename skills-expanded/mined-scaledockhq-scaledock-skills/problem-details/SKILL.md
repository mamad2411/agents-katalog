---
name: problem-details
description: "RFC 9457 Problem Details: return standard HTTP API errors as application/problem+json, with the type, title, status, detail and instance members plus extension members. Use when designing, implementing or reviewing API error responses: an error envelope, a 4xx or 5xx body, validation errors, a problem type URI or an IANA HTTP Problem Types registry entry, or the WWW-Authenticate challenge that goes next to a 401 or 403 (RFC 9110, RFC 6750 Bearer, RFC 9470 step-up). Triggers: problem details, problem+json, application/problem+xml, RFC 7807 (obsoleted by RFC 9457, upgrade to RFC 9457), about:blank, error response format, invalid_token, insufficient_scope, insufficient_user_authentication."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# Problem Details for HTTP APIs

RFC 9457, published by the IETF, defines a JSON object (and an equivalent XML format) that carries machine-readable details of an error in an HTTP response. It obsoletes RFC 7807. With this skill the agent produces and consumes `application/problem+json` responses, defines problem types, and pairs them with the right `WWW-Authenticate` challenge on 401 and 403.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer (an API that returns problems), consumer (a client that reads them), or both.
- Authentication: none, Bearer tokens (RFC 6750), or another HTTP authentication scheme. This decides the 401 and 403 headers.
- Target version: RFC 9457 (default). RFC 7807 is legacy: read it and upgrade from it, never author against it; the wire format is the same. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the RFC Editor entry for RFC 9457 for errata or an obsoleting RFC, check the IANA registry for new problem types, and update the pins.

## Invariants

1. **Media type.** A JSON problem document is served as `application/problem+json` (§ 3); the XML form is `application/problem+xml` (Appendix B). A server may send it even when the client did not list it in `Accept` (§ 3).
2. **`status` matches the response.** If present, `status` is the same code as the actual HTTP response (§ 3.1.2). Generic HTTP software only sees the real status code.
3. **`type` is the identifier.** Consumers use the resolved `type` URI as the primary identifier of the problem (§ 3.1.1). A missing `type` means `about:blank` (§ 3.1.1, § 4.2.1). Absolute URIs are recommended (§ 3.1.1).
4. **`title` is stable per type.** It does not change between occurrences except for localization (§ 3.1.3). With `about:blank`, it is the status phrase for the code, such as "Not Found" (§ 4.2.1).
5. **`detail` helps the client fix the problem and is not parsed.** It explains this occurrence (§ 3.1.4). Machine-readable facts go in extension members, because consumers should not parse `detail` (§ 3.1.4).
6. **Consumers are tolerant.** A member with the wrong JSON type is ignored as if absent (§ 3.1), and unknown extension members are ignored (§ 3.2).
7. **New problem types document a type URI, a title and a status code** (§ 4). Extension member names start with a letter, use only letters, digits and `_`, and are at least three characters (§ 4).
8. **One problem per response.** When several problems of different types occur, return the most relevant or urgent one (§ 3).
9. **No internals in the body.** No stack traces or implementation details; vet every field for information leaks (§ 5, § 4).
10. **401 always carries a challenge.** A 401 response includes `WWW-Authenticate` with at least one challenge (RFC 9110 § 15.5.2, § 11.6.1). Valid but inadequate credentials get 403 (RFC 9110 § 11.4). For Bearer tokens, the error code in the challenge follows RFC 6750 § 3.1.

## Workflow

1. **Pick the version.** Use RFC 9457. If the API or its documentation cites RFC 7807, plan the upgrade (step 8).
   -> [`references/versions.md`](references/versions.md)
   ✓ New documentation and code cite RFC 9457.
2. **Decide whether a problem type is needed.** A generic condition that the status code already explains needs no new type; use `about:blank` or omit `type` (§ 4, § 4.2.1). Check the IANA HTTP Problem Types registry for a reusable type before minting one (§ 4.1, § 4.2).
   -> [`references/members.md`](references/members.md)
   ✓ Every error the API returns maps to a status code and either `about:blank`, a registered type, or a type you document.
3. **Define each new problem type.** Write down its type URI (stable and under your control), title, status code and extension members (§ 4, § 4.1). Make the type URI resolve to human-readable documentation (§ 3.1.1, § 4).
   -> [`references/members.md`](references/members.md)
   ✓ Each type has a documented URI, title, status and members, and every extension name follows the naming rule.
4. **Pair authentication errors with the right header.** Pick the status and the `WWW-Authenticate` challenge for each authentication or authorization failure, then build the body from the same reason.
   -> [`references/auth-challenges.md`](references/auth-challenges.md)
   ✓ Every 401 has a challenge; `invalid_token`, `insufficient_scope` and `insufficient_user_authentication` use the status RFC 6750 and RFC 9470 give them; a request without credentials gets no error code.
5. **Generate responses.** Set the status, `Content-Type: application/problem+json`, and the body. Put field-level validation errors in an extension array such as the `errors` example in § 3. For 429 and 503, add `Retry-After` where the type calls for it (§ 4).
   -> [`references/examples.md`](references/examples.md)
   ✓ The body validates against the JSON Schema in Appendix A, and `status` equals the response code.
6. **Consume responses.** Switch on `type`, read extensions you know, ignore the rest, and fall back to the HTTP status code when `type` is `about:blank` or unknown.
   -> [`references/examples.md`](references/examples.md)
   ✓ The client never parses `detail`, never auto-dereferences `type` (§ 3.1.1), and survives a malformed member.
7. **Review security.** Check each type and each generated body against the security considerations.
   -> [`references/security.md`](references/security.md)
   ✓ No stack traces, internal identifiers or other users' data appear in any body or `instance` URI.
8. **Upgrade** (only when asked). Follow the RFC 7807 to RFC 9457 checklist: update references, keep the media types, namespace and every `type` URI, and apply the multiple-problem and wrong-type guidance.
   -> [`references/versions.md`](references/versions.md)
   ✓ Bodies validate against Appendix A, and no existing `type` URI changed.

## Verify before done

- [ ] Every error response has `Content-Type: application/problem+json` (or `application/problem+xml`) and a body that validates against the RFC 9457 Appendix A schema.
- [ ] `status`, when present, equals the HTTP status code of the response (§ 3.1.2).
- [ ] Every non-`about:blank` type URI is absolute, stable, documented, and listed with its title and status (§ 3.1.1, § 4).
- [ ] With `about:blank`, `title` is the status phrase (§ 4.2.1).
- [ ] Extension member names match `^[A-Za-z][A-Za-z0-9_]{2,}$` (§ 4), or the deviation comes from a specification that defines the member.
- [ ] Every 401 carries `WWW-Authenticate`; Bearer challenges follow RFC 6750 § 3 and § 3.1.
- [ ] Consumers ignore unknown members and wrongly typed members (§ 3.1, § 3.2).
- [ ] No body exposes implementation details (§ 5).

## Reference index

- **`references/versions.md`**: RFC 9457 and RFC 7807 with their status, what RFC 9457 changed, and the upgrade checklist. Load for steps 1 and 8.
- **`references/members.md`**: every standard member, `about:blank`, extension naming, the registry and its current entries, and the Appendix A JSON Schema. Load for steps 2 and 3.
- **`references/auth-challenges.md`**: status and `WWW-Authenticate` per authentication outcome (RFC 9110, RFC 6750, RFC 9470), and how the body lines up with the header. Load for step 4.
- **`references/examples.md`**: full HTTP examples and framework-neutral TypeScript for producing and consuming problems. Load for steps 5 and 6.
- **`references/security.md`**: information leaks, `status` disagreement, and what to keep out of `detail` and `instance`. Load for step 7.

## Related skills

- `ratelimit-headers` for 429 responses with `Retry-After`, `RateLimit` and `RateLimit-Policy`: `npx skills add ScaleDockHQ/scaledock-skills --skill ratelimit-headers`.
- `standard-schema` for turning validation issues from any Standard Schema validator into an `errors` extension: `npx skills add ScaleDockHQ/scaledock-skills --skill standard-schema`.
- `http-semantics` for choosing the status code and headers that a problem response carries: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457): RFC (Proposed Standard), RFC 9457, checked 2026-10-05.
- [RFC 7807: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc7807): RFC (Proposed Standard, obsoleted by RFC 9457), RFC 7807, checked 2026-10-05.
- [IANA HTTP Problem Types registry](https://www.iana.org/assignments/http-problem-types): IANA registry, last updated 2026-06-26, checked 2026-10-02.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): RFC (Internet Standard, STD 97), RFC 9110, checked 2026-10-02.
- [RFC 6750: OAuth 2.0 Bearer Token Usage](https://www.rfc-editor.org/rfc/rfc6750): RFC (Proposed Standard, updated by RFC 8996 and RFC 9700), RFC 6750, checked 2026-10-02.
- [RFC 9470: OAuth 2.0 Step Up Authentication Challenge Protocol](https://www.rfc-editor.org/rfc/rfc9470): RFC (Proposed Standard), RFC 9470, checked 2026-10-02.
