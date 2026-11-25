---
name: stop-slop
description: Use when drafting, editing, or reviewing prose to eliminate predictable AI writing patterns. Detects filler phrases, formulaic structures, passive constructions, vague declaratives, and rhythm monotony. Supports both English and Chinese text.
provenance:
  origin: cursor-plugins (fusion: unslop extended catalog absorbed into stop-slop)
  license: MIT
  upstream_url: https://github.com/cursor/plugins/tree/main/pstack/skills/unslop
  maintained_by: my-skills
---

# Stop Slop

Eliminate predictable AI writing patterns from prose.

## Core Rules

1. **Cut filler phrases.** Remove throat-clearing openers, emphasis crutches, and all adverbs. See [references/phrases.md](references/phrases.md).
2. **Break formulaic structures.** Avoid binary contrasts, negative listings, dramatic fragmentation, rhetorical setups, false agency. See [references/structures.md](references/structures.md).
3. **Use active voice.** Every sentence needs a human subject. No passive constructions. No inanimate objects performing human actions.
4. **Be specific.** Name the thing. No vague declaratives, no lazy extremes ("every," "always," "never").
5. **Put the reader in the room.** "You" beats "People." Specifics beat abstractions.
6. **Vary rhythm.** Mix sentence lengths. Two items beat three. No em dashes.
7. **Trust readers.** State facts directly. Skip softening and justification.
8. **Cut quotables.** If it sounds like a pull-quote, rewrite it.

## Quick Checks

Before delivering prose, scan for these. Fix any that appear.

| Check | Action |
|-------|--------|
| Adverbs | Kill them |
| Passive voice | Find the actor, make them the subject |
| Inanimate thing doing a human verb | Name the person |
| Sentence starts with Wh- word | Restructure |
| "Here's what/this/that" throat-clearing | Cut to the point |
| "Not X, it's Y" contrast | State Y directly |
| Three consecutive sentences same length | Break one |
| Paragraph ends with punchy one-liner | Vary it |
| Em-dash | Remove |
| Vague declarative | Name the specific thing |
| Narrator-from-a-distance | Put the reader in the scene |
| Meta-joiners ("The rest of this essay...") | Delete |

## Extended Catalog

After the quick checks, scan [references/unslop-rules.md](references/unslop-rules.md) — the numbered pattern catalog (AI vocabulary, superficial -ing phrases, colon/bold overuse, inline-header lists, abstract metaphor nouns, over-compression, and more) merged from the unslop skill. Rule numbers are stable ids other skills cite; when merging in a new offender, append it there with the next free number.

## Scoring

Rate 1-10 on each dimension. Below 35/50: revise.

| Dimension | Question |
|-----------|----------|
| Directness | Statements or announcements? |
| Rhythm | Varied or metronomic? |
| Trust | Respects reader intelligence? |
| Authenticity | Sounds human? |
| Density | Anything cuttable? |

## References

- [references/phrases.md](references/phrases.md) — Phrases to remove (filler, jargon, adverbs, meta-commentary)
- [references/structures.md](references/structures.md) — Structures to avoid (contrasts, fragmentation, false agency, rhythm)
- [references/examples.md](references/examples.md) — Before/after transformations
- [references/ai-patterns-zh.md](references/ai-patterns-zh.md) — 中文 AI 写作模式（高频词、套话句式、句式结构）
- [references/unslop-rules.md](references/unslop-rules.md) — Extended numbered catalog (来源：cursor/plugins unslop，MIT)
