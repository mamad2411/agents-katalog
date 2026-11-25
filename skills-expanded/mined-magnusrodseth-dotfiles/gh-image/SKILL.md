---
name: gh-image
description: Attach local images or videos to GitHub issues, pull requests, and comments using native gh --attach. Use for screenshot uploads, before/after evidence, gh image requests, or reusing user-attachments URLs in GitHub markdown. For finding macOS screenshots, use the screenshots skill first.
license: MIT
compatibility: opencode
user-invokable: true
metadata:
  scope: global
  tools: gh
---

# gh-image

Use native `--attach` on `gh pr` and `gh issue` commands. GitHub CLI uploads the files and inserts their hosted references into the body.
This skill keeps its name for existing callers; its workflow uses the built-in flags.

## Verify support

```bash
gh --version
gh auth status
gh pr edit --help
```

`--attach` requires GitHub CLI 2.99.0 or newer. Check the target command's help for the flag; upgrade `gh` if it is absent.
Uploads use normal `gh` authentication, including OAuth and personal access tokens. Browser cookies and the `gh-image` extension are unnecessary.
The authenticated account needs write access to the target repository. GitHub.com and GitHub Enterprise Cloud support attachments; GitHub Enterprise Server does not.

## Choose the destination

Inspect each image before uploading and keep only files that explain the change. For files in `~/screenshots/`, use the **screenshots** skill to find candidates.
Run inside the target repository, or pass `--repo OWNER/REPO` explicitly.

| Destination | Command |
|---|---|
| New PR | `gh pr create --title "Fix login error" --body-file /tmp/pr-body.md --attach ./login.png` |
| Existing PR body | `gh pr edit 123 --attach './login.png#Login error state'` |
| PR comment | `gh pr comment 123 --body "Verified login fix." --attach ./login.png` |
| New issue | `gh issue create --title "Login fails" --body-file /tmp/issue-body.md --attach ./login.png` |
| Existing issue body | `gh issue edit 123 --attach './login.png#Login error state'` |
| Issue comment | `gh issue comment 123 --body "Reproduction attached." --attach ./login.png` |

Repeat `--attach` for multiple files, up to 50 per command. `gh issue edit --attach` targets one issue at a time.
On `edit`, omitting body flags preserves the current body and appends the attachments. Supplying `--body` or `--body-file` replaces the body.

## Place images in the body

Write the body to a file with normal file tools. Reference the local paths where the images should appear:

```markdown
## Screenshots

| Before | After |
|---|---|
| ![Login error before the fix](/tmp/login-before.png) | ![Successful login after the fix](/tmp/login-after.png) |
```

Then attach those same files in the write command:

```bash
gh pr edit 123 --body-file /tmp/pr-body.md \
  --attach /tmp/login-before.png \
  --attach /tmp/login-after.png
```

For an existing body, fetch it first with `gh pr view 123 --json body --jq .body > /tmp/pr-body.md`, then edit the file.
Use `gh issue view` for issues. Creation and comments accept the same body-file workflow.

`gh` rewrites matching Markdown destinations to uploaded URLs and preserves the body's image alt text. Unreferenced attachments append at the end.
Relative paths resolve from the command's working directory, including paths written in the body file. Absolute paths avoid ambiguity.
For appended images, supply alt text after `#`, as in `--attach '/tmp/login.png#Login error state'`. Quote paths containing spaces.
Videos render as players and accept no alt text: `--attach /tmp/walkthrough.mp4`. Let `gh` generate the video reference.

## Verify the result and recover

Create and edit commands print the resource URL, rather than standalone image Markdown. Read the saved body to confirm the images are hosted:

```bash
gh pr view 123 --json body --jq .body
gh issue view 123 --json body --jq .body
```

For comments, inspect the posted comment using its returned URL or `gh pr view 123 --comments` / `gh issue view 123 --comments`.
If some uploads fail, the command can still create or update the resource with the successful files, then exit non-zero.
Inspect the returned resource and stderr before retrying. Retry only missing files on that resource; use `edit` after a partial create to avoid duplicates.

Native attachment flags do not provide a standalone upload command or direct README, gist, or Discussion uploads.
When those destinations need an existing asset, reuse the hosted reference from an authorized PR, issue, or comment in the same repository.
Create resources only when the user's task calls for them.

## Troubleshooting

| Symptom | Action |
|---|---|
| Unknown `--attach` flag | Upgrade `gh`, then check the command's help. |
| Authentication failure | Check `gh auth status` and any `GH_TOKEN` / `GITHUB_TOKEN` override; sign in with `gh auth login` if needed. |
| Write-access error or upload 404 | Confirm the selected account and target repo with `gh api repos/OWNER/REPO --jq .permissions`. |
| Read-only on the upstream of a fork PR | Upload with the `gh image` extension instead: `gh image --repo UPSTREAM_OWNER/REPO shot.png` prints `![shot.png](https://github.com/user-attachments/assets/…)`. Paste those lines into the body file. It uses the browser session from `gh image check-token`, not write access. Verified with `viewerPermission: READ` on Aprende-AS/EksamensportalenV2, 12.11.2026. |
| Local reference remains in the body | Check the attachment path, working directory, and upload errors. References inside code spans or fences are not rewritten. |
| Rejected file | Use a non-empty supported image or video file. Check stderr for type and size limits. |

Reference: [attachment release notes](https://github.com/cli/cli/releases/tag/v2.99.0), [PR edit manual](https://cli.github.com/manual/gh_pr_edit), and the installed command's `--help`.
