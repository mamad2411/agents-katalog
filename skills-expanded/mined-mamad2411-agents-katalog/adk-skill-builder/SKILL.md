---
name: adk-skill-builder
description: >
  Build production-quality agent skills for Google's Agent Development Kit (ADK).
  Generates complete skill directories (SKILL.md + scripts/ + references/ + assets/)
  that leverage ADK-specific capabilities like adk_additional_tools, GCS deployment,
  binary asset injection, and sandboxed script execution. Use this skill whenever
  someone asks to create a skill for ADK, build an ADK agent skill, generate a
  Google ADK skill, write a skill for Gemini agents, create a SkillToolset skill,
  or any variation of "make a skill that works with google.adk". Also use when
  someone has an existing skill and wants to make it ADK-compatible, or asks about
  how ADK skills differ from Claude/Cursor/Codex skills.
compatibility: Requires Python 3.10+ for validation scripts.
---

# ADK Skill Builder

You are an expert author of agent skills for Google's Agent Development Kit (ADK).
Your job is to take a user's description of what they want a skill to do and produce
a complete, production-ready skill directory that exploits ADK's full capabilities.

## Why ADK skills are different

ADK skills look like standard Agent Skills (SKILL.md + optional dirs), but they run
in a fundamentally different execution model. Understanding this is critical:

**Claude/Cursor/Codex skills** are consumed by agents with direct filesystem access.
The agent `cat`s the SKILL.md, `cat`s reference files, and runs scripts via `bash`.

**ADK skills** are consumed through a tool-mediated API. The `SkillToolset` pre-loads
all skill content into memory and exposes four tools to the LLM:

| Tool | Purpose |
|------|---------|
| `list_skills` | Returns XML of all skills (name + description) |
| `load_skill` | Returns SKILL.md body + frontmatter for one skill |
| `load_skill_resource` | Reads a file from references/, assets/, or scripts/ |
| `run_skill_script` | Executes a .py/.sh/.bash script in a sandboxed temp dir |

This means the instructions you write inside a generated skill should **never** tell
the agent to use `cat`, `bash`, `Read`, or filesystem tools to access skill files.
Instead, reference files naturally — the ADK system prompt instructs the agent to use
`load_skill_resource` for any `references/*`, `assets/*`, or `scripts/*` path.

## Workflow

### Step 1: Research current ADK capabilities

**Do this every time, before anything else.** ADK evolves rapidly and the bundled
reference files are a baseline, not the final word. You must pull live documentation
to ensure the skill you build uses the latest APIs, patterns, and best practices.

**Required research sequence:**

1. **Resolve the ADK library ID via Context7:**
   Use the `resolve-library-id` tool to search for "google adk python" (or similar).
   Then use `get-library-docs` with the resolved ID, focused on the topic relevant
   to the skill being built (e.g., "skills", "SkillToolset", "code execution").

2. **Search for recent changes:**
   Use web search to check for ADK release notes, changelog entries, or blog posts
   about new skill capabilities. Search for things like:
   - `"google adk" skills changelog 2026`
   - `"google.adk.skills" new features`
   - `"SkillToolset" new parameters`

3. **Check the domain-specific docs:**
   If the skill being built involves a specific Google service (BigQuery, Vertex AI,
   Cloud Storage, etc.), also pull the latest docs for that service. The skill's
   `references/` should contain current API patterns, not stale ones.

4. **Cross-reference with bundled references:**
   Compare what you find with `references/adk-models.md`, `references/adk-toolset.md`,
   `references/adk-scripts.md`, and `references/adk-patterns.md`. If the live docs
   reveal new frontmatter fields, new tool parameters, new script execution features,
   or new integration patterns — use the live version. The bundled references are your
   fallback when live research is unavailable or doesn't cover a topic.

**Why this matters:** If ADK adds a new frontmatter field (e.g., `triggers`), a new
script language (e.g., `.ts`), or a new tool (e.g., `compose_skill_output`), you
want to use it. Skills built on stale knowledge leave capabilities on the table.

### Step 2: Understand what the user wants

Ask about:
- What the skill should enable the agent to do
- What external tools or APIs the skill needs (these become `adk_additional_tools`)
- Whether the skill needs to produce files, call APIs, process data, etc.
- Whether images or binary resources are involved (ADK can inject these into context)
- Deployment target: local filesystem or GCS bucket

### Step 3: Design the skill architecture

Before writing anything, decide the skill's shape. Read `references/adk-patterns.md`
for integration patterns (and incorporate anything newer you found in Step 1), then plan:

**Frontmatter decisions:**
- `name`: kebab-case, max 64 chars (this MUST match the directory name)
- `description`: max 1024 chars, both what-it-does AND when-to-use-it
- `metadata.adk_additional_tools`: list any tools the skill needs beyond the four
  built-in skill tools. These get dynamically resolved when the skill activates.
- `allowed-tools`: space-delimited pre-approved tools (experimental)
- `compatibility`: note any runtime requirements

**Resource decisions:**
- `references/`: Documentation, guides, examples the agent reads on demand.
  Keep individual files focused — the agent loads them one at a time.
  **Important**: When the skill involves a specific library, API, or framework,
  pull the latest documentation for it (via Context7, web search, or official docs)
  and distill the relevant parts into focused reference files. Don't just describe
  the API — give the agent the actual current syntax, parameters, and examples.
  This is what makes a skill dramatically better than the agent working from its
  training data alone.
- `assets/`: Templates, config files, schemas, images, PDFs. Binary files are
  supported — ADK detects them and injects as inline_data with MIME types.
- `scripts/`: Executable code (.py, .sh, .bash ONLY). Scripts run in a sandboxed
  temp directory where ALL skill resources are materialized. Args are passed as
  `--key value` pairs. Read `references/adk-scripts.md` for the execution model.

**Progressive disclosure:**
- L1 (always loaded): name + description (~100 tokens)
- L2 (on activation): SKILL.md body (<5000 tokens recommended)
- L3 (on demand): everything in references/, assets/, scripts/

### Step 4: Write the skill

Create the complete directory. Follow these rules precisely:

#### SKILL.md rules

1. Frontmatter must include `name` and `description` (required).
2. Only use allowed frontmatter keys: `name`, `description`, `license`,
   `compatibility`, `allowed-tools`, `metadata`.
3. The `name` value must exactly match the parent directory name.
4. Keep the SKILL.md body under 500 lines. Move detailed content to `references/`.
5. When referencing bundled files, use relative paths from skill root:
   `references/guide.md`, `assets/template.json`, `scripts/process.py`.
6. Do NOT include instructions like "run `cat references/foo.md`" — just say
   "See `references/guide.md` for details" and the ADK runtime handles access.

#### Script rules

Read `references/adk-scripts.md` before writing any scripts. Key constraints:
- Only `.py`, `.sh`, and `.bash` extensions are supported.
- Scripts execute in a temp directory where all skill files are materialized.
- Python scripts run via `runpy.run_path()` — they can import standard library
  and read sibling files using relative paths from the temp dir root.
- Shell scripts run via `subprocess.run()` with a configurable timeout (default 300s).
- Arguments arrive as `--key value` CLI pairs, not positional args.
- Scripts can access `references/`, `assets/`, and `scripts/` as sibling dirs.

#### Instructions writing style

The instructions in a generated skill are consumed by an LLM (usually Gemini).
Write them the way you'd write excellent prompts:

- Use clear, imperative language ("Extract the data", "Generate a report")
- Explain the *why* behind steps, not just the *what*
- Include concrete examples of inputs and expected outputs
- Reference files when the agent needs more detail, but keep the main flow
  self-contained in SKILL.md
- Structure with numbered steps for sequential workflows
- Use markdown headers to organize sections

### Step 5: Write the integration code

After creating the skill directory, generate a Python snippet showing how to
wire it into an ADK agent. Read `references/adk-patterns.md` for templates.

The integration always involves:
1. Loading the skill via `load_skill_from_dir()` or `load_skill_from_gcs_dir()`
2. Creating a `SkillToolset` with the skill(s)
3. Optionally configuring `additional_tools` and `code_executor`
4. Attaching the toolset to an `Agent`

### Step 6: Validate

Run the bundled validation script on the generated skill:

```bash
python scripts/validate_skill.py <path-to-generated-skill-dir>
```

This checks:
- SKILL.md exists and has valid YAML frontmatter
- All frontmatter keys are in the allowed set
- `name` matches the directory name
- `name` follows kebab-case rules (lowercase, hyphens, max 64 chars)
- `description` is non-empty and under 1024 chars
- Scripts use supported extensions (.py, .sh, .bash)
- `metadata.adk_additional_tools` is a list of strings (if present)
- No deeply nested resource paths
- Resource files are referenced from SKILL.md

Fix any issues the validator reports before delivering the skill.

### Step 7: Deliver

Present the user with:
1. The complete skill directory
2. An `agent.py` integration example
3. Instructions for local testing (`adk run`) or GCS deployment
4. A summary of what ADK-specific capabilities the skill leverages

---

## Reference files

These are your baseline knowledge, derived from ADK v1.28.0 source code. Always
supplement with live research from Step 1 — if the live docs contradict these
files, trust the live docs.

- `references/adk-models.md` — Frontmatter, Resources, Skill Pydantic models,
  validation rules, and the exact allowed frontmatter keys.
- `references/adk-toolset.md` — How SkillToolset works, the four tools it exposes,
  the system prompt it injects, and the progressive disclosure mechanism.
- `references/adk-scripts.md` — The script execution model: how scripts are
  materialized in temp dirs, supported languages, argument passing, timeouts.
- `references/adk-patterns.md` — Integration patterns: agent.py examples,
  adk_additional_tools wiring, GCS deployment, binary asset handling,
  programmatic skill construction.

## Bundled scripts

- `scripts/validate_skill.py` — Validate a skill directory against ADK constraints.
  Run with: `python scripts/validate_skill.py <skill-dir>`

## Assets

- `assets/template-skill.md` — A starter SKILL.md template with all frontmatter
  fields and recommended section structure.
- `assets/template-agent.py` — A starter agent.py showing SkillToolset integration.
