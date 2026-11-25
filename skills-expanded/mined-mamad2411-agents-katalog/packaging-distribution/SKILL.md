---
name: packaging-distribution
description: "This skill should be used when the user is building wheels, creating sdists, packaging compiled extensions, configuring cibuildwheel, setting up maturin for Rust extensions, using scikit-build-core, optimizing package size, working with platform tags, namespace packages, or choosing between pure Python and compiled distributions. Covers wheel format, abi3 stable ABI, manylinux/musllinux tags, dual-package strategy, environment markers, PyPI metadata, and TestPyPI."
version: 1.0.0
---

# Ship Wheels for Every Platform Your Users Run

A package without pre-built wheels forces users to have a compiler toolchain, correct system headers, and patience. Pydantic-core ships 30+ platform-specific wheels so `pip install pydantic` takes seconds, not minutes. Pure Python packages get this for free with a single `py3-none-any` wheel. Compiled extensions require deliberate CI investment -- but cibuildwheel and maturin-action make it tractable.

## Pure Python vs Compiled Extensions

Default to pure Python. Only add compiled extensions when profiling proves Python is the bottleneck and the speedup is 10x or greater.

| Situation | Choice | Examples |
|-----------|--------|----------|
| I/O-bound (network, disk) | Pure Python | FastAPI, httpx, Rich, Click |
| CPU-bound tight loops, parsing, serialization | Compiled extension | Pydantic-core, orjson, Polars |
| Wrapping existing C/C++/Rust library | Compiled extension | cryptography, lxml |

### Extension Technology Decision

| Technology | Language | Build Backend | Used By |
|-----------|----------|---------------|---------|
| PyO3 + maturin | Rust | `maturin` | Pydantic-core, Polars, Ruff, uv, orjson |
| Cython | Cython/C | `setuptools` | uvloop, lxml, scikit-learn |
| pybind11 | C++ | `scikit-build-core` | SciPy (partial), Open3D |
| scikit-build-core | C/C++/Fortran | `scikit_build_core.build` | CMake-dependent projects |
| cffi | C | `hatchling`/`setuptools` | cryptography (backend) |

Rust + PyO3 + maturin is the dominant choice for new compiled extensions (2023-2025). Prefer it for greenfield performance-critical work.

## Wheel Format and Platform Tags

A wheel filename encodes compatibility: `{name}-{version}-{python}-{abi}-{platform}.whl`

```
httpx-0.28.0-py3-none-any.whl                           # Pure Python
pydantic_core-2.27.0-cp312-cp312-manylinux_2_17_x86_64.whl  # CPython 3.12, Linux
cryptography-44.0.0-cp39-abi3-manylinux_2_28_x86_64.whl     # Stable ABI, cp39+
```

### Minimum Wheel Matrix for Compiled Extensions

| Priority | Platform | Tag | Covers |
|----------|----------|-----|--------|
| **Must** | Linux x86_64 | `manylinux_2_28_x86_64` | Most servers, CI, Docker |
| **Must** | macOS ARM | `macosx_11_0_arm64` | Modern Mac (M1-M4) |
| **Must** | Windows x64 | `win_amd64` | Windows users |
| **Should** | macOS Intel | `macosx_10_12_x86_64` | Older Macs |
| **Should** | Linux ARM64 | `manylinux_2_28_aarch64` | AWS Graviton, RPi 4+ |
| **Should** | Linux musl x64 | `musllinux_1_2_x86_64` | Alpine Docker images |

### The abi3 Stable ABI

Build one wheel per platform instead of one per Python-version-per-platform. For a package supporting cp39-cp313 across 3 platforms, abi3 reduces 15 wheels to 3.

```toml
# Cargo.toml (PyO3)
[dependencies]
pyo3 = { version = "0.22", features = ["abi3-py39"] }
```

Used by: cryptography (cp37-abi3), bcrypt, PyYAML.

## sdist vs Wheel Contents

| | sdist (source) | wheel (built) |
|---|---|---|
| **Include** | All source (`.py`, `.rs`, `.c`, `.pyx`), `pyproject.toml`, `Cargo.toml`, `Cargo.lock`, `LICENSE`, `README.md` | Installed packages, compiled `.so`/`.pyd`, `py.typed`, `dist-info/` |
| **Exclude** | `.git/`, CI configs, pre-built binaries, `__pycache__/` | Tests, docs, build scripts, source files for extensions |

```toml
# hatchling
[tool.hatch.build.targets.wheel]
packages = ["src/my_library"]

[tool.hatch.build.targets.sdist]
include = ["src/", "tests/", "pyproject.toml", "README.md", "LICENSE"]
```

Never create a `MANIFEST.in` for new projects. Modern backends manage inclusion in `pyproject.toml`.

## maturin: Rust + Python Packaging

Use the mixed Python/Rust layout for packages with both Python and Rust code.

```toml
[build-system]
requires = ["maturin>=1.7,<2.0"]
build-backend = "maturin"

[tool.maturin]
python-source = "python"
module-name = "my_library._core"
features = ["pyo3/extension-module"]
strip = true
include = ["Cargo.lock"]
```

Ship `.pyi` stub files for the Rust module to enable full type-checking support (as Pydantic-core does with `core_schema.pyi`).

## Pydantic's Dual-Package Strategy

Split into two packages when the compiled core and Python API have different release cadences, contributor pools, and CI complexity. Keep them together (Polars, orjson) when they are tightly coupled.

| | `pydantic` | `pydantic-core` |
|---|---|---|
| Language | Pure Python | Rust (PyO3 + maturin) |
| Build backend | hatchling | maturin |
| Wheel type | `py3-none-any` | 30+ platform wheels |
| CI time | 5-10 minutes | 30-60 minutes |

Pin the core dependency to an exact version: `"pydantic-core==2.27.0"`.

## Multi-Platform Builds with cibuildwheel

```yaml
# .github/workflows/wheels.yml
jobs:
  build-wheels:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [ubuntu-latest, macos-14, windows-latest]
    steps:
      - uses: actions/checkout@v4
      - uses: pypa/cibuildwheel@v2.22
        env:
          CIBW_BUILD: "cp310-* cp311-* cp312-* cp313-*"
          CIBW_SKIP: "*-win32 *-manylinux_i686"
          CIBW_MANYLINUX_X86_64_IMAGE: manylinux_2_28
          CIBW_MANYLINUX_AARCH64_IMAGE: manylinux_2_28
          CIBW_TEST_REQUIRES: pytest
          CIBW_TEST_COMMAND: pytest {project}/tests -x
          CIBW_ARCHS_MACOS: "x86_64 arm64"
      - uses: actions/upload-artifact@v4
        with:
          name: wheels-${{ matrix.os }}
          path: wheelhouse/*.whl
```

For Rust projects, use `PyO3/maturin-action@v1` instead -- it handles cross-compilation natively and is faster than QEMU emulation for aarch64.

## Package Size Optimization

| Technique | Impact |
|-----------|--------|
| Exclude tests/docs from wheel | High -- often 2-5x reduction |
| Strip debug symbols (`strip = true`) | High -- 5-10x for compiled extensions |
| Enable LTO (`lto = "fat"` in Cargo.toml) | Medium -- smaller and faster binaries |
| Set `codegen-units = 1` in release profile | Medium -- better optimization |
| Store large data externally | High -- avoid bundling datasets |

Audit wheel contents: `unzip -l my_package.whl | tail`

## Conditional Dependencies and Environment Markers

Use PEP 508 markers for platform-specific and version-specific dependencies:

```toml
dependencies = [
    "tomli>=2.0; python_version < '3.11'",
    "uvloop>=0.20; sys_platform != 'win32'",
    "typing-extensions>=4.12; python_version < '3.13'",
]
```

Use minimum version constraints for libraries, not exact pins: `"requests>=2.28"`, not `"requests==2.31.0"`.

## PyPI Metadata

Provide complete, accurate metadata in `[project]`:

```toml
[project.urls]
Homepage = "https://github.com/you/my-library"
Documentation = "https://my-library.readthedocs.io"
Repository = "https://github.com/you/my-library"
Issues = "https://github.com/you/my-library/issues"
Changelog = "https://github.com/you/my-library/blob/main/CHANGELOG.md"
```

Only claim Python version classifiers you actually test in CI. Include `"Typing :: Typed"` if you ship `py.typed`. Preview README rendering with `twine check dist/*` before publishing.

## TestPyPI Workflow

1. Push a pre-release tag (`v1.0.0rc1`)
2. CI builds wheels and sdist
3. CI publishes to TestPyPI
4. Verify the TestPyPI page and test installation
5. Create the release tag (`v1.0.0`)
6. CI publishes to production PyPI

Test installation with: `pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ my-library`

## Review Checklist

When reviewing code for packaging and distribution:

- [ ] Pure Python packages produce a single `py3-none-any` wheel
- [ ] Compiled extensions ship wheels for Linux x86_64, macOS ARM, and Windows x64 at minimum
- [ ] sdist includes all source files needed to build from scratch
- [ ] Wheel excludes tests, docs, benchmarks, and build scripts
- [ ] Debug symbols are stripped from compiled extensions (`strip = true`)
- [ ] `MANIFEST.in` is not used (configure inclusion in `pyproject.toml`)
- [ ] Rust extensions use maturin with the mixed Python/Rust layout
- [ ] `.pyi` stubs exist for compiled extension modules
- [ ] Environment markers handle backport dependencies (`tomli`, `exceptiongroup`)
- [ ] Library dependencies use minimum version bounds, not exact pins
- [ ] PyPI classifiers match versions actually tested in CI
- [ ] `[project.urls]` includes Repository, Issues, and Changelog
- [ ] Built wheel is installed and smoke-tested in CI before publishing
- [ ] Both wheels and sdist are published to PyPI
