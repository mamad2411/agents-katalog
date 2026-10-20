---
name: micropub
description: >-
  Micropub: The Micropub protocol is used to create, update and delete posts on one's own domain using third-party clients. Covers Micropub. Use when creating posts with Micropub. Triggers: Micropub.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Micropub

The Micropub protocol is used to create, update and delete posts on one's own domain using third-party clients. Web apps and native apps (e.g., iPhone, Android) can use Micropub to post and edit articles, short notes, comments, likes, photos, events or other kinds of posts on your own website.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when creating posts with Micropub.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Micropub (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words " MUST ", " MUST NOT ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", " SHOULD NOT ", " RECOMMENDED ", " MAY ", and " OPTIONAL " in this document are to be interpreted as described in [ RFC2119 ]."
2. **2.1 Conformance Classes.** "All implementations MUST support UTF-8 encoding."
3. **2.1.1 Publishing Clients.** "A conforming Micropub client that creates posts: MUST support sending x-www-form-urlencoded requests MUST support the [ h-entry ] vocabulary If the client creates posts by uploading file attachments, it MUST check for the presence of a Media Endpoint and if present, send the file there instead of to the Micropub endpoint SHOULD handle server error messages gracefully, presenting helpful messages…"
4. **2.1.2 Editing Clients.** "A conforming Micropub client that edits posts: MUST support sending JSON-encoded requests MUST support the [ h-entry ] vocabulary"
5. **2.1.3 Servers.** "A conforming Micropub server: MUST support both header and form parameter methods of authentication MUST support creating posts with the [ h-entry ] vocabulary MUST support creating posts using the x-www-form-urlencoded syntax SHOULD support updating and deleting posts Servers that support updating posts MUST support JSON syntax and the source content query Servers that do not specify a Media…"
6. **3.1 Overview.** "When a response body is necessary, it SHOULD be returned as a [ JSON ] encoded object."
7. **3.1.1 Form-Encoded and Multipart Requests.** "Specifically, this means in order to send multiple values for a given property, you MUST append square brackets [] to the property name."
8. **3.2 Reserved Properties.** "The server MUST NOT store the access_token property in the post."

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

- [Micropub](https://www.w3.org/TR/micropub/): Recommendation, micropub REC-micropub-20170523 (Recommendation, 2017-05-23), checked 2026-10-06.
