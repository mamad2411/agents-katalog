---
title: Integration Testing — Project Implementation
topic: integration-testing
last-verified: 2026-03-11
---

## Stack

pytest 7.0+ with pytest-asyncio 0.21+, same as unit testing. No additional integration testing frameworks or dependencies are used.

## Configuration

Integration tests share the same pytest configuration as unit tests via `pytest.ini`. No separate test configuration, markers, or environment setup exists for integration tests. They run as part of the standard `pytest` invocation.

## Patterns

Integration tests are co-located with unit tests in `tests/test_main.py` within a dedicated `TestIntegration` class. The `test_full_workflow_integration()` method tests the complete application flow — argument parsing, configuration loading, cache lookup, TTS generation, and audio playback — with external dependencies (OpenAI API, VLC, filesystem) mocked at the boundary. This provides end-to-end verification of internal component interaction without requiring network access or audio hardware.

## File Locations

- `tests/test_main.py` — `TestIntegration` class (lines 228-260)
- `pytest.ini` — shared test configuration
