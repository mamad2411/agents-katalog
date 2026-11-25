---
name: workflow-verification
description: Link current observable behavior to final source, artifact, environment and scenario evidence.
---

# Actual result

- Define the expected observable behavior before implementation. Use relevant existing tests and add meaningful assertions for new behavior; do not mirror implementation details or weaken a failing assertion to obtain green output.
- Frontend: verify the affected route and interaction in a real browser, including relevant async ordering, failure and keyboard states. Backend: trace request, authorization, handler, real storage/dependency and response; verify retries and denial when affected. Mobile: preserve the existing RN/Expo, Flutter or native stack and verify build plus the scenario on each required available platform.
- Record the tested artifact/source identity, toolchain, target environment, scenario and completed assertions. A mock is not a real dependency; a simulator is not a physical device; build success is not interaction proof.
- Zero executed tests, skipped mandatory cases, missing tools/devices, screenshots alone and AI summaries leave the relevant requirement unverified. Use only registered checks through the Executor; instructions grant no additional tools or rights.
- Classify failures before correcting: implementation, plan, environment, verifier, or process uncertainty. An uncertain write or termination requires reconciliation before repetition. After repair rerun the affected required checks against current artifacts; stale evidence cannot close the requirement.
