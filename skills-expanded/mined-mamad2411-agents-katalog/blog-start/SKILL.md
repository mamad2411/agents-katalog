---
name: blog-start
description: |
  This skill should be used when the user runs /4d-blog-engine:blog-start or asks any variant of "open my blog project," "resume my blog work," "start a blog session," "what's in progress on the blog," or "load the blog plugin." It locates the user's blog-project-instructions.md marker file, mounts the two declared directories (blog project + GitHub repo), surfaces in-progress and unpublished pieces, and proposes the next step. Do NOT use this skill for: first-time setup (use /4d-blog-engine:blog-init), running the pipeline (use /4d-blog-engine:blog-pipeline), or publishing (use /4d-blog-engine:blog-publish).
allowed-tools: [Read, Glob, Grep, Bash, AskUserQuestion]
---

# Blog-Start — open or resume a blog session

> **Read this when:** the user runs `/4d-blog-engine:blog-start`. Your job is to find the marker file, mount the two directories, surface state, and propose the next action.

## STEP 1 — Find the blog-project-instructions.md marker

Walk up from the current working directory looking for `blog-project-instructions.md` at any ancestor's root. Use Bash:

```bash
find_blog_project() {
  local d="$PWD"
  while [ "$d" != "/" ]; do
    if [ -f "$d/blog-project-instructions.md" ]; then
      echo "$d"
      return 0
    fi
    d="$(dirname "$d")"
  done
  echo ""
  return 1
}
BLOG_PROJECT_DIR=$(find_blog_project)
```

If the walk finds nothing, also check the standard fallback locations (in order):

1. `~/Documents/MyBlog/blog-project-instructions.md`
2. `~/Blog/blog-project-instructions.md`
3. `$HOME/4d-blog-engine-work/blog-project-instructions.md`

If still nothing, halt with:

> *No blog project found. I walked up from the current directory and checked the standard locations but didn't find a `blog-project-instructions.md` file. Run `/4d-blog-engine:blog-init` first to set up your blog project.*

If exactly one is found, proceed. If multiple are found at different fallback locations, ask the user which to use via `AskUserQuestion`.

## STEP 2 — Read the marker file

Read `<BLOG_PROJECT_DIR>/blog-project-instructions.md` in full. Extract from the "Project Setup" section:

- `BLOG_PROJECT_DIR` (confirm matches the walk's result)
- `GITHUB_REPO_DIR`
- `POSTS_SUBFOLDER`
- `IMAGES_SUBFOLDER`
- `LIVE_URL_PATTERN`
- `AUTHOR_NAME`

If the file's schema version (`schema:` field in frontmatter) is unknown to this plugin version, warn the user but proceed with best-effort parsing.

## STEP 3 — Mount both directories in Cowork

The whole point of mounting both directories at session start is that **`/blog-publish` shouldn't have to do this mid-flow**. The writer should never see "Cowork is requesting access to X" right in the middle of a publish confirmation. So this step is load-bearing.

Use the Cowork directory-mount tool (`mcp__cowork__request_cowork_directory`) once for each path, even if you think they're already mounted:

1. `BLOG_PROJECT_DIR` — where pieces live
2. `PUBLISHING_REPO_DIR` — where the publish skill writes finished posts

The tool is idempotent — if the path is already mounted, it reports that and continues without prompting. If a mount fails (the writer dismissed the dialog or the path no longer exists), surface a clear one-line note in the briefing so they can fix it before publish time, not during.

After mounting, verify each path is actually reachable:

```bash
ls "$BLOG_PROJECT_DIR" >/dev/null 2>&1 && echo "blog_ok"
ls "$PUBLISHING_REPO_DIR/.git" >/dev/null 2>&1 && echo "repo_ok"
```

Capture both states. Use them in STEP 5's briefing display. If `PUBLISHING_REPO_DIR` isn't reachable, note "Publishing repo not mounted — `/blog-publish` will mount it on demand, but resolve now to avoid mid-flow friction" in the briefing.

If running outside Cowork (e.g., Claude Code CLI), the file tools (Read/Write/Edit/Glob/Grep) already have host-level access — the mount step is a no-op there. Detect this gracefully: if the mount tool isn't available, skip it and continue.

## STEP 3.5 — Voice file inventory

Glob `<BLOG_PROJECT_DIR>/*-voice.md` to enumerate voice files. The set determines what's shown to the writer:

- **Zero voice files:** flag this in the briefing. The pipeline can't write a post without a voice profile. The "What to do next" prompt should lead with *"Run `/4d-blog-engine:blog-voice` to capture your voice."*
- **One voice file:** record its path as `SELECTED_VOICE_FILE` silently. Mention it on a single line in the briefing as the active voice. No question asked.
- **Two or more voice files:** list them in the briefing with the author name pulled from each file's frontmatter, but do not auto-pick. The "What to do next" prompt for a `/blog` action will ask which voice to use at that point (the orchestrator handles this at pipeline STEP 0). This skill just surfaces the available voices.

Capture the count and the author-name list in `VOICE_FILES_AVAILABLE` for use in STEP 5.

## STEP 3.7 — Scan uploads for dropped files (new-post ingest)

After mounting and voice resolution, scan the session's uploads folder for files the writer dragged into Cowork chat during this session. The uploads folder is read-only to the plugin; copy what we need to the right places in the blog project folder.

```bash
# Resolve the uploads dir from the session — actual path varies, but it's
# /sessions/<session-id>/mnt/uploads in the sandbox. List its contents.
UPLOADS_DIR=$(ls -d /sessions/*/mnt/uploads 2>/dev/null | head -1)

if [ -n "$UPLOADS_DIR" ] && [ -d "$UPLOADS_DIR" ]; then
  # Group by type
  MARKDOWN_UPLOADS=$(find "$UPLOADS_DIR" -maxdepth 1 -type f -iname "*.md" 2>/dev/null)
  OTHER_UPLOADS=$(find "$UPLOADS_DIR" -maxdepth 1 -type f ! -iname "*.md" ! -name ".*" 2>/dev/null)
fi
```

Classification:

- **No uploads:** skip to STEP 4. Don't mention it in the briefing.
- **Markdown upload(s) only, no media:** treat each markdown as a potential new-post base-doc. Surface in STEP 6's briefing.
- **Markdown + media:** the new-post-with-media intent. Surface in STEP 6 with a "start a new post?" option (priority placement).
- **Media only, no markdown:** likely the writer is adding attachments to an existing in-progress piece. Surface in STEP 6 as "<N> media files uploaded — add to which piece?" with the in-progress pieces as options. If no in-progress pieces, ask whether to just copy them to `drafts/blog-media/` for later use.

For markdown uploads, check whether each file is already a base-doc for an in-progress piece (look at `Posts/<slug>/01-delegation.md`'s recorded `base_doc:` path). If it matches an existing piece, deduplicate — don't offer to start a new post from a file that's already in flight.

Store the classification in `UPLOAD_INTENT` for STEP 6 to use:

- `UPLOAD_INTENT.kind` = `"none" | "new-post" | "media-only" | "markdown-only"`
- `UPLOAD_INTENT.markdown_files` = list of (path, basename) tuples
- `UPLOAD_INTENT.media_files` = list of (path, basename) tuples

### When the writer accepts "start a new post"

Copy the media files (only) to `<BLOG_PROJECT_DIR>/drafts/blog-media/<basename>`. Use `mkdir -p` to ensure the folder exists. Do NOT copy the markdown — the orchestrator reads it once at Phase 1 directly from the uploads path; copying it would litter `drafts/` with unsigned drafts.

After the copy, hand off to the orchestrator: invoke `/4d-blog-engine:blog-pipeline <markdown-uploads-path>`. The orchestrator's Phase 2 will scan `drafts/blog-media/` and ask the writer for a caption for each newly-arrived file.

### When the writer accepts "add media to an existing piece"

Same media copy to `<BLOG_PROJECT_DIR>/drafts/blog-media/<basename>`. Then tell the writer: *"Media files copied. When you next run `/4d-blog-engine:blog-describe` (or resume Phase 2) on `<slug>`, the pipeline will ask you to caption each new file. Or, if Phase 4 is already signed, edit `drafts/<slug>.md` directly to add a `media:` YAML entry before `/blog-publish`."*

## STEP 4 — Scan for in-progress pieces

List `<BLOG_PROJECT_DIR>/Posts/`. For each piece subdirectory:

```bash
ls -1 "<BLOG_PROJECT_DIR>/Posts/" 2>/dev/null
```

For each piece, read `<piece>/state.md` if present. Capture:

- `slug` (from frontmatter)
- `title` (from frontmatter)
- `current_phase` (01 / 02 / 03 / 04 / done)
- `gates_passed` (list)
- Last modification timestamp of `state.md`

Bucket the pieces into three categories:

- **In-progress** — `gates_passed` does not include `04` (Phase 4 not yet signed)
- **Signed but not yet published** — `04` is in `gates_passed`, AND `<piece>/04-diligence/blog.md` exists, AND there's NO file at `<GITHUB_REPO_DIR>/<POSTS_SUBFOLDER>/<slug>.md` (check with Glob)
- **Published** — `04` in `gates_passed`, AND the post file exists in the GitHub repo

Sort each bucket by `state.md` mtime descending (most recent first).

## STEP 5 — Display the briefing

Compose a structured briefing to the user. Skip empty sections.

```
Blog session ready.

Project:               <BLOG_PROJECT_DIR>
Publishing repo:       <PUBLISHING_REPO_DIR>
Live URL pattern:      <LIVE_URL_PATTERN or "(not set)">
Default author:        <AUTHOR_NAME>

Voices available:
  <If 0 voice files:>
    None yet — run /4d-blog-engine:blog-voice before /blog.
  <If 1 voice file:>
    • <author-name-from-frontmatter> (<filename>)
  <If 2+ voice files:>
    • <author-1> (<filename-1>)
    • <author-2> (<filename-2>)
    ... (the pipeline will ask which voice to use when you start writing)

In-progress pieces (most recent first):
  • <slug-1>  —  Phase <N>, gates passed [<list>]  —  last touched <date>
  • <slug-2>  —  …
  (or "None")

Signed but not yet published:
  • <slug-3>  —  signed <date>
  (or "None")

Recently published (last 5):
  • <slug-4>  —  in <GITHUB_REPO_DIR>/<POSTS_SUBFOLDER>/<slug-4>.md
  (or "None")
```

## STEP 6 — Propose the next step

Use `AskUserQuestion` with options pulled from the briefing in this priority order:

1. **If `UPLOAD_INTENT.kind == "new-post"`:** lead with *"Start a new post from your uploads (`<draft.md>` + `<N>` media files)."* This is the highest priority because the writer explicitly just dropped files and almost certainly wants to act on them. Route this option to STEP 3.7's "start a new post" handler (copy media, invoke `/blog`).
2. **If `UPLOAD_INTENT.kind == "markdown-only"`:** offer *"Start a new post from `<draft.md>`."*
3. **If `UPLOAD_INTENT.kind == "media-only"` and there's an in-progress piece:** offer *"Add the `<N>` uploaded media file(s) to `<most-recent-in-progress-slug>`."*
4. **If `UPLOAD_INTENT.kind == "media-only"` and no in-progress piece:** offer *"Copy the `<N>` uploaded media files to `drafts/blog-media/` for later use."*
5. **If signed-but-not-published exists:** *"Publish `<most-recent-signed-slug>` to your live site"* (runs `/4d-blog-engine:blog-publish <slug>`).
6. **If in-progress exists:** *"Resume `<most-recent-in-progress-slug>` at Phase <N>"* (runs the appropriate phase command).
7. **Always:** *"Start a new piece"* (prompts for a base doc, then runs `/4d-blog-engine:blog-pipeline`).
8. **Always:** *"Just looking — exit"*.

Cap the question at four options. Upload-intent options take precedence over publish/resume because the writer's most-recent action was the upload — surface what they just did first.

## STEP 7 — Hand off

When the user picks, route to the appropriate command. For publish, format the invocation: `/4d-blog-engine:blog-publish <slug>`. For resume, route to the matching phase command. For new, prompt for the base doc path and then call `/4d-blog-engine:blog-pipeline`.

If the user picks "just looking — exit," report cleanly and stop.

## What this skill does NOT do

- It does not write any files. Read-only briefing.
- It does not run the discovery walk that the orchestrator skill (`4d-blog-engine`) uses during pipeline runs. That walk is in the orchestrator's STEP 1. This skill uses a simpler walk because at session-start the user hasn't necessarily told us a piece slug yet.
- It does not validate the GitHub repo. That's `/blog-publish`'s job at publish time.

## Degradation behaviors

- **`Posts/` directory missing entirely:** report "No `Posts/` directory yet — your first `/4d-blog-engine:blog-pipeline` run will create it." Then go straight to the "start a new piece" prompt.
- **A piece directory has no `state.md`:** skip it silently. Likely an aborted run; the user can clean up manually.
- **GitHub repo path is invalid or moved:** report the failure, recommend re-running `/4d-blog-engine:blog-init` to update paths. Don't halt the briefing — in-progress writing work can continue without the repo being reachable.
- **The mount tool isn't available** (CLI-only environment): silently skip the mount step. The file tools already have host access there.
