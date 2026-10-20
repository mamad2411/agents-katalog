# Config

Kernel-owned configuration and secrets management.

- `config.ts` — KOTA configuration schema, layered loading (global < scope < overrides), and sanitization.
- `scope-config-writer.ts` — no-follow, atomic scope configuration mutation inside the verified real scope root.
- `config-warnings.ts` — validation of unknown config keys and invalid concurrency settings.
- `scope-root.ts` — single source of truth for resolving the scope root
  the daemon and operator CLI act on. Operator surfaces that need a scope
  root must go through `resolveScopeRoot` rather than reaching for
  `process.cwd()` directly, so the `KOTA_SCOPE_ROOT` env var and the
  `--scope-root` CLI flag are honored consistently.
- `secrets.ts` — canonical-scope secret-store registry, provider-based resolution, and output masking.
- `secret-providers.ts` — secret provider implementations (env file, JSON file, macOS keychain).

These are core primitives. Do not add module-specific configuration logic here.
Config fields, defaults, and enum values are code-owned contracts. Keep the
TypeScript schema, JSON Schema generation, warnings, and focused tests as the
source of truth instead of maintaining a parallel prose catalog.

Module config slices register from `KotaModule.configSlices` only after shared
module identity admission. Composition roots expose admitted slices before
loading configuration, and loaders hold exact lifecycle leases. Slice modules
declare and export their contract; discovery imports do not mutate the config
registry.

Tests here cover parsing, sanitization, validation, layer precedence, trust
boundaries, and downstream propagation. Do not assert a handwritten inventory
of config keys or copy shipped default values merely to freeze the registry;
inspect declarative values in their canonical source.

Machine authority keys (`trustedScopes`, `scopePolicies`, `scopeAuthority`)
are global-config only. Always strip them from scope config and caller
overrides, including for an otherwise trusted scope; daemon mutations go
through `ScopeAuthorityStore` so trust, policy, revision, and audit remain one
atomic transaction.

Secret files are untrusted input: providers expose only decoded string values.
Keychain commands pass literal arguments to the process boundary, and validate
replacement input before any destructive effect. Tests control that external
process port; unavailable host keychain access must not silently skip rejection
proof.
