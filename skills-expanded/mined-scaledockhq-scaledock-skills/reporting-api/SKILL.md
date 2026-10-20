---
name: reporting-api
description: >-
  Reporting API: This document defines a generic reporting framework which allows web developers to associate a set of named reporting endpoints with an origin. Covers Reporting API Level 1 (track), Network Error Logging (track). Use when generating, delivering or collecting browser reports, including network errors. Triggers: Reporting API, Report-To, Network Error Logging, NEL.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Reporting API

This document defines a generic reporting framework which allows web developers to associate a set of named reporting endpoints with an origin. Various platform features can use these endpoints to deliver feature-specific reports in a consistent manner.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when generating, delivering or collecting browser reports, including network errors.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Reporting API Level 1 (default, posture track); Network Error Logging (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **3.1. Document configuration.** "Each object implementing WindowOrWorkerGlobalScope has an endpoints list, which is a list of endpoints , each of which MUST have a distinct name ."
2. **3.2. The Reporting-Endpoints HTTP Response Header Field.** "If its value is not a valid URI-reference, that endpoint member MUST be ignored."
3. **3.2. The Reporting-Endpoints HTTP Response Header Field.** "Moreover, the URL that the member’s value represents MUST be potentially trustworthy [SECURE-CONTEXTS] ."
4. **3.5. Report Delivery.** "That said, a user agent SHOULD make an effort to deliver reports as soon as possible after queuing, as a report’s data might be significantly more useful in the period directly after its generation than it would be a day or a week later."
5. **5.1. Delivery.** "The user agent SHOULD attempt to deliver reports as soon as possible to provide feedback to developers as quickly as possible."
6. **5.1. Delivery.** "For instance, the user agent SHOULD prioritize the transmission of reporting data lower than other network traffic."
7. **5.2. Garbage Collection.** "Periodically, the user agent SHOULD walk through the cached reports and endpoints , and discard those that are no longer relevant."
8. **8.1. Capability URLs.** "Specifications which extend this API and which include any URLs in a report’s body SHOULD require that they be similarly stripped."

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

- [Reporting API](https://www.w3.org/TR/reporting-1/): Working Draft, reporting-1 WD-reporting-1-20250611 (Working Draft, 2025-06-11), checked 2026-10-06.
- [Network Error Logging](https://www.w3.org/TR/network-error-logging/): Working Draft, network-error-logging WD-network-error-logging-20250505 (Working Draft, 2025-05-05), checked 2026-10-06.
