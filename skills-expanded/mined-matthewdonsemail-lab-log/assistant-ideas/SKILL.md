---
name: assistant-ideas
description: "One run of the personal assistant's ideas job: for each item the check tagged, find photo ideas (gifts, recipes, places, a plan) or the biller's own payment page, and record them with assistant_ideas."
version: 0.1.0
platforms: [linux, macos, windows]
---
# Assistant ideas

This runs on its own, not in a chat, after the assistant's check tagged something (a birthday, a guest coming to eat,
a trip, a bill). You never see mail: only each item's title, its kind and a few plain words. Prepare what a thoughtful
assistant would have ready before the user asks.

## Steps

1. **See what's waiting.**

```text
{"tool": "assistant_ideas", "args": {"action": "list"}}
```

2. **For gift, recipes, places or plan**: look for photos with the item's words, specific and visual ("chocolate
   layer cake", "peony bouquet", "herb roasted turkey", "Austin food trucks"). Make 2 to 4 searches if one isn't
   enough; keep 4 ideas that differ from each other.

```text
{"tool": "assistant_ideas", "args": {"action": "photos", "query": "chocolate layer birthday cake"}}
```

3. **Record them**: a short title (≤ 40 characters), a note that helps decide (≤ 80: "Order by Monday", "4 h, serves
   6", "Same-day delivery"), and the photo exactly as `photos` returned it.

```text
{"tool": "assistant_ideas", "args": {"action": "record", "id": "3f2a91c0", "ideas": [{"title": "Chocolate layer cake", "note": "Order by Monday", "photo": "https://upload.wikimedia.org/wikipedia/commons/a/a1/Cake.jpg"}, {"title": "Peonies and ranunculus", "note": "Same-day delivery", "photo": "https://upload.wikimedia.org/wikipedia/commons/b/b2/Peonies.jpg"}]}}
```

4. **For pay**: search the web (`web_search`) for "<words> pay bill online" (a licence or certificate: "<words>
   renew online") and record the first **https** result on the item's `site` as `pay_link`. A result on any other
   site is refused, so don't pick one. When nothing is on the item's site, record the item with no `pay_link`, so
   it isn't asked again.

```text
{"tool": "assistant_ideas", "args": {"action": "record", "id": "8c0d11ab", "pay_link": "https://www.citylight.example/pay"}}
```

## Rules

- Only the item's words, nothing else: you can't read mail and mustn't guess about it.
- Photos only from `photos`; links only https.
- One `record` per item. If nothing good turns up, record no ideas: an empty card is better than a wrong one.
- No blocks, no HTML, no `::preview`: this run draws nothing.
