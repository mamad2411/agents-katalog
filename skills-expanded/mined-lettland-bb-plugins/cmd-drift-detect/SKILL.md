---
name: cmd-drift-detect
description: Command — Detect system configuration drift - find stale rules, contradictions, and orphans
---

Self-monitoring command. Scans your entire Claude Code configuration for drift — stale rules, contradictions, orphaned files, and configuration inconsistencies.

## Scope detection (Step 0)

Resolve the target paths the same way `/system-audit` does:

```bash
if [[ -d "agents" && -d "commands" && -d "hooks" && -d "skills" ]]; then
  TARGET_AGENTS="agents"; TARGET_COMMANDS="commands"; TARGET_HOOKS="hooks"; TARGET_SKILLS="skills"
else
  TARGET_AGENTS=".claude/agents"; TARGET_COMMANDS=".claude/commands"; TARGET_HOOKS=".claude/hooks"; TARGET_SKILLS=".claude/skills"
fi
```

Apply these to every reference to `.claude/agents/`, `.claude/commands/`, `.claude/skills/`, `.claude/hooks/` in the checks below.

## Steps

### Step 1: Scan system files (parallel)

Read all configuration sources simultaneously:

- `CLAUDE.md` — project instructions
- `.claude/memory.md` — active memory
- `.claude/knowledge-base.md` — learned rules
- `.claude/settings.json` — hooks configuration
- `.claude/command-index.md` — command registry (if exists)

### Step 2: Check for contradictions

**Within CLAUDE.md:**

- Are there conflicting instructions? (e.g., "always do X" and "never do X")
- Are there references to files or directories that don't exist?
- Are there references to commands or agents that aren't defined?

**Between CLAUDE.md and knowledge-base:**

- Does the knowledge base contain rules that contradict CLAUDE.md?
- Are there duplicate rules across both files?

**Between memory and reality:**

- Does memory reference tasks, files, or states that no longer exist?
- Are there "current focus" items that are clearly stale?

### Step 3: Check for orphans

Scan for:

- **Orphaned commands:** Files in `$TARGET_COMMANDS/` not referenced in command-index.md
- **Orphaned agents:** Agent definitions in `$TARGET_AGENTS/` with no command or skill that invokes them
- **Orphaned skills:** Skills in `$TARGET_SKILLS/` not referenced by any command, agent, or CLAUDE.md
- **Dead references:** Mentions of files, URLs, or paths that don't exist — in the top-level config (`CLAUDE.md`, memory, knowledge-base, `settings.json`). The shipped skill/command/agent/reference doc corpus is swept separately in Step 5.
- **Unused hooks:** Hook scripts in `$TARGET_HOOKS/` that exist but aren't wired in settings.json

### Step 4: Check for staleness

- **Memory.md:** Is "Now" section from more than 3 days ago?
- **Knowledge-base entries:** Do any reference outdated tools, APIs, or patterns?

### Step 5: Check reference integrity (docs ↔ code/config)

The doc corpus — `$TARGET_SKILLS/*/SKILL.md`, `references/*.md`, `$TARGET_COMMANDS/`, `$TARGET_AGENTS/` — names concrete things that rot independently of the prose around them: file paths, script names, bundled package ids, command/agent/skill slugs, and tool flags. A reference that no longer resolves silently misleads the next reader. Steps 2–3 cover dead references in `CLAUDE.md` and memory; this step extends the same check to the documentation that ships with the plugin.

Glob the corpus (the `*.md` skill/command/agent/reference files), then for each file flag references that no longer resolve. Check existence with `Read` / `Glob` — do not build a `find` invocation around a path string lifted from file content; reserve `find` for enumerating fixed, literal directories.

- **File / script paths:** backtick-quoted paths containing `/` and an extension (e.g., `scripts/foo.sh`, `hooks/baz.sh`, a `references/` page). Confirm each with `Read` / `Glob`.
- **Slugs:** skill, command, and agent names invoked in bodies (`Skill(...)`, `/...`, `Agent(...)`) with no matching definition under `$TARGET_SKILLS` / `$TARGET_COMMANDS` / `$TARGET_AGENTS`. (`related:` slugs are already gated by the frontmatter validator — focus on body invocations.)
- **Bundled package ids:** server package names referenced by name in skills/docs that no longer match `.mcp.json`.
- **Tool flags / env vars:** flags and `DEVKIT_*` env vars named in docs that aren't defined or read by any script, hook, or `settings.json`. A var consumed only by the agent/harness at runtime (e.g. a `DEVKIT_<NAME>` var) is valid — don't flag it for being absent from shell scripts.

**Ignore illustrative references.** Flag only references the doc presents as real. Skip example and placeholder tokens: angle-bracket placeholders (`<slug>`, `exact/path/to/file.py`), and any path or `Skill()` / `Agent()` token inside a fenced code block used as a syntax example or template — the same way Step 6 ignores `[[ -f x ]]`-style non-references.

**Relink gate (do not silently fix).** When a reference is stale, the fix is a judgement call — the target may have been renamed, moved, or deliberately removed. Report each stale reference with its file, the dead target, and the likely current target if one is obvious, and let the user bless the re-point. Never auto-rewrite a reference to a guessed target.

### Step 6: Check memory corpus integrity

Keep the memory stores consistent. The project-local check runs with this command's tools (`Read` / `Grep`); the global auto-memory sweep is manual (that dir lives outside the project, so project-scoped Glob/Grep can't reach it). Report entity and file **names only** — never quote stored values, since the JSONL store is plaintext and a report may be shared.

- **Knowledge-graph ↔ markdown drift (project-local):** the rule is "don't write the same fact into both stores — they drift." Use `.codex/memory.jsonl` when it exists, otherwise `.claude/memory.jsonl`; both are gitignored runtime state, so skip this sub-check if neither exists. List entity names with `grep '"name":' <memory-file>` and check whether the same fact also lives in `knowledge-base.md`; flag duplicates by name, and graph entities whose observations reference removed files, tools, or APIs.
- **Global auto-memory sweep (manual):** the auto-memory corpus — a `MEMORY.md` index plus one `.md` file per fact, cross-linked with `[[slug]]` wiki-links — lives outside the project. When asked to sweep it, point `Read` / `Grep` at that dir and flag: index lines whose target file is missing, fact files absent from the index, and dangling `[[slug]]` links (a slug with no matching file). Match `[[kebab-slug]]` note references only — ignore code/TOML/shell double-brackets such as `[[ -f x ]]` or `[[tool.mypy]]`. Note in the report whether this sweep ran or was skipped.

### Step 7: Check configuration health

- **settings.json:** Is `.claude/settings.json` valid JSON? (always at project `.claude/`, regardless of MODE)
- **Hook scripts executable?** Check `$TARGET_HOOKS/*.sh` — each should have +x. List any without it.
- **CLAUDE.md size:** Is it growing too large? (>500 lines is a warning)
- **Memory.md size:** Is it within limits? (<100 lines target)
- **Knowledge-base size:** Is it within limits? (<200 lines target)

### Step 8: Generate drift report

```markdown
# Drift Detection Report

**Date:** [date]
**Status:** [CLEAN / WARNINGS / ISSUES FOUND]

## Contradictions Found

- [contradiction with file references]

## Orphaned Items

- [orphaned file or reference]

## Stale Items

- [stale memory, task, or reference]

## Reference Integrity

- [stale doc↔code reference: file → dead target → likely current target, or note none is obvious. Awaiting relink confirmation — not auto-fixed.]

## Memory Corpus

- [knowledge-graph ↔ markdown drift; if the global sweep ran, index/wiki-link orphans — else note it was skipped]

## Configuration Health

| Check                   | Status    | Note           |
| ----------------------- | --------- | -------------- |
| settings.json valid     | Pass/Fail |                |
| CLAUDE.md size          | [lines]   | [ok / warning] |
| memory.md size          | [lines]   | [ok / warning] |
| knowledge-base size     | [lines]   | [ok / warning] |
| Hook scripts executable | Pass/Fail |                |

## Recommended Actions

1. [Specific fix]
2. [Specific fix]
3. [Specific fix]

---

Run monthly or when system behaviour feels off.
```

Output the status line and any critical issues. Offer to fix automatically if issues are simple — but Step 5 reference re-points always go through the relink gate (report and let the user confirm), never auto-fixed.
