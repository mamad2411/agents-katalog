---
name: scim
description: "SCIM 2.0: provision users and groups across domains with the RFC 7643 schema and RFC 7644 protocol, as a service provider or a client. Use when building, consuming or reviewing a SCIM API or an identity provider provisioning connector: /Users, /Groups, /Me, /Bulk and /.search endpoints, PATCH PatchOp with value paths, filter expressions, sortBy, startIndex and count, RFC 9865 cursor pagination (cursor, nextCursor), ETags with If-Match and If-None-Match, ListResponse and Error messages with scimType, /ServiceProviderConfig, /ResourceTypes and /Schemas discovery, the core User and Group schemas, the Enterprise User extension, attribute mutability and returned rules, externalId, deprovisioning with active false, bearer token and RFC 7523 JWT client authentication, RFC 9967 SCIM security events and asynchronous requests (Set-Txn), the IPSIE AL and FastFed SCIM profiles, and upgrading SCIM 1.1 (urn:scim:schemas:core:1.0, /v1) to 2.0. Pins RFC 7643, RFC 7644, RFC 9865 and RFC 9967; no next-line draft exists."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# SCIM 2.0

The System for Cross-domain Identity Management (SCIM) 2.0 is an HTTP and JSON protocol for provisioning identities across domains. A SCIM client, usually the identity provider, creates, updates, deactivates and deletes Users and Groups at a SCIM service provider, usually the application. This skill pins RFC 7643 (schema), RFC 7644 (protocol), RFC 9865 (cursor pagination) and RFC 9967 (security events), and produces a server, client or review that meets their rules.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: SCIM service provider (server), SCIM client, or both. RFC 7643 §1.2 defines both roles; RFC 7642 §2.2.2 describes the actors behind them.
- Target version: SCIM 2.0 (current, the default). SCIM 1.1 is legacy: read it and upgrade from it, never author it. No preview is listed. See [`references/versions.md`](references/versions.md).
- Resources: Users only, or Users and Groups, plus any extensions such as the Enterprise User extension.
- Profile: plain RFC 7643 and RFC 7644, the IPSIE AL SCIM profile (AL1 or AL2), or the FastFed Enterprise SCIM profile.
- Optional features: PATCH, Bulk, filtering, sorting, ETags, cursor pagination, security events.
- Sources: when refreshing this skill or when a rule looks out of date, check the RFC Editor info page of each RFC for "Updated by" entries, re-read the IPSIE AL draft and FastFed specification pages, then every URL in [Sources](#sources). Update the pins and bump the version.

## Invariants

1. **TLS always.** Clients and service providers MUST require TLS; the service provider MUST support TLS 1.2; the client MUST check the server identity (RFC 7644 §7.2). Bearer tokens and cookies MUST be exchanged over TLS (RFC 7644 §7.4).
2. **Every request maps to an access policy.** The service provider MUST map the authenticated client to an access control policy before it retrieves or updates resources (RFC 7644 §2). Bearer tokens MUST have enough entropy and a limited lifetime (RFC 7644 §7.4).
3. **The service provider owns `id` and `meta`.** It assigns them on create; `id` is unique across the service provider, stable, never reassigned, and MUST NOT be set by the client; `meta` is ignored when a client sends it (RFC 7643 §3.1).
4. **The client owns `externalId`.** The service provider MUST NOT set it and MUST interpret it as scoped to the provisioning domain (RFC 7643 §3.1).
5. **Every resource and message declares `schemas`.** Resources carry their schema URIs (RFC 7643 §3); messages use the `urn:ietf:params:scim:api:messages:2.0:` URIs (RFC 7644 §3.1).
6. **Mutability decides what a write can change.** `readOnly` values are ignored on create and PUT; `immutable` values must match once set; PATCH MUST NOT modify `readOnly` or set `immutable` attributes (RFC 7644 §3.3, §3.5.1, §3.5.2).
7. **PUT never creates, and PATCH is atomic.** PUT MUST NOT be used to create resources (RFC 7644 §3.5.1). A PATCH is applied in order and atomically; if one operation fails the resource MUST be restored (RFC 7644 §3.5.2).
8. **Errors use the SCIM Error message.** Errors MUST be returned in the body as `urn:ietf:params:scim:api:messages:2.0:Error` with `status` as a string, plus `scimType` for 400s where defined (RFC 7644 §3.12).
9. **Conflicts are 409 `uniqueness`.** A create that duplicates a unique value such as `userName` MUST return 409 with `scimType` `uniqueness` (RFC 7644 §3.3).
10. **Deleted means gone.** After DELETE, the service provider MUST return 404 for the resource and omit it from queries (RFC 7644 §3.6).
11. **Unknown filters fail.** A service provider MUST reject an unrecognized filter operation with 400 `invalidFilter` (RFC 7644 §3.4.2.2), and MUST return 413 when a bulk request exceeds its limits (RFC 7644 §3.7.4).
12. **Passwords are write-only.** `password` is never returned in any form, and stored values MUST NOT be cleartext (RFC 7643 §4.1.1, §9.2).
13. **Sensitive filters do not go in URLs.** Clients SHOULD use POST `/.search` for filters with personal data, and servers SHOULD answer such GETs with 403 (RFC 7644 §7.5.2).

## Workflow

1. **Pick the version and scope the work.** Target SCIM 2.0; if a peer speaks SCIM 1.1, plan its upgrade. Confirm the role, resources, profile and optional features from Inputs.
   -> [`references/versions.md`](references/versions.md)
   ✓ The design names SCIM 2.0 as the target, lists each endpoint and method to support, and says which profile applies.
2. **Model the resources.** Define User, Group and extension attributes with their characteristics, and the common attributes.
   -> [`references/schema.md`](references/schema.md)
   ✓ Every attribute has type, mutability, returned, uniqueness and caseExact settled.
3. **Implement create, read, replace, patch and delete.** Apply the mutability rules, status codes, `Location` and `meta.location`.
   -> [`references/protocol.md`](references/protocol.md)
   ✓ POST returns 201 with `Location`; DELETE returns 204; a later GET returns 404.
4. **Implement queries.** Filters, sorting, `attributes` and `excludedAttributes`, index or cursor pagination, and POST `/.search`.
   -> [`references/protocol.md`](references/protocol.md), [`references/pagination.md`](references/pagination.md)
   ✓ An empty result is 200 with `totalResults` 0, and an unknown operator is 400 `invalidFilter`.
5. **Add Bulk, ETags and errors.** Bulk with `bulkId` and `failOnErrors`, ETags with `If-Match` and `If-None-Match`, and the error tables.
   -> [`references/protocol.md`](references/protocol.md)
   ✓ A stale `If-Match` gets 412, and an oversized bulk request gets 413.
6. **Publish discovery.** Serve `/ServiceProviderConfig`, `/ResourceTypes` and `/Schemas`, with the RFC 9865 `pagination` and RFC 9967 `securityEvents` attributes where used.
   -> [`references/discovery.md`](references/discovery.md)
   ✓ The ServiceProviderConfig flags match what the server actually supports.
7. **Secure it.** Authentication, authorization per client, tenancy, TLS, privacy and credential handling.
   -> [`references/security.md`](references/security.md)
   ✓ A token for one tenant cannot read or change another tenant's resources.
8. **Apply the profile.** For IPSIE AL or FastFed, add their authentication, filter and timing rules.
   -> [`references/profiles.md`](references/profiles.md)
   ✓ Each MUST in the chosen profile maps to a test.
9. **Add security events if used.** Emit or consume RFC 9967 SETs, and support asynchronous requests.
   -> [`references/events.md`](references/events.md)
   ✓ A 202 response carries `Set-Txn`, and the completion SET has the same `txn`.
10. **Upgrade from SCIM 1.1** (only when a peer runs it). Move URNs, endpoints, PATCH bodies, list responses and errors to their 2.0 forms.
    -> [`references/versions.md`](references/versions.md)
    ✓ No `urn:scim:schemas:core:1.0`, `/v1`, `meta.attributes` or `Errors` array remains, and the checks below pass.

## Verify before done

- [ ] All traffic is HTTPS, and requests without valid credentials get 401 (RFC 7644 §3.12).
- [ ] Responses use `Content-Type: application/scim+json` (RFC 7644 §8.1).
- [ ] POST `/Users` with a duplicate `userName` gets 409 with `"scimType": "uniqueness"`.
- [ ] PATCH with a failing second operation leaves the resource unchanged.
- [ ] `GET /Users?filter=userName eq "x"` works, and a bad filter gets 400 `invalidFilter`.
- [ ] `ListResponse` carries `totalResults`, and `startIndex` and `itemsPerPage` when paged.
- [ ] `/ServiceProviderConfig` reports `patch`, `bulk`, `filter`, `changePassword`, `sort`, `etag` and `authenticationSchemes`.
- [ ] Error bodies use the Error schema and `status` is a string.
- [ ] `password` is never returned, and no resource uses the string `bulkId` in an identifier (RFC 7643 §3.1).

## Reference index

- **`references/versions.md`**: the SCIM 2.0 and SCIM 1.1 lines, which to use, what changed, the 1.1 to 2.0 upgrade steps, and why no preview is listed.
- **`references/schema.md`**: attribute characteristics and data types, multi-valued attributes, common attributes, User, Group, the Enterprise User extension and schema extensions.
- **`references/protocol.md`**: endpoints and methods, create, read, PUT, PATCH, DELETE, filters, sorting, attribute selection, `/.search`, Bulk, `/Me`, errors, versioning and ETags.
- **`references/pagination.md`**: index pagination from RFC 7644 and cursor pagination from RFC 9865.
- **`references/discovery.md`**: `/ServiceProviderConfig`, `/ResourceTypes`, `/Schemas`, and the RFC 9865 and RFC 9967 additions.
- **`references/security.md`**: authentication options, bearer tokens, RFC 7523 JWT client authentication, tenancy, TLS, privacy and credential storage.
- **`references/profiles.md`**: the IPSIE AL SCIM 2.0 profile and the FastFed Enterprise SCIM profile.
- **`references/events.md`**: RFC 9967 security events, the `sub_id` format, provisioning and feed events, asynchronous requests and `Set-Txn`.

## Related skills

- `oauth`, for the OAuth 2.0 token endpoint and client credentials that SCIM clients use: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`
- `jwt`, for the RFC 7523 assertions and signed security event tokens: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 7642: SCIM Definitions, Overview, Concepts, and Requirements](https://www.rfc-editor.org/rfc/rfc7642): RFC (Informational), RFC 7642, checked 2026-10-02.
- [RFC 7643: SCIM Core Schema](https://www.rfc-editor.org/rfc/rfc7643): RFC (Proposed Standard, updated by RFC 9865 and RFC 9967), RFC 7643, checked 2026-10-05.
- [RFC 7644: SCIM Protocol](https://www.rfc-editor.org/rfc/rfc7644): RFC (Proposed Standard, updated by RFC 9865 and RFC 9967), RFC 7644, checked 2026-10-05.
- [RFC 9865: Cursor-Based Pagination of SCIM Resources](https://www.rfc-editor.org/rfc/rfc9865): RFC (Proposed Standard), RFC 9865, checked 2026-10-02.
- [RFC 9967: SCIM Profile for Security Event Tokens](https://www.rfc-editor.org/rfc/rfc9967): RFC (Proposed Standard), RFC 9967, checked 2026-10-02.
- [RFC 7523: JWT Profile for OAuth 2.0 Client Authentication and Authorization Grants](https://www.rfc-editor.org/rfc/rfc7523): RFC (Proposed Standard), RFC 7523, checked 2026-10-02.
- [SCIM Core Schema 1.1](http://www.simplecloud.info/specs/draft-scim-core-schema-01.html): Draft (simplecloud.info), 1.1, 9 July 2012, checked 2026-10-05. Legacy line.
- [SCIM Protocol 1.1](http://www.simplecloud.info/specs/draft-scim-api-01.html): Draft (simplecloud.info), 1.1, 9 July 2012, checked 2026-10-05. Legacy line.
- [SCIM specification index](http://www.simplecloud.info/): Index (simplecloud.info), page as read 2026-10-05, lists SCIM 2.0, SCIM 1.1 and SCIM 1.0 (deprecated), checked 2026-10-05.
- [IETF SCIM working group documents](https://datatracker.ietf.org/wg/scim/documents/): Index (IETF), working group drafts as listed 2026-10-05, checked 2026-10-05.
- [IPSIE AL SCIM 2.0 Profile](https://openid.github.io/ipsie-scim-al/draft-openid-ipsie-al-scim-profile.html): Editor's draft (IPSIE Working Group), Draft 00, editor's copy at commit 1a9985f (2026-09-08); Draft posture: track, checked 2026-10-02.
- [IPSIE AL SCIM profile repository](https://github.com/openid/ipsie-scim-al): Editor's draft source, main at 1a9985f (2026-09-08), checked 2026-10-02.
- [FastFed Enterprise SCIM Profile 1.0](https://openid.net/specs/fastfed-scim-1_0-03.html): Implementer's Draft (archived working group), draft 03, identical to ID1, 2020-10-07; Draft posture: track, checked 2026-10-02.
- [FastFed working group specifications](https://openid.net/wg/fastfed/specifications/): Working group page (archived), lists draft 03 as the most recent, checked 2026-10-02.
