---
name: microsoft-rest-api-guidelines
description: >-
  Microsoft REST API Guidelines: design consistent REST APIs by the Microsoft guidelines. Covers Microsoft REST API Guidelines. Use when designing a REST API. Triggers: REST API Guidelines.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# Microsoft REST API Guidelines

The Microsoft REST API Guidelines from the microsoft/api-guidelines repository. The top-level vNext `Guidelines.md` is now a deprecation notice that points to two companion documents, so this skill reads those: the Microsoft Azure REST API Guidelines (`azure/Guidelines.md`) and the Microsoft Graph REST API Guidelines (`graph/GuidelinesGraph.md`).

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text, labelled with the section they come from. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: Designer or reviewer of an HTTP/REST service API that follows the Azure or the Microsoft Graph guidelines.
- Target version: Microsoft REST API Guidelines (current). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher for a newer revision or version line.

## Invariants

1. **Exactly Once Behavior = Client Retries & Service Idempotency.** "**DO** ensure that _all_ HTTP methods are idempotent."
2. **HTTP Query Parameters and Header Values.** "**DO NOT** fail a request that contains an unrecognized header. Headers may be added by API gateways or middleware and this must be tolerated"
3. **Resource Schema & Field Mutability.** "**DO** create and update resources using PATCH [RFC 5789] with JSON Merge Patch [(RFC 7396)](https://datatracker.ietf.org/doc/html/rfc7396) request body."
4. **Handling Errors.** "**DO** ensure that the top-level error's `code` value is identical to the `x-ms-error-code` header's value."
5. **JSON.** "**DO** use camel case for all JSON field names. Do not upper-case acronyms; use camel case."
6. **API Versioning.** "**DO** use a required query parameter named `api-version` on every operation for the client to specify the API version."
7. **API Versioning.** "**DO NOT** introduce any breaking changes into the service."
8. **Naming.** "**MUST** use lower camel case for _all_ names and namespaces."
9. **Resource modeling patterns.** "**MUST** use a root object with a value property to return a collection."
10. **Behavior modeling.** "**MUST** use PATCH to edit updatable resources."
11. **Error handling.** "The top-level error code MUST match the HTTP response status code description, converted to camelCase, as listed in the [Status Code Registry (iana.org)]"

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

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`: `http-semantics`, `json`, `json-patch`, `odata`, `problem-details`, `openapi`, `google-aip`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [Microsoft Azure REST API Guidelines](https://raw.githubusercontent.com/microsoft/api-guidelines/a7022a299442a8352431874e63ec4dff548a1b81/azure/Guidelines.md): Guidelines, vNext at commit a7022a2, 2026-08-05, checked 2026-10-06.
- [Microsoft Graph REST API Guidelines](https://raw.githubusercontent.com/microsoft/api-guidelines/a7022a299442a8352431874e63ec4dff548a1b81/graph/GuidelinesGraph.md): Guidelines, vNext at commit a7022a2, 2026-08-05, checked 2026-10-06.
