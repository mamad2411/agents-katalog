---
name: search_spec
version: 1.0.0
license: MIT
---

# search_spec

BM25 search over the llms-txt-skills spec snapshot (4 documents: the RFC, the
executable-skills extension, the skill-attestations extension, and the mcpwasm
reference README). Uses the gateway-provided `host.memorySearch` capability over
a hash-pinned snapshot declared in `/llms.txt` via the `skills-memory` line.

## Arguments

- `q` (string, required): free-text BM25 query.
- `k` (number, optional): max hits to return, integer 1..10, default 5.

## Returns

`{ hits: [{ text, score, title, concept_id }] }` — `text` is the matched chunk
snippet, `score` is the BM25 score (higher magnitude = better match), `title`
is `<doc>: <section>`, `concept_id` identifies the chunk.

## Example

```json
{ "q": "tool_sha256 integrity verification", "k": 5 }
```