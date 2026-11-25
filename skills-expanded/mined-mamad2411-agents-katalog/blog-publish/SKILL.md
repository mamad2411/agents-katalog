---
name: blog-publish
description: >
  Ships a Phase-4-signed post to the writer's blog. Use it for /4d-blog-engine:blog-publish or any
  variant of "publish this post", "ship the blog", "push the post to my site", "deploy the post".
  It takes the signed draft, applies the typographer's-quote transform (frontmatter and JSON-LD
  preserved verbatim), normalizes status to published, bumps dateModified, commits, and ships:
  it pushes as the moxywolf-agent app, opens and merges a pull request when the target's default
  branch is protected, pulls the local clone back, and reports done only when the live page shows
  the post with its hub link (BP-001). When LinkedIn derivatives are present it can
  optionally publish them through the writer's own logged-in browser, with an explicit
  confirmation before every irreversible action. Do not use it to run the pipeline. It refuses
  every unsigned post; there is no override.
allowed-tools: [Read, Write, Edit, Bash, AskUserQuestion, Glob, ToolSearch, mcp__cowork__request_cowork_directory, mcp__Claude_in_Chrome__tabs_context_mcp, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__browser_batch, mcp__Claude_in_Chrome__computer, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__form_input]
---

# Publish — ship a signed post to the writer's blog

## When this skill applies

This skill should be used when the user runs /4d-blog-engine:blog-publish or asks any variant of "publish this post," "ship the blog," "push the post to my site," "deploy the post," "get this on the live site." It takes a Phase-4-signed post (staged as a clean draft at <blog-project-dir>/drafts/<slug>.md by the sign-off step), applies a reliable typographer's-quote transform via scripts/smart_quotes.py (preserves YAML frontmatter and JSON-LD verbatim), normalizes status to published, bumps dateModified to today, and commits with an auto-generated Summary + Description, and ships it with scripts/ship.py: push as the moxywolf-agent app, a pull request merged on green checks when the default branch is protected, pull-back, and a live-page check for the hub link (BP-001). The local drafts/ folder is the draft state — there is no --draft flag and no content/draft/ folder in the publishing repo. /blog-publish always ships from drafts/ to content/blog/ with status=published. The writer types no git words and takes no manual step after saying go. Optionally, when LinkedIn derivatives are present, it can publish them to the channel chosen in /blog-social through Claude in Chrome running in the writer's own logged-in LinkedIn (opt-in, with an explicit confirmation before every irreversible publish). On a personal profile that's the feed Post plus its first comment; on a Company/Showcase Page it's the Article-led trio — Article first, then the teaser Post, then a first comment with the freshly-captured Article URL substituted in. After the post is live, an opt-in step can post a #general Slack @channel nudge asking the team to reshare it. Do NOT use this skill for: running the pipeline (use /4d-blog-engine:blog-pipeline), publishing an unsigned post (always refused), or pushing to anywhere other than the configured publishing repo.


> **Read this when:** the user runs `/4d-blog-engine:blog-publish [<slug>]`. Your job is to take a Phase-4-signed piece, copy its publication-ready files into the configured publishing repo with the typographer's-quote transform applied correctly, normalize status to `published`, and commit and ship it — without making the writer type a single git command and without the YAML-breaking quote bug. Then ship it with `scripts/ship.py` (push, pull request and merge when protected, pull-back, live check).

## Design principles (read first)

1. **The writer never writes a commit message, never picks a branch, never types a git command.** The plugin auto-generates the Summary and Description, creates the commit, and ships it. The writer's signature in `changelog.md` is the only approval publishing needs (BP-001).
2. **The plugin ships; the writer never pushes** (BP-001). `scripts/ship.py` pushes through gstack-execution's `agent_token.py`, so git on GitHub acts as the `moxywolf-agent` app (GA-005), never under a person's login. When the target descriptor says `default_branch_protected: true`, the commit goes on `publish/<SLUG>` and `ship.py merge` opens the pull request, waits for the descriptor's `required_checks`, merges pinned to the pushed head only when every one concluded success, and pulls the default branch back into the local clone. `ship.py verify-live` then fetches the live post and requires the hub link. Run git and `ship.py` from the device's macOS shell (Desktop Commander), because minting the app token needs GitHub's `/app` endpoints, which the cloud proxy refuses.
3. **Auto-generated commit messages.** Summary: `Publish: <title>` (≤72 chars). Description: a short structured body naming the files written, the status, and the slug. The writer never types either.
3. **The typographer's-quote transform is vendored, not improvised.** Use `scripts/smart_quotes.py` — it explicitly preserves YAML frontmatter and JSON-LD `<script>` blocks. Never write ad-hoc Python that touches the file's quote characters.
4. **The publishing repo must be reachable** — either mounted in the session so we can read `.git/config` to find the remote URL, or the writer supplies the remote URL directly. `blog-start` handles the mount; if missed, this skill mounts on demand.
5. **Source of truth is `<blog-project-dir>/drafts/<slug>.md`.** Phase 4 sign-off stages the signed post there as a clean writer-facing copy. `/blog-publish` reads from `drafts/`, applies the transform, commits to the GitHub repo's `content/blog/<slug>.md` with `status: published`. There is no `--draft` flag and no `content/draft/` folder in the publishing repo.

6. **The piece directory at `<blog-project-dir>/Posts/<slug>/` stays untouched.** Forensic archive (delegation, description, discernment, diligence artifacts).

7. **Byte-identical republish silently bumps `dateModified`.** Don't show the writer a dialog about "empty commit vs dateModified bump" — that's an implementation detail. Always pick: bump `dateModified` to today, transform, commit. Site rebuild fires from the real diff once `ship.py` pushes it.
5. **The post file in `<piece>/04-diligence/blog.md` is the source of truth.** Never re-edit it. The transform writes to the repo path; the source stays untouched.

## STEP 0 — Resolve the piece slug

If `$1` (the slug) was passed:

1. Verify `<BLOG_PROJECT_DIR>/Posts/<slug>/` exists.
2. Verify `<piece>/state.md` exists.

If `$1` was omitted:

1. Glob `<BLOG_PROJECT_DIR>/drafts/*.md` to enumerate signed-and-staged drafts.
2. Filter out drafts whose slug already exists in the publishing repo's posts folder (they've been published; you can still re-publish them by passing the slug explicitly).
3. **One unpublished candidate:** use it.
4. **Multiple candidates:** ask the user via `AskUserQuestion` which to publish.
5. **No candidates:** halt with: *"No drafts ready to publish. Sign a piece by completing Phase 4 first (`/4d-blog-engine:blog-diligence`) — that stages a clean copy to `<blog-project-dir>/drafts/<slug>.md`."*

Store as `SLUG` and `PIECE_DIR = <BLOG_PROJECT_DIR>/Posts/<SLUG>`.

## STEP 1 — Read project config

Locate `blog-project-instructions.md` (walk up from PIECE_DIR; fall back to `<BLOG_PROJECT_DIR>/blog-project-instructions.md`). If missing, halt with: *"No `blog-project-instructions.md` found. Run `/4d-blog-engine:blog-init` first."*

Read it and extract:

- `BLOG_PROJECT_DIR`
- `PUBLISHING_REPO_DIR`
- `LIVE_URL_PATTERN` (may be empty)
- `AUTHOR_NAME`

The writer's marker file does not pin subfolders (per v0.3.x writer-first design). Detect them from the repo's content layout at publish time.

**Conceptual model:** Phase 4 sign-off stages the signed post at `<blog-project-dir>/drafts/<slug>.md` — that's the writer-facing draft file (clean, single, easy to find). The writer reviews and refines there if needed. `/blog-publish` reads from `drafts/`, applies the transform, and ships to `content/blog/<slug>.md` in the publishing repo, status `published`. There's no `content/draft/` folder in the publishing repo and no `--draft` flag on `/blog-publish` — the local `drafts/` folder IS the draft state.

**The audit-trail tradeoff (explicit by design):** `drafts/<slug>.md` is editable. If the writer fixes a typo, a broken link, or a small phrasing tweak in `drafts/` after Phase 4 signed, that change ships when `/blog-publish` runs — and it does NOT propagate back to `Posts/<slug>/04-diligence/blog.md`. So the forensic archive shows "what the Release Owner Gate signed" and `drafts/` shows "what got published." For small polish, divergence is fine — the substantive content that passed the gate is still in the audit trail. For substantive edits, the framework's expectation is: go back to the pipeline, re-run Phase 3 or Phase 4, re-sign. Don't smuggle a structural rewrite past the gate through a post-sign-off `drafts/` edit.

```bash
# Posts folder — common static-site-generator conventions, priority order:
for posts_dir in "content/blog" "content/posts" "_posts" "src/content/blog" "src/content/posts" "posts"; do
  [ -d "$PUBLISHING_REPO_DIR/$posts_dir" ] && POSTS_SUBFOLDER="$posts_dir" && break
done

# Images (hero) folder:
for images_dir in "public/blog-hero" "public/images/blog" "static/images/blog" "assets/images/blog" "public/images" "static/images"; do
  [ -d "$PUBLISHING_REPO_DIR/$images_dir" ] && IMAGES_SUBFOLDER="$images_dir" && break
done

# Media folder (for non-hero attachments referenced via `media:` in YAML — spreadsheets, PDFs, audio, etc.):
for media_dir in "public/blog-media" "public/media/blog" "static/blog-media" "static/media/blog" "public/media" "static/media"; do
  [ -d "$PUBLISHING_REPO_DIR/$media_dir" ] && MEDIA_SUBFOLDER="$media_dir" && break
done

# Social derivatives folder (for the LinkedIn/Twitter/Facebook source-of-truth files produced by /blog-social):
for social_dir in "$POSTS_SUBFOLDER/social" "content/social" "social"; do
  [ -d "$PUBLISHING_REPO_DIR/$social_dir" ] && SOCIAL_SUBFOLDER="$social_dir" && break
done
# Default silently to <POSTS_SUBFOLDER>/social — the directory is created on first social publish.
[ -z "$SOCIAL_SUBFOLDER" ] && SOCIAL_SUBFOLDER="$POSTS_SUBFOLDER/social"
```

**Resolution rules:**

- **If posts and images subfolders detected:** proceed.
- **If either detection fails:** ask via `AskUserQuestion` for the missing one, with the conventional defaults as options plus a "Custom — type the path" fallback.
- **If `MEDIA_SUBFOLDER` detection fails (no media folder yet exists in repo):** default silently to `public/blog-media` (Next.js convention — served at `/blog-media/<file>`). Only ask the writer if the post actually references media files (STEP 4 catches this). Don't bug them about a folder they may not need.
- **`SOCIAL_SUBFOLDER` defaults silently** to `<POSTS_SUBFOLDER>/social` if no existing convention is detected. Created on first publish that ships social derivatives. Don't ask the writer about it — most pieces won't have social yet, and the default mirrors the blog folder cleanly (`content/blog/foo.md` + `content/blog/social/foo/*.md`).

Store the resolved choices in the writer's marker file under `## Publish paths (auto-detected)` so the next publish doesn't re-ask.

## STEP 2 — Reach the publishing repo (local clone)

We need two things from the repo:

- **Owner + repo name** — for the success-message commit URL. Derived by parsing the `remote.origin.url` from the local clone's `.git/config`.
- **Default branch** — read from `.git/refs/remotes/origin/HEAD` in the local clone.

If the local clone is mounted in this session, read the remote URL directly from `<PUBLISHING_REPO_DIR>/.git/config`:

```bash
ls "$PUBLISHING_REPO_DIR/.git" >/dev/null 2>&1 && echo "mounted" || echo "not_mounted"
```

If `not_mounted`, call `mcp__cowork__request_cowork_directory` with `PUBLISHING_REPO_DIR` as the `path` argument. The writer approves the mount. Continue once mounted.

If mount fails, fall back: ask the writer once via `AskUserQuestion` for the GitHub URL of their repo (`https://github.com/<owner>/<repo>`). Parse owner + repo from that. Store both in the marker file so we don't re-ask.

Parse the remote URL into owner + repo:

```bash
REMOTE_URL=$(grep -E "^\s*url\s*=" "$PUBLISHING_REPO_DIR/.git/config" | head -1 | sed 's/.*=//; s/^[[:space:]]*//')
# Handles both git@github.com:owner/repo.git and https://github.com/owner/repo[.git]
OWNER=$(echo "$REMOTE_URL" | sed -E 's@^git@github\.com:@@; s@^https?://github\.com/@@; s@/.*$@@')
REPO=$(echo "$REMOTE_URL" | sed -E 's@.*github\.com[:/]@@; s@\.git$@@' | cut -d/ -f2)
```

Store as `OWNER` and `REPO`.

## STEP 3 — Verify Phase 4 signed

Read `<PIECE_DIR>/changelog.md`. Search for a line matching:

```
Verified — <initials>, <YYYY-MM-DD>
```

The date must be today or earlier.

- **If the line exists:** proceed.
- **If missing:** halt with *"Piece `<SLUG>` has not been signed. Run `/4d-blog-engine:blog-diligence` and complete the Release Owner sign-off."* There is no override: an unsigned post never reaches `ship.py` (BP-001).

Also verify `<BLOG_PROJECT_DIR>/drafts/<SLUG>.md` exists. If not, halt: *"Staged draft missing at `<blog-project-dir>/drafts/<SLUG>.md`. Re-run `/4d-blog-engine:blog-diligence` to re-stage from the signed Phase 4 artifact."*

Store the source path as `DRAFT_PATH = <BLOG_PROJECT_DIR>/drafts/<SLUG>.md`.

## STEP 4 — Read post + extract title and hero ref

Read `$DRAFT_PATH`. Parse the frontmatter (YAML between leading `---` lines). Extract:

- `title` — for the commit message
- Hero image reference (check `og_hero`, `hero_image`, `image`, `cover` fields, in that priority order). The value is typically a relative filename like `og-hero.png` — we'll rewrite it to the in-repo path.

If no title, halt. Don't invent.

If no hero image reference in frontmatter, scan the first 20 lines of body for an inline `![<alt>](og-hero.png)` pattern. If found, treat that as the hero ref and we'll rewrite the inline path too. If still not found, warn but don't halt — some templates render the hero from a fixed convention based on the slug.

### STEP 4b — Parse the media: array (non-hero attachments)

Many posts reference additional files in their frontmatter via a `media:` array. These are NOT hero images; they're spreadsheets, PDFs, audio clips, supplementary downloads, etc. The publish skill must copy each one into the repo's media folder so the rendered post can link to it.

Parse the YAML frontmatter for a `media:` field. Expected shape:

```yaml
media:
  - file: /blog-media/4d-blog-engine-feature-comparison-2026-05-26.xlsx
    caption: "Feature-comparison workbook — 269 catalog entries × 40 features"
  - file: /blog-media/another-file.pdf
    caption: "..."
```

For each entry:

1. **Source path:** the file's basename, looked up under `<BLOG_PROJECT_DIR>/drafts/blog-media/<basename>`. The writer keeps media files in `drafts/blog-media/` alongside their markdown drafts.

2. **Dest path:** `<PUBLISHING_REPO_DIR>/<MEDIA_SUBFOLDER>/<basename>`. The YAML's `/blog-media/<file>` is the URL path (e.g., Next.js serves `public/blog-media/foo` at `/blog-media/foo`); the repo location is `MEDIA_SUBFOLDER/<basename>`.

3. **Pre-flight check:** verify the source file exists. If any media entry's source is missing, HALT before any writes with:

   > *Media file referenced in the post but not found in `<BLOG_PROJECT_DIR>/drafts/blog-media/`:*
   >
   > *  Missing: `<basename>` (referenced as `<entry.file>`)*
   >
   > *Drop the file into `<BLOG_PROJECT_DIR>/drafts/blog-media/`, then re-run `/4d-blog-engine:blog-publish <SLUG>`.*

Store the parsed media list as `MEDIA_FILES` — an array of `(source_path, dest_path, in_repo_url)` tuples. Use it in STEPs 7, 9, and 10.

If `media:` is absent or empty, set `MEDIA_FILES = []` and proceed silently.

### STEP 4c — Detect social derivatives

After Phase 4 sign-off, the writer may have run `/4d-blog-engine:blog-social` to produce social-platform derivatives. If they have, those files land at:

```
<piece>/04-diligence/social/
├── linkedin-post.md          (the feed Post — carries linkedin_channel in its frontmatter)
├── linkedin-first-comment.md (companion to the Post)
├── linkedin-article.md       (optional long-form)
├── twitter-thread.md
├── facebook-post.md
└── scorecards/
    ├── *.score.md
    └── *.score.json
```

The publish skill ships any of these that exist, in the same commit as the post, so downstream distribution automation (or a teammate) can read them straight from the repo. The plugin still does NOT auto-post to LinkedIn / Twitter / Facebook — pasting on each platform remains a manual step, by design (see the whitepaper's Diligence ethos). What changed: the source-of-truth derivative files now ship to the repo alongside the post, instead of forcing the writer to copy them out of the local `<piece>/04-diligence/` archive every time.

**Detection:**

```bash
SOCIAL_SRC="$PIECE_DIR/04-diligence/social"
if [ -d "$SOCIAL_SRC" ]; then
  # Enumerate the top-level .md files (the four supported platform names).
  SOCIAL_POST_FILES=$(find "$SOCIAL_SRC" -maxdepth 1 -name '*.md' -type f 2>/dev/null)
  # Enumerate scorecards (both .md and .json sidecars).
  SOCIAL_SCORECARD_FILES=$(find "$SOCIAL_SRC/scorecards" -maxdepth 1 -type f 2>/dev/null)
else
  SOCIAL_POST_FILES=""
  SOCIAL_SCORECARD_FILES=""
fi
```

If `SOCIAL_SRC` doesn't exist at all (writer hasn't run `/blog-social` yet), set `SOCIAL_FILES = []` and proceed silently. **Do not warn.** Most pieces won't have social derivatives, and the publish skill must stay quiet about absent optional artifacts.

For each `.md` post file found, build:

- **Source:** `<piece>/04-diligence/social/<basename>.md`
- **Dest:** `<PUBLISHING_REPO_DIR>/<SOCIAL_SUBFOLDER>/<SLUG>/<basename>.md`

For each scorecard file:

- **Source:** `<piece>/04-diligence/social/scorecards/<basename>`
- **Dest:** `<PUBLISHING_REPO_DIR>/<SOCIAL_SUBFOLDER>/<SLUG>/scorecards/<basename>`

Combine into a single list `SOCIAL_FILES` — an array of `(source_path, dest_path)` tuples. Use it in STEPs 7, 9, and 10.

**Pre-flight check:** every source file must be readable. If `find` enumerated a file but `cat` can't read it, halt with the path and the filesystem error — almost always a permissions issue, never a missing file (since `find` just listed it).

**Frontmatter rewrite for social .md files (STEP 9 detail, surfaced here for completeness):** the `source_blog:` field in each social post originally points to the local archive path (`Posts/<slug>/04-diligence/blog.md`). On the way into the repo, rewrite it to the in-repo path:

```
source_blog: <POSTS_SUBFOLDER>/<SLUG>.md
```

Downstream automation reading from the GitHub repo can then resolve the source post cleanly. The local archive path is meaningless in the repo context, so this rewrite is mechanical, not a content edit. Scorecards copy verbatim — no rewrites.

## STEP 5 — Resolve the default branch

Prefer reading from the local clone (no API call needed):

```bash
# .git/HEAD's symbolic ref usually tracks origin/HEAD; otherwise read the packed-refs
DEFAULT_BRANCH=$(cat "$PUBLISHING_REPO_DIR/.git/refs/remotes/origin/HEAD" 2>/dev/null | sed 's@^ref: refs/remotes/origin/@@')
[ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH=$(grep "refs/remotes/origin/HEAD" "$PUBLISHING_REPO_DIR/.git/packed-refs" 2>/dev/null | awk '{print $2}' | sed 's@^refs/remotes/origin/@@')
[ -z "$DEFAULT_BRANCH" ] && DEFAULT_BRANCH="main"
```

If the local clone isn't reachable, discover a `list_branches`-style tool via `ToolSearch` and query the GitHub API for the default branch. Fall back to `main` if neither path works.

Store as `DEFAULT_BRANCH`.

**Working-tree state** — the publish skill is going to add files and create a commit in the local clone, so if there are unrelated uncommitted changes already there, surface that to the writer before proceeding. Most writers won't have any (their blog repo is just for blog posts, no parallel editing). If there are unrelated changes, ask: *"Your blog repo has uncommitted changes unrelated to this post. Continue? The publish commit will only include the new post and hero — your other changes stay uncommitted alongside."* On decline, halt.

## STEP 6 — Compute destination paths and stage the publish plan

```
DEST_POST = <PUBLISHING_REPO_DIR>/<POSTS_SUBFOLDER>/<SLUG>.md
DEST_HERO = <PUBLISHING_REPO_DIR>/<IMAGES_SUBFOLDER>/<SLUG>.png
```

Check whether either already exists:

- **If neither exists:** new publish. Commit message: `Publish: <title>`.
- **If `DEST_POST` already exists:** republish. Ask the writer to confirm overwrite: *"A previous version of `<title>` is already in the repo at `<DEST_POST>`. Overwrite (republish)?"* Commit message on accept: `Republish: <title>`.

Truncate the title in the commit subject to keep total subject ≤72 chars; add ellipsis if truncated.

If `LIVE_URL_PATTERN` is set in the marker file, compute the predicted live URL using `{slug}` substitution (and `{YYYY}` / `{MM}` / `{DD}` from the slug's leading date if present).

## STEP 7 — Show the publish plan and confirm

Display the plan to the writer. Keep it short and writer-shaped — no git words, no infrastructure leaks:

```
Ready to publish "<title>" to your live site.

  Source:        drafts/<SLUG>.md
  Repo:          <OWNER>/<REPO>
  Predicted URL: <computed URL or "(your site will pick it up on rebuild)">

Files going in:
  - <POSTS_SUBFOLDER>/<SLUG>.md       (the post)
  - <IMAGES_SUBFOLDER>/<SLUG>.png      (hero)
<for each media file in MEDIA_FILES:>
  - <MEDIA_SUBFOLDER>/<basename>      (media — from drafts/blog-media/)
<if SOCIAL_FILES non-empty, one section:>
  - <SOCIAL_SUBFOLDER>/<SLUG>/        (social derivatives — N files + scorecards)

Type "go" to publish, or "cancel" to stop.
```

Only show the "Files going in" media line(s) when `MEDIA_FILES` is non-empty. Likewise, only show the social line when `SOCIAL_FILES` is non-empty — display it as a single summary line naming the directory and the file count, not one line per social file (the social bundle is typically 4 posts + 8 scorecards; listing each would drown the plan). If the hero is already in the repo unchanged, annotate it as `(hero — already in repo)`.

Wait for the writer's reply. Accept "go" / "yes" / "publish" as confirmation. Anything else cancels.

(The plugin handles the commit, the push, the pull request and the merge. The writer's "go" here is the last thing they do.)

## STEP 8 — Run the typographer's-quote transform via the vendored script

Copy the source draft into a temp location, then apply the transform:

```bash
TMP=$(mktemp)
cp "$DRAFT_PATH" "$TMP"
python3 "$CLAUDE_PLUGIN_ROOT/scripts/smart_quotes.py" --in "$TMP" --in-place
```

If the script exits non-zero, halt with the script's stderr and tell the writer their draft may have malformed frontmatter — they should look at `$DRAFT_PATH`.

The transformed file at `$TMP` is what gets copied to the repo in STEP 9. The original at `<BLOG_PROJECT_DIR>/drafts/<SLUG>.md` is never modified — it remains as the canonical local draft, available for re-publish without going through Phase 4 again.

## STEP 9 — Normalize status, rewrite hero reference, copy files

Apply the status normalization in-memory (Python on the temp file):

- Find the `status:` field in the YAML frontmatter.
- Replace its value with `published`.
- If no `status:` field exists, insert `status: published` at the end of the frontmatter.

(The local `drafts/` folder is the draft state. `/blog-publish` always ships to `published`.)

**Always bump `dateModified` to today.** This is what makes byte-identical republishes still produce a real diff (and trigger the site rebuild) without the writer needing to think about it.

- Find `dateModified:` in the YAML frontmatter. Replace with today's ISO date.
- If absent, insert `dateModified: <today YYYY-MM-DD>` at the end of the frontmatter.
- Also check inside any JSON-LD `<script>` block for a `dateModified` field (Schema.org BlogPosting); update that value too. The smart_quotes transform preserves the script block content, so a regex inside the JSON-LD region is safe.

Rewrite the hero image reference to its in-repo path. The repo's templates typically expect an absolute-from-repo-root path like `/blog-hero/<slug>.png`. Use:

```
/<IMAGES_SUBFOLDER_RELATIVE_TO_PUBLIC>/<SLUG>.png
```

Where `IMAGES_SUBFOLDER_RELATIVE_TO_PUBLIC` strips the `public/` prefix if the images dir starts with `public/` (Next.js convention — `public/blog-hero/x.png` is served at `/blog-hero/x.png`). For other generators, use the configured subfolder as-is.

Patterns to rewrite (in priority order in the frontmatter):

- `og_hero: og-hero.png` → `og_hero: /<resolved-path>`
- `hero_image: og-hero.png` → `hero_image: /<resolved-path>`
- `image: og-hero.png` → `image: /<resolved-path>`
- `cover: og-hero.png` → `cover: /<resolved-path>`

Also in body:

- `![<alt>](og-hero.png)` → `![<alt>](/<resolved-path>)`

Use Python on `$TMP` for this (not sed — sed can break on YAML edge cases). Embed the rewrite logic inline; it's straightforward.

The transformed file at `$TMP` is what STEP 10 will copy into the publishing repo. Hero image is copied as-is (no encoding — it's a regular file copy via bash, not an API call).

## STEP 9b — Register the spoke in the pillar's linking map

Hub-and-spoke upkeep. Every post is a spoke on one pillar (set at orchestrator
STEP 1.5). Read `target`, `pillar`, and `hub_url` from `<piece>/state.md`. Load
the target descriptor `${CLAUDE_PLUGIN_ROOT}/targets/<target>.md` for
`linking_map_dir`, `auto_linker`, and the pillar's `hub_term`.

1. **Open the linking map** at
   `<PUBLISHING_REPO_DIR>/<linking_map_dir>/<pillar-slug>.md` (scaffolded by STEP
   1.5 / `/blog-pillar` from `references/linking-map-template.md`). If it does not
   exist, HALT — the pillar must exist before a spoke publishes.
2. **Add this post to the spoke inventory** table: title, in-repo path, direction
   `spoke → hub`, anchor/treatment, action `published`. Bump the map's
   frontmatter `updated` to today. Add this linking-map file to the set STEP 10
   stages, so the map update lands in the **same commit** as the post.
3. **Spoke → hub link.** Confirm the post body mentions the pillar's `hub_term`
   at least once. Every target's `auto_linker` is the shared `@moxywolf/hub-links`
   adapter, which links the first mention **at build time** — so do **not**
   hand-insert the first-mention link (that double-links). Just ensure the term
   appears (registered in `hub-links/src/map.ts` via `/blog-term` or `/blog-pillar`),
   and add one explicit "Read the full *<Pillar>* →" CTA near the close, **varying
   the anchor text**. Link to the URL, never a screenshot.
4. **Hold-until-hub-exists.** If the map's `hub_status` is `planned` (the hub page
   isn't live), register the spoke and add the plain-text "Part of *<Pillar>*"
   note, but do **not** ship a live spoke→hub link to a page that 404s — a link to
   nothing is worse than no link. Add the live link when the hub ships
   (`hub_status: built|deployed`).
5. **Hub → spoke "Related reading."** Do not auto-add this spoke to the hub's
   down-links — that block is curated and held until the cluster has enough real
   spokes. Leave it to `/blog-pillar edit`.
6. **register-only target:** also print the descriptor's site-side gaps that block
   a clean render.
7. **Pin hub-links in the target** (BP-001). Before the commit, run
   `python3 "$CLAUDE_PLUGIN_ROOT/scripts/hub_term.py" pin --repo "$PUBLISHING_REPO_DIR" --site <hub_links_site_slug> --file <auto_linker_file>`.
   It moves the target's hub-links pin to the current hub-links head with the repo's own
   package manager and checks the renderer passes the descriptor's site slug. Stage the
   lockfile with the post, so the term, the pin and the post land in one commit. Exit 1
   halts the publish and shows the script's reason: a renderer passing the wrong site is
   fixed in the renderer, never worked around.

## STEP 10 — Copy files, commit, and ship

First, copy the transformed post and the hero into the repo:

```bash
mkdir -p "$(dirname "$DEST_POST")"
mkdir -p "$(dirname "$DEST_HERO")"
cp "$TMP" "$DEST_POST"
cp "$PIECE_DIR/04-diligence/og-hero.png" "$DEST_HERO"
rm "$TMP"

# Copy each media file from drafts/blog-media/ into the repo's media subfolder.
# Create the media subfolder if it doesn't exist yet (first publish with media).
for entry in MEDIA_FILES:
  mkdir -p "$(dirname "${entry.dest_path}")"
  cp "${entry.source_path}" "${entry.dest_path}"

# Copy each social derivative into the repo's social subfolder.
# .md files get the source_blog rewrite (see STEP 4c); scorecards copy verbatim.
for entry in SOCIAL_FILES:
  mkdir -p "$(dirname "${entry.dest_path}")"
  if [[ "${entry.source_path}" == *.md && "${entry.source_path}" != */scorecards/* ]]; then
    # Rewrite the source_blog: frontmatter field to the in-repo path on the way in.
    sed -E 's|^source_blog:.*$|source_blog: '"$POSTS_SUBFOLDER"/"$SLUG"'.md|' \
      "${entry.source_path}" > "${entry.dest_path}"
  else
    cp "${entry.source_path}" "${entry.dest_path}"
  fi
```

If `MEDIA_FILES` is empty, the media loop is a no-op. If `SOCIAL_FILES` is empty (writer never ran `/blog-social`), the social loop is a no-op and the publish ships post + hero + media only — same behavior as pre-v0.9. The `mkdir -p` calls are safe to run multiple times — they'll create `<repo>/<MEDIA_SUBFOLDER>/` and `<repo>/<SOCIAL_SUBFOLDER>/<SLUG>/` (and the nested `scorecards/` subdir) the first time those folders are needed.

Then create the commit from bash. The Summary and Description are auto-generated so the writer never types either:

```bash
cd "$PUBLISHING_REPO_DIR"

# Stage the post + hero + any media files + any social files
git add "$POSTS_SUBFOLDER/$SLUG.md" "$IMAGES_SUBFOLDER/$SLUG.png"
for entry in MEDIA_FILES:
  git add "${entry.dest_path_relative_to_repo}"
for entry in SOCIAL_FILES:
  git add "${entry.dest_path_relative_to_repo}"

# Auto-generated commit message
COMMIT_SUBJECT="Publish: $TITLE"
# Truncate subject to 72 chars if needed
[ ${#COMMIT_SUBJECT} -gt 72 ] && COMMIT_SUBJECT="${COMMIT_SUBJECT:0:69}..."

COMMIT_BODY="Published via /4d-blog-engine:blog-publish.

Post:   $POSTS_SUBFOLDER/$SLUG.md
Hero:   $IMAGES_SUBFOLDER/$SLUG.png
<if MEDIA_FILES non-empty:>
Media:  <comma-separated list of dest paths relative to repo root>
<if SOCIAL_FILES non-empty:>
Social: <SOCIAL_SUBFOLDER>/<SLUG>/ (N posts + M scorecards)
Status: published
Slug:   $SLUG"

git commit --no-verify -m "$COMMIT_SUBJECT" -m "$COMMIT_BODY"
```

**Branch first when the default branch is protected.** If the descriptor says `default_branch_protected: true`, run `git switch -c publish/$SLUG` from an up-to-date default branch before the `git add` above, so the commit never lands on the default branch.

**Then ship it** (BP-001), from the device's macOS shell:

```bash
BRANCH=$(git -C "$PUBLISHING_REPO_DIR" rev-parse --abbrev-ref HEAD)
if [ "<default_branch_protected>" = true ]; then
  PUSH_OUT=$(python3 "$CLAUDE_PLUGIN_ROOT/scripts/ship.py" push --repo "$PUBLISHING_REPO_DIR" --branch "$BRANCH") || exit 1
  HEAD_SHA=${PUSH_OUT##* }   # the SHA push verified on the remote; never a later rev-parse
  python3 "$CLAUDE_PLUGIN_ROOT/scripts/ship.py" merge --repo "$PUBLISHING_REPO_DIR" --slug "$OWNER/$REPO" \
    --branch "$BRANCH" --head "$HEAD_SHA" --base "$DEFAULT_BRANCH" --checks "<required_checks, comma-separated>" \
    --title "$COMMIT_SUBJECT" --body "$COMMIT_BODY" --state "$PIECE_DIR/state.md" || exit 1
else
  python3 "$CLAUDE_PLUGIN_ROOT/scripts/ship.py" push --repo "$PUBLISHING_REPO_DIR" --branch "$BRANCH" \
    --state "$PIECE_DIR/state.md" || exit 1
fi
python3 "$CLAUDE_PLUGIN_ROOT/scripts/ship.py" verify-live --url "<post_url_pattern with the slug>" --hub-path "<hub path>" \
  --term "<hub_term>" --deadline 900 --state "$PIECE_DIR/state.md"
```

Each exits 0 on success and 1 with `refused: <reason>` on stderr. A refusal stops the publish: report the script's reason in the writer's words and leave the piece unpublished. On an unprotected target `push --state` writes `published_pr: none` and `published_merge: <pushed SHA>` (the push is the publish). On a protected target `push` writes nothing, so a failed check leaves the previous publication record intact, and `merge --state` writes the pull request number and the merge SHA only after the merge. Either write resets `live_verified_at: pending`; `verify-live` sets it, and only on exit 0. A post is published when `verify-live` exits 0, not before.

**Capture the commit SHA for the success message:**

```bash
COMMIT_SHA=$(cd "$PUBLISHING_REPO_DIR" && git rev-parse --short HEAD)
```

The success message uses this SHA; after `merge` it reports the merge SHA instead.

### Byte-identical content edge case

If the file at `<DEST_POST>` is byte-identical to what was already there AND nothing else changed (the dateModified bump from STEP 9 normally prevents this), `git commit` will fail with `nothing to commit`. Surface a quiet message:

> *Nothing changed since the last publish — your draft and the staged file are already byte-identical. If you wanted to force a republish, edit the post and try again.*

### Silent lockfile recovery

If `git add` or `git commit` fails with `fatal: Unable to create '.../.git/index.lock': File exists`, that's the GitHub Desktop file-watcher race. Recover silently:

```bash
LOCKFILE="$PUBLISHING_REPO_DIR/.git/index.lock"
```

1. Call `mcp__cowork__allow_cowork_file_delete` with `LOCKFILE` (the sandbox blocks .git/* deletes by default; this grants permission for the specific path).
2. `rm -f "$LOCKFILE"`
3. Retry the failed `git add` / `git commit`.

Retry up to **two** times. If still failing after the second retry, surface this — only after recovery attempts have failed:

> *Something inside your blog repo is holding a lock — usually that's GitHub Desktop scanning the folder. Quit GitHub Desktop entirely (`Cmd+Q`), then re-run `/4d-blog-engine:blog-publish <SLUG>`.*

This message ONLY shows up after silent recovery fails. The vast majority of publishes succeed silently on the first try.

### Byte-identical content

If the file at `<DEST_POST>` is byte-identical to what's already there AND no other staged change exists, `git commit` will fail with `nothing to commit`. The dateModified bump from STEP 9 normally prevents this. If somehow we're still byte-identical (dateModified was already today AND content didn't change), surface a quiet message:

> *Nothing changed since the last publish — your draft and the live post are already byte-identical. If you wanted to force a republish (to trigger a rebuild), edit the post and try again.*

### After the commit succeeds

Capture the new commit SHA for the success message:

```bash
COMMIT_SHA=$(cd "$PUBLISHING_REPO_DIR" && git rev-parse --short HEAD)
```

The success message uses it until `merge` reports the merge SHA.

## STEP 11 — Update piece state

Append to `<PIECE_DIR>/state.md`:

```markdown
- [x] Published to live site (<published | draft>)
```

And to the process log:

```
<ISO-8601 now> — Published to <REMOTE_URL> branch <DEFAULT_BRANCH> at commit <SHORT_SHA>. Status: <published|draft>.
```

Update the state.md frontmatter:

- `published: <YYYY-MM-DD>`
- `published_commit: <short SHA>`
- `published_status: <published|draft>`

## STEP 11b — Optional: publish the LinkedIn Post to its channel via Claude in Chrome

By default this skill does **not** post to any platform — pasting by hand stays the default (see the Diligence ethos). This step is an **opt-in** convenience: if the writer wants the LinkedIn **feed Post** published straight to the channel chosen in `/blog-social` STEP 2b, drive their own logged-in LinkedIn through Claude in Chrome. No third-party scheduler — the post is authored in the writer's real browser session, exactly as if they typed it. Run this step only when ALL of these hold:

- A `linkedin-post.md` derivative shipped in this publish (it's in `SOCIAL_FILES`).
- Claude in Chrome is connected — `mcp__Claude_in_Chrome__tabs_context_mcp` returns a browser. If the extension isn't connected, skip this step silently (no error; manual paste stays the path) and remind the writer in STEP 12.
- The writer explicitly opts in (ask once — see below). On anything but a clear yes, skip and leave posting manual.

Read `linkedin_channel`, `linkedin_channel_type`, `linkedin_channel_url`, and `publish_sequence` from the shipped LinkedIn frontmatter (recorded by `/blog-social` STEP 2b). If `linkedin_channel` is absent, skip this step — there's no chosen channel to post as.

**Detect the shape and pick the path:**

- If any shipped LinkedIn file carries `publish_sequence: company-page-trio` (the channel is a Company/Showcase Page) → run the **Company-page trio** path: Article first, then the teaser Post, then the first comment with the Article URL substituted in. Jump to "Company-page trio" below.
- Otherwise (personal profile) → run the **single Post** path immediately below (Confirm → Drive the composer → Offer the first comment).

---

### Single Post path (personal profile)

#### Confirm before touching the browser

Posting to LinkedIn is irreversible once the **Post** button is clicked. Show the writer exactly what will post and where, and get a clear yes BEFORE you open the composer:

```
Publish the LinkedIn Post now, in your browser, as <linkedin_channel>?

  Channel:  <linkedin_channel> (<linkedin_channel_type>)
  Body:     <first ~200 chars of the Post>… (<N> chars total)
  Link:     none in the body (the first comment carries the URL)

I'll open your LinkedIn, switch "Post as" to <linkedin_channel>, type the body,
and stop for your final OK before I click Post.

Reply "post it" to proceed, or "skip" to leave it for manual pasting.
```

On anything but a clear yes, skip to STEP 12.

#### Drive the composer (Claude in Chrome)

Claude in Chrome runs in the writer's real, authenticated browser. Drive by screenshots and the accessibility tree, **not** fixed pixel coordinates — LinkedIn moves its DOM; identify controls by their heading/label text and re-screenshot between steps.

1. `mcp__Claude_in_Chrome__tabs_context_mcp` with `createIfEmpty: true`.
2. `mcp__Claude_in_Chrome__navigate` to `https://www.linkedin.com/feed/`. Wait ~3 seconds.
3. **Confirm the session is live.** If a login/auth wall shows instead of the feed (no "Start a post" box), STOP and tell the writer: *"Sign into LinkedIn in Chrome, then re-run — I couldn't reach your logged-in session."* Leave the Post for manual pasting.
4. Click **Start a post** to open the composer.
5. **Switch the actor to the chosen channel.** Click the **caret next to your name** ("Post to Anyone ▾") → **Post settings** panel → click the **author row at the top** ("<Your name> ›") → the **Posting as** panel. Select the radio whose label matches `linkedin_channel`. If no label matches (the channel isn't authorable in this session), STOP and tell the writer the channel wasn't available — do NOT post as a different actor. Return to the composer (Save/Back).
6. **Enter the body.** Focus the composer text area and input the Post body from `linkedin-post.md` (frontmatter stripped — body text only, NO link). Use `mcp__Claude_in_Chrome__form_input` for the text area; fall back to `computer` typing if needed. Screenshot and verify the actor still reads `<linkedin_channel>` and the body landed intact.
7. **Final OK, then post.** Show the writer a screenshot of the composer (right actor, right body) and ask once more: *"Ready — click Post as <linkedin_channel>?"* On their yes, click **Post**. This is the irreversible action; never click it without that confirmation. Wait ~3 seconds and screenshot to confirm the post published.

#### Offer the first comment as the follow-up

The first comment is what carries the blog URL and sources. Immediately after the Post publishes, offer to add it:

*"Posted. Want me to add the first comment (the blog link + sources) under it, as <linkedin_channel>?"*

On a yes: open the just-published post's comment box, confirm the commenting identity is `<linkedin_channel>` (LinkedIn comments as the same actor the post was published as), input the contents of `linkedin-first-comment.md` (bare URLs, no markdown link syntax), screenshot for the writer's OK, then submit. On a no, remind them the first comment still needs pasting by hand.

Then skip to "Record the outcome" below.

---

### Company-page trio path (Article → teaser Post → first comment)

This path posts the trio **in order**, because the teaser Post's first comment links to the Article, and the Article's URL doesn't exist until it's published. Same browser-driving discipline as the single-Post path: screenshots and label text, never fixed coordinates, re-screenshot between steps, and never click a publish/Post button without an explicit OK on a screenshot first.

**Two-stage reality.** Per `/blog-social`'s company-page flow, only `linkedin-article.md` is written up front (Stage 1). The teaser Post and first comment are written in **Stage 2 — after the Article is live** — so they may not exist in the social directory yet when this path starts. This path publishes the Article first, captures its URL, then generates Stage 2 with that real URL, then posts the teaser (with its image) and the comment. Identify files by frontmatter: `publish_order: 1` / `trio_stage: 1-article` is `linkedin-article.md`; `2` / `2-teaser` is `linkedin-post.md`; `3` / `2-comment` is `linkedin-first-comment.md`.

**Confirm the whole sequence before touching the browser:**

```
Publish the company-page trio now, in your browser, as <linkedin_channel>?

  1. Article  — "<article title>" (<words> words), via Write article
  2. Post     — teaser, <N> chars, points readers to the Article
  3. Comment  — under the teaser, links to the Article + blog + sources

I'll publish the Article first, grab its URL, post the teaser, then add the
comment with the Article URL filled in. I'll stop for your OK before each
irreversible publish.

Reply "post it" to proceed, or "skip" to leave it all for manual pasting.
```

On anything but a clear yes, skip to STEP 12.

**1 — Publish the Article (and capture its URL).**

1. `navigate` to `https://www.linkedin.com/article/new/`. Wait ~3 seconds. Confirm the session is live (login wall → STOP, tell the writer to sign in, leave the trio for manual pasting).
2. **Set the publishing identity to the Page.** The article editor has a "Publishing as / Publish as" selector (top of the editor). Set it to `<linkedin_channel>`. If the Page isn't offered as a publishing identity in this session, STOP and tell the writer the Article can't be authored as `<linkedin_channel>` here — do NOT publish it as a different actor, and do NOT silently fall back to the personal profile.
3. Enter the **title** (the Article's `title`) and the **body** from `linkedin-article.md` (frontmatter stripped); set the cover image from the Article's `image:` if present. Inline links are allowed in the Article body. LinkedIn also prompts for a "tell your network what your article is about" share blurb on publish — use the Article's `share_blurb` field if present, else a one-line summary.
4. Screenshot, show the writer (right identity, title, body), and ask: *"Ready — Publish this Article as <linkedin_channel>?"* On their yes, click **Publish**.
5. After it publishes, capture the **Article URL** from the address bar (read the tab URL via `tabs_context_mcp` or a screenshot of the address bar). Store it as `ARTICLE_URL`. If you can't read a stable published URL, STOP before going further — the comment needs that URL — and hand the rest to the writer to finish by hand.

**2 — Write Stage 2 (teaser Post + first comment) with the real URL.**

The teaser and comment are written only now that the Article is live. If `linkedin-post.md` and `linkedin-first-comment.md` aren't already in the social directory, generate them via `/4d-blog-engine:blog-social` Stage 2 (or inline, following its STEP 5a company-page spec), passing `ARTICLE_URL` so the teaser's hook points at the Article and the first comment carries the real `ARTICLE_URL` + blog URL + sources. The teaser must carry an image — reuse the Article hero or generate a teaser-specific one, recorded in its `image:` field. If both files already exist (writer pre-generated them), just substitute `ARTICLE_URL` for any `<LINKEDIN_ARTICLE_URL>` placeholder.

**3 — Publish the teaser Post (with its image).**

Run the single-Post composer flow (above) for `linkedin-post.md` as `<linkedin_channel>`: Start a post → switch "Post as" to the Page → enter the teaser body (no link in body) → **attach its image** (the `image:` file) → screenshot → OK → **Post**. Confirm it published.

**4 — Add the first comment.**

Under the just-published teaser Post, as the same actor (`<linkedin_channel>`), open the comment box, input the contents of `linkedin-first-comment.md` (the real `ARTICLE_URL` already in place; bare URLs, no markdown link syntax), screenshot for the writer's OK, and submit.

If any step stalls (identity not available, URL not readable, UI doesn't match), STOP at that step, report exactly which pieces published and which didn't, and hand the remainder to the writer — never guess-click forward through a publish button.

### Limits to state plainly (don't paper over them)

- **Article publishing as a Page is LinkedIn-dependent.** Some accounts can't author a long-form Article as a Company Page from the personal session. If the publishing-identity selector doesn't offer `<linkedin_channel>`, this path STOPS at the Article and hands off — it never posts the Article as the wrong actor.
- **Twitter / Facebook** stay manual in this step — its scope is the LinkedIn trio (or single Post) the writer chose a channel for. Drive them through their own composers only on explicit request.
- **If any composer UI doesn't match** what's described (LinkedIn redesign) and you can't confidently locate the identity selector, the body field, or the publish/Post button: STOP, leave that piece unposted, and tell the writer to finish by hand. Never guess-click toward a publish button.

Record the outcome in `<PIECE_DIR>/state.md`'s process log: `<ISO> — LinkedIn published via Chrome as <linkedin_channel>: <single Post | company-page trio> (article: <url|n/a>; teaser: posted|skipped; first comment: added|skipped).` If the writer skipped the whole step, record nothing.

## STEP 11c — Optional: ask the team to amplify on Slack

Once the post is live — whether this skill published it (STEP 11b) or the writer posted it by hand — offer to drop an amplification nudge in the team's Slack so colleagues reshare it. **Opt-in.** Run only when ALL of these hold:

- A LinkedIn post is live and you have its **public post URL** — the teaser/feed Post URL people can reshare, NOT the Article editor URL. If you don't have it, ask the writer for it; if they'd rather not, skip.
- A Slack connector is available — discover a send-message tool via `ToolSearch` (e.g. query `slack send`). If none is connected, skip silently and note it in STEP 12.
- The writer explicitly opts in.

Posting to a shared channel and pinging people is a real, visible action, so **always show the exact message and the target channel and wait for a clear yes before sending** — never auto-send.

**Default message** (short; URL on its own line so Slack unfurls it):

```
@channel New on LinkedIn — give it a quick boost: open the post and reshare it with one person who'd get value from it. Takes 30 seconds and it helps a lot.

<post-url>
```

- **Channel:** `#general` by default (the writer can name a different one). Resolve the channel id first if the send tool needs one.
- **Mention:** `@channel` by default (pings everyone in the channel). Offer `@here` (only currently-active members) as the quieter option and honor whichever the writer picks. In Slack these are the broadcast tokens `<!channel>` / `<!here>` — emit whichever form the connector's send tool expects.
- Send via the Slack connector's send-message tool. Capture the message permalink if it's returned.

This step never DMs anyone, never posts anywhere but the channel the writer named, and never sends without the explicit confirmation above.

Record in `<PIECE_DIR>/state.md`'s process log: `<ISO> — Slack amplification posted to #<channel> (<@channel|@here>) with the post URL.` If the writer skipped, record nothing.

## STEP 12 — Report back

Report only after `verify-live` exits 0:

```
✓ Published "<title>".

Live:    <post URL> (hub link to <hub path> verified at <live_verified_at>)
Merged:  <OWNER>/<REPO> #<published_pr> as <published_merge>   (or: pushed <COMMIT_SHA> to <DEFAULT_BRANCH>)
Local:   <DEFAULT_BRANCH> pulled back, remote == local
Files:
  - <POSTS_SUBFOLDER>/<SLUG>.md
  - <IMAGES_SUBFOLDER>/<SLUG>.png
  - <lockfile>   (hub-links pin, when it moved)
<media and social lines as in STEP 7>
```

When any `ship.py` step refuses, report what it said and what's left undone instead. Never tell the writer to push.

## What this skill does NOT do

- It does not post to Twitter/X or Facebook on your behalf, and does not auto-post anything without an explicit opt-in. The skill ships the *source-of-truth* social derivative files (`<piece>/04-diligence/social/*.md`) into the repo at `<SOCIAL_SUBFOLDER>/<SLUG>/`, so downstream automation (or a teammate) can read them straight from GitHub. Paste-and-post stays the default, by design (see the whitepaper's Diligence ethos). The **one** exception is the opt-in STEP 11b: when the writer explicitly asks, it publishes the chosen LinkedIn channel's derivatives through Claude in Chrome in the writer's own logged-in LinkedIn — stopping for a final OK before every irreversible publish. On a personal profile that's the feed Post plus its first comment. On a Company/Showcase Page it's the Article-led trio in order (Article → teaser Post → first comment with the captured Article URL). If LinkedIn won't let the Article be authored as the Page in that session, the path stops and hands off rather than posting as the wrong actor.
- It does not push under a person's login. Git on GitHub runs as the `moxywolf-agent` app through `agent_token.py`; a repository the app isn't installed on is reported as a gap.
- It does not bypass a protected branch. It opens a pull request and merges only on green required checks.
- It does not delete the source draft at `<BLOG_PROJECT_DIR>/drafts/<SLUG>.md`. The draft stays as the canonical local copy. Re-running `/blog-publish <slug>` re-publishes it.
- It does not delete files in `<PIECE_DIR>/04-diligence/`. The piece directory remains the forensic archive.
- It does not trigger your site's rebuild directly. The merge triggers your hosting webhook; `verify-live` waits for the result.
- It does not rewrite source images. The hero PNG goes into the repo as-is.
- It does not modify the source post's quotes. The transform writes to the repo path; the source stays untouched.

## Degradation behaviors

- **`git` not available in the sandbox:** halt with a clear message. Rare.
- **Repo is on iCloud / Google Drive / Dropbox synced filesystem:** publish may work but expect lockfile races. Strongly recommend the writer move the repo to a non-synced local path (`~/GitHub/`, outside iCloud Desktop & Documents). Don't refuse; flag it once and proceed.
- **Default branch detection fails** (no `origin/HEAD`): ask the writer whether to push to `main` or `master`. Don't assume.
- **smart_quotes.py exits with code 3 (malformed frontmatter):** halt and tell the writer their source post needs the frontmatter fixed before publish — show them the line.
- **Images folder doesn't exist and writer's site uses on-demand hero**: skip the hero copy if the IMAGES_SUBFOLDER detection found nothing AND no hero reference exists in frontmatter. Log it.
- **Status normalization fails** (unexpected YAML shape): surface the issue, ask whether to publish as-is or halt.
