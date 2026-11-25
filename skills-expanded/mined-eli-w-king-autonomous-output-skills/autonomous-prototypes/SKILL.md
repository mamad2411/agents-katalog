---
name: autonomous-prototypes
description: "Prototypes and PRs (AI-First edition): make a UI change in your own repo, test it in the integrated browser, and ship it: a branch per change, a PR in your repo, a merge when you ask, and a live GitHub Pages link with a page for everyone. Use for 'make this change', 'fix what confused people', 'test it in the browser', 'fix the bug', 'open a PR', 'merge it', 'publish it'."
---

# Prototypes and PRs (AI-First edition)

Turn a design ask into a working change in the person's own repo, prove it in the integrated browser, and ship it
as a PR and a live link. Options to pick from follow [autonomous-variations](../autonomous-variations/SKILL.md);
the video follows [autonomous-demos](../autonomous-demos/SKILL.md).

## Rules

1. **Their repo only.** Target it explicitly: `--repo <owner>/<repo>` (from `gh repo view --json nameWithOwner`).
   Never push to, or open anything on, the project it came from.
2. **Read `AGENTS.md` first** and follow it: how to start, the port, the build, the review page, Pages.
3. **A branch per change** from the latest main (`git switch main`, `git pull`, `git switch -c <short-name>`).
   Commit locally as you go.
4. **Problem first.** When the ask is a problem ("what confused testers"), make the smallest change that solves
   it, then say what you changed and why in two lines.
5. **Surgical.** Change only what the ask needs; `git diff --stat` shows only the files you meant.
6. **The default is explicit.** What the person picks becomes the default in one clear line, never behind a flag.
7. **Show it.** Every change ends on the localhost link in the integrated browser, in the changed state.
8. **Ship when asked.** Push, open a PR, merge and publish when the person asks or the use case says to.
9. **Cheap.** No new test frameworks, no extra installs, no big files.
10. **Windows:** call `npm.cmd` and `npx.cmd`, since PowerShell can block the plain `npm` script.

## Test it in the integrated browser

1. Start the app, or reuse the running server (`AGENTS.md` says where the port is), and open the localhost link
   in the integrated browser.
2. Use it the way a person would: read the page, click what changed. To draw on a canvas, run a short Playwright
   snippet there: `await page.mouse.move(400, 300); await page.mouse.down(); await page.mouse.move(600, 420,
   { steps: 12 }); await page.mouse.up();` and look at a screenshot.
3. If something's broken, find the cause in the code (console errors, then the code path), fix it with the
   smallest change, reload and try again.
4. End on the proof (for a drawing bug, a shape drawn after the fix) and say what was wrong in one line.

## Ship it

1. **Scope check:** `git status` and `git diff --stat main...HEAD`. No `node_modules`, build output, scratch
   files, secrets or files over 25 MB.
2. **Push and open the PR** in their repo:
   ```text
   git push -u origin <branch>
   gh pr create --repo <owner>/<repo> --base main --head <branch> --title "<what changed>" --body-file <file>
   ```
   The body: what and why in a few lines, a screenshot
   (`https://github.com/<owner>/<repo>/blob/<branch>/<path>?raw=true`), the video when there is one, and how to
   try it. Keep the body file out of the repo.
3. **The page for everyone:** if the repo has one (such as `/review/`, filled from `review/review.json`), fill in
   the variations, the favorite, the video and the PR link on the same branch and push. Without one, add a plain,
   light `review/index.html` with the same.
4. **Merge when asked:** `gh pr merge <number> --repo <owner>/<repo> --squash`, then `git switch main`,
   `git pull`.
5. **Publish with GitHub Pages.** The repo's Actions workflow deploys main. Once per repo, turn Pages on for
   Actions: `gh api -X POST repos/<owner>/<repo>/pages -f build_type=workflow` (`-X PUT` if Pages exists). Watch
   it: `gh run list --repo <owner>/<repo> --limit 1`, then `gh run watch <id> --repo <owner>/<repo> --exit-status`.
6. **Open the results** in the integrated browser: the PR, `https://<owner>.github.io/<repo>/` and its
   `review/` page. Report the links and what changed in a few bullets.
