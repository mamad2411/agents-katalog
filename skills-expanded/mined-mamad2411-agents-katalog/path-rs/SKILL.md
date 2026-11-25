---
name: path-rs
description: >
  Use, implement, test, and explain the path-rs Rust library: expansion, lexical
  normalize/resolve, platform dirs, listing, discovery, glob/predicate search,
  caching, identity keys, UTF-8, and Windows/WSL helpers. Includes every
  repository example and when to run it. Use when the user runs /path-rs, asks
  how to expand/normalize/resolve paths, list/search directories, app_paths,
  PathError, or path-rs APIs, or when integrating path-rs into application code.
  Triggers: path-rs, expand_input, normalize, resolve_inside, list, search,
  MemoryCache, app_paths, path_identity_key, PathBuf complement.
---

# path-rs agent playbook

Load this skill for **using or extending** `path-rs`. For crate layout / features / CI conventions, also load `rust-crate-setup` when changing package structure.

`path-rs` **complements** `std::path::{Path, PathBuf}` — it does not replace them. Internal representation is always `Path` / `PathBuf` / `OsStr`.

Full copy-paste example sources live in `examples/*.rs` and are summarized in [references/examples-catalog.md](references/examples-catalog.md).

## Mental model

| Layer | What | FS I/O? | Symlinks? |
| --- | --- | ---: | --- |
| Expand | `~`, `%VAR%`, `$VAR` / `${VAR}` | Home/env only | No |
| Lexical | `normalize`, `resolve_*`, `join_relative`, containment | No | No |
| Canonical | `canonicalize_existing` | Yes, must exist | Yes |
| Platform | drive/UNC/verbatim/reserved/WSL classify | No (syntax) | No |
| Dirs | `platform_dirs`, `app_paths` | Platform APIs | No |
| Inspect | existence / metadata summary | Yes | Partial |
| List / discover / search | walk, globs, predicates (`listing`/`search`) | Yes | Configurable |
| Cache | memory / optional persistent | Via search | N/A |
| Identity / text / UTF-8 | comparison keys, tokens, encoding | Configurable / none | Configurable |

**Product-specific logic** (VCS roots, repo inventories, mutations, cloud remotes) stays in the app. Compose path-rs primitives; do not hardcode domain skip lists inside the crate.

## Install

```toml
[dependencies]
path-rs = "0.1"
# optional:
# path-rs = { version = "0.1", features = ["persistent-cache", "unicode", "async"] }
```

Default features: `listing`, `search`.

| Feature | Enables |
| --- | --- |
| `listing` | `list`, `walk`, `discover_*`, `visit_directories` |
| `search` | `search`, `search_with`, `search_with_cache` (+ listing) |
| `persistent-cache` | `PersistentCache` |
| `unicode` | `logical_path_key` |
| `async` | spawn_blocking wrappers for list/search |

## Hard rules (do not regress)

1. Lexical APIs must not hide filesystem I/O.
2. Do not follow symlinks by default.
3. Do not enable caching by default (`CachePolicy::Bypass`).
4. Lexical root containment is **not** symlink-safe.
5. Never expand `$(command)` / backticks / shell syntax.
6. Reject Windows drive-relative paths (`C:foo`, `C:`) where the crate does.
7. Never round-trip `path_to_string_lossy` back into FS operations.
8. Identity keys and logical path keys are for **comparison**, not I/O paths.
9. Public fallible APIs return `Result<…, PathError>`.

## Run all examples

From repo root:

```bash
cargo run --example expand
cargo run --example normalize
cargo run --example resolve
cargo run --example dirs
cargo run --example identity
cargo run --example inspect
cargo run --example match_path
cargo run --example platform
cargo run --example text_utf8
cargo run --example text_utf8 --features unicode
cargo run --example list              # needs listing (default)
cargo run --example discovery         # needs listing
cargo run --example search            # needs search
cargo run --example cache             # needs search
cargo run --example persistent_cache --features persistent-cache
```

## API by task

### 1. Expand user / CLI path input

**When:** raw user strings with `~` or env vars.  
**Example:** `expand`  
**Key types:** `ExpandOptions`, `expand_input`, `expand_tilde`, `expand_percent_variables`, `expand_dollar_variables`

```rust
use path_rs::{expand_input, ExpandOptions};

let opts = ExpandOptions {
    expand_tilde: true,
    expand_percent_variables: true,
    expand_dollar_variables: true,
    translate_wsl_paths: false,
    reject_undefined_variables: true, // strict: error on missing env
    trim_cli_input: true,
    max_expansion_depth: 8,
};
let path = expand_input("~/work/${PROJECT}", &opts)?;

// No expansion:
let literal = expand_input("~", &ExpandOptions::none())?;
```

Supported: `~` / `~/path` only (no `~user`); `%VAR%` (+ `%%` escape); `$VAR` / `${VAR}`.  
Optional WSL: set `translate_wsl_paths` or call `translate_wsl_path("/mnt/c/...")`.

### 2. Lexical normalize vs canonicalize

**When:** clean `.` / `..` / duplicate separators without I/O; or real FS identity.  
**Example:** `normalize`

```rust
use path_rs::{normalize, canonicalize_existing};

let n = normalize("foo/./bar/../baz")?; // PathBuf::from("foo/baz") — no I/O
let c = canonicalize_existing(".")?;    // must exist; resolves symlinks
```

Do **not** call canonicalize merely to “clean” a path.

### 3. Resolve, join, root containment

**When:** join under a base; reject absolute children; lexical sandbox.  
**Example:** `resolve`  
**Security:** not symlink-safe.

```rust
use path_rs::{
    absolute, ensure_inside, is_lexically_inside, join_relative,
    resolve_against, resolve_inside,
};

let abs = absolute("src/lib.rs")?;
let joined = join_relative("/repo", "src/main.rs")?; // Err if child is absolute
let inside = resolve_inside("/repo", "src/main.rs")?;
// resolve_inside("/repo", "../escape") => Err(PathError::RootEscape)
let ok = is_lexically_inside(Path::new("/repo/src"), Path::new("/repo"));
let ensured = ensure_inside("/repo", "/repo/src/lib.rs")?;
```

| API | Absolute child | Escaping `..` |
| --- | --- | --- |
| `resolve_against` | allowed (ignores base) | may leave root |
| `join_relative` | **error** | may leave root |
| `resolve_inside` | error / escape | **error** `RootEscape` |

### 4. Windows / WSL classification

**When:** policy checks, display cleanup, WSL→Windows.  
**Example:** `platform`  
**I/O:** none (syntax only).

```rust
use path_rs::{
    is_device_namespace, is_drive_relative, is_reserved_windows_name, is_unc,
    is_verbatim, path_contains_reserved_name, simplify_for_display, translate_wsl_path,
};
use std::ffi::OsStr;
use std::path::Path;

let p = Path::new(r"\\?\C:\repo");
let _ = (
    is_drive_relative(p),
    is_unc(p),
    is_verbatim(p),
    is_device_namespace(p),
    path_contains_reserved_name(p),
    is_reserved_windows_name(OsStr::new("CON")),
    simplify_for_display(p),
);
// Only /mnt/<letter>/... :
let win = translate_wsl_path("/mnt/c/Users/demo")?; // Some(C:\Users\demo) on translation
```

### 5. Platform dirs and app roots

**When:** config/data/cache roots for an application name.  
**Example:** `dirs`  
Never conflate **app root** with **repo root** or CWD.

```rust
use path_rs::{
    app_paths, app_paths_with_options, AppPathsOptions, AppRootPolicy,
    cache_dir, config_dir, data_dir, platform_dirs, temp_dir,
};

let dirs = platform_dirs()?;
let paths = app_paths("my-tool")?;
let custom = app_paths_with_options(AppPathsOptions {
    application_name: "my-tool".into(),
    environment_override: Some("MY_TOOL_HOME".into()),
    create_directories: true,
    root_policy: None, // or Some(AppRootPolicy::…)
})?;
// Product subdirs are app-owned:
let _ = custom.root_dir.join("mutations");
```

### 6. Path identity and dedup

**When:** compare paths without treating them as FS paths.  
**Example:** `identity`

```rust
use path_rs::{
    CaseNormalization, PathIdentityOptions, PathRecord,
    deduplicate_paths, path_display_string, path_identity_key,
};

let opts = PathIdentityOptions {
    case: CaseNormalization::AsciiLowercase,
    ..PathIdentityOptions::default()
};
let key = path_identity_key(r"C:\Users\Floris\Repo", opts)?;
let unique = deduplicate_paths([/* PathBufs */], opts)?;
let record = PathRecord::from_path("src/lib.rs", Some(opts))?;
```

### 7. Inspect directories

**When:** existence / readability / metadata summary before walk.  
**Example:** `inspect`

```rust
use path_rs::{directory_exists, inspect_directory, is_existing_directory, require_directory};

if directory_exists(".") {
    let info = inspect_directory(".")?;
    let dir = require_directory(".")?; // Err if missing / not dir
    let _ = (info, dir, is_existing_directory("."));
}
```

### 8. Executable / command-line path match

**When:** compare exe paths or detect a path token in a cmdline string.  
**Example:** `match_path`  
Does **not** spawn processes.

```rust
use path_rs::{
    CommandLinePathMatchOptions, ExecutableMatchOptions,
    command_line_contains_path, executable_paths_match,
};
use std::path::Path;

let same = executable_paths_match(
    Path::new("C:/Tools/app.exe"),
    Path::new(r"C:\Tools\app.exe"),
    ExecutableMatchOptions::new(),
)?;
let found = command_line_contains_path(
    r#"tool --input "C:\repo\src\main.rs""#,
    Path::new(r"C:\repo\src\main.rs"),
    CommandLinePathMatchOptions::new(),
)?;
```

### 9. Text tokens and UTF-8

**When:** normalize string tokens; strict or lossy UTF-8 conversion.  
**Example:** `text_utf8`

```rust
use path_rs::{
    CaseNormalization, TextNormalizationOptions, normalize_path_token,
    path_to_string_lossy, path_to_utf8,
};
use std::path::Path;

let token = normalize_path_token(
    r"  Foo\Bar\  ",
    &TextNormalizationOptions {
        trim_whitespace: true,
        trim_trailing_separators: true,
        normalize_separators: true,
        case: CaseNormalization::AsciiLowercase,
    },
);
let s = path_to_utf8(Path::new("src/lib.rs"))?;
let log = path_to_string_lossy(Path::new("src/lib.rs")); // UI/logs only

#[cfg(feature = "unicode")]
let nfc = path_rs::logical_path_key(Path::new("café/path"));
```

### 10. List and walk (`listing`)

**When:** directory enumeration.  
**Example:** `list`  
Defaults: no symlink follow, no cache, hidden excluded, fail-fast, optional sort.

```rust
use path_rs::{EntryKind, FileEntry, ListOptions, SortMode, list, sort_entries, walk};

let entries = list(
    ".",
    &ListOptions::new()
        .recursive(true)
        .include_hidden(false)
        .max_depth(Some(8))
        .sort(SortMode::DirsFirst),
)?;

for entry in walk(".", &ListOptions::new().recursive(true).max_depth(Some(2)))? {
    let entry = entry?;
    let _ = entry.kind; // EntryKind
}

let mut batch = vec![/* FileEntry */];
sort_entries(&mut batch, SortMode::DirsFirst);
```

### 11. Discovery (`listing`)

**When:** find directories by options or predicate; visitor control flow.  
**Example:** `discovery`  
Skip lists are **caller-configured** (not hardcoded VCS rules).

```rust
use path_rs::{
    DirectoryInspection, DirectoryVisitor, DiscoveryOptions, VisitControl,
    discover_directories, discover_where, visit_directories,
};
use std::path::Path;

let opts = DiscoveryOptions::new()
    .recursive(true)
    .max_depth(Some(2))
    .max_entries(Some(50))
    .skip_names(["target", ".git"]);

let dirs = discover_directories(".", &opts)?;
let cargo_roots = discover_where(".", &opts, |path, _| {
    path.join("Cargo.toml").is_file()
})?;

struct Counter { seen: usize }
impl DirectoryVisitor for Counter {
    fn visit_directory(&mut self, path: &Path, inspection: &DirectoryInspection) -> VisitControl {
        let _ = (path, inspection);
        self.seen += 1;
        if self.seen >= 20 { VisitControl::Stop } else { VisitControl::Continue }
    }
    fn visit_error(&mut self, _path: &Path, _error: &path_rs::PathError) -> VisitControl {
        VisitControl::Continue
    }
}
visit_directories(".", &opts, &mut Counter { seen: 0 })?;
// Or closure: VisitControl::Continue | SkipChildren | Stop
```

### 12. Search (`search`)

**When:** glob includes/excludes or predicate filters.  
**Example:** `search`  
Patterns are relative to the search root.

```rust
use path_rs::{
    EntryKind, ListOptions, SearchRequest, search, search_with,
    search::predicates,
};

let hits = search(
    &SearchRequest::new(".", ["**/*.rs", "**/Cargo.toml"])
        .exclude(["**/target/**"])
        .options(ListOptions::new().recursive(true).max_depth(Some(3))),
)?;

let opts = ListOptions::new().recursive(true).max_depth(Some(2));
let rs = search_with(".", &opts, predicates::extension("rs"))?;
let cargo = search_with(".", &opts, predicates::filename("Cargo.toml"))?;
let dirs = search_with(".", &opts, predicates::kind(EntryKind::Directory))?;
// Also: predicates::{min_size, max_size, is_hidden, …}
```

### 13. Caching

**When:** opt-in read-through discovery/search cache.  
**Examples:** `cache` (memory), `persistent_cache` (feature)  
**Never** treat cache hits as a security boundary. Keys include root + patterns + options.

```rust
use path_rs::{
    CacheKey, CacheMode, CacheOptions, CachePolicy, CacheValue, DiscoveryCache,
    MemoryCache, SearchRequest, search_with_cache,
};
use std::sync::Arc;
use std::time::Duration;

let cache = Arc::new(MemoryCache::new(CacheOptions {
    mode: CacheMode::Memory,
    ttl: Some(Duration::from_secs(60)),
    max_entries: 128,
    validate_metadata: false,
}));

let mut req = SearchRequest::new(".", ["**/*.rs"]);
req.cache = CachePolicy::ReadThrough;
let hits = search_with_cache(&req, Some(cache.as_ref()))?;

// Manual: cache.get/put/invalidate/clear; CacheKey::from_search(&req)
// Disabled: CacheMode::Disabled is a no-op store
```

Persistent (feature `persistent-cache`):

```rust
use path_rs::{CacheMode, CacheOptions, CachePolicy, PersistentCache, SearchRequest, search_with_cache};
use std::time::Duration;

let cache = PersistentCache::open(
    "my-app",
    "search-cache.json",
    CacheOptions {
        mode: CacheMode::Persistent,
        ttl: Some(Duration::from_secs(60)),
        max_entries: 128,
        validate_metadata: false,
    },
)?;
let req = SearchRequest::new(".", ["**/*.rs"]).cache_policy(CachePolicy::ReadThrough);
let _ = search_with_cache(&req, Some(&cache))?;
```

## Errors

All structured failures use `path_rs::PathError` (`thiserror`, `#[non_exhaustive]`). Common variants:

- `EmptyInput`, `EmbeddedNul`
- `UndefinedEnvironmentVariable`, `MalformedEnvironmentVariable`
- `HomeDirectoryUnavailable`, `CurrentDirectoryUnavailable`
- `DriveRelativePath`, `AbsoluteChildPath`, `RootEscape`
- `NotUtf8`, `InvalidPath`, filesystem I/O variants

Match with `matches!(err, PathError::RootEscape { .. })` etc.

## Choosing an API (decision tree)

1. User-typed path with `~`/env? → `expand_input` first.
2. Need clean lexical form without existence? → `normalize`.
3. Need real symlink-resolved path? → `canonicalize_existing` (must exist).
4. Join under base without absolute children? → `join_relative`.
5. Lexical “stay under root”? → `resolve_inside` / `ensure_inside` (document symlink risk).
6. App config/data/cache locations? → `app_paths*` / `platform_dirs`.
7. Compare paths for maps/sets? → `path_identity_key` / `deduplicate_paths`.
8. Enumerate tree? → `list` / `walk`.
9. Find dirs by predicate? → `discover_where` / visitor.
10. Glob or filter files? → `search` / `search_with`.
11. Repeated expensive search? → opt-in `search_with_cache` + `MemoryCache` / `PersistentCache`.

## Implementing new API in this crate

1. Own module under `src/`; re-export from `lib.rs` (feature-gate if needed).
2. Document FS access / existence / symlink behavior in rustdoc.
3. Use `Path`/`PathBuf`; return `PathError`.
4. Add unit + integration/`edge_*` tests; example binary if user-facing.
5. Update crate operation matrix in `lib.rs` + README when behavior classes change.
6. Verify: `cargo test --all-features` and `cargo test --no-default-features`.

See skill `rust-crate-setup` for layout, CI, and package gates.

## Security summary for agents

- Lexical normalize ≠ canonicalize  
- Lexical containment ≠ symlink-safe sandbox  
- Cache ≠ authority  
- Env expansion is untrusted input  
- Glob/search can explode — set `max_depth` / `max_entries` / excludes  
- Details: `SECURITY.md`

## Example index

| Example | Features | Surfaces |
| --- | --- | --- |
| `expand` | — | tilde, `%VAR%`, `$VAR`, `ExpandOptions` |
| `normalize` | — | `normalize`, `canonicalize_existing` |
| `resolve` | — | absolute, join, resolve_inside, containment |
| `dirs` | — | platform + app paths |
| `identity` | — | identity keys, PathRecord, dedup |
| `inspect` | — | directory inspect / require |
| `match_path` | — | executable + cmdline matching |
| `platform` | — | Windows classify, WSL, display |
| `text_utf8` | optional `unicode` | tokens, UTF-8, logical key |
| `list` | `listing` | list, walk, sort_entries |
| `discovery` | `listing` | discover_*, visit_directories |
| `search` | `search` | globs + predicates |
| `cache` | `search` | MemoryCache + search_with_cache |
| `persistent_cache` | `search` + `persistent-cache` | on-disk cache |

Canonical sources: `examples/<name>.rs`. Expanded listings: [references/examples-catalog.md](references/examples-catalog.md).
