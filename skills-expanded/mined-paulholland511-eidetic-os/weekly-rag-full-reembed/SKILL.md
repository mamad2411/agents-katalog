---
name: weekly-rag-full-reembed
description: Weekly full re-embed of all vault notes into the RAG vector store.
---

Run a full re-embed of the entire vault to ensure the vector store is complete
and consistent.

> Placeholders: `{{VAULT_PATH}}` = vault path, `{{EIDETIC_OS}}` = repo path,
> `{{EMBED_HOST}}:{{EMBED_PORT}}` = your local embeddings endpoint.

**Objective:** Re-embed all vault notes from scratch, replacing the existing
vector store.

**Steps:**

1. Request access to `{{VAULT_PATH}}`
2. Run the full embed script:
   ```bash
   EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} EMBED_HOST={{EMBED_HOST}} EMBED_PORT={{EMBED_PORT}} \
     eidetic embed --full
   ```
3. The script will:
   - Walk all `.md` files in the vault (excluding `.obsidian/`, `.git/`, `.rag/`, `.claude/`)
   - Chunk each file (~500 tokens, 50-token overlap)
   - Embed all chunks using the embeddings endpoint at `http://{{EMBED_HOST}}:{{EMBED_PORT}}/v1/embeddings`
   - Overwrite `vectors.json` with the fresh vector store
   - Update `last_embed.txt` and rebuild the knowledge graph
4. Report total files, chunks, and time taken

**If the embeddings endpoint is unreachable:** Do NOT overwrite the existing
`vectors.json`. Log the error and abort. Try again next week.

**Constraints:**
- Typically scheduled weekly (e.g. Sunday early morning)
- Do NOT modify any vault notes
- Runtime scales with vault size (roughly a minute per ~40 files, endpoint-dependent)
