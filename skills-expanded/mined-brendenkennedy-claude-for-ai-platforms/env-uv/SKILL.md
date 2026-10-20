---
name: env-uv
description: >
  The Python environment via uv — creating/syncing the venv, adding pinned deps, and the part that
  actually bites in CV/ML: matching the torch + CUDA wheel to the machine's driver. Carries the
  exact commands: `uv sync` to materialize the locked env, `uv add` to add a dep (never hand-edit
  `pyproject.toml`), `uv run` to execute inside it, the `[[tool.uv.index]]` + `[tool.uv.sources]`
  pattern pinning PyTorch to the right CUDA build, the GPU sanity check, and the reproducibility
  rule (commit `uv.lock`; `uv sync --frozen` in CI). Load before installing anything, when
  `torch.cuda.is_available()` is False, or when setting up a new box. Triggers: uv, uv add, uv sync,
  uv lock, uv run, venv, install a package, add a dependency, pyproject.toml, uv.lock, torch,
  pytorch, cuda, cpu wheel, cuda not available, nvidia-smi, gpu not found, pin versions,
  reproducible environment.
---

# env-uv — the uv + CUDA environment workflow

**Pinned:** uv, torch — unpinned · authored 2026-07 · run `/skill-update env-uv` once the env exists

> On-demand: load this before installing a package, standing up the env on a new machine, or when the
> GPU isn't visible to torch. It carries the commands that work **today** — don't reach for `pip install`
> or hand-edit `pyproject.toml`; both desync the lockfile.

## When this applies
Creating/syncing the env, adding or bumping a dependency, pinning the torch build to a CUDA version, or
debugging "why is `torch.cuda.is_available()` False".

## Create / sync the env
- **Materialize the locked env:** `uv sync` — creates `.venv/` and installs exactly what `uv.lock` pins.
  Use `uv sync --frozen` when the lock must not move (CI, a reproducible run).
- **Run inside it:** `uv run <cmd>` (e.g. `uv run python train.py`) — no manual `activate` needed.
- **New project from scratch:** `uv init` then add deps below.

## Adding & pinning deps (never hand-edit the manifest)
- **Add:** `uv add <pkg>` — resolves, installs, and writes both `pyproject.toml` and `uv.lock`.
- **Dev-only tools** (tests, notebooks, linters): `uv add --dev <pkg>`.
- **Bump / remove:** `uv add <pkg>@<ver>` · `uv remove <pkg>`.
- **Never** edit `pyproject.toml` dependencies or `uv.lock` by hand — that silently desyncs the two. This
  backs the always-on **"deps via `uv`"** convention.

## The torch + CUDA matrix (the sharp one)
PyTorch wheels are CUDA-specific; the default PyPI wheel often isn't the build you want. Pin the index:

```toml
# pyproject.toml — pick the cuXXX that matches the box's driver (see `nvidia-smi`)
[[tool.uv.index]]
name = "pytorch"
url = "https://download.pytorch.org/whl/cu124"
explicit = true

[tool.uv.sources]
torch = { index = "pytorch" }
torchvision = { index = "pytorch" }
```

Then `uv sync`. For a CPU-only box use `.../whl/cpu`. The wheel must match on **two** axes:
- **CUDA version** ≤ the driver's CUDA (from `nvidia-smi`, top-right) — a wheel newer than the driver is
  the usual cause of a silent CPU fallback or a load error.
- **CPU arch** — the default index serves `x86_64`; on **`aarch64`/ARM** boxes (Grace-Blackwell, GB10,
  Jetson) use the arch-appropriate index/source (`<PLACEHOLDER: ARM torch index for your box>`), not the
  x86 URL.

Developing over SSH on a remote GPU host? This all runs the same there — the env lives on that box; just
`uv run` inside the repo over the SSH session.

## Appliance boxes (DGX Spark · GB10/Grace-Blackwell · Jetson) — never `apt`

Know which kind of box you're on before installing anything:

```bash
uname -m                    # aarch64 => not the default x86 wheel index
nvidia-smi -L               # "GB10" / "DGX Spark" => appliance box
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
```

If it's an appliance box, its OS image is **vendor-managed**: kernel, driver, CUDA and boot chain are
a tested set of pinned packages. `apt update` re-points the indexes and the next upgrade walks them
off it — and recovery is a **re-image, not a rollback**. This is canon (`security.md` `S10`) and
`validate-bash.sh` blocks it; the block is host-gated, so it's inert on an ordinary box.

**Install things this way instead:**

| Want | Do |
|---|---|
| A Python package | `uv add <pkg>` — as always |
| A Python CLI (ruff, pre-commit, huggingface-cli) | `uv tool install <pkg>` — no system packages involved |
| A non-Python CLI (ripgrep, jq, conftest, trivy) | Download the **`aarch64`/`arm64`** release binary into `~/.local/bin` and `chmod +x`. An x86 binary will not run — this is the mistake that wastes the most time here |
| Something that genuinely wants a distro | A container — `docker run … apt-get install …` is **allowed**, because the blast radius is an image and not the host |
| A system package, unavoidably | The **user** does it, outside the session, against vendor guidance |

The guard judges the command rather than pattern-matching it, so read-only queries (`apt list`,
`apt show`, `apt policy`, `dpkg -l`) work normally and talking *about* apt — a commit message, a
grep, this table — is never mistaken for running it. It does block `ssh box sudo apt upgrade`: the
far end may be an appliance too, and it has no way to know.

Two more things these boxes change, beyond installation:

- **Unified memory.** Host and GPU share one pool (a Spark has ~128 GB), so the usual "will the
  weights fit in VRAM" arithmetic doesn't transfer — models that are impossible on a 24 GB discrete
  card run here, at very different memory *bandwidth*. Size from measurement, not from a discrete-GPU
  rule of thumb.
- **`aarch64` narrows the wheel and image supply.** Many prebuilt wheels and most published container
  images are x86-only. Check the arch before assuming an image or a `pip install` will work, and
  prefer NVIDIA's ARM-built images (`nvcr.io`) for CUDA workloads.

## When a GPU stack won't co-resolve → an isolated second env
Some GPU libraries can't share one lock with the base project — their transitive pins conflict with the
versions your DS stack needs. The one that bites: **RAPIDS** (`cuml-cu13`, `cudf`) drags in a `numba`
that caps `numpy` *below* what a modern pandas/sklearn base requires, so `uv add cuml-cu13` fails to
resolve into the project lock (or silently downgrades numpy and breaks everything else).

Don't fight the solver or pin numpy backwards for the whole project. **Isolate the conflicting stack in
its own env** and treat it as a separate tool:
- Keep the base `.venv` (project deps) clean and unbroken.
- Stand up a second env — e.g. `.venv-gpu` with its own `pyproject`/lock (a `[project.optional-dependencies]`
  extra, a `uv`-workspace member, or a sibling project dir) — holding *only* the GPU stack + the minimum
  it shares.
- Invoke it explicitly for the GPU step (`uv run --project .venv-gpu …` or activate it for that script);
  the main pipeline stays on `.venv`.
- **Document the split** (which env owns which step, and why) in a short `docs/GPU.md` so the next person
  doesn't re-hit the resolution wall — the conflict is not obvious from the error.

Rule of thumb: one irreconcilable transitive cap is a signal to *separate envs*, not to bend the base
env's pins. (Surfaced by the dota2 dogfood — RAPIDS `cuml-cu13` numba-vs-numpy — resolved exactly this way.)

## GPU sanity check (run after any torch/CUDA change)
```bash
uv run python -c "import torch; print(torch.__version__, torch.cuda.is_available(), \
  torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```
`False` with a GPU present ⇒ wheel/driver mismatch (above) or you're not inside the uv env (use `uv run`).

## Reproducibility
- **Commit `uv.lock`.** It's the reproducibility contract — the same lock reproduces the same env.
- Pin the Python version in `pyproject.toml` (`requires-python`) and, if the project needs it, a
  `.python-version` file so `uv` picks the same interpreter everywhere.
- CI / a "run it for real" invocation uses `uv sync --frozen` so a stale lock fails loudly instead of
  silently resolving something new.

## Lint config (set line-length once, up front)
The `validate-python` hook runs `ruff format` + `ruff check --fix` after every edit. `ruff format`
reflows *code* but **not** prose — it will never wrap a long docstring or comment line, so those throw
E501 that the autofix can't clear and you end up hand-wrapping prose across several edit round-trips.
Set the budget once so lines land right the first time; register it in `pyproject.toml` (via a targeted
Edit — this is config, not a dependency, so the guard allows it):

```toml
[tool.ruff]
line-length = 100   # matches the prose budget; keep docstrings/comments ≤ this as you write
```

100 is the scaffold's convention (ruff's default 88 is tight for prose-heavy modules). It's a limit the
formatter enforces on code but can't satisfy for you on prose — so the real fix is writing prose to it,
not chasing E501 after the fact.

## Gotcha
`uv run` is the boundary — a command that works in your shell but fails under the agent is almost always
running outside the env. Prefix with `uv run`. And if `pyproject.toml` and `uv.lock` ever disagree, you
hand-edited one: `uv sync` (or re-`uv add`) to reconcile, don't patch the lock.
