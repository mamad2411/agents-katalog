---
name: blueprint-compare-pair
description: "Pair every article of the old version with its article in the new one, and say whether each changed, was added or was removed — writing .blueprint/comparison.json and changing no document."
---

# Pair the articles of the two versions

`.blueprint/answers.json` names the old version (`old`), the new version (`new`) — one file each — and what the
person wants looked at first (`focus`, may be empty). Read both in full. The person may not be an engineer: say
what you do in plain words.

Change nothing in the repository: neither version is touched. Write only under `.blueprint/`.

## Find the articles

Run `sh <base pack>/checks/chaff.sh tree <file> --format json` on each version. Every node whose `kind` is
`article` is one article; its `address` (`"4"`) is how you name it below, and `attrs.label` (`第4条`,
`Article 4`) is how the person reads it. The check uses the same tree, so an article chaff does not read as one
is not yours to pair.

## Pair them

For each article of the old version, find the article of the new version that carries the same provision — by
what it says, not by its number: a provision that moved or was renumbered (old 第9条 is new 第8条) is one pair.
Then write `.blueprint/comparison.json`:

```json
{ "rows": [
  { "old": "1", "new": "1", "change": "same" },
  { "old": "4", "new": "4", "change": "changed", "what": "委託料が月額200,000円から220,000円になった" },
  { "old": null, "new": "5", "change": "added", "what": "毎月5日までの報告の条が足された" },
  { "old": "8", "new": null, "change": "removed", "what": "成果物の扱いの条が消えた" },
  { "old": "9", "new": "8", "change": "same" }
] }
```

- `same` / `changed` — both `old` and `new`. `changed` needs `what`: one line, in the person's language, saying
  what is different, with the words or numbers from both versions. A change in a paragraph or an item is a change
  to the article that holds it.
- `added` — only `new`; `removed` — only `old`. A `what` saying what the article is about helps the person.
- Every article of each version appears in exactly one row.

Whether a pair is `same` or `changed` is not a judgement: the check compares the two articles' text (spacing
aside, and leaving out the article's own number) and refuses a `same` whose text differs and a `changed` whose
text does not. When you pair two articles that the check calls different but you think the change is trivial
(punctuation, a character's width), it is still `changed`: say so in `what`.

## Done when

`node <usecase pack>/checks/comparison.mjs` (with `BLUEPRINT_BASE` and `BLUEPRINT_USECASE` set to the pack folders
from your prompt) passes. It writes `.blueprint/comparison.txt`, the pairing a person reads before the table.
