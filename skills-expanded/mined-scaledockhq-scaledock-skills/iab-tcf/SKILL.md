---
name: iab-tcf
description: >-
  IAB TCF 2.2: encode and decode Transparency and Consent Framework consent strings. Covers TCF 2.2. Use when encoding a TCF consent string. Triggers: TCF.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# IAB TCF

The IAB Europe Transparency and Consent Framework (TCF) lets Consent Management Platforms (CMPs) record a user's transparency and consent choices in a TC String that vendors in the ad supply chain read. IAB Tech Lab publishes the technical specifications on GitHub; this skill quotes the TCF v2 "Consent string and vendor list formats" and "CMP API" documents.

**Scope.** The TCF Policies from IAB Europe (purposes, legal bases, CMP and vendor obligations) are a separate legal document and are not pinned here; the quotes are the technical specifications only.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: CMP creating TC Strings and providing `__tcfapi`, publisher loading a CMP, or vendor reading TC Strings and the Global Vendor List.
- Target version: TCF 2.2 (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Who should create a TC string.** "Vendors or any other third-party service providers must neither create nor alter TC Strings."
2. **When should a TC string be created.** "A TC String that contains positive consent signals must not be created before clear affirmative action is taken by a user that unambiguously signifies that user's consent."
3. **What are publisher restrictions.** "Vendors must always respect a restriction signal that disallows them the processing for a specific purpose regardless of whether or not they have declared that purpose to be "flexible"."
4. **URL-based services.** "TC Strings must always be propagated as is, and not modified."
5. **Managing conflicting string versions.** "Post 30 September 2023 a TC String created with a policy version set to smaller than 4 will be deemed invalid."
6. **TC String Format.** "There are 3 distinct TC String segments that are joined together on a "dot" character."
7. **Accessing and caching the Global Vendor List.** "All requests for the GVL must now be server-side."
8. **How does the CMP provide the API.** "The function `__tcfapi` **must always be a function** and cannot be any other type, even if only temporarily on initialization - the API must be able to handle calls at all times."
9. **addEventListener.** "The `addEventListener` callback shall be immediately called upon registration with the current TC data, even if the CMP status is `loading` and the CMP has incomplete TC Data, so that the calling script may have access to its registered `listenerId`."
10. **How can scripts on a page determine if there is a CMP present.** "Publishers must load the CMP in a parent (or ancestor) of all iframes that may need to establish a GDPR legal basis."
11. **Requirements for the CMP "stub" API script.** "The stub code must be loaded and executed synchronously before any other scripts that depend on the `__tcfapi` function to be there - this usually means between the `<head></head>` tags of the HTML document - in order to ensure that it can be executed before all calls from third parties."

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
- [ ] A TC String the CMP writes contains the Core and Disclosed Vendors segments and a policy version of at least 4.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification, grouped by source. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `iab-gpp`, `gdpr`, `eprivacy`, `gpc`, `http-cookies`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [IAB Tech Lab - Consent string and vendor list formats v2](https://raw.githubusercontent.com/InteractiveAdvertisingBureau/GDPR-Transparency-and-Consent-Framework/703fc2964ba8fe1086b18a3c509c46a48c1aee1c/TCFv2/IAB%20Tech%20Lab%20-%20Consent%20string%20and%20vendor%20list%20formats%20v2.md): IAB Tech Lab Final specification, Document revision 2.4 (May 2026), commit 703fc29, 2026-07-28, checked 2026-10-06.
- [IAB Tech Lab - CMP API v2](https://raw.githubusercontent.com/InteractiveAdvertisingBureau/GDPR-Transparency-and-Consent-Framework/703fc2964ba8fe1086b18a3c509c46a48c1aee1c/TCFv2/IAB%20Tech%20Lab%20-%20CMP%20API%20v2.md): IAB Tech Lab Final specification, Version 2.2 (February 2026 update), commit 703fc29, 2026-07-28, checked 2026-10-06.
