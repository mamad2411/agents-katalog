# codex-rs/secrets/src/

This file applies to `codex-rs/secrets/src/` and its descendants. Follow the repo root `AGENTS.md` first, then use the local rules below when you edit this subtree.

## Agent Guidance
- Follow the repo-root Rust rules in `/Users/no9labs/Developer/Recursive/codex/AGENTS.md`: keep modules focused, prefer exhaustive matches, and avoid touching sandbox-env handling unless the task explicitly requires it.
- This subtree belongs to the `codex-secrets` crate. Keep public re-exports, module wiring, and tests in sync with any behavior changes here.

## Validate
- `cd /Users/no9labs/Developer/Recursive/codex/codex-rs && just fmt`
- `cd /Users/no9labs/Developer/Recursive/codex/codex-rs && cargo test -p codex-secrets`

## Directory Map
The summary below is based on the existing directory documentation and cross-checked against the files currently present here.

Source code for the `codex-secrets` crate.

### What this folder does

Contains the implementation of encrypted secrets management, including the backend abstraction, local age-encrypted storage, and output sanitization.

### Key files

- `lib.rs` -- Core types and manager:
  - `SecretName` -- Validated name type (A-Z, 0-9, _ only)
  - `SecretScope` -- `Global` or `Environment(String)` with `canonical_key()` for storage keys (e.g., `"global/MY_KEY"`, `"env/myrepo/MY_KEY"`)
  - `SecretListEntry` -- Listing entry with scope and name
  - `SecretsBackendKind` -- Enum (currently only `Local`), derives `JsonSchema`
  - `SecretsBackend` trait -- `set`, `get`, `delete`, `list` operations
  - `SecretsManager` -- Wraps `Arc<dyn SecretsBackend>`, delegates all operations
  - `environment_id_from_cwd(cwd)` -- Derives an environment ID from git repo name or SHA-256 hash of cwd
  - `compute_keyring_account(codex_home)` -- Derives a keyring account string from SHA-256 of codex home path
  - `keyring_service()` -- Returns the constant `"codex"`

- `local.rs` -- `LocalSecretsBackend`:
  - Stores secrets in `~/.orbit/secrets/local.age` (age-encrypted JSON file)
  - Passphrase management: generates random 32-byte passphrase, stores in OS keyring via `KeyringStore`
  - Uses `age::scrypt` for encryption/decryption with `SecretString` passphrases
  - `SecretsFile` -- Internal versioned JSON structure (`version: 1`, `secrets: BTreeMap<String, String>`)
  - Read-modify-write pattern: decrypt, modify, re-encrypt, write atomically

- `sanitizer.rs` -- `redact_secrets(input)`:
  - Regex patterns for common secret formats:
    - `OPENAI_KEY_REGEX` -- `sk-[A-Za-z0-9]{20,}`
    - `AWS_ACCESS_KEY_ID_REGEX` -- `AKIA[0-9A-Z]{16}`
    - `BEARER_TOKEN_REGEX` -- `Bearer [token]`
    - `SECRET_ASSIGNMENT_REGEX` -- `api_key=`, `token:`, `secret=`, `password=` patterns
  - Replaces matches with `[REDACTED_SECRET]`

### Imports from / exports to

**Key imports:**
- `age::{encrypt, decrypt, scrypt::{Identity, Recipient}, secrecy::SecretString}`
- `codex_keyring_store::KeyringStore`
- `regex::Regex` with `LazyLock` for compiled patterns
- `serde::{Serialize, Deserialize}`, `serde_json`

**All public types re-exported through `lib.rs`.**
