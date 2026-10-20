# Ozymandias — Agent-Instruktionen

## Projekt
Persönlicher KI-Assistent mit Rust-Kern (Validierung, Governance) und Python-Orchestrierung (FastAPI, LLM, DB).

## Architektur
- Rust: ozy-contracts (Typen) → ozy-core (Logik) → ozy-bindings (PyO3)
- Python: FastAPI + SQLAlchemy 2.0 + Pydantic v2 + Celery
- DB: Postgres + pgvector
- Deployment: Docker-only, VPS + Nginx

## Wichtigste Regeln
- Rust = synchron, kein I/O. Python = async, DB, LLM.
- Kein unwrap() in Produktionscode.
- Claims nur über Proposals, nie direkt in DB.
- .env nie lesen, editieren oder in Code einbetten.
- S3 nur lokal, S4 nur lokal+isoliert.
- Alle Aktionen ins Audit-Log.
- Commits immer erstellen, wenn Arbeit abgeschlossen ist.
- Commits so granular wie moeglich halten (kleine, thematisch klare Einheiten).

## Referenz-Docs
- @OZY_ZUSAMMENFASSUNG_v5_2026-04-03.md — Gesamtspec
- @OZY_CONTRACTS_SPEC_v1_2026-04-03.md — Rust-Typen
- @OZY_DB_Schema.sql — Datenbankschema
