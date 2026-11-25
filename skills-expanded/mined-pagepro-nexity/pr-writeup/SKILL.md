---
name: pr-writeup
description: >-
  Write or refresh a pull/merge request description a reviewer can follow in one read:
  the problem as a visitor saw it, a before/after table of the values that changed,
  reviewer notes, matching before/after screenshots committed with the PR under
  `.github/pr-assets/<topic>/` (the branch name, `/` → `-`), and a concrete test plan,
  with the text put through the `work-humanizer` skill and its check before it goes up. Use it when a PR/MR is opened
  or updated and needs a description, e.g. "write the PR description", "add screenshots
  to the PR", "update the PR after review", "refresh the before/after shots". Not for
  commit messages or release notes. Optional argument: the PR/MR number or URL.
---

# PR write-up

**When to use:** a PR/MR exists (or is about to) and its description has to carry the
change to a reviewer: what was wrong, what changed, with numbers, what the reviewer should
know, how it looks before and after, and how to test it. Also when review feedback changes
the work and the description, table and screenshots need a refresh.

Stack-agnostic. Requirements, all optional except the forge CLI:
- **Forge CLI:** `gh` (GitHub) or `glab` (GitLab), picked from the remote host
  (`git remote get-url origin`).
- **A browser you can drive** for screenshots: the `agent-browser` CLI, Playwright, or the
  Chrome DevTools MCP. Without one, skip screenshots and say so.
- **python3** for the humanizer check, plus **Pillow** (or ImageMagick) for cropping.

The helpers live next to this file in `scripts/` (`prepare.js`, `region.js`, `crop.py`,
`compose.py`). The humanizer is the sibling skill `work-humanizer` (`../work-humanizer/`
relative to this file, e.g. `.agents/skills/work-humanizer/` once both are copied into a
project). Below, `S` is this skill's `scripts/` folder and `H` the humanizer folder:

```bash
S=.agents/skills/pr-writeup/scripts     # adjust to where the skills live
H=.agents/skills/work-humanizer
```

## Step 1 — Collect the facts

The description is only as good as what you measured. Before writing:

1. **Diff and history:** `git log --oneline <base>..HEAD`, `git diff --stat <base>...HEAD`.
   Read the commit bodies: they usually hold the *why*.
2. **The numbers.** For a visual change, measure computed values in the browser
   (`getComputedStyle`, `getBoundingClientRect`) on the base deploy and on the branch: gaps,
   sizes, line heights, at desktop and mobile widths. For performance, the measured KB, ms
   or score (PageSpeed Insights or Lighthouse, mobile, median of three runs). Never put a
   number in the description you didn't measure or read from the code.
3. **The story of the PR.** Approaches tried and reverted during review, and why. Rules or
   docs updated alongside. Content or data issues found on the way that the PR does not fix.

## Step 2 — Draft the body

Write it to a file (`/tmp/<topic>/body.md`), never inline in the command. `<topic>` is
the PR branch name with `/` replaced by `-` (`feat/hero-gap` → `feat-hero-gap`). Keep
this shape; drop a section only when it would be empty:

```markdown
## Summary

<Where the problem showed, what a visitor or user saw, in their terms. One short
paragraph.> <What changes now, one or two sentences.>

| <Thing> | Before | After |
|---|---|---|
| <property, with unit and breakpoint> | <measured> | <measured> |

## Notes for the reviewer

- <Decision and its reason, e.g. why 28px on mobile instead of 32px.>
- <What was tried first and reverted, and why. Reviewers trust a PR that shows this.>
- <How a non-obvious piece works: the helper, the edge case it guards.>
- <Docs/rules updated in the same PR.>

## Screenshots

<Where "before" and "after" come from, e.g. "Before is production. After is this
branch, run locally against the same dataset.">

**<Page, what to look at> (desktop, 1280px)**

| Before | After |
|---|---|
| ![<page> before](<image url>) | ![<page> after](<image url>) |

**<Page> on mobile (390px)**

| Before | After |
|---|---|
| <img src="<image url>" width="300" alt="<page> on mobile, before"> | <img src="<image url>" width="300" alt="<page> on mobile, after"> |

Screenshots are committed in this PR under `.github/pr-assets/<topic>/`.

## Test plan

- [ ] `<url or route>` on desktop and mobile: <expected, with the numbers from the table>
- [ ] <Regression check on the pages that must not change>
- [ ] `<lint/typecheck/test command>` (<ran in the pre-commit hook / CI>)

<attribution line, if the session has one>
```

Writing rules: lead with the visitor's view, not the CSS. Every row of the table is a
measured value with its unit. Notes explain decisions, not the diff. The test plan names
URLs and expected values a reviewer can check without asking.

## Step 3 — Screenshots

Only for changes a reviewer can see. **Before** comes from production or the base
branch's deploy; **after** from the branch (local dev server or its preview) against the
**same data**. Same page, same viewport, same crop, or the comparison means nothing.

For each page and width:

1. **Open the page, then set the viewport and confirm it.** Some drivers reset the
   viewport on navigation (agent-browser does): check `window.innerWidth` after every
   `open` and set it again if needed.
2. **Dismiss the cookie banner once per origin** (click "Reject"/"Decline"); it keeps the
   choice for the session. Re-check before each shot that no banner is visible.
3. **Prepare the page:** run `scripts/prepare.js` (hides dev overlays, turns off smooth
   scrolling, scrolls to the bottom and back so lazy content renders).
4. **Measure the crop:** `(<region.js>)("<start anchor>", "<end anchor>", 32)`. An anchor is
   a CSS selector, optionally `selector|text` for "the first match starting with text",
   e.g. `"h2|Key takeaways"`. Save the printed JSON to a file.
5. **Take a full-page screenshot to an absolute path**, then
   `python3 "$S/crop.py" full.png region.json out.png`.
   For a mobile shot, a plain viewport screenshot after scrolling the anchor to the top
   (minus the header height) usually reads better than a long crop.
6. **Name the files** `before-<page>-<width>.png` and `after-<page>-<width>.png`
   (`before-home-hero-1280.png`, `after-home-hero-390.png`). Only cropped shots go into
   the repo, never the full-page originals.
7. **Optional: one labelled image.** When a table is too narrow (tall crops) or the
   label should carry the measured value, put both into one image with `compose.py` and
   commit it as `compare-<page>-<width>.png`. Before goes left with a red label, after
   right with a green one:

   ```bash
   python3 "$S/compose.py" before-home-hero-1280.png after-home-hero-1280.png compare-home-hero-1280.png \
     --before-label "BEFORE (main) · pretitle 3.69:1 (fail)" \
     --after-label "AFTER (branch) · pretitle 5.07:1"
   ```
8. **Look at every image before committing it.** Check for a cookie banner, a dev
   overlay, blank lazy images, the wrong viewport, personal or customer data, and that
   before and after are on the right sides.

With agent-browser:

```bash
agent-browser open "$URL" && agent-browser set viewport 1280 900
agent-browser eval "$(cat "$S/prepare.js")"
agent-browser eval "($(cat "$S/region.js"))('h2|Key takeaways', 'h2|Next heading', 32)" > /tmp/<topic>/region.json
agent-browser screenshot --full /tmp/<topic>/full.png
python3 "$S/crop.py" /tmp/<topic>/full.png /tmp/<topic>/region.json /tmp/<topic>/after-<page>-1280.png
# same steps on the base URL for before-<page>-1280.png
```

### Where the images go

Screenshots are **committed on the PR branch**, in a folder named after it, and merge
with the PR:

```
.github/pr-assets/<topic>/
├── before-<page>-<width>.png
├── after-<page>-<width>.png
└── compare-<page>-<width>.png      # only if you used compose.py
```

```bash
mkdir -p .github/pr-assets/<topic>
cp /tmp/<topic>/before-*.png /tmp/<topic>/after-*.png .github/pr-assets/<topic>/
git add .github/pr-assets/<topic>
git commit -m "docs(pr): before/after screenshots for <topic>"
git push
SHA=$(git rev-parse HEAD)          # the commit that holds the images
```

Keep each file small (crop to the region, under ~500 KB): images stay in git history
after they are deleted. `.github/` is outside the app's build, so these files never
reach a deploy, and the commit needs no hook bypass.

**Link format (GitHub).** Use an absolute `blob` URL pinned to the commit SHA, with
`?raw=true`:

```
https://github.com/<owner>/<repo>/blob/<SHA>/.github/pr-assets/<topic>/after-<page>-<width>.png?raw=true
```

Why this form and not a shorter one:
- **A relative path** (`.github/pr-assets/…`) does not work in a PR body. GitHub
  resolves relative image paths only in files rendered from the repo, not in PR
  descriptions or comments, so the image shows as broken. Relative paths are fine
  inside committed Markdown files.
- **The branch name** (`blob/<branch>/…?raw=true`) renders during review, but breaks
  when the branch is deleted after merge, which most repos do automatically.
- **The commit SHA** keeps working after merge, squash merge and branch deletion,
  because GitHub keeps the PR's commits. It also never shows a cached old image,
  because a new commit is a new URL.
- **`?raw=true`** renders in private repos for anyone with access.
  `raw.githubusercontent.com` links do not.

**GitLab.** The same folder works; link
`<project-url>/-/raw/<SHA>/.github/pr-assets/<topic>/<file>.png`. If the project
prefers it, upload instead with
`glab api --method POST projects/:id/uploads -F file=@<file>.png` and paste the returned
`markdown`; then don't commit the files.

## Step 4 — Humanize, then sweep

1. Edit the draft with the **`work-humanizer`** skill (rewrite mode). Keep every fact,
   number, caveat and commitment as is.
2. Run the mechanical sweep and fix what it flags (em dashes, semicolons, stock phrases,
   pause-and-point lines, uniform sentence length):

   ```bash
   python3 "$H/check.py" /tmp/<topic>/body.md
   ```

   Image markdown `![](…)` counts as exclamation marks. Ignore those. A flagged phrase that
   quotes the product (a heading, a label) is still worth rewording around in your own
   sentences.
3. Fact audit: every number in the body still matches what you measured in Step 1.

## Step 5 — Publish

Creating the PR and editing its body are outward actions: confirm first unless the user
already asked for them. Push the screenshot commit before you publish, or the images 404.

```bash
gh pr create --base <base> --head <branch> --title "<conventional title>" --body-file /tmp/<topic>/body.md
gh pr edit <number> --body-file /tmp/<topic>/body.md        # existing PR
glab mr create --source-branch <branch> --target-branch <base> --title "<title>" --description "$(cat /tmp/<topic>/body.md)"
glab mr update <number> --description "$(cat /tmp/<topic>/body.md)"
```

Open the PR page and check that every image renders. Report the URL.

## Step 6 — After review

When feedback changes the work:

- Re-measure and update the table. Say in the notes what an earlier commit did and why it
  was taken back. Don't rewrite history out of the description.
- **Add new screenshots under new names** (`after-<page>-<width>-v2.png`, `-v3`, …),
  commit them, and point the body at them with the new commit's SHA. Don't overwrite or
  delete the earlier files in the PR: older comments may link to them.
- Retitle the PR if its scope changed (`gh pr edit <n> --title …`).
- Run the sweep again before `gh pr edit`.

`.github/pr-assets/` grows with every visual PR. Pruning old folders on the main branch
later is safe: the SHA-pinned links in merged PRs keep working, because they point at
commits, not at the current tree.

## Hard rules

- **Facts only.** Every number is measured or read from the code. Never invent a value or a
  screenshot, never describe a check you didn't run.
- **Before and after match:** same page, data, viewport, crop. Say where each side comes
  from.
- **Images live in `.github/pr-assets/<topic>/` on the PR branch**, committed with the
  PR, linked by commit SHA. No separate screenshots branch, no relative paths in the
  PR body.
- **Check every image before committing it.** No cookie banners, dev overlays, personal or
  customer data, tokens or admin UI. A committed image stays in history.
- **Humanize and sweep before every publish**, including edits after review.
- **Confirm before outward actions** (creating the PR, editing its body, pushing)
  unless the user asked for them in this conversation.

## Fallback paths

- **No browser driver available:** write the body without the Screenshots section and tell
  the user. Offer to add shots they take themselves (commit them the same way).
- **Preview behind SSO (e.g. Vercel Deployment Protection):** ask the user for a share link
  (`?_vercel_share=…`) or test locally. Never extract or mint a bypass token.
- **Can't run the branch locally** (env files blocked, missing secrets): ask the user to run
  it or to link `.env` into the worktree themselves. Don't copy, source or read secret
  files. As a last resort, preview the change on production by injecting the CSS it adds,
  and label those shots as a simulation in the body.
- **Viewport won't stick:** set it after `open`, assert `innerWidth`, and re-measure.
- **Pillow missing:** `crop.py` and `compose.py` print the equivalent ImageMagick command
  (`compose.py`'s has no labels, so name the sides in the text above the image).
- **Forge unclear:** infer it from the remote host and the base from the PR, and say what
  you assumed.
