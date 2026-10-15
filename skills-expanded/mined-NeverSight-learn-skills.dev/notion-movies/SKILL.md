---
name: notion-movies
description: Semantic search, intelligent enrichment, and duplicate detection for a Notion movie database using TMDB, embeddings, and Qdrant.
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "requires": { "env": ["NOTION_API_KEY", "TMDB_API_KEY"] },
        "optional": { "env": ["QDRANT_URL", "OLLAMA_URL"] },
        "primaryEnv": "NOTION_API_KEY"
      }
  }
---

# 🎬 Notion Movies Skill

This skill transforms a Notion movie database into an intelligent, searchable, and self-enriching system.

It combines:

- Notion (data storage)
- TMDB (movie metadata)
- Ollama (embeddings)
- Qdrant (semantic search)

---

# 🧠 Why this skill exists

This is **not just about saving and searching movies**.

It turns Notion into a **semantic knowledge system for movies**, allowing agents to:

- understand meaning (not just keywords)
- enrich data automatically
- avoid duplicates
- recommend content intelligently

---

# 🔥 What you can actually do with it

## 🎬 1. Smart movie ingestion

Instead of manually filling fields:

```txt
"add Interstellar"
````

The agent will:

* create the page
* fetch poster
* fetch plot
* fetch director
* fetch genres
* fetch actors, runtime, year
* format everything properly

---

## 🧬 2. Automatic duplicate detection

Prevents:

* Interstellar
* Interstellar (2014)
* Interestellar ❌

Agent behavior:

```txt
"This movie already exists. Enriching instead of duplicating."
```

Detection uses:

* fuzzy matching (typos)
* normalized titles (removes year)
* semantic similarity (vector-based)

---

## 🔎 3. Human-like search (semantic + explainable)

Instead of exact filters, you can ask:

```txt
"movies about time travel"
"romantic movies in Europe"
"movies like Nolan"
"movies that make you think"
```

The system understands intent, not just words.

---

### 🧠 Explainable results

Each result includes:

* similarity score
* reasoning

Example:

```json
{
  "title": "Interstellar",
  "score": 0.92,
  "explanation": "Similar because: genre similarity, plot similarity"
}
```

This makes results **transparent and debuggable**.

---

## 🤖 4. Personal recommendation engine

Example:

```txt
"recommend something like Fight Club"
```

→ returns semantically similar movies

---

## 🧠 5. Turn Notion into a knowledge system

From:

```txt
Static database
```

To:

```txt
Living, searchable, intelligent system
```

---

## ⚡ 6. Agent workflows (OpenClaw)

Example flow:

```txt
User → "I want something like Interstellar"

→ searchMovies
→ rank results
→ explain results
→ suggest options
→ user selects one
→ addMovie
→ enrichMovie
→ index vector
```

---

# ⚙️ Environment Variables

Required:

* `NOTION_API_KEY`
* `TMDB_API_KEY`

Optional:

* `QDRANT_URL` (default: [http://localhost:6333](http://localhost:6333))
* `OLLAMA_URL` (default: [http://localhost:11434](http://localhost:11434))

---

# 🧩 Actions

---

## ➕ addMovie

Creates a movie page (basic structure)

```json
{
  "title": "Interstellar"
}
```

Behavior:

* checks duplicates before creating
* prevents near-identical entries

---

## 🎬 enrichMovie

Enriches a movie with:

* Poster (property + cover)
* Plot (Notion blocks)
* Director
* Genres
* Actors (top 5)
* Year
* Runtime
* Emoji 🎬
* Embedding (vector index)

```json
{
  "title": "Interstellar"
}
```

---

## 🔎 searchMovies

Semantic search with explainability

```json
{
  "query": "movies about space exploration"
}
```

Returns:

* top matches
* similarity score
* explanation

---

## 🔁 indexAllMovies

Sync Notion → Qdrant (vector DB)

---

## 🧠 searchMovies (advanced behavior)

Search uses enriched semantic context:

* themes
* emotional meaning
* relationships
* inferred intent

Not just keywords.

---

## 🧠 recommendMovies

Returns semantically similar movies based on a given title.

```json
{
  "title": "Interstellar"
}
```

Returns:

* top similar movies
* similarity score

---

# 🧠 Embedding Strategy

Embeddings are built from enriched semantic content:

```txt
Title
Genres
Director
Plot
Themes (inferred)
```

---

### ✨ Example embedding input

```txt
Title: Interstellar
Genres: Science Fiction, Drama
Director: Christopher Nolan
Plot: A team travels through a wormhole in space...

Themes: space, time, futuristic
```

---

### ⚡ Optimization

* important fields are repeated (weighting)
* themes inferred automatically from plot
* improves semantic recall and ranking

---

# 🧠 Data Enrichment Logic

## 🎥 Director

* Source: TMDB `/credits`
* Stored in: `Director/es`

---

## 🏷️ Genres

* Source: TMDB `/movie/{id}`
* Stored in: `Género`

---

## 🧠 Plot

* Source: TMDB overview
* Stored as Notion blocks:

  * Callout
  * Quote

---

## 🖼️ Poster

* Source: TMDB
* Stored as:

  * `Portada`
  * Notion cover

---

## 🎭 Actors

* Source: TMDB `/credits`
* Top 5 stored in `Actores`

---

## 📅 Year

* Source: release date
* Stored in `Año`

---

## ⏱️ Runtime

* Source: TMDB details
* Stored in `Duración`

---

# 🔐 Edge Case Handling

## ❌ Movie not found

```json
{
  "error": "Movie not found in TMDB"
}
```

---

## ⚠️ Ambiguous results

```json
{
  "error": "Multiple matches found",
  "options": [
    { "title": "Dune", "year": "2021" },
    { "title": "Dune", "year": "1984" }
  ]
}
```

---

## 🧠 Embedding fallback

If embedding fails:

* returns zero vector
* prevents system crashes
* keeps pipeline running

---

## 🧬 Duplicate handling

System prevents:

* typos
* alternate titles
* same movie with year variations

---

# ⚠️ Notion Schema Requirements

| Property    | Type         |
| ----------- | ------------ |
| Nombre      | title        |
| Director/es | rich_text    |
| Género      | multi_select |
| Portada     | files        |
| Rating      | select       |
| Estado      | status       |

---

# 🧩 Extended Schema (Recommended)

| Property | Type      | Description  |
| -------- | --------- | ------------ |
| Año      | number    | Release year |
| Actores  | rich_text | Main cast    |
| Duración | number    | Runtime      |

---

# 🤖 Agent Guidelines

Agents should:

* ALWAYS use DATABASE_NAME
* ALWAYS check duplicates before adding
* prefer semantic search over filters
* explain recommendations when possible
* enrich instead of duplicating
* only fill missing data
* handle ambiguity before proceeding
* gracefully handle API failures

---

# ⚡ Performance Notes

* embeddings generated via Ollama (`nomic-embed-text:v1.5`)
* vectors stored in Qdrant
* each movie indexed as semantic document
* payload includes metadata for explainability

---

# 🚀 Advanced Capabilities

* Semantic search (embedding-based)
* Explainable recommendations
* Hybrid duplicate detection (semantic + fuzzy)
* Automatic enrichment pipeline
* Robust error handling
* Agent-ready design (OpenClaw compatible)