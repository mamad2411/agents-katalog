# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
npm install          # Install dependencies

npm start            # Start REST API server on http://localhost:5000
npm run sync         # Load data/barrios.json into SQLite via POST /api/sincronizar-barrios
npm run scraping     # Run full pipeline: DB barrios → scrape Fincaraiz → ETL → DB propiedades
```

There are no automated tests (`npm test` exits with an error by design).

To run a specific script standalone:
```bash
node scripts/scraper.js   # Not standalone — import ejecutarScraping() from pipeline.js
node scripts/etl.js       # Not standalone — import ejecutarETL() from pipeline.js
node scripts/pipeline.js  # Full pipeline (requires server NOT running — opens its own DB)
node scripts/sincronizar.js  # Requires server to be running on port 5000
```

## Architecture

This is a three-phase data pipeline project for rental property data in Cartagena de Indias, Colombia.

### Data Flow

```
data/barrios.json
      │
      ▼  npm run sync (sincronizar.js → POST /api/sincronizar-barrios)
  SQLite: barrios table
      │
      ▼  npm run scraping (pipeline.js)
  scraper.js  ──→  Fincaraiz HTML (axios + cheerio)
      │               URL pattern: /arriendo/{slug}/cartagena
      │               Scrapes up to 3 pages/barrio, 1500ms pause between requests
      ▼
  etl.js      ──→  raw records → cleaned propiedades
      │               Discards records without price or price outside [$300k–$100M COP]
      ▼
  SQLite: propiedades table (FK → barrios.id)
      │
      ▼  npm start (server.js)
  REST API → GET /api/propiedades, /api/barrios, etc.
```

### Key Architectural Notes

**DB access pattern**: `better-sqlite3` is synchronous. `src/config/database.js` exports module-level functions (`inicializar`, `insertarBarrios`, `obtenerPropiedades`, etc.) that operate on a shared singleton `db` variable. `inicializar()` must be called before any other DB function — the server calls it at startup, and `pipeline.js` calls it directly when run standalone.

**Pipeline vs. server**: `pipeline.js` opens the SQLite DB directly (bypasses the HTTP API). It **cannot run at the same time as the server** if `better-sqlite3` is in exclusive mode — but WAL mode is enabled (`journal_mode = WAL`) so concurrent reads work; only writes conflict. Safe to run pipeline while server is up.

**Schema migration**: `database.js` auto-migrates on startup — adds the `slug` column if missing and generates slugs for existing rows with `generarSlug()`.

**ETL pipeline clears propiedades table**: `db.limpiarPropiedades()` deletes all existing property records before each pipeline run. Each run is a full replace, not an incremental upsert.

**Scraper selectors**: The scraper targets `div.listingCard` cards on Fincaraiz. If Fincaraiz changes their HTML structure, update the selectors in `scripts/scraper.js` (search for `card.find()`).

### Module Responsibilities

| File | Role |
|------|------|
| `src/config/database.js` | SQLite connection, schema, all DB operations |
| `src/config/logger.js` | Winston logger (writes to `logs/`) |
| `src/server.js` | Express entry point, registers routes, calls `db.inicializar()` |
| `src/routes/barrios.routes.js` | POST `/api/sincronizar-barrios`, GET `/api/barrios` |
| `src/routes/propiedades.routes.js` | GET `/api/propiedades`, `/api/propiedades/stats`, `/api/propiedades/:barrioId` |
| `src/middleware/errorHandler.js` | Centralized 404 and global error handlers |
| `scripts/sincronizar.js` | Reads `data/barrios.json`, POSTs batches to running server |
| `scripts/scraper.js` | Exports `ejecutarScraping(barrios[])` — fetches and parses Fincaraiz HTML |
| `scripts/etl.js` | Exports `ejecutarETL(rawRecords[])` — cleans/transforms scraper output |
| `scripts/pipeline.js` | Orchestrator: calls `db.inicializar()`, `ejecutarScraping()`, `ejecutarETL()`, `db.insertarPropiedades()` |

### Database

- File: `data/barrios.db` (generated, not in source)
- `barrios`: 200 Cartagena neighborhoods with coordinates, estrato, infrastructure data
- `propiedades`: scraped rental listings linked to `barrios` via `barrio_id` FK
- WAL mode and `foreign_keys = ON` are always set at connection time
