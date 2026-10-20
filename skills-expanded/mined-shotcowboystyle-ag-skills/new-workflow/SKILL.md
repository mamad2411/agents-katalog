---
name: new-workflow
description: Scaffold a multi-touchpoint image workflow inside the registered image workspace — a structured pipeline with explicit human review gates and optional cloud-AI generation/edit steps (Fal nano-banana via MCP). Use when the user says "new image workflow", "scaffold a workflow", "set up an image pipeline", "iterative image project", or describes a job that needs multiple rounds of generation → review → revision → export.
allowed-tools: Bash(test *), Bash(mkdir *), Bash(echo *), Bash(seq *), Bash(git init:*), Bash(git rev-parse:*), Bash(date *), Bash(jq *), Bash(sed *), Bash(file *), Bash(curl *), Read, Write, Edit
---

# New Image Workflow

Scaffold a structured, multi-stage image workflow inside the user's registered image workspace. Unlike `new-project` (a flat source/working/exports layout), a workflow expects **iteration**: generation, human review, revision, and export are explicit stages, each with their own folder and manifest entry.

Cloud AI (Fal nano-banana via a `nano-tech-diagrams` MCP server) is wired in as an optional driver for the generation and revision stages. That server is **not** shipped with this plugin — see the `nano-tech-diagrams` skill for what the user has to configure. If it is not available, scaffold the workflow with driver `none` and say so; the folder structure and review gates are useful on their own.

## When to use this vs. new-project

- **`new-project`** — single batch of images, photo-editing style, no iteration loop.
- **`new-workflow`** — generative or hybrid work with multiple touchpoints: brief → references → generate → review → revise → export. Use when the user expects to come back to the project across several sessions and wants a stable structure to resume into.

## Procedure

### 1. Resolve the workspace

```bash
CONFIG="${CLAUDE_USER_DATA:-${XDG_DATA_HOME:-$HOME/.local/share}/claude-plugins}/image-ops/workspace.json"
test -f "$CONFIG" || { echo "No workspace registered — run workspace-setup first."; exit 1; }
WS=$(jq -r .path "$CONFIG" 2>/dev/null) \
  || WS=$(sed -n 's/.*"path"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$CONFIG")
test -d "$WS" || { echo "Workspace path missing: $WS — run workspace-setup."; exit 1; }
```

The `sed` fallback covers a host without `jq`; `grep -oP` would not, since macOS ships BSD grep with no PCRE support.

### 2. Gather workflow metadata

Ask (or infer if obvious):

- **Name** — required. Slugify (lowercase, hyphens).
- **Brief** — one or two sentences describing the deliverable.
- **Cloud-AI driver** — `fal-nano-banana` if a nano-tech-diagrams MCP server is configured in this session, otherwise `none`. Also use `none` when the user is bringing their own images. Resolve the actual tool namespace from the tools available in session rather than assuming a server name.
- **Expected rounds** — how many revision cycles to scaffold (default 3).
- **Final aspect ratio / resolution** — for export-stage placeholders.

### 3. Create the layout

```bash
PROJ="$WS/$slug"
test -e "$PROJ" && { echo "Already exists: $PROJ"; exit 1; }
mkdir -p "$PROJ"/{01-brief,02-references,03-generation,04-review,05-revision,06-export,_manifest} \
  || { echo "Could not create $PROJ — check permissions on $WS"; exit 1; }

# Brace expansion happens before variable expansion, so `round-{1..$ROUNDS}`
# would create one literal directory named `round-{1..$ROUNDS}`. Loop instead.
for i in $(seq 1 "$ROUNDS"); do
  mkdir -p "$PROJ/05-revision/round-$i"
done
```

| Stage              | Purpose                                                                 | Touchpoint? |
|--------------------|-------------------------------------------------------------------------|:-----------:|
| `01-brief/`        | `brief.md` — goal, audience, constraints, do/don't list                 | ✓ user      |
| `02-references/`   | Mood board, reference images, prompt fragments                          | ✓ user      |
| `03-generation/`   | First-pass generations (Fal output lives here)                          | ai          |
| `04-review/`       | Selected candidates from `03-generation/` + review notes                | ✓ user      |
| `05-revision/`     | Per-round sub-folders with revised generations + notes                   | ai + user   |
| `06-export/`       | Final deliverables — sized, formatted, metadata-scrubbed                | ai          |
| `_manifest/`       | `workflow.json` — pipeline state; `prompts.md` — running prompt log     | ai          |

### 4. Write the manifest

`$PROJ/_manifest/workflow.json`:

```json
{
  "slug": "<slug>",
  "created": "<ISO date>",
  "brief": "<one-line summary>",
  "driver": "fal-nano-banana | none",
  "stages": [
    {"id": "01-brief",       "status": "pending", "type": "human"},
    {"id": "02-references",  "status": "pending", "type": "human"},
    {"id": "03-generation",  "status": "pending", "type": "ai"},
    {"id": "04-review",      "status": "pending", "type": "human"},
    {"id": "05-revision",    "status": "pending", "type": "ai+human", "rounds": <ROUNDS>, "current_round": 0},
    {"id": "06-export",      "status": "pending", "type": "ai"}
  ],
  "final": {"aspect_ratio": "<...>", "resolution": "1K", "format": "png"}
}
```

### 5. Seed templates

- `01-brief/brief.md` — markdown template with sections: Goal, Audience, Deliverables, Constraints, Do, Don't, Reference Links.
- `_manifest/prompts.md` — append-only log; one heading per generation call with the prompt, model params, and resulting filenames.
- `README.md` at project root — slug, brief, driver, ISO date, stage checklist (mirrors `workflow.json`), and a "Resume here" pointer to the first non-`done` stage.

### 6. (Optional) git init

If the workspace itself is a git repo (check `git -C "$WS" rev-parse --git-dir`), the new workflow is automatically tracked — no separate init. Otherwise, ask whether to `git init` the project folder.

### 7. Confirm and hand off

Report:
- Project path
- Current stage (`01-brief`)
- Next action (open `01-brief/brief.md` and fill in)

## Driving the workflow

Subsequent sessions resume by reading `_manifest/workflow.json` and continuing from the first stage with `status != "done"`.

### Cloud AI generation (stage 03 + 05)

When the active stage is `ai`-typed and the driver is `fal-nano-banana`:

1. Read the brief + references; compose a dense one-paragraph prompt — concrete subject, composition, style, and palette in a single paragraph, no bullet lists.
2. Call the server's `text_to_image` tool with `resolution: "1K"` and the configured aspect ratio. For revision rounds that build on a prior image, use `image_to_image` and pass the selected candidate. Use whatever namespace the configured server exposes (the `nano-tech-diagrams` skill covers staging local files for a remote server).
3. Download the returned `fal.media` URL into the stage folder:
   ```bash
   out="$PROJ/03-generation/$(date +%s)-$slug.png"
   curl -fsSL -o "$out" "$fal_url" \
     || { echo "download failed — the fal.media URL may have expired" >&2; exit 1; }
   file "$out"
   ```
   `-f` is what makes this safe: without it curl exits 0 on an HTTP error and writes the error page to disk as a `.png`, which then gets logged as a generated candidate. Verify with `file` before recording it.
4. Append a log entry to `_manifest/prompts.md`: stage, round, prompt, params, output filename.
5. Mark the stage `awaiting-review` in `workflow.json` and surface the candidates to the user.

### Human touchpoints (stage 01, 02, 04, 05-review)

At each human stage, **stop and prompt the user**. Do not auto-advance. Show:
- What was just produced (file list, thumbnails if available)
- The decision needed (which candidates to keep, what to change, etc.)
- Where to record the decision (a `notes.md` in the stage folder)

After the user records the decision, mark the stage `done` and advance.

### Export (stage 06)

When all revision rounds are `done`:

1. Take the selected final images from the last `05-revision/round-N/` folder.
2. Apply: resize to target resolution, convert to target format, scrub metadata — via the `fast-resize`, `convert-to-avif`, `optimize-jpeg`, and `scrub-metadata` skills, or `web-ready` to do all of it in one pass.
3. Write to `06-export/` with stable filenames (`<slug>-<variant>.<ext>`).
4. Mark stage `done`.

## Notes

- Don't overwrite existing files in `03-generation/` or `05-revision/round-*/` — always timestamp-prefix.
- The manifest is the source of truth; the README is a human-readable mirror, regenerate it from the manifest when state changes.
- If the user changes the driver mid-flow (e.g., switches from cloud-AI to bringing their own), update `workflow.json` and note it in `prompts.md`.
