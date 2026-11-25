---
name: smart-on-fhir
description: >-
  SMART App Launch: launch apps against a FHIR server. Covers SMART App Launch 2.2. Use when launching a SMART on FHIR app.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# SMART App Launch

The HL7 SMART App Launch Implementation Guide (v2.2.0, STU 2.2, based on FHIR R4): how apps launch from an EHR or standalone, obtain OAuth 2.0 authorization with PKCE, request scopes and launch context, authenticate with asymmetric keys, run as backend services, and discover server capabilities through .well-known/smart-configuration, read from the guide's published pages.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: SMART app (public or confidential client), backend service, or EHR authorization server and FHIR resource server.
- Target version: SMART App Launch 2.2 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **App protection.** "Apps SHALL ensure that when protocol steps include transmission of sensitive information (authentication secrets, authorization codes, tokens), transmission is ONLY to authenticated servers, over TLS-secured channels."
2. **Considerations for PKCE Support.** "All SMART apps SHALL support Proof Key for Code Exchange (PKCE)."
3. **Considerations for PKCE Support.** "SMART servers SHALL support the S256 code_challenge_method and SHALL NOT support the plain method."
4. **Obtain authorization code, Request.** "The app SHALL use an unpredictable value for the state parameter with at least 122 bits of entropy (e.g., a properly configured random uuid is suitable)."
5. **Obtain authorization code, Response.** "The app SHALL validate the value of the state parameter upon return to the redirect URL and SHALL ensure that the state value is securely tied to the user's current session (e.g., by relating the state value to a session identifier issued by the app)."
6. **Access FHIR API, Response.** "The resource server SHALL validate the access token and ensure that it has not expired and that its scope covers the requested resource."
7. **Scopes for requesting identity data.** "A SMART app SHALL NOT pass the auth_time claim or max_age parameter to a server that does not support receiving them."
8. **Registering a client (communicating public keys).** "The client SHALL protect the associated private key from unauthorized disclosure and corruption."
9. **Authenticating to the Token endpoint, Signature Verification.** "The FHIR authorization server SHALL NOT cache a JWKS for longer than the client's cache-control header indicates."
10. **FHIR Authorization Endpoint and Capabilities Discovery using a Well-Known Uniform Resource Identifiers (URIs).** "FHIR endpoints requiring authorization SHALL serve a JSON document at the location formed by appending /.well-known/smart-configuration to their base URL."
11. **Metadata.** "The S256 method SHALL be included in this list, and the plain method SHALL NOT be included in this list."
12. **Obtain access token, Evaluate Requested Access.** "Once the client has been authenticated, the FHIR authorization server SHALL mediate the request to assure that the scope requested is within the scope pre-authorized to the client."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> [`references/versions.md`](references/versions.md)
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in [`references/requirements.md`](references/requirements.md) and implement each one that applies to the role.
   -> [`references/requirements.md`](references/requirements.md)
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the section it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> [`references/versions.md`](references/versions.md)
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in [`references/requirements.md`](references/requirements.md) holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `fhir`, `oauth`, `openid-connect`, `jwt`, `cds-hooks`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [SMART App Launch 2.2: App Launch](https://hl7.org/fhir/smart-app-launch/STU2.2/app-launch.html): Standard for Trial Use, SMART App Launch v2.2.0 (STU 2.2), based on FHIR R4, checked 2026-10-06.
- [SMART App Launch 2.2: Scopes and Launch Context](https://hl7.org/fhir/smart-app-launch/STU2.2/scopes-and-launch-context.html): Standard for Trial Use, SMART App Launch v2.2.0 (STU 2.2), based on FHIR R4, checked 2026-10-06.
- [SMART App Launch 2.2: Asymmetric (public key) client authentication](https://hl7.org/fhir/smart-app-launch/STU2.2/client-confidential-asymmetric.html): Standard for Trial Use, SMART App Launch v2.2.0 (STU 2.2), based on FHIR R4, checked 2026-10-06.
- [SMART App Launch 2.2: Conformance](https://hl7.org/fhir/smart-app-launch/STU2.2/conformance.html): Standard for Trial Use, SMART App Launch v2.2.0 (STU 2.2), based on FHIR R4, checked 2026-10-06.
- [SMART App Launch 2.2: Backend Services](https://hl7.org/fhir/smart-app-launch/STU2.2/backend-services.html): Standard for Trial Use, SMART App Launch v2.2.0 (STU 2.2), based on FHIR R4, checked 2026-10-06.
