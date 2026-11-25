---
license: CC-BY-4.0
description: >-
  Use this skill to help agents manage Python projects, dependencies, environments,
  and builds using the `pixi` package manager. Covers installation, project creation
  (pyproject.toml, workspaces, cross-compilation), managing dependencies, security,
  and migrating from other tools like uv.
compatibility: >-
  Pixi 0.78.0 CLI baseline, checked 2026-09-29; pixi-build still requires
  workspace.preview = ["pixi-build"]. Vendored references are an older
  documentation snapshot, not a claim that every example was tested on 0.78.0.
metadata:
  repo: https://github.com/nq-rdl/agent-extensions
  upstream: https://pixi.prefix.dev/
---

# pixi — Package management for reproducible environments

Pixi is a fast, cross-platform, next-generation package manager that provides reproducible environments.

Before relying on version-sensitive commands or build-backend settings, check
the project's Pixi version and the [canonical documentation](https://pixi.prefix.dev/latest/).
The 24 RST references were converted from pixi.prefix.dev documentation and
vendored by 2026-04-26 through agent-skills v0.6.0; their exact upstream
revision was not recorded. Read the reference for the task at hand. Offline,
use it as a snapshot, check local CLI help and report anything unverified.

---

## When to use Pixi

- To create and manage reproducible development environments.
- To handle both Python and non-Python dependencies (e.g., system libraries) in the same environment.
- To manage cross-platform builds and cross-compilation.
- To migrate from `uv` or other package managers.
- When working with PyTorch, Rust, C++, or R.

## Key Concepts

- **Workspaces:** Pixi allows managing multiple projects with shared dependencies using workspaces.
- **Global Tools:** Install isolated CLI tools globally using `pixi global install`.
- **Reproducibility:** Pixi uses lockfiles (`pixi.lock`) to ensure exact versions of packages across platforms.
- **Backends:** Pixi integrates with various build backends (e.g., `pixi-build-cmake`, `pixi-build-python`).

## Consumer checks

- `pixi task add` only registers a command; it does not add its executable as
  a dependency. A pytest task also needs `pytest` in the environment that runs it.
- For an offline deployment, check that `pixi.lock` exists and is current;
  run `pixi lock` on the connected build machine before `pixi-pack`. Packing
  does not create the lockfile. Select only an environment present in the
  manifest; omit `--environment` for default. `pixi exec` does not install a
  global command: keep that prefix on subsequent invocations. Use
  `pixi-unpack` or a self-extracting archive
  on the target; `pixi-pack pack` and `pixi-pack unpack` are not subcommands.
  See [Pixi Pack](references/pixi_pack.rst).
- A named environment includes the default feature unless
  `no-default-feature = true`. `pixi add --feature dev` and
  `pixi add --environment dev` are alternative scopes, not combinable flags.
  Inspect the manifest before choosing one; keep tools out of other environments.

## References

For detailed usage, consult the references:

- [Installation](references/installation.rst)
- [First Workspace](references/first_workspace.rst)
- [Python Tutorial](references/python_tutorial.rst)
- [Python - pyproject.toml](references/pyproject_toml.rst)
- [Python - PyTorch](references/pytorch.rst)
- [Rust Tutorial](references/rust.rst)
- [Global Tools Introduction](references/global_tools_introduction.rst)
- [Build - Getting Started](references/build_getting_started.rst)
- [Build - Python](references/python.rst)
- [Build - C++](references/cpp.rst)
- [Build - Workspace](references/workspace.rst)
- [Build - Advanced C++](references/advanced_cpp.rst)
- [Build - Cross Compilation](references/cross_compilation.rst)
- [Build - Backends](references/backends.rst)
- [Build - pixi-build-cmake](references/pixi-build-cmake.rst)
- [Build - pixi-build-python](references/pixi-build-python.rst)
- [Build - pixi-build-rattler-build](references/pixi-build-rattler-build.rst)
- [Build - pixi-build-r](references/pixi-build-r.rst)
- [Build - pixi-build-rust](references/pixi-build-rust.rst)
- [Key Concepts - Compilers](references/compilers.rst)
- [Deployment - Prefix](references/prefix.rst)
- [Deployment - Pixi Pack](references/pixi_pack.rst)
- [Security](references/security.rst)
- [Switching from uv](references/uv.rst)

## Examples

### Initialize a project

```bash
pixi init
```

### Add dependencies

```bash
pixi add python
pixi add numpy pandas
```

### Run a command inside the environment

```bash
pixi run python script.py
```
