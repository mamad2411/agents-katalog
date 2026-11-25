---
name: verify
description: Review the delivered diff against the plan, then run checks sized to the change's impact radius (P0–P5 discovery).
allowed-tools:
  - read
  - search_files
  - list_dir
  - bash
  - task_output
  - task_list
  - task_stop
  - tool_search
  - tool_describe
  - tool_call
  - update_plan
---

## Acceptance flow

Follow this order exactly:

```text
review diff against plan → fix confirmed issues → verify by impact radius

   development complete
          │
          ▼
   [1] Review against the plan
        · compare the diff against the plan
        · deviations / omissions / scope creep / over-design / P0 · P1
        · fix confirmed issues before going on
          │
          ▼
   [2] Verify by impact radius
        · cover affected boundaries:  L0 / L1 / L2 / L3
        · reuse still-valid results; run missing or affected checks
          │
          ▼
   [2b] UI acceptance          (only when the change is user-visible)
        · render the page + capture PNG / ARIA / console evidence
          │
          ▼
     accept / close out
```

Do not run the full suite by default. Move to L3 only when the change touches core/shared/infra code, configuration, build files, dependency manifests or lockfiles, a wire/protocol contract, multiple packages, or the user explicitly requests it.

## Review against the plan

Before final verification, inspect the current `git diff` against the active plan:

1. Check every promised behavior and deliverable: flag a plan deviation, omitted item, or changed scope.

2. Challenge unreasonable implementation and over-design. A mechanism is over-designed when it exists for a scenario outside this change's impact radius or requirements and deleting it would still leave this change's acceptance checks green.

3. Look for P0 issues (correctness, crashes, data loss, security, or a broken build) and P1 issues (user-visible defects or a material mismatch with the plan). Fix confirmed issues before accepting the change.

4. Add or update the regression check that owns any behavior changed while fixing.

## Verify by impact radius

Produce real evidence that the current code builds and passes its checks — do not describe what would be tested.

1. First identify the project and its documented verification commands. Use this order:

   - P0: an explicit command from the user or the approved plan;
   - P1: repository instructions such as `AGENTS.md`, `CLAUDE.md`, `CONTRIBUTING.md`, or the nearest README;
   - P2: the nearest project manifest and its scripts/tasks;
   - P3: workspace-level configuration or CI workflow;
   - P4: a narrowly scoped smoke command inferred from the changed code;
   - P5: if no runnable command can be found, explain that fact with the files inspected and run the smallest safe parse/type/build check available.

2. Choose the initial verification scope, then reuse valid results:

   - Ladder: for what the diff actually touched, widen from the change outward until every affected boundary is covered:

     L0 the tests owning the changed files;

     L1 the whole package / crate / module that owns them, plus that package's lint or typecheck;

     L2 every package that depends on it, when the change touches a public API, an exported symbol, a shared type, or a wire/protocol contract;

     L3 the project's full documented check set, when the change touches core/shared/infra code, configuration, build files, dependency manifests or lockfiles, spans several packages, or the plan names it.

     Compute dependents from the project's own graph (for example `cargo tree -i <crate>`, workspace manifests, or package imports) instead of guessing.

   - Reuse: keep successful results whose relevant source, tests, dependencies, configuration, and environment are unchanged. Run only missing or invalidated checks. If validity is uncertain, investigate before relying on the result. A previous full run does not require another full run after every fix; a full project run is not the default.

   Do not invent project tests or claim visual checks that do not exist.

3. Start every verification command with `bash(run_in_background=true)`. If the next step does not strictly depend on its result, do other independent work and wait for `<background-task-finished>`. If it does, call `task_output(block=true)` with a realistic wait slice until it finishes.

4. Treat a command as passed only when it has finished successfully with exit code 0. If discovery finds no meaningful command, report the concrete missing verification path rather than claiming success.

## UI acceptance

For a user-visible web, frontend, or VS Code webview change, verify the rendered result in addition to the project's normal checks. A build, typecheck, or DOM-only test does not prove that the page is visible, positioned correctly, or free of browser runtime errors.

1. Discover the project's documented way to start a local development server. Start it with `bash(run_in_background=true)`, then use `task_output` to obtain the actual URL and confirm the server is ready before opening it.

2. Prepare the managed browser runtime explicitly when needed:

   ```text
   node <work_dir>/skills/verify/scripts/bootstrap.mjs
   ```

   `bootstrap.mjs` installs the locked Node dependency and Chromium. `shot.mjs` never installs dependencies or browsers during acceptance; if they are missing, run bootstrap and record its outcome instead of claiming the browser is unavailable.

3. Capture the three evidence types with a background task:

   Before choosing an output directory, read `workspace.project_resource_dir` from the active Tomcat configuration. It defaults to `.agents`. Pass the resolved project directory explicitly to `--out` so a custom setting such as `.workspace-data` stores screenshots under `.workspace-data/shots`; never rely on the script default for a custom configuration.

   ```text
   node <work_dir>/skills/verify/scripts/shot.mjs <url> \
     --out <workspace>/<project_resource_dir>/shots --name <screen> --viewport 1440x900
   ```

   This writes `<screen>.png` (visual truth), `<screen>.aria.txt` (structure), and `<screen>.console.json` (browser runtime). A page error or `console.error` makes the shot task fail. Its exact command and successful task ID are valid verification evidence for the delivery record.

4. Read all three artifacts. Use the PNG for blank screens, clipping, overlap, spacing, color, and layout; use ARIA for roles, labels, and expanded/disabled state; use console output for runtime faults. For responsive UI, capture at least desktop and a narrow viewport such as `390x844`.

5. Fetch or curl important JavaScript, CSS, image, or API subresources when relevant. HTML `200` alone does not prove that the page's dependent assets or data loaded.

6. Do not rationalize a missing check. “Looks right”, “cannot run a browser”, or “the screenshot is probably fine” is not evidence. Diagnose the concrete cause: dev server URL, browser bootstrap, selector/readiness condition, asset request, or browser console error. If it cannot be resolved, leave acceptance open with the artifacts and failure evidence.

For a known fixed interaction sequence, encode it in a deterministic headless script. When the next interaction depends on what the previous page state looks like, discover configured Playwright tools through the deferred connector path: `tool_search(source="playwright")` → `tool_describe(names=[...])` → `tool_call(name="mcp__playwright__...", arguments={...})`. Retain screenshots and structural evidence from that interaction loop. Never assume Playwright is configured: if the source search is empty or reports an error, report that fact.

For a visual screenshot that must return to the model through Playwright MCP, call `tool_call(name="mcp__playwright__browser_take_screenshot", arguments={...})` **without** `filename` and without `fullPage=true`. Current `@playwright/mcp` intentionally saves a filename/full-page capture to disk and returns only a Markdown file link; it omits the image content needed for the model vision loop. Use the default viewport screenshot for visual judgement.

## Artifacts and delivery

- Put temporary helper scripts, reports, and replay captures under `<project_resource_dir>/scripts`, `acceptance`, and `replays` (resolved as in UI acceptance). Code, tests, fixtures, and docs the project keeps maintaining stay in their normal locations.
- If acceptance produced screenshots, embed every final PNG behind the verdict, failures included, one `![feature · viewport](/absolute/path.png)` each, and match the count before replying. Skip only debug or superseded shots; never substitute a representative image, collage, or folder link.
