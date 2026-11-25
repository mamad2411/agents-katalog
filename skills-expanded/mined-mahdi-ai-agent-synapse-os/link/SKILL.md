---
name: link
description: Finds and adds a node's missing connections — its project or area, mentioned people, related notes and ideas — from its category's sub-index and at most five opened candidates. Use for "اینو به … وصل کن", "لینک‌هاش رو درست کن", "ربطش به چیه", "link this", "connect this", "what is this related to", or after a batch capture.
---

# link

## Steps

1. Open the target node; note its title, summary, tags, people and the project or area it names.
2. Read `index/INDEX.md`, then the node's category sub-index `index/by-area/<area>.md` (no category yet: `index/by-type/project.md` and `person.md`). From the lines, pick at most 5 candidates that share its people, project or topic words; open only those. `Grep -i` one specific term only when the lines carry nothing.
3. Add relations: set `area` / `project` / `people` when clearly implied; add `[[Title]]` links under a `## Related` section, one per line with a short why. Only titles that exist in the index.
4. Set `updated`. Reply with the links added, one per line, in the user's language.
