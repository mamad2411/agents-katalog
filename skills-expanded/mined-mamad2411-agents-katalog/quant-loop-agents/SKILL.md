# Quant Research Loop — Agent Instructions

## Overview

Autonomous AI agent loop for CTA timing strategy research. Each iteration is a fresh AI instance that advances the research by one step. Memory persists via git history, `progress.txt`, and `research.json`.

Supports multiple AI tools: Kiro CLI, Claude Code, Amp, GitHub Copilot CLI, OpenCode.

## Commands

```bash
# Run research loop (default tool: kiro)
./quant-loop.sh --duration 4h

# Run with specific tool against a separate project
./quant-loop.sh --tool claude --duration 4h --project ~/research/btc-ma

# Run with deadline
./quant-loop.sh --tool amp --deadline "2026-03-29T10:00:00"

# Generate report manually
python3 generate_report.py
python3 generate_report.py --final
```

## Key Files

| File | Purpose |
|------|---------|
| `quant-loop.sh` | Time-driven bash loop spawning fresh AI instances |
| `prompt.md` | Agent prompt template (used by all tools) |
| `compact.md` | Memory compaction prompt (spawned every N iterations) |
| `research.json` | Research state: hypothesis, targets, phase, best metrics |
| `research.json.example` | Example research config |
| `progress.txt` | Agent memory: Patterns, Anti-Patterns, Metrics History, iteration logs |
| `progress.txt.template` | Template for new progress files |
| `validate.py` | Validation framework — checks improvement + overfitting |
| `validate_example.py` | Example validation implementation |
| `generate_report.py` | HTML report generator |
| `skills/hypothesis/` | Skill: generate strategy hypothesis |
| `skills/research/` | Skill: convert hypothesis → research.json |

## Architecture

- **Framework ↔ Project separation**: Loop framework lives here; research projects live separately. Use `--project` to point at any project directory.
- **Memory compaction**: Every N iterations (configurable via `--compact-every`), the shell spawns a dedicated agent with `compact.md` to compress `progress.txt` and clean up dead-end scripts. This is enforced by the shell, not by the research agent.
- **Hints**: Users drop `.md` files into the project's `hints/` folder mid-run. The next iteration digests them and renames to `consumed-*.md`.

## Patterns

- Each iteration: read state → decide action → execute → validate → commit/record → update state
- Agent self-directs: chooses phase advancement, branching, or direction changes
- Anti-Patterns in progress.txt prevent repeating failed explorations
- Rust used only when Python is too slow (parameter search, event-driven backtest)
- Strategy logic must follow Occam's razor — simplicity over complexity
