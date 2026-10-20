---
alwaysApply: true
description: "Rust/Python-Grenze für Ozymandias"
---

# Rust/Python-Grenze

Rust = synchrone Validatoren ohne I/O, kein Async, keine DB-Zugriffe.
Python = Orchestrierung, Async, DB, LLM-Aufrufe, Connectors.

## 8 Rust-Module
- Memory Write-Gates (G1–G3)
- Sensitivity Router
- Approval / PolicyResolver
- Taint Tracker
- Audit Validator
- Decay Engine
- Circuit Breaker (einzig stateful: Arc<Mutex<HashMap>>)
- Token Budget Enforcer

## Crate-Struktur
- ozy-contracts: Typen, Enums, Fehler (kein Verhalten)
- ozy-core: Logik (importiert nur ozy-contracts)
- ozy-bindings: PyO3-Wrapper (importiert ozy-core)

## Regeln
- Rust-Module geben Result<T, OzyError> zurück
- Kein unwrap() in Produktionscode
- Python ruft Rust über PyO3-Bindings auf, nie umgekehrt
