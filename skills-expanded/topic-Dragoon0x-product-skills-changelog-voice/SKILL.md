---
name: changelog-voice
description: "Ship updates people actually want to read. Structures release notes, changelog entries, and product updates with what-changed, why-it-matters, and what-to-do-next. Use when writing changelogs or release announcements."
---

# Changelog Voice

Ship updates people actually want to read.

## How to use

- `/changelog-voice` Apply changelog constraints to this conversation.

## Constraints

### Entry Structure
1. What changed (specific, concrete, no marketing language)
2. Why it matters (what the user can now do that they couldn't before)
3. How to use it (link or brief instruction)

### Rules
- MUST lead with the user benefit, not the technical change
- MUST categorize: New, Improved, Fixed, Removed
- SHOULD include a visual (screenshot, gif, video) for UI changes
- NEVER say "various bug fixes" without specifics
- NEVER announce something as "new" that was previously broken and is now working
- SHOULD mention breaking changes prominently with migration steps

### Tone
- Direct, not corporate ("You can now..." not "We are pleased to announce...")
- Honest about what's still missing or in progress
- Brief. Respect the reader's time.
- SHOULD acknowledge when a change was user-requested ("You asked, we built it")

### Anti-Patterns
- Changelogs that read like marketing emails
- Burying breaking changes in a long list of improvements
- Announcing features that aren't actually available yet
- Using changelogs as a growth channel (no "invite a friend" CTAs in release notes)
- Updates without dates
