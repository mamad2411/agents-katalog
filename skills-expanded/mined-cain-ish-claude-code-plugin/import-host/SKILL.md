---
name: import-host
description: Detect existing AI-context files on the host (CLAUDE.md, AGENTS.md, .cursorrules, .windsurfrules, .continuerules, .aider.conf.yml, instructions.md) at $HOME and the current repo, and propose USER.md preferences plus PROJECT.md content. Prompts to confirm each chunk. Idempotent.
user-invocable: true
disable-model-invocation: true
allowed-tools: Read Write Edit Bash(test *) Bash(ls *) Bash(cat *) Bash(wc *) Bash(date *) Bash(grep *) Bash(find *) Bash(basename *) Bash(tr *) Bash(git rev-parse:*) mcp__plugin_second-brain_knowledge-base__pin_to_user mcp__plugin_second-brain_knowledge-base__pin_to_project
---

# Import host

Bootstrap the v1.0 hot tier (`USER.md` + `PROJECT.md`) from AI-context files you've already written for Claude Code, Aider, Cursor, Continue, Windsurf, or AGENTS.md (the OpenCode/agent-rules standard). The skill is read-only against your host files and explicit-confirm against second-brain writes.

## Steps

### 1. Detect candidates

Walk known locations and report what exists. Search at two scopes: home (`$HOME`) and the current repo root (the directory containing `.git`, walking up from cwd).

```bash
declare -a CANDIDATES=(
  "$HOME/CLAUDE.md"
  "$HOME/AGENTS.md"
  "$HOME/.cursorrules"
  "$HOME/.windsurfrules"
  "$HOME/.continuerules"
  "$HOME/.aider.conf.yml"
  "$HOME/.claude/CLAUDE.md"
  "$HOME/.claude/instructions.md"
)

GIT_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -n "$GIT_ROOT" ]; then
  for f in CLAUDE.md AGENTS.md .cursorrules .windsurfrules .continuerules .aider.conf.yml instructions.md; do
    [ -f "$GIT_ROOT/$f" ] && CANDIDATES+=("$GIT_ROOT/$f")
  done
fi

for c in "${CANDIDATES[@]}"; do
  if [ -f "$c" ]; then
    LINES=$(wc -l < "$c" | tr -d ' ')
    printf '  %s (%s lines)\n' "$c" "$LINES"
  fi
done
```

Report the matched list to the user. If nothing matches, exit with: "No host AI-context files found — run `/second-brain:setup` to scaffold from scratch."

### 2. Categorize each file

For each detected file, read the first ~60 lines. Decide whether the content is primarily:

- **User-level preferences** — global how-to-behave rules (tone, style, "never do X", language preferences, formatting defaults). Targets `USER.md`.
- **Project-level facts** — repo-specific Goal, State, Conventions, decisions, blockers. Targets the active repo's `PROJECT.md`.
- **Mixed** — recommend splitting; propose a USER.md slice and a PROJECT.md slice.

Files at `$HOME` are usually user-level. Files at `$GIT_ROOT` are usually project-level. The first ~60-line read confirms.

Report the categorisation to the user before any writes.

### 3. Propose USER.md content

For files (or slices) categorized as user-level:

1. Distill the content into ≤15 short bullet lines of cross-project preferences. Drop verbose prose, repo-specific facts, and anything stale.
2. Show the proposed USER.md content as a single block.
3. Prompt: `Append these <N> preferences to USER.md? (Y / N / edit)`
4. On `Y`: for each preference, call `pin_to_user(text: "<preference>")`. The MCP tool caps at 15 dated `- [YYYY-MM-DD] …` PIN LINES only (never the whole file — hand-written About/Intent sections don't count against it) and adds the new entry; on overflow it returns `{ok: false}` and the skill must surface the rejection.
5. On `edit`: let the user revise the block, then re-prompt.
6. On `N`: skip.

If `~/.second-brain/USER.md` does not exist yet, the first `pin_to_user` call will create it with the standard header.

### 4. Propose PROJECT.md content

For files (or slices) categorized as project-level, resolve the active project slug:

```bash
# Monorepo-aware detection (same idiom as the setup skill): source lib.sh for sb_detect_project.
. "${CLAUDE_PLUGIN_ROOT}/scripts/lib.sh"
_det=$(sb_detect_project "$(git rev-parse --show-toplevel 2>/dev/null || pwd)")
IFS=$'\t' read -ra _det_fields <<< "$_det"
SLUG="${_det_fields[0]:-}"
```

If `~/.second-brain/projects/$SLUG/PROJECT.md` does not exist, instruct the user to run `/second-brain:setup` first — this skill fills in content but does not scaffold the file.

If it exists, propose section-by-section:

- **Goal** (≤3 lines): show your distilled draft and prompt `Replace existing Goal? (Y/N/edit)`. Apply via `Edit` tool — replace the body of the `## Goal` section only.
- **Conventions** (≤5 lines): same flow, target `## Conventions`.
- **Recent decisions** (≤3 entries): for each, prompt and call `pin_to_project(text: "<decision text>", slug: "$SLUG", section: "decisions")` on accept. The tool prefixes `- [decision] ` automatically.
- **Open blockers** (≤15 lines): for each, prompt and call `pin_to_project(text: "<blocker text>", slug: "$SLUG", section: "blockers")` on accept. The tool prefixes `- [active] ` automatically.

Skip `## State` and `## Cross-references` — those are runtime-maintained, not import targets.

### 5. Skip duplicates

Before each `pin_to_user` or `pin_to_project` proposal, grep the destination file for the candidate text. If a fuzzy match exists, prompt: `<text> already present (or close); skip / replace?` and act accordingly.

### 6. Done

Report a one-block summary:

```
# Import summary
- USER.md: 4 preferences appended (skipped 1 duplicate)
- PROJECT.md (my-repo):
  - Goal updated
  - Conventions updated
  - 2 [active] blockers added
  - 1 [decision] decision added
- Source files left untouched.
```

Suggest follow-ups: `/second-brain:lint` (catch any orphan or dead references introduced by the import) and `/second-brain:status` (sanity-check hot-tier byte counts stay under cap).

## Notes

- This is a **bootstrap** skill — it is most useful right after `/second-brain:setup`. Re-running it later is safe but will mostly hit the duplicate-skip path.
- The skill never deletes or modifies your host files (`~/CLAUDE.md`, `.cursorrules`, etc.). They stay where they are.
- All writes go through the v1.0 MCP tools (`pin_to_user`, `pin_to_project`) or direct `Edit`s on `PROJECT.md`. There is no critic-gate, no persona/quality-rules file, no `archive_to_wiki` invocation here — graduating resolved entries (`archive_to_wiki`) stays an explicit user request, and session-insight capture is automatic (Stop-hook extraction + dream consolidation).
- Hot-tier cap reminder: `pin_to_user` caps at 15 dated PIN lines, NOT a 15-line whole-file cap on USER.md — hand-written content outside the `## Pinned` section doesn't count against it. The byte-size contract (USER.md ~3200 B target; emit caps 6000/3000; 8000 B SessionStart budget) lives in the `setup` skill. If a proposed import would push over, distill harder before re-trying.
