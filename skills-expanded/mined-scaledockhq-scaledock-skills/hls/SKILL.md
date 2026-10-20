---
name: hls
description: >-
  HLS (RFC 8216): serve and play HTTP Live Streaming playlists and media segments. Covers RFC 8216. Use when serving HTTP Live Streaming. Triggers: HLS.
license: MIT
metadata:
  author: ScaleDockHQ
  version: "1.0.1"
  kind: standard
---

# HLS

RFC 8216: HTTP Live Streaming | RFC Editor Your browser has JavaScript disabled. Most of this site works without JS, but some features require it. If something seems broken please try enabling JavaScript and reloading the page. The JavaScript used by this site is served directly from IETF infrastructure and does not include any code that links to a third party service. Skip to content

The publisher of the pinned text is named in [Sources](#sources). With this skill the agent applies that text: when serving HTTP Live Streaming.

**Follow the workflow below step by step.** Every rule here comes from a source in [Sources](#sources). Quoted requirements are sentences taken from the pinned text. When a rule and the pinned source disagree, the source wins; when the source has a newer revision than the pin, follow the refresh steps.

## Inputs (fill in, or ask before starting)

- Role: producer or consumer of this specification.
- Target version: RFC 8216 (default). See [`references/versions.md`](references/versions.md).
- Revision: the pinned revision in [Sources](#sources), unless the user names another.
- Sources: when refreshing this skill, re-read every URL in [Sources](#sources) and check the publisher index for a newer revision or version line.

## Invariants

1. **RFC 8216 : HTTP Live Streaming.** "Data SHOULD be carried over HTTP [ RFC7230 ], but, in general, a URI can specify any protocol that can reliably transfer the specified resource on demand."
2. **RFC 8216 : HTTP Live Streaming.** "The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in BCP 14 [ RFC2119 ] [ RFC8174 ] when, and only when, they appear in all capitals, as shown here."
3. **RFC 8216 : HTTP Live Streaming.** "Each Media Segment MUST carry the continuation of the encoded bitstream from the end of the segment with the previous Media Sequence Number, where values in a series such as timestamps and Continuity Counters MUST continue uninterrupted."
4. **RFC 8216 : HTTP Live Streaming.** "Any Media Segment that contains video SHOULD include enough information to initialize a video decoder and decode a continuous set of frames that includes the final frame in the Segment; network efficiency is optimized if there is enough information in the Segment"
5. **RFC 8216 : HTTP Live Streaming.** "For example, any Media Segment containing H.264 video SHOULD contain an Instantaneous Decoding Refresh (IDR); frames prior to the first IDR will be downloaded but possibly discarded."
6. **RFC 8216 : HTTP Live Streaming.** "Supported Media Segment Formats All Media Segments MUST be in a format described in this section."
7. **RFC 8216 : HTTP Live Streaming.** "The Media Initialization Section MUST NOT contain sample data."
8. **RFC 8216 : HTTP Live Streaming.** "Transport Stream Segments MUST contain a single MPEG-2 Program; playback of Multi-Program Transport Streams is not defined."

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

- [RFC 8216](https://www.rfc-editor.org/rfc/rfc8216): RFC, RFC 8216, fetched 2026-10-06 (RFC, 2026-10-06), checked 2026-10-06.
