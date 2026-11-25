---
name: chunkmaster-pro
description: "Use when chunking, tagging, exporting, and indexing documents step-by-step. Prepares documents for RAG pipelines, embeddings, and knowledge bases."
category: productivity
---

# Chunkmaster Pro — Document Chunking & Indexing

## Overview
Chunkmaster Pro takes raw documents (PDFs, markdown, text, HTML) and systematically prepares them for RAG pipelines, vector databases, and embedding workflows. It handles chunking strategy, metadata tagging, export formatting, and indexing readiness checks.

## When to Use
- Preparing a corpus for a RAG pipeline (LlamaIndex, LangChain, custom).
- Chunking long documents for embedding into Pinecone, Weaviate, Chroma, or similar.
- Building a knowledge base from a collection of markdown or PDF files.
- Tagging and organizing documents with metadata for semantic search.

## How It Works
The pipeline follows five stages:
1. **Ingest** — Load and normalize the document (extract text, clean encoding).
2. **Segment** — Apply chunking strategy (fixed-size, semantic, recursive, or sentence-aware).
3. **Tag** — Generate metadata per chunk (source, page, section, topics, keywords).
4. **Export** — Format as JSONL, CSV, or direct embeddings-ready arrays.
5. **Validate** — Check chunk overlap, token counts, and metadata completeness.

## Steps
1. **Assess the document.** Identify format, length, structure (headings, tables, code blocks).
2. **Choose chunking strategy.** 
   - Fixed-size (256-1024 tokens): for uniform embedding.
   - Semantic/sentence-aware: for preserving meaning across chunk boundaries.
   - Recursive: for hierarchical docs with nested sections.
3. **Set chunk parameters.** Size, overlap %, separators (newlines, periods, headings).
4. **Run chunking.** Process the document and assign sequential IDs.
5. **Generate metadata.** Source filename, chunk index, section heading, auto-extracted keywords.
6. **Export.** JSONL (preferred for most vector DBs) or CSV. Include embedding-ready text field.
7. **Validate.** Spot-check 3-5 chunks for coherence, token count, and metadata accuracy.

## Common Pitfalls
- **Wrong chunk size.** Too small = lost context. Too large = diluted embeddings. Aim for 256-512 tokens for most general-purpose use.
- **No overlap.** Chunks without overlap can split sentences and break query matching. Minimum 10-20% overlap.
- **Skipping metadata.** Chunks without source/position metadata are nearly useless for retrieval attribution.
