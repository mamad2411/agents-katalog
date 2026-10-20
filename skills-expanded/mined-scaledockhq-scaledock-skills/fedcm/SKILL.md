---
name: fedcm
description: >-
  Federated Credential Management (FedCM): A Web Platform API that allows users to login to websites with their federated accounts in a privacy preserving manner. Covers Federated Credential Management API Level 1 (track). Use when a browser, identity provider or relying party implements federated sign-in. Triggers: FedCM, IdentityCredential, navigator.credentials.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# Federated Credential Management (FedCM)

A Web Platform API that allows users to login to websites with their federated accounts in a privacy preserving manner.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when a browser, identity provider or relying party implements federated sign-in.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Federated Credential Management API Level 1 (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1.5. Clearing the Login Status Map data.** "User agents MUST also clear the Login Status map data when: the user clears all cookies or site settings data The user agent MUST clear the entire map."
2. **2.1.5. Clearing the Login Status Map data.** "the user clears all cookies or all site data for a specific origin The user agent MUST remove all entries that would be affected by the deleted cookies, that is, any entry with an origin to which a deleted cookie could be sent to."
3. **2.1.5. Clearing the Login Status Map data.** "the user agent receives a Clear-Site-Data header with a value of "cookies" or "*" , and the request 's client is not null, and the client’s origin is same origin with the top-level origin while clearing cookies for origin it MUST remove any entries in the Login Status Map where the key is the input origin."
4. **2.2. The connected accounts set.** "If a user clears browsing data for an origin (cookies, localStorage, etc.), the user agent MUST remove all triples with an origin matching the origin from connected accounts set ."
5. **2.3.3. The [[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors) internal method.** "When the IdentityCredential 's [[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors) algorithm is invoked, the user agent MUST execute the following steps."
6. **2.3.3. The [[DiscoverFromExternalSource]](origin, options, sameOriginWithAncestors) internal method.** "The user agent SHOULD wait a random amount of time before the next step if all of the following conditions hold: throwImmediately is false The promise rejection delay was not disabled by user agent automation The user agent has not implemented another way to prevent exposing to the RP whether the user has an account logged in to the RP Note: The intention here is as follows."
7. **2.3.4. Create an IdentityCredential.** "If loginStatus is logged-out , the user agent MUST do one of the following: Return (failure, false)."
8. **2.3.4. Create an IdentityCredential.** "If the user continues, the user agent SHOULD set loginStatus to unknown ."

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

- `openid4vc`, when the work also follows that specification: `npx skills add ScaleDockHQ/scaledock-skills --skill openid4vc`

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Federated Credential Management API](https://www.w3.org/TR/fedcm-1/): First Public Working Draft, fedcm-1 WD-fedcm-1-20240820 (First Public Working Draft, 2024-08-20), checked 2026-10-06.
