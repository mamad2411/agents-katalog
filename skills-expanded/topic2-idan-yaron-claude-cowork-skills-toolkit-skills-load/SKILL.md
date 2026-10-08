---
name: skills-load
description: >
  Load skills from a GitHub repository into the current Cowork session as a 
  unified plugin. Use when the user says "load skills from GitHub", "import 
  skills from repo", "add skills from URL", "install skills from this link", 
  or runs /skills-load with a GitHub URL. Also trigger when the user pastes a 
  GitHub URL and mentions skills, plugins, or Claude capabilities they want to add.
argument-hint: <github-url>
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# Load Skills from GitHub

Fetch a GitHub repo, show its skill catalog, resolve dependencies, and package
selected skills as a single `.plugin` file that installs into Cowork with one click.

## How it works

Cowork's plugin system accepts `.plugin` files (ZIP archives with a standard
directory layout). When presented via `mcp__cowork__present_files`, Cowork
renders a rich preview with an **"Save plugin"** button. Clicking it installs the
entire plugin — all skills appear in the `/` menu immediately, mid-session.

This is better than installing skills individually because:
- One click installs everything (not N clicks for N skills)
- Dependencies stay bundled together as a coherent package
- The plugin can be shared as a single file

Skills are also injected into the conversation for immediate use, even before
the user clicks Save plugin.

## VM constraints

- **Bash** runs in an isolated Linux VM — use for cloning repos and building ZIPs.
- **Write tool** bridges to the HOST filesystem.
- Host paths like `~/AppData/...` don't exist inside the VM.

## Step 1: Parse the URL

Extract the GitHub URL from `$ARGUMENTS`. Handle these formats:

- `https://github.com/owner/repo`
- `https://github.com/owner/repo/tree/branch`
- `https://github.com/owner/repo/tree/branch/path/to/subdir`
- `github.com/owner/repo` (no protocol)
- `git@github.com:owner/repo.git` (SSH)

Extract `owner` and `repo` from the URL — you'll use `repo` as the default
plugin name (kebab-case, lowercase). If no valid URL, ask the user.

Sanitize the repo name: only `a-z`, `0-9`, and hyphens. Strip anything else.

## Step 2: Fetch the repository

```bash
FETCH_JSON=$(bash "${CLAUDE_PLUGIN_ROOT}/skills/skills-load/scripts/fetch-repo.sh" "<github-url>" "<branch-if-any>")
```

`fetch-repo.sh` outputs JSON with four fields: `path`, `branch`, `subpath`, `sha`.
Parse them all — `path` is needed for skill discovery, the other three are carried
through to the plugin manifest as source provenance so `/skills-update` can later
refresh against the SAME branch and do fast-path SHA comparisons.

```bash
REPO_PATH=$(echo "$FETCH_JSON" | python3 -c "import json,sys; print(json.load(sys.stdin)['path'])")
BRANCH=$(echo "$FETCH_JSON"    | python3 -c "import json,sys; print(json.load(sys.stdin)['branch'])")
SUBPATH=$(echo "$FETCH_JSON"   | python3 -c "import json,sys; print(json.load(sys.stdin)['subpath'])")
SHA=$(echo "$FETCH_JSON"       | python3 -c "import json,sys; print(json.load(sys.stdin)['sha'])")
```

On failure, suggest checking the URL and access.

## Step 3: Discover skills

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/skills-load/scripts/discover-skills.sh" "<repo-path>"
```

Returns JSON: `[{name, description, path, fullPath}, ...]`

If empty: "No SKILL.md files found in this repository."

Show a compact numbered catalog:

> **Found {N} skills in `owner/repo`:**
>
> | # | Skill | Description |
> |---|-------|-------------|
> | 1 | discovery-process | Run a structured product discovery process... |
> | 2 | roadmap-planning | Build quarterly roadmaps with dependency mapping... |
>
> Pick by number (`1, 3`), name, keyword search (`"research"`), or `all`.

Wait for the user to choose before proceeding.

## Step 4: Resolve dependencies

Read each selected SKILL.md and scan the body for references to OTHER skills in
the catalog. A dependency exists when:

- The body mentions another skill's path (e.g., `skills/discovery-process/SKILL.md`)
- The body names another skill as a prerequisite, protocol, or input
  (e.g., "Use insights from discovery-process", "see workshop-facilitation for",
  "requires competitive-analysis")
- The body contains a relative reference like `../other-skill/SKILL.md`

For each dependency found that isn't already selected, add it automatically and
tell the user: "`roadmap-planning` references `discovery-process` — including it."

Resolve transitively (dependencies of dependencies). Track processed skills to
avoid circular loops.

This matters because skills in a repo are often designed as a connected system.
Installing one without its dependencies means the model will reference skills
that don't exist.

## Step 5: Check for already-installed skills

Before building the plugin, check whether any of the selected skills (user picks
+ resolved dependencies) are already installed in this session. Two sources:

**A. On-disk installed skills** — run:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/skills-load/scripts/check-installed.sh"
```

Returns a JSON array of skill names present in the SkillsPlugin registry,
domain plugins, and remote plugins.

**B. Conversation-loaded skills** — scan THIS conversation for any
`### LOADED SKILL: {name}` headers from earlier `/skills-load` runs. Those
skills are already active in context.

**Compare both lists against the selected skills.** If any overlap:

> **Already installed — skipping by default:**
>
> | Skill | Where it came from |
> |-------|-------------------|
> | `roadmap-planning` | Already in `/` menu (SkillsPlugin) |
> | `discovery-process` | Loaded earlier this conversation |
>
> These will be **excluded** from the new plugin. Reply "replace" to include
> them anyway (will overwrite the existing versions), or "proceed" to continue
> with only the new skills.

Wait for the user's response. Default is **skip duplicates** — the user has to
explicitly say "replace" to include them. If all selected skills are already
installed, tell the user there's nothing to do and suggest running the command
without those skills, or loading a different repo.

## Step 6: Build and present the plugin

### A. Read all selected SKILL.md files

Use the Read tool with each skill's `fullPath`. Capture the complete content.

### B. Build a unified .plugin file

Package ALL selected skills (plus dependencies) as a single `.plugin` ZIP.
The ZIP must have this structure:

```
{repo-name}/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    ├── discovery-process/
    │   ├── SKILL.md
    │   └── references/        (if any supporting files exist)
    ├── roadmap-planning/
    │   └── SKILL.md
    └── competitive-analysis/
        └── SKILL.md
```

Build it with Bash + Python:

```bash
python3 << 'PYEOF'
import zipfile, json, os, re, datetime, glob

# ── Substitute these values from the /skills-load context ──
owner = "<OWNER>"            # e.g., "deanpeters"
repo = "<REPO>"              # e.g., "Product-Manager-Skills"
repo_name = "<REPO_NAME>"    # e.g., "product-manager-skills" (kebab-case)
branch = "<BRANCH>"          # e.g., "main" or "develop"
subpath = "<SUBPATH>"        # e.g., "" or "skills/pm-stuff"
sha = "<SHA>"                # commit SHA or empty string
skill_dirs = [<SKILL_DIRS>]  # e.g., ["/tmp/tmp.abc/repo/skills/roadmap", ...]

# Cowork outputs dir lives at /sessions/<session>/mnt/outputs/ — discover it.
out_dirs = glob.glob('/sessions/*/mnt/outputs')
if not out_dirs:
    raise RuntimeError("Cowork outputs dir not found - is this a Cowork VM session?")
out_dir = out_dirs[0]
out = os.path.join(out_dir, repo_name + '.plugin')

installed_at = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Write plugin manifest (includes source provenance)
    manifest = json.dumps({
        "name": repo_name,
        "description": f"Skills loaded from {owner}/{repo}",
        "version": "1.0.0",
        "author": {"name": "skills-toolkit"},
        "repository": f"https://github.com/{owner}/{repo}",
        "source": {
            "branch": branch,
            "subpath": subpath,
            "sha": sha,
            "installedAt": installed_at
        },
        "keywords": ["skills", "skills-toolkit", repo_name]
    }, indent=2)
    zf.writestr(f".claude-plugin/plugin.json", manifest)

    # Write each skill
    for skill_path in skill_dirs:
        skill_name = os.path.basename(skill_path)
        skill_name = re.sub(r'[^a-zA-Z0-9_-]', '-', skill_name).strip('-')
        for root, dirs, files in os.walk(skill_path):
            for f in files:
                fp = os.path.join(root, f)
                arc = "skills/" + skill_name + "/" + os.path.relpath(fp, skill_path)
                if f == 'SKILL.md':
                    with open(fp, 'r', encoding='utf-8') as fh:
                        content = fh.read()
                    # Cowork user-upload rejects SKILL.md > ~12,900 bytes.
                    # Truncate long description fields to fit.
                    if len(content.encode('utf-8')) > 12800:
                        lines = content.split('\n')
                        fm_end = next((i for i in range(1, len(lines)) if lines[i].strip() == '---'), -1)
                        if fm_end > 0:
                            ds = next((i for i in range(1, fm_end) if lines[i].startswith('description')), -1)
                            if ds >= 0:
                                de = next((i for i in range(ds+1, fm_end) if lines[i] and not lines[i][0].isspace()), fm_end)
                                desc = '\n'.join(lines[ds:de])
                                trim = len(content.encode('utf-8')) - 12800 + 100
                                if len(desc) > trim + 80:
                                    short = desc[:len(desc)-trim]
                                    cut = short.rfind(' ')
                                    if cut > 50: short = short[:cut]
                                    lines = lines[:ds] + [short] + lines[de:]
                                    content = '\n'.join(lines)
                                    print(f'  [!] Truncated {skill_name}/SKILL.md description to fit 12.8KB limit', flush=True)
                    zf.writestr(arc, content)
                else:
                    zf.write(fp, arc)

print(out)
PYEOF
```

Substitute actual values into the `<PLACEHOLDER>` slots above. The assistant
fills in `owner`, `repo`, `repo_name`, `branch`, `subpath`, `sha`, and
`skill_dirs` from earlier steps. `skill_dirs` is a Python list of quoted path
strings. The repo name should be kebab-case (e.g., `Product-Manager-Skills` →
`product-manager-skills`). The `source` object lets `/skills-update` later
refresh against the same branch and use SHA for a fast "no changes" check.

### C. Present the .plugin file to Cowork

Load `mcp__cowork__present_files` via ToolSearch, then call it with this exact
shape — `files` is a list of objects, each with a single `file_path` key:

```
mcp__cowork__present_files(files=[{"file_path": "<output-path-from-python>"}])
```

The path MUST be the Linux path printed by the Python script above (under
`/sessions/<session>/mnt/outputs/`). Windows-style paths and `/outputs/` paths
are rejected.

Cowork renders a rich preview of the plugin and the user clicks **"Save plugin"**
to install. All skills appear in the `/` menu immediately, mid-session.

### D. Inject into conversation

Output each skill's full content so it's usable immediately:

```
### LOADED SKILL: {skill-name}

**Description:** {description}

{Full SKILL.md body — do NOT truncate}

---
```

Include ALL skills — both user-selected and auto-resolved dependencies. Present
dependencies first, then the skills that reference them.

## Step 7: Report

> **Plugin `{repo-name}` ready** — {N} skills (including {M} dependencies):
>
> | Skill | Why |
> |-------|-----|
> | discovery-process | Dependency of roadmap-planning |
> | roadmap-planning | Selected |
> | competitive-analysis | Selected |
>
> **Click "Save plugin"** on the plugin preview above to install all skills at once.
> They'll appear in your `/` menu immediately.
>
> Skills are already active in this conversation — try them by name.
>
> Want to load more skills from this repo, or from a different one?

## Step 8: Follow-up

Keep the temp repo directory alive for loading more skills from the same catalog.

If the user wants more skills from the same repo, add them to the existing
plugin and rebuild the `.plugin` file. Present the updated version.

Clean up only when loading a different repo, the user says they're done, or the
conversation ends.

## Edge cases

- **present_files unavailable**: Skills are still injected into context (usable
  by name). The `.plugin` file is at the path printed by the build script
  inside the VM — tell the user it's there, or write it to the host via the
  Write tool so they can upload manually via Customize > Personal Plugin.
- **Name conflict with existing plugin**: Warn the user. Saving the plugin will
  replace the existing plugin with the same name.
- **MCP servers in repo**: Note that `.mcp.json` configs need separate setup and
  can't be loaded mid-session.
- **Large repos (>10 skills)**: Warn before loading all. Suggest a focused subset.
- **Single skill with no dependencies**: Still package as a `.plugin` for
  consistency. The one-click Save plugin flow works the same way.
