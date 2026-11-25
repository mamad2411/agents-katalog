---
description: Enforce standards for Cursor rule files (.mdc) regarding format, naming, content, and AI interaction.
globs: .cursor/rules/*.mdc
tags: [cursor, rules, standards, meta]
priority: 1
version: 1.2.1
alwaysApply: true
---

# Cursor Rules Standards

## Context

This rule defines mandatory standards for all Cursor rule files (`.mdc`) to ensure consistency and correct AI behavior. Apply when creating or modifying any `.mdc` file.

## Requirements

- **Location & Naming:**
    - Directory: `.cursor/rules/`
    - Filename: `kebab-case-name.mdc` (no prefixes).
- **Frontmatter (YAML block enclosed by `---`):**
    - **No Comments:** The frontmatter block itself must not contain YAML comments (`#`).
    - **Required Fields:**
        - `description` (String): Concise (under 150 chars), ideally `ACTION when TRIGGER to OUTCOME`.
        - `globs` (String): Comma-separated glob patterns.
            - **No Quotes:** Do NOT quote individual patterns or the entire string.
                - Correct: `**/*.ts, **/*.tsx`
                - Correct: `src/app/**/*.js`
                - Incorrect: `"**/*.ts, **/*.tsx"`
                - Incorrect: `'**/*.ts', '**/*.tsx'`
            - **No Array Format:** Do NOT use YAML/JSON array syntax.
                - Incorrect: `['**/*.svelte']`
            - **Clarity:** Target only intended files (e.g., `.cursor/rules/*.mdc` for these rules).
        - `tags` (Array of Strings): Relevant keywords (e.g., `[javascript, formatting]`).
        - `priority` (Integer): Precedence (e.g., 1-5; lower may be more general).
        - `version` (String): Semantic version (e.g., `1.0.0`).
        - `alwaysApply` (Boolean): `true` for fundamental AI guidelines; `false` otherwise.
- **Body Content:**
    - Required Sections: `# Rule Title`, `## Context`, `## Requirements`, `## Examples`.
    - Concise, actionable, and testable requirements.
    - **Example Formatting:**
        - Use `<example>` tags for valid examples and `<example type="invalid">` for invalid ones.
        - `<example>` and `</example>` tags should not be indented relative to their parent heading (e.g., `## Examples`).
        - Code blocks (using ` ``` `) within `<example>` tags should be indented (e.g., by 2 spaces).
- **Formatting:**
    - Concise Markdown.
    - Blank line before and after ` ``` ` code blocks within examples.
    - In `<example>` tag `description` attributes, prefer plain text or single quotes for emphasis or paths; avoid backticks unless absolutely necessary and properly escaped if they conflict with the description string itself.
- **Versioning:**
    - Update `version` (semantic: MAJOR.MINOR.PATCH) upon modification.
- **AI Interaction for Rule Modification (Critical):**
    - When creating/modifying `.cursor/rules/*.mdc` files, the AI **must** use `edit_file`.
    - Use markdown extension instead of `*.mdc`
    - **DO NOT** save the file into `.cursor/rules/*.mdc`
    - **YOU MUST** add the files into `cursortemp/rules/*.md`
    - The AI **must** generate the _full, complete content_ of the rule file and present it to the user for manual update/creation.

## AI Optimization Tips

- Use precise `ACTION when TRIGGER to OUTCOME` in `description`.
- Include only essential `tags`.
- Set clear `priority` levels.
- Provide minimal, clear, positive and negative `examples` that adhere to the specified formatting.
- Focus on machine-actionable instructions.
- Remove non-essential prose to optimize for AI context window.
- Suggest relevant workflow rules (e.g., `feature-workflow`) if applicable.

## Examples

<example description="Correct frontmatter: no comments, correct glob format">

```mdc
---
description: Guide Svelte 5 component development with DaisyUI.
globs: src/routes/(layout)/**/*.svelte, src/components/**/*.svelte
tags: [svelte, daisyui, components]
priority: 2
version: 1.0.0
alwaysApply: false
---

# Svelte DaisyUI Component Guide

...
```

</example>

<example type="invalid" description="Incorrect glob: quotes around entire string">

```mdc
---
description: Rule for TypeScript files.
globs: "**/*.ts, **/*.tsx" # Incorrect
tags: [typescript, standards]
priority: 2
version: 1.0.0
alwaysApply: false
---

# TypeScript Standards

...
```

</example>

<example type="invalid" description="Incorrect glob: YAML array format">

```mdc
---
description: Svelte file standards.
globs: ['**/*.svelte', '**/+page.svelte'] # Incorrect
tags: [svelte, formatting]
priority: 2
version: 1.0.0
alwaysApply: false
---

# Svelte File Rule

...
```

</example>

<example type="invalid" description="Incorrect frontmatter: comment inside">

```mdc
---
description: API key security.
globs: **/*.env, **/.env.*
# version: 1.0.0 # This comment is invalid here
tags: [security, secrets]
priority: 1
version: 1.0.0
alwaysApply: true
---

# API Key Security

...
```

</example>

<example description="Correct example formatting: <example> tag not indented, code block indented">

````mdc
## Examples

<example description="This is a well-formatted example.">

  ```python
  # Code inside the example is indented
  print("Hello, World!")
  ```

</example>
````

</example>
