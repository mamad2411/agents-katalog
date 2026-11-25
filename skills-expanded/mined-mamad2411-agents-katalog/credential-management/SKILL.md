---
name: credential-management
description: >-
  Credential Management: This specification describes an imperative API enabling a website to request a user’s credentials from a user agent, and to help the user agent correctly store user credentials for future use. Covers Credential Management Level 1 (track), A Well-Known URL for Changing Passwords (track), A Well-Known URL for Relying Party Passkey Endpoints Level 1 (track). Use when storing, retrieving or mediating credentials, or publishing the change-password and passkey well-known URLs. Triggers: Credential Management, navigator.credentials, change-password, passkey-endpoints.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Credential Management

This specification describes an imperative API enabling a website to request a user’s credentials from a user agent, and to help the user agent correctly store user credentials for future use.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when storing, retrieving or mediating credentials, or publishing the change-password and passkey well-known URLs.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Credential Management Level 1 (default, posture track); A Well-Known URL for Changing Passwords (default, posture track); A Well-Known URL for Relying Party Passkey Endpoints Level 1 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1. Infrastructure.** "User agents MUST internally provide a credential store , which is a vendor-specific, opaque storage mechanism to record which credentials have been effective ."
2. **2.2.1. Credential Internal Methods.** "Unless otherwise specified, each interface object created for interfaces which inherit from Credential MUST provide implementations for at least one of these internal methods, overriding Credential ’s default implementations, as appropriate for the credential type."
3. **2.2.1.4. [[Create]] internal method.** "This algorithm MUST be invoked from a task ."
4. **2.2.2. CredentialUserData Mixin.** "This URL MUST be an potentially trustworthy URL ."
5. **2.3. navigator.credentials.** "partial interface Navigator { [ SecureContext , SameObject ] readonly attribute CredentialsContainer credentials ; }; The credentials attribute MUST return the CredentialsContainer associated with the active document ’s browsing context ."
6. **2.3. navigator.credentials.** "store(credential) When store() is called, the user agent MUST return the result of executing Store a Credential on credential ."
7. **2.3. navigator.credentials.** "create(options) When create() is called, the user agent MUST return the result of executing Create a Credential on options ."
8. **2.3. navigator.credentials.** "preventSilentAccess() When preventSilentAccess() is called, the user agent MUST return the result of executing Prevent Silent Access on the current settings object ."

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

- `webauthn`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill webauthn`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Credential Management Level 1](https://www.w3.org/TR/credential-management-1/): Working Draft, credential-management-1 WD-credential-management-1-20260903 (Working Draft, 2026-09-03), checked 2026-10-06.
- [A Well-Known URL for Changing Passwords](https://www.w3.org/TR/change-password-url/): Working Draft, change-password-url WD-change-password-url-20240603 (Working Draft, 2024-06-03), checked 2026-10-06.
- [A Well-Known URL for Relying Party Passkey Endpoints](https://www.w3.org/TR/passkey-endpoints-1/): Working Draft, passkey-endpoints-1 WD-passkey-endpoints-1-20260114 (Working Draft, 2026-01-14), checked 2026-10-06.
