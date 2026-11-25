---
name: chezmoi-creator
description: Create, migrate, review, and debug chezmoi source states, templates, scripts, and config files. Use this skill when managing dotfiles with chezmoi, mapping target files to source-state names, writing run_once/run_onchange scripts, handling special files like .chezmoiignore or .chezmoiexternal, or building cross-platform home-directory setups for Linux, macOS, Windows, and Codespaces.
---

# Chezmoi Creator

This skill is an operating guide for creating and maintaining chezmoi-managed dotfile repositories.

Default assumption: the user wants a working source state, not a broad tutorial. Prefer producing or modifying concrete chezmoi files over explaining the tool abstractly.

## Mandatory planning

Before creating or changing chezmoi-managed files, make a concise plan that covers:

- target platforms: Linux, macOS, Windows, Codespaces, or a subset
- target files and directories to manage
- whether each target should be a regular file, template, symlink, script, create file, modify file, or external
- whether secrets, encryption, or machine-specific data are involved
- whether hooks are needed, or whether a normal chezmoi script is sufficient

If secrets or sensitive data are involved, load [references/security-practices.md](references/security-practices.md) before designing the source state.

## Installation and local-project mode

When the user asks to install chezmoi itself, prefer the official install script.

### Install to `/usr/local/bin`

Use one of these commands:

```sh
sh -c "$(curl -fsLS get.chezmoi.io)" -- -b /usr/local/bin
```

If elevated privileges are required:

```sh
sudo sh -c "$(curl -fsLS get.chezmoi.io)" -- -b /usr/local/bin
```

### Use the current project directory as the source directory

If the user wants a repo-local setup instead of chezmoi's default source directory, prefer isolating the source state in a `src/` subdirectory so the repo root can also contain README files, CI configuration, helper scripts, and other non-dotfile project files.

Example `chezmoi.yaml` in the project root:

```yaml
sourceDir: ./src
workingTree: .
```

Recommended layout:

- project root: `README.md`, CI files, `install.sh`, `chezmoi.yaml`
- `src/`: the actual chezmoi source state

Create the directory before first use:

```sh
mkdir -p src
```

Note: in this repo-local layout, `.chezmoiignore` patterns apply to *target* paths (for example `~/.config/chezmoi/chezmoi.yaml`), not to repository files like `./chezmoi.yaml` in the project root. The repo-local `chezmoi.yaml` shown above is not part of the source state and does not need to be ignored.




Then run commands from the project root with the explicit config path, for example:

```sh
mkdir -p ./src
chezmoi --config ./chezmoi.yaml add ~/.zshrc
chezmoi --config ./chezmoi.yaml add --template ~/.gitconfig
chezmoi --config ./chezmoi.yaml source-path ~/.zshrc
chezmoi --config ./chezmoi.yaml diff
chezmoi --config ./chezmoi.yaml apply
```

This keeps the source state under `./src` and avoids relying on the default `~/.local/share/chezmoi` location.

For Codespaces or other bootstrap scripts, follow the `chezmoi/dotfiles` example in one respect: always pass an explicit source path during bootstrap instead of assuming chezmoi defaults. In this skill, prefer that explicitness together with a `src/` source root.

## Core rules

1. Model the result as source state first. Work backward from the target file in the home directory to the correct chezmoi source path and attributes.
2. Respect attribute order strictly. Prefix order is semantic, not cosmetic.
3. Prefer templates only when the file truly varies by machine, OS, host, user, or secret source.
4. Prefer scripts for side effects and installers. Prefer templates for file content.
5. Use hooks sparingly. Hooks run even with dry-run and should stay fast and idempotent.
6. Reuse bundled assets when they match the request closely enough. Adapt them instead of rewriting common bootstrap files from scratch.
7. Keep platform-specific behavior explicit. Do not hide Windows, POSIX, or Codespaces branches in a confusing template unless that complexity is justified.
8. Prefer `src/` as the repo-local `sourceDir` when the repository also contains CI, documentation, or helper files.
9. For any design involving secrets or sensitive information, consult [references/security-practices.md](references/security-practices.md) and choose explicitly between password-manager lookup, encryption, and machine-local config.

## Workflow

1. Identify the desired targets and the platforms that need support.
2. If the user is working from a project-local repo, prefer a command pattern based on `chezmoi --config ./chezmoi.yaml ...`.
3. Choose the source-state representation for each target. Load [references/source-state-naming-rules.md](references/source-state-naming-rules.md) when naming is non-trivial.
4. If the repository needs special control files, load [references/special-files-and-directories.md](references/special-files-and-directories.md).
5. If the request involves templating, load:
   - [references/template-data-and-functions.md](references/template-data-and-functions.md)
   - [references/template-directives.md](references/template-directives.md)
6. If the request involves secrets, encrypted files, password managers, tokens, or private keys, load [references/security-practices.md](references/security-practices.md).
7. If the request involves config, interpreters, formats, or hooks, load [references/configuration-formats-and-hooks.md](references/configuration-formats-and-hooks.md).
8. If the request involves command usage or migration workflow, load [references/commands.md](references/commands.md).
9. Prefer the bundled Codespaces bootstrap asset in `assets/codespaces/install.sh` when the user needs a repo bootstrap entrypoint. Do not invent or retain extra asset variants unless the user explicitly asks for them.
10. Prefer command-line creation and mutation of managed files over manual source-state editing when the target already exists.
11. Generate or edit the final chezmoi source files.
12. Sanity-check attribute order, script timing, special file placement, platform assumptions, and any secret-handling decisions.

## Command-first workflow

When the user already has a target file in the home directory, prefer command-line operations in this order:

1. `chezmoi add $TARGET` to import an existing file.
2. `chezmoi add --template $TARGET` if the file should immediately become a template.
3. `chezmoi chattr +template $TARGET` to convert an already managed file into a template.
4. `chezmoi edit $TARGET` or `chezmoi edit --apply $TARGET` for follow-up edits.
5. `chezmoi source-path $TARGET` to verify where the source-state file landed.

Prefer manual file creation in the source state only when:

- creating special files such as `.chezmoiignore`, `.chezmoiexternal.*`, or `.chezmoiroot`
- creating `run_*` scripts
- creating `.chezmoitemplates` partials
- creating files for targets that do not yet exist locally

## When to use which mechanism

- Use a normal file when content is stable across machines.
- Use `.tmpl` when content depends on `.chezmoi`, config data, prompts, or secret backends.
- Use `create_` when the file should only be created if absent.
- Use `modify_` when mutating an existing unmanaged file is safer than fully owning it.
- Use `run_`, `run_once_`, and `run_onchange_` scripts for imperative setup.
- Use `before_` scripts only when setup must happen before targets are updated.
- Use `after_` scripts when depending on files, externals, or directories that are applied during the update phase.
- Use `.chezmoiexternal.*` for downloaded archives, files, or git repositories.
- Use hooks only for command lifecycle integration that should happen outside the normal source-state application model.

## Best practices

These are the distilled practices from the user guide and should shape default behavior.

### Daily workflow

- Prefer `chezmoi status` and `chezmoi diff` before `chezmoi apply` when changing anything non-trivial.
- Use `chezmoi update` as the normal pull-and-apply workflow across machines.
- Use `chezmoi edit --apply` for quick single-file edits and `chezmoi edit --watch` only when the editor workflow benefits from it.

### Templates and machine differences

- Put machine-specific values in config data instead of duplicating whole files unnecessarily.
- Prefer `chezmoi add --template` when onboarding files that vary by OS, hostname, user identity, or secret backend.
- Use `.chezmoitemplates` to share common fragments across multiple target paths.
- Use `.chezmoiignore` for coarse machine-specific inclusion or exclusion of files and directories.
- If a template may intentionally render nothing on some machines, remember that an empty rendered file is removed unless the target uses the `empty_` attribute.

### Secrets and private data

- Prefer password-manager functions, encrypted files, or machine-local config over committing plaintext secrets.
- Prefer password managers for tokens, passwords, and small structured secrets; prefer encryption for whole secret files.
- Treat private repos as optional, not as a substitute for secret hygiene.
- If storing sensitive values in a local config file, ensure restrictive permissions.
- Store local references to secret backends more readily than local secret values themselves.

### Scripts and side effects

- Use scripts sparingly. They are imperative escape hatches and should remain idempotent.
- Prefer `run_onchange_` for package installation or one-way setup that should rerun only when the script changes.
- Prefer `run_once_` for bootstrap actions whose exact rendered content defines whether they need to rerun.
- Do not rely on `run_before_` scripts to consume externals fetched later in the same apply.

### Partial-file and externally modified config management

- Use `modify_` when only part of a file should be managed and full ownership is unsafe.
- Use full templates when regenerating the whole file is simpler and safer than patching fragments.
- For application-managed configs that constantly drift, consider symlinking back to the source state or using a `modify_` flow instead of fighting repeated rewrites.

### Externals and imported assets

- Use `.chezmoiexternal.*` for third-party archives, plugin trees, or remote single files that should be refreshed declaratively.
- Set `refreshPeriod` only for moving targets such as branch snapshots.
- Avoid large externals because chezmoi validates them during diff, apply, and verify.

### Containers, Codespaces, and automation

- Keep init-time config generation non-interactive in unattended environments such as Codespaces and containers.
- In Codespaces-like environments, explicitly set `sourceDir` when the repo is already cloned into a non-default location.
- Prefer generated or checked-in install scripts when bootstrap must work in a fresh ephemeral environment.

### Debugging and inspection

- Use `chezmoi data` to inspect available template data.
- Use `chezmoi execute-template` to test template fragments before editing larger files.
- Use `chezmoi doctor` first when behavior looks environment-specific or interpreter-specific.

## Assets

Use this bundled asset set as the single starting point when the user needs a Codespaces-friendly chezmoi repository that follows the recommended `src/` layout:

- Repository bootstrap: [./assets/codespaces/install.sh](./assets/codespaces/install.sh)
- Init-time config template: [./assets/codespaces/src/.chezmoi.yaml.tmpl](./assets/codespaces/src/.chezmoi.yaml.tmpl)

This asset set should stay structurally aligned with the upstream `chezmoi/dotfiles` repository:

- `install.sh` remains at repository root and keeps the upstream install flow
- `.chezmoi.yaml.tmpl` remains the init-time config template, but lives under `src/` because `src/` is the source root

## References

- [references/concepts-and-application-order.md](references/concepts-and-application-order.md)
- [references/commands.md](references/commands.md)
- [references/special-files-and-directories.md](references/special-files-and-directories.md)
- [references/source-state-naming-rules.md](references/source-state-naming-rules.md)
- [references/template-data-and-functions.md](references/template-data-and-functions.md)
- [references/template-directives.md](references/template-directives.md)
- [references/security-practices.md](references/security-practices.md)
- [references/configuration.md](references/configuration.md)
- [references/configuration-formats-and-hooks.md](references/configuration-formats-and-hooks.md)
- [references/platform-patterns.md](references/platform-patterns.md)

## Output expectation

When you finish, the result should be a coherent chezmoi source state with correct naming, clear platform handling, and only the minimum moving parts needed for the user's setup.
