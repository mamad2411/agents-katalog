---
name: articulate
description: >
  Content creation pipeline orchestrator for any AI agent. Chains great-writer ->
  brilliant-visualizer -> typeset -> deliver into a complete write-to-deliver flow.
  Optional multi-platform publishing via /publish skill (superb-publisher).
  Loose coupling: depends only on skill names and I/O contracts, not sub-skill internals.
  Works with Claude Code, Codex, Gemini CLI, and any agent that supports skill loading.
triggers:
  # Chinese
  - 一键发文
  - 写文章并排版
  - 从头写一篇
  - 写完整文章
  - 全流程写作
  - 内容流水线
  - 多平台发布
  - 跨平台发文
  # English
  - articulate
  - content pipeline
  - write and publish
  - full article
  - end to end article
  - cross post
  - multi platform publish
---

# Crisp Articulator -- Content Creation Pipeline

Orchestrator for the content creation flow. Chains sub-skills, does not do content work itself.

```
write (great-writer) -> illustrate (brilliant-visualizer) -> format (typeset) -> deliver (built-in) -> [publish (/publish skill)]
```

Brackets indicate optional/conditional stages. The Publish stage requires `--publish` flag and delegates entirely to the `/publish` skill (superb-publisher).

**Loose coupling contract:** This skill knows sub-skill names and their I/O types (file paths). It does NOT read or depend on any sub-skill's internal files, modes, phases, engines, or themes.

---

## Step 0: Dependency Check + Auto-Install

Before executing, verify that all dependency skills are available. Missing skills are auto-installed from GitHub.

The skill directory varies by agent platform:

| Agent | Typical skill directory |
|-------|----------------------|
| Claude Code | `~/.claude/skills/` |
| Codex | `~/.agents/skills/` |
| Gemini CLI | `~/.gemini/skills/` |
| Other | Check agent documentation |

### Dependency Registry

All dependencies are declared here. To add a new skill to the pipeline, add one row — the check engine handles the rest.

<!-- DEPENDENCY_REGISTRY_START -->
| Skill name | GitHub repo | Policy | Stage | Post-install |
|------------|------------|--------|-------|-------------|
| `great-writer` | `d-wwei/great-writer` | required | Write | — |
| `typeset` | `d-wwei/excellent-typesetter` | required | Typeset | — |
| `brilliant-visualizer` | `d-wwei/brilliant-visualizer` | optional | Visualize | — |
| `superb-publisher` | `d-wwei/superb-publisher` | optional | Publish | `npm install` |
<!-- DEPENDENCY_REGISTRY_END -->

**Policy values:**
- `required` — pipeline cannot run without it. Auto-install; if still missing, STOP.
- `optional` — skip the corresponding stage if missing. Auto-install; if still missing, warn and continue.

**Post-install:** extra command to run after `git clone` (e.g., `npm install` for skills with native dependencies). Leave `—` for none.

### Generic check engine

The script below reads from the registry above. It does not hardcode any skill name — extending the pipeline means editing only the registry table.

```bash
SKILL_DIR="${SKILL_DIR:-$HOME/.claude/skills}"
_AVAILABLE="" _MISSING="" _INSTALLED=""

# Generic: check one skill, auto-install if missing
_resolve() {
  _name="$1"; _repo="$2"; _policy="$3"; _postinstall="$4"
  if [ -f "$SKILL_DIR/$_name/SKILL.md" ]; then
    _AVAILABLE="$_AVAILABLE $_name"
    echo "OK: $_name"
    return 0
  fi
  echo "MISSING: $_name — auto-installing..."
  if ! command -v git >/dev/null 2>&1; then
    echo "FAILED: git not available"
    _MISSING="$_MISSING $_name"
    return 1
  fi
  git clone --depth 1 "https://github.com/$_repo.git" "$SKILL_DIR/$_name" 2>/dev/null
  if [ ! -f "$SKILL_DIR/$_name/SKILL.md" ]; then
    echo "FAILED: clone failed for $_name"
    _MISSING="$_MISSING $_name"
    return 1
  fi
  echo "INSTALLED: $_name (from $_repo)"
  _INSTALLED="$_INSTALLED $_name"
  _AVAILABLE="$_AVAILABLE $_name"
  # Post-install hook
  if [ "$_postinstall" != "-" ] && [ -n "$_postinstall" ]; then
    echo "  Running post-install: $_postinstall"
    (cd "$SKILL_DIR/$_name" && eval "$_postinstall" 2>/dev/null)
  fi
  return 0
}

# ── Read from registry (mirror the table above) ──
_resolve "great-writer"          "d-wwei/great-writer"          "required" "-"
_resolve "typeset"               "d-wwei/excellent-typesetter"  "required" "-"
_resolve "brilliant-visualizer"  "d-wwei/brilliant-visualizer"  "optional" "-"
_resolve "superb-publisher"      "d-wwei/superb-publisher"      "optional" "npm install --silent"

echo ""
echo "AVAILABLE:$_AVAILABLE"
[ -n "$_INSTALLED" ] && echo "AUTO-INSTALLED:$_INSTALLED"
[ -n "$_MISSING" ] && echo "STILL MISSING:$_MISSING"
```

### Interpret the results

- **All available** (including auto-installed): proceed normally.
- **Required skill still missing** after auto-install: STOP. Show: `"{skill} is required. Manual install: git clone https://github.com/{repo}.git $SKILL_DIR/{skill}"`.
- **Optional skill still missing**: warn that the corresponding stage will be skipped. Continue with remaining stages.
- To check dependencies without running the pipeline: use `--check-deps` flag.

### Adding a new dependency

1. Add a row to the **Dependency Registry** table above.
2. Add the matching `_resolve` call in the bash block (same 4 values).
3. Wire the new skill into a pipeline stage in Step 2.
4. Done — no other changes needed.

---

## Step 1: Parse Input and Detect Entry Point

Parse the user's `/articulate` invocation to determine:
1. **What to write about** (topic text or existing file path)
2. **Where to start** (which pipeline stage)
3. **How to run** (gated or auto mode)
4. **Target platform and theme** (for typeset stage)

### Command syntax

```
/articulate <topic_or_file> [--from write|visualize|typeset|deliver|publish] [--auto] [--platform PLATFORM] [--theme default|elegant|tech|minimal|vibrant] [--publish] [--title T] [--author A] [--digest D] [--thumb F] [--publish-args "..."] [--check-deps]
```

Multi-platform: `--platform wechat,medium,x` (comma-separated, passed through to /publish).

### Argument extraction

From the user's input, extract these parameters:

| Parameter | Source | Default |
|-----------|--------|---------|
| `TOPIC_OR_FILE` | First positional argument | (required) |
| `FROM_STAGE` | `--from` flag value | (auto-detect) |
| `AUTO_MODE` | Presence of `--auto` | false |
| `PLATFORM` | `--platform` flag value (can be comma-separated) | wechat |
| `THEME` | `--theme` flag value | default |
| `PUBLISH` | Presence of `--publish` | false |
| `TITLE` | `--title` flag value | (auto-extract from HTML/Markdown) |
| `AUTHOR` | `--author` flag value | (empty) |
| `DIGEST` | `--digest` flag value | (auto-extract from first paragraph) |
| `THUMB_FILE` | `--thumb` flag value | (none) |
| `PUBLISH_ARGS` | `--publish-args` flag value | (none) |

If `--platform` is not specified, ask the user: "Target platform? (default: wechat)"

If `--check-deps` is present, run only the dependency check from Step 0 and stop.

### Entry point detection

If `--from` is specified, use that stage directly. Otherwise, auto-detect:

**Rule 1: Input is a `.md` file path (file exists on disk)**
- Read the file. Check if it contains image references matching `![...](images/...)` or `![...](./images/...)`.
- If image references exist AND at least one referenced image file exists on disk:
  -> Start at **Typeset** (article already has illustrations)
- If no image references, or referenced images don't exist:
  -> Start at **Visualize** (article needs illustrations)

**Rule 2: Input is a `.html` file path (file exists on disk)**
- Start at **Deliver** (just preview and copy)

**Rule 3: Input is plain text (not an existing file path)**
- Start at **Write** (create article from scratch)

**Rule 4: Input is a `.md` file path but file doesn't exist**
- Treat as topic text. Start at **Write**.

**Rule 5: `--from publish` specified**
- Input must be an existing `.html` file. Set `HTML_PATH = TOPIC_OR_FILE`.
- If input is not a valid `.html` file, show error: "Publish stage requires an HTML file path as input."
- Implies `--publish` (no need to set both).

After detection, announce: "Starting pipeline from [stage name]. Remaining stages: [list]."

Also check: if the detected start stage requires a sub-skill that is missing (from Step 0), skip forward to the next available stage. Warn the user.

---

## Step 2: Execute Pipeline

Execute stages in order from the detected entry point. Each stage follows the same pattern:
1. Check if the sub-skill is available (from Step 0 results)
2. Invoke the sub-skill using your agent's skill invocation mechanism
3. Collect the output artifact (file path)
4. Run the stage gate (unless `AUTO_MODE` is true)
5. Pass the artifact to the next stage

---

### Stage: Write

**Skill:** `great-writer`
**Input:** Topic text from `TOPIC_OR_FILE` + writing type (inferred from topic or platform context)
**Output:** Markdown file path

**Invocation:** Invoke the `great-writer` skill with the user's topic as argument. Pass the topic text directly. Example argument:

```
"写一篇关于 AI Agent 安全的技术博客"
```

Let great-writer handle its own internal pipeline. Do not interfere with or reference its internal phases.

**After completion:** great-writer will produce a Markdown file. Note the file path as `MD_PATH` for the next stage.

**Gate (if not AUTO_MODE):**
Show the user:
```
Write stage complete.
  File: {MD_PATH}
  Words: ~{word_count}

Continue to illustration? (Y: continue / n: stop here / edit: pause for manual edits)
```

If user says "n", output the current artifact path and stop the pipeline.
If user says "edit", tell the user to edit the file and say "done" when ready, then continue.
If user says "Y" or presses enter, continue to the next stage.

---

### Stage: Visualize

**Skill:** `brilliant-visualizer`
**Input:** Markdown file path (`MD_PATH` from Write stage or from user input)
**Output:** Markdown file path (same file, now with image references)

**Skip condition:** If `brilliant-visualizer` is not installed (from Step 0), skip this stage. Warn the user: "brilliant-visualizer not installed, skipping illustration stage." Set `ILLUSTRATED_MD_PATH` = `MD_PATH` and continue to the next stage.

**Mid-pipeline entry:** If the pipeline starts at this stage via `--from visualize` or auto-detection, set `MD_PATH` = `TOPIC_OR_FILE` (the user-provided file path).

**Invocation:** Invoke the `brilliant-visualizer` skill with the markdown file path as argument:

```
"{MD_PATH}"
```

Let brilliant-visualizer handle its own analysis, plan confirmation, and generation. Do not interfere with its engine selection or internal workflow.

**After completion:** The Markdown file now contains image references. The file path may be the same as the input. Note the (possibly updated) path as `ILLUSTRATED_MD_PATH`.

**Gate (if not AUTO_MODE):**
Show the user:
```
Illustration stage complete.
  File: {ILLUSTRATED_MD_PATH}
  Images added: {count} (check the images/ directory)

Continue to typesetting? (Y: continue / n: stop here / edit: pause for manual edits)
```

Same gate behavior as Write stage.

---

### Stage: Typeset

**Skill:** `typeset`
**Input:** Markdown file path (`ILLUSTRATED_MD_PATH`) + `--platform {PLATFORM}` + `--theme {THEME}`
**Output:** HTML file path

**Mid-pipeline entry:** If the pipeline starts at this stage via `--from typeset` or auto-detection, set `ILLUSTRATED_MD_PATH` = `TOPIC_OR_FILE` (the user-provided file path). If `TOPIC_OR_FILE` is not a valid file path, show an error: "Typeset stage requires a Markdown file path as input."

**Invocation:** Invoke the `typeset` skill with the markdown path and platform/theme parameters as argument:

```
"{ILLUSTRATED_MD_PATH} --platform {PLATFORM} --theme {THEME}"
```

Let typeset handle its own rendering, platform-specific constraints, and theme application. Do not interfere with its internal logic.

**After completion:** typeset will produce an HTML file. Note the file path as `HTML_PATH`.

No gate after Typeset. Proceed directly to Deliver.

---

### Stage: Deliver (Built-in)

This stage is handled by the orchestrator directly. No sub-skill invocation.

**Input:** HTML file path (`HTML_PATH`)

**Actions:**

1. Copy rendered rich text to clipboard (NOT raw HTML source):

On macOS, use `NSPasteboard` to set clipboard content as `public.html` type. This allows rich text editors (WeChat, Zhihu, etc.) to receive rendered content instead of raw source code.

```bash
/usr/bin/python3 -c "
import AppKit
with open('{HTML_PATH}', 'r') as f:
    html = f.read()
pb = AppKit.NSPasteboard.generalPasteboard()
pb.clearContents()
pb.setData_forType_(html.encode('utf-8'), 'public.html')
print('Rich text copied to clipboard')
"
```

**Why not `cat | pbcopy`?** `pbcopy` copies as plain text (`public.utf8-plain-text`). When pasted into a rich text editor, it shows raw HTML tags instead of rendered content. Using `public.html` clipboard type tells the editor to interpret and render the HTML.

**Fallback** (if Python/AppKit unavailable): Open the HTML in a browser, then tell the user to Cmd+A -> Cmd+C from the browser preview.

2. Open HTML in default browser for preview:
```bash
open "{HTML_PATH}"
```

3. Print pipeline summary:

```
Pipeline complete!

  Source:    {TOPIC_OR_FILE}
  Article:  {ILLUSTRATED_MD_PATH}
  Output:   {HTML_PATH}
  Platform: {PLATFORM}
  Theme:    {THEME}
  Words:    ~{word_count}
  Images:   {image_count}

  Rich text copied to clipboard -- paste directly into editor.
  Preview opened in browser.

  Next: {next_hint}
```

Adjust the "Next" hint:
- Without `--publish`: "Cmd+V to paste into your platform's editor. Or re-run with --publish to publish via /publish skill."
- With `--publish`: "Continuing to publish stage..."

---

## Stage 5: Publish (optional, requires --publish)

Delegates to the `/publish` skill (superb-publisher).

This stage does NOT do platform routing or content adaptation itself.
It passes the deliverables from Stage 4 (Deliver) to /publish and lets
that skill handle everything.

### What to pass to /publish:
- `--platform`: from user's `--platform` argument
- `--title`: from the article title (extracted or user-provided)
- `--html`: the typeset HTML file (from Stage 3)
- `--images`: any illustration files (from Stage 2, if available)
- Any additional args from the user's `--publish-args`

### How to invoke:

For Claude Code:
  Use the Skill tool: `skill="publish", args="--platform <PLATFORM> --title <TITLE> --html <HTML_FILE> [--images ...] [additional publish-args]"`

For Codex:
  `activate_skill("publish", "--platform <PLATFORM> --title <TITLE> --html <HTML_FILE>")`

For Gemini CLI:
  `activate_skill("publish", args)`

For other agents:
  Invoke the publish skill per your platform's skill loading mechanism.

### Mid-pipeline entry:

If `--from publish`, set `HTML_PATH = TOPIC_OR_FILE`. Validate it is an existing `.html` file.
Pass `HTML_PATH` and the user's other arguments directly to /publish.

### On success:
Report which platform(s) published successfully and the URL(s) returned by /publish.

### On failure:
Report the error from /publish. Do not retry automatically. Let the user decide.

---

## Error Handling

| Scenario | Action |
|----------|--------|
| Sub-skill invocation fails or produces an error | Show the error. Ask user: "Retry this stage / Skip to next stage / Abort pipeline?" |
| Sub-skill completes but no output file found | Show error: "Expected output file not found after {stage} stage." Abort pipeline. |
| User says "n" at a stage gate | Output the current artifact path. Print partial summary. Stop. |
| `AUTO_MODE` + any error | Abort the entire pipeline. Print error summary with the last successful stage and its artifact. |
| Missing optional sub-skill at runtime | Skip that stage. Warn: "{skill} not installed, skipping {stage} stage." Continue to next. |
| Missing `typeset` at runtime | Abort: "typeset is required. Install it at ~/.claude/skills/typeset/ first." |
| Invalid `--from` value | Show valid options: write, visualize, typeset, deliver, publish. Ask user to correct. |
| Publish skill not found | "superb-publisher skill not installed. Install it to use --publish. See: https://github.com/d-wwei/superb-publisher" |
| Publish failed | Report error from /publish. Do not retry automatically. Let user decide. |

---

## Extension Slots (v2+)

The pipeline has two reserved extension points.

### Pre-Write Slot (upstream)

Position: Before the Write stage.
Purpose: Topic selection, content strategy, material gathering.
Status: Empty. No skill registered.

When a skill is registered here in a future version, the pipeline becomes:
```
[topic-scout] -> write -> illustrate -> format -> deliver -> [publish]
```

### Post-Deliver Slot (downstream)

Position: After the Deliver stage.
Purpose: Multi-platform publishing.
Status: **Active.** Delegates to the `/publish` skill (superb-publisher).

Current pipeline:
```
write -> illustrate -> format -> deliver -> [/publish]
```

To add new platforms, extend superb-publisher. The orchestrator does not need modification.
