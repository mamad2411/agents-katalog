# AGENTS.md

This file provides guidance to agents when working with code in this repository.

- Reproduce CLI tests using generated per-test configs and temp workspaces; pass the config via -c when invoking the binary ([tests/cli_test.rs](tests/cli_test.rs)).
- Force mock LLM with BORG_USE_MOCK_LLM=true (or provider="mock" in test config) to avoid real API calls during debugging ([src/main.rs](src/main.rs), [tests/cli_test.rs](tests/cli_test.rs)).
- ComprehensiveTestRunner skips rustfmt/clippy if not installed—treat skipped as “not run,” not success ([src/testing/comprehensive.rs](src/testing/comprehensive.rs)).
- Timeouts wrap cargo test execution; intermittent stalls surface as timeout errors per configured limits ([src/testing/test_runner.rs](src/testing/test_runner.rs)).
- Complexity metrics fall back to heuristic text parsing if cargo-complexity is missing; validate with the real tool when thresholds matter ([src/core/agent.rs](src/core/agent.rs)).
- Merge operations abort on conflicts; no automatic resolution is attempted ([src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).