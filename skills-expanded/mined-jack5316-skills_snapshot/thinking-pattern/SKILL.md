---
name: thinking-pattern
description: Decode the thinking pattern underlying your writing. Analyzes text to reveal reasoning style, argument structure, cognitive frameworks, assumptions, and blind spots. Use when you want to understand how you think by examining what you write, or /thinking-pattern.
---

# Thinking Pattern Skill (/thinking-pattern)

Decodes the cognitive structure underlying your writing. Writing is thought made visible — this skill analyzes your text to infer how you think: reasoning style, argument structure, mental models in use, assumptions, decision-making patterns, and blind spots.

## Quick Start

```bash
python3 _scripts/thinking_pattern.py path/to/your/note.md
```

## What It Does

1. **Reasoning Style** — Deductive, inductive, abductive, dialectical, or associative
2. **Argument Structure** — Claim-evidence flow, logical connectors, linear vs branching
3. **Cognitive Frameworks** — Mental models, first principles, how you handle uncertainty
4. **Assumptions** — What you take for granted, implicit beliefs, limiting priors
5. **Decision-Making Patterns** — How you weigh options, acknowledge tradeoffs
6. **Blind Spots** — Unexamined premises, what you might be unable to see

## Options

- `input`: Path to markdown/text file, or `-` for stdin (required)
- `--focus DIMENSION`: Focus on one dimension (reasoning, structure, frameworks, assumptions, decisions, blindspots)
- `--save`: Save output to Sources folder
- `--output PATH`: Custom output path

## Examples

```bash
# Analyze a vault note
python3 _scripts/thinking_pattern.py "Sources/Weekly Synthesis - 2026-02-19.md"

# Focus on reasoning style only
python3 _scripts/thinking_pattern.py "Atlas/Essay - topic.md" --focus reasoning

# Save to Sources
python3 _scripts/thinking_pattern.py "Maps/My MOC.md" --save

# Pipe text from stdin
echo "Your reflective writing here..." | python3 _scripts/thinking_pattern.py -
```

## Output

- **Terminal**: Markdown report with thinking pattern analysis
- **Saved note**: `Sources/Thinking Pattern - [source] - YYYY-MM-DD.md` (when using `--save`)

## When to Use

Use /thinking-pattern when:
- You want to understand your own reasoning style
- You're revising writing and want to see its cognitive structure
- You're preparing for a debate and want to surface your assumptions
- You want to identify blind spots in your thinking
- You've written something and want meta-cognitive feedback
- You're building self-awareness about how you process information

## Pairing with Other Skills

- **/ai-insight** — Vault-wide self-knowledge; /thinking-pattern is single-piece deep dive
- **/converge** — Use thinking-pattern to decode your writing, then converge to prioritize insights
- **/socrates** — Surface assumptions with thinking-pattern, then probe with Socratic questions
- **/gradient** — Decode pattern, then iteratively refine your writing
- **/memory** — Save your thinking pattern summary for future reference
