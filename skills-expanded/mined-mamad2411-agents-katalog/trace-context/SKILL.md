---
name: trace-context
description: >-
  W3C Trace Context Level 1 and W3C Baggage: parse, validate, generate and
  propagate the traceparent, tracestate and baggage headers. Covers trace-id,
  parent-id and trace-flags, invalid values and higher-version parsing,
  tracestate keys, limits, truncation and mutation, baggage grammar,
  percent-encoding, properties and limits, the processing model for tracers
  and proxies, and privacy and security. Version lines: Trace Context Level 1
  (W3C Recommendation, current), Trace Context Level 2 (Candidate
  Recommendation Draft, preview, adds the random trace-id flag) and W3C Baggage
  (Candidate Recommendation, current). Use when writing or reviewing a tracer,
  propagator, middleware, gateway or proxy that reads or writes these headers,
  debugging broken or restarted traces, or deciding what to strip at a trust
  boundary. Triggers: W3C trace context, traceparent, tracestate, baggage
  header, trace-id, span-id, sampled flag, random trace-id flag, context
  propagation.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# W3C Trace Context and Baggage

W3C Trace Context, published by the W3C Distributed Tracing Working Group, defines the `traceparent` and `tracestate` HTTP headers that carry a distributed trace across services and vendors. W3C Baggage, from the same group, defines the `baggage` header for application-defined properties. With this skill the agent parses, validates, generates, mutates and forwards these headers as a tracer, a pass-through proxy or an edge service.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

Citations: "§" is Trace Context Level 1, "L2 §" is Trace Context Level 2, "Baggage §" is W3C Baggage.

## Inputs (fill in, or ask before starting)

- Role: forwarder (a proxy, load balancer or message bus that passes headers through), participant (a tracer or propagator that adds its own span), originator (a client that starts traces), edge (a service at a trust boundary), and whether it also reads or writes `baggage`.
- Trust boundary: which inbound callers and outbound targets are external or untrusted. This decides restarts and stripping.
- Your `tracestate` key, if you participate: a simple key or, in Level 1, a `tenant@system` multi-tenant key.
- Target version: Trace Context Level 1 (default) for `traceparent` and `tracestate`. Trace Context Level 2 is a preview (posture: build): implement it behind a switch. W3C Baggage (Candidate Recommendation Snapshot, posture: build) is the only Baggage line. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the W3C publication history pages for Trace Context Level 1, Level 2 and Baggage for a newer publication or status, check the `Errata` label on `w3c/trace-context`, and update the pins.

## Invariants

1. **`traceparent` format.** Version `00` is `version-trace-id-parent-id-trace-flags`: 2, 32, 16 and 2 lowercase hex characters, 55 in total (§ 3.2.2). Version `ff` is invalid (§ 3.2.2.1).
2. **Invalid IDs void the header.** An all-zero or non-lowercase-hex `trace-id` or `parent-id` MUST make the vendor ignore `traceparent` (§ 3.2.2.3, § 3.2.2.4); then start a new trace and delete `tracestate` (§ 4.3).
3. **Header names.** Accept `traceparent` and `tracestate` in any case; send them lowercase (§ 3.2.1, § 3.3.1). Send `baggage` lowercase (Baggage § 3.1).
4. **Forward what you receive.** A vendor receiving `traceparent` or `tracestate` MUST send it on outgoing requests (§ 3.4, § 3.5). If `traceparent` is unchanged, `tracestate` MUST NOT be modified (§ 3.4).
5. **Only four `traceparent` mutations.** Update `parent-id`; update `sampled`, which MUST come with a new `parent-id`; restart the trace; downgrade the version. No other mutation is allowed (§ 3.4).
6. **Flags are a bit field.** Test bits with a mask (§ 3.2.2.5). Undefined flags MUST be written as zero (§ 3.2.2.5.2). In Level 1 that includes bit `0x02`; in Level 2 the random trace-id flag MUST be copied unchanged when continuing a trace (L2 § 3.2.2.5.2).
7. **Higher versions.** Parse the first three fields with the `00` layout, check the dashes, never assume anything about unknown fields, and write the outgoing header as `00` (§ 3.2.4).
8. **`tracestate` depends on `traceparent`.** Do not parse it when `traceparent` failed; its failure MUST NOT affect `traceparent` (§ 3.3). A `tracestate` without `traceparent` MUST be discarded (§ 4.2).
9. **`tracestate` list rules.** At most 32 members; one entry per key; keys and values follow the § 3.3.1.3 grammar; multiple fields are combined in order per RFC 7230 (§ 3.3.1.1, § 3.3.1.4).
10. **`tracestate` order and truncation.** Keep unmodified pairs in order, put new and updated pairs on the left (§ 3.5, § 4.3), and truncate whole entries only: longer than 128 characters first, then from the right (§ 3.3.1.5).
11. **No personal data in trace headers.** No PII in `traceparent` or `tracestate`, and no user-identifiable seed for ID generators (§ 6, § 6.1, § 6.2).
12. **Baggage values are percent-encoded.** Everything outside `baggage-octet`, and `%` itself, MUST be percent-encoded; invalid UTF-8 MUST decode to U+FFFD; `=` may appear in values (Baggage § 3.3.1.3).
13. **Baggage limits.** Propagate every member while the result is at most 64 members and 8192 bytes, across all `baggage` headers combined; never propagate a partial member (Baggage § 3.3.2).

## Workflow

1. **Pick the version.** Use Trace Context Level 1 and W3C Baggage. Turn on Trace Context Level 2 only behind a switch.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target level is recorded, and nothing from the editor's drafts (`traceresponse`, the `trace` Server-Timing metric) is emitted.
2. **Choose the compliance level per request.** Forward only, or participate (§ 2.3). A forwarder never changes `tracestate` without changing `traceparent` (§ 3.4, § 4.4).
   -> [`references/processing-and-privacy.md`](references/processing-and-privacy.md)
   ✓ Each component has a documented role, and pass-through components forward both headers byte for byte.
3. **Parse `traceparent`.** Validate the version prefix, length, hex and all-zero rules; handle higher versions per § 3.2.4.
   -> [`references/traceparent.md`](references/traceparent.md)
   ✓ The invalid examples in the reference are rejected, the valid ones parse, and a `01-…-01-extra` header parses its first three fields.
4. **Parse `tracestate`.** Only after `traceparent` succeeded. Combine multiple fields, accept empty members, and discard invalid entries or the whole header (§ 4.3).
   -> [`references/tracestate.md`](references/tracestate.md)
   ✓ A malformed `tracestate` never causes a new `trace-id`; a lone `tracestate` is dropped.
5. **Start or continue the trace.** With no valid `traceparent`, generate a random 16-byte `trace-id` and 8-byte `parent-id` (§ 4.2, § 8.2); otherwise keep the `trace-id` and mint a new `parent-id` (§ 4.3). Set `sampled` from the recording decision.
   -> [`references/traceparent.md`](references/traceparent.md)
   ✓ No all-zero IDs; `sampled` only changes together with `parent-id`; undefined flag bits go out as `0`.
6. **Write the outgoing headers.** Put your `tracestate` entry on the left, keep the rest in order, enforce 32 members and truncate whole entries.
   -> [`references/tracestate.md`](references/tracestate.md)
   ✓ The Congo and Rojo example in the reference reproduces exactly.
7. **Handle `baggage`.** Parse with the Baggage grammar, percent-encode values, keep properties, respect the limits, and forward it.
   -> [`references/baggage.md`](references/baggage.md)
   ✓ `Amélie` round-trips as `Am%C3%A9lie`; a value containing `=` survives; 64 members of under 8192 bytes are all forwarded.
8. **Apply the trust boundary.** Decide restarts at front gates, guard against `sampled` abuse, strip `tracestate` and `baggage` toward external systems, and return trace headers in responses only to participants.
   -> [`references/processing-and-privacy.md`](references/processing-and-privacy.md)
   ✓ The trust-boundary checklist is answered for every edge, and CORS allows the headers the browser app sends.
9. **Upgrade** (only when asked). Follow the Level 1 to Level 2 checklist behind the switch.
   -> [`references/versions.md`](references/versions.md)
   ✓ Flags `03` keep bit `0x02` across the component, and Level 1 behaviour is unchanged with the switch off.

## Verify before done

- [ ] Version `00` `traceparent` values are exactly 55 lowercase-hex-and-dash characters, with non-zero IDs (§ 3.2.2).
- [ ] Invalid `traceparent` restarts the trace and deletes `tracestate` (§ 4.3); a lone `tracestate` is discarded (§ 4.2).
- [ ] Higher versions are parsed by the § 3.2.4 algorithm and re-emitted as `00`.
- [ ] Flags are tested with masks, and undefined bits are written as zero (§ 3.2.2.5); Level 2 mode preserves the random flag (L2 § 3.2.2.5.2).
- [ ] Unchanged `traceparent` means unchanged `tracestate` (§ 3.4).
- [ ] `tracestate` keeps order, has your entry on the left, no duplicate keys, at most 32 members, and truncates whole entries (§ 3.3.1, § 3.5).
- [ ] At least 512 characters of `tracestate` are propagated, or the lower limit is documented (§ 3.3.1.5).
- [ ] `baggage` values are percent-encoded and decoded with U+FFFD; limits apply to all `baggage` headers together (Baggage § 3.3.1.3, § 3.3.2).
- [ ] No PII in trace headers; ID generators use no user-identifiable seed (§ 6.1, § 6.2).
- [ ] Public endpoints rate-limit recording and do not trust `sampled` blindly (§ 7.2).
- [ ] Nothing from the editor's drafts is emitted, and Level 2 behaviour sits behind a switch.

## Reference index

- **`references/versions.md`**: Trace Context Level 1, Trace Context Level 2 and W3C Baggage with their W3C status, what Level 2 and the editor's drafts change, the upgrade checklist and the preview. Load for steps 1 and 9.
- **`references/traceparent.md`**: grammar, field rules, valid and invalid examples, sampled and random flags, higher-version parsing with a parser sketch, mutations and ID generation. Load for steps 3 and 5.
- **`references/tracestate.md`**: header combining, Level 1 and Level 2 key grammars, values, limits and truncation, mutations, the worked example and common mistakes. Load for steps 4 and 6.
- **`references/baggage.md`**: grammar, keys, values, properties, percent-encoding with an encode and decode sketch, limits, mutations, security and privacy. Load for step 7.
- **`references/processing-and-privacy.md`**: forwarding versus participating, the processing model and decision table, other protocols, privacy, security and the trust-boundary checklist. Load for steps 2 and 8.

## Related skills

- `opentelemetry` for OpenTelemetry instrumentation and context propagation, whose Baggage implementations the W3C Working Group audits (Baggage, Status): `npx skills add ScaleDockHQ/scaledock-skills --skill opentelemetry`.
- `opentelemetry-genai` for tracing generative AI calls on top of the same context: `npx skills add ScaleDockHQ/scaledock-skills --skill opentelemetry-genai`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Trace Context (latest version)](https://www.w3.org/TR/trace-context/): W3C Recommendation, Level 1 of 23 November 2021 (same document as the Level 1 URL), checked 2026-10-05.
- [Trace Context Level 1](https://www.w3.org/TR/trace-context-1/): W3C Recommendation, 23 November 2021 (REC-trace-context-1-20211123), checked 2026-10-05.
- [Trace Context Level 2](https://www.w3.org/TR/trace-context-2/): W3C Candidate Recommendation Draft, 28 March 2024 (CRD-trace-context-2-20240328), checked 2026-10-05.
- [Propagation format for distributed context: Baggage](https://www.w3.org/TR/baggage/): W3C Candidate Recommendation Snapshot, 30 May 2024 (CR-baggage-20240530), checked 2026-10-05.
- [Trace Context editor's draft](https://w3c.github.io/trace-context/): Editor's Draft, `w3c/trace-context` commit `acab820` (2026-06-29), checked 2026-10-05.
- [Baggage editor's draft](https://w3c.github.io/baggage/): Editor's Draft, `w3c/baggage` commit `bfe9a3b` (2026-06-30), checked 2026-10-05.
- [Trace Context Protocols Registry](https://www.w3.org/TR/trace-context-protocols-registry/): W3C Working Group Note, 19 November 2019, checked 2026-10-05.
