---
name: converge
description: Convergent thinking skill - synthesis, prioritization, decision making, and actionable next steps. Use when you need to narrow down options, make decisions, prioritize, find patterns, or identify concrete next steps.
---

# Converge Skill

Synthesizes multiple ideas into coherent wholes, prioritizes options, and narrows possibilities to actionable next steps.

## Usage

```bash
python3 _scripts/converge.py "future projects" --ideas "idea1" "idea2" "idea3"
python3 _scripts/converge.py "which tool?" --decide --ideas "A" "B" --framework pros-cons
```

## Options

- `topic` — Topic or question to converge on (required)
- `--ideas LIST` — Ideas/options to process
- `--synthesize` — Find patterns across ideas
- `--prioritize` — Rank options (default framework: impact-effort)
- `--decide` — Make a decision with justification
- `--nextsteps` — Generate actionable next steps
- `--tradeoffs` — Analyze tradeoffs
- `--distill FILE` — Distill a file to its essence (`--ratio 0.1-0.9`)
- `--framework NAME` — impact-effort, pros-cons, SWOT, urgent-important, etc.
- `--full` — Full convergence session
- `--save` — Save output to vault

## Output

`Sources/Converge - [topic] - YYYY-MM-DD.md`
