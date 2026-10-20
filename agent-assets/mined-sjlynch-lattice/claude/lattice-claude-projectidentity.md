# projectIdentity/

Submodules behind the `../projectIdentity.ts` facade (`physicalProjectPath`,
`projectStorageHash`, `matchesStoredProjectIdentity`, `storedProjectRoot`,
`clearProjectIdentityCaches`, re-exported `ProjectIdentityConflictError`).
This code decides which on-disk store (`per-project/<hash>/`, worktrees,
snapshots, backups) belongs to a folder: a mistake strands or cross-wires a
project's whole task DB. Design rationale: `../PROJECT_IDENTITY.md` (stays at
`backend/src/`; `taskCache/` and `worktree/` CLAUDE.md link to it).

## Modules

- `caches.ts` — the process caches (`physicalPaths`, `storageHashes`, `inventories`, `boundStorage`), bounded FIFO at `MAX_PATHS` (2048) by `remember()`; `STORAGE_HASH_LEN` = 12 / `STORAGE_HASH_RE`; `legacyPath` (resolve + upper-case only a Windows drive letter) and `hashPath` (sha1 prefix).
- `inventory.ts` — `inventoryFor(home)`: which existing store hashes under a home are evidence for which physical project, from bindings, `projects.json`, `.canonical-path` markers, the leading ≤64 KB (`METADATA_SCAN_BYTES`) of task/run JSON, and snapshot manifests. Cached per home.
- `binding.ts` — durable `~/.lattice/project-identities/<sha1(physical)[:12]>.json` (`BINDING_VERSION` 1): validation, `readBinding`, exclusive-create `publishBinding` (temp file + `linkSync`, EEXIST → accept only an identical hash), `BINDING_FILE_RE` / `isBindingFileName`.
- `fsProbe.ts` — `exists` / `readDirectory`: ENOENT → false / `[]`; every other error throws.
- `errors.ts` — `ProjectIdentityConflictError`. Keep it dependency-free: every module throws it, so an import here would create a cycle.

## Invariants

- **Never lowercase a whole path.** Case-sensitive Windows dirs and POSIX paths must stay distinct; `legacyPath` touches only the drive letter.
- **A missing path is not cached across turns.** `physicalProjectPath` memoizes a failed realpath only until `setImmediate` (the rest of the current event-loop turn), so a just-created folder resolves physically. Successful resolutions are pinned until restart.
- **Bindings are never overwritten or deleted.** Publish is exclusive-create; nothing in the backend removes `project-identities/`. `clearProjectIdentityCaches` clears memory only (tests / explicit reconfiguration; not while operations own a project).
- **A corrupt or mismatched binding refuses** (`ProjectIdentityConflictError`) rather than being skipped: skipping would release its reservation and could lend that store to an alias's new target.
- **Two existing hashes for one physical project refuse**, preserving every store; never pick one. A hash already reserved for a different physical path also refuses.
- **Escape `.` (and `\s`, `\d`, …) as `\\.` in any `new RegExp(\`…\`)`.** The ac13fa0 split lost the escapes twice: the metadata regex in `inventory.ts` (legacy stores unrecognized, fresh hash chosen — fixed f33bed1) and `BINDING_FILE_RE` (a stray `<hash>_json` parsed as a binding, every project threw — fixed dad030b).
- **`projectIdentity.ts` must not use `latticeHomeDir()`**: `projectPath.ts` imports it (cycle). `identityHome()` is `os.homedir()/.lattice`.
- **Adding a submodule?** The terminal-server imports this module: list it in `FINGERPRINT_FILES` (`../terminalFingerprint.ts`).

## Tests (`../__tests__/`)

- `projectIdentity.test.ts` — case/junction aliases, legacy-store reuse across restart, duplicate-store and retargeted-junction refusals, corrupt/invalid bindings, stray files, `isBindingFileName`.
- `projectIdentityMissingMemo.test.ts` — the per-turn missing-path memo.
- `regExpTemplateEscapes.test.ts` — guard: single-backslash escapes in any template-literal RegExp.
- `terminalFingerprint.test.ts` — `FINGERPRINT_FILES` covers the terminal-server's imports.
