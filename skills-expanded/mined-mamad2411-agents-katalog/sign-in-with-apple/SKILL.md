---
name: sign-in-with-apple
description: >-
  Sign in with Apple: sign users in with their Apple Account and verify Apple identity tokens. Covers Sign in with Apple. Use when signing users in with Apple. Triggers: Sign in with Apple.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Sign in with Apple

Sign in with Apple lets users sign in to apps and websites with their Apple Account. Apple documents the flow, the REST endpoints at `appleid.apple.com` and the server-to-server notifications in its developer documentation; this skill quotes those pages, read from Apple's documentation JSON.

**Scope.** Apple publishes Sign in with Apple as developer documentation, not as a versioned specification. The pages are JavaScript-rendered; the pins are the documentation JSON that backs them. The flow follows OAuth 2.0 and OpenID Connect; install those skills for the general protocol rules.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: App or website signing users in (relying party), its app server verifying tokens, or the server endpoint receiving Sign in with Apple notifications.
- Target version: Sign in with Apple (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Authenticate the user and request information.** "Initialize an authentication session with your app server and associate a client session with an ID token using the `nonce` value."
2. **Verify the identity token.** "Verify the JWS E256 signature using the server's public key"
3. **Verify the identity token.** "Verify the `nonce` for the authentication"
4. **Verify the identity token.** "Verify that the `iss` field contains `https://appleid.apple.com`"
5. **Verify the identity token.** "Verify that the `aud` field is the developer's `client_id`"
6. **Verify the identity token.** "Verify that the time is earlier than the `exp` value of the token"
7. **Obtain a refresh token.** "You may verify the refresh token up to once a day to confirm that the user's Apple Account on that device is still in good standing with Apple's servers. Apple's servers may throttle your call if you attempt to verify a user's Apple Account more than once a day."
8. **Send the required query parameters, client_id.** "The identifier must not include your Team ID, to help mitigate the possibility of exposing sensitive data to the end user."
9. **Send the required query parameters, redirect_uri.** "It must include a domain name and can't be an IP address or `localhost`, and must not contain a fragment identifer (#)."
10. **Send the required query parameters, response_type.** "Requesting only `id_token` is unsupported. When requesting `id_token`, `response_mode` must be either `fragment` or `form_post`."
11. **Send the required query parameters, response_mode.** "If you requested any scopes, the value must be `form_post`."
12. **Decode and validate the notifications.** "After your server receives a notification, examine the JWS payload and use the algorithm specified in the header's `alg` parameter to validate the signature."

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
- [ ] The server rejects an identity token whose signature, `iss`, `aud`, `exp` or `nonce` check fails.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `openid-connect`, `oauth`, `jwt`, `apple-app-site-association`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Authenticating users with Sign in with Apple](https://developer.apple.com/tutorials/data/documentation/signinwithapple/authenticating-users-with-sign-in-with-apple.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [Verifying a user](https://developer.apple.com/tutorials/data/documentation/signinwithapple/verifying-a-user.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [Token validation (Sign in with Apple REST API)](https://developer.apple.com/tutorials/data/documentation/signinwithapplerestapi/generate-and-validate-tokens.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [Incorporating Sign in with Apple into other platforms](https://developer.apple.com/tutorials/data/documentation/signinwithapple/incorporating-sign-in-with-apple-into-other-platforms.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
- [Processing changes for Sign in with Apple accounts](https://developer.apple.com/tutorials/data/documentation/signinwithapple/processing-changes-for-sign-in-with-apple-accounts.json): Apple Developer Documentation, Apple Developer Documentation JSON, read 2026-10-06, checked 2026-10-06.
