---
name: openid-federation
description: "OpenID Federation: build and validate trust chains, entity statements and metadata policy. Use when building or reviewing a Trust Anchor, Intermediate, Leaf, Trust Mark Issuer or resolver, or when an OpenID Connect RP or OP must trust a peer through a federation: entity configurations at /.well-known/openid-federation, subordinate statements, authority_hints, trust_anchor_hints, trust chain resolution and validation, metadata_policy operators (value, add, default, one_of, subset_of, superset_of, essential) and metadata_policy_crit, constraints (max_path_length, naming_constraints, allowed_entity_types), trust marks and delegation, fetch, list, resolve, trust mark status and historical keys endpoints, Automatic and Explicit Registration, the trust_chain header, the Subordinate Events and Extended Subordinate Listing drafts, and upgrading pre-Final drafts (ID4). Targets OpenID Federation 1.1 (Federation 1.1 and Federation for OpenID Connect 1.1, Final) and supports OpenID Federation 1.0 Final."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# OpenID Federation

OpenID Federation lets two entities with no prior relationship trust each other through a common Trust Anchor. Each entity publishes a signed Entity Configuration, and Superiors publish signed Subordinate Statements about their Immediate Subordinates. A verified chain of these, with its metadata policy applied, gives the peer's Resolved Metadata.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), cited inline as (Spec § section). If a rule is not in a source, it is not in this skill.

Federation 1.1 contains the protocol-independent parts of Federation 1.0, and Federation for OpenID Connect 1.1 contains the OpenID Connect and OAuth 2.0 parts. Neither adds functionality beyond 1.0 (Federation 1.1 § 1, Federation Connect 1.1 § 1). This skill cites the 1.1 documents as "Federation" and "Federation Connect". Federation 1.0 holds the same rules in one document.

## Inputs (fill in, or ask before starting)

- **Role:** Trust Anchor, Intermediate, Leaf (RP, OP, OAuth client, authorization server or protected resource), Trust Mark Issuer, or resolver. One entity can have several Entity Types.
- **Target version:** OpenID Federation 1.1 (current, the default). OpenID Federation 1.0 is supported: use it when the federation or a conformance profile names it. OpenID Federation 1.0 drafts (ID4 and earlier working-group drafts) are legacy: read them and upgrade, never emit their parameter names. No preview is listed. See [`references/versions.md`](references/versions.md).
- **Revision:** the pinned revisions in [Sources](#sources). Ask before using a draft.
- **Trust Anchors:** the Entity Identifiers and public keys of the Trust Anchors this deployment trusts, obtained out of band (Federation § 4).
- **Federation policy:** signing algorithms, required trust marks, client registration methods and any additional policy operators the federation defines.
- **Sources refresh:** before relying on a pin, compare it with the [OpenID Foundation specifications index](https://openid.net/developers/specs/). If a revision changed, re-read the source and update `metadata.json` and [Sources](#sources).

## Invariants

1. An Entity Identifier is an `https` URL with a host and optional port and path, and no query or fragment (Federation § 1.2).
2. Entity Statements have `typ: entity-statement+jwt` and are rejected otherwise. `alg` is never `none`, and `kid` exactly matches a key in the issuer's Entity Configuration `jwks` (Federation § 3, § 3.2).
3. The Entity Configuration is served at the Entity Identifier, minus any trailing `/`, plus `/.well-known/openid-federation`, as `application/entity-statement+jwt`. Trust Anchors and Intermediates MUST publish it (Federation § 9, § 9.2).
4. A chain is valid only if every statement is current, `ES[j].iss == ES[j+1].sub`, each statement is signed by a key in the next statement's `jwks`, and the last statement is the Trust Anchor's, verified with the Trust Anchor key held out of band (Federation § 10.2).
5. Metadata policy resolves from the most Superior statement down. Any policy error, conflict, or unknown operator listed in `metadata_policy_crit` makes the chain invalid (Federation § 6.1.4).
6. Every `constraints` claim in the chain is applied, and any failure makes the chain invalid (Federation § 6.2).
7. A chain expires at the smallest `exp` in it. A registration based on a chain never outlives it (Federation § 10.4, Federation Connect § 12.3).
8. A trust mark is trusted only after trust in its issuer is established through a chain. It has `typ: trust-mark+jwt`, and it needs a valid `delegation` when the Trust Anchor lists an owner for its type (Federation § 7, § 7.3).
9. Entity Statements already fetched are never fetched again during one resolution, and an `authority_hints` entry that leads to a loop is dropped (Federation § 10.1). Implementations limit how many `authority_hints` they follow (Federation § 18.1).
10. With Automatic Registration, the RP's Entity Identifier is its `client_id`, requests are authenticated with asymmetric keys, and the RP resolves the OP's chain before sending anything (Federation Connect § 12.1).

## Workflow

1. **Pick the version.** Use Federation 1.1 unless the federation names 1.0. If a peer speaks a pre-Final draft, plan an upgrade (step 10).
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and no draft parameter name is emitted.
2. **Publish the Entity Configuration.** Set `iss` equal to `sub`, plus `jwks`, `metadata` per Entity Type, and `authority_hints` for non-Trust-Anchors.
   -> [`references/entity-statements.md`](references/entity-statements.md)
   ✓ `/.well-known/openid-federation` returns a signed, typed JWT that passes (Federation § 3.2).
3. **Issue Subordinate Statements and endpoints (Trust Anchors and Intermediates).** Expose fetch and list, and add `metadata_policy` and `constraints` where needed.
   -> [`references/endpoints.md`](references/endpoints.md), [`references/metadata-policy.md`](references/metadata-policy.md)
   ✓ The fetch endpoint returns `application/entity-statement+jwt`, and errors use (Federation § 8.9).
4. **Resolve a peer's trust chain.** Collect statements bottom-up from `authority_hints`, or use a resolver.
   -> [`references/trust-chains.md`](references/trust-chains.md)
   ✓ Loops and unknown Trust Anchors are skipped, and the number of hints followed is bounded.
5. **Validate the chain, then apply policy and constraints.**
   -> [`references/trust-chains.md`](references/trust-chains.md), [`references/metadata-policy.md`](references/metadata-policy.md)
   ✓ Tests cover a broken signature link, an expired statement, a policy conflict and a constraint failure, and each one invalidates the chain.
6. **Evaluate trust marks when the federation uses them.**
   -> [`references/trust-marks.md`](references/trust-marks.md)
   ✓ The trust mark issuer's chain is validated before the trust mark itself.
7. **Register OpenID Connect or OAuth 2.0 clients.** Use Automatic or Explicit Registration.
   -> [`references/registration.md`](references/registration.md)
   ✓ The Request Object or registration JWT `aud` is only the OP's Entity Identifier, and the registration lifetime is at most the chain lifetime.
8. **Refresh and roll keys.** Re-resolve when chains expire, and roll Federation Entity Keys with overlap.
   -> [`references/trust-chains.md`](references/trust-chains.md)
   ✓ An expired chain is never used, and old keys stay published until Subordinates have the new ones.
9. **Add draft endpoints only when asked.**
   -> [`references/endpoints.md`](references/endpoints.md)
   ✓ Each draft in use is pinned to the revision in [Sources](#sources), with its posture recorded.
10. **Upgrade** (only when asked). Move a draft implementation to the Final names and behaviour, or re-cite a 1.0 implementation against the 1.1 documents.
    -> [`references/versions.md`](references/versions.md)
    ✓ No `anchor`, trust mark `id`, `trust_mark_id`, `homepage_uri` or draft error code remains, and the federation's chains resolve to the same Resolved Metadata.

## Verify before done

- [ ] Every Entity Statement, trust mark, resolve response and historical keys JWT checks its `typ` and rejects a missing or wrong value.
- [ ] Chain validation enforces `iss`/`sub` linkage, signature linkage, `iat`, `exp`, and the out-of-band Trust Anchor key (Federation § 10.2).
- [ ] Policy resolution starts at the Trust Anchor's statement, merges operators per their rules, and fails closed (Federation § 6.1.4).
- [ ] Operators are applied in order: `value`, `add`, `default`, `one_of`, `subset_of`, `superset_of`, then `essential` (Federation § 6.1.3.1).
- [ ] Subordinate `metadata` is applied before the resolved policy (Federation § 6.1.4.2).
- [ ] `max_path_length`, `naming_constraints` and `allowed_entity_types` are enforced (Federation § 6.2).
- [ ] Endpoint URLs are published in the Entity Configuration, not in Subordinate Statements (Federation § 8.1, § 8.2).
- [ ] Chain and registration lifetimes use the minimum `exp` (Federation § 10.4, Federation Connect § 12.3).
- [ ] Every draft in use carries its pinned revision and posture.
- [ ] Nothing emitted uses a parameter name, error code or media type from a pre-Final draft.

## Reference index

| File                                                                 | Covers                                                                                                                         |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| [`references/versions.md`](references/versions.md)                   | Version lines, which to use, what changed from the drafts and in the 1.1 split, upgrade steps, why no preview is listed        |
| [`references/entity-statements.md`](references/entity-statements.md) | Entity Statement claims, validation, the well-known URL, `federation_entity` metadata, Entity Types, media types               |
| [`references/trust-chains.md`](references/trust-chains.md)           | Chain structure, collection, validation, selection, expiry, constraints, key rollover, DoS limits                              |
| [`references/metadata-policy.md`](references/metadata-policy.md)     | Policy structure, the seven standard operators, combination and merge rules, resolution and application                        |
| [`references/trust-marks.md`](references/trust-marks.md)             | Trust mark claims, issuers and owners, delegation, validation, status                                                          |
| [`references/endpoints.md`](references/endpoints.md)                 | Fetch, list, resolve, trust mark status, listing and issuance, historical keys, client authentication, errors, draft endpoints |
| [`references/registration.md`](references/registration.md)           | Automatic and Explicit Registration for OpenID Connect and OAuth 2.0                                                           |

## Related skills

- `openid-connect`: the OpenID Connect protocol that Federation Connect registers clients for. `npx skills add ScaleDockHQ/scaledock-skills --skill openid-connect`
- `openid`: the umbrella skill that routes between the OpenID Foundation specifications. `npx skills add ScaleDockHQ/scaledock-skills --skill openid`
- `jwt`: JWS and JWT processing that every Entity Statement relies on. `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`
- `oauth`: OAuth 2.0 clients, authorization servers and protected resources in a federation. `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OpenID Federation 1.0](https://openid.net/specs/openid-federation-1_0-final.html): Final, 1.0 (17 February 2026), checked 2026-10-02.
- [OpenID Federation 1.1](https://openid.net/specs/openid-federation-1_1.html): Final, 1.1 (5 May 2026), checked 2026-10-02.
- [OpenID Federation for OpenID Connect 1.1](https://openid.net/specs/openid-federation-connect-1_1.html): Final, 1.1 (5 May 2026), checked 2026-10-02.
- [OpenID Federation 1.0 - draft 49](https://openid.net/specs/openid-federation-1_0-49.html): Draft, draft 49 (15 February 2026), checked 2026-10-05. Read for its Document History; superseded by the Final.
- [OpenID Federation 1.0 - draft 36 (Implementer's Draft 4)](https://openid.net/specs/openid-federation-1_0-ID4.html): Implementer's Draft, ID4 (document draft 36, 31 May 2024), checked 2026-10-05. Legacy line.
- [OpenID Connect Federation 1.0 - draft 17 (Implementer's Draft 3)](https://openid.net/specs/openid-connect-federation-1_0-ID3.html): Implementer's Draft, ID3 (document draft 17, 9 September 2021), checked 2026-10-05. Legacy line, under the earlier name.
- [OpenID Connect Relying Party Metadata Choices 1.0](https://openid.net/specs/openid-connect-rp-metadata-choices-1_0-final.html): Final, 1.0 (25 March 2026), checked 2026-10-02.
- [OpenID Federation Subordinate Events Endpoint 1.0](https://openid.net/specs/openid-federation-subordinate-events-1_0-ID1.html): Implementer's Draft, ID1 (document draft 01, 3 July 2026), checked 2026-10-02. Draft posture: track, pinned to ID1.
- [OpenID Federation Extended Subordinate Listing 1.0](https://openid.net/specs/openid-federation-extended-listing-1_0-ID1.html): Implementer's Draft, ID1 (document draft 03, 2 July 2026), checked 2026-10-02. Draft posture: track, pinned to ID1.
