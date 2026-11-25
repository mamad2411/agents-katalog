---
name: ogc-api-features
description: >-
  OGC API Features: Part 1 Core for publishing geospatial features. Covers OGC
  API Features Part 1. Use when publishing geospatial features.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# OGC API Features

External identifier of this OGC® document: http://www.opengis.net/doc/IS/ogcapi-features-1/1.0.1

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when publishing geospatial features.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: OGC API Features Part 1 (default). See `references/versions.md`.
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **OGC API - Features - Part 1: Core corrigendum.** "ANY USE OF THE INTELLECTUAL PROPERTY SHALL BE MADE ENTIRELY AT THE USER’S OWN RISK."
2. **OGC API - Features - Part 1: Core corrigendum.** "IN NO EVENT SHALL THE COPYRIGHT HOLDER OR ANY CONTRIBUTOR OF INTELLECTUAL PROPERTY RIGHTS TO THE INTELLECTUAL PROPERTY BE LIABLE FOR ANY CLAIM, OR ANY DIRECT, SPECIAL, INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY DAMAGES WHATSOEVER RESULTING FROM ANY ALLEGED INFRINGEMENT OR ANY LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR UNDER ANY OTHER LEGAL THEORY, ARISING OUT OF…"
3. **7.2.1. Operation.** "Requirement 1 /req/core/root-op A The server SHALL support the HTTP GET operation at the path / ."
4. **7.2.2. Response.** "Requirement 2 /req/core/root-success A A successful execution of the operation SHALL be reported as a response with a HTTP status code 200 ."
5. **7.2.2. Response.** "B The content of that response SHALL be based upon the OpenAPI 3.0 schema landingPage.yaml and include at least links to the following resources: the API definition (relation type service-desc or service-doc ) /conformance (relation type conformance ) /collections (relation type data ) Recommendations 1 /req/core/root-links A A 200 -response SHOULD include the following links in the links…"
6. **7.3.1. Operation.** "Requirement 3 /req/core/api-definition-op A The URIs of all API definitions referenced from the landing page SHALL support the HTTP GET method."
7. **7.3.2. Response.** "Requirement 4 /req/core/api-definition-success A A GET request to the URI of an API definition linked from the landing page (link relations service-desc or service-doc ) with an Accept header with the value of the link property type SHALL return a document consistent with the requested media type."
8. **7.3.2. Response.** "Recommendation 2 /rec/core/api-definition-oas A If the API definition document uses the OpenAPI Specification 3.0, the document SHOULD conform to the OpenAPI Specification 3.0 requirements class ."

## Workflow

1. **Pick the version.** Use the current line unless a named consumer needs a supported one. Do not author a legacy line. Emit a preview only when its posture is build and the user asked for that draft.
   -> `references/versions.md`
   ✓ The target version is recorded, and it is not a legacy line.
2. **Apply the pinned requirements.** Walk the quotes in `references/requirements.md` and implement each one that applies to the role.
   -> `references/requirements.md`
   ✓ Each applicable quote is either implemented or recorded as out of scope for the role, with the heading it came from.
3. **Upgrade** (only when asked). Follow the upgrade section from the source line to the target.
   -> `references/versions.md`
   ✓ The result cites the target line and no longer depends on a requirement that only the old line stated.

## Verify before done

- [ ] The artifact cites the target line's revision from [Sources](#sources).
- [ ] Every applicable quoted requirement in `references/requirements.md` holds.
- [ ] Nothing from a preview line is emitted unless its posture is build and the user opted in.

## Reference index

- **`references/versions.md`**: every version line, which one to use, and how to upgrade. Load for steps 1 and 3.
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [OGC API Features Part 1](https://docs.ogc.org/is/17-069r4/17-069r4.html): Implementation Standard, OGC API - Features - Part 1: Core corrigendum (Implementation Standard, 2026-10-06), checked 2026-10-06.
