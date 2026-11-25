---
name: super-init
description: "Initialize or audit a project's CLAUDE.md against best-practice criteria. Use on first-time setup ('init', 'set up project', 'first time in this repo'), when scanning a project to create CLAUDE.md, or when refreshing an existing CLAUDE.md against the current state of the codebase. Replaces Claude Code's default /init."
phase: meta
produces:
  - claude-md
---

# super-init

Initialize or audit a project's CLAUDE.md. Less is more — a 50-line CLAUDE.md that Claude actually follows beats a 300-line one it ignores.

**Announce at start:** "I'm using super-init to scan your project and generate or audit your CLAUDE.md."

## Branch Detection

```bash
if [ -f ./CLAUDE.md ]; then
  echo "branch=AUDIT"
else
  echo "branch=GENERATE"
fi
```

`GENERATE` runs the 9-step generate flow below. `AUDIT` runs the 8-step audit flow below.

## The Golden Rule

For every line you generate, ask: **"Would removing this cause Claude to make a mistake?"**

If Claude would figure it out from the code anyway — don't include it. CLAUDE.md is for things Claude can't infer.

## What to Include vs Exclude

| Include (Claude can't infer) | Exclude (Claude can figure out) |
|------------------------------|--------------------------------|
| Non-obvious build/test/lint commands | Standard language conventions |
| Unconventional project structure | Obvious file organization |
| Environment quirks (required env vars, setup steps) | Framework defaults |
| Code conventions that differ from defaults | Things visible in config files |
| Common gotchas and non-obvious behaviors | File-by-file codebase descriptions |
| Architectural decisions not visible in code | Detailed API documentation |
| Branch naming / PR conventions | Standard git workflow |

## GENERATE branch (no CLAUDE.md present)

### Step 1: Detect Tech Stack

```bash
cat package.json 2>/dev/null        # Node.js
cat requirements.txt 2>/dev/null     # Python
cat pyproject.toml 2>/dev/null       # Python (PEP 621 / poetry)
cat Cargo.toml 2>/dev/null           # Rust
cat go.mod 2>/dev/null               # Go
cat pom.xml 2>/dev/null              # Java
```

Extract: language, framework, key dependencies. Only note what's non-obvious.

### Step 2: Discover Commands

```bash
# Prefer jq when available; fall back to plain-text grep otherwise.
if command -v jq >/dev/null 2>&1; then
  cat package.json 2>/dev/null | jq '.scripts' 2>/dev/null
else
  # jq missing — grep the scripts block as plain text.
  awk '/"scripts"[[:space:]]*:/{flag=1} flag{print} /^[[:space:]]*\}/{if(flag){flag=0; exit}}' package.json 2>/dev/null
fi

# Check for Makefile
cat Makefile 2>/dev/null | grep '^[a-z].*:' | head -10

# Check for justfile, taskfile, etc.
ls Makefile justfile Taskfile.yml .taskfile 2>/dev/null
```

Only include commands Claude can't guess. If the test command is `npm test`, skip it. If it's `npm run test:unit -- --coverage --bail`, include it.

### Step 3: Detect Non-Obvious Conventions

Read 3-5 source files to spot patterns:
- Import style (named exports vs default, absolute vs relative paths).
- Component patterns (functional vs class, co-located tests vs separate).
- Naming conventions (if non-standard).
- Any `.eslintrc`, `.prettierrc`, `tsconfig.json` enforcing unusual rules.

**Only note conventions that differ from language/framework defaults.**

### Step 4: Check for Gotchas

```bash
# Monorepo?
ls packages/ apps/ modules/ 2>/dev/null

# Custom tooling?
ls scripts/ tools/ bin/ 2>/dev/null

# Environment requirements?
cat .env.example 2>/dev/null
cat .tool-versions 2>/dev/null
cat .nvmrc 2>/dev/null

# Commit message convention.
git log --oneline -10 2>/dev/null
```

Skip the `git log` step silently if `git` is missing or there are no commits.

### Step 5: Detect Layout + Pick Template

Apply the auto-detection rules in `references/templates.md` (monorepo signals → `monorepo`; package signals → `package`; minimal-root signals → `minimal-root`; otherwise → `comprehensive-root`).

State the chosen template with a one-line rationale, e.g.:
> Detected `pnpm-workspace.yaml` + `packages/` at root → using `monorepo` template.

The user can override at step 7.

### Step 6: Draft + Self-Score

Fill the chosen template with scan results. Apply the Golden Rule and the "What NOT to Add" list from `references/update-guidelines.md`.

Self-score the draft against `references/quality-criteria.md` (6 criteria, weights 20/20/15/15/15/15, total 100, grade A≥85 / B≥70 / C≥55 / F<55).

### Step 7: User Review + Write

Present the draft, the score, and the grade.

**Line-budget warning (AT-4).** If the draft is over 100 lines:
> "Draft is N lines, target is <=100. This is usually a sign of including too much. Type `override` to proceed anyway, or `cut` to revise."

The skill does not proceed to write until the user types `override` (or revises and re-scores under 100). No silent overwrite of the budget.

Approval prompt:
> "Here's the generated CLAUDE.md (N lines, grade X). Review it — I've tried to include only things I can't infer from the code. Apply, override-template (`minimal-root` / `comprehensive-root` / `package` / `monorepo`), or cancel?"

On approval, write `./CLAUDE.md`. On cancel, exit cleanly without writing or scaffolding.

### Step 8: `.claude/rules/` Scaffold (monorepo + opt-in only)

Run this step **only if** the chosen template was `monorepo`. On any other template, skip silently.

Prompt:
> "This is a monorepo. Want me to scaffold `.claude/rules/` with one starter rule per package or app directory? (y/n)"

On `y`: create `.claude/rules/` and one starter rule file per directory directly under any monorepo workspace root. A directory is "detected" when it lives directly under `packages/`, `apps/`, or any directory matched by a `workspaces` glob in `package.json` / `pnpm-workspace.yaml` / `lerna.json`. Both `packages/*` and `apps/*` are scaffolded when both exist.

On `n`: skip; continue to step 9.

### Step 9: Onboarding Panel (one-shot, GENERATE-first-run only)

This step runs **only on GENERATE** (`./CLAUDE.md` was absent at the start of the run). It is **never** printed on AUDIT or on any subsequent re-run.

Print:
```
==========================================
super-init complete
==========================================
File:     ./CLAUDE.md
Lines:    <N>
Template: <template-name>
Grade:    <grade> (<score>/100)
<.claude/rules/ summary, only if scaffolded>

Tips for getting more out of CLAUDE.md:

1. The `#` shortcut: typing `#` at the start of a message stages a memory addition.
2. Organic correction persistence: when Claude is corrected on a project convention, it will offer to persist the correction to the Gotchas section.
3. Hooks vs CLAUDE.md compliance reality: research suggests CLAUDE.md rules are followed roughly 70% of the time. This plugin's hooks (already shipped) provide the deterministic enforcement layer for the rules that need to be hard rules.
4. Re-run /super-init: running the command again later enters AUDIT mode and refreshes the file against the current state of the project.
==========================================
```

## AUDIT branch (existing CLAUDE.md present)

### Step 1: Read existing CLAUDE.md

Read `./CLAUDE.md` into memory.

**Unparseable existing CLAUDE.md.** If the read fails or markdown parsing yields no recognizable section structure, present:
> "Existing ./CLAUDE.md couldn't be parsed cleanly. Options: (a) back it up to ./CLAUDE.md.bak and re-route to GENERATE, (b) exit. Pick a or b."

On `a`: `cp ./CLAUDE.md ./CLAUDE.md.bak`, then `rm ./CLAUDE.md`, then re-enter the skill (which now sees no CLAUDE.md and routes to GENERATE). On `b`: exit cleanly.

### Step 2: Re-run scan

Run GENERATE steps 1-4 (Detect Tech Stack, Discover Commands, Detect Non-Obvious Conventions, Check for Gotchas).

### Step 3: Score against rubric

Score the existing file against `references/quality-criteria.md`. Report the score and grade.

### Step 4: Compute diff

Compute the section-keyed unified-diff per `references/update-guidelines.md`:
- **Stale lines:** commands or conventions in the file that no longer match the scan.
- **Missing additions:** non-obvious commands or gotchas the scan surfaced that aren't in the file.

If the diff is empty:
> "No patches needed. Score: <score>/100, Grade: <grade>. Exiting."

Exit without writing.

### Step 5: Present score + patches

Show the score, grade, and the diff hunks (one per touched section).

### Step 6: Per-patch or bulk approval

Per the approval prompt format in `references/update-guidelines.md`:
- Per-section: `[y/n/skip-all]` for each touched section.
- Bulk: `[Y]` to apply every hunk.

Unapproved hunks are dropped.

### Step 7: Apply approved patches in place

Apply the approved hunks. Sections the diff did not touch remain untouched. No whole-file overwrite.

### Step 8: `.claude/rules/` Bootstrap (monorepo + missing + opt-in)

Run this step **only if** the layout signals `monorepo` AND `./.claude/rules/` does not exist. On any other layout, or if the directory exists, skip silently.

Prompt:
> "This is a monorepo and `.claude/rules/` is missing. Want me to scaffold it? (y/n)"

On `y`: same scaffold as GENERATE step 8. On `n`: skip.

**Do not print the onboarding panel on AUDIT.** AT-8 requires it to be GENERATE-first-run only.

## Forbidden Writes (AT-10)

The skill writes only to:
- `./CLAUDE.md`
- `./.claude/rules/` (only on opt-in monorepo paths)
- `./CLAUDE.md.bak` (only on the AUDIT unparseable-fallback path)

The skill **never** writes to:
- `~/.claude/settings.json`
- `./.claude/settings.json` (the settings file)
- `./.claude.local.md`
- `./.claude/settings.local.json`

Configuring the harness is out of scope. The plugin's existing `hooks/hooks.json` `PostToolUseFailure` Bash matcher already ships pre-wired; no user-side `.claude/settings.json` change is required for organic growth to work.

## Organic Growth

### Persisting Corrections

When the user corrects you about a project convention during normal work (e.g., "No, we use pnpm here, not npm"), offer to persist it:

> "Got it — want me to add this to CLAUDE.md so I remember next time?"
>
> Proposed addition to ## Gotchas:
> `- Use pnpm, not npm (no package-lock.json in this project)`

If the user agrees, append the line to the Gotchas section of CLAUDE.md. **If no Gotchas section exists, create one.**

**This is a behavioral instruction for all skills, not just super-init.** Any time Claude is corrected about something project-specific, it should offer to persist the correction.

### Auto-Detecting Failures

A `PostToolUseFailure` hook fires when commands fail. The hook prompts Claude to consider whether the failure was caused by a project-specific convention that should be recorded:

```json
"PostToolUseFailure": [
  {
    "matcher": "Bash",
    "hooks": [
      {
        "type": "prompt",
        "prompt": "A command failed. If this failure was caused by a project-specific convention, setup requirement, or non-obvious configuration that Claude should know about for future sessions, suggest adding a rule to CLAUDE.md's Gotchas section. Only suggest this if the failure reveals something non-obvious — don't suggest adding rules for typos or standard errors."
      }
    ]
  }
]
```

This block already ships in this plugin's `hooks/hooks.json`. No user-side `.claude/settings.json` change is required. This creates a feedback loop: failures → rules → fewer failures.

## Anti-Rationalizations

| Thought | Reality |
|---------|---------|
| "I'll add everything just in case" | More rules = more ignored rules. Every unnecessary line dilutes the important ones. |
| "Claude needs to know the full architecture" | Claude can read the code. It needs to know what the code doesn't tell it. |
| "I'll generate it once and forget it" | CLAUDE.md should grow organically. The Gotchas section is where the real value accumulates. |
| "This project is too simple for CLAUDE.md" | Even 5 lines (commands + one gotcha) save time across sessions. |

## Red Flags

- Generated CLAUDE.md over 100 lines — too verbose, cut ruthlessly.
- Including standard conventions (functional components, ES modules) that Claude knows.
- Including file-by-file descriptions of the codebase.
- No Gotchas section — this is where organic growth happens.
- Never updating CLAUDE.md after generating it — it should be a living document.

## Verification

After generating or auditing CLAUDE.md:

- [ ] File is under 100 lines
- [ ] Every line passes the "would removing this cause a mistake?" test
- [ ] Commands section only has non-obvious commands
- [ ] Conventions section only has things that differ from defaults
- [ ] Gotchas section exists (even if empty) for organic growth
- [ ] User has reviewed and approved the content
- [ ] Rubric grade >= B for the generated/audited file
