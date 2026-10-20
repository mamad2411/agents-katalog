---
description: One-shot opt-in for local semantic search — installs deps, builds embeddings, verifies.
when_to_use: Run once when the user wants hybrid (lexical + semantic) retrieval. After this, every /wiki-ingest, /wiki-query, /wiki-compile, /wiki-lint, /wiki-promote auto-maintains embeddings — no further action needed. Triggered by phrases like "enable semantic search", "turn on hybrid", "install the embedding model".
allowed-tools: Read, Write, Bash
---

# Wiki Enable Semantic

Turn on local hybrid retrieval. One command; idempotent; safe to re-run.

## What this does

1. Installs `numpy` + `sentence-transformers` from `requirements.txt`.
   Respects an active virtualenv; otherwise installs with `--user`.
2. Triggers the first embedding pass (`build_meta.py --embed`).
   Downloads the 384-dim `all-MiniLM-L6-v2` model (~90MB) into
   `~/.cache/huggingface/` on first run.
3. Runs `scripts/check_invariants.sh` to confirm the embedding
   manifest matches the backlink graph and vectors are normalized.
4. Leaves the vault in a "semantic-enabled" state — every subsequent
   operation that rebuilds the sidecar auto-embeds changed pages
   (via `--embed-if-enabled`).

## Protocol

1. Confirm with the user:
   > "This will install numpy + sentence-transformers (~500MB total on
   > disk including torch) and download a ~90MB embedding model on
   > first run. Proceed? (y/n)"
   Wait for a yes.
2. Invoke:
   ```bash
   bash scripts/enable_semantic.sh
   ```
   Stream the output. Do not swallow errors.
3. If step 2 fails at `pip install`, print the error and stop.
   Common causes:
   - No internet.
   - Restricted environment (corporate Python / managed Python).
   - Disk space.
   Suggest the user fix it manually and re-run `/wiki-enable-semantic`.
4. If step 2 fails at the embedding step, the most common cause is
   the model download being interrupted. Suggest re-running. The
   incremental embed picks up where it left off.

## After it succeeds

- `wiki/.meta/embeddings.npy` + `embeddings-manifest.tsv` exist.
- `/wiki-search` and `/wiki-query` auto-upgrade from lexical → hybrid.
  No command changes; no user action.
- Every `/wiki-ingest` / `/wiki-compile` / `/wiki-lint` embeds the
  pages it touches via `--embed-if-enabled` (incremental — only
  pages whose text SHA changed).

## To disable

Tell the user:
> Delete `wiki/.meta/embeddings.npy` and `wiki/.meta/embeddings-manifest.tsv`.
> The next operation will notice they are gone and stop trying to embed.
> Lexical search keeps working throughout.

## Reporting

- Pip install output (last ~5 lines).
- Embed count: `N pages embedded`.
- Invariant suite result.
- One-liner confirming semantic search is now live.
