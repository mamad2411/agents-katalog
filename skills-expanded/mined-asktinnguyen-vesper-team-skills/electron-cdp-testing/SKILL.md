---
name: electron-cdp-testing
description: Debug Electron renderer behavior through CDP. Use when testing the real Electron window, `window.electronAPI`, screenshots, or `remote-debugging-port` flows.
---

# Electron CDP Testing

<objective>
Use Chrome DevTools Protocol against the real Electron renderer so automation can verify UI state, inspect `window.electronAPI`, and capture evidence without drifting into a regular browser tab.
</objective>

<essential_principles>

1. **Connect to Electron, not Vite in a browser.** A `localhost` tab does not expose `window.electronAPI`; the Electron renderer does.
2. **In Vesper, prefer repo-native helpers first.** Reach for `scripts/e2e/cdp-utils.cjs`, `scripts/e2e/run-all.cjs`, and existing E2E tests before hand-rolling WebSocket code.
3. **Treat CDP availability as a hard gate.** If `curl -s http://127.0.0.1:9222/json` fails or no `page` target is present, stop and fix launch first.
4. **Use Vesper dev-instance env when relaunching manually.** Source `scripts/detect-instance.sh` before launching Electron with `--remote-debugging-port=9222`.
5. **Prove the cheap checks first.** Verify target selection, `typeof window.electronAPI`, one route change, and one screenshot before attempting long IPC-heavy flows.

</essential_principles>

## Scope

- Vesper UI feature or regression work: prefer `vesper-electron-testing`. Use this skill when you specifically need raw CDP, direct renderer evaluation, or preload-bridge probing.
- Generic Electron CDP diagnostics: use this skill.
- Local web app in a normal browser: use `webapp-testing`.
- Public-web browser automation: use `agent-browser`.

## Success Criteria

- `curl -s http://127.0.0.1:9222/json` returns JSON.
- A non-DevTools `page` target for `Vesper` or `Vesper Dev (...)` is found, or the actual app title is documented.
- `typeof window.electronAPI` returns `object`, or its absence is explicitly documented as intentional.
- At least one screenshot or structured DOM summary is captured as evidence.
- The final report names concrete pass/fail checks, not just “looks good.”

## Process

1. If you are in the Vesper repo, read [references/vesper-cdp-reference.md](references/vesper-cdp-reference.md) and follow [workflows/vesper-direct-cdp.md](workflows/vesper-direct-cdp.md).
2. If you are in another Electron app, adapt the same flow: launch Electron with `--remote-debugging-port`, verify `/json`, connect to the real `page` target, then probe the renderer.
3. Prefer maintained helpers over custom sockets:
   - Vesper repo helpers: `scripts/e2e/cdp-utils.cjs`, `scripts/e2e/run-all.cjs`, `apps/electron/src/__tests__/e2e/`
   - Skill-local quick probes: `scripts/cdp-connect.js`, `scripts/cdp-test.js`, `scripts/validate-setup.sh`
4. Only use a session-scoped Electron MCP surface if the current session already exposes matching tool IDs. This skill does not assume any `mcp__electron__*` contract exists in Vesper.
5. When a test is flaky, reduce scope in this order:
   - CDP endpoint
   - correct target
   - `window.electronAPI`
   - one route or one DOM probe
   - one screenshot
   - only then long async IPC flows

## Report Format

```md
ELECTRON CDP CHECK
- CDP endpoint: PASS/FAIL (`curl /json`)
- Target selection: PASS/FAIL (`page` target title)
- Preload bridge: PASS/FAIL (`typeof window.electronAPI`)
- UI evidence: PASS/FAIL (screenshot or DOM summary path)
- Interaction probe: PASS/FAIL (specific action and observed result)
- Issues / blockers:
```

## Next Step

- Vesper launch notes and failure modes: [references/vesper-cdp-reference.md](references/vesper-cdp-reference.md)
- Vesper smoke workflow: [workflows/vesper-direct-cdp.md](workflows/vesper-direct-cdp.md)
