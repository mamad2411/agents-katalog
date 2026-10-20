---
description: Rules for LLM prompt management
globs: src/**
alwaysApply: false
---
# Prompt Management Rules

## PromptBuilder Required for Content Generation

**All content generation prompts MUST use `PromptBuilder`** (`core/prompt_builder.py`).
Do NOT create new `load_prompt()` helper functions. Use `PromptBuilder.build()` with
decomposed persona + function YAML files.

Deterministic tool prompts (autograde, rubric generation, sentiment scoring, guideline
generation, worksheet gen/fill) may use direct YAML loading since they don't need
persona/brand injection.

## No Inline Prompts

All LLM prompt text — system prompts, user prompts, image-generation prompts,
and ICL templates — MUST live in YAML files under `prompts/`.

Python code loads prompts via `PromptBuilder.build()` (preferred) or
`yaml.safe_load` + Jinja2 (tool prompts only); it must never contain
hardcoded prompt strings.

## Standard YAML Schema

Chat prompts use two keys:

```yaml
system: |
  The AI's persona, rules, and constraints.
  Uses {{ jinja2_variables }} for dynamic data.

user: |
  The per-request template with {{ variables }}.
```

ICL (in-context learning) templates use the `block:` key:

```yaml
block: |
  {% for ex in examples %}...{% endfor %}
```

Image-generation fallback prompts may use custom keys (e.g. `simplify_template:`,
`fallback:`).

## Resolution Order

`PromptBuilder` and adapter `load_prompt()` helpers resolve files in this order:

1. `projects/{slug}/prompts/{platform}/{file}` — project + platform override
2. `projects/{slug}/prompts/{file}` — project-level default
3. `prompts/{platform}/{file}` — global default

## Onboarding Templates

Persona templates used during `mmn project add` live in `prompts/templates/`.
These are YAML files with placeholder tokens (`{{ persona_description }}`, etc.)
that get filled in by `core/project_templates.py` and written to the new project.

## Exempt from This Rule

- LangChain tool docstrings (`integrations/langchain.py`) — required by framework
- Error messages, CLI help text, log messages
- The `labeling_instruction` conditional fragment in `worksheet.py` which is a
  short inline string passed as a template variable, not a standalone prompt

## Prompt Types

| Type | Use PromptBuilder? | persona param | brand param |
|------|--------------------|---------------|-------------|
| Content generation (comments, replies, threads, posts, scripts, carousels) | Yes | Required | Required |
| Outreach (prospect scoring, message generation) | Yes | None | None |
| Platform metadata (YouTube metadata, email paraphrase) | Yes | Optional | Optional |
| Deterministic tools (autograde, rubric gen, sentiment, guidelines, worksheets) | No | N/A | N/A |

## Adding a New Content Generation Prompt

1. Create `prompts/{platform}/functions/{function_name}.yaml` with `system:` + `user:` keys (Jinja2).
2. If persona-driven: ensure `prompts/{platform}/persona.yaml` exists.
3. In code: `PromptBuilder().build(platform=..., function=..., persona=..., brand=..., template_vars=...)`.
4. Add an entry to the inventory table in `prompts/prompt.md`.

## Anti-Patterns

- Creating new `load_prompt()` functions for content generation -- use `PromptBuilder`
- Using Python `.format()` in YAML templates -- use Jinja2 `{{ }}`
- Hardcoding brand names in prompt files -- use `{{ brand.name }}`, `{{ brand.url }}`
- Embedding persona instructions in function YAML -- keep persona in `persona.yaml`
