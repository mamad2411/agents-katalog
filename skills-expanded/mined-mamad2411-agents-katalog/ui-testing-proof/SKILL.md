---
name: ui-testing-proof
description: Test an interactive browser workflow, assert each result, record the real run, and deliver validated visual evidence.
compatibility: Requires a browser controller, patched Pagecast, Playwright Chromium, and ffmpeg. Local Chrome may require remote-debugging approval.
---

# UI testing with proof

Use the browser controller for inspection and assertions. Use Pagecast for the final recorded run.

A successful tool call does not prove the workflow passed.

## Rules

1. Test every required step and result.
2. Record the real test run. Do not reenact it later for proof.
3. Verify state after each meaningful action.
4. Stop on the first required failure and capture it.
5. Ask for passwords, MFA, consent, or ambiguous account choices.
6. Keep secrets and personal data out of media and filenames.
7. Finalize and validate media before reporting.
8. Never present a local path as a downloadable artifact.

## 1. Build the assertion list

For each step, record:

- Action.
- Observable expected state.
- Failure signal.
- Proof frame or transcript.

Define PASS, FAIL, and BLOCKED before interacting.

## 2. Inspect with the browser controller

Read the installed `browser-use` skill. Run its preflight.

Use accessibility state, stable selectors, URLs, visible text, and network evidence to learn the workflow.

If `browser-use` is unavailable, use a configured browser MCP with equivalent inspection. State the substitution.

## 3. Start Pagecast

Pagecast uses a separate browser context. It does not share Browser Use cookies.

Read `references/local-pagecast-setup.md` when setup, authentication, cursor behavior, or export matters.

Use Pagecast through MCP when available. Otherwise start the local controller:

```bash
./scripts/pagecast-controller-start.sh
./scripts/pagecast-call.py --health
```

Start the recording before the final workflow and retain its exact session ID.

## 4. Authenticate safely

For protected pages:

1. Open the page in the visible Pagecast browser.
2. Ask the user to complete protected authentication.
3. Keep the same Pagecast session alive.
4. Trim authentication from the final media when needed.

Do not automate personal credentials.

## 5. Run and assert

Use short action batches. After each batch, verify the expected state.

Check relevant signals:

- URL and title.
- Visible records or messages.
- Selected control state.
- Counts before and after filtering.
- Loading completion.
- Error banners, console errors, and failed requests.
- Persistence after refresh or navigation.

Capture screenshots at decisive states. Save evidence in a scenario-specific directory.

## 6. Finalize and validate

Stop the exact Pagecast session. Keep the source WebM and timeline until delivery is complete.

Export MP4 by default. Use GIF only when the delivery channel needs it.

Run:

```bash
./scripts/validate-evidence.sh <media-path>
```

Also inspect the first useful frame, final state, cursor, duration, and sensitive content.

## 7. Decide the result

- **PASS:** every required assertion succeeded and evidence opens correctly.
- **FAIL:** at least one required assertion failed.
- **BLOCKED:** credentials, consent, fixtures, or environment access prevented the test.

For FAIL, report the first failing step, expected state, observed state, and captured evidence.

## 8. Deliver

Upload final media and screenshots when an artifact tool exists. Use correct MIME types and returned URLs.

If upload is unavailable, state that artifacts are local. Offer the exact path without calling it downloadable.

Report the result, assertion checklist, evidence, observed values, environment, and any skipped step.
