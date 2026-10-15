---
name: kyn-wiki-ingest
description: Ingest a new source (URL, local file, or a synthesized answer from earlier in the conversation) into the user's wiki/vault — save a raw copy, then synthesize it into a Concept, Entity, or Source page. Trigger when the user pastes a URL with no other context, gives a local file path, says "ingest this", "add this to the wiki", "process this source", or asks to save/persist an answer kyn-wiki-query produced — this skill always targets the user's wiki/vault, regardless of the current working directory.
argument-hint: "URL, file path, or text to ingest"
disable-model-invocation: true
---

**Vault resolution:** `{vault}` below is the write-target vault: the `path:` of the `default:` vault in `~/.almagest/config.yml`, if that file exists and declares one; otherwise `~/vault`. That single lookup is the only thing Kuyen reads from the shared Almagest config — no registry machinery, no vault-name arguments.

1. **Save the raw source.** If given a URL or local file, fetch it: use a specialized scraping/parsing tool if available (e.g., Firecrawl) for cleaner extraction, otherwise fall back to a regular fetch or file-read tool. If given text directly (e.g., a synthesized answer from kyn-wiki-query), skip fetching — use that text as-is. Either way, save an unmodified copy under `{vault}/.raw/<slug>.md` (or the source's original extension for non-text files), deriving `<slug>` from the source's title, URL, or the gist of the text — never edit a file already in `.raw/`. Done when the raw copy exists in `.raw/` and matches the source verbatim.

2. **Classify the source.** Decide whether it's best captured as a Concept, Entity, or Source page — templates live in the `templates/` folder next to this `SKILL.md` (this skill's own base directory).
   - **Concept** (`wiki/concepts/`) — synthesized knowledge with no existence outside the wiki, even when derived from a source; an idea you'd look up in a textbook. Use when it has a proper name (principle, pattern, framework, technique), can be applied or referenced in future sessions, and warrants its own article. Skip concrete instances and topics too generic to stand alone.
   - **Entity** (`wiki/entities/`) — a person, organization, tool, or service that exists in the world independently and can go stale (acquired, deprecated); something a journalist could write breaking news about. Use when it appears in more than one context or has an active role in the user's work. Skip passing mentions with no role of their own.
   - **Source** (`wiki/sources/`) — a purely conversational origin (a synthesized answer with no URL or file behind it) never classifies as Source — that type models an external artifact, and its `resource`/`source_author` fields and `.raw/` copy assume one exists; use Concept or Entity instead.

   One source can seed more than one page only when they cover genuinely distinct nouns, not the same content restated. Done when the target page(s) and matching template(s) are named.

3. **Synthesize the page(s).** Copy the matching template from that `templates/` folder and fill it in with a synthesis, not a copy-paste of the raw source. Save it under `{vault}/wiki/concepts/`, `wiki/entities/`, or `wiki/sources/` to match its type. If a page for this concept/entity already exists, update it in place instead of duplicating — single source of truth, cross-link instead of restating. Reference the raw file in `.raw/` by path rather than re-quoting it at length. Done when every new/updated page is saved under its matching `wiki/` subfolder and links back to its `.raw/` source.

4. **Update the index.** Add or update the entry in the matching section of `{vault}/wiki/index.md` (Conceptos / Entidades / Fuentes). Done when every page from step 3 is discoverable from `index.md`.

5. **Log the ingest.** Append one line to `{vault}/wiki/meta/log.md`: `**[YYYY-MM-DD] ingest** | <source> → <pages created/updated>`. Done when the entry is appended — `log.md` is append-only, never edit prior entries.

6. **Confirm the ingest.** End your response with a short line: "Ingested." followed by which pages were created or updated.
