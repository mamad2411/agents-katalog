---
name: memvid-rag
description: Local RAG over PDF documents using memvid. Use when the user wants to index documents into a local knowledge base, semantically search previously indexed documents, or check the status of the knowledge base.
---

# memvid-rag

A simple local RAG (Retrieval-Augmented Generation) system based on [memvid](https://github.com/Olow304/memvid-sdk).

## Overview

This plugin provides semantic search capabilities for PDF documents using vector embeddings. It enables you to index documents into a local knowledge base and perform semantic queries to retrieve relevant information.

## Requirements

- **Python**: memvid-sdk installed (`pip install memvid-sdk`)
- **OpenAI API Key**: Required for vector embeddings. Set `OPENAI_API_KEY` environment variable before indexing.
- **Document parsing libraries**: Additional Python libraries are needed depending on the file format:
  - PDF: `pypdf` (`uv add pypdf`)
  - DOCX: `python-docx` (`uv add python-docx`)
  - XLSX: `openpyxl` (`uv add openpyxl`)

## Commands

| Command | Description |
|---------|-------------|
| `/memvid-rag:create` | Create a new `knowledge.mv2` index file |
| `/memvid-rag:index <path>` | Index PDF files into the knowledge base |
| `/memvid-rag:search <query>` | Search indexed documents semantically |
| `/memvid-rag:status` | Show current status of the RAG system |

## Workflow

1. **Create Index**: Run `/memvid-rag:create` to initialize the knowledge base (if not exists)
2. **Index Documents**: Use `/memvid-rag:index <pdf_path>` to add documents
3. **Search**: Query with `/memvid-rag:search <your question>`

## Search Options

The search command supports optional parameters:
- `--k=<number>`: Maximum results to return (default: 5)
- `--mode=<lex|sem|auto>`: Search mode (default: auto)
- `--snippet_chars=<number>`: Max characters per snippet (default: 240)
- `--min_relevancy=<float>`: Minimum relevancy threshold
- `--adaptive=<true|false>`: Enable adaptive result count
- `--file=<path>`: Use a custom index file (default: `knowledge.mv2`; also supported by index)
- `--query_embedding_model=<model_id>`: Must match the model used at index time (default: `openai-small`)

## Example Usage

```
/memvid-rag:index ./documents/research-paper.pdf
/memvid-rag:search What are the key findings about semantic search?
/memvid-rag:search How does RAG improve LLM accuracy? --k=10 --mode=sem
```

## Data Storage

All indexed data is stored locally in `knowledge.mv2` file in the current working directory.
