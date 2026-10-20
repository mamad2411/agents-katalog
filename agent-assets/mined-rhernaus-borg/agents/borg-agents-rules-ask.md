# AGENTS.md

This file provides guidance to agents when working with code in this repository.

- Ask streams directly to stdout when --stream is true; output is not post-processed ([src/main.rs](src/main.rs)).
- LLM selection for Ask: llm.default → llm.code_generation → first available; ensure at least one entry or force mock ([src/main.rs](src/main.rs)).
- LLM logging follows llm_logging settings; the log directory is created if missing ([src/core/config.rs](src/core/config.rs), [src/main.rs](src/main.rs)).
- Use BORG_USE_MOCK_LLM=true to decouple from external APIs during experiments ([src/main.rs](src/main.rs)).
- Ask path does not initialize StrategyManager or Git; it’s isolated from codegen/merge paths ([src/main.rs](src/main.rs)).