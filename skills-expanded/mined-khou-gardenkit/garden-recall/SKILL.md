---
name: garden-recall
description: Search the garden vault for notes relevant to a query and surface them with citations. Use when the user asks about past decisions ("what did I decide about X"), past work ("what's the state of Y"), or anything where the vault might already hold the answer. Greps + reads files under ~/garden/.
---

# garden-recall

Pulls relevant notes from `~/garden/` for a query. Used by the SessionStart hook automatically; can also be invoked explicitly.

## How

1. **Identify search terms** from the query. Include synonyms and related concepts.

2. **Grep the vault** for matches:
   ```bash
   grep -ril "<term>" ~/garden --include="*.md" | head -20
   ```

3. **Skim summaries first** (cheap pass). For each candidate, read just the frontmatter to get title + `summary:` + `updated:`:
   ```bash
   for f in <candidate-files>; do
     awk '/^---$/{n++; if(n==2) exit} n==1' "$f"
     echo "FILE: $f"
     echo "---"
   done
   ```
   Notes ship with a one-sentence `summary:` field for exactly this purpose. Decide which 3–5 are worth opening in full based on summaries alone.

4. **Rank candidates** by relevance:
   - Summary directly answers the query > summary tangentially related
   - Exact match in title (frontmatter or H1) > body match
   - Recent `updated:` > older
   - Files in `decisions/` and `projects/` > generic `notes/`

5. **Read the top 3–5 files in full.** Only the ones the summary pass flagged as worth the tokens.

6. **Follow links one hop** when top hits reference unread notes that look on-topic. Use the typed edges in frontmatter to prune:
   - `supersedes: [X]` → if the query is about current state, skip X (it's been replaced). If the query is historical, X is exactly what to read.
   - `depends-on: [X]` → follow X only if the query is about prerequisites or root cause.
   - `contradicts: [X]` → always show both sides; surface the tension to the user.
   - `derived-from: [X]` → follow X only if the user wants source material or provenance.
   - `part-of: [X]` → X is the parent; read it for broader context. Sibling splits (other notes with the same `part-of`) may be relevant too.
   - Plain `[[wiki-links]]` in the body → skim summary first, then decide.

   For reverse-direction lookups ("what supersedes this?" / "what depends on this?"), grep:
   ```bash
   grep -rl "^supersedes:.*<note-name>" ~/garden --include="*.md"
   ```

7. **Synthesize for the user** with citations (use the note's `summary:` as the gist when it's accurate):
   ```
   From the vault:
   - [[<note-name>]] (updated YYYY-MM-DD): <summary or refined gist>
   - …
   
   <synthesized answer>
   ```

If a candidate has no `summary:` field, fall back to reading the first 20 lines. The gardener will backfill missing summaries on its next run; recall stays read-only.

## When to use

- User asks "what did we decide about X"
- User asks about state of a project, person, or topic
- Before answering any question where the vault might already hold context: silent recall, then synthesize

## Don't

- Don't read every match: top-ranked few only.
- Don't guess if the vault has nothing: say so plainly: "Nothing in the vault on that yet."
- Don't write to the vault from this skill. Recall is read-only.

## Speed

For broad recall (many candidate files), use:
```bash
grep -ril "<term>" ~/garden --include="*.md" | xargs -I{} sh -c 'echo "=== {} ==="; head -20 "{}"' | head -200
```
to get a fast overview before deep-reading.
