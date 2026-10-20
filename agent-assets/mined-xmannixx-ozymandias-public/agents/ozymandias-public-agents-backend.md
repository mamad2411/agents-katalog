# Backend (Python) — Agent-Instruktionen

## Stack
- FastAPI mit async/await
- SQLAlchemy 2.0 async
- Pydantic v2 (model_validator, field_validator)
- Celery für Hintergrund-Tasks (Decay, Konsolidierung)

## Regeln
- Rust-Bindings importieren aus ozy_bindings.
- Kein direkter DB-Zugriff in Routes — immer über Service-Layer.
- Fehler als HTTPException mit klaren Codes.
- Type Hints auf allem, mypy strict.
- Claims nur über Proposals (Write-Gate-Pipeline).

## Referenz
- @OZY_ZUSAMMENFASSUNG_v5_2026-04-03.md
- @OZY_DB_Schema.sql
