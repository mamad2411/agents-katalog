---
name: skill-marketplace
description: Detects the tech stack of the current project and installs matching Agent Skills from a curated registry. Use when the user asks for skill recommendations, wants to set up skills for a project, or says "install skills for my stack".
---

# Skill Marketplace

You help the user discover and install Agent Skills that match their project's tech stack. You have two local resources:

- `scripts/detect.py` — stack detector. Run it against a project directory.
- `references/registry.md` — curated registry of real, verified Agent Skills with stack tags and source URLs.

## Workflow

### 1. Detect the stack

Run the detector against the user's project directory (default: current working directory):

```
python3 <skill-dir>/scripts/detect.py /path/to/project
```

It prints JSON like:

```json
{"stacks": ["node", "react", "typescript"], "signals": {"package.json": ["react", "typescript"]}}
```

If detection finds nothing, say so plainly and ask what stack the project uses instead of guessing.

### 2. Look up matching skills

Open `references/registry.md` and collect every entry whose **Stacks** tags intersect the detected stacks. Rank matches by number of overlapping tags (more overlap first). If nothing matches, say so and offer the closest general-purpose entries.

### 3. Present matches and ask before installing

Show the user a short list: skill name, one-line description, and which of their stacks it matches. Then ask:

- Which skills to install (default: all matches)
- Install scope: **project-local** (`.claude/skills/` in the project, preferred) or **global** (`~/.claude/skills/`)

Never install without an explicit yes.

### 4. Install

For each approved skill:

1. Clone or sparse-download the skill directory from its **Source repo** into the target skills dir:
   ```
   git clone --depth 1 --filter=blob:none --sparse <repo-url> <tmp>
   git -C <tmp> sparse-checkout set <install-path>
   cp -r <tmp>/<install-path> .claude/skills/<skill-name>/
   ```
   (If `git` is unavailable, fetch the `SKILL.md` URL directly with curl and recreate the directory.)
2. Verify the install: `.claude/skills/<skill-name>/SKILL.md` must exist and its YAML frontmatter must contain `name` and `description`. The frontmatter `name` should match the directory name.
3. Report what was installed and where. If verification fails, remove the partial directory and tell the user.

### 5. Confirm

Summarize: which skills are now active, where they live, and that they take effect in new Claude Code sessions.

## Examples

**Example 1 — fresh Python API project:**
User: "install skills for my stack"
You: run `detect.py` in the project → `{"stacks": ["python", "fastapi", "docker"]}` → registry matches `python-pro`, `fastapi-developer`, `docker-expert` → present the three, ask project-local vs global → on approval install to `.claude/skills/` and verify each SKILL.md.

**Example 2 — user asks for recommendations only:**
User: "what skills should I use for this Next.js app?"
You: detect → `["node", "react", "nextjs", "typescript"]` → recommend `nextjs-developer`, `react-specialist`, `typescript-pro`, `frontend-design` with one-line reasons. Do not install anything; the user asked for recommendations, not installation.

**Example 3 — global install:**
User: "set up the docker skill globally"
You: confirm the skill exists in the registry (`docker-expert`), ask for confirmation, then install to `~/.claude/skills/docker-expert/` and verify.

## Guidelines

- Ask before installing. Always.
- Prefer project-local installs (`.claude/skills/`) so the skills travel with the repo. Use global (`~/.claude/skills/`) only when the user asks.
- Never invent registry entries. If a skill is not in `references/registry.md`, do not claim it is available.
- After install, verify `SKILL.md` exists and has valid frontmatter. A skill without frontmatter will not load; fix or remove it.
- Keep the registry fresh: every URL in it was verified with an HTTP 200 check when the registry was written. If a download fails, tell the user the source may have moved instead of silently substituting another.
