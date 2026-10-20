---
name: iab-gpp
description: >-
  IAB Global Privacy Platform: encode and decode GPP strings that carry privacy signals across jurisdictions. Covers Global Privacy Platform. Use when encoding a Global Privacy Platform string. Triggers: GPP.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# IAB GPP

The IAB Tech Lab Global Privacy Platform (GPP) carries privacy and consent signals for several jurisdictions in one GPP String: a header that lists the section IDs, followed by one discrete section per framework (for example IAB Europe TCF or the US state sections), joined on `~`. IAB Tech Lab publishes the specifications on GitHub; this skill quotes the Core "Consent String Specification" and "CMP API Specification".

**Scope.** Each discrete section (TCF EU, TCF Canada, MSPA US National and the US state sections) has its own technical specification under `Sections/` in the same repository; those are not pinned here.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: CMP or publisher creating GPP Strings and providing `__gpp`, or vendor and ad tech service reading GPP Strings and the `gpp` and `gpp_sid` URL parameters.
- Target version: Global Privacy Platform (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Who should create a GPP String.** "Vendors or any other third-party service providers must neither create nor alter GPP Strings."
2. **GPP String Format.** "The GPP string is comprised of distinct sections joined together on a "~" (tilde) character."
3. **Header.** "The header is always required and comes first."
4. **Header Encoding.** "The IDs must be represented in the order the related sections appear in the string."
5. **Creating a GPP String.** "For sections that use a different encoding mechanism, ensure that the data is websafe and does not include the "~" (tilde) character or the "." (dot) character."
6. **URL-based services.** "GPP Strings must always be propagated as is, and not modified."
7. **How does the CMP provide the API.** "If a CMP cannot immediately respond to a query, the CMP must queue all calls to the function and execute them later. The CMP must execute the commands in the same order in which the function was called."
8. **How does the CMP provide the API.** "All generic commands must always be executed immediately without any asynchronous logic and call the supplied callback function immediately."
9. **EventListener.** "A call to the `addEventListener` command must always trigger an immediate call to the callback function. When registering new event listeners, the CMP (and stub) must therefore generate new listenerIds for each call to this command."
10. **EventListener.** "Whenever the CMP starts to change or is about to change any of the existing sections or is processing user input for an existing GPP string, it **must always** first set "signalStatus" to "not ready" and fire the corresponding event."

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
- [ ] A GPP String the CMP writes starts with the header, lists its section IDs in the order the sections appear, and joins sections on `~`.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `iab-tcf`, `ccpa-cpra`, `gpc`, `gdpr`, `base-encodings`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Global Privacy Protocol String (Core Consent String Specification)](https://raw.githubusercontent.com/InteractiveAdvertisingBureau/Global-Privacy-Platform/03fdf0332d261ee896b77d7f9a10edde1498fc7c/Core/Consent%20String%20Specification.md): IAB Tech Lab Final specification, Version 1.0 (2023-11-03 update), commit 03fdf03, 2026-08-06, checked 2026-10-06.
- [GPP CMP API Specification](https://raw.githubusercontent.com/InteractiveAdvertisingBureau/Global-Privacy-Platform/03fdf0332d261ee896b77d7f9a10edde1498fc7c/Core/CMP%20API%20Specification.md): IAB Tech Lab Final specification, Version 1.1 (June 2023), commit 03fdf03, 2026-08-06, checked 2026-10-06.
