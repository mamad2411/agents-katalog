---
name: gnap
description: "GNAP (RFC 9635): request, issue and verify access tokens. Covers the Grant Negotiation and Authorization Protocol core: grant requests, the access rights array, interaction start and finish modes with the interaction hash, continuation, token rotation and revocation, key binding with httpsig, mtls, jwsd and jws proofs, and RS-first discovery. Also covers RFC 9767 GNAP resource server connections: the token model, token formats, /.well-known/gnap-as-rs discovery, introspection, resource registration and derived tokens, and how the access array relates to OAuth Rich Authorization Requests (authorization_details, RFC 9396). Use when building a GNAP client, authorization server or resource server, validating key-bound GNAP tokens, writing WWW-Authenticate: GNAP challenges, designing access types, or comparing GNAP with OAuth 2.0. RFC 9635 is the only version line; pre-RFC drafts are upgraded to it, and no preview exists."
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# GNAP

The Grant Negotiation and Authorization Protocol (GNAP, RFC 9635) is an IETF protocol in which a client instance negotiates access with an authorization server (AS) through one JSON grant endpoint, with key-bound tokens by default. RFC 9767 defines how resource servers (RS) connect to the AS. With this skill the agent builds or reviews a GNAP client, AS or RS, and designs access rights that also fit OAuth Rich Authorization Requests.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources), with the section it cites. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: client instance, authorization server, resource server, or an RS that derives tokens for another RS.
- Coupling: whether the AS and RS share storage, or the RS uses RFC 9767 discovery, introspection and registration.
- Proofing method: `httpsig`, `mtls`, `jwsd` or `jws`.
- Target version: RFC 9635 (current, the only line), with RFC 9767 for resource server connections. Code written against a pre-RFC `draft-ietf-gnap-core-protocol` revision is upgraded to it. No preview exists. See [`references/versions.md`](references/versions.md).
- Revision: the pinned revisions in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill or when a rule looks out of date, re-read every URL in [Sources](#sources) first, check the RFC Editor for errata or updating RFCs, and update the pins.

## Invariants

1. **Every client request to the AS is signed with the client instance's key**, and every presented key is validated in the request that presents it (RFC 9635 § 2.3, § 7.3).
2. **Tokens are key-bound unless the `bearer` flag is set.** A bound token is sent with `Authorization: GNAP` and a proof of the bound key (RFC 9635 § 2.1.1, § 7.2).
3. **Bearer GNAP tokens go only in the `Authorization` header**, never in a form body or query (RFC 9635 § 7.2).
4. **The interaction hash is always sent by the AS and always validated by the client** (RFC 9635 § 4.2.3).
5. **Continuation tokens only continue grants.** They MUST NOT work at resource servers, and access tokens MUST NOT work for continuation (RFC 9635 § 5).
6. **Clients wait `wait` seconds before continuing**, 5 when absent (RFC 9635 § 3.1).
7. **Access types are compared by exact byte match**, and the AS keeps them collision-free (RFC 9635 § 8).
8. **The `access` returned with a token reflects what the token actually allows** (RFC 9635 § 3.2.1).
9. **JWK keys carry `alg` and `kid`, and `alg` is never `none`** (RFC 9635 § 7.1).
10. **The RS validates both the token and the key proof on every request**, and never reuses a proof result for another message (RFC 9767 § 6.2, § 6.4).
11. **Introspection reports a token active only when every criterion holds**, never for the AS's own continuation or management tokens (RFC 9767 § 3.3, § 2.1.14).
12. **Clients check that a challenge's `referrer` equals the RS URI** before using it (RFC 9635 § 9.1).

## Workflow

1. **Pick the version and fix roles and coupling.** Target RFC 9635 and RFC 9767. Decide who signs what, with which proofing method, and whether the RS validates self-contained tokens or introspects. For code built on a pre-RFC draft, run the upgrade checklist first.
   -> [references/versions.md](references/versions.md)
   ✓ The target is RFC 9635, every wire value comes from its registries, each party has a key and a proofing method, and the RS's validation path is chosen.
2. **Design the access types.** Define each `type`, its fields and their cross-product meaning, plus any reference strings.
   -> [references/access-rights.md](references/access-rights.md)
   ✓ Every type is a URI or otherwise collision-free, and the same definition serves RAR if OAuth is also in use.
3. **Build the grant request and key proof** on the client.
   -> [references/grant-flow.md](references/grant-flow.md)
   ✓ The request has `client.key` with `proof`, and the `httpsig` signature covers `@method`, `@target-uri` and `content-digest` with `tag="gnap"`.
4. **Handle interaction** with the start and finish modes both sides support, and verify the hash.
   -> [references/grant-flow.md](references/grant-flow.md)
   ✓ A finish redirect with a wrong `hash` is rejected before continuation.
5. **Continue and manage the grant**: polling with `wait`, modification, revocation, and token rotation or revocation through `manage`.
   -> [references/grant-flow.md](references/grant-flow.md)
   ✓ Continuation calls carry the continuation token and a fresh proof, and never go faster than `wait`.
6. **Validate tokens at the RS** and answer with `WWW-Authenticate: GNAP` when access is missing.
   -> [references/resource-servers.md](references/resource-servers.md)
   ✓ A valid token with a missing or wrong proof, a token for another RS, and a continuation token are each refused.
7. **Connect the RS to the AS** if they are loosely coupled: discovery, signed introspection, resource registration and derived tokens.
   -> [references/resource-servers.md](references/resource-servers.md)
   ✓ The RS reads `/.well-known/gnap-as-rs`, signs introspection with its own key, and derives downstream tokens instead of forwarding the client's token.
8. **Upgrade** (only when asked). Move a pre-RFC draft implementation to RFC 9635 and RFC 9767 with the checklist.
   -> [references/versions.md](references/versions.md)
   ✓ Every wire value is in an RFC 9635 or RFC 9767 registry, and the same client instance gets the same access as before.

## Verify before done

- [ ] Grant requests, continuation calls and RS calls to the AS are all signed, and the signatures are verified.
- [ ] Bound tokens are refused without a valid proof; bearer tokens are accepted only in the `Authorization` header.
- [ ] The client computes and checks the interaction hash from both nonces, `interact_ref` and the grant endpoint.
- [ ] `access` objects all have `type`, and type comparison is exact with no normalization.
- [ ] Introspection requests carry `resource_server`, and `active: false` responses carry no other fields.
- [ ] Token formats named anywhere come from the GNAP Token Formats registry.

## Reference index

- **`references/versions.md`**: the RFC 9635 line, the pre-RFC drafts, what RFC 9635 fixed, the draft-to-RFC upgrade checklist, and why no preview is listed. Load for step 1.
- **`references/grant-flow.md`**: the grant request, client keys and proofing methods, interaction and its hash, the grant response and errors, continuation, token use and management, and discovery.
- **`references/access-rights.md`**: the `access` array, reference strings, granted versus requested rights, and the comparison with RAR `authorization_details`.
- **`references/resource-servers.md`**: the RFC 9767 token model with JWT and introspection names, token formats, RS-facing discovery, introspection, resource registration, derived tokens and RS validation.

## Related skills

- `oauth` for OAuth 2.0 and 2.1, including Rich Authorization Requests: `npx skills add ScaleDockHQ/scaledock-skills --skill oauth`
- `jwt` for JWT-formatted GNAP tokens and the JOSE verification checklist: `npx skills add ScaleDockHQ/scaledock-skills --skill jwt`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 9635: Grant Negotiation and Authorization Protocol (GNAP)](https://www.rfc-editor.org/rfc/rfc9635): RFC (Proposed Standard), RFC 9635, checked 2026-10-02.
- [RFC 9767: GNAP Resource Server Connections](https://www.rfc-editor.org/rfc/rfc9767): RFC (Proposed Standard), RFC 9767, checked 2026-10-02.
- [RFC 9396: OAuth 2.0 Rich Authorization Requests](https://www.rfc-editor.org/rfc/rfc9396): RFC (Proposed Standard), RFC 9396, checked 2026-10-02.
- [draft-ietf-gnap-core-protocol history](https://datatracker.ietf.org/doc/draft-ietf-gnap-core-protocol/history/): Datatracker page (became RFC 9635), last draft draft-ietf-gnap-core-protocol-20 (2024-03-19), checked 2026-10-05.
