# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A proof-of-concept for privacy-preserving semantic file search ("Option A"). File **content is embedded in memory and never persisted** — only float[768] vectors and file metadata are stored. The core compliance guarantee is enforced by schema design: `file_chunks` deliberately has no `text`/`content` column (see [db/init.sql](db/init.sql)). Preserve this invariant — do not add columns or logging that would persist extracted document text.

## Running

One script brings up infra (docker compose + Ollama model pull) and then whichever
services you ask for via a mode argument — default `all`:

```bash
./start.sh              # docker compose up, pulls Ollama model, runs Worker + API + Web; Ctrl+C stops them
./start.sh worker       # Worker only — indexes then exits
./start.sh api          # API only
./start.sh worker-api   # Worker + API, no UI
./start.sh ui-api       # Web UI + API, no Worker
```

Logs stream to `.logs/{worker,api,web}.log`. To run pieces individually without the script:

```bash
docker compose up -d                                   # postgres (pgvector) + ollama
docker exec semantic-search-poc-ollama-1 ollama pull nomic-embed-text   # first time only, ~270 MB
dotnet run --project src/SemanticSearch.Worker         # index data/sample-files/ then exits when done
dotnet run --project src/SemanticSearch.Api            # http://localhost:5050
npm --prefix src/SemanticSearch.Web run dev            # http://localhost:5173 (proxies /api → :5050)
```

Frontend build / lint (there is **no .NET test project** in this repo):

```bash
npm --prefix src/SemanticSearch.Web run build   # tsc -b && vite build
npm --prefix src/SemanticSearch.Web run lint     # eslint
```

Requires .NET 10 SDK, Node 20+, Docker. Postgres is exposed on host port **5433** (not 5432 — the README's config table is stale here); connection strings in `appsettings.json` already point at 5433.

## Architecture

Three .NET 10 projects + a React frontend, wired around pgvector and a local Ollama embedding model. Solution file is [SemanticSearch.slnx](SemanticSearch.slnx).

```
data/sample-files/ → Worker (extract → chunk → embed) → pgvector ← API (embed query + cosine search) ← React UI
```

**Worker** ([src/SemanticSearch.Worker](src/SemanticSearch.Worker)) — a `BackgroundService` that scans the indexing folder once, then the pipeline for each file:
1. [ContentExtractor](src/SemanticSearch.Worker/Services/ContentExtractor.cs) pulls text from PDF (PdfPig) / DOCX / XLSX (OpenXml) — in memory only.
2. [IndexingPipeline](src/SemanticSearch.Worker/Services/IndexingPipeline.cs) normalizes the filename (splitting `_`, `-`, camelCase, letter/digit boundaries) and **prepends it as a "Document title:" line before chunking** so filename-encoded meaning ends up in the vectors. This is deliberate — it's how queries match files with sparse body text.
3. [TextChunker](src/SemanticSearch.Worker/Services/TextChunker.cs) splits at ~400 words with 40-word overlap.
4. Each chunk is embedded via Ollama and only the vector is inserted. Files are deduplicated by `nas_path` (re-running skips already-indexed files; to re-index, clear the DB).

**API** ([src/SemanticSearch.Api](src/SemanticSearch.Api)) — ASP.NET controllers over Dapper/Npgsql.
- [SearchService](src/SemanticSearch.Api/Services/SearchService.cs) embeds the query, runs a cosine (`<=>`) vector search, dedupes chunks back to one row per file, and **falls back to / merges Postgres full-text keyword search when the top vector score is below `ConfidenceThreshold` (0.65)**. Also falls back to keyword-only if embedding fails.
- [FilesController](src/SemanticSearch.Api/Controllers/FilesController.cs) streams the original file from its stored `nas_path` for preview/download (range-enabled). Note this reads the file from disk on demand — it does not violate the no-persisted-content rule, which is about the search index.

**Web** ([src/SemanticSearch.Web](src/SemanticSearch.Web)) — Vite + React 19 + MUI. Debounced search via [use-search.ts](src/SemanticSearch.Web/src/hooks/use-search.ts) hitting the relative `/api/search`, proxied to the API by [vite.config.ts](src/SemanticSearch.Web/vite.config.ts).

Both .NET services share a near-identical `OllamaEmbeddingClient` (model `nomic-embed-text`, 768-dim) and read the same config keys. Embedding dimension (768) is hardcoded in three places that must stay in sync: `VECTOR(768)` in the schema, and the Ollama model.

## Conventions

- Config lives in each project's `appsettings.json`: `ConnectionStrings:Postgres`, `OllamaBaseUrl`, and (Worker only) `IndexingFolder` — when blank the Worker defaults to `data/sample-files/` resolved relative to its build output.
- Vectors are passed to Postgres as string literals (`[f1,f2,...]`) cast to `::vector`, since Npgsql has no native vector type here.
- Dapper is configured with `MatchNamesWithUnderscores` so snake_case columns map to PascalCase DTO properties.
- `tools/GenerateSamples` regenerates the demo documents in `data/sample-files/`; it is not part of the solution build.
