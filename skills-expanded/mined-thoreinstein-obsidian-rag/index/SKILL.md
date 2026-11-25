---
name: index
description: >-
  Use when the user wants to index their vault for semantic search, rebuild
  the RAG index, or says "index", "reindex", or "rebuild index".
---

# Index Vault

Trigger vault indexing for semantic search (RAG).

## Default Action

Call `obsidian_rag_index` with no special arguments. This runs an incremental index — only changed files are re-embedded.

## Force Reindex

If the user says "force" or "rebuild from scratch":
- Call `obsidian_rag_index` with `force_reindex: true`

## Single File

If the user specifies a file:
- Call `obsidian_rag_index` with `file_path` set to the relative path

## After Indexing

Report the result: how many chunks were indexed, whether it was incremental or full.
