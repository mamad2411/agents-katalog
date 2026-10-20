---
name: uma
description: >-
  User-Managed Access: This specification defines a means for a client, representing a requesting party, to use a permission ticket to request an OAuth 2.0 access token to gain access to a protected resource asynchronously from the time a resource owner authorizes access. Covers UMA 2.0 Grant, UMA 2.0 Federated Authorization. Use when granting and federating access with UMA 2.0. Triggers: UMA, User-Managed Access.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# User-Managed Access

This specification defines a means for a client, representing a requesting party, to use a permission ticket to request an OAuth 2.0 access token to gain access to a protected resource asynchronously from the time a resource owner authorizes access.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when granting and federating access with UMA 2.0.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: UMA 2.0 Grant (default); UMA 2.0 Federated Authorization (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1.1 Notational Conventions.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC2119] ."
2. **1.1 Notational Conventions.** "Any entity receiving or retrieving a JSON data structure SHOULD ignore extension parameters it is unable to understand."
3. **2. Authorization Server Metadata.** "The authorization server MUST make a discovery document available."
4. **2. Authorization Server Metadata.** "The structure of the discovery document MUST conform to that defined in [OAuthMeta] ."
5. **2. Authorization Server Metadata.** "The discovery document MUST be available at an endpoint formed by concatenating the string /.well-known/uma2-configuration to the issuer metadata value defined in [OAuthMeta] , using the well-known URI syntax and semantics defined in [RFC5785] ."
6. **2. Authorization Server Metadata.** "As discussed in Section 4 , an authorization server supporting a profile or extension related to UMA SHOULD supply the specification's identifying URI (if any) here."
7. **2. Authorization Server Metadata.** "If the authorization server supports dynamic client registration, it MUST allow client applications to register claims_redirect_uri metadata, as defined in Section 3.3.2 , using the following metadata field: claims_redirect_uris OPTIONAL."
8. **3.2 Resource Server Responds to Client's Tokenless Access Attempt.** "The resource server MUST obtain a permission ticket from the authorization server to provide in its response, but the means of doing so is outside the scope of this specification."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [UMA 2.0 Grant](https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-grant-2.0.html): Recommendation, UMA 2.0 Grant for OAuth 2.0, fetched 2026-10-06 (Recommendation, 2026-10-06), checked 2026-10-06.
- [UMA 2.0 Federated Authorization](https://docs.kantarainitiative.org/uma/wg/rec-oauth-uma-federated-authz-2.0.html): Recommendation, UMA 2.0 Federated Authorization, fetched 2026-10-06 (Recommendation, 2026-10-06), checked 2026-10-06.
