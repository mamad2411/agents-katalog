# AGENTS.md

This file provides guidance to agents when working with code in this repository.

- Bootstrapping guarantees a Git repo with an initial commit in agent.working_dir; designs relying on empty repos must account for this invariant ([src/core/agent.rs](src/core/agent.rs)).
- Current authentication is permissive: Agent grants Developer role automatically; strategy permission checks always return allowed ([src/core/agent.rs](src/core/agent.rs), [src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).
- Strategy registration defaults to CodeImprovement; extend via StrategyManager registration points ([src/core/strategy.rs](src/core/strategy.rs), [src/core/agent.rs](src/core/agent.rs)).
- Planning subsystem is optional and time-bounded; milestone generation respects short timeouts and may proceed without planning results ([src/core/planning.rs](src/core/planning.rs)).
- Evaluation gates (coverage/complexity/error-handling) are soft by default due to runner stubs and heuristics; do not assume production-grade enforcement ([src/testing/test_runner.rs](src/testing/test_runner.rs), [src/core/agent.rs](src/core/agent.rs)).
- The borg git subcommand bypasses Agent/StrategyManager, invoking LLM codegen directly; architecture depending on StrategyManager won’t apply there ([src/main.rs](src/main.rs)).