# AGENTS.md

This file provides guidance to agents when working with code in this repository.

- Always include an explicit file path near code blocks (e.g., “// File: path/to.rs”) to prevent defaulting writes to src/main.rs ([src/code_generation/llm_generator.rs](src/code_generation/llm_generator.rs), [src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).
- Commit messages are generated from LLM output; keep proposed messages succinct and context-rich without extra prose ([src/code_generation/llm_generator.rs](src/code_generation/llm_generator.rs)).
- Do not rely on the plan engine to apply/test changes; its default execution is a no-op for those steps—ensure real edits/tests are triggered in your flow ([src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).
- Respect repo quality gates (clippy -D warnings -W clippy::cognitive_complexity, audit deny warnings) when proposing code ([.roo/rules/linting.md](.roo/rules/linting.md)).
- Prefer llm.code_generation from config; main and Agent fall back to llm.default when absent ([src/main.rs](src/main.rs), [src/core/agent.rs](src/core/agent.rs)).
- Merges are not auto-resolved; structure changes to minimize conflicts and avoid wide, risky edits in a single step ([src/core/strategies/code_improvement.rs](src/core/strategies/code_improvement.rs)).
- Keep Ask vs Codegen providers separate; Ask may select default/any available entry, while Code/Git paths prefer code_generation ([src/main.rs](src/main.rs)).