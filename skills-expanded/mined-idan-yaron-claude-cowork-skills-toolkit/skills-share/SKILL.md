---
name: skills-share
description: >
  Package skills already installed in your Cowork session as a downloadable
  .zip file you can save to disk and share. Use when user says "share my
  skills", "export installed skills", "download my skills", "send these
  skills to a colleague", "package skills for sharing", or runs /skills-share.
  This is for exporting skills you ALREADY have — to get skills from a GitHub
  repo, use /skills-load instead.
argument-hint: "[skill-name... | --all]"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Glob
  - Grep
---

# Share Installed Skills

Export one or more **already-installed** skills as a downloadable `.zip` file.
The user downloads it via the Cowork preview and saves it wherever they want —
Desktop, Documents, a project folder, Slack, email attachment.

**This skill does NOT install the exported plugin back into Cowork.** The
skills are already installed. The `.zip` format deliberately avoids the
"Save plugin"/"Save skill" install prompts that `.plugin`/`.skill` extensions
trigger — the user gets a standard file download instead.

**This skill is for exporting what you already have.** To get new skills from
a GitHub repo, use `/skills-load`.

## VM constraints (why we use the session outputs folder and .zip)

The Cowork VM has a fixed set of mount points. None of them is the user's
Desktop or an arbitrary host path — the Write tool cannot reach
`~/Desktop/anything` unless the user has explicitly mounted that folder.

What DOES work: `/sessions/<session>/mnt/outputs/` is a VM→host bridge mount.
Files written there are surfaced in the Cowork UI by `mcp__cowork__present_files`.
A `.zip` file presented this way gives the user a download button — they save
it wherever they want via their OS file picker.

- **Bash** runs in the VM — use it to enumerate installed skills AND build
  the ZIP entirely inside the VM.
- **Read tool** can read from VM-mounted skill directories (not used in the
  new flow — Bash+Python reads files directly).
- **Write tool** bridges to the host but only where mounts exist — NOT used
  in this skill.
- **`mcp__cowork__present_files`** surfaces the built ZIP for download.

## When to use this vs /skills-load

| Situation | Use |
|-----------|-----|
| "I found a repo with skills I want" | `/skills-load <url>` |
| "I want to send skills from my session to a colleague" | `/skills-share` |
| "I want to archive the skills I use" | `/skills-share` |
| "I want to hand off skills whose GitHub source is gone" | `/skills-share` |

## Step 1: Enumerate installed skills

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/skills-share/scripts/list-installed-skills.sh"
```

Returns JSON array of `{name, description, path, source}` objects where
`source` is one of `skills-plugin`, `domain-plugin`, or `remote-plugin`.

If the array is empty:

> **No skills installed in this session.**
>
> Use `/skills-load <github-url>` to install skills from a repo first.

Then stop.

## Step 2: Show the catalog

Display a numbered table:

> **Installed skills in this session ({N} total):**
>
> | # | Skill | Description | Source |
> |---|-------|-------------|--------|
> | 1 | pdf | PDF processing toolkit | skills-plugin |
> | 2 | xlsx | Excel spreadsheet handling | skills-plugin |
> | 3 | roadmap-planning | Build quarterly roadmaps... | domain-plugin |
> | 4 | discovery-process | Run product discovery... | domain-plugin |
>
> Which to include? Pick by number (`1, 3`), name, keyword search
> (`"roadmap"`), or `--all`.

If `$ARGUMENTS` contains skill names or `--all`, use those directly. Otherwise
wait for the user to choose.

Also ask for a package name:

> **Package name?** (default: `shared-skills`)

Don't ask where to save — the user will choose that when they download the
`.zip` from the preview.

## Step 3: Confirm selection (with dependency warning)

Before building, show what will be packaged:

> **Will package:**
>
> | Skill | Source |
> |-------|--------|
> | roadmap-planning | domain-plugin |
> | discovery-process | domain-plugin |

**Warn about missing cross-references (do not auto-include):** Read each
selected SKILL.md and scan for references to OTHER installed skills not in
the selection. If found:

> **Note:** `roadmap-planning` references `competitive-analysis` (installed
> but not selected). The shared plugin may point to a skill the recipient
> doesn't have. Include it? (y/n)

User stays in control. Skills-share is a packaging tool, not a curator.

## Step 4: Build the .zip inside the VM

Sanitize the package name: kebab-case, `[a-z0-9-]` only. Reject and re-ask if
sanitizing produces an empty string.

Build the ZIP entirely in Bash+Python. All file reading happens inside the VM
— no content passes through Claude's context.

```bash
python3 << 'PYEOF'
import zipfile, json, os, re, glob

# ── Substitute these values from the /skills-share context ──
pkg_name = "<PKG_NAME>"       # e.g., "my-shared-skills"
skill_paths = [<SKILL_PATHS>] # e.g., ["/path/to/skill-a", "/path/to/skill-b"]

# Cowork outputs dir lives at /sessions/<session>/mnt/outputs/ — discover it.
out_dirs = glob.glob('/sessions/*/mnt/outputs')
if not out_dirs:
    raise RuntimeError("Cowork outputs dir not found - is this a Cowork VM session?")
out_dir = out_dirs[0]
out_path = os.path.join(out_dir, pkg_name + '.zip')

with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    # Plugin manifest
    manifest = json.dumps({
        "name": pkg_name,
        "description": "Skills exported from Cowork session",
        "version": "1.0.0",
        "author": {"name": "Exported by skills-toolkit"},
        "keywords": ["skills", "shared", pkg_name]
    }, indent=2)
    zf.writestr(".claude-plugin/plugin.json", manifest)

    # Copy each skill's full directory tree
    for skill_path in skill_paths:
        if not os.path.isdir(skill_path):
            continue
        skill_name = os.path.basename(skill_path)
        skill_name = re.sub(r'[^a-zA-Z0-9_-]', '-', skill_name).strip('-')
        for root, dirs, files in os.walk(skill_path):
            for f in files:
                fp = os.path.join(root, f)
                rel = os.path.relpath(fp, skill_path)
                arc = "skills/" + skill_name + "/" + rel.replace('\\', '/')
                zf.write(fp, arc)

print(out_path)
PYEOF
```

Substitute actual values into the `<PLACEHOLDER>` slots above. `skill_paths`
is a Python list of quoted path strings. Capture the output path printed by
the script.

**Why `.zip` not `.plugin`:** presenting a `.plugin` file via `present_files`
triggers Cowork's "Save plugin" install button, which is wrong here — the user
already has these skills installed. `.zip` surfaces as a plain download, and
it's still directly accepted by Customize > Personal Plugin on the receiving end.

**Why the session outputs folder, not `/tmp/`:** `/sessions/<session>/mnt/outputs/`
is a VM→host bridge mount that `present_files` surfaces in the Cowork UI.
`/tmp/` is VM-only.

## Step 5: Present the .zip for download

Load `mcp__cowork__present_files` via ToolSearch, then call it with this exact
shape — `files` is a list of objects, each with a single `file_path` key:

```
mcp__cowork__present_files(files=[{"file_path": "<zip-path-from-python>"}])
```

The path MUST be the Linux path printed by the Python script in step 4 (under
`/sessions/<session>/mnt/outputs/`). Windows-style paths and `/outputs/` paths
are rejected.

The Cowork UI shows a download action. The user clicks it, picks a location
with their OS file picker (Desktop, Documents, anywhere), and the file lands
on their host. No mount configuration needed, no manual zipping.

## Step 6: Report

> **`{pkg-name}.zip` ready to download** — {N} skills packaged:
>
> | Skill | Source |
> |-------|--------|
> | roadmap-planning | domain-plugin |
> | discovery-process | domain-plugin |
>
> **Download** the `.zip` from the preview above. Save it wherever you want.
>
> **To use/share it:**
> - **Send to a colleague**: Email, Slack, or attach the `.zip` directly.
> - **Install in Cowork**: Customize > Personal Plugin (+) > Create plugin > Upload plugin (accepts
>   `.zip` directly — no renaming needed).
> - **Use with Claude Code CLI**: Extract the `.zip`, then
>   `claude --plugin-dir ./{pkg-name}/`

## Edge cases

- **No skills installed**: Exit with a suggestion to run `/skills-load` first.
- **Skill with only SKILL.md (no supporting files)**: Works fine — the ZIP
  just contains the manifest and one SKILL.md.
- **User picks skills from multiple sources**: Fine, all get bundled together.
  Note mixed sources in the report.
- **Sanitized name empty**: If the package name sanitizes to nothing, ask for
  a new name.
- **Binary supporting files** (fonts, images, etc.): Bash+Python copies them
  correctly into the ZIP — no content passes through Claude. This is an
  advantage of the VM-build approach.
- **`present_files` unavailable**: Tell the user the file is at
  `/sessions/<session>/mnt/outputs/{pkg-name}.zip` in the VM. The session
  outputs folder maps to Cowork's app data on the host — on Windows that's
  `%APPDATA%\Claude\local-agent-mode-sessions\...`, on macOS it's
  `~/Library/Application Support/Claude/local-agent-mode-sessions/...`.
