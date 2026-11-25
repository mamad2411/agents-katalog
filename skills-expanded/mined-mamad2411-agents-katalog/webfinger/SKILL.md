---
name: webfinger
description: >-
  WebFinger (RFC 7033): discover information about people and resources from a URI. Covers RFC 7033 WebFinger. Use when discovering a resource with WebFinger. Triggers: WebFinger, RFC 7033.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# WebFinger

WebFinger

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when discovering a resource with WebFinger.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 7033 WebFinger (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 7033 § 4.** "The path component of a WebFinger URI MUST be the well-known path "/.well-known/webfinger"."
2. **RFC 7033 § 4.1.** "The query component MUST contain a "resource" parameter and MAY contain one or more "rel" parameters."
3. **RFC 7033 § 4.2.** "A client MUST query the WebFinger resource using HTTPS only."
4. **RFC 7033 § 4.2.** "If the client determines that the resource has an invalid certificate, the resource returns a 4xx or 5xx status code, or if the HTTPS connection cannot be established for any reason, then the client MUST accept that the WebFinger query has failed and MUST NOT attempt to reissue the WebFinger request using HTTP over a non-secure connection."
5. **RFC 7033 § 4.2.** "A WebFinger resource MUST return a JRD as the representation for the resource if the client requests no other supported format explicitly via the HTTP "Accept" header."
6. **RFC 7033 § 4.2.** "A WebFinger resource MAY redirect the client; if it does, the redirection MUST only be to an "https" URI and the client MUST perform certificate validation again when redirected."
7. **RFC 7033 § 4.4.** "When processing a JRD, the client MUST ignore any unknown member and not treat the presence of an unknown member as an error."
8. **RFC 7033 § 5.** "The current best practice is to make resources available to browsers through Cross-Origin Resource Sharing (CORS) [7], and servers MUST include the Access-Control-Allow-Origin HTTP header in responses."
9. **RFC 7033 § 9.1.** "Clients MUST verify that the certificate used on an HTTPS connection is valid (as defined in [12]) and accept a response only if the certificate is valid."
10. **RFC 7033 § 9.2.** "WebFinger MUST NOT be used to provide any personal data unless publishing that data via WebFinger by the relevant service was explicitly authorized by the person whose information is being shared."

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
- **`references/requirements.md`**: quotes taken from the pinned specification. Load for step 2.

## Related skills

Install related spec skills by name with `npx skills add ScaleDockHQ/scaledock-skills --skill <name>`.

## Sources

Status uses the publishing body's own maturity term. Checked is the date the source was last read.

- [RFC 7033 WebFinger](https://www.rfc-editor.org/rfc/rfc7033.html): PROPOSED STANDARD, RFC 7033 (PROPOSED STANDARD, September ), checked 2026-10-06.
