---
name: generate-dita-topic
description: Generates a valid DITA 1.3 XML topic template for a given topic type. Use this skill when you need a correctly structured starting point for concept, task, reference, troubleshooting, glossentry, or base topic authoring. Output includes the correct DOCTYPE declaration, required elements, and commonly used optional elements pre-scaffolded.
compatibility: Python 3.9+. No third-party dependencies.
---

## Overview

Generates a DITA 1.3 XML topic template from a topic type, title, and ID.

## Usage

```bash
# Generate a concept
python scripts/generate_dita_topic.py concept "My Concept Title" my-concept-id

# Generate a task (writes to stdout)
python scripts/generate_dita_topic.py task "Install the Software" install-software

# Supported types: topic | concept | task | reference | troubleshooting | glossentry
```

## Output

Well-formed XML printed to stdout, including:
- Correct `<?xml?>` declaration and `<!DOCTYPE>` with DITA 1.3 public identifier
- All required elements for the topic type
- Commonly used optional elements pre-scaffolded (e.g., `<prereq>`, `<result>` for tasks)
- Placeholder text `{{FILL}}` marking elements that need content

## Examples

See [assets/](assets/) for pre-rendered template examples for each type.

## Common edge cases

- `id` must be a valid XML `ID` (starts with letter or `_`, no spaces); the script normalises spaces to hyphens
- `glossentry` does not use a conventional body element — output is `<glossterm>` + `<glossdef>`
- Task template includes `<prereq>`, `<context>`, `<result>`, `<postreq>` as optional scaffolding — remove unused ones before validation
