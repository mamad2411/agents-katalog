---
name: out-yaml
description: Instructs the agent to produce output strictly in valid YAML format, ensuring no conversational filler or markdown wrappers.
license: MIT
---
# Skill: out-yaml

<!-- markdownlint-disable MD013 MD023 MD031 MD032 -->

Instructs the agent to produce output strictly in valid YAML format, ensuring no conversational filler, markdown wrappers (like ```yaml), or additional explanations are present.

## WHEN TO USE

- When an automated downstream process strictly expects a raw YAML response to parse.
- To enforce pure structural output without the LLM adding "Here is your config:" headers.
- When generating infrastructure-as-code manifests (like Kubernetes or Ansible) inline.

## WHEN NOT TO USE

- If the user explicitly asks for an explanation or tutorial alongside the YAML code.
- When outputting to a Markdown file where standard ```yaml codeblocks are expected and required.
- For generating structured data where JSON is strictly preferred by the parsing tool.

## Common Pitfalls

- **Markdown Wrapping**: The LLM outputting `` ```yaml ... ``` `` despite instructions, breaking a strict parser
  expecting raw file content.
- **Lost Comments**: Instructing the agent to output strict YAML and accidentally having it strip out important explanatory comments from the original structure.
- **Invalid Types**: Outputting unquoted boolean strings like `yes` or `no` when a specific parser strictly expects `true` or `false`.

## Core Process

1. **Activate**: Triggered when the goal requires YAML output.
2. **Format**: Format the output entirely as valid YAML.
3. **Verify**: Ensure no text exists outside the YAML structure.
4. **Emit**: Output the YAML string directly.

## Core Principles

- **Strict Schema Adherence**: Output must be 100% valid YAML, parsable by standard YAML parsers.
- **Zero Conversational Output**: Absolutely no preambles, postambles, or explanatory text.
- **No Markdown Formatting**: Do not wrap the output in Markdown code blocks. Only emit raw YAML.

## Commands / Usage Patterns

Produce raw YAML as shown below:

```yaml
key: value
list:
  - item1
  - item2
```

## Diagnostics and Troubleshooting

- If parsers fail, check for invisible characters, invalid indentation, or unescaped strings.

## What to Avoid

- Including "Here is the YAML you requested:" or similar conversational text.
- Enclosing the output in Markdown backticks (e.g., `` ```yaml ... ``` ``).
- Including non-YAML comment styles (e.g., `//`, `/* */`, `<!-- -->`) or omit comments entirely unless explicitly allowed.

## Limitations

- The agent cannot validate the output against a specific schema unless one is provided.
- Only enforces syntax, not semantic correctness.
