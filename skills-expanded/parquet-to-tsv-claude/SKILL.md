# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this project is

A small, single-purpose CLI that converts a Parquet file to a TSV
(tab-separated values) file. It is built for use as a step inside
computational workflows (Snakemake, Nextflow, plain shell pipelines),
where correctness, predictable failure modes, and bounded memory matter
more than feature breadth.

Core behaviours that callers (and any change you make) must preserve:

- **Streaming.** Rows flow from parquet in batches via
  `pyarrow.parquet.ParquetFile.iter_batches`. The full table is never
  loaded into memory.
- **Atomic output.** Bytes are written to a sibling `<output>.tmp`,
  `fsync`'d, validated, then `Path.replace()`'d into place. Any failure
  unlinks the temp file and leaves any pre-existing output untouched.
- **Row-count verification.** The number of rows actually written is
  compared to `pf.metadata.num_rows` before the rename. A mismatch raises
  `RowCountMismatchError`.
- **Fail-loud.** Tab/newline/CR inside string cells, unsupported column
  types (binary, list, struct, map, …), and bad arguments all abort
  *before* any byte is written. No silent malformed output, ever.
- **Reproducible exit codes.** `0` success, `1` `ConversionError`, `2`
  `ValueError` (programmer/argument error). Workflow tools depend on
  this.

## Critical rule: virtual environment only

All Python work — installs, tests, lint, type-check, running the CLI —
happens inside the project venv at `./venv/`. **Never** `pip install` to
the system Python. Invoke tools through `./venv/bin/<tool>` rather than
relying on PATH. (The host is Ubuntu/Debian, where the system Python is
PEP 668 protected.) Requires Python 3.10+.

If the venv doesn't exist:

```bash
python3 -m venv venv
./venv/bin/pip install -e ".[dev]"
```

## CLI surface

```text
parquet-to-tsv [-h] [-v] [--null-string NULL_STRING]
               [--on-illegal-char {error,replace}]
               [--batch-size BATCH_SIZE]
               input output
```

- `-v` / `--version` — print `parquet-to-tsv <version>` and exit 0.
- `--null-string` — rendered for SQL NULL. Default: empty string. Must
  not itself contain tab/CR/LF (raises `ValueError` if it does).
- `--on-illegal-char {error,replace}` — what to do with tab/CR/LF inside
  cell values. `error` (default) raises `IllegalCharError`; `replace`
  substitutes a single space.
- `--batch-size` — rows per pyarrow batch when streaming. Default
  `65536`. Must be positive.

### Output format

- UTF-8.
- LF (`\n`) line endings, never CRLF.
- One header row of column names, in parquet schema order.
- Booleans render as `true` / `false` (lowercase).
- Dates / timestamps / times render via `isoformat()`
  (e.g. `2024-01-02`, `2024-01-02T03:04:05+00:00`).
- Decimals render via `str(Decimal)` (preserves scale).
- Supported types: integer, floating, boolean, string/large_string,
  decimal, date, timestamp, time, null. Anything else raises
  `UnsupportedTypeError` upfront.

## Common commands

```bash
./venv/bin/pytest                                         # full suite
./venv/bin/pytest tests/test_converter.py                 # one file
./venv/bin/pytest -k illegal_char                         # match test names
./venv/bin/pytest tests/test_cli.py::test_smoke_help -x   # one test, fail-fast
./venv/bin/ruff check .                                   # lint
./venv/bin/mypy                                           # strict type-check
./venv/bin/parquet-to-tsv input.parquet output.tsv        # run the CLI
```

When passing `VERSION` to `docker build`, the value must be valid PEP 440
(setuptools-scm rejects bare commit SHAs). For local builds, omit the
build-arg and accept the `0.0.0+unknown` fallback, or pass an explicit
PEP 440 string (e.g. `--build-arg VERSION=1.2.3` or
`--build-arg VERSION=0.0.0+g$(git rev-parse --short HEAD)`).

CI runs ruff + mypy + pytest, then builds the Docker image and verifies
it end-to-end. Don't merge work that hasn't passed all three locally.

## Architecture

One streaming pipeline in `src/parquet_to_tsv/converter.py`. Order of
operations matters far more than the file layout:

1. **Validate up front** (`_validate_args`, `_validate_header_chars`,
   `_formatter_for`). Bad arguments, missing input, output dir that
   doesn't exist, an unsupported column type, illegal characters in
   column names — all raise *before* any byte is written. New checks
   belong here, not partway through the write loop.
2. **Stream parquet** via `pq.ParquetFile.iter_batches(batch_size=...)`.
   Inside `_write_body`, each batch is pulled to native Python once via
   `to_pylist()` per column, then iterated row-wise. Don't reintroduce
   full-table loads (`Table.to_pylist()`, `read_table().to_pandas()`,
   etc.).
3. **Format per cell** through type-specific formatters, looked up once
   at the top of `convert()` and indexed by column position. The
   formatter contract is: input is *non-None*, output is `str`. NULL is
   handled by the caller before the formatter is invoked.
4. **Atomic write**. Bytes go to a sibling `<output>.tmp`, `fsync`, then
   the count of rows written is compared against `pf.metadata.num_rows`.
   Only on match does `Path.replace()` move the temp into place. A
   `try / except BaseException: tmp.unlink()` block guarantees any
   failure leaves zero artifacts and doesn't touch any pre-existing
   output file.

The CLI (`src/parquet_to_tsv/cli.py`) is deliberately thin: parse argv,
call `converter.convert()`, translate `ConversionError` → exit 1 and
`ValueError` → exit 2. New behaviour belongs in `converter.py`, not the
CLI. `__main__.py` exists so `python -m parquet_to_tsv` works.

The exception hierarchy is part of the public API; callers catch these:

- `ConversionError` — base for "anything went wrong"
- `IllegalCharError`, `UnsupportedTypeError`, `RowCountMismatchError` — subclasses
- `ValueError` — caller-bug-style argument errors

## Testing discipline

Tests exercise real pyarrow IO via the `write_parquet` fixture
(`tests/conftest.py`), which writes a parquet file to `tmp_path` and
optionally controls `row_group_size` so the streaming code path can be
exercised. Pyarrow internals are not mocked; the one exception is the
row-count-mismatch test, which monkeypatches `pq.ParquetFile` because
that's the only way to force a metadata/data divergence.

This project was built test-driven: write a failing test first, run
pytest to confirm red, then implement to green. Follow that discipline
for new features and bug fixes — don't add behaviour that has no test.

`tests/test_cli.py` contains both in-process tests (calling
`cli.main([...])`) and true subprocess smoke tests (calling
`python -m parquet_to_tsv ...`) — keep both forms working.

## Tooling is strict by design

`pyproject.toml` selects a deliberately broad set of ruff rule families
(F, E, W, I, N, D, UP, ANN, S, B, A, C4, DTZ, EM, ISC, PT, RET, SIM,
TCH, ARG, PTH, ERA, PL, TRY, PERF, RUF, …) and runs mypy in `--strict`
mode. Tests get per-file ignores only for `ANN`, `D`, `S101`, `PLR2004`,
`SLF001`, `INP001`.

Prefer fixing a ruff finding over adding a `# noqa`. When `# noqa` is
the right call, append a one-line justification matching the existing
style (e.g. `# noqa: TRY301 -- caught only for cleanup`).

`pyarrow` ships no type stubs, so `[[tool.mypy.overrides]]` sets
`ignore_missing_imports = true` for `pyarrow.*` only. Do not broaden
that override or disable strict mode globally.

## Docker

Multi-stage `Dockerfile` based on `ubuntu:24.04`. The package installs
into a venv at `/opt/venv` which is on `PATH`. The entrypoint is a
minimal `entrypoint.sh` containing `exec "$@"`, so anything after the
image name is the command. Default `WORKDIR` is `/work`.

```bash
# Build. Without --build-arg VERSION, the image reports the
# "0.0.0+unknown" fallback; that's fine for ad-hoc builds. To stamp a
# specific version, pass a valid PEP 440 string (a bare commit SHA is
# NOT valid PEP 440 and will be rejected by setuptools-scm):
docker build -t parquet-to-tsv .
docker build --build-arg VERSION=1.2.3 -t parquet-to-tsv .
docker build --build-arg VERSION="0.0.0+g$(git rev-parse --short HEAD)" \
             -t parquet-to-tsv .

# Convert ./data.parquet -> ./data.tsv
docker run --rm -v "$PWD":/work parquet-to-tsv \
    parquet-to-tsv data.parquet data.tsv

# Show version (for workflow logs)
docker run --rm parquet-to-tsv parquet-to-tsv --version

# Default CMD prints --help when no command is given
docker run --rm parquet-to-tsv
```

The container runs as root; pass `--user "$(id -u):$(id -g)"` if you
need host-user ownership of mounted output files.

Released images are built once and pushed to **three** registries with
identical content (same digest), tagged with the release version,
`<major>.<minor>`, `<major>`, and `latest`:

- **Docker Hub:** `mriffle/parquet-to-tsv`
- **GHCR:** `ghcr.io/mriffle/parquet-to-tsv`
- **Quay.io:** `quay.io/protio/parquet-to-tsv` (note: `protio`
  namespace, not `mriffle` — this is hardcoded in `release.yml`, not
  derived from `github.repository`)

Auth:
- GHCR — workflow's default `GITHUB_TOKEN` (`packages: write`)
- Docker Hub — `secrets.DOCKERHUB_USERNAME` / `secrets.DOCKERHUB_PASSWORD`
- Quay.io — `secrets.QUAY_USER` / `secrets.QUAY_PASSWORD`

## Versioning

Version is dynamic via `setuptools-scm`, derived from `git describe`. At
runtime it's read via `importlib.metadata.version("parquet-to-tsv")` and
exposed as `parquet_to_tsv.__version__`. Two gotchas:

- **After creating a new git tag locally**, re-run
  `./venv/bin/pip install -e ".[dev]"` to refresh installed metadata;
  otherwise `parquet-to-tsv -v` keeps reporting the version captured at
  last install.
- **Docker builds** can't see `.git/` (it's in `.dockerignore`). The
  Dockerfile reads `ARG VERSION` and exports
  `SETUPTOOLS_SCM_PRETEND_VERSION_FOR_PARQUET_TO_TSV`. CI computes
  `VERSION` from `git describe`; the Release workflow uses the GitHub
  release tag with the leading `v` stripped. `fallback_version` in
  `pyproject.toml` is `0.0.0+unknown` so a build with no version info
  fails loud at runtime rather than reporting something misleading.

To cut a release:

```bash
git tag v1.2.3
git push origin v1.2.3
# Then create a GitHub Release from that tag (UI or `gh release create`).
```

The Release workflow (`.github/workflows/release.yml`) builds and pushes
the image, then pulls it and re-asserts `--version` matches the tag
before the job exits.

## CI / Release workflows

- `.github/workflows/ci.yml` — runs on every push and PR. Job 1: ruff +
  mypy + pytest. Job 2: docker build, then verify `--version`, the help
  CMD, an end-to-end conversion through a mounted volume, and that an
  illegal-char failure exits non-zero with no output artifacts.
- `.github/workflows/release.yml` — runs on GitHub release publish.
  Logs in to GHCR (default `GITHUB_TOKEN`, `packages: write`), Docker
  Hub (`secrets.DOCKERHUB_USERNAME` / `secrets.DOCKERHUB_PASSWORD`), and
  Quay.io (`secrets.QUAY_USER` / `secrets.QUAY_PASSWORD`), builds the
  image once with the release tag as `VERSION`, pushes the same
  multi-tagged image to all three registries, then pulls each and
  verifies `--version` round-trips.
