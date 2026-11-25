---
name: update-env
description: >
  Update installed Claude Code plugins (user/global, project, or local scope) and
  upgrade package dependencies in the project's virtual environment to newer versions.
  Use when the user says "update my plugins", "update claude plugins", "upgrade
  packages", "check for outdated packages", "update dependencies", "bump versions",
  or "/update-env". Does not set up or restore environments — use /env-check for that.
argument-hint: [plugins|deps|all] [--scope user|project|local]
user-invocable: true
disable-model-invocation: false
allowed-tools: Read, Grep, Glob, Bash, Write, Edit
---

# Skill: update-env

Update installed Claude Code plugins and/or upgrade package dependencies to newer
versions. Language is detected automatically. Run `/env-check` first if the environment
does not exist yet.

---

## Phase 0: Detect intent

Parse `$ARGUMENTS`:

- Contains "plugins" (and not "deps"/"packages"/"dependencies") → run **Phase A only**
- Contains "deps", "packages", or "dependencies" (and not "plugins") → run **Phase B only**
- Neither, or "all" → run **Phase A then Phase B**

If `--scope <value>` is present in `$ARGUMENTS`, record `<value>` (user, project, or
local) for use in Phase A.

---

## Phase A: Claude plugin updates

*Skip this phase if intent is `deps` only.*

### Step 1 — List installed plugins

```bash
claude plugin list --json
```

Parse the output and display a summary table:

| Plugin | Version | Scope | Marketplace |
|--------|---------|-------|-------------|

Group by scope: **user** (global), **project**, **local**.

If `--scope` was provided, show only the plugins matching that scope and note that
other scopes are being skipped.

If no plugins are installed: report "No plugins installed" and skip to Phase B (or stop
if deps-only was not requested).

### Step 2 — Choose what to update

Ask:

> "Which plugins would you like to update?
>
> 1. All plugins (shown above)
> 2. All plugins in a specific scope
> 3. Choose specific plugins by name
> 4. Skip — no plugin updates"

Wait for the user's choice before continuing.

### Step 3 — Run updates

For each selected plugin, run:

```bash
claude plugin update <plugin-name>
```

If `--scope` was provided, add `-s <scope>` to each update command:

```bash
claude plugin update <plugin-name> -s <scope>
```

Surface any failures immediately. If a command is permission-blocked:

> "The following command needs to be run manually:
>
> ```
> <exact command>
> ```
>
> Please run it in your terminal, then reply **done** to continue."

### Step 4 — Confirm changes

After all updates complete, run:

```bash
claude plugin list --json
```

Compare versions with Step 1. Report which plugins were updated and their new versions.
If nothing changed (already up to date), say so clearly.

---

## Phase B: Package dependency upgrades

*Skip this phase if intent is `plugins` only.*

### Step 1 — Detect language

If `$ARGUMENTS` names a language explicitly, use it. Otherwise detect from signal files:

| Signal files | Language | Reference |
|---|---|---|
| `pyproject.toml`, `setup.py`, `requirements.txt`, `Pipfile` | Python | `${CLAUDE_PLUGIN_ROOT}/../references/python.md` |
| `package.json` (no `tsconfig.json`) | JavaScript | `${CLAUDE_PLUGIN_ROOT}/../references/javascript.md` |
| `package.json` + `tsconfig.json` | TypeScript | `${CLAUDE_PLUGIN_ROOT}/../references/typescript.md` |
| `Cargo.toml` | Rust | `${CLAUDE_PLUGIN_ROOT}/../references/rust.md` |
| `go.mod` | Go | `${CLAUDE_PLUGIN_ROOT}/../references/go.md` |
| `DESCRIPTION`, `renv.lock`, `.Rprofile` | R | `${CLAUDE_PLUGIN_ROOT}/../references/r.md` |

**Load the reference file before taking any language-specific action.**

If multiple signal files match different languages, list what was found and ask the user
which language to proceed with.

### Step 2 — Confirm environment exists

Check for the environment indicator from the loaded reference (`.venv/`, `node_modules/`,
`target/` or `Cargo.lock`, `go.sum`, `renv/`).

If not found:

> "No environment found for this project. Run `/env-check` first to set one up, then
> return here to upgrade packages."

Stop.

### Step 3 — List outdated packages

Run the appropriate command for the detected language and toolchain:

| Language / Tool | Outdated command |
|---|---|
| Python + uv | `uv pip list --outdated` |
| Python + pip | `pip list --outdated` |
| JavaScript + npm | `npm outdated` |
| JavaScript + yarn | `yarn outdated` |
| JavaScript + pnpm | `pnpm outdated` |
| TypeScript (same as JS) | same as the detected package manager |
| Rust | `cargo outdated` (see note below) |
| Go | `go list -u -m all` |
| R | `Rscript -e "renv::update(check = TRUE)"` |

**Rust note:** `cargo outdated` requires the `cargo-outdated` crate. Check first:

```bash
cargo outdated --version
```

If not installed:

> "`cargo outdated` is not installed. To check for outdated crates, run:
>
> ```
> cargo install cargo-outdated
> ```
>
> Install it, then reply **done** to continue — or skip package updates."

Wait for the user's response. Do not proceed with outdated-checking until the tool is
confirmed available or the user skips.

**For Python**, detect the active tool before running the outdated command:

```bash
which uv
```

- `uv` found → use `uv pip list --outdated`
- Not found → use `pip list --outdated` (run from inside `.venv/`)

**For JavaScript/TypeScript**, detect the package manager from the lockfile:

| Lockfile | Tool |
|---|---|
| `pnpm-lock.yaml` | pnpm |
| `yarn.lock` | yarn |
| `package-lock.json` | npm |
| None | npm |

If nothing is outdated: report "All packages are up to date" and skip to Phase C.

### Step 4 — Choose upgrade strategy

Display the outdated package list, then ask:

> "How would you like to upgrade?
>
> 1. **Conservative** — patch and minor updates only (respects semver ranges)
> 2. **Full** — upgrade all packages to their latest published versions
> 3. **Selective** — I'll list packages and you choose which to upgrade
> 4. Skip — no package upgrades"

Wait for the user's choice before continuing.

### Step 5 — Run upgrades

#### Python (uv)

```bash
# Conservative (upgrade within pinned ranges in uv.lock)
uv lock --upgrade
uv sync

# Full (upgrade all to latest)
uv lock --upgrade-package <pkg>   # repeat per package, or:
uv pip install --upgrade <pkg1> <pkg2> ...

# Selective
uv pip install --upgrade <package-name>
```

If the project has a `uv.lock`, prefer `uv lock --upgrade` (conservative) or
`uv lock --upgrade-package <pkg>` (selective) over direct `uv pip install --upgrade`.

#### Python (pip)

```bash
# Conservative — re-install from spec with latest compatible versions
pip install -e ".[dev]"           # if pyproject.toml present
pip install -r requirements.txt   # if requirements file present

# Full — upgrade all outdated packages
pip list --outdated --format=freeze | grep -v '^\-e' | cut -d = -f 1 | xargs pip install -U

# Selective
pip install --upgrade <package-name>
```

**Warning:** Full pip upgrade can introduce incompatibilities. Ask the user to confirm
before running the bulk upgrade command.

#### JavaScript / TypeScript

```bash
# Conservative (respects semver ranges in package.json)
npm update          # or: yarn upgrade / pnpm update

# Full (ignores semver ranges, upgrades to absolute latest)
npx npm-check-updates -u && npm install    # npm
yarn upgrade --latest                       # yarn
pnpm update --latest                        # pnpm

# Selective
npm install <pkg>@latest      # or yarn add <pkg>@latest / pnpm add <pkg>@latest
```

Note: `npm-check-updates` may not be installed. If `npx npm-check-updates` fails,
surface the install command:

```bash
npm install -g npm-check-updates
```

#### Rust

```bash
# Conservative (update Cargo.lock within existing semver constraints in Cargo.toml)
cargo update

# Selective (update one crate's lock entry)
cargo update -p <crate-name>

# Full (bump dependency versions in Cargo.toml) — not automated
```

**Full Rust upgrades** require editing `Cargo.toml` directly (changing version
constraints). Do not modify `Cargo.toml` automatically. If the user wants full
upgrades, show the outdated versions from `cargo outdated` and ask them to update
`Cargo.toml` manually, then run `cargo update` to refresh `Cargo.lock`.

#### Go

```bash
# Upgrade all direct dependencies to their latest minor/patch versions
go get -u ./...

# Upgrade a specific module
go get <module-path>@latest

# Tidy after upgrading
go mod tidy
```

If the project uses a `vendor/` directory, also run:

```bash
go mod vendor
```

#### R

```bash
# Check for updates and upgrade (interactive prompt per package)
Rscript -e "renv::update()"

# Snapshot the new state into renv.lock
Rscript -e "renv::snapshot()"
```

`renv::update()` will prompt for each package by default. If the user wants
non-interactive upgrade, they can run it themselves — surface the command and wait for
"done".

---

### Step 6 — Verify

Run the language-specific verify command from the loaded reference file to confirm the
environment is still functional after upgrades. For compiled languages (Rust, Go), a
successful build confirms no breaking changes slipped through.

---

## Phase C: Document in CLAUDE.md

After any successful upgrades (plugins or packages), find the `## Active Environment`
section in `CLAUDE.md` (if present) and update the `Last setup` line to today's date:

```
- Last setup: <YYYY-MM-DD>
```

Rules:

- **No `## Active Environment` section** → do not create one here; suggest running
  `/env-check` to set up the documented baseline.
- **Section found** → update `Last setup` only. Do not modify other fields unless the
  interpreter version actually changed (e.g., after a Go toolchain upgrade).
- Use the Edit tool; do not rewrite the entire file.

---

## Constraints

- Never run package upgrades without first showing what is outdated and getting explicit
  user confirmation of the upgrade strategy.
- Never modify project manifests (`pyproject.toml`, `package.json`, `Cargo.toml`,
  `go.mod`) automatically. Only lockfiles and the dependency installation state may
  change.
- Always load the language reference file before taking any language-specific action.
  Do not invent language-specific commands from memory.
- For `cargo outdated`: if not installed, surface the install command and wait — do
  not silently skip or proceed to upgrades without it.
- For full pip upgrades: require explicit user confirmation before running the bulk
  `xargs pip install -U` command — it can break constraints set by other packages.
- If a Bash command is blocked by Claude Code's permission system, surface the exact
  command and wait for "done" — do not retry or silently skip.
- If Phase B detects no environment (`env-check` has not been run), stop and direct
  the user to `/env-check` before attempting upgrades.
