# Claude Command: Iterative Deep Research

Execute the Iterative Deep Research Agent for multi-pass research with gap analysis.

## Usage

```
/iterative-research "Your research topic here"
```

Or with arguments:
```
/iterative-research --check   # Check dependencies only
/iterative-research --help    # Show help
```

## Difference from /deep-research

| Feature | /deep-research | /iterative-research |
|---------|----------------|---------------------|
| Passes | 1 (single-pass) | 1-5 (configurable) |
| Queries | 5-10 (soft limit) | 15-45 (per iteration) |
| Sources | Variable | Minimum guaranteed |
| Gap Analysis | None | After each iteration |
| Refinement | None | Query refinement based on gaps |

## What This Command Does

1. **Phase 1 - Decomposition**: Breaks topic into 5-15 searchable sub-vectors
2. **Phase 2 - Search Iteration**: Executes queries for each sub-vector
3. **Phase 3 - Gap Analysis**: LLM identifies what's missing
4. **Phase 4 - Refinement**: Generates new queries for gaps
5. **Loop**: Repeats until stopping criteria met
6. **Phase 5 - Synthesis**: Compiles final report

### Stopping Criteria
- `max_iterations` reached (default: 5)
- `min_sources` found (default: 20)
- Saturation detected (no new information)

## Execution

When the user invokes this command, execute:

```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "/home/cmr-auto/claude-work/repos/lex-vector")
cd "$REPO_ROOT/adk-agents" && ./run-iterative-research.sh "$ARGUMENTS"
```

If `$ARGUMENTS` is empty, ask the user for a research topic.

If `$ARGUMENTS` is `--check`, run:
```bash
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null || echo "/home/cmr-auto/claude-work/repos/lex-vector")
cd "$REPO_ROOT/adk-agents" && ./run-iterative-research.sh --check-deps
```

## Prerequisites

- `GOOGLE_API_KEY` environment variable (loaded from `adk-agents/.env`)
- Python virtual environment at `adk-agents/deep_research_sandbox/.venv/`
- Required packages: `google-adk`, `google-genai`

## Output Format

Research results are saved as Markdown with:
- **Iteration Summary**: Queries and sources per iteration
- **Key Findings**: Bulleted facts with citations
- **Technical Details**: Data tables
- **Limitations & Gaps**: What wasn't found
- **Source Index**: Full list of all sources

## Examples

Basic iterative research:
```
/iterative-research "Compare LLM inference frameworks: vLLM vs TensorRT-LLM vs TGI"
```

Complex topic (benefits from multiple iterations):
```
/iterative-research "Comprehensive analysis of vector database architectures and their tradeoffs"
```

Check setup:
```
/iterative-research --check
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "No API key found" | Check `adk-agents/.env` has `GOOGLE_API_KEY` |
| "Agent initialization failed" | Run `/iterative-research --check` |
| Too few sources | Topic may be too niche; try broader terms |
| Takes too long | Reduce iterations with `--iterations 3` |

## Notes

- Research typically takes 1-3 minutes depending on iterations
- Uses `gemini-2.5-flash` model by default
- Output directory: `adk-agents/deep_research_sandbox/research_output/`
- Files prefixed with `iterative_research_` for easy identification
- Logs saved alongside output for debugging
