---
name: puda-manual-ui
description: >-
  Build and maintain PUDA manual-control Streamlit operator UIs backed by the
  PUDA CLI. Use when building operator dashboards, manual machine control
  panels, jogging UIs, or apps that start/complete/reset runs and dispatch
  individual queued machine commands from buttons.
---

# PUDA Manual UI

Build Streamlit operator UIs that drive machines through the **PUDA CLI**. The CLI remains the control plane; the UI only shells out to `puda`.

For Streamlit layout, widgets, and styling, also follow the `developing-with-streamlit` skill.

## Required session controls

Every manual-control UI **must** include these three buttons:

| Button | Role |
|--------|------|
| **Start** | Open a manual run on all relevant machines |
| **Complete** | Close the manual run on all relevant machines |
| **Reset** | Reset a machine via CLI |

### UI state machine

1. **Idle (default):** Enable **Start** and **Reset**. Disable all machine actions and **Complete**.
2. **Start** must run from the PUDA project root:
   ```bash
   puda machine start <machine_ids> --run-id manual
   ```
   Set `st.session_state.started = True` only if it succeeds. Then enable machine actions and **Complete**.
3. **Complete** must run the same machine set and run ID:
   ```bash
   puda machine complete <machine_ids> --run-id manual
   ```
   Return to idle only on success.
4. **Reset** remains visible in every state and runs:
   ```bash
   puda machine reset <machine_id>
   ```
   Return to idle after a successful reset.

Do not send machine action commands until **Start** has succeeded for the current session.

## CLI backend

Always invoke `puda` from the project root (where `puda.config` / `project.md` live). Capture stdout/stderr and show failures in the UI.

If `puda machine start` or `puda machine complete` is missing / unknown, tell the user to update the PUDA CLI to version **>= 0.0.36** (e.g. `puda version`, then `puda update`).

`<machine_ids>` may be comma-separated (same pattern as `puda machine reset biologic,first`). Start and Complete must hit the **same** set for a session. Resolve targets from project memory, user selection, or workflow skill; discover with `puda machine list` when needed.

### Dispatch individual actions

Use the maintained CLI path for *every* action button:

```bash
puda machine run <machine_id> <command_name> --params '<json-object>' --run-id manual
```

Implement with `subprocess.run(..., cwd=<PUDA project root>, capture_output=True, text=True, timeout=<per-command timeout>)`.

- `puda machine run` queues exactly one command and does not send START or COMPLETE; invoke it only after manual Start succeeds.
- Always pass `--run-id manual` so actions belong to the open manual session.
- Serialize parameters as a JSON object with `--params`; use `--kwargs '<json-object>'` only when a command requires keyword arguments.
- Record the invoked CLI command, exit code, stdout, and stderr in the operator-facing command log.
- Surface failures without changing session state.

### Prohibited legacy dispatch paths

Do not generate temporary protocol JSON/YAML files, invoke `puda protocol run`, or use a custom NATS-publishing helper for dashboard action buttons. Those paths duplicate maintained CLI dispatch, can add unintended lifecycle semantics, and leave stale protocol artifacts.

## Implementation rules

- Backend = subprocess/`puda` only. Do not open a parallel NATS client from the UI.
- Keep `run_id` hard-coded to `"manual"` for Start, Complete, and action dispatch.
- Gate every non-Start/non-Reset control on session state (`started == True`).
- Surface CLI errors; do not flip UI state to “started” or “idle” if the corresponding Start/Complete call failed.
- Prefer a small helper module (e.g. `puda_cli.py`) that wraps start / complete / reset / run / list so buttons stay thin.

## Command log and fragment behavior

Keep the command log in `st.session_state` and show the invoked CLI command, exit code, stdout, and stderr after every action. If action controls run inside `@st.fragment`, render the command log **inside that same fragment**: clicking a fragment button reruns the fragment only, so a page-level log renderer will remain stale. Expand the log automatically after a command result is recorded.

## Layout and livestream

Prefer a **single-screen layout**: livestream and all controls visible together. Do not hide core controls in tabs unless explicitly requested.

- Put **Start** / **Complete** / **Reset** at the top.
- Put compact machine controls on the left and the camera on the right when screen width allows.

When Tailnet MagicDNS is enabled, use the machine's MagicDNS name for cross-machine/player URLs rather than a changing Tailnet IP. Discover it with `tailscale status --json` (`Self.DNSName` locally, or the target peer's `DNSName`) and remove its trailing dot.

Use the short MagicDNS hostname when it resolves for the operator, otherwise the full MagicDNS name:

```text
http://<machine-hostname>:<player-port>/<path>
http://<machine-hostname>.<tailnet>.ts.net:<player-port>/<path>
```

Embed the player URL in `st.iframe(...)` and optionally link its API endpoint. Verify the selected player URL returns HTTP 200 before sharing or embedding. A Tailnet IP is a fallback only when neither MagicDNS form is available.

### Dashboard URL

For a deployed manual-control dashboard, share its reachable MagicDNS hostname and Streamlit port:

```text
http://<machine-hostname>:<streamlit-port>/
```

Verify `http://<machine-hostname>:<streamlit-port>/_stcore/health` returns HTTP 200 before reporting it. **Example only:** the First dashboard currently uses `http://first:8501/`; do not hard-code First or port 8501 for another machine.

## Reference implementation

See [`references/first-manual-app.py`](references/first-manual-app.py) for a verified First/Qubot single-screen manual-jogging dashboard. It demonstrates the lifecycle state machine, direct `puda machine run` dispatch, semantic Complete/Reset buttons, in-fragment command logging, and the livestream layout. Copy and adapt it for another dashboard rather than importing it as a runtime dependency.

## Scaffold checklist

When creating a new manual-control app:

- [ ] Streamlit entrypoint (e.g. `app.py` / `streamlit_app.py`)
- [ ] Session state: idle vs started; list of relevant `machine_id`s
- [ ] **Start**, **Complete**, **Reset** always present
- [ ] Idle: enable **Start** and **Reset**; disable machine actions and **Complete**
- [ ] Start → `puda machine start … --run-id manual`
- [ ] Complete → `puda machine complete … --run-id manual`
- [ ] Reset → `puda machine reset <machine_id>`
- [ ] Actions → `puda machine run … --run-id manual` (no temp protocols / direct NATS)
- [ ] Machine action buttons only enabled after Start
- [ ] Command log inside the same `@st.fragment` as action buttons (if fragments are used)
- [ ] Single-screen layout with livestream when a camera is available

## Verification

Before reporting a dashboard update as complete:

1. Run the dashboard virtualenv's `python -m py_compile app.py`.
2. Confirm the source contains the direct `machine run` path and no references to temp protocol creation, `puda protocol run`, or custom direct-NATS dispatch.
3. Confirm Streamlit is running.
4. Check `http://127.0.0.1:<port>/_stcore/health` returns HTTP 200.
5. Only provide a Tailnet URL after its health endpoint also succeeds.
