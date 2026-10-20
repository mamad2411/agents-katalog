## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:
- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current

## Engineering Principles

### 1. Think Before Coding
- State assumptions explicitly.
- Ask when confused.
- Push back on unclear requirements.

### 2. Simplicity First
- Use the minimum code needed for the problem.
- If 200 lines can be 50, rewrite it.
- Do not add speculative features.

### 3. Surgical Changes
- Touch only what is necessary.
- Match existing style.
- Leave unrelated code unchanged.

### 4. Goal-Driven Execution
- Define verifiable success criteria.
- Use test loops, not vague tasks.
- For "fix bug" work: write a test, then make it pass.
