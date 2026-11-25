---
name: garden-voice
description: Extract or refresh the user's writing voice profile from their actual Slack messages. Pulls sent messages, synthesizes style patterns, anchors with short redacted examples, writes meta/voice.md. Use when the user says "init voice", "refresh voice", "extract my voice", "build voice profile", or during initial vault bootstrap. Three modes: init (first-time broad sample), refresh (periodic top-up), add (manual snippet).
---

# garden-voice

Builds and maintains `~/garden/meta/voice.md`: the user's voice profile derived from their own messages. Loaded on-demand by drafting tasks for tone-matching.

## Why this exists

Asking a user to describe their writing voice in the abstract gives shallow results. Sampling their actual messages and synthesizing patterns gives the agent a concrete, calibrated reference. Per the source video, having a voice profile is reportedly the single biggest output-quality multiplier for any drafting work.

## Modes

### init

First-time bootstrap. Sample broadly across the user's recent sent messages.

1. **Find user ID** via `slack_search_users` (use the user's name or email from `meta/user.md`).
2. **Pull sent messages.** Use `slack_search_public_and_private` with query `from:<USER_ID>`. Paginate to gather ~500–1000 messages. Skip threads where the only content is reactions or single-emoji replies.
3. **Aggregate** text into a single corpus.
4. **Redact** (see redaction rules below): strip proper nouns, numbers, URLs, but preserve all linguistic content.
5. **Synthesize patterns**: observe and write down:
   - Sentence rhythm (terse / flowing / fragments)
   - Capitalization habits (lowercase casual / sentence case / mixed)
   - Punctuation tics (em-dashes, ellipses, parenthetical asides, trailing `?` for soft asks)
   - Vocabulary preferences (favored words, slang, technical register)
   - Emoji and reaction patterns (which, how often, in what positions)
   - Greeting / closing patterns
   - Sentence starters and connector words
   - Tone markers (irony, hedging, directness)
6. **Pick 10–15 anchored examples**: short snippets (≤2 sentences each, redacted) that demonstrate the patterns concretely.
7. **Write** `~/garden/meta/voice.md` per the output format below.
8. **Commit** to the vault git repo with message `voice: init from <N> Slack messages`.

### refresh

Periodic update: appends new observations rather than overwriting.

1. Read existing `voice.md` to know what patterns are already noted.
2. Pull last ~200 messages since the file's `updated:` date.
3. Diff: any new patterns or notable shifts in style?
4. Update `voice.md`: refresh anchored examples (drop oldest, add freshest), append new pattern observations.
5. Commit with `voice: refresh: <summary of changes>`.

### add `<snippet>`

Manual addition. The user gives a representative message that should be preserved.

1. Append to the "Anchored examples" section of `voice.md` with light redaction.
2. If it surfaces a pattern not yet noted, add it.
3. Commit with `voice: add: <one-line summary>`.

## Output format: meta/voice.md

```markdown
---
type: meta
updated: YYYY-MM-DD
sample_size: <N messages>
sample_window: <date range or "all-time">
---

# Voice profile

Derived from <N> Slack messages sent by the user.

## Patterns

### Sentence structure
- <observation 1>
- <observation 2>

### Capitalization & punctuation
- <observation>

### Vocabulary
- Favored words: <list>
- Avoided words: <list>
- Register: <casual / formal / mixed by audience>

### Tone markers
- <observation>

### Emoji & reactions
- <observation>

### Greetings / closings
- <observation>

## Anchored examples

Short, redacted snippets demonstrating the patterns. `<NAME>`, `<COMPANY>`, `<NUM>`, `<URL>` are placeholders.

1. "<example 1>"
2. "<example 2>"
...
```

## Redaction rules

The voice profile captures **style**, not **content**. Apply these substitutions before writing examples:

| Replace | With |
|---|---|
| Person names | `<NAME>` |
| Company / product names | `<COMPANY>` or `<PRODUCT>` |
| Email addresses | `<EMAIL>` |
| URLs | `<URL>` |
| Specific numbers (currencies, IDs, percentages) | `<NUM>` |
| Specific dates | `<DATE>` |
| Long quoted text from others | `<QUOTED>` |

Preserve unchanged: vocabulary, punctuation, sentence structure, emoji, line breaks, slang, profanity.

If a message can't be meaningfully redacted (i.e. removing the proper nouns leaves nothing distinctive), skip it.

## Privacy & safety

- `voice.md` lives in the **private** vault. Never copies of it land in the public `gardenkit` repo.
- Only the user's own sent messages are sampled: never quote others.
- Don't pull DMs unless the user explicitly opts in for a future variant.
- If a Slack message contains obvious secrets (credentials, tokens), drop the message entirely.

## How `voice.md` gets used

`meta/soul.md` instructs the agent: *"When drafting in the user's voice (Slack, email, PRs, tweets, blog posts), reference `[[meta/voice]]` first."*

Voice is **load-on-demand**, not always-on. The SessionStart hook doesn't inject it (would bloat context). The agent loads it only when a drafting task surfaces.

## Don't

- Don't sample messages from before the user joined a workspace they care about.
- Don't include verbatim examples longer than 2 sentences.
- Don't synthesize more than 15 anchored examples: beyond that, agent context-load gets unwieldy.
- Don't push voice.md to a public repo (sanity-check `git remote -v` shows the private vault before committing).
