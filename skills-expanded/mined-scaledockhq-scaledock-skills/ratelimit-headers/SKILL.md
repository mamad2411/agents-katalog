---
name: ratelimit-headers
description: "RateLimit headers: advertise HTTP API quotas, handle 429 with the IETF RateLimit and RateLimit-Policy header fields (draft-11 of draft-ietf-httpapi-ratelimit-headers), Retry-After (RFC 9110) and 429 Too Many Requests (RFC 6585). Use when adding rate limiting or quota headers to an API, returning or handling a 429, writing a client that backs off or paces itself, upgrading from X-RateLimit-Limit, X-RateLimit-Remaining and X-RateLimit-Reset or from older drafts (RateLimit-Limit, RateLimit-Remaining, RateLimit-Reset, or a limit/remaining/reset RateLimit dictionary), or choosing the quota-exceeded problem type for a throttled response. Triggers: rate limit headers, RateLimit-Policy, quota policy, throttling, backoff, Retry-After, Too Many Requests, partition key, Structured Fields (RFC 9651)."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.1"
  kind: standard
---

# RateLimit header fields for HTTP

The IETF HTTPAPI working group's draft defines two response header fields: `RateLimit-Policy` advertises a server's quota policies, and `RateLimit` reports the quota currently available under one of them. With this skill the agent emits and reads both, pairs them with `Retry-After` (RFC 9110) and `429 Too Many Requests` (RFC 6585), and writes the throttled response body.

Draft posture: build (`draft-ietf-httpapi-ratelimit-headers-11`, 23 May 2026). Implement the pinned revision's current shape. `Retry-After` and the 429 status are the stable fields that carry the essential "wait" signal to clients that ignore the draft.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. Bare section numbers (§ 4.1) refer to the pinned draft. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: server (emits the fields), client (reads them), or intermediary (gateway or proxy that passes or rewrites them).
- Quota policies: for each one, a name, the quota, the window in seconds, the unit (requests, content bytes or concurrent requests) and how clients are partitioned.
- Target version: draft-11 (default, posture build: implement and emit it). draft-07, draft-06 and earlier, and X-RateLimit headers are legacy: read them and upgrade from them, never emit them in new work. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned draft revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the [datatracker page](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/) for a newer revision or an RFC number, and update the pins. The pinned revision expires on 24 November 2026.

## Invariants

1. **`RateLimit-Policy` is a non-empty Structured Fields List** of quota policy Items whose value MUST be a String naming the policy (§ 3). Each Item has a REQUIRED `q` (non-negative Integer quota) and optional `qu` (String unit, default requests), `w` (positive Integer window in seconds) and `pk` (Byte Sequence partition key) (§ 3.1, § 3.1.1 to § 3.1.4).
2. **`RateLimit` is a Structured Fields List** of service limit Items, each identifying a policy (§ 4, § 4.1). Each has a REQUIRED `r` (non-negative Integer available quota) and optional `t` (non-negative Integer effective window in seconds) and `pk` (§ 4.1.1 to § 4.1.3).
3. **Never in trailers.** Neither field may appear in a trailer section (§ 3.1, § 4.1).
4. **`Retry-After` wins.** When both are present, the client MUST give `Retry-After` precedence (§ 7), and the server SHOULD NOT make `Retry-After` point earlier than the end of the effective window (§ 6).
5. **Hints, not guarantees.** Clients MUST NOT treat a positive `r` as a guarantee (§ 4.1.1, § 8.3), MUST NOT assume the quota is fully restored after `t` (§ 4.1.2), and MUST NOT assume later responses carry the fields at all (§ 7).
6. **Malformed fields are ignored.** Clients MUST ignore malformed RateLimit fields (§ 7); a Structured Fields parse failure means the whole field is ignored (RFC 9651 § 4.2).
7. **No capacity leaks.** A server MUST NOT convey values that expose an unwanted volume of requests, and SHOULD cap the ratio between `r` and `t` (§ 6, § 8.5).
8. **Policy names are printable ASCII.** Structured Fields Strings allow only `%x20` to `%x7E`, with `"` and `\` escaped; anything else fails serialization (RFC 9651 § 3.3.3, § 4.1.6).
9. **A 429 is not cached.** Responses with 429 MUST NOT be stored by a cache, and SHOULD include details explaining the condition (RFC 6585 § 4).

## Workflow

1. **Pick the version.** Use draft-11. If the server or client already uses `X-RateLimit-*`, `RateLimit-Limit` or a `limit=` dictionary, identify its line and plan the upgrade (step 7).
   -> [`references/versions.md`](references/versions.md)
   ✓ Every field the work emits is a draft-11 `RateLimit-Policy` or `RateLimit` field, or `Retry-After`.
2. **Model the quota policies.** Name each policy and set `q`, `w`, `qu` and `pk`. Prefix any service-specific parameter with a vendor identifier (§ 3.1, § 4.1). Decide how partition keys are derived and document it (§ 6.1).
   -> [`references/fields.md`](references/fields.md)
   ✓ Every policy has an ASCII name, an Integer `q`, and a window in whole seconds; partition keys contain no sensitive data.
3. **Emit the fields.** Send `RateLimit-Policy` where policies are stable and `RateLimit` with the current `r` and `t` (§ 3, § 4). Sending them on every response is optional (§ 6.2), and they are independent of the status code (§ 6).
   -> [`references/fields.md`](references/fields.md), [`references/examples.md`](references/examples.md)
   ✓ Serialized values parse as Structured Fields Lists, and `r` and `t` never reveal more capacity than intended.
4. **Answer throttled requests.** Return 429 (or 503 for reduced capacity) with `Retry-After`, the RateLimit fields, and a problem details body using the draft's problem types (§ 5).
   -> [`references/examples.md`](references/examples.md)
   ✓ `Retry-After` is not earlier than the end of the effective window, and the body explains the condition (RFC 6585 § 4).
5. **Implement the client.** Parse both fields, ignore malformed ones, honor `Retry-After` first, and pace requests so the available quota is not exceeded within the effective window (§ 7).
   -> [`references/behavior.md`](references/behavior.md)
   ✓ The client survives missing, malformed and implausible values, and ignores fields on cached responses (§ 7.3, § 8.5.1).
6. **Check intermediaries, caching and security.** Make sure gateways only tighten the advertised policy, and review the security and privacy considerations.
   -> [`references/behavior.md`](references/behavior.md)
   ✓ No intermediary makes the policy more permissive or strips the fields (§ 7.2), and reset times carry jitter (§ 8.5).
7. **Upgrade** (only when asked). Follow the checklist for the source line: name each policy, move the limit into `q`, the remaining count into `r` and the reset into `t` as delay-seconds.
   -> [`references/versions.md`](references/versions.md)
   ✓ The new fields parse as RFC 9651 Lists, and clients back off at the same points as before.

## Verify before done

- [ ] Every `RateLimit-Policy` and `RateLimit` value parses with an RFC 9651 List parser, and every Item value is a String.
- [ ] Every policy Item has `q`; every service limit Item has `r`; all numbers are non-negative Integers, and `w` is greater than zero (§ 3.1.1, § 3.1.3, § 4.1.1, § 4.1.2).
- [ ] Each `RateLimit` Item names a policy the server defines, and `pk` values, if any, are Byte Sequences (§ 3.1.4, § 4.1.3).
- [ ] Throttled responses carry `Retry-After` in the RFC 9110 § 10.2.3 format, no earlier than the effective window ends (§ 6).
- [ ] The client gives `Retry-After` precedence, ignores malformed fields, and does not rely on the fields being present (§ 7).
- [ ] The output matches the shapes in the draft's examples (§ 3.2, § 4.2, Appendix B), without copying their known typos (see `references/examples.md`).

## Reference index

- **`references/versions.md`**: draft-11 and the legacy lines with their status, what changed between the header designs, and upgrade checklists from each. Load for steps 1 and 7.
- **`references/fields.md`**: syntax of both fields, every parameter, Structured Fields serialization rules, and how they map onto the legacy `X-RateLimit-*` headers. Load for steps 2 and 3.
- **`references/behavior.md`**: server, client and intermediary rules, caching, and the security and privacy considerations. Load for steps 5 and 6.
- **`references/examples.md`**: full HTTP exchanges, the draft's problem types, and framework-neutral TypeScript for serializing and parsing. Load for steps 3 and 4.

## Related skills

- `problem-details` for the RFC 9457 body of a 429 or 503 response: `npx skills add ScaleDockHQ/scaledock-skills --skill problem-details`.
- `http-semantics` for RFC 9110 status codes, `Retry-After` and caching around rate-limited responses: `npx skills add ScaleDockHQ/scaledock-skills --skill http-semantics`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

Draft posture: build, pinned to `draft-ietf-httpapi-ratelimit-headers-11`.

- [RateLimit header fields for HTTP (draft-ietf-httpapi-ratelimit-headers-11)](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-11): WG draft (IETF HTTPAPI), revision 11 of 23 May 2026, checked 2026-10-05.
- [Datatracker: draft-ietf-httpapi-ratelimit-headers](https://datatracker.ietf.org/doc/draft-ietf-httpapi-ratelimit-headers/): WG draft (IETF HTTPAPI), active, no RFC; revision 11 latest, history back to draft-polli-ratelimit-headers-00, checked 2026-10-05.
- [draft-ietf-httpapi-ratelimit-headers-08](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-08): WG draft (IETF HTTPAPI), superseded, revision 08 of 7 October 2024, checked 2026-10-05.
- [draft-ietf-httpapi-ratelimit-headers-07](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-07): WG draft (IETF HTTPAPI), superseded, revision 07 of 24 June 2023, checked 2026-10-05.
- [draft-ietf-httpapi-ratelimit-headers-06](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-06): WG draft (IETF HTTPAPI), superseded, revision 06 of 22 December 2022, checked 2026-10-05.
- [draft-ietf-httpapi-ratelimit-headers-00](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-ratelimit-headers-00): WG draft (IETF HTTPAPI), superseded, revision 00 of 18 December 2020, checked 2026-10-05.
- [draft-polli-ratelimit-headers-00](https://datatracker.ietf.org/doc/html/draft-polli-ratelimit-headers-00): Individual draft, replaced by draft-ietf-httpapi-ratelimit-headers, revision 00 of 5 September 2019, checked 2026-10-05.
- [RFC 9110: HTTP Semantics](https://www.rfc-editor.org/rfc/rfc9110): RFC (Internet Standard, STD 97), RFC 9110, checked 2026-10-02.
- [RFC 6585: Additional HTTP Status Codes](https://www.rfc-editor.org/rfc/rfc6585): RFC (Proposed Standard), RFC 6585, checked 2026-10-02.
- [RFC 9651: Structured Field Values for HTTP](https://www.rfc-editor.org/rfc/rfc9651): RFC (Proposed Standard), RFC 9651, checked 2026-10-02.
- [RFC 9457: Problem Details for HTTP APIs](https://www.rfc-editor.org/rfc/rfc9457): RFC (Proposed Standard), RFC 9457, checked 2026-10-02.
- [IANA HTTP Problem Types registry](https://www.iana.org/assignments/http-problem-types): IANA registry, last updated 2026-06-26, checked 2026-10-02.
- [IANA HTTP Field Name registry](https://www.iana.org/assignments/http-fields): IANA registry, read 2026-10-02 (no RateLimit entries yet), checked 2026-10-02.
