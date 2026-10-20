# SQLite Memory Module

This directory owns the `sqlite-memory` repo module — an alternative SQLite-backed memory provider.

- Registers a SQLite-backed memory provider when `providers.memory` is set to `"sqlite-memory"` in config.
- Data is stored in `memory.db` under the module's `ModuleStorage` directory.
- The provider class and its test are module-owned and live in this directory. Core only owns the `MemoryProvider` contract and the provider registry.
- Requires the `sqlite3` CLI on the host; health check probes it before reporting healthy.
