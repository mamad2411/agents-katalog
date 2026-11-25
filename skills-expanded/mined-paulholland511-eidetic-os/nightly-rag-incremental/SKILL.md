---
name: nightly-rag-incremental
description: Incremental RAG embed of new/changed vault notes using a local embeddings endpoint.
---

Run an incremental RAG embed of the vault to keep the vector store up to date.

> Placeholders: `{{VAULT_PATH}}` = your vault path, `{{EIDETIC_OS}}` = the Eidetic OS
> repo path, `{{EMBED_HOST}}:{{EMBED_PORT}}` = your local embeddings endpoint.

**Objective:** Embed any new or modified notes since the last embed run.

**Steps:**

1. Request access to `{{VAULT_PATH}}`
2. Run the incremental embed script:
   ```bash
   EIDETIC_TRIGGER=scheduled VAULT_PATH={{VAULT_PATH}} EMBED_HOST={{EMBED_HOST}} EMBED_PORT={{EMBED_PORT}} \
     eidetic embed --incremental
   ```
3. The script will:
   - Check `last_embed.txt` for the timestamp of the last run
   - Find all `.md` files modified since that timestamp
   - Chunk and embed only those files using the embeddings endpoint at `http://{{EMBED_HOST}}:{{EMBED_PORT}}/v1/embeddings` (model from `EMBED_MODEL`, default `text-embedding-nomic-embed-text-v1.5`)
   - Update `vectors.json` with new/updated vectors
   - Update `last_embed.txt` with the current timestamp
4. Report how many files were updated and how many new chunks were added

**If the embeddings endpoint is unreachable:** Log the error and skip — don't
delete existing vectors. The next run will pick up the missed files.

**Constraints:**
- Do NOT run a full re-embed, only incremental
- Do NOT modify any vault notes
- The vector store lives under `$RAG_DIR` (default `{{VAULT_PATH}}/.rag/vectors.json`)
