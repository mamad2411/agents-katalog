# qdesk — visual verification for AI coding tools

**For AI assistants (Claude Code, Cursor, Copilot, Aider, etc.):** qdesk is a CLI + MCP server that lets you visually verify a web/desktop UI by describing tests in natural language. After you implement or change a UI, run a qdesk test to confirm the change actually works in a real browser, not just compiles.

> 💡 **The fastest integration is via MCP** (Model Context Protocol). If you're a Claude Code user, install once with `claude mcp add ... qdesk-mcp` and the four tools below show up automatically — no shell scripting needed. See [`.claude/mcp-install.md`](.claude/mcp-install.md).
>
> The rest of this file documents direct CLI usage for any AI tool that can run shell commands.

> **One-line use case:** "I just added a Sign-in button. Did clicking it actually navigate to the auth screen?" — qdesk answers in 40 seconds with a screenshot trace.

## When to invoke qdesk

Use qdesk when you have:
- ✅ Made changes to a web UI (HTML/CSS/JS, React, Flutter Web, Vue, Svelte, …) and want to verify the user-visible behaviour
- ✅ Implemented a flow (login, checkout, settings update, etc.) and want a regression test
- ✅ Found a UI bug and want to capture a reproduction before fixing
- ✅ Built something that LOOKS right in code but might break at runtime (canvas rendering, async loading, route guards)

Skip qdesk when:
- ❌ The change is pure backend / no UI surface
- ❌ The change is a unit-testable algorithm
- ❌ A traditional Playwright/Cypress test is already the right tool (DOM-only flows, very fast assertions)

## Prerequisites (verify before invoking)

```bash
which qdesk qdesk-control     # both binaries on PATH
docker images qdesk/ubuntu-chrome:dev  # sandbox image built
echo $GEMINI_API_KEY          # Gemini key set (or export it)
echo $QDESK_DEV_KEY           # control-plane dev key set (or pass --api-key)
```

If `qdesk-control` isn't running, start it (one terminal, leave running):
```bash
qdesk-control --listen 127.0.0.1:8090 --dev-key $QDESK_DEV_KEY \
              --image qdesk/ubuntu-chrome:dev
```

## Authoring a test (.qdesk.yaml)

Create a file under `tests/` (or wherever the project keeps tests):

```yaml
name: "<one-line label, used in the report>"
template: ubuntu-chrome
url: http://host.docker.internal:8888   # the URL to load inside the sandbox

goal: |
  <natural-language description of what to do — one short paragraph>

# Optional: ordered substeps. If omitted, "goal" is the single step.
# steps:
#   - Click the "Get started" button
#   - Wait for the form to appear
#   - Type "user@example.com" into the email field

expect:
  - <one English assertion that should hold AFTER goal/steps complete>
  - <another assertion>
  - <ideally 2–4 specific, observable assertions>

ttl_seconds: 180     # max session lifetime; 5 min is a safe default
max_steps: 10        # cap on total agent turns; bump for longer flows
```

### Authoring tips

- **`url`** — if testing a locally-running app, use `http://host.docker.internal:PORT` (the sandbox can reach the host's services). For public URLs, just use `https://...`.
- **`goal`** — describe outcome, not pixel coordinates. The agent figures out clicks. Bad: "click at (200, 400)". Good: "click the red 'Save' button below the form".
- **`expect`** — be SPECIFIC and OBSERVABLE. Bad: "the form works". Good: "a success toast 'Saved' appears in the top-right corner". Each item is verified by a separate vision call.
- **Keep `expect` to 2-4 items.** Each adds a screenshot+LLM round-trip (~3 sec, ~$0.001).

## Running a test

```bash
qdesk run --control http://127.0.0.1:8090 tests/my-test.qdesk.yaml
```

Exit code: `0` on PASS, `1` on FAIL, `2` on usage / error.

The command prints a summary + a `file://...report.html` link. The trace dir
also contains `trace.json` (machine-readable) and per-turn screenshots.

## Interpreting results programmatically

After `qdesk run`, parse the trace JSON:

```bash
trace=$(find qdesk-runs -name trace.json -newer /tmp/qdesk-marker | head -1)
status=$(jq -r '.status' "$trace")           # "pass" | "fail" | "error"
fails=$(jq -r '.verifies[] | select(.passed==false) | .expectation' "$trace")
diag=$(jq -r '.diagnosis // ""' "$trace")
```

If `status == "fail"`, the model has populated `diagnosis` with a short
root-cause hypothesis — surface it to the human user.

## Common pitfalls (qdesk-specific)

1. **Gemini Flash mis-clicks Flutter / canvas UIs.** Y-coordinates drift up
   by 50-150 pixels. The default prompt mitigates this, but if you see
   repeated "click did not register" turns, retry with `--llm gemini-2.5-pro`
   or wait for the Replay mode (Phase 1) to be available.
2. **Flutter Web route transitions need ~1.2s.** If a test is checking
   navigation, the runner already waits, but if you write very tight
   sequential `steps:`, expect the agent to use a `wait` action between them.
3. **`http://localhost`** doesn't reach your host from inside the sandbox.
   Use `http://host.docker.internal:PORT` (auto-resolved by the runtime).
4. **CORS / mixed-content / cookies:** the sandbox's Chromium runs with
   `--disable-gpu --no-sandbox`. If your app needs specific headers / TLS,
   add them to your dev server, not to qdesk.

## When tests fail

- Open the `report.html` — every turn has a screenshot, the agent's
  reasoning, and the action JSON. Easier than reading logs.
- The `diagnosis` field on the trace is a single-paragraph LLM-written
  hypothesis. Often correct, sometimes wrong; treat as a hint, not truth.
- If the agent mis-clicks, the screenshots will show it visually — you'll
  see the click target was off. Tighten the `goal` text or add a `steps:`
  list with smaller increments.
- If the agent gets stuck in a loop on the same screen, the page may not
  be responding. Check the server logs for the underlying app.

## Examples in this repo

- `examples/recompdaily-landing.qdesk.yaml` — landing page → sign-in flow
  for a Flutter Web app. Uses `host.docker.internal` to reach a dev server.

## Architecture (so you can extend it)

```
qdesk run X.yaml
   │
   ├─ qdesk-control HTTP API (POST /v1/sessions, etc.)
   │     └─ DockerRuntime spins qdesk/ubuntu-chrome:dev container
   │           └─ qdesk-agentd (Linux + Xvfb + Chromium + xdotool + scrot)
   │
   └─ runner.Run(): loop { screenshot → llm.Act → execute → done? }
         └─ llm.Gemini  (default; multi-model adapter via VisionAgent)
         └─ trace.json + report.html
```

Source layout:
- `pkg/protocol/` — wire types (Action, Session)
- `pkg/client/` — Go SDK for control plane
- `internal/agentd/` — in-sandbox HTTP daemon
- `internal/control/` — control plane (sessions, auth, proxy)
- `internal/llm/` — VisionAgent backends
- `internal/runner/` — agent loop + report

Adding a new model is one file under `internal/llm/` implementing the
`VisionAgent` interface.

---

**TL;DR for AI assistants:** Write a tiny YAML, run `qdesk run`, read the
HTML report or trace JSON. It's the visual unit-test you've been missing.
