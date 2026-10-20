# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CloudMask is a Python library and CLI tool that anonymizes AWS infrastructure identifiers (resource IDs, account IDs, ARNs, IPs, domains, company names) for secure LLM processing. Anonymization is deterministic (HMAC-SHA256 + seed), reversible via encrypted mapping files, and structure-preserving (AWS prefixes like `vpc-`, `i-`, `sg-` are retained).

## Development Commands

```bash
# Setup
uv venv && uv pip install -e ".[dev]"

# Quality checks
make format          # black (line-length 100)
make lint            # ruff check
make lint-fix        # ruff check --fix
make type-check      # mypy (strict mode)
make quality-check   # all of the above + pydocstyle

# Tests
make test            # pytest (includes coverage)
make test-cov        # pytest with HTML coverage report
pytest tests/test_cloudmask.py              # single file
pytest tests/test_cloudmask.py::test_name   # single test

# Docs
make docs            # Sphinx HTML docs → docs/_build/html/
```

## Architecture

Source lives in `src/cloudmask/` using a src-layout. The package is organized into four subpackages:

**Core layer** (`core.py`, `anonymizer.py`, `mapper.py`):
- `CloudMask` — main entry point; composes `Anonymizer` + `MappingManager`
- `CloudUnmask` — reverses anonymization using a mapping dict or file
- `TemporaryMask` — context manager for scoped anonymization
- `Anonymizer` — HMAC-SHA256 hashing engine with 16-hex-char truncation; maintains an in-memory mapping dict
- `MappingManager` — JSON mapping file I/O with atomic writes, seed verification, and merge support

**config/** — `Config` and `CustomPattern` dataclasses, multi-format loader (YAML/JSON/TOML + env vars), predefined templates via `ConfigTemplates`. `DEFAULT_SEED = "default-seed"` defined here.

**io/** — `Storage` singleton for `~/.cloudmask/` central storage (secure permissions 700/600), `FileProcessor` for bounded file I/O (100MB limit), `streaming.py` for chunked large-file processing with optional tqdm progress

**utils/** — `patterns.py` has pre-compiled regex for all AWS resource types + `AWS_RESOURCE_PREFIXES` frozenset; `security.py` provides Fernet/AES-256 encryption with PBKDF2 key derivation; `cache.py` has LRU cache (1000 entries); `ratelimit.py` has token-bucket rate limiters

**cli/** — argparse-based CLI dispatching to handler functions in `cli_handlers.py`. Entry point: `cloudmask.cli.cli:main`

## Claude Code Hooks

CloudMask integrates with Claude Code via hooks that intercept file and prompt operations. The hook system lives in `scripts/hooks/` and is installed globally to `~/.claude/hooks/`.

### Hook Files

| File | Event | Purpose |
|------|-------|---------|
| `_hook_common.py` | (shared module) | Seed resolution, cached PBKDF2 Fernet crypto, mapping I/O, constants |
| `mask-hook.py` | PreToolUse (Read/Write/Edit) | Anonymizes file content via shadow copies at `~/.cloudmask/hooks/shadow/` |
| `demask-hook.py` | PostToolUse (Write/Edit) | Restores real values when Claude writes back to shadow files |
| `prompt-mask-hook.py` | UserPromptSubmit | Blocks prompts containing sensitive IDs, saves masked version to `~/.cloudmask/.blockedprompts/` |

### Seed Resolution (3-tier)

Hooks read the seed in order: OS keychain (`keyring.get_password("cloudmask", "seed")`) → file (`~/.cloudmask/seed`, 0o400) → env var (`$CLOUDMASK_SEED`).

### Key Design Decisions

- **Fail-closed**: mask-hook emits a `block` decision (not silent exit) when seed is missing
- **Encrypted mapping**: `mapping.json` is Fernet-encrypted with PBKDF2-derived key; deterministic salt from seed hash enables `@lru_cache` (one PBKDF2 derivation per process, not per operation)
- **No double anonymization**: Files and prompts containing `<!-- CLOUDMASK:SANITIZED -->` marker are passed through without re-anonymization
- **Empty mapping safety**: demask-hook refuses to write anonymized content to real files when reverse mapping is empty
- **Prompt blocking UX**: Blocked prompts are saved to `~/.cloudmask/.blockedprompts/YYYYMMDD-HHMMSS-<hash>.txt` with instructions header; user resubmits via `@path`. Files auto-cleaned after 15 days.
- **demask-hook avoids cloudmask imports**: For fast startup, it uses `_hook_common.py` crypto directly instead of importing the full cloudmask package

### Installing / Uninstalling Hooks

```bash
python3 scripts/install-hooks.py                        # interactive install
python3 scripts/install-hooks.py --seed <seed>           # install with specific seed
python3 scripts/install-hooks.py --status                # check installation
python3 scripts/install-hooks.py --uninstall             # remove hooks
```

The installer copies hook files to `~/.claude/hooks/`, stores the seed in the OS keychain + file fallback, and merges hook config into `~/.claude/settings.json` (tagged `cloudmask-hooks` for clean uninstall).

## Key Conventions

- **Python 3.10+** required. Uses `match/case`, `X | Y` union types, `list[T]`/`dict[K,V]` generics.
- **Type annotations** on all public functions (mypy strict mode).
- **Google-style docstrings** enforced by pydocstyle.
- **Line length**: 100 characters (black + ruff).
- **Import order**: ruff isort with `cloudmask` as known first-party.
- **Exceptions**: custom hierarchy rooted at `CloudMaskError` in `exceptions.py`. Six subclasses: `ConfigurationError`, `ValidationError`, `FileOperationError`, `MappingError`, `EncryptionError`, `ClipboardError`.
- **`__init__.py`** re-exports the full public API (~91 names) via lazy `__getattr__`. New public symbols must be added there.
- **Ruff ignores**: `F401` in `__init__.py`, `ARG`/`S101` in tests.
- **Atomic file writes**: All hook file I/O uses `tempfile.mkstemp` + `os.fdopen` + `Path.replace` pattern.
- **File locking**: `fcntl.flock` (LOCK_EX for writes, LOCK_SH for reads) on `mapping.json.lock`.

## Known Development Gotchas

### zsh `\!` escaping in hook-wrapped output

When developing with hooks active, zsh's history expansion can escape `!` to `\!` in content that passes through the Bash hook wrapper. This corrupts Python operators like `!=` to `\!=` (SyntaxError). **This only affects developers editing CloudMask source through Claude Code** — library users and normal hook users are not affected.

**Workarounds:**
- Add `setopt NO_BANG_HIST` to `~/.zshrc` to disable zsh history expansion (recommended)
- Use string concatenation in tests for values containing `!` (e.g., `"vpc-" + "A1B2C3D4"`) to avoid hook interception
- When writing files via Claude Code, verify no `\!` was injected: `grep -r '\\!' src/ tests/`

### Hooks venv

Hooks run from a dedicated venv at `~/.cloudmask/.venv/` (not the project venv). The installer creates this automatically. If hooks fail silently in other projects, run `python3 scripts/install-hooks.py` to recreate the venv.
