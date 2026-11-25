---
name: skill-checker
description: Validate and review Claude Code skill folders and SKILL.md files for manifest correctness, triggering quality, concise instructions, progressive disclosure, portability, safety, and testability. Use when a user asks to check, audit, debug, grade, or improve a skill, especially when it fails to trigger, triggers too broadly, has broken references, or is being prepared for distribution.
---

# Skill Checker

Separate deterministic defects from editorial judgment. Current official product documentation is the source of truth; do not promote a blog post, old guide, or this skill's heuristics into a platform requirement.

## Review modes

- **Validate:** run structural checks and report errors and warnings.
- **Review:** add trigger, workflow, safety, portability, and maintainability analysis.
- **Improve:** propose or implement fixes only when the user asks for changes.

## 1. Establish scope

Locate the skill directory and read its entire `SKILL.md`. Read referenced files only as needed to validate links, routing, scripts, and claimed behavior. If the skill belongs to a plugin, also inspect the plugin manifest and component paths when relevant.

Identify the target runtime and confirm current official rules when a platform detail may have changed.

## 2. Run deterministic checks

When the folder is available locally, run:

```bash
python "${CLAUDE_PLUGIN_ROOT}/skills/skill-checker/scripts/validate_skill.py" <skill-path>
```

Use `--json` for machine-readable output. The validator checks:

- exact `SKILL.md` filename and frontmatter delimiters;
- required `name` and `description` fields;
- kebab-case name, folder-name match, and description length;
- supported and suspicious frontmatter fields;
- body length and progressive-disclosure signals;
- broken local Markdown links;
- long references without navigation;
- Python and shell script syntax when `--check-scripts` is supplied.

Treat warnings as review prompts, not automatic failures.

## 3. Review triggering

The description should say what the skill does and when it should be used, using concepts and user intent that distinguish it from adjacent skills. Exact quoted phrases are optional. Negative scope belongs in the description only when it prevents likely over-triggering.

Test at least:

- an obvious request that should trigger;
- two natural paraphrases;
- an adjacent request that should not trigger;
- a request where another available skill should win.

Report observed or predicted ambiguity and provide a concise description rewrite when useful.

## 4. Review instructions

Assess whether the body:

- leads with critical constraints and the core workflow;
- uses ordered steps only where order matters;
- explains tool and reference routing conditionally;
- preserves user authority for external, destructive, or consequential actions;
- defines inputs, outputs, validation, failure handling, and stopping conditions;
- avoids hard-coded installation paths and unavailable tool names;
- avoids time-sensitive facts that should be looked up at execution time;
- stays concise by moving detailed variants, examples, and schemas into referenced files.

Do not penalize a simple skill for lacking a complex workflow, examples, scripts, or references it does not need.

## 5. Review bundled resources

- Scripts should be deterministic, scoped, safe with paths and secrets, and accompanied by an invocation contract.
- References should be linked from `SKILL.md` with a clear condition for reading them.
- Assets should be reusable inputs rather than unexplained outputs.
- Avoid duplication between the body and references.

## 6. Report

Use this format:

```text
Skill: <name>
Verdict: valid | valid with warnings | invalid

Blocking errors
- ...

Warnings and evidence
- ...

Trigger review
- should trigger: ...
- should not trigger: ...

Top improvements
1. ...
2. ...
3. ...

Checks run
- command: result
```

Give file and line references for local findings. Avoid a numerical score unless the user requests one and the rubric is defined up front; scores can hide blocking defects and imply false precision.

For a condensed checklist, read [quick-reference.md](references/quick-reference.md).
