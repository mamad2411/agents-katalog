---
name: playwright-e2e-visual-testing
description: Build or strengthen Playwright browser E2E tests with deterministic production-component fixtures, mobile Vision inspection, MP4 evidence, hit-testing, screenshots, contact sheets, and structured reports. Use for UI fixes, responsive/interaction audits, visual regression, or requests for complete video end-to-end visual proof.
version: 2.2.0
license: MIT
metadata:
  hermes:
    tags: [playwright, e2e, vision, visual-regression, video, mobile, web-testing]
    related_skills: [test-driven-development, systematic-debugging, web-visual-verify, requesting-code-review]
---

# Playwright E2E Vision Testing

Prove behavior, geometry, pointer reachability, and rendered appearance. DOM assertions alone are not Vision verification, and a video alone is not a test.

## Required companion workflow

1. Load and follow `test-driven-development` for product changes.
2. Use this skill for browser acceptance and evidence.
3. Use `systematic-debugging` for unexpected failures; understand the root cause before editing.
4. Run `requesting-code-review` before committing or pushing.

## Definition of done

A workflow passes only when all of the following are true:

- behavior assertions pass after the action that should cause them;
- geometry, overflow, stacking, and pointer-hit checks pass;
- **one single unified, continuous walkthrough video (H.264 MP4)** is produced covering the full workflow journey (do not fragment into separate mini-videos per page);
- **the agent directly reads and inspects the video (using `view_file` on the MP4) and snapshot images with Vision tools** to verify layout, rendering, contrast, interactive flow, and **confirm ZERO transient error banners, alert messages, failed toasts, or glitch states** throughout the entire playback;
- **讀影片的時候要看有沒有任何 error message（無論是紅色/黃色 Alert Banner、對話內的錯誤訊息、未預期的狀態異常或例外崩潰）。一旦發現任何 error message，嚴禁忽略或當作通過，必須暫停並進行深度的 root cause 排查與 debug，找出根本原因並修復後重新錄製。**
- **any visual error banner, alert notification, or failed status indicator (e.g. red error bar, network retry, "任務暫時無法讀取", etc.) seen in video playback immediately invalidates the run**, even if the process exited with code 0 or later completed in the background;
- the passing run produced a valid, validated MP4 at the target viewport;
- there are no unexpected page or console errors;
- the report states exactly what was and was not exercised.

Do not report “0 visual violations” from DOM checks or exit codes alone without directly reading the walkthrough video with `view_file` and thoroughly verifying all video frames and snapshot images.

## 1. Establish the visual contract

Before writing a test:

- read project instructions, `DESIGN.md`, existing Playwright config, tests, app entry points, and relevant components/CSS completely;
- identify the requested workflow and every child state reachable inside it: menus, drawers, dialogs, popovers, editors, loading/streaming states, attachments, confirmations, and close/back behavior;
- translate design requirements into explicit checks, for example minimum target size, viewport containment, internal scrolling, ghost/active states, safe areas, and icon semantics;
- default to `390 × 844`, `isMobile: true`, `hasTouch: true` for a phone-first app unless the product defines another target;
- choose focused workflow coverage by default; sweep every application page only when the user asks for a site-wide audit.

Create a milestone list before automation. Number screenshot names in workflow order, such as `00-launcher.png`, `01-open.png`, and `02-model-picker.png`.

## 2. Start RED, then fix the root cause

Add the smallest failing contract before changing production behavior. Useful RED checks include:

- a CSS/source contract for required hit-area, overflow, or stacking rules;
- a rendered target below the required size;
- a popup outside the visual viewport;
- `document.elementFromPoint()` returning an overlay instead of Send/Stop;
- a modal failing to block the control beneath it;
- a long list that cannot scroll internally.

Run the exact test and confirm the failure represents the bug, not a selector typo, stale server, unavailable browser, or missing fixture. Keep unit/source contracts and rendered Playwright checks: they catch different regressions.

## 3. Use isolated deterministic state with production UI

Render the real production entry point, components, and CSS unchanged. Determinism may come from API fixtures or Playwright route interception at the network boundary; do not copy styles into a test-only page or patch the DOM to make assertions pass.

The isolated environment must:

- bind local services to loopback only;
- use disposable data and a dedicated account/session;
- disable caches that could serve stale frontend assets;
- expose health endpoints or otherwise prove readiness before testing;
- model enough data to stress the UI: long labels, overflow lists, busy/streaming output, confirmation dialogs, proposal/result states, and attachment previews where relevant;
- return state transitions that correlate to real clicks rather than merely presenting the final state.

Credentials, URLs containing secrets, tokens, and personal data must not appear in source, screenshots, reports, or logs. Require secrets through named environment variables and fail early with a clear message when absent. For live deployments, make the run explicitly opt-in.

Record exact service PIDs and ports. On completion, stop only those processes and remove disposable test data; never use broad `pkill`, `killall`, or unrelated service restarts.

## 4. Configure evidence-first recording

Use project-appropriate equivalents of:

```ts
use: {
  viewport: { width: 390, height: 844 },
  isMobile: true,
  hasTouch: true,
  video: 'on',
  screenshot: 'only-on-failure',
  trace: 'retain-on-failure',
}
```

Also configure a stable named browser project, a dedicated output directory, and list/HTML reporters when the project supports them. Keep evidence in an ignored artifact directory unless the repository explicitly commits reviewed baselines.

Playwright records WebM natively. Treat that file as an intermediate and transcode it—never merely rename its extension—to an H.264 MP4 for inspection and delivery:

```bash
skill_dir="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills/software-development/playwright-e2e-visual-testing"
"$skill_dir/scripts/webm-to-mp4.sh" \
  artifacts/<run>/videos/workflow.webm \
  artifacts/<run>/videos/workflow.mp4
```

The converter writes H.264 with `yuv420p` and `faststart`, then validates the result with `ffprobe`. Keep the WebM only as a temporary/native diagnostic source; delete it only after the MP4 passes validation.

### Unified Video Recording Principle
- Record **ONE single complete walkthrough video (MP4)** for the entire user workflow or test suite session rather than generating fragmented video files per page or step.
- Capture distinct **milestone snapshot images (PNG)** for every page, dialog, or key state transition.

A complete focused audit should produce:

```text
artifacts/<run>/
├── screenshots/
│   ├── 01_login.png
│   ├── 02_dashboard.png
│   ├── ...
├── videos/
│   └── full_workflow.mp4
├── contact-sheet.png
├── metrics.json
├── report.md
└── logs/
```

Do not commit generated videos, traces, reports, credentials, or disposable data unless the user explicitly requests it. Reviewed screenshot baselines may be committed when they are part of the test suite.

## 5. Add a permanent Playwright test and document it

Do not leave the result only as an ad-hoc audit script. When the repository supports Playwright, add or update a maintained spec under its normal E2E directory, for example `tests/e2e/<feature>-vision.spec.ts`. Reuse the project's fixtures and config rather than creating a second test framework.

The permanent test must cover the regression that motivated the visual work. Keep large fixture builders in support modules, but retain the acceptance assertions in the spec so future maintainers can see what is protected.

Use a project-appropriate version of this documented test pattern:

```ts
import { expect, test, type Locator, type Page } from '@playwright/test'

async function expectPointerReachable(locator: Locator) {
  const result = await locator.evaluate((element) => {
    const rect = element.getBoundingClientRect()
    const hit = document.elementFromPoint(
      rect.left + rect.width / 2,
      rect.top + rect.height / 2,
    )
    return {
      reachable: hit === element || Boolean(hit && element.contains(hit)),
      blocker: hit instanceof HTMLElement
        ? hit.getAttribute('aria-label') || hit.className || hit.tagName
        : null,
    }
  })
  expect(result, `pointer blocker: ${result.blocker}`).toMatchObject({ reachable: true })
}

async function visibleUndersizedTargets(page: Page) {
  return page.locator('button, a, input, textarea, select, [role="button"]').evaluateAll(
    (elements) => elements.flatMap((element) => {
      const rect = element.getBoundingClientRect()
      const style = getComputedStyle(element)
      if (style.display === 'none' || style.visibility === 'hidden' || rect.width <= 1 || rect.height <= 1) return []
      if ((element as HTMLButtonElement).disabled || element.closest('[inert]')) return []
      return rect.width < 44 || rect.height < 44
        ? [{
            label: element.getAttribute('aria-label') || element.textContent?.trim(),
            width: rect.width,
            height: rect.height,
          }]
        : []
    }),
  )
}

test('mobile workflow remains visually and interactively usable', async ({ page }, testInfo) => {
  const pageErrors: string[] = []
  const consoleErrors: string[] = []
  page.on('pageerror', (error) => pageErrors.push(error.message))
  page.on('console', (message) => {
    if (message.type() === 'error') consoleErrors.push(message.text())
  })

  await page.goto('/')
  await expect(page.getByRole('main')).toBeVisible()

  await test.step('open and capture the primary state', async () => {
    await page.getByRole('button', { name: /open/i }).click()
    await expect(page.getByRole('dialog')).toBeVisible()
    await page.screenshot({ path: testInfo.outputPath('01-open.png') })
  })

  await test.step('verify popup containment and internal overflow', async () => {
    await page.getByRole('button', { name: /model|menu/i }).click()
    const popup = page.getByRole('listbox')
    await expect(popup).toBeVisible()
    const contained = await popup.evaluate((element) => {
      const rect = element.getBoundingClientRect()
      const viewport = window.visualViewport
      const width = viewport?.width ?? window.innerWidth
      const height = viewport?.height ?? window.innerHeight
      return rect.left >= 0 && rect.top >= 0 && rect.right <= width && rect.bottom <= height
    })
    expect(contained).toBe(true)
  })

  await test.step('prove the critical action receives a real pointer click', async () => {
    const action = page.getByRole('button', { name: /send|save|submit/i })
    await expectPointerReachable(action)
    await action.click()
    await expect(page.getByText(/complete|saved|sent/i)).toBeVisible()
  })

  expect(await visibleUndersizedTargets(page)).toEqual([])
  expect(pageErrors).toEqual([])
  expect(consoleErrors).toEqual([])
  await expect(page.getByRole('dialog')).toHaveScreenshot('mobile-workflow.png', {
    animations: 'disabled',
    caret: 'hide',
  })
})
```

Adapt selectors and assertions to the real workflow; never copy generic `/open|send/` selectors unchanged when they could match the wrong control. The test must verify the result of each click, not only that the click call returned.

Update the project's `README.md`, testing guide, or closest maintained developer document with a section like:

```md
## Playwright E2E Vision verification

- Spec: `tests/e2e/<feature>-vision.spec.ts`
- Run: `npx playwright test tests/e2e/<feature>-vision.spec.ts`
- Update reviewed baselines: `npx playwright test tests/e2e/<feature>-vision.spec.ts --update-snapshots=all`
- Required environment variables: `<names only; never values>`
- Evidence: `test-results/` or `artifacts/<run>/`
- Covered workflow: `<ordered milestone list>`
```

If the project intentionally keeps the evidence runner outside the permanent suite, document why, where it lives, its exact run command, and which maintained test protects the underlying regression. “The video exists” is not sufficient documentation.

## 6. Exercise behavior with real user input

At every milestone:

1. perform the real pointer, touch, keyboard, upload, or scroll action;
2. wait on a uniquely correlated observable result;
3. assert state and geometry;
4. capture a screenshot;
5. collect page and console errors.

Do not use `evaluate(() => element.click())` as proof that a visible control is clickable. For critical controls such as Send, Stop, Save, Delete, Close, and submit actions, first hit-test them, then use Playwright's normal `click()` and verify the resulting network/state transition.

Avoid fixed sleeps except when deliberately creating overlap between two actions. A condition that was already true before the action cannot prove the action succeeded. For streaming output, capture pre-action state, require command-specific output, exclude partial rows, and verify Stop changes the durable job state.

## 7. Add quantitative rendered checks

### Visual viewport containment

For drawers, menus, pickers, dialogs, and popovers, compare their bounding boxes with `window.visualViewport` (fall back to `innerWidth/innerHeight`). Check all four edges, not only document overflow.

### Horizontal overflow

Assert both:

- the document and full-screen drawer do not exceed their client width;
- intentionally wide content scrolls inside its designated container.

For a long menu/list, prove `scrollHeight > clientHeight`, perform an internal scroll, and verify `scrollTop` changes while the page remains fixed.

### Touch target size

Measure every visible, enabled, non-inert scoped control. On phone/coarse-pointer layouts, enforce the product contract, commonly at least `44 × 44px`. Report selector/name, dimensions, and state for every violation. Exclude only documented semantic exceptions; never silently filter a failing target.

Icon-only controls must remain semantic buttons with accessible names even when their visual surface is transparent.

### Pointer reachability

For each critical action:

```js
const rect = element.getBoundingClientRect();
const x = rect.left + rect.width / 2;
const y = rect.top + rect.height / 2;
const hit = document.elementFromPoint(x, y);
const reachable = hit === element || element.contains(hit);
```

Record the blocking element when `reachable` is false. Then execute a normal Playwright click. This catches invisible resize handles and stacking overlays that DOM visibility checks miss.

### Modal stacking

When a modal is open, verify:

- its backdrop/dialog is the hit-test result above underlying controls;
- the underlying control cannot receive the pointer;
- the modal's own action remains reachable;
- focus/close behavior returns to the expected state.

### Errors

Collect `pageerror`, failed requests relevant to the workflow, and console errors. Allowlist only specific understood messages, such as a known unauthenticated probe, and list them explicitly in the report. Never use a broad console-error ignore.

## 8. Capture complete workflow evidence

Cover the full scoped state machine, not only the happy-path first screen. A representative interactive workflow includes:

- idle launcher/control;
- drag versus stationary-touch/click behavior;
- full drawer/window open;
- every resize surface if the component exposes them;
- overflow menu or long model/data picker;
- destructive confirmation;
- rename/edit settings;
- configured/active visual state;
- management/editor dialog;
- image/file attachment and removal;
- real Send and Stop actions;
- streamed reply/result/proposal;
- close and restoration of the original launcher/control.

Use deterministic long lists and long labels to expose clipping. Capture intermediate states before closing them.

## 9. Perform direct Vision & Video inspection

After the passing run, the agent **MUST directly read and inspect the produced walkthrough video (`full_workflow.mp4`) using `view_file`** in addition to the milestone snapshot images:

- **Direct Video Reading (`view_file`)**: Call `view_file(AbsolutePath="/path/to/workflow.mp4")` to watch the complete continuous video recording.
- **Inspect Full Temporal Flow**: Review animation fluidity, page navigation transitions, gesture handling, streaming responses, and responsive state updates throughout the video.
- **Scrutinize Intermediate Frames for Error Messages**: 讀影片的時候要看有沒有任何 error message（無論是紅色/黃色 Alert Banner、對話內的錯誤訊息、未預期的狀態異常或例外崩潰）。Check every second of playback for transient error messages, red notice bars (such as "Agent 任務暫時無法讀取", "無法載入", "伺服器忙碌", network retry toasts, or unexpected popup warnings). If any error banner flashes or stays visible at any point, the run is **FAILED**.
- **Mandatory Root Cause Debugging (發現任何錯誤訊息必須深入 Debug Root Cause)**:
  若在影片閱讀或截圖檢視中發現**任何** error message、錯誤提示、警告條或非預期狀態：
  1. **嚴禁視而不見或當作通過**：即使自動化測試腳本 exit code 為 0，只要畫面出現 error message，該次測試即判定為不合格。
  2. **定位完整呼叫鏈與日誌**：查閱相關 API endpoint、後端服務日誌（`data/logs/`）、瀏覽器控制台錯誤以及資料庫狀態。
  3. **找出根本原因（Root Cause）**：分析是後端資料缺失（如未同步行情表）、狀態機非法跳轉、例外被吞噬或前端過早渲染空狀態等根本原因。
  4. **實作修復並重啟/重建**：在程式碼層面徹底根治問題，完成單元與整合測試。
  5. **重新執行 Video Test**：重新執行完整的 E2E 流程並錄製新影片，再次調用 `view_file` 仔細檢視，確保最終交付的影片 100% 零任何 error message。
- **Inspect Static Snapshots & Contact Sheet**: Check visual geometry, spacing rhythm, touch targets, and layout stability.

Inspect actual pixels and playback frames for:

- **Zero unwanted error banners, red alerts, or failure toasts**;
- clipping at all viewport edges;
- overlap, occlusion, and incorrect z-order;
- cramped fields, truncated labels, or hidden list items;
- visual hierarchy, spacing rhythm, and consistent icon language;
- ghost versus configured/active surfaces;
- contrast and adjacent-color interaction in the rendered theme;
- safe-area and fixed-navigation obstruction;
- loading, empty, error, streaming, confirmation, and restored states.

Record the Vision conclusion separately from automated metrics. If pixels or video playback reveal an error banner, visual glitch, or defect, diagnose the root cause, fix it, and rerun the entire workflow so the final video contains only clean, correct behavior.

## 10. Build the contact sheet, metrics, and report

Create a chronological contact sheet from milestone screenshots without deleting the originals. Keep labels legible and preserve aspect ratio.

`metrics.json` should include:

- viewport, browser, video codec/dimensions/duration;
- ordered milestone/check names and pass/fail values;
- measured target violations with dimensions;
- overflow, viewport, hit-test, and modal-blocking results;
- page/console errors and documented allowlisted messages;
- overall violation count.

`report.md` should include:

1. scope, fixture isolation, viewport, and overall result;
2. fixes or requirements verified;
3. the recorded workflow in order;
4. automated check results;
5. direct Vision findings;
6. build/unit/E2E/lint/typecheck/review gates;
7. known unrelated baseline failures, clearly separated;
8. artifact paths and anything not inspected.

Do not claim complete coverage without naming the traversed states.

## 11. Verify artifacts and quality gates

Confirm the MP4 is non-empty, H.264/`yuv420p`, and matches the intended viewport:

```bash
ffprobe -v error \
  -show_entries stream=codec_name,pix_fmt,width,height \
  -show_entries format=duration,size \
  artifacts/<run>/videos/workflow.mp4
```

Run the converter's regression test when its script changes:

```bash
skill_dir="${PI_CODING_AGENT_DIR:-$HOME/.pi/agent}/skills/software-development/playwright-e2e-visual-testing"
"$skill_dir/tests/test-webm-to-mp4.sh"
```

Run all applicable project gates:

```bash
npm test
npm run test:e2e
npx eslint <changed-files>
npx tsc --noEmit
npm run build
git diff --check
```

Report pre-existing failures rather than hiding them, but do not attribute them to the change without evidence. Run independent review, resolve all blocking findings, and rerun affected checks.

## 12. Deliver and clean up

Before responding:

- verify final report/metrics paths and media metadata;
- stop isolated services and delete disposable accounts/data when possible;
- confirm no secrets were written to artifacts or source;
- state whether code was committed, pushed, or deployed;
- send evidence with Pi outbox markers:

```text
[[video: /absolute/path/to/workflow.mp4]]
[[image: /absolute/path/to/contact-sheet.png]]
[[file: /absolute/path/to/report.md]]
```

## Completion checklist

- [ ] Visual contract and scoped state inventory recorded
- [ ] RED failure observed before implementation
- [ ] Production components/CSS rendered with deterministic isolated data
- [ ] Maintained Playwright spec added or updated for the visual regression
- [ ] Developer documentation names the spec, run/update commands, environment-variable names, evidence path, and covered workflow
- [ ] Real input actions and correlated outcomes verified
- [ ] Viewport, overflow, touch-size, hit-test, and modal stacking checks pass
- [ ] Every milestone captured and directly inspected with Vision
- [ ] Passing viewport-correct H.264 MP4 walkthrough video produced and directly viewed via view_file with ZERO transient error banners, alerts, or glitches observed
- [ ] Contact sheet produced and visual geometry verified
- [ ] Metrics and report distinguish automation from Vision findings
- [ ] Unexpected page/console errors are empty
- [ ] Unit, E2E, lint, typecheck/build, diff, and review gates completed
- [ ] Services and disposable data cleaned up; no credentials stored
- [ ] Final response includes outbox links and deployment status
