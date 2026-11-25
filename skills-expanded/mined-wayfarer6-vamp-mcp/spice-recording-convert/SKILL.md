---
name: spice-recording-convert
description: Convert manually recorded PyAutoGUI Python into a reviewed Robot/SPICE RPA package, or scaffold a manually authored RPA. Use for recorder imports, guest/host coordinate calibration, and Windows Win+R launch conventions.
---

Work from `/home/ssh1032007/spice_kvm_based_rpa` or the repository checkout. Read `docs/RECORDING_CONVERSION.md` and `agent/rpas/README.md`. Use `skill-creator` when a new independent execution skill is also requested; ordinary recording imports use this existing conversion skill.

## Inputs and safe conversion

Identify source path, guest OS, resolution, whether coordinates were recorded inside the guest or on a host viewer, display scale/zoom and intended result. A `.py` extension is not required. The owner's current input is `/home/ssh1032007/naver_login_rpa`; its generated draft is `agent/rpas/windows_naver_recorded/`.

Do not import, run, eval or exec recorder source. Use the AST/literal-only converter:

```bash
.venv/bin/python scripts/convert_recording.py /home/ssh1032007/naver_login_rpa --id windows_naver_recorded --guest-os windows11 --coordinate-space guest --width 1920 --height 1080
```

Existing packages are never overwritten; choose a new ID for another import. Reject unsupported calls/control flow and report their line numbers instead of dropping them. The converter writes `manifest.json`, `run.robot`, `workflow.py`, `conversion.json`, README and a private `recording.local.json`. Typed key sequences can contain credentials even when no `write('password')` exists: do not echo reconstructed text into chat or commit the private data. The source remains unchanged. Public sharing requires removal/replacement of private input first.

For new manual packages use `.venv/bin/python scripts/new_rpa.py <id> --guest-os windows11` (or `debian`). The scaffold is `not_configured` and does not connect to a VM. Follow its README to add reviewed steps and meaningful assertions.

## Universal program launch

**Windows program startup uses Win+R and an executable/command, not desktop-icon coordinates.** Use a guest shortcut or OS search only when the requested app cannot be launched from Run, and document why. Windows desktops differ by user. `cmd`/`win` recorder keys map to SPICE Super/Windows; `shift_r` maps to right Shift. Debian GNOME uses Alt+F2 plus a command, with documented alternatives for other desktops. Do not reuse Windows launch keys in Debian.

Keep the recorder's Win+R prefix if present. If a recording launches through a desktop icon, identify the application and replace only the launch prefix with a common launcher. Do not guess an executable or replay a desktop click while investigating. The current input's Win+R prefix was mechanically identified; its 80 actions were live-replayed once on the Windows KVM guest. The initial merged-label validation failed and was corrected; read-only re-observation confirmed the login form. See the package evidence rather than assuming account login occurred.

## Coordinate and semantic refinement

Guest-space recordings keep native pixel coordinates; require matching resolution. Equal 1920×1080 resolution does not imply equal OS UI, display scaling or browser zoom. For host-space input, require an explicit guest image viewport in the same recorded coordinate units and use `--coordinate-space host --viewport LEFT TOP WIDTH HEIGHT`; reject points outside it. Do not guess titlebar offsets, DPI transforms or proportional scaling after layout changes.

Review `conversion.json` first. Use the private action file only as needed. Coordinates stay in Python-consumed action/locator data; Robot controls sequence and branches. Preserve key-down/up order and explicit waits, note unmatched keys, and retain teardown key release. Replace fragile clicks with a unique OCR/YOLO anchor and replace long fixed waits with bounded expected-state checks where evidence supports the change. Use `spice-rpa-repair` for subsequent UI drift.

Private credential spans must be removed from recorded key events and replaced with a dedicated credential routine or a `write_env` event, with no actual secret in Robot variables. Do not replay recorded CAPTCHA answers. Use the existing CAPTCHA handoff, and check current state before a submission. Login, payment and other externally mutating actions require the relevant user task, not merely a conversion request.

## Verify without claiming live success

Run package validation, tests relevant to converter/runtime, and the target Robot `--dryrun`. A normal generated run returns `needs_review` and SKIP without a SPICE connection. Do not enable `ALLOW_REPLAY` just to test a conversion when only import/scaffolding was requested.

When the user requests replay, confirm the actual Windows/Debian SPICE URI and the authorized scope. Run one package/entrypoint, after review, with `--var ALLOW_REPLAY:True`. Missing local data must be regenerated. A geometry mismatch blocks input; it is not permission to guess new coordinates. Raw replay returns `replayed_unverified`; only an explicit meaningful positive check can justify `succeeded`. The optional `EXPECTED_TEXT` OCR check is a starter check, not full application/authentication verification.

Report generated paths, supported/unsupported actions, coordinate space/resolution, review warnings, private-data handling, dry-run outcome and whether live replay occurred. No model is called by the converter itself; AI refines the generated package when this skill is invoked.

## Default verification when authoring GUI RPAs

When implementing or refining a new GUI RPA, add task-specific local OCR and/or YOLO verification code to `workflow.py` and call it from the Robot task before asserting success. Choose the expected text/state from the actual task and observed UI; do not invent an expected result. Use OCR for visible text/state and YOLO for relevant UI regions, with text or a concrete state change to establish meaning. Input dispatch or an arbitrary detected box is not success. Add file/content/hash checks when the task produces an artifact.

Use bounded local waits and persistent workers; limit images to relevant regions and results to compact status/evidence paths. Ordinary successful replay must not depend on an LLM reading screenshots. Check positive and failed/absent expected states before calling the workflow verified. If no meaningful expected state is configured, keep `not_configured` or `completed_unverified` rather than claiming success. The blank scaffold and AST-only converter cannot infer a task outcome; add this verification during AI/manual implementation and preserve the normal review gate. See [the authoring checklist](../../../docs/LOW_TOKEN_AUTOMATION.md#새-gui-rpa를-작성할-때).
