---
name: comfyui-testing-and-qa
description: Use when adding or repairing tests, CI, workflow tests, custom-node QA, regression checks, compatibility matrices, or when deciding how to prove a ComfyUI change works.
metadata:
  version: "00.01.11"
---
# ComfyUI Testing and QA

## Sources

Relevant official tools include:

- target project's own test suite;
- `Comfy-Org/ComfyUI-test-framework`;
- `Comfy-Org/comfy-qa-tools`;
- `Comfy-Org/custom-node-qa`;
- `Comfy-Org/Comfy-PR`;
- `Comfy-Org/comfyci-dashboard`;
- frontend/core repository tests.

Inspect current tool docs before invoking them.

## Test pyramid

Use the cheapest test that can actually catch the regression, then add integration coverage where interface boundaries matter.

Typical layers:

1. pure unit tests for transformations/helpers;
2. schema/registration tests for node interfaces;
3. import/load tests for extension packaging;
4. frontend unit/type/build tests;
5. workflow preflight;
6. workflow execution tests;
7. multi-version or GPU matrix only when the supported contract requires it.

## Regression rule

For a bug fix, add a test that fails for the old behavior and passes for the fix whenever practical.

## Environment truth

Record enough environment/version information to interpret failures. A GPU or dependency mismatch can otherwise look like an application regression.

## Expensive tests

Do not automatically run large model downloads, long generations, paid Cloud jobs, or broad GPU matrices without the user asking or an established project test command that clearly implies them.

## Acceptance gate

Before calling testing complete:

- include a regression test for a bug fix when practical;
- run the focused suite that covers the changed contract;
- record enough environment information to interpret hardware or dependency failures;
- do not silently skip expensive or unavailable tests;
- report skipped test layers and the reason.

