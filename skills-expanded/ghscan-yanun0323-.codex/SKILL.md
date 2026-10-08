---
description: Create or update prompt, rule, and skill assets with normalized naming, metadata, and packaging.
---

Use this prompt when asked to create, migrate, or normalize a prompt, rule, or skill.

Required resources:
- `skills/skill-create-prompt-or-skill/references/normalization-rules.md`
- `skills/skill-create-prompt-or-skill/references/openai_yaml.md` when touching `agents/openai.yaml`
- `skills/skill-create-prompt-or-skill/scripts/init_skill.py`
- `skills/skill-create-prompt-or-skill/scripts/generate_openai_yaml.py`
- `skills/skill-create-prompt-or-skill/scripts/normalize_skill_catalog.rb`
- `skills/skill-create-prompt-or-skill/scripts/quick_validate.py`

Classify the target before editing:
- `Prompt`: a single Markdown file under `prompts/`
- `Rule`: a folder whose name and frontmatter use the `rule-` prefix
- `Skill`: a folder whose name and frontmatter use the `skill-` prefix

Normalization rules:
- Prompts must not use the `command-` prefix.
- Prompt frontmatter must contain `description` only.
- Prompt bodies should be short, task-oriented, and written in Codex prompt style.
- Rules must use `rule-` names, `assets/rule-small.svg`, and `interface.display_name: "Rule - Xxx Xxx"`.
- Skills must use `skill-` names, `assets/skill-small.svg`, and `interface.display_name: "Skill - Xxx Xxx"`.
- Normalize any legacy `agents-*` folder to `rule-*`.
- Convert any legacy `command-*` request into `prompts/<name>.md` with the prefix removed.

Workflow:
1. Identify whether the request targets a prompt, rule, or skill.
2. Decide whether the item needs `scripts/`, `references/`, or `assets/`; keep instructions concise and move bulky detail into references.
3. Initialize or migrate the item with the provided scripts when they save work.
4. Edit the content to match the target type.
5. Validate the result.
6. Iterate if validation or real usage exposes gaps.

Useful commands:
```bash
python3 skills/skill-create-prompt-or-skill/scripts/init_skill.py <name> --kind <prompt|rule|skill> --path <output-root>
python3 skills/skill-create-prompt-or-skill/scripts/generate_openai_yaml.py <path/to/skill-folder> --interface display_name="..." --interface short_description="..."
python3 skills/skill-create-prompt-or-skill/scripts/quick_validate.py <path/to/skill-or-prompt>
ruby skills/skill-create-prompt-or-skill/scripts/normalize_skill_catalog.rb --check
```

Editing rules:
- For prompts, keep the body concise and task-oriented. Do not add `assets/` or `agents/openai.yaml`.
- For rules and skills, keep `SKILL.md` frontmatter limited to `name` and `description`.
- Do not remove unrelated fields from `agents/openai.yaml`.
- Keep repository artifacts in English.
- Do not create extra documentation files unless the workflow requires them.

Success criteria:
- Naming matches the target type.
- Frontmatter is valid and normalized.
- Required icon and OpenAI YAML metadata are present for rules and skills.
- Prompt output validates when the target is a prompt.
