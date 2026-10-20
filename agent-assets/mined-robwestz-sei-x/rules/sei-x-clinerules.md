# SIE-X — Cline Instructions

## Projekt
SIE-X (Semantic Intelligence Engine X) — modulär Python-motor för semantisk analys, nyckelordsextraktion och domänspecifik textbearbetning. Primärt SEO-fokus.

## Om mig
- Använder LLMs som utvecklingsverktyg
- Skriver svenska i konversation/docs, engelska i kod
- Föredrar att saker funkar framför "elegant" kod

## Stack
Python 3.10+, spaCy, sentence-transformers, PyTorch, FAISS, FastAPI, Redis, NetworkX, Prometheus/OpenTelemetry.

## Regler
- Enkel, rak kod. Ingen overengineering.
- Redigera befintliga filer — skapa inte nya utan anledning
- Typehints på publika funktioner, skippa på interna
- Docstrings bara där logiken inte är självklar
- Följ befintlig kodstil i filen du redigerar
- Lägg inte till features, refactoring eller docs som inte efterfrågats
- Ingen error handling för omöjliga scenarion
- Inga emojis

## Struktur
- `core/` — huvudmotorer (engine.py, simple_engine.py)
- `transformers/` — domänspecifika (SEO, medicinsk, juridisk, finans, kreativ)
- `api/` — FastAPI-server, routes, auth, middleware
- `sdk/` — Python SDK
- `cache/` — CacheManager + Redis
- `monitoring/` — metrics, observability
- `agents/` — autonoma agenter (Ray)
- `chunking/` — dokumentuppdelning
- `graph/` — grafoptimering
