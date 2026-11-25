---
name: make
description: Writes in the user's own voice — a post, a caption, a message, a bio — from the map it is for and its connected maps (the character map carries the voice); saves nothing unless asked. Use for "بنویس", "یه پست بساز", "کپشن بنویس", "یه پیام بنویس", "بیو بنویس", "write a post", "draft a caption", "write a message", or the Make switch.
---

# make

The piece, in their voice, from what the vault knows. Index first; never bulk-read; read-only unless asked to save.

## Steps

1. Read `index/INDEX.md`. Its **Maps** section says which maps exist, what each is for and what it connects to; the runtime context's **Scope** line, when present, says which maps are in reach (the core, or one map cut off from the mind map) — never use one outside it. Within the scope pick the map the piece is for: the one the user names, else the one whose purpose fits the request (a caption for the page → the page's map), else the mind map.
2. Read that map's sub-indexes, `index/by-area/<category>.md` (its voice / tone and audience categories first, then the topic). If the map connects to the character map — or the piece is for the mind map and the character map connects to `mind` — read the character map's voice and values sub-indexes too. Open at most 5 nodes: the thing the piece is about, one example of the voice, the facts it rests on.
3. Missing something that changes the piece — the platform, the length, who it is for, the one fact it rests on? Ask at most two short questions and write nothing yet. Otherwise write.
4. Reply with the piece first, ready to paste, per [references/approach.md](references/approach.md): the user's language, the platform's conventions, the voice as the vault describes it, never an invented fact about them or their work. Then one line on what it drew on, as `[[links]]`. Variants only when asked.
5. Save nothing unless asked. «ذخیره کن» / "save it" → a `note` in the map's outputs category («خروجی‌ها» / "Outputs"; create it inside that map with `map:` when missing): `summary` = what it is and for where, body = the piece, `source: brain`; reply `created [[Title]] (note) → [[Category]]`.
