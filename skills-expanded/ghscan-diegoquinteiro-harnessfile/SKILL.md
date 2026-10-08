---
name: video-test
description: Record a video test of any feature or user flow via Playwright. Use when the user says "record video test", "video test", "record a test", "show me the feature", "record the UI", "capture video", or wants a visual demo of a feature. Accepts a description of what to test as an argument (e.g., `/video-test the brainstorm creation flow`).
---

# Video Test

Write and run a Playwright browser test with video recording for any feature or user flow, then attach the resulting video to the PR for the current branch.

## Step 1: Understand what to test

- The user provides a description of the feature/flow to test via the skill argument or conversation context.
- If no description is provided, ask the user what they'd like to test.
- Explore the relevant frontend routes in `web/app/` and backend GraphQL schemas to understand the flow and the pages involved.
- This can be any feature or flow — not just what's being developed in the current branch.

## Step 2: Start the app stack

Start the full stack (backend + frontend + database) in E2E mode with the repo's run-app
script (a checked-in script — no skill dependency):

```bash
scripts/run-app.sh --skip-tunnels
```

The script outputs the ports and RUN_ID. Parse them from the output:
- `RUN_ID` — needed for cleanup
- `FRONTEND_PORT` — the port the frontend is running on
- `BACKEND_PORT` — the port the backend is running on

Ensure Playwright and Chromium are installed in `e2e/`:
```bash
cd e2e && npm install && npx playwright install chromium
```

### How E2E auth works

The `/run-app` script runs in E2E mode by default:
- **Frontend**: Clerk auth is bypassed, Apollo sends `X-E2E-User-Id`/`X-E2E-Org-Id` headers
- **Backend**: E2E auth middleware recognizes headers and sets user/account context

No Clerk login flow is needed. All authenticated pages are accessible.

## Step 3: Write the Playwright test

Create `e2e/tests/<feature>.video.spec.ts`. Key requirements:

- Import `test` and `expect` from `@playwright/test`
- Use the `page` fixture (browser context), NOT the `request` fixture
- **Name the file `<feature>.video.spec.ts`** (the `.video.spec.ts` suffix matters — see below).
- **Do NOT hard-code `video.size` via `test.use`.** Video size and viewport come from the Playwright `projects` (`desktop` 1280×720 + `mobile` iPhone 13) in `e2e/playwright.config.ts`. The `mobile` project is scoped (via `testMatch`) to `*.video.spec.ts` only, so a correctly-named video spec runs once per project — producing a desktop and a mobile video automatically — while the rest of the suite stays desktop-only. If you need a per-run `baseURL`, set only that:
  ```typescript
  test.use({ baseURL: "http://localhost:<FRONTEND_PORT>" });
  ```
- **Pre-warm the route before the watchable part** to avoid the long white intro: in dev (`yarn dev`) Next compiles the route on first hit, which is the main cause of the blank video start. Begin the test by navigating and waiting for the UI to actually mount, *before* any deliberate pause:
  ```typescript
  await page.goto("/path");
  await page.waitForLoadState("networkidle");
  await expect(page.getByRole("main")).toBeVisible(); // an anchor that proves the UI mounted
  ```
- **Use `{ force: true }` on click actions** — the app has overlay elements (sidebar, page containers) that can intercept pointer events
- Add deliberate pauses (`await page.waitForTimeout(2000)`) at key moments so the video is watchable
- **Capture anchor screenshots (3–4 per viewport)** at the key moments of the flow, so reviewers get quick visual evidence without watching the video. Prefix the filename with the project name so desktop and mobile don't collide, and save under a predictable per-project folder:
  ```typescript
  const shotDir = `test-results/${test.info().project.name}/screenshots`;
  // (1) first useful screen, (2) main action, (3) result/final state, (4) optional confirmation
  await page.screenshot({ path: `${shotDir}/01-first-screen.png` });
  // ...later, after the main interaction:
  await page.screenshot({ path: `${shotDir}/02-main-action.png` });
  // ...at the result/final state:
  await page.screenshot({ path: `${shotDir}/03-result.png` });
  ```
- Use try/catch around actions that might fail (e.g., dropdown selections, navigation waits) to keep the video recording going
- Use descriptive test names that explain what is being demonstrated

The test file should be a **real integration E2E test** that will be committed to the project under `e2e/tests/`. Name it descriptively based on the feature **with the `.video.spec.ts` suffix** (e.g., `brainstorm-creation.video.spec.ts`, `search-flow.video.spec.ts`). The suffix is what opts the spec into the dual desktop+mobile recording (the `mobile` project's `testMatch`); a plain `*.spec.ts` name would only record desktop. Do NOT use generic names like `video-recording.video.spec.ts`. The test should have proper assertions that verify the feature actually works — do NOT use try/catch to swallow failures.

## Step 4: Run the test (desktop + mobile)

Run the spec across **both** viewports (the `desktop` and `mobile` projects defined in `playwright.config.ts`):

```bash
cd e2e && npx playwright test tests/<feature>.video.spec.ts
```

This produces one video per project. Playwright saves them under
`e2e/test-results/<...>-<project>/video.webm` and the screenshots under
`e2e/test-results/<project>/screenshots/`. To record a single viewport, add
`--project=desktop` or `--project=mobile`.

The video is saved even if the test fails. If the test fails, review the error
and the error-context.md file (contains a page snapshot). Fix the test and
re-run. Iterate until the test passes and produces a good video on both
viewports.

## Step 5: Trim the white intro from each video (ffmpeg)

Even with the route pre-warmed, Playwright starts recording when the browser
context is created — a fraction of a second before the first useful frame. Trim
that residual head off each `.webm` so the video opens on real UI:

```bash
for VIDEO in $(find e2e/test-results -name "*.webm" -type f); do
  TRIMMED="${VIDEO%.webm}.trimmed.webm"
  # Simple, robust: drop a conservative fixed head (~1.5s).
  ffmpeg -y -ss 1.5 -i "$VIDEO" -c copy "$TRIMMED" && mv "$TRIMMED" "$VIDEO"
done
```

If a fixed offset still leaves white (e.g. a slow first compile), detect where
the white intro ends and cut from there. The intro is **white** (luma ~235), so
`blackdetect` alone won't catch it — `negate` first so white becomes black, then
`blackdetect`'s `black_end` marks the moment the UI appears:

```bash
START=$(ffmpeg -i "$VIDEO" -vf "negate,blackdetect=d=0.1:pic_th=0.98" -an -f null - 2>&1 \
  | grep -oP 'black_end:\K[0-9.]+' | head -1)
ffmpeg -y -ss "${START:-1.5}" -i "$VIDEO" -c copy "$VIDEO.trimmed.webm"
```

## Step 6: Attach key screenshots to the Multica issue

The anchor screenshots go on the **issue** (where humans review), while the
video goes on the PR (Step 7). Collect the PNGs and attach them in a single
comment. The issue ID comes from the task context (e.g. `ALT-147`'s UUID); if it
is not available, skip this step and just report the local screenshot paths.

```bash
SHOTS=$(find e2e/test-results -path '*/screenshots/*.png' -type f | sort)
ATTACH=$(printf -- '--attachment %q ' $SHOTS)
multica issue comment add <ISSUE_ID> \
  --content "Visual E2E evidence (desktop + mobile) — key moments of the flow." \
  $ATTACH
```

## Step 7: Attach video to PR

1. Find the video files (one per viewport):
   ```bash
   VIDEO_PATHS=$(find e2e/test-results -name "*.webm" -type f | sort)
   ```

2. Upload each .webm directly to catbox.moe (no GIF conversion needed — GitHub renders video links):
   ```bash
   VIDEO_URL=$(curl -s -F "reqtype=fileupload" -F "fileToUpload=@$VIDEO_PATH" https://catbox.moe/user/api.php)
   ```
   Do this for both the desktop and mobile videos and keep both URLs.

3. Get the current branch and PR:
   ```bash
   PR_JSON=$(gh pr view --json number,url 2>/dev/null)
   ```

   If no PR exists, create one:
   ```bash
   BRANCH=$(git branch --show-current)
   gh pr create --title "$BRANCH" --body "## Summary

   (auto-created by video-test skill)

   🤖 Generated with [Claude Code](https://claude.com/claude-code)"
   PR_JSON=$(gh pr view --json number,url)
   ```

4. Post a PR comment with **both** videos linked:
   ```bash
   PR_NUMBER=$(echo "$PR_JSON" | jq -r '.number')
   gh pr comment "$PR_NUMBER" --body "## Video Test

   ▶️ [Desktop recording]($DESKTOP_VIDEO_URL)
   ▶️ [Mobile recording]($MOBILE_VIDEO_URL)

   Recorded with Playwright on $(date -u +%Y-%m-%dT%H:%M:%SZ)"
   ```

5. **Fallback** if catbox upload fails: Tell the user the local path to the .webm file and suggest they drag-and-drop it into the PR on GitHub's web UI. On macOS: `open <path>` to preview.

## Step 8: Cleanup

```bash
scripts/stop-app.sh $RUN_ID
```

## Step 9: Report results

- Confirm whether the videos (desktop + mobile) were attached to the PR and the screenshots to the issue
- Include the PR URL
- Report the local video/screenshot paths as backup
- **Return the VIDEO_URLs** so callers can attach them to the Multica issue or the PR
