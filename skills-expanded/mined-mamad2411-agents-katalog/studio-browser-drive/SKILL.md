---
name: studio-browser-drive
description: >-
  Drive Studio Chrome (logged-in profile) from the `studio` Hermes agent via
  cua-driver browser tools + ONE Gemini-3.6-flash screenshot sweep per screen
  (box_2d normalized 0-1000). Use for ALL browser work on the Studio —
  payments, forms, checkouts. Never use Kernel browsers here (fallback only).
version: 1.0.0
metadata:
  hermes:
    tags: [studio, cua-driver, browser, payments, vision, box2d]
    category: devops
    related_skills: [payment-operations]
---

# Studio browser drive (CDP screenshot → one 3.6-flash sweep → CSS-pixel actions)

This is the ONLY sanctioned loop for driving Studio Chrome. It replaces the
old AX-snapshot-ping-pong that wasted minutes per form. Kernel browsers are a
fallback for when this whole path is broken — never the default.

## Non-negotiables (Cooper, 2026-08-03)

1. **Model:** the driving agent runs `google/gemini-3.6-flash` (openrouter).
   Vision sweeps use the SAME model via `scripts/vmap.py` / `scripts/vcoord.py`.
2. **Out-of-1000 scaling:** NEVER ask vision for raw pixels. Always Gemini
   `box_2d` convention, normalized 0–1000, `[ymin,xmin,ymax,xmax]` (y FIRST).
3. **Initial screenshot sweep:** on every new screen, ONE `get_browser_state`
   call with `include_screenshot=true` gives you BOTH the semantic refs AND the
   CDP screenshot; then ONE `vmap.py` pass maps ALL interactive elements at
   once. Never look up one element per vision call.
4. **Kernel browsers = fallback only.** If this loop works, Kernel is never used.

## Architecture

```
studio Hermes agent (Pro) ──ssh MCP──> cua-driver on Mac Studio ──CDP──> Studio Chrome (logged-in profile)
```

- MCP server `cua-driver` is already configured on the `studio` profile
  (ssh BatchMode to `coopermaruyama@<REDACTED>`).
- Session id: use ONE stable id for the whole task (e.g. `payments-<date>`).
- Sessions EXPIRE when idle and after daemon restarts. `session has ended`
  refusal → re-run `start_session` with the same id. Bindings invalidate after
  every daemon restart and every navigation → re-bind (below).

## Lifecycle (exact order)

1. `start_session {session, capture_scope:"window"}`
2. Find Chrome: `list_windows` → Google Chrome pid + native window_id
   (title may be empty; pick by size). If a prior binding/target is known and
   the daemon never restarted, skip to step 4.
3. `browser_prepare {session, pid, window_id, strategy:{kind:"existing_profile"}}`
   → then `get_browser_state {session, pid, window_id}` (bind mode) →
   `target_id` + `tabs[]` with `tab_id`s.
4. **THE SWEEP** — one call:
   ```
   get_browser_state {session, target_id, tab_id,
                      snapshot_format:"semantic_v2", include_screenshot:true}
   ```
   Returns: `structuredContent.screenshot_png_b64`, `screenshot_width/height`
   (device px), `screenshot.pixel_to_css_scale_x/y` (≈0.5),
   `viewport_css_width/height`, plus typed action `refs` (textbox refs carry
   their current `value` — verification for free) and an `outline`.
5. Decode the PNG to `/tmp/shot.png`, then ONE vision sweep:
   ```bash
   set -a; source ~/.hermes/.env; set +a        # OPENROUTER_API_KEY
   python3 <skill>/scripts/vmap.py /tmp/shot.png --plan
   ```
   Every control comes back as `ref  type  label  x,y  value/state` in image
   pixels. This single call is "send an initial screenshot to get all text
   fields at once".

## Coordinate math (validated on the Google payment form)

box_2d is normalized against the SCREENSHOT image. Actions want CSS viewport px:

```python
px_x = ((xmin + xmax) / 2) / 1000 * screenshot_width
px_y = ((ymin + ymax) / 2) / 1000 * screenshot_height
css_x = px_x * pixel_to_css_scale_x      # measured 0.5
css_y = px_y * pixel_to_css_scale_y      # measured 0.5
```

Then `browser_click {target_id, tab_id, x: css_x, y: css_y}`.

## Driving rules

- **Text/email/number fields:** click once by CSS coords, then
  `browser_type {ref, text, replace:true}` using the semantic ref for that
  field from the SAME sweep (refs expose the field value — re-read it to
  verify). If the field has no usable ref (shadow/iframe weirdness), click by
  coords and type via `browser_type` on the nearest editable ref; verify by
  re-sweep.
- **Buttons (Save, Continue, Pay…):** `browser_click` by CSS coords from vmap.
  Trusted route may refuse standalone-background posture → retry the SAME
  click with `input_route:"dom_event"` plus a semantic `ref` for the button.
- **Selects/dropdowns:** one at a time — click → wait → re-sweep the open
  list → click the option row. Never batch select commits.
- **After EVERY navigation:** re-bind (step 3) and re-sweep (step 4). Refs and
  coords are garbage across navigations.
- **Incomplete snapshot:** `snapshot.continuation` token → call again with
  `continuation:` to page remaining refs (Save buttons live past the budget).
- **Verify state with the next sweep's `value` column**, not with assumptions.
  `effect: "unverifiable"` is delivery-only — require read-back.

## Recovery table

| Symptom | Fix |
|---|---|
| `session … has ended` | re-run `start_session` same id, then re-bind |
| `not a live binding in this session` | re-bind: `get_browser_state` with pid+window_id |
| `browser_requires_setup` | re-run `browser_prepare` for exact pid/window |
| `browser_consent_required` | restart Studio daemon: `pkill -f "cua-driver serve"`, then `nohup env CUA_DRIVER_RS_PERMISSIONS_GATE=0 cua-driver serve --grant existing-profile --no-permissions-gate >/tmp/cua-driver-serve.log 2>&1 &`, re-prepare |
| Click "confirmed" but page unchanged | click missed or wrong layer — re-sweep, use vmap coords, or `dom_event` route with ref |
| Field value wrong after type | `browser_type` with `replace:true`; never append to stale content |

## Screenshot source: CDP, NOT screencapture

Studio TCC Screen Recording for `com.trycua.driver` is currently false, so
`get_window_state` screenshots and bare `screencapture` FAIL
(`px_capture_unavailable`). **Always** use `include_screenshot:true` on
`get_browser_state` (CDP Page.captureScreenshot — bypasses TCC, exact tab
viewport, no foregrounding). If `permissions status` ever shows
`screen_recording: true` window capture recovers, but CDP stays preferred.

## Payment forms

Governed by the `payment-operations` skill: card entry + saving the payment
method are the TASK (no gate); the ONLY stop is the charge-triggering click
(Pay / Submit payment / Confirm charge). Card data comes from the `op` wrapper
(drkmttr.1password.com, vault `cm`) via a 0600 temp file — never printed.
Amex on Google: 15-digit PAN, expiry MM/YY split fields, 4-digit CVC,
cardholder name, ZIP. Google shows the saved card in a list after Save.

## Anti-patterns

- Asking vision for raw `[x,y]` pixels (bimodal ~178px Y errors).
- One vision call per field (the exact latency failure this replaces).
- Kernel browsers while this path works.
- Reusing refs/coords after navigation or a newer snapshot.
- Driving by `get_window_state` AX dumps alone when a screenshot sweep gets
  every control in one call.
- Reporting success from `effect:` fields without a read-back sweep.

## Scripts

- `scripts/vmap.py` — one-sweep full-screen mapper (box_2d → pixels, `--plan`
  groups by drive type). Model via `VCOORD_MODEL` (default
  `google/gemini-3.6-flash`). Needs `OPENROUTER_API_KEY` from `~/.hermes/.env`.
- `scripts/vcoord.py` — locate a named list of controls on a screenshot.
