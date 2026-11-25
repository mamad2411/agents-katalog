---
name: prompt
description: Generate well-structured and orchestrated prompts. Create prompts with clear role, context, task, output format, and constraints. Apply templates to content, design multi-step workflows, or generate custom prompts from descriptions. Use when you need prompt engineering, structured prompts, or /prompt.
---

# Prompt Skill

Generates well-structured prompts and orchestrates multi-step prompt workflows from a curated template library.

## Usage

```bash
python3 _scripts/prompt_skill.py list                                         # browse templates
python3 _scripts/prompt_skill.py generate "Summarize technical docs for non-experts" --save
python3 _scripts/prompt_skill.py apply summarize --from-path "Sources/Article.md"
python3 _scripts/prompt_skill.py orchestrate "Research topic → report with recommendations"
python3 _scripts/prompt_skill.py template steelman                            # raw template text
```

## Template Library

`summarize`, `analyze`, `explain`, `critique`, `expand`, `compare`, `extract-actions`, `socratic`, `steelman`, `synthesis`

## Output

- Generated prompts: `Templates/Prompt - [description] - YYYY-MM-DD.md`
- Applied results: `Sources/[Template Name] - YYYY-MM-DD.md`
- Workflows: `Templates/Prompt Workflow - [goal] - YYYY-MM-DD.md`
