# AGENTS.md

## Scope
SwiftData models and stores for iOS. Applies to `RefWatchiOS/Core/Persistence/SwiftData/`.

## Conventions
- Keep models and `ModelContainerFactory` self‑contained. No view/UI dependencies.
- Provide in‑memory stores for tests (e.g., `InMemory*Store`).
- Versioning/migrations: centralize decisions in the factory; avoid scattering across features.

## Testing
- Use in‑memory containers by default in tests. Validate fetch/save flows with small fixtures.

