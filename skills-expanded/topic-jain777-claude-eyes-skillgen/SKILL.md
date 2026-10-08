---
name: skillgen
description: Watch a tutorial or demo video and scaffold a runnable Claude Code skill from it. Use when the user wants to turn a how-to video, screencast, or tool demo into an invocable skill or plugin.
argument-hint: "<tutorial-url-or-path> [skill-name]"
allowed-tools: Bash, Read, Write, AskUserQuestion
user-invocable: true
---

# /skillgen — turn a tutorial video into a Claude Code skill

The user gives you a tutorial video. You watch it (via the `/see` pipeline
with the `tutorial` profile + OCR), then synthesize a working Claude Code
skill from what was demonstrated. The skill scaffolder owns the file layout
and frontmatter; you own the synthesis (workflow identification, commands,
prose).

## Step 0 — Silent preflight

```bash
"${CLAUDE_PLUGIN_ROOT}"/scripts/setup.py --check --quiet
```

Same exit-code table as `/claude-eyes:see`. If a key is missing AND the user
didn't pass `--transcript`, Whisper will be unavailable for tutorials without
captions — many tutorials DO have captions, so it's often fine to proceed.

## Step 1 — Parse user input

```
/claude-eyes:skillgen <video-url-or-path> [skill-name] [--ask "…"] [--start T --end T]
```

- **source** — first positional arg. URL or path.
- **skill-name** — second positional arg. Optional; if missing, derive one
  from the video title later. Must be valid as a directory name; the script
  normalizes it.
- `--ask "…"` — optional clarifying question to focus extraction.
- `--start` / `--end` — pass through if user wants to scope to one section.

## Step 2 — Watch the video

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/skillgen.py" "<source>" \
    [--name "<skill-name>"] \
    [--ask "<question>"] \
    [--start T --end T] \
    [--transcript PATH]
```

This runs `/see` internally with `--profile tutorial --ocr` and appends a
**handoff template** to the report. Read the report, then follow the
template's instructions verbatim — it tells you exactly what to extract from
the OCR + transcript + frames.

## Step 3 — Read the evidence

The report's `## Frames` section lists JPEGs and (because OCR ran) `.txt`
siblings. The handoff template instructs:

- **Read every `.txt` first** — they're cheap. Most tutorial content
  (commands, code, file paths, UI labels) is text. The transcript explains
  the WHY; OCR captures the WHAT.
- Only `Read` JPEGs when OCR was empty for a frame OR when the synthesis
  needs a visual (a UI screenshot in the README, e.g.).

## Step 4 — Synthesize

Before writing anything, answer these in your head:

| Question | Where to find the answer |
|---|---|
| What ONE workflow does the video demonstrate? | Transcript + OCR overview |
| When should Claude invoke this skill in future? | The first sentence of the description |
| What's the input? URL? Path? Free text? | What the demo's user types first |
| What tools does the skill need? | Bash for shell commands; Read for files; Write for generated artifacts; AskUserQuestion for choices |
| What EXACT commands does the video run? | OCR of terminal frames — verbatim |

A skill that tries to do everything in the video does nothing well. If the
video covers three workflows, ask the user via `AskUserQuestion` which one to
generate; or generate the most prominent one and tell them you skipped the
others.

## Step 5 — Write the SKILL.md body

Write the body to a temp file using the Write tool. **No frontmatter** — the
scaffold adds it. Match the structure of well-written skills (the `see` skill
in this plugin is a good template):

```markdown
# {{name}} — {{one-line purpose}}

## When to use
- {{trigger sentences}}

## How to invoke

**Step 1 — {{what to parse from user input}}**

**Step 2 — run the command(s) demonstrated in the tutorial:**

```bash
{{exact-command-from-OCR}}
```

**Step 3 — {{what to do with output}}**

## Failure modes
- {{x}} → {{action}}
```

Style guidelines:
- Action-oriented, no "I will now…" filler.
- Specific exit codes → specific remediation tables.
- Verbatim commands from OCR (don't paraphrase shell syntax).
- Cite timestamps from the original tutorial in `<!-- comments -->` so the
  user can audit your synthesis.

## Step 6 — Scaffold

Once the body file is written:

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/skillgen.py" --scaffold \
    --name "<skill-name>" \
    --description "<one-line description for frontmatter>" \
    --argument-hint "<e.g. \"<input> [flag]\">" \
    --allowed-tools "Bash, Read, Write" \
    --body-file "<path-to-body-you-wrote>" \
    [--dest "<custom-dir>"] \
    [--plugin-name "<plugin-name>"] \
    [--overwrite]
```

Default destination is `${CLAUDE_PLUGIN_DATA}/generated/<plugin-name>/`. The
script prints the final SKILL.md path and the exact `/plugin install`
command. **DO NOT install the plugin yourself** — show the install command
to the user so they can review the generated SKILL.md first.

If the destination already has a SKILL.md for this name, the script exits 3.
Either pass `--overwrite` (if user confirms), or pick a different name —
use `AskUserQuestion` to ask the user which.

## Step 7 — Hand off

Tell the user:
1. The generated SKILL.md path.
2. A one-line summary of what the skill does.
3. The exact `/plugin install <path>` command.
4. If you made tradeoffs (skipped a workflow, simplified a step), say so.
5. If a wrapper script was warranted but you didn't create one, mention it.

## When to propose a wrapper script

If the tutorial demonstrates a multi-step bash workflow (≥4 commands or
nontrivial piping), the skill is cleaner with a single wrapper rather than
inlining every command. Ask the user via `AskUserQuestion` whether to:

- **Inline the commands** in the SKILL.md (good for ≤3 simple commands).
- **Generate a wrapper script** at `<dest>/scripts/<name>.sh` that the SKILL.md
  invokes via `"${CLAUDE_PLUGIN_ROOT}"/scripts/<name>.sh "$@"`.

If wrapper is chosen, Write it before calling `--scaffold`.

## Failure modes

- **Video too long / dense** → tell the user, suggest they pass `--start --end`
  scoping the most representative section.
- **OCR text mostly garbage** (low-resolution screencast) → re-run `/see` part
  with `--resolution 768` to improve OCR; the rest of skillgen flow is unchanged.
- **Workflow ambiguous** → ask the user via `AskUserQuestion`. Don't guess.
- **Scaffold exit 3 (file exists)** → ask the user to pick a different name OR
  confirm overwrite.

## Security & permissions

Inherits everything from `/see` (yt-dlp, ffmpeg, optional Whisper API). Adds:
- Writes a new SKILL.md and `plugin.json` to `${CLAUDE_PLUGIN_DATA}/generated/`
  (or to a user-specified `--dest`).
- Never installs the generated plugin automatically — that's a user action.
