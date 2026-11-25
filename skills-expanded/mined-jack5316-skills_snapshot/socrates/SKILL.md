---
name: socrates
description: Socratic questioning method to explore and deepen understanding of a question or topic. Use the SOCRATES framework to uncover assumptions, clarify concepts, and reveal implications through thoughtful inquiry.
---

# Socrates Skill (/socrates)

Apply the Socratic questioning method to systematically explore topics and deepen understanding through guided inquiry.

## Quick Start

```bash
python3 _scripts/socrates.py "What is the nature of consciousness?"
```

## What It Does

The Socrates skill uses the **SOCRATES framework** to generate thought-provoking questions that help you:

1. **Clarify concepts** - Better understand what you mean by terms and ideas
2. **Uncover assumptions** - Identify what you're taking for granted
3. **Explore origins** - Trace where ideas come from
4. **Examine consequences** - Consider what follows from your beliefs
5. **Challenge perspectives** - Look at things from opposite viewpoints
6. **Evaluate evidence** - Question how you know something is true
7. **Find examples** - Test ideas with concrete cases
8. **Synthesize connections** - See how ideas relate to each other

## The SOCRATES Framework

- **S** - Clarification Questions (What do you mean by...?)
- **O** - Origin Questions (Where did this idea come from?)
- **C** - Consequence Questions (What follows from this?)
- **R** - Role Reversal Questions (What if the opposite were true?)
- **A** - Assumption Questions (What are we taking for granted?)
- **T** - Truth/Evidence Questions (How do we know this is true?)
- **E** - Example/Counterexample Questions (Can you think of an example?)
- **S** - Synthesis Questions (How does this relate to...?)

## Options

- `question`: The question or topic to explore (required)
- `--from-path PATH`: Path to a note containing context (e.g., Atlas/Essay - topic.md)
- `--title TEXT`: Custom output filename
- `--save`: Save output to vault (default: prints to terminal only)

## Examples

```bash
# Basic usage - prints to terminal
python3 _scripts/socrates.py "What is the meaning of life?"

# With vault note context
python3 _scripts/socrates.py "AI safety" --from-path "Atlas/Essay - AI Ethics.md"

# Save to vault
python3 _scripts/socrates.py "The future of work" --save

# With custom title
python3 _scripts/socrates.py "Consciousness" --title "Exploring Consciousness" --save
```

## Output

- **Terminal**: Markdown-formatted Socratic questions organized by SOCRATES framework
- **Saved note**: `Atlas/Socratic Inquiry - [Topic].md` with YAML frontmatter

## Why This Matters

- **Deepens understanding** - Questions reveal layers of meaning you might miss
- **Uncovers biases** - Helps identify implicit assumptions and blind spots
- **Encourages reflection** - Promotes thoughtful, deliberate thinking
- **Sparks creativity** - New questions lead to new insights and perspectives
- **Builds wisdom** - The journey of questioning is as valuable as any answer
