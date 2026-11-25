---
name: android-camera-porting-debug
description: End-to-end Android camera porting and debugging workflow for new sensor bring-up and runtime issue diagnosis. Use when working on Android camera integration or failures across kernel driver, sensor probe, I2C/power sequence, static metadata, provider/HAL/app open, CamCal/OTP/EEPROM, AWB/LSC/3A, tuning, NVRAM, build/merge, and log-based root cause analysis. Especially use for tasks such as porting a new sensor, diagnosing camera open failure, wrong resolution, metadata crash, color cast, CamCal read failure, ERR_NO_3A_GAIN, ERR_NO_SHADING, or similar camera integration issues.
---

# Android Camera Porting And Debugging

Use this skill to handle Android camera work as a controlled workflow, not as ad hoc trial-and-error.

## Core Rule

Always default to:

`Diagnose -> Decision Gate -> Execute -> Verify -> Document`

Do not jump directly to edits unless the problem layer is already clear.

## Working Style

- Start by locating the failure layer before changing code.
- Prefer minimal, reversible changes.
- Touch only files relevant to the current root-cause path.
- For high-risk paths such as driver, boot-time probe, partitioned calibration flow, or cross-layer dispatch, add logs before larger logic changes.
- Do not claim a fix without runtime evidence.
- After two failed execute-verify rounds, narrow to one root-cause direction and one minimal patch.

## First Step

Classify the task into one of these paths:

1. New sensor bring-up
2. Camera runtime failure
3. Image quality issue
4. CamCal / OTP / EEPROM / calibration issue
5. Metadata / provider / HAL exposure issue
6. Tuning / NVRAM issue
7. Build / merge / packaging / flash verification issue

Then read only the relevant reference files.

## Reference Map

- For overall process and phase control, read `references/workflow.md`.
- For probe, sensor ID, I2C, power sequence, driver registration, and kernel-side bring-up, read `references/bringup-kernel-driver.md`.
- For static metadata, provider enumeration, HAL open path, stream config, resolution mismatch, and app open failures, read `references/metadata-provider-hal.md`.
- For CamCal, OTP, EEPROM, layout/header parsing, calibration dispatch, and related log signatures, read `references/camcal-otp-eeprom.md`.
- For red tint, color cast, AWB, LSC, 3A gain, shading, and image-quality symptoms, read `references/awb-lsc-3a-tuning.md`.
- For tuning blobs, NVRAM, sensor tuning library behavior, and default/fallback tuning paths, read `references/nvram-and-tuning.md`.
- For build flow, split build, merge, package verification, flash readiness, and log collection rules, read `references/build-verify-document.md`.
- For project-specific overrides such as platform quirks, product layout, local build entrypoints, and repo-specific conventions, read `references/project-adaptation.md`.
- For reusable session-start prompts and handoff templates, read `references/invocation-templates.md`.

## Standard Output Structure

When diagnosing, always produce:

1. Conclusion
2. Evidence
3. Candidate explanations with risks
4. Recommended next step

When executing, always state:

1. What file(s) will change
2. Why this is the minimum valid change
3. What evidence will confirm success or failure

When verifying, always report:

1. What was actually run
2. What logs or runtime evidence were checked
3. What remains unproven

## Decision Gates

Before editing, decide which layer currently owns the problem:

- If sensor is not detected, stay in driver/probe/I2C/power.
- If sensor is detected but app cannot open, inspect metadata/provider/HAL path.
- If app opens but image is wrong, inspect 3A/AWB/LSC/tuning/calibration.
- If calibration-related errors appear, inspect CamCal/OTP/EEPROM dispatch before tuning.
- If build artifacts are suspect, verify build/merge/package inputs before runtime inference.

Do not mix multiple root-cause layers in one patch unless evidence requires it.

## Execution Constraints

- Do not modify metadata, driver, tuning, and calibration simultaneously without a hard reason.
- Do not blind-edit calibration tables without confirming actual storage type and layout when that information is still unknown.
- Do not treat color issues as tuning-only problems until calibration and gain paths are ruled in or out.
- If runtime logs show code path A never executes, stop modifying inside A and move to its caller or dispatch layer.

## Verification Rules

A fix is not verified by compilation alone.

Use the strongest available evidence:

- build success
- merge/package success
- sensor probe success
- provider enumeration
- runtime log signature change
- error disappearance
- expected gain/shading/calibration values appearing
- image symptom improvement

If only compile evidence exists, say so explicitly.

## Documentation Rules

Record progress in the active project tracking files if they exist:

- `task_plan.md`
- `findings.md`
- `progress.md`

Document:

- current root-cause hypothesis
- evidence gained this round
- what changed
- what was verified
- exact next step

## Typical Triggers

This skill should be used for requests like:

- “Help me port a new Android camera sensor”
- “The sensor probes but the camera app fails”
- “The camera opens but color is wrong”
- “The front camera is red or green tinted”
- “CamCal / OTP / EEPROM is not working”
- “I see ERR_NO_3A_GAIN or ERR_NO_SHADING”
- “Metadata is missing and camera crashes”
- “Resolution is wrong after sensor integration”
- “Please continue the camera bring-up/debug session”
