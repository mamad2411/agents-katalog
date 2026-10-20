---
name: webmention
description: >-
  Webmention: Webmention is a simple way to notify any URL when you mention it on your site. Covers Webmention. Use when sending or receiving a webmention. Triggers: Webmention.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# Webmention

Webmention is a simple way to notify any URL when you mention it on your site. From the receiver's perspective, it's a way to request notifications when other sites mention it.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when sending or receiving a webmention.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: Webmention (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2. Conformance.** "The key words " MUST ", " MUST NOT ", " REQUIRED ", " SHALL ", " SHALL NOT ", " SHOULD ", " SHOULD NOT ", " RECOMMENDED ", " MAY ", and " OPTIONAL " in this document are to be interpreted as described in [ RFC2119 ]."
2. **3.1.2 Sender discovers receiver Webmention endpoint.** "The sender MUST fetch the target URL (and follow redirects [ FETCH ]) and check for an HTTP Link header [ RFC5988 ] with a rel value of webmention ."
3. **3.1.2 Sender discovers receiver Webmention endpoint.** "If the content type of the document is HTML, then the sender MUST look for an HTML <link> and <a> element with a rel value of webmention ."
4. **3.1.2 Sender discovers receiver Webmention endpoint.** "Senders MUST support all three options and fall back in this order."
5. **3.1.2 Sender discovers receiver Webmention endpoint.** "The endpoint MAY be a relative URL, in which case the sender MUST resolve it relative to the target URL according to [ URL ]."
6. **3.1.2 Sender discovers receiver Webmention endpoint.** "The endpoint MAY contain query string parameters, which MUST be preserved as query string parameters and MUST NOT be sent as POST body parameters when sending the Webmention request."
7. **3.1.3 Sender notifies receiver.** "The sender MUST post x-www-form-urlencoded [ HTML5 ] source and target parameters to the Webmention endpoint, where source is the URL of the sender's page containing a link, and target is the URL of the page being linked to."
8. **3.1.3 Sender notifies receiver.** "Note that if the Webmention endpoint URL contains query string parameters, the query string parameters MUST be preserved, and MUST NOT be sent in the POST body."

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

- [Webmention](https://www.w3.org/TR/webmention/): Recommendation, webmention REC-webmention-20170112 (Recommendation, 2017-01-12), checked 2026-10-06.
