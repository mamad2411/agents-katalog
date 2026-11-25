---
name: follow-tool-usage
description: Define a CLI spec with usage to generate completions/docs/SDKs
argument-hint: "[scope]"
related:
  - report-usage
  - deep-review-codebase
  - follow-best-practice
  - setup-cicd
  - resolve-errors
  - follow-tool-mise
  - follow-tool-fnox
  - follow-tool-packslip
  - research-setup-integrations
---

## Goal

Use a usage spec (KDL) to define a CLI, then generate completions, docs, manpages, and a type-safe SDK

## Scope

Covers installation, the KDL spec, `usage generate` subcommands, integrations, and validation

- Boundary: use usage when you want a spec-driven CLI (a single `usage.kdl` → completions/docs/SDK); if the project already uses a framework-native spec (clap/cobra/commander), generate the integration instead of hand-writing a parser — not the npm package `usage` (the real one is `usage-cli` on crates.io)
- Latest: `usage@6.12.0` (the usage CLI by jdx — usage-rs/usage-go + spec + generators, verified 2026-10-02)

## Execute

### 1. Install

> Goal: have the usage CLI ready

1. Install through mise is recommended: `mise use -g usage` or `mise use usage`
2. Alternatives: `cargo install usage-cli`, `brew install usage`
3. If the project has no mise, do `/follow-tool-mise` first
4. Confirm with `usage --version`

### 2. Define Spec

> Goal: Define the CLI with KDL

1. Create `usage.kdl` or `cli.usage.kdl` in the project
2. Define the metadata: `name`, `bin`, `about`, `version`, `author`, `license`
3. Define `flag`, `arg`, `cmd` with `help`
4. Use `effect` such as `read`, `write`, `destructive` for commands and flags
5. Use `config_file` and `env` to bind config/env/defaults
6. Use `global=#true` for global flags
7. Use `min_usage_version "6.x"` to pin the minimum CLI version the spec requires
8. Use `clause` for repeatable positional groups with scoped flags (usage 6.5+)

### 3. Generate Outputs

> Goal: Produce artifacts from the spec

1. `usage generate completion <shell> <bin> -f usage.kdl` for bash/zsh/fish/pwsh/nushell
2. `usage generate completion-init <shell>` for the shell init script
3. `usage generate markdown` for markdown docs (use `--link-extension .html` when serving as HTML)
4. `usage generate manpage` for manpages
5. `usage generate sdk <language>` for a type-safe SDK
6. `usage generate json` for consumption by a framework
7. `usage generate fig` for Fig completions

### 4. Validate and Scripts

> Goal: Check the spec and use scripts

1. Run `usage lint` to validate the spec
2. Use `usage exec` to execute spec-based scripts
3. Use `usage bash|zsh|fish|powershell <script>` to run shebang scripts with spec-based arg parsing

### 5. Framework Integrations

> Goal: Integrate with the existing CLI frameworks

1. clap (Rust) — see `spec/integrations/clap`
2. cobra, kong, urfave/cli (Go)
3. commander.js, oclif, yargs (Node.js)
4. argparse, typer, click (Python)
5. picocli, JCommander (Java)
6. Clikt (Kotlin)

## Rules

### 1. Spec Conventions

- Use the KDL format
- Use `flag "-f --force"` for short/long flags
- Use `arg "<required>"` for a required positional
- Use `arg "[optional]"` for an optional positional
- Define an `effect` for commands that change state
- Use `global=#true` for global flags
- Use `hide=#true` to hide a command/alias from docs

### 2. Example usage.kdl

```kdl
name "My CLI"
bin "mycli"
about "A sample CLI"
version "1.0.0"

flag "-v --verbose" help="Enable verbose logging" global=#true count=#true
flag "-f --force" help="Skip confirmation" effect="destructive"

arg "<dir>" help="Working directory"

cmd "build" help="Build the project" effect="write" {
  flag "-w --watch" help="Watch for changes"
}

cmd "deploy" help="Deploy to production" effect="destructive" {
  flag "-e --env <env>" help="Target environment"
}
```

### 3. Common Commands

- `usage lint`
- `usage generate completion bash mycli`
- `usage generate markdown`
- `usage generate manpage`
- `usage generate sdk typescript`
- `usage generate json`
- `usage generate completion-init bash`

### 4. Integration Pattern

- Generate the JSON spec with `usage generate json -f usage.kdl`
- Consume the JSON in the CLI framework or build pipeline
- Keep `usage.kdl` as the single source of truth
- Regenerate completions/docs in CI whenever the spec changes

- Use /report-usage if needed
- Use /deep-review-codebase if needed
- Use /follow-best-practice if needed
- Use /setup-cicd if needed
- Use /resolve-errors if needed

## References

- [CLI reference](references/cli.md)

- Use /research-setup-integrations if needed (usage shell completions/framework integrations)


- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- A complete `usage.kdl`
- Able to generate completions for bash/zsh/fish/pwsh/nushell
- Able to generate markdown docs/manpages
- Able to generate a type-safe SDK for multiple languages
- Able to integrate with the existing CLI frameworks
- `usage lint` passes
