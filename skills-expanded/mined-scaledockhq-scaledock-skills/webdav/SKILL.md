---
name: webdav
description: >-
  WebDAV (RFC 4918): implement distributed authoring over HTTP, plus CalDAV and CardDAV. Covers RFC 4918 HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV), RFC 4791 Calendaring Extensions to WebDAV (CalDAV), RFC 6352 CardDAV: vCard Extensions to Web Distributed Authoring and Versioning (WebDAV). Use when implementing WebDAV, CalDAV or CardDAV. Triggers: WebDAV, CalDAV, CardDAV.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.1.0"
  kind: standard
---

# HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)

HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when implementing WebDAV, CalDAV or CardDAV.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 4918 HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV) (default); RFC 4791 Calendaring Extensions to WebDAV (CalDAV) (default); RFC 6352 CardDAV: vCard Extensions to Web Distributed Authoring and Versioning (WebDAV) (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 4918 § 6.1.** "A server MUST NOT create conflicting locks on a resource."
2. **RFC 4918 § 6.4.** "When a locked resource is modified, a server MUST check that the authenticated principal matches the lock creator (in addition to checking for valid lock token submission)."
3. **RFC 4918 § 6.6.** "Clients MUST assume that locks can arbitrarily disappear at any time, regardless of the value given in the Timeout header."
4. **RFC 4918 § 8.1.** "Servers MUST return authorization errors in preference to other errors."
5. **RFC 4918 § 8.2.** "If a server receives XML that is not well-formed, then the server MUST reject the entire request with a 400 (Bad Request)."
6. **RFC 4918 § 9.2.** "Servers MUST process PROPPATCH instructions in document order (an exception to the normal rule that ordering is irrelevant)."
7. **RFC 4918 § 17.** "A recipient of a WebDAV message with an XML body MUST NOT validate the XML document according to any hard-coded or dynamically-declared DTD."
8. **RFC 4918 § 20.1.** "Since Basic authentication for HTTP/1.1 performs essentially clear text transmission of a password, Basic authentication MUST NOT be used to authenticate a WebDAV client to a server unless the connection is secure."
9. **RFC 4791 § 4.1.** "The UID property value of the calendar components contained in a calendar object resource MUST be unique in the scope of the calendar collection in which they are stored."
10. **RFC 6352 § 5.1.** "Address object resources contained in address book collections MUST contain a single vCard component only."

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

- [RFC 4918 HTTP Extensions for Web Distributed Authoring and Versioning (WebDAV)](https://www.rfc-editor.org/rfc/rfc4918.html): PROPOSED STANDARD, RFC 4918 (PROPOSED STANDARD, June 2007), checked 2026-10-06.
- [RFC 4791 Calendaring Extensions to WebDAV (CalDAV)](https://www.rfc-editor.org/rfc/rfc4791.html): PROPOSED STANDARD, RFC 4791 (PROPOSED STANDARD, March 2007), checked 2026-10-06.
- [RFC 6352 CardDAV: vCard Extensions to Web Distributed Authoring and Versioning (WebDAV)](https://www.rfc-editor.org/rfc/rfc6352.html): PROPOSED STANDARD, RFC 6352 (PROPOSED STANDARD, August 201), checked 2026-10-06.
