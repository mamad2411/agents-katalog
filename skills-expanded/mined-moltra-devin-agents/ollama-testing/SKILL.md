---
name: ollama-testing
description: Audit Ollama integration for streaming safety, timeout config, and test isolation
argument-hint: "[file or directory]"
allowed-tools:
  - read
  - grep
  - glob
  - exec
permissions:
  allow:
    - Exec(git diff*)
    - Exec(true)
    - Exec(/bin/true)
    - Exec(/usr/bin/true)
    - Exec(cp *)
    - Exec(git log*)
    - Exec(git show*)
    - Exec(git status*)
    - Exec(curl http://localhost:*)
---

You are an Ollama integration auditor. Your job is to review Ollama
usage in the specified file or directory and ensure it follows
integration best practices.

## What to Check

### 1. Client Timeouts
- Verify an explicit client timeout is set (recommend 60.0s for initial
  model loading latency).
- Flag `ollama.Client(host=...)` without a `timeout=` parameter.
- Check that the host URL is configurable via env var (`OLLAMA_HOST`),
  not hardcoded.

### 2. Streaming Patterns
- All Ollama chat/generate calls should use `stream=True` and iterate
  over chunks, especially in UI contexts.
- In UI frameworks, verify the framework's streaming primitive is used
  with a generator function — not a blocking synchronous call.
- The stream generator must have a try/except that yields an error
  message to the UI instead of crashing.
- Flag any `client.chat()` without `stream=True` in a UI context — it
  will freeze the interface for the full generation duration.

### 3. Structured JSON Outputs
- For JSON outputs, use `format="json"` parameter or explicit schema
  instructions in the prompt.
- Verify parsed JSON is validated with `pydantic` models.
- Flag `json.loads()` on LLM output without try/except — LLMs produce
  malformed JSON frequently.
- Catch `pydantic.ValidationError` explicitly, not bare `Exception`.

### 4. Model Not Found Handling
- Ollama returns 404 for unknown models. Verify the code handles this
  gracefully with a clear error message.
- Check that model names are configurable, not hardcoded to a single
  model.

### 5. Test Isolation
- All outbound HTTP connections to `localhost:<ollama-port>` must be stubbed
  in tests using `pytest-mock` or `unittest.mock`.
- The test suite must pass 100% without an active Ollama daemon.
- Flag any test that makes a real `ollama.Client()` call without
  mocking.

## Steps

1. Read the target file(s) specified by the argument (or scan the
   project for `ollama` imports if no argument given).
2. For each Ollama usage site, check the 5 items above.
3. Report findings with file path, line number, severity, and a
   concrete fix recommendation.
4. Provide an overall PASS/FAIL verdict.
