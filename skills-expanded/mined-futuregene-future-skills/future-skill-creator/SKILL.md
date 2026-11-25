---
version: 1.1.2
name: future-skill-creator
description: >
  Create, review or improve a custom Future skill with clear triggers, concise
  instructions, optional scripts/references/assets and offline validation. Use for
  requests to add a skill, update SKILL.md, port a workflow or create a custom skill.
  Default installation scope is ~/.future/agent/skills (Windows USERPROFILE equivalent).
allowed-tools: Bash(future:*)
category: tools
---

# Custom Skill Creator

A skill is a folder with a `SKILL.md` entry and only the resources needed at runtime.
Prefer a small, testable workflow over an inventory of general advice.

## Scope and location

The default **app scope** is `<home>/.future/agent/skills/<name>/SKILL.md` on macOS,
Linux and Windows (use the actual home/USERPROFILE path). **Shared agent scope** is
`<home>/.agents/skills`; use it only when requested. App scope takes discovery
precedence for duplicate names. Do not silently install into both scopes.

When asked to edit repository-maintained builtin skills, edit their source in the
repository/worktree, not the user's installed copy. Reuse the requested destination
and existing authorizations. Do not overwrite an unrelated or locally modified skill
without confirming the intended replacement.

## Workflow

1. Identify concrete triggers, inputs, output, tools, failure modes and how success
   will be checked. Infer routine details; ask only about unresolved material choices.
2. Choose a lowercase letters/digits/hyphens name, under 64 characters, matching its
   folder. Write a description that says what the skill does and when it should trigger.
3. Write `SKILL.md` using the file write/edit tool, not shell redirection. Frontmatter
   needs `name`, `version` and `description`; use folded/quoted YAML for text containing
   colon-space. Keep examples syntactically valid.
4. Add `references/` only for optional detail, `scripts/` for fragile/repeated deterministic
   work, and `assets/` for actual reusable templates. Explain when to load each resource;
   resolve its path relative to the skill directory. Do not invent helper/dependency paths.
5. Validate structure and metadata using the included validator. Then test representative
   positive and negative workflow cases at the appropriate risk level. Metadata alone does not
   prove the skill is reachable: a skill the agent can load but the clients never list looks
   identical to "no skill" — silently, with no error anywhere. Confirm the client's skill list
   shows it before calling the work done.
6. Improve from actual usage failures. Tighten trigger descriptions for over-triggering;
   add discriminating examples for under-triggering; remove duplicated generic instructions.

## Minimal entry

```yaml
---
name: example-skill
version: 1.0.0
description: >
  Do a specific task with specified inputs and outputs.
  Use when the user asks for these concrete task families.
---
```

Follow with purpose, the shortest useful workflow, checks, failure handling and
conditional resource pointers. Match the user's language and deliverable. Do not
force repeated approval questions when the current request already settles them.

## Future CLI tools

Load the relevant builtin skill and consult `future tools describe <tool>` rather
than copying a stale interface. Examples of current entry points:

```bash
future tools call web_search --query "topic" --count 5
future tools call fetch_url --url "https://example.com"
future tools call image_gen --prompt "A diagram" --output ./image.png --timeout 600
future tools call parse_doc --input ./report.pdf
```

Authentication is handled by the CLI. Never embed real credentials. Explain when
files or queries leave the machine, respect offline/confidential constraints, and
distinguish local timeouts from remote cancellation before retrying paid actions.
Tool allow-lists in frontmatter are not substitutes for the harness's permission checks.

## Validation

The included `scripts/validate_skill.py` uses PyYAML (see `requirements.txt`). Reuse
an installed interpreter/dependency or an authorized task-local environment. Resolve
the script's absolute path from this skill directory before running it:

```bash
python /absolute/skill/path/scripts/validate_skill.py /absolute/custom-skill-directory
```

It validates folder/name/version/description, semantic versions (including prerelease
plus build metadata), unique YAML keys and boolean invocation flags. Also inspect resource existence, CLI examples and the output checks; metadata
validation alone does not prove correct model behavior. For paid/live behavior tests,
use the user's authorized scope and budget and report exactly what was exercised.

## Updating an existing skill

Read the current entry and relevant resources first. Preserve useful task-specific
knowledge, provenance and safety boundaries. Make the smallest change that addresses
the observed failure; move low-frequency detail out of a growing entry. Bump its version,
rerun validation and the affected tests, then report the actual save paths and test limits.
No extra changelog/README or platform-wide rule is needed for a one-off skill update.
