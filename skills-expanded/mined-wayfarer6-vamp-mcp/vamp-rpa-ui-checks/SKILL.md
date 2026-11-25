---
name: vamp-rpa-ui-checks
description: Define reusable UI locators and outcome checks for VAMP Robot/Python RPAs. Use for screen automation reliability, host versus guest coordinates and compact validation evidence.
---

# VAMP RPA UI checks

Read rpa-reuse and the relevant virtualbox-rpa, hyperv-rpa or spice-vm-rpa skill before driving a guest. Reuse a reviewed package that matches the VM, input contract and expected application state.

## Define the contract

Read [display preflight](references/display.md). Verify 1920×1080 and 100% guest scaling before coordinate-based work; if different, adjust the guest and verify fresh evidence before continuing, subject to the user's current authorization and pause state.

Record the VM UUID, host platform, hypervisor, application, expected starting state, guest resolution and display scaling. State whether coordinates belong to the host window, viewport or guest framebuffer. Recalibrate when resolution, scaling, crop or window placement changes; never silently mix coordinate spaces.

Prefer semantic locators for host webviews and native accessibility controls. For guest screenshots, use the existing backend's OCR/YOLO pipeline and localized anchors. Limit searches to the relevant region and require an unambiguous match before clicking. Keep language recognition multilingual even when product explanations are English.

## Execute and verify

Use bounded waits for observable state changes. After each consequential action, check an independent outcome such as a dialog closing, expected page appearing, file existing or completion marker being written. A click, typed command or successful tool return proves delivery only.

When installation must run automatically, observe its result without manually starting the installer. Separate diagnostics from setup. On ambiguous state, capture targeted evidence and stop dependent input; use the repair skill for a failed saved RPA. Respect user pauses immediately and do not create snapshots unless requested.

## Mark editable steps in GUI recordings

Surround each reusable local block with paired standalone Python comments. Choose a stable ID that describes the action. Keep the entry and completion text in the step plan.

```python
# vamp-step: open-menu
p.press('f2')
# vamp-end: open-menu
```

Use `{"name":"open-menu","section":"open-menu","entry":"Operations desk","exit":"Inventory menu"}` in the plan. Moving the block or adding comments above it preserves its identity. Mark whole actions and include both the press and release of a held key. Use each section ID once and keep the blocks unnested. Pinned steps retain their original RPA ID, commit and step.

For an existing saved recording, call `rpa_revision` with `action="annotate"`, its ID and expected commit. Supply a step plan with inclusive source lines and screen checks if one is missing. Show the returned source and plan to the user. On an authorized update, submit that exact pair and expected commit through `rpa_revision` with `action="update"` and `confirmed=true`. Review the new revision in RPA Library before replay. Keep any existing `# vamp-target` annotations on the click lines.

## Save reusable evidence

Store locator intent, timing bounds, coordinate mapping, expected outcome and failure condition with the RPA. Return compact status and artifact paths. Export only targeted failure crops or OCR excerpts when needed. Exclude passwords, tokens and private session data from recordings and shared skills. Report completed_unverified distinctly from verified success.

## Human approval during sign-in

Name the Vault entry, destination and field before requesting approval. Focus the
matching blank field and use `vault_deliver_credential`, which returns only a
receipt. Close the recorder and pause screen capture during entry. An authorized
routine login submission is a separate action after checking the expected page.
Pause before a passkey, MFA, security-key, CAPTCHA or unexpected consent prompt.
Ask the user to complete it and verify the next screen before resuming.
