# CLAUDE.md

Coding conventions for `aws-research-train-demo`. This file governs **how code is
written**. It does **not** track tasks, plans, or status — that lives in GitHub.
The **what/why** of the demo lives in `SPEC.md`.

---

## Scope of this file

- ✅ Language, tooling, style, dependency, the head contract, testing, commits.
- ❌ Roadmaps, todos, status, design debate, "next steps." Those are GitHub
  issues/milestones, not prose in the repo.

If you (Claude Code) feel the urge to write a plan or track progress in a markdown
file, open a GitHub issue instead.

---

## Architecture rule (read SPEC.md §2 first)

One **neutral spine**, four **domain heads** behind the contract in
`src/heads/base.py`.

- The spine must **never** branch on which domain is loaded. No `if domain == ...`
  anywhere in `src/spine/`, the scripts, the board, or the viewers. If you need to,
  the contract is missing a method — add it to `base.py` instead.
- Heads **train their own way** (HF/PEFT, torch_geometric, neuralop, custom loop)
  but **report through one `MetricSink`** and **checkpoint to the `Run` contract**.
  That uniformity is load-bearing — it's what makes the board, sweep, and compare
  view domain-blind.
- Build the **molecular** head first, end to end, then add weather / genomics / llm
  against the unchanged contract. Adding a head must not touch the spine.

## Language & tooling

- **Python** for the ML spine + heads, because the ecosystem forces it there.
  **Go** for the board (`dashboard/`), because it's a control-plane client, not ML.
  See the language-split rule under *Repo conventions*.
- **`uv` exclusively** for all Python — environment, deps, running, locking.
  - `uv sync` to install core. `uv sync --group <head>` to add a head's deps.
  - `uv add --group <head> <pkg>` to add a head dep. `uv run <cmd>` to execute.
  - **Never** `pip`, `python -m venv`, `poetry`, `conda`, or `requirements.txt`.
  - `pyproject.toml` is the manifest; `uv.lock` committed.
  - Core deps stay minimal. **Each head's deps live in its own uv dependency
    group** keyed to `head.dependency_group`, so installing one head never drags in
    another's stack (no `neuralop` when you only want `molecular`).
  - PEP 723 inline metadata is fine for self-contained scripts (e.g. the marimo
    notebook carrying its own deps).
- Single current stable Python, pinned in `pyproject.toml`; `.python-version`
  committed.

## Code style

- Format + lint with **ruff** (formatter + linter). No black/isort/flake8.
- Type-hint public functions; the head contract in `base.py` is a typed
  `Protocol`/ABC. Run one type checker (declare it in `pyproject.toml`; don't mix).
- Hyperparameters are **CLI arguments**, never module constants. `train.py` runs as
  `uv run python train.py --domain molecular --feat graph --depth deep ...`.
- "Let things be what they want to be": a run wants to be a parameterized job, not
  notebook state; a notebook wants to be a viewer; a head wants to train its own
  way. Don't fight the grain — enforce uniformity only at the contract seam.

## Repo conventions

- Naming follows `aws-<project>-demo`. Layout is fixed by `SPEC.md §6`.
- The notebook in `analysis/` is **marimo** (a `.py` file), not Jupyter. Do not add
  `.ipynb` files to this repo. Don't relocate it to the root or make it the entry
  point.
- **Language split — Go for control-plane / infra clients, Python only where the ML
  ecosystem forces it.** The training spine and heads are Python (PyTorch / PEFT /
  RDKit force it). The board is Go because it's a control-plane client, not ML code.
  Cleanly partitioned by directory; the repo is polyglot but each component is
  single-language.
- **Streamlit is reserved for the science result viewer** (`app/`). **marimo**
  (`analysis/explore.py`) is the operator's reactive cockpit — `marimo edit` to
  author, `marimo run` to serve read-only. Both are Python and dispatch to
  `head.viewer()`.
- **The board (`dashboard/`) is a Go module** (`aws-sdk-go-v2`): own `go.mod`,
  `gofmt`/`go vet` clean, compiles to one static binary. Serves the approved
  `board_template.html` at `/` plus a `/api/jobs` JSON feed; the page's JS polls it
  (relative URLs) and mutates only tiles/curves. Keep AWS calls **read-only**; the
  board never touches compute. **The board never imports head code** — it reads the
  hypothesis label and metric from job **tags** that `scripts/sweep.py` writes at
  submit time (`Hypothesis=`, `Metric=`, `Sweep=`). Served apps run under the
  **JupyterLab** app, not Code Editor (proxy constraint).
- Secrets/credentials never in code or committed. Read from env or the AWS
  credential chain.

## Testing & validation

- A smoke path must always exist per head: `train.py --domain <h> --max-steps 5`
  runs a real forward/backward in seconds on one GPU. Keep it fast.
- Test what you own: the head contract conformance (every head implements
  `base.py`), `data.py` shapes, argument parsing, the `MetricSink` fan-out. Don't
  test the cloud SDK.
- Add a contract-conformance test that every registered head satisfies — this is
  the guard rail that keeps a new head from special-casing the spine.
- Prefer **SageMaker local mode** for container validation over speculative cloud
  submission.

## Verify-first (no stale names)

Before writing code against the SageMaker SDK / DLC URIs / per-head libraries,
**confirm current names/paths against live docs** — the "SageMaker AI" rebrand
moved labels, and the ML libraries move fast. Capture findings (with date) in the
relevant GitHub issue. See `SPEC.md §7`.

---

## Versioning — SemVer 2.0.0

Follow [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html) strictly.

- `MAJOR.MINOR.PATCH`.
  - **MAJOR** — incompatible change to the demo's public surface: the head contract
    in `base.py`, `train.py` CLI flags, script entry points, layout contracts.
  - **MINOR** — backward-compatible capability: a new head, a new sweep axis, a new
    viewer panel. (Adding a head is a MINOR bump.)
  - **PATCH** — backward-compatible fixes.
- Pre-1.0.0 (`0.y.z`): the shape is still settling; minor may break. Say so in the
  changelog.
- The head contract is the most load-bearing public surface — changing `base.py` in
  a breaking way is a MAJOR event even pre-1.0; call it out loudly.
- Tag releases `vMAJOR.MINOR.PATCH`. Git tag and `CHANGELOG.md` must agree.

## Changelog — Keep a Changelog 1.1.0

Maintain `CHANGELOG.md` per [Keep a Changelog 1.1.0](https://keepachangelog.com/en/1.1.0/).

- Newest first; an `## [Unreleased]` section accrues between releases.
- Group under **Added, Changed, Deprecated, Removed, Fixed, Security.**
- Entries explain *impact*, not raw commit messages. New heads land under **Added**.
- On release: rename `[Unreleased]` to `[X.Y.Z] - YYYY-MM-DD`, open a fresh
  `[Unreleased]`, ensure version matches the SemVer bump and the git tag.
- Link versions to compare URLs at the bottom.

## Commits

- Conventional Commits (`feat:`, `fix:`, `docs:`, `refactor:`, `test:`, `chore:`,
  `build:`, `ci:`). Type drives the SemVer reasoning above; a new head is `feat:`.
- Reference the GitHub issue (`Refs #N` / `Closes #N`).
- Small, reviewable commits — one logical change each.

---

## Project tracking — GitHub, not files

All planning and status lives in GitHub. Do not duplicate it in the repo.

- **Issues** — one per unit of work. The seven stages (`SPEC.md §4`) and the four
  heads (`SPEC.md §3`) map to issues.
- **Milestones** — group toward a releasable increment, e.g.
  `v0.1.0 spine + molecular (local→single job)`,
  `v0.2.0 sweep + spot + board`,
  `v0.3.0 viewers (marimo + streamlit)`,
  `v0.4.0 weather head`, `v0.5.0 genomics head`, `v0.6.0 llm head`.
- **Labels** — at minimum: `stage:author`, `stage:smoke`, `stage:job`,
  `stage:sweep`, `stage:spot`, `stage:compare`, `stage:viewer`; plus
  `head:molecular`, `head:weather`, `head:genomics`, `head:llm`;
  plus `area:spine`, `area:board`, `area:contract`, `lang:go`, `lang:python`,
  `verify-first`, `bug`, `enhancement`, `docs`, `blocked`.
- **Project board** — the single source of truth for what's in flight.

When in doubt: code and conventions go in the repo; everything about *what to do
next* goes in GitHub.
