---
name: skills-save
description: >
  Save the current in-conversation version of loaded skills as a new plugin.
  Use when the user says "save these skills", "save my iterated skills", "save
  loaded", "package what I've been working on", "save this as a plugin",
  "install what I loaded", "I forgot to click save plugin", or runs
  /skills-save. Captures the CURRENT state from this conversation — iterated
  versions if any, originals otherwise. For fetching from GitHub, use
  /skills-load instead.
argument-hint: "[plugin-name]"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
  - Grep
---

# Save Loaded Skills as a New Plugin

Package the skills loaded in THIS conversation as a fresh `.plugin` file —
either the iterated versions (if you modified them), or the originals (if you
loaded but never clicked Save plugin). The saved plugin reflects the current
in-context state.

**This saves what `/skills-load` brought in.** To fetch skills from GitHub,
use `/skills-load`. To refresh installed plugins from their GitHub sources,
use `/skills-update`. To package already-installed skills for sharing, use
`/skills-share`.

## When to use this

- You ran `/skills-load <github-url>` and iterated one or more skills — save the iterated versions
- You ran `/skills-load <github-url>` but never clicked Save plugin — save it now so you can install with one click
- You want a named snapshot of the current in-context skill state

## How it works

Skills loaded via `/skills-load` are injected into the conversation as
`### LOADED SKILL: {name}` blocks. This skill gathers skills from two sources
unconditionally — (A) conversation markers, which preserve any iterations, and
(B) already-installed `skills-toolkit` plugins on disk — then cross-references
them to pick the right action: save iterations, install a load that was never
saved, save originals post-compaction, or report nothing to do. The result is
packaged as a `.plugin` file presented for install via Cowork's "Save plugin" button.

## Step 1: Discover loaded skills (two sources)

Skills can come from two sources. Gather from BOTH, then decide which to use.

### Source A: Conversation markers (primary — captures iterations)

Find all `### LOADED SKILL: {name}` markers in this conversation. For each
marker, extract:
- The skill name (from the header)
- The description (from the `**Description:**` line)
- The body content (everything until the next `---` separator or next
  `### LOADED SKILL:` block)

This source preserves any iterations you made during the conversation. It's
the happy path when conversation context is intact.

### Source B: Installed plugins on disk

Run the discovery script to find skills-toolkit plugins already installed in
this Cowork session:

```bash
bash "${CLAUDE_PLUGIN_ROOT}/skills/skills-save/scripts/discover-installed-plugins.sh"
```

Returns a JSON array of `{pluginName, pluginRoot, manifestPath, skills: [{name, path, currentSha}]}`.
The script already filters for the `skills-toolkit` keyword and excludes plugins
tagged `iterated` (those are already saved).

### Cross-reference

For each Source B plugin, check whether ALL of its skill names appear in
Source A's marker set. A full match means Source A's load was previously
saved as that installed plugin. If no plugin matches the Source A skills,
the user loaded but never clicked Save plugin.

**Never claim a plugin is installed without running Source B.** The
discovery script is the only ground truth. Do not infer from context that
the user clicked Save plugin — that's a hallucination.

### Decide by case

**Case A — markers present, matching installed plugin, some skills iterated.**
Use markers. Go to Step 2 to synthesize iterations. Save as `iterated-{name}`
with the `iterated` keyword.

**Case B — markers present, matching installed plugin, nothing iterated.**
Tell the user:

> **Already saved as `{pluginName}`** ({N} skills, all unchanged).
> Nothing new to save. Reply `snapshot` to save anyway as a separate copy.

Wait. If `snapshot`, proceed with the Case A flow (iterated-* naming).
Otherwise stop.

**Case C — markers present, NO matching installed plugin (never clicked Save plugin).**
Tell the user:

> **Not installed yet.** These skills came from `/skills-load` but Save plugin
> wasn't clicked. I can package them as `{repo-name}` now so you can install
> with one click. `/skills-update` will refresh them from upstream later.
>
> Plugin name? (default: `{repo-name}`)

After user confirms the name, go to Step 2 (in case they iterated despite not
installing). In Step 4, use `{repo-name}` with NO `iterated-` prefix. In Step 5,
DROP the `iterated` keyword AND include the `repository` field (find the
`https://github.com/...` URL from the earlier `/skills-load` output in this
conversation).

**Case D — markers empty, installed plugins found (post-compaction fallback).**
Warn the user before proceeding:

> **Conversation markers not found — likely compacted.** Falling back to
> `{N}` skills-toolkit plugins installed on disk. This saves the **originals**
> as an `iterated-*` plugin; any iterations from this conversation are NOT
> captured (the edit history was in the compacted span).
>
> Found:
> - `{pluginName-1}` ({M1} skills)
> - `{pluginName-2}` ({M2} skills)
>
> Save originals as `iterated-*` plugins? Reply `yes`, pick plugin names, or `cancel`.

If confirmed, for each chosen plugin read every `{skill.path}/SKILL.md` from
disk. Skip Step 2's synthesis. Go to Step 3.

**Case E — both empty.**

> **No skills to save.** No conversation markers AND no skills-toolkit plugins
> installed on disk.
>
> Run `/skills-load <github-url>` first.

Stop.

## Step 2: Synthesize current state (Source A only)

**Skip this step entirely if Step 1 chose Source B** — those are originals
read from disk. They don't need synthesis.

For each Source A skill (from conversation markers), examine the conversation
holistically to determine its CURRENT state:

- If the skill was discussed/modified/iterated on after the initial injection
  (e.g., user said "add a step for X", "reword the intro", "make it more
  concise"), produce the updated version that reflects those changes
- If the skill was not modified, use the original injected content verbatim

Track which skills were iterated and summarize what changed (high level —
not a full diff, just enough for the user to confirm).

## Step 3: Show the summary

Display a compact table with a Source column so the user can tell which
skills came from conversation markers vs. the installed-plugin fallback:

> **Found {N} skills to save:**
>
> | # | Skill | Source | Status | Notes |
> |---|-------|--------|--------|-------|
> | 1 | roadmap-planning | conversation | iterated | Added stakeholder-review step |
> | 2 | discovery-process | conversation | unchanged | — |
> | 3 | competitive-analysis | conversation | iterated | Reworded intro, added 2 criteria |
> | 4 | positioning-workshop | conversation | unchanged | — |
>
> Save all {N} as a new plugin? Reply with a plugin name, `all`, or pick
> by number (`1, 3`).

When all skills come from Source B, the Source column shows `installed plugin`
and the Status column shows `original` for every row (no iterations to display).

## Step 4: Parse user response and plugin name

- Empty / `all` / `yes` → include all loaded skills
- Comma-separated numbers → include only selected
- Plugin name string → include all, use this as plugin name

**Plugin name default** depends on the Step 1 case:

- **Cases A, B (snapshot), D**: `iterated-{repo-name}` (e.g.,
  `iterated-product-manager-skills`). Fallback if no repo known: `iterated-skills`.
- **Case C** (never installed): `{repo-name}` — no `iterated-` prefix, because
  this IS the plugin, not an iteration of one. Fallback: `skills-from-conversation`.

Sanitize the plugin name: kebab-case, `[a-z0-9-]` only. Reject empty names
and re-ask.

## Step 5: Build the .plugin file

Build the `.plugin` ZIP via Python inside the VM. Pass skill content as JSON
(the content came from conversation markers in Source A, or from disk reads
in Source B — the build step doesn't care which):

```bash
python3 << 'PYEOF'
import zipfile, json, os, glob

# ── Substitute these values from the /skills-save context ──
plugin_name = "<PLUGIN_NAME>"   # e.g., "iterated-product-manager-skills" or "geo-seo-claude"
skills_json = '<SKILLS_JSON>'   # JSON: [{"name": "...", "body": "..."}, ...]
is_iterated = <TRUE_OR_FALSE>   # True for Cases A/B/D, False for Case C
repository  = "<REPO_URL>"      # Case C: "https://github.com/owner/repo"; others: ""

# Cowork outputs dir lives at /sessions/<session>/mnt/outputs/ — discover it.
out_dirs = glob.glob('/sessions/*/mnt/outputs')
if not out_dirs:
    raise RuntimeError("Cowork outputs dir not found - is this a Cowork VM session?")
out_dir = out_dirs[0]
out = os.path.join(out_dir, plugin_name + '.plugin')

skills = json.loads(skills_json)

keywords = ["skills", "skills-toolkit", plugin_name]
if is_iterated:
    keywords.insert(2, "iterated")  # tells /skills-update to skip

manifest_dict = {
    "name": plugin_name,
    "description": "Skills saved from Cowork session",
    "version": "1.0.0",
    "author": {"name": "skills-toolkit"},
    "keywords": keywords,
}
if repository:
    manifest_dict["repository"] = repository  # Case C only — lets /skills-update refresh from upstream

with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as zf:
    zf.writestr(".claude-plugin/plugin.json", json.dumps(manifest_dict, indent=2))
    for skill in skills:
        zf.writestr(f"skills/{skill['name']}/SKILL.md", skill['body'])

print(out)
PYEOF
```

Substitute actual values into the `<PLACEHOLDER>` slots above. `skills_json`
is a JSON-encoded string of `[{"name": "...", "body": "..."}, ...]`.
`is_iterated` is Python `True` for Cases A/B/D, `False` for Case C.
`repository` is the GitHub URL for Case C, empty string for others.

**Case C manifest:** no `iterated` keyword, includes `repository` field.
`/skills-update` will later find it via the `skills-toolkit` keyword and
refresh it from the repo URL, same pattern as a fresh `/skills-load`.

**All other cases:** `iterated` keyword is present, no `repository` field —
tells `/skills-update` to skip these (they have no upstream).

## Step 6: Present the .plugin file to Cowork

Load `mcp__cowork__present_files` via ToolSearch, then call it with this exact
shape — `files` is a list of objects, each with a single `file_path` key:

```
mcp__cowork__present_files(files=[{"file_path": "<output-path-from-python>"}])
```

The path MUST be the Linux path printed by the Python script above (under
`/sessions/<session>/mnt/outputs/`). Windows-style paths and `/outputs/` paths
are rejected.

Cowork renders a rich preview with a **"Save plugin"** button. Clicking it
installs the iterated plugin — distinct from the original GitHub-sourced
plugin (they have different names if you used the default `iterated-*`
prefix).

## Step 7: Re-inject into conversation

Output the saved skills back into conversation so they remain accessible
by name:

```
### LOADED SKILL: {skill-name}

**Description:** {description}

{Full synthesized body — do NOT truncate}

---
```

This keeps them usable immediately, even before the user clicks Save plugin.

## Step 8: Report

> **Plugin `{plugin-name}` ready** — {N} skills saved:
>
> | Skill | Status |
> |-------|--------|
> | roadmap-planning | iterated |
> | discovery-process | unchanged (kept original) |
> | competitive-analysis | iterated |
>
> **Click "Save plugin"** on the preview above to install. The skills will
> appear in your `/` menu immediately.
>
> If an original `/skills-load` plugin is already installed, it stays
> untouched — this saves AS A SEPARATE PLUGIN named `{plugin-name}`.

If all skills came from Source B (installed-plugin fallback), add this note:

> **Heads-up:** This plugin was built from the originals on disk because
> conversation markers were lost to compaction. To capture iterations next
> time, run `/skills-save` before the conversation gets long enough to
> compact — or redo your edits in a fresh conversation after reloading with
> `/skills-load`.

## Edge cases

- **No `### LOADED SKILL:` markers in conversation**: Go to Step 1's Case D
  (installed plugins on disk) or Case E (both empty). No plugin is built in
  Case E.
- **Markers present but Source A's skills don't fully match ANY installed plugin**:
  Case C — user never clicked Save plugin for this load. Offer to install
  via `/skills-save` with no `iterated-` prefix.
- **Multiple `/skills-load` runs from different repos**: Show a single
  table listing ALL found skills across sources. Let the user pick which
  to save. Offer "iterated-mixed" as a default name if sources differ.
- **Name collision with existing plugin**: If `{plugin-name}` matches an
  installed plugin, warn the user — Save plugin will replace it. Suggest
  a unique name or confirm the replace.
- **Iteration detection unclear**: Default to the most recent version
  discussed. If unsure, use the original injected content and flag as
  "unchanged (could not detect iteration)" in the table.
- **`present_files` unavailable**: Still re-inject into context (Step 7).
  Tell the user the `.plugin` file is at the path printed by the build script
  in the VM, or write it to the host via the Write tool for manual upload.
- **Single loaded skill**: Still package as a `.plugin` for consistency.
  The Save plugin flow works the same way.
