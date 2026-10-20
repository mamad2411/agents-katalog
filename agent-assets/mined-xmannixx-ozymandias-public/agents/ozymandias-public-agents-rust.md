# Rust — Agent-Instruktionen

## Crates
- ozy-contracts: Nur Typen, Enums, Error-Types. Kein Verhalten.
- ozy-core: Validierungslogik. Importiert nur ozy-contracts.
- ozy-bindings: PyO3-Wrapper. Importiert ozy-core.

## Regeln
- Result<T, OzyError> überall.
- Kein unwrap(), kein panic!() in Produktionscode.
- Serde Serialize/Deserialize auf allen public Typen.
- String statt &str in Structs (PyO3-Kompatibilität).
- #[cfg(test)] mod tests {} in jedem Modul.
- cargo clippy --all-targets -- -D warnings muss sauber sein.
- Commits immer erstellen, wenn Arbeit abgeschlossen ist.
- Commits so granular wie moeglich halten.

## Standard-Testreihe (ozy-contracts)
- Enum-DB-Mappings vollständig testen (serialize + deserialize).
- Roundtrip-Tests pro Typ (Enums, Structs, OzyError).
- Negativtests für geschlossene Enums.
- MemoryType unknown-Werte müssen zu Other(String) werden.
- OzyError JSON-Shape (`type`/`detail`) prüfen.
- Golden-JSON und Property-Tests für Stabilität verwenden.
- Vor Abschluss immer laufen lassen:
  - cargo fmt -- --check
  - cargo test
  - cargo clippy --all-targets -- -D warnings

## Typen-Referenz
- @OZY_CONTRACTS_SPEC_v1_2026-04-03.md
