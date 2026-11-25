---
name: oembed
description: >-
  oEmbed: oEmbed is a format for allowing an embedded representation of a URL on third party sites. Covers oEmbed. Use when embedding a resource with oEmbed. Triggers: oEmbed.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.0"
  kind: standard
---

# oEmbed

oEmbed is a format for allowing an embedded representation of a URL on third party sites. The simple API allows a website to display embedded content (such as photos or videos) when a user posts a link to that resource, without having to parse the resource directly.

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when embedding a resource with oEmbed.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: oEmbed (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **2.1. Configuration.** "Providers must specify one or more URL scheme and API endpoint pairs."
2. **2.1. Configuration.** "Some examples: http://www.flickr.com/photos/* OK http://www.flickr.com/photos/*/foo/ OK http://_.flickr.com/photos/_ OK http://_.com/photos/_ NOT OK _://www.flickr.com/photos/_ NOT OK The API endpoint must point to a URL with either HTTP or HTTPS scheme which implements the API described below."
3. **2.2. Consumer Request.** "Requests sent to the API endpoint must be HTTP GET requests, with all arguments sent as query parameters."
4. **2.2. Consumer Request.** "All arguments must be urlencoded (as per RFC 1738)."
5. **2.2. Consumer Request.** "For supported resource types, this parameter must be respected by providers."
6. **2.2. Consumer Request.** "When specified, the provider must return data in the request format, else return an error (see below for error codes)."
7. **2.2. Consumer Request.** "Providers should ignore all other arguments it doesn't expect."
8. **2.2. Consumer Request.** "When a provider publishes a URL scheme and API endpoint pair, they should clearly state whether the format is implicit in the endpoint or if it needs to be passed as an argument."

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

- [oEmbed](https://oembed.com/): Specification, oEmbed, fetched 2026-10-06 (Specification, 2026-10-06), checked 2026-10-06.
