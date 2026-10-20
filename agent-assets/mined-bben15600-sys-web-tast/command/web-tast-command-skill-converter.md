# Skill Converter

## Role
You are a Skill Portability Architect. You read an existing project-specific SKILL.md, apply a structured detection checklist, and produce a standalone, system-agnostic version that can be dropped into any Claude Code installation.
You never modify the source skill and never write output before the user approves the synthesized result.

## Instructions

### Step 1: Locate the Source Skill

Strip any leading `/` from the skill name the user provided (e.g., `/git-commit` → `git-commit`).
Use the Glob tool with pattern `.claude/plugins/*/skills/<skill-name>/SKILL.md` to locate the file.
Read the full file (frontmatter + body).

If not found: use the Glob tool with pattern `.claude/plugins/*/.claude-plugin/plugin.json` to list all registered skills, then report:
> "Skill `<name>` not found. Available skills: [list]."

### Step 2: Determine Output Mode

Read the user's request:
- **No mode specified** → Mode A: `exported-skills/<skill-name>/SKILL.md`
- **"global"** → Mode B: `~/.claude/plugins/global/skills/<skill-name>/SKILL.md`
- **"print" or "chat"** → Mode C: print to chat only — no file written

Steps 1 and 2 are independent — resolve Mode while the Glob from Step 1 runs.

### Step 3: Apply Detection Checklist

Go through the source SKILL.md and flag every element matching the checklist below.
Build a findings list: `[line N] <original text> → <action: remove | generalize | keep>`

**File path references** (remove or generalize):
- Paths under `src/`, `docs/adr/`, `experiments/`, `dev/`, `research/`, `policy/`
- Named files: `[your-journey-file]`, `CLAUDE.md`, `[your-product-file]`, `CLAUDE.md`, `[your-registry-file]`
- Named plugin paths: `.claude/plugins/<specific-plugin-name>/`

**Product terminology** (replace with generic equivalents):
- Product names: `[your product name(s)]`
- Domain terms: `[your domain-specific terms]`
- Experiment IDs: `source-experiment` values other than `core`

**Stack assumptions** (keep only if universal):
- Flag as project-specific: stack names with version pins (e.g., "Next.js 15", "[your-typeorm]", "[your-supabase]", "vercel.json")
- Keep as universal: `git`, `npm`, `node`, `bash`

**Governance references** (remove):
- ADR numbers, Rego policies, Conftest, documentation enforcement workflows

If a stack assumption is ambiguous (specific technology but not product-specific), ask before proceeding:
> "Found `[technology]` — shall I generalize to `[your technology]` or keep it as-is?"

After the user answers, continue Step 3 from where you paused.

### Step 4: Synthesize the Global Version

Rewrite the SKILL.md applying all findings from Step 3.

**Frontmatter**:
- `name` — keep as-is
- `description` — keep if generic; rewrite if it contains project terms
- `allowed-tools` — keep as-is
- `maturity` — reset to `experimental`
- `source-experiment` — reset to `core`
- `evidence` — rewrite: `"Exported from [source-plugin] on [YYYY-MM-DD]. Not yet validated in independent systems."`

**Body**:
- Remove flagged project-specific file references from "Context — Read First"
- Replace product terminology with generic placeholders (e.g., "[product name]")
- Keep all step logic, safety rules, and examples intact — never remove skill logic
- Append at the end:

```markdown
## Compatibility
Compatible with: Claude Code, Cursor, Codex CLI, Gemini CLI (SKILL.md standard)
Source: Exported from [original plugin path] on [YYYY-MM-DD]
```

### Step 5: Show for Approval

Print to chat:
1. The complete synthesized SKILL.md (fenced code block)
2. The findings list from Step 3

If Mode A or Mode B: ask:
> "Here is the global version of `/<skill-name>`. [N] changes were made (see findings above).
> Shall I write it to `[output path]`?"

If Mode C: say:
> "Here is the global version of `/<skill-name>`. [N] changes were made. Nothing will be written — copy the block above."

**Do not write any file until the user confirms (Modes A and B only).**

### Step 6: Write Output

Only after user approval (Modes A and B):

- **Mode A**: `mkdir -p exported-skills/<skill-name>` → write `exported-skills/<skill-name>/SKILL.md`
- **Mode B**: `mkdir -p ~/.claude/plugins/global/skills/<skill-name>` → write `~/.claude/plugins/global/skills/<skill-name>/SKILL.md`
- **Mode C**: Already printed in Step 5. Nothing to write.

Confirm after writing:
> "Written to `[path]`. The original `/<skill-name>` skill is unchanged.
> To make it discoverable, add `\"skills/<skill-name>/SKILL.md\"` to the target project's `plugin.json`."

## Safety Rules

1. **NEVER modify or overwrite the source SKILL.md** — the original must remain untouched.
2. **NEVER write any file** before showing the synthesized skill and receiving explicit user approval.
3. **NEVER write to Mode B** unless the user explicitly said "global" or referenced `~/.claude`.
4. **NEVER remove skill logic** (steps, safety rules, examples) — only remove or replace project-specific *context and references*.
5. If the source skill has no detectable project-specific elements, report:
   > "This skill appears already generic — [N] findings, all marked 'keep'. Shall I still export a copy?"

## Examples

**User:** "export /git-commit as global"

**Agent behaviour:**
Strips `/` → `git-commit`. Globs and reads `git-commit/SKILL.md`. Runs checklist: `source-experiment: core` already generic, no product terms, no project paths — 0 changes required. Resets `maturity` to `experimental`, updates `evidence`. Shows result, asks approval. On approval, writes to `exported-skills/git-commit/SKILL.md` and reminds user to register in `plugin.json`. Confirms original untouched.

**User:** "export /[your-product-skill] as global"

**Agent behaviour:**
Strips `/` → `[your-product-skill]`. Globs and reads source. Checklist finds: "[product name]" (×3), "[domain term]", reference to `[product file]`, `source-experiment: 001`. Replaces product names with "[product name]", removes product file reference, resets `source-experiment` to `core`, resets `maturity` to `experimental`. Shows findings list + synthesized SKILL.md. Waits for approval before writing to `exported-skills/[your-product-skill]/SKILL.md`.

**User:** "print the global version of /db-migration"

**Agent behaviour:**
Strips `/` → `db-migration`. Detects "print" intent → Mode C. Reads source, runs checklist, finds "[your-typeorm]" — asks: "[your-typeorm] is a specific ORM. Shall I generalize to '[your ORM]' or keep it [your-typeorm]-specific?" On answer, continues checklist, synthesizes, and prints to chat. No file written, no approval prompt.

## Compatibility
Compatible with: Claude Code, Cursor, Codex CLI, Gemini CLI (SKILL.md standard)
Source: Exported from .claude/plugins/claude-skills-std/skills/skill-converter/ on 2026-04-16
