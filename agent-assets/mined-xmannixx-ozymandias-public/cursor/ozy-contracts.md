---
alwaysApply: true
description: "Rust/ozy-contracts Standards: Typen, Serde, Testreihe"
---

# Rust/ozy-contracts Standards

- Alle public Typen in ozy-contracts definieren
- Enums statt Strings für: Sensitivity (S0–S4), TrustLevel (T0–T3), 
  VerificationState, Lifecycle, HandlingPolicy, ApprovalClass
- Serde Serialize/Deserialize auf allen Typen
- PyO3-kompatible Typen (kein &str in Structs, String verwenden)
- Tests in jedem Modul, #[cfg(test)] mod tests {}
- Standard-Testreihe für `rust/ozy-contracts` immer vollständig halten:
  - Enum-String-Mapping-Tests (exakte DB-Strings, serialize + deserialize)
  - Roundtrip-Tests pro Enum/Struct/Error
  - Negativtests für closed Enums (invalid values failen)
  - `MemoryType` unknown -> `Other(String)` statt Fehler
  - OzyError JSON-Shape (`type`/`detail`) testen
  - Golden-JSON-Tests für kritische Fälle
  - Property-Tests für `MemoryType::Other`
- Standard-Check vor Abschluss ausführen:
  - `cargo fmt -- --check`
  - `cargo test`
  - `cargo clippy --all-targets -- -D warnings`
