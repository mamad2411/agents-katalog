---
name: kyn-wiki-query
description: Answer questions grounded in the user's wiki/vault (wiki/concepts, wiki/entities, wiki/sources) — never from training knowledge. Trigger when the user asks what the vault knows about something, references prior research/decisions/terminology that could live in the wiki, or explicitly asks to search/consult it. Works from any session, regardless of the current working directory.
argument-hint: "The question to answer from the wiki"
disable-model-invocation: true
---

**Vault resolution:** `{vault}` below is the write-target vault: the `path:` of the `default:` vault in `~/.almagest/config.yml`, if that file exists and declares one; otherwise `~/vault`. That single lookup is the only thing Kuyen reads from the shared Almagest config — no registry machinery, no vault-name arguments.

1. **Search the wiki.** Look across `{vault}/wiki/concepts/`, `wiki/entities/`, and `wiki/sources/` (filenames, titles, aliases, and content) for anything relevant to the question. Done when every matching page across all three subfolders has been found.

2. **Ground the answer.** If nothing relevant turned up, say so explicitly ("Nothing in the wiki covers this") and stop — do not fill the gap with training knowledge. Otherwise, answer using only what the matched pages say, citing every page you drew from by path. Done when the answer either states no match was found, or cites every page it used.

3. **Offer to persist, rarely.** Only when the answer synthesizes something genuinely new — combines two or more pages into an insight not written down anywhere, or fills a real gap the wiki had no page for — end with a one-line offer to save it via `kyn-wiki-ingest`. Skip this for anything answerable by pointing at a single existing page verbatim. Done when either no offer was made, or exactly one line offering to persist appears at the end.

Persisting itself is not this skill's job: if the user asks to save the answer — now or in a later message, unprompted or accepting the offer above — that invokes `kyn-wiki-ingest` directly, treating this answer as the source content instead of a URL or file.
