# SIE-X — Cursor Rules

## Om projektet
SIE-X (Semantic Intelligence Engine X) är en modulär Python-motor för semantisk analys, nyckelordsextraktion och domänspecifik textbearbetning. Primärt SEO-fokus.

## Om mig
- Använder LLMs som utvecklingsverktyg, inte som produkt
- Kommer från PyCharm, ny i Cursor/VS Code
- Skriver svenska i kommentarer/docs, engelska i kod
- Föredrar att saker funkar framför att de är "eleganta"

## Stack
- Python 3.10+
- spaCy, sentence-transformers, PyTorch, FAISS
- FastAPI + Uvicorn (API)
- Redis (cache), Prometheus/OpenTelemetry (monitoring)
- NetworkX (grafanalys)

## Kodstil
- Skriv enkel, rak kod. Ingen overengineering.
- Använd dataclasses, inte onödiga abstraktioner
- Typehints på publika funktioner, skippa på interna helpers
- Docstrings bara där logiken inte är självklar
- Följ befintlig kodstil i filen du redigerar

## Gör INTE
- Lägg inte till features som inte efterfrågats
- Skapa inte nya filer om du kan redigera befintliga
- Lägg inte till error handling för scenarion som inte kan hända
- Refaktorera inte omkringliggande kod vid buggfixar
- Skriv inte README/docs utan att bli ombedd
- Använd inte emojis

## Projektstruktur
- core/ — huvudmotorer (engine.py, simple_engine.py)
- transformers/ — domänspecifika transformers (SEO, medicinsk, juridisk, etc.)
- api/ — FastAPI-server, routes, auth, middleware
- sdk/ — Python SDK-klient
- cache/ — CacheManager + Redis
- monitoring/ — Prometheus metrics, observability
- agents/ — autonoma agenter (Ray)
- chunking/ — dokumentuppdelning
- graph/ — grafoptimering
