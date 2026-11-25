---
name: whiteboard-react-to-share
description: When the user shares a note or capture via a [USER_SHARED] trigger or [Spotlight Context], naturally bring it up in conversation (getting an image description via whiteboard_describe first if needed) and voice your opinion.
allowed_tools:
  - whiteboard_describe
  - whiteboard_extract_links
  - opsidian_read
  - knowledge_read
execution_mode: inline
examples:
  - "What do you think of that note I just shared?"
  - "Take a look at this screen for me."
  - "[USER_SHARED] handling"
---

# Whiteboard: React to Share — React naturally to a share

Use this skill when the user has explicitly shared a note/image/screen capture.

## Two trigger forms

1. **Immediate trigger** — a synthetic prompt for a single turn that starts with `[USER_SHARED] {json...}`.
   - Read the JSON's `title`, `kind`, `source_filename`, `excerpt`, `seen_before`, and `attachments_count`, and react naturally.
2. **Persistent context** — the `[Spotlight Context]` block is included in the system prompt every turn. Active items persist until they expire (~30 minutes).

## Reaction Ladder

Decide in order:

### Step 1: Check `seen_before`

- If `seen_before == true`: "you shared that [title] again that we saw last time" — **don't act as if you're seeing it for the first time**. Pick up the prior context.
- If `seen_before == false`: take it as new info, e.g. "oh, this is material/an image I haven't seen before".

Next to each item in the `[Spotlight Context]` block there is a marker like `⚑ previously seen — 3× read, 7× injected` or `⚑ first time / 처음 보는 자료`. **Ignoring this marker breaks the persona.**

### Step 2: Handle attachments

| Situation | Action |
|---|---|
| No attachment + sufficient `excerpt` | Voice your opinion from the excerpt alone. No extra tool call needed. |
| Image attachment + **your model is vision-capable** | It's attached to the system prompt as an image content block → look at it directly and react. |
| Image attachment + **your model is NOT vision-capable** | **You must call `whiteboard_describe(capture_id="...")`** and react based on that caption. Don't *guess* at the image. |
| Body appears to have many links (lots of URLs in the excerpt) | Call **`whiteboard_extract_links(filename="...")`** → point out just 1–2 key URLs to the user. |

The `capture_id` is in the `capture_id` field of the `[USER_SHARED]` payload.

### Step 3: Read if you need more of the body

If you feel the excerpt is insufficient (e.g. a decision/summary/number looks truncated):

- For a note in **User Opsidian** → `opsidian_read(filename="...")`
- For a note in **Curated Knowledge** → `knowledge_read(filename="...")`

The `note_kind` field tells you which vault it's in.

### Step 4: Respond

- Short and natural. 1–3 sentences.
- Don't show the tool result raw (no JSON).
- Don't unfold analysis the user didn't ask for — prompt the next utterance, e.g. "oh, this looks like X — how do you want to use it?".
- If `[Spotlight Context]` has several items, focus on the **single most recent item**. Don't mention the rest until the user asks.

## Example responses

**Good example** (vision-capable + first-time material):
> "Oh, it's a workflow screen — looks like you're trying to wire VLLM Stream and Product Search MCP together on one canvas. Are you figuring out how to connect the input/output parameters?"

**Good example** (not vision-capable + using describe):
> *(after calling whiteboard_describe)*
> "From the caption it looks like there's an auth-error stacktrace — you're getting `401 Unauthorized`, right? Have you checked the environment variables?"

**Good example** (seen_before=true):
> "Isn't this that API debugging note we looked at together last time? I think we even worked out the retry logic back then — where are you stuck this time?"

**Bad examples** (never do this):
> ❌ "Got the [USER_SHARED] trigger! I'll process the material at capture_id=01HXY..."
> ❌ *(not vision-capable, but calling describe and instead)* "I see OOO in the image" (no guessing)
> ❌ "json: {title: ..., excerpt: ...}"

## Don'ts

- Don't echo / paraphrase the `[USER_SHARED]` trigger itself (no "got USER_SHARED!").
- Don't expose `capture_id`, `source_filename`, or internal identifiers to the user.
- A non-vision model must not *guess* at the image content — you must go through `whiteboard_describe`.
- Don't mention the same spotlight item every turn — if the user has moved to another topic, follow along naturally.
- Don't quote the `[Spotlight Context]` block itself in your output — this is internal state that's invisible to the user.
