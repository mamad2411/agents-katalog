---
name: besimple-tiny-broccoli
description: "Small-change wrapper: implement → run repo checks → atomic commit → run dedup (BASE_SHA..HEAD)."
---

# Tiny Broccoli: Implement → Check → Commit → Dedup

Use this when the user request is already clear and you can safely implement directly (no plan docs), but you still want:
1) repo checks to be green, and
2) a dedupe pass over the resulting diff.

## Not for

- Big/ambiguous work that needs research, design decisions, or a multi-phase plan.
- “Refactor the whole repo” style requests.

## Preconditions (hard stop if missing)

- Confirm you are in the intended repo: `git rev-parse --show-toplevel`
- Start from a clean working tree: `git status --porcelain` is empty
- Ensure git can create commits (`user.name` / `user.email` configured)
- Ensure required CLIs exist (dedup requires distinct vendors): `codex`, `claude`

## Required subskills

- `dedup`

## Workflow

### 0) Record `BASE_SHA` (required)

Capture the base ref **before any changes** (used later for `dedup`):

```bash
BASE_SHA="$(git rev-parse HEAD)"
```

### 1) Choose the repo check command(s) once (required)

Do a one-time **tooling detection + configuration** so the per-step “build/lint” commands match the target repo.

**Detect languages and entrypoints**
   - **Node/TS**: look for `package.json` in repo root and common subprojects (for example `functions/package.json`).
   - **Python**: look for `pyproject.toml`, `uv.lock`, `poetry.lock`, `requirements.txt`.
**Pick build/lint/typecheck commands (prefer repo-native scripts)**
   - Prefer existing package scripts when present (e.g. `npm run build`, `npm run lint`, `npm test`).
   - Prefer the repo’s configured Python toolchain:
     - If `uv` is clearly in use: use `uv`-based commands.
     - If Poetry is clearly in use: use `poetry run ...`.
     - If neither: use the repo’s documented commands (README/CONTRIBUTING) if available.
   - If multiple options exist or it’s unclear, ask the user **once** for the canonical build/lint/typecheck commands, then reuse them for every step.
**Write down a “Tooling config” block and reuse it for every step**
   - Example format (adapt to the repo):
     - **Root (Node)**: build=`...`, lint=`...`
     - **functions/ (Node)**: build=`...`, lint=`...`
     - **Root (Python)**: build=`...`, typecheck=`...`, lint/format=`...`
   - From now on, *only* run the commands from this block after each step (instead of hard-coded defaults).
**If the repo has no build/lint tooling**
   - Explicitly record “No build/lint configured” and skip build/lint steps (do not invent tooling). Call this out in the final summary.

### 2) Implement the requested change (required)

- Make the smallest correct change that satisfies the request.
- Prefer reusing existing patterns/utilities over creating new ones.
- Keep the change set small and reviewable.

### 3) Run repo checks and fix only what you broke (required)

- Run the commands from your **Tooling config**.
- If checks fail due to changes you introduced, fix and re-run until green.
- If checks fail for clearly pre-existing/unrelated reasons, stop and report:
  - the exact command(s) you ran, and
  - the first actionable error output.

### 4) Commit once checks are green (required)

- `git add -A`
- Make a single atomic commit for the user-requested change:
  - `git commit -m "<imperative summary>"` (example: `Fix flaky upload retry`).
- Do not create empty/no-op commits (`--allow-empty` is prohibited).

### 5) Run `dedup` against `BASE_SHA` (required)

Ensure the working tree is clean, then run the dedupe loop:

```bash
if [ -n "$(git status --porcelain)" ]; then
  echo "Working tree is not clean; commit or stash before running dedup." >&2
  exit 1
fi
```

```bash
resolve_skill_dir() {
  local name="$1"
  local repo_root=""
  repo_root="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"

  local candidates=(
    "$repo_root/.agents/skills/$name"
    "$repo_root/.claude/skills/$name"
    "$HOME/.agents/skills/$name"
    "$HOME/.codex/skills/$name"
    "$HOME/.claude/skills/$name"
  )

  for d in "${candidates[@]}"; do
    if [[ -d "$d" ]]; then
      echo "$d"
      return 0
    fi
  done

  echo "Error: skill '$name' not found in repo-scoped or user-scoped skill dirs." >&2
  return 1
}

DEDUP_SKILL_DIR="$(resolve_skill_dir dedup)"
python3 "$DEDUP_SKILL_DIR/scripts/run_dedup_loop.py" "${BASE_SHA}"
```

If `dedup` creates additional commits, re-run the **Tooling config** checks once at the end and fix only issues introduced by dedupe changes.
Do not interrupt/restart the dedup loop if it looks quiet; the loop script owns timeouts and retries.

## Guardrails

- Keep changes tightly scoped to the user request + required dedupe.
- Avoid drive-by refactors, renames, formatting-only churn, or dependency upgrades unless required.
- End state must be: checks green (or explicitly “no checks configured”), clean working tree, and at least one meaningful commit.
