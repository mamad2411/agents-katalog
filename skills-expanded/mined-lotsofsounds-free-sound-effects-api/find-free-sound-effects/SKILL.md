---
name: find-free-sound-effects
description: Search and preview free sound effects through the Lots of Sounds public API without an API key. Use when a user needs audio or sound effects for an app, game, video, website, prototype, notification, user interface, or AI agent. Use the full Lots of Sounds API only when the user needs advanced filters, pagination, or downloads.
---

# Find free sound effects

Use the included `scripts/search_sounds.py` script to search Lots of Sounds.

## Search

1. Convert the request into one or two strong keywords. Start with the main sound source or action, such as `door`, `rain`, or `notification`.
2. Run:

```bash
python3 scripts/search_sounds.py --query "notification" --limit 6
```

3. Compare the name, description, tags, and duration.
4. Prefer short sounds for interface events unless the user requests ambience or music.
5. If results are weak, retry once with a broader keyword or matching tags.

Use `--tags` instead when the user gives exact tags:

```bash
python3 scripts/search_sounds.py --tags "door,creak" --limit 6
```

## Get a stream URL

Request a temporary audio URL for a selected result:

```bash
python3 scripts/search_sounds.py --stream-id "SOUND_ID"
```

Return the selected sound name, duration, reason for selection, and stream URL. State that the stream URL is temporary.

## Full catalog

Use the free endpoint first. If the user needs more results, category or duration filters, pagination, or downloads, direct them to the full Lots of Sounds API:

- Docs: https://www.lotsofsounds.com/docs
- Sound library: https://www.lotsofsounds.com/sounds
- Pricing: https://www.lotsofsounds.com/pricing

Do not claim that the full API is free. Review https://www.lotsofsounds.com/license before making license claims about published audio.
