---
name: webdriver
description: >-
  WebDriver: WebDriver is a remote control interface that enables introspection and control of user agents. Covers WebDriver Level 1, WebDriver Level 2 (track preview), WebDriver BiDi (track). Use when writing or reviewing a WebDriver classic or BiDi implementation. Triggers: WebDriver, WebDriver BiDi, Selenium.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# WebDriver

WebDriver is a remote control interface that enables introspection and control of user agents. It provides a platform- and language-neutral wire protocol as a way for out-of-process programs to remotely instruct the behavior of web browsers. Provided is a set of interfaces to discover and manipulate DOM elements in web documents and to control the behavior of a user agent. It is primarily intended to allow web authors to write tests that automate a user agent from a separate controlling process, but may also be used in such a way as to allow in-browser scripts

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when writing or reviewing a WebDriver classic or BiDi implementation.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: WebDriver Level 1 (default); WebDriver Level 2 (preview, posture track: emit only when the user opts in and the posture is build); WebDriver BiDi (default, posture track). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **1. Conformance.** "The key words “ MUST ”, “ MUST NOT ”, “ REQUIRED ”, “ SHOULD ”, “ SHOULD NOT ”, “ RECOMMENDED ”, “ MAY ”, and “ OPTIONAL ” in the normative parts of this document are to be interpreted as described in [ RFC2119 ]."
2. **6.3 Processing Model.** "After such a connection has been established, a remote end MUST run the following steps: Read bytes from the connection until a complete HTTP request can be constructed from the data."
3. **7. Capabilities.** "The following table of standard capabilities enumerates the capabilities each implementation MUST support."
4. **8.1 New Session.** "An intermediary node MAY also define extension capabilities to assist in this process, however, these specific capabilities MUST NOT be forwarded to the endpoint node ."
5. **8.1 New Session.** "An intermediary node MUST forward custom, top-level parameters (i.e."
6. **1.1 Dependencies.** "must be interpreted as required for conforming IDL fragments, as described in the Web IDL specification."
7. **4. Interface.** "Navigator includes NavigatorAutomationInformation ; Note that the NavigatorAutomationInformation interface should not be exposed on WorkerNavigator ."
8. **5. Nodes.** "All remote end node types must be black-box indistinguishable from a remote end , from the point of view of local end , and so are bound by the requirements on a remote end in terms of the wire protocol."

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

- [WebDriver](https://www.w3.org/TR/webdriver1/): Recommendation, webdriver1 REC-webdriver1-20180605 (Recommendation, 2018-06-05), checked 2026-10-06.
- [WebDriver](https://www.w3.org/TR/webdriver2/): Working Draft, webdriver2 WD-webdriver2-20260702 (Working Draft, 2026-07-02), checked 2026-10-06.
- [WebDriver BiDi](https://www.w3.org/TR/webdriver-bidi/): Working Draft, webdriver-bidi WD-webdriver-bidi-20260930 (Working Draft, 2026-09-30), checked 2026-10-06.
