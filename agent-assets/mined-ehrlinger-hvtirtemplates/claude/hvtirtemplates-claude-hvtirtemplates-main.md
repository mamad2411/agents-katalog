@AGENTS.md

# Claude Code specifics

[`AGENTS.md`](AGENTS.md), imported above, is the operational contract and applies in full. It is written
to be tool neutral so that Codex and other agents read the same rules. Only the Claude Code
affordances live here.

## Before you touch code

`AGENTS.md` says to orient before editing. In Claude Code the way to do that is the codemap:
it lives in the Obsidian vault under `Claude/repomaps/` and is read via the `read-codemap`
skill (`/codemap hvtiRtemplates`). If the codemap looks stale, say so and offer to refresh it
(`/regenerate-codemap`) rather than working from a guess.

If the vault is not available, say so rather than staying quiet about it, then orient from the
repo itself — `NAMESPACE` exports, `R/`, `inst/templates/README.md` and the templates
themselves — before editing.

## Prose

`AGENTS.md` points at the house voice. In Claude Code, apply the `ehrlinger-writing` skill:
it carries the same voice, reader persona and project context, kept in sync from the vault
sources. For documentation *structure* — README shape, roxygen contract, vignette roles — the
`r-package-style` skill is the companion.
