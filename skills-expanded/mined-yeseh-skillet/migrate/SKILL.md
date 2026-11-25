---
name: migrate
description: "Migrate plain markdown SKILL.md files to a managed skillet workspace with typed refs and extracted fragments."
---

# migrate

Use this skill when converting a project's plain-markdown `SKILL.md` files into a fully managed `skillet` workspace with `.pan` sources, typed references, and shared fragments.

## Phase 1 — Adopt existing skills

Check whether the workspace is already initialised before doing anything else.

1. Look for `skillet.toml` in the project root.
2. If it is absent, run:
   ```
   skillet init --adopt
   ```
   `--adopt` copies every `skills/<name>/SKILL.md` it finds into
   `src/skills/<name>/<name>.pan` so the existing compiled outputs become
   editable sources without losing the original files.
3. Confirm the source files were created:
   ```
   ls src/skills/
   ```
4. If `skillet.toml` already exists but `.pan` source files are missing, run
   adoption manually: copy each `skills/<name>/SKILL.md` to
   `src/skills/<name>/<name>.pan` then add the required YAML frontmatter:
   ```markdown
   ---
   name: <name>
   description: "One-line description."
   ---
   ```
---

## Phase 2 — Resolve untyped references

Run lint in pedantic mode to surface all backtick spans that look like refs:

```
skillet lint --pedantic
```

For each `untyped-backtick` diagnostic, rewrite the backtick to the suggested
typed ref using the table below.  The lint output already tells you which type
to use (e.g. `looks like a path — consider` `ref::...`):

| Type | Example | Typed ref |
|---|---|---|
| `ref`         | `./scripts/deploy.sh`   | `ref::./scripts/deploy.sh`  |
| `cmd`         | `kubectl apply -f …`    | `cmd::kubectl`              |
| `skill`       | `diagnose`              | `skill::diagnose`           |
| `url`         | `https://example.com`   | `url::https://example.com`  |
| `var`         | repeated project-specific string | extract to [vars] and use `var::name` |
| `env`         | environment variable name     | `env::VAR_NAME`             |

After each batch of rewrites, re-run lint to confirm the warning count drops:

```
skillet lint --pedantic
```

Also scan for standard markdown links whose target is a local path:

```
[text](./path/to/file.md)
```

Where the link target should be treated as a file reference, inline it as a
typed ref: `ref::./path/to/file.md`.

---

## Phase 3 — Fragment extraction

Scan all `.pan` files for duplicate or near-duplicate passages that appear in
two or more skills.  Common candidates:

- Repeated safety / disclaimer notes
- Shared prerequisites or environment-setup sections
- Copy-pasted command-reference tables
- Boilerplate headers that vary only in the skill name

**Detection approach**

1. Open each `.pan` file and read the body (below the frontmatter).
2. Break each body into logical paragraphs or sections.
3. Compare paragraphs across files — flag any passage of ≥ 3 lines that
   appears verbatim or near-verbatim in two or more skills.
4. Also check `skillet lint` output for `duplication` diagnostics, which
   surface text that exceeds the similarity threshold automatically.

**Extraction steps for each candidate**

1. Create the fragment file:
   ```
   src/skills/_fragments/<name>.fragment.pan
   ```
   Paste the shared passage as its entire content (no frontmatter required).
2. Replace every occurrence in the `.pan` files with a fragment include on its
   own line: wrap the fragment name in the fragment delimiters — an opening `{`
   immediately followed by `>`, then the name, then the closing pair `<}`.
   Includes are block-level and cannot be nested.
3. Rebuild and verify:
   ```
   skillet build
   skillet lint
   ```
   Confirm no `unused-fragment` warning fires (every fragment is referenced
   at least once) and that the compiled `SKILL.md` output is unchanged.

---

## Phase 4 — Configure skillet.toml

Open `skillet.toml` and tune it for the project.  The default file written by
`skillet init` is a starting point; adjust each section as needed.

**[workspace]** — workspace-wide settings. The only path it owns is the
global fragments directory; source and output paths live per-plugin:

```toml
[workspace]
fragments_dir = "src/skills/_fragments"
```

**[plugin.<name>]** — each plugin declares its own source/output pair.
`skillet init` writes a single `default` plugin; add or rename plugins only if
the project ships more than one source/output tree:

```toml
[plugin.default]
src_dir = "src/skills"
out_dir = "skills"
version = "0.1.0"
```

**[vars]** — promote any project-specific string that appears in multiple
skills to a named variable, then reference it with `var::name`:

```toml
[vars]
project_name = "my-project"
repo_url     = "https://github.com/org/repo"
```

**[env]** — declare environment variables that skills reference, with
sensible defaults so builds work locally without every variable set:

```toml
[env]
CI        = { default = "false" }
TEAM_NAME = { default = "engineering" }
```

**[lint]** — token budgets and rule control.  Add rule IDs to `disable` only
when a rule genuinely does not apply to the project:

```toml
[lint]
max_activation_tokens = 4000
max_discovery_tokens  = 100
max_fragment_tokens   = 500
disable               = []
```

**`allowed_commands`** — a top-level array (not under [lint]) listing every
shell command referenced via `cmd::…` that should be treated as available
regardless of whether it is found on `PATH`:

```toml
allowed_commands = ["docker", "kubectl", "make"]
```

**[build]** — enable URL verification once you are confident all links are
reachable; leave it off during the initial migration pass to avoid noise:

```toml
[build]
tokenizer   = "cl100k_base"
verify_urls = false
```

---

## Phase 5 — Verify and finalize

Run the full pipeline to confirm the workspace is clean:

```
skillet build          # compile all .pan sources to SKILL.md
skillet check          # confirm outputs are fresh
skillet lint --strict  # promote warnings to errors; fix any that remain
skillet budget         # review token costs; split oversized skills if needed
```

Commit both the source files and the compiled outputs together:

```
git add src/skills/ skills/ skillet.toml skillet.lock
git commit -m "Migrate skills to skillet workspace"
```
