---
name: implementation-reality-verification
description: Eliminates false-greens: verifies code is reachable, exercised, evidenced, and verified beyond shallow unit tests.
---
# Implementation Reality Verification

## 1. Do Not Confuse File Presence with Feature Implementation
Finding a file does not mean the feature works. Verify interfaces, call sites, runtime wiring, lifecycle, error paths, and CLI exposure.

## 2. Eliminate False-Green Oracles
Detect tests that pass because assertions are weak, mocks are used instead of real capabilities, or errors are silently swallowed.

## 3. Terminal State Hierarchy
Derive completion strictly through:
implemented -> reachable -> exercised -> evidenced -> verified -> accepted -> released.
Agents are strictly prohibited from declaring DONE by text output.
