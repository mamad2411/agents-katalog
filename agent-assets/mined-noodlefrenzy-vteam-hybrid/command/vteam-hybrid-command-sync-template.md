<!-- agent-notes: { ctx: "reapply vteam-hybrid template evolutions to in-flight repo", deps: [CLAUDE.md], state: active, last: "grace@2026-02-15" } -->
Reapply vteam-hybrid template evolutions to this repo.

**Template source:** `$ARGUMENTS`

If no path is provided, ask the user: "Where is your vteam-hybrid template repo? (e.g., `/home/user/dev/vteam-hybrid` or a GitHub URL)"

This command syncs template improvements (agent definitions, commands, doc templates, CLAUDE.md sections) from the vteam-hybrid template into an in-flight project. It is designed to be **non-destructive** — it will not overwrite project-specific content.

---

## What gets synced (safe to overwrite)

These files are template-standard and don't contain project-specific content:

### 1. Agent definitions
Copy all `.claude/agents/*.md` from the template to this repo:
```
cp <template>/.claude/agents/*.md .claude/agents/
```
These define agent personas, responsibilities, and tooling. They don't contain project-specific state.

### 2. Command definitions
Copy all `.claude/commands/*.md` from the template to this repo:
```
cp <template>/.claude/commands/*.md .claude/commands/
```
**Exception:** If this repo has project-specific command modifications (e.g., a customized `tdd.md` with project-specific test patterns), note them to the user before overwriting. Check `git diff` after copy to verify.

### 3. Doc templates (new files only)
Create any doc directories and template files that don't exist yet. **Do not overwrite existing docs** — they may contain project data.

Check for and create if missing:
- `docs/scaffolds/threat-model.md` → `docs/security/threat-model.md` (copy from template, mkdir -p)
- `docs/scaffolds/performance-budget.md` → `docs/performance-budget.md` (copy from template)
- `docs/scaffolds/test-strategy.md` → `docs/test-strategy.md` (copy from template)
- `docs/scaffolds/tech-debt.md` → `docs/tech-debt.md` (copy from template)
- `docs/scaffolds/config-manifest.md` → `docs/config-manifest.md` (copy from template)
- `docs/scaffolds/runbook-template.md` → `docs/runbooks/template.md` (copy from template, mkdir -p)
- `docs/scaffolds/sbom.md` → `docs/sbom/sbom.md` (copy from template, mkdir -p)
- `docs/scaffolds/dependency-decisions.md` → `docs/sbom/dependency-decisions.md` (copy from template, mkdir -p)
- `CHANGELOG.md` (copy from template)

For each: `mkdir -p <dir>` then copy only if the file doesn't already exist.

---

## What needs manual merging (CLAUDE.md)

CLAUDE.md contains both template sections and project-specific content. It cannot be blindly overwritten. Instead, diff and merge:

1. **Read the template's CLAUDE.md** and this repo's CLAUDE.md.
2. **Identify new sections** in the template that don't exist here. Add them.
3. **Identify updated sections** in the template. For each:
   - If the section here is unmodified from the original template → replace with the new version.
   - If the section here has project-specific modifications → merge carefully, preserving project content.
4. **Sections that are always project-specific** (never overwrite):
   - Project Overview
   - GitHub Project Board Integration (board URL, project number)
   - Known Patterns and Gotchas
   - Any project-specific Critical Rules (e.g., "Don't Skip the Done Gate")
   - During Development (Per Work Item) workflow customizations
5. **Sections that are always template-standard** (safe to replace):
   - Agent-Notes Protocol
   - Hybrid Team Methodology (phase table, capability roster)
   - Development Philosophy
   - Adversarial Debate Protocol
   - Agent Voice and Personality
   - Tiered Communication Protocol
   - Parallel Agent Teams
   - Conventions
6. **Sections that need careful merge** (template structure + project additions):
   - Critical Rules (template rules + project-specific rules)
   - Persona Triggers table
   - Done Gate checklist
   - Project Structure tree
   - Custom Commands table
   - Workflow sections

**Report to the user:** After merging, show a summary of what changed in CLAUDE.md so they can verify.

---

## What is NOT synced (kickoff-only concerns)

These are only relevant at project creation and should be skipped:
- Kickoff Phase 1-2 changes (Cam elicitation, Dani sacrificial concepts) — already happened.
- Initial project board creation — board already exists.
- Initial sprint setup — sprints are already in flight.

---

## Post-sync checklist

After syncing:

1. **Verify agent files:** `ls .claude/agents/` — confirm all agents are present.
2. **Verify command files:** `ls .claude/commands/` — confirm new commands (sprint-boundary, pin-versions, sync-template) are present.
3. **Verify doc templates:** Check that new directories exist under `docs/`.
4. **Review CLAUDE.md diff:** `git diff CLAUDE.md` — verify project-specific content was preserved.
5. **Commit:** `git add -A && git commit -m "chore: sync vteam-hybrid template evolutions"`
6. **Report:** Summarize what was added/updated to the user.
