---
name: skill-creator
description: Guide users through creating new cawpilot skills with a structured process and template. Use when the user asks to create a new skill, make a skill, add a skill, build a custom skill, or extend cawpilot's capabilities with new domain knowledge or workflows.
---

# Skill Creator

Guide for creating cawpilot skills — modular packages that extend the agent with specialized knowledge, workflows, and tool integrations.

## Skill Structure

```
skill-name/
├── SKILL.md              (required — metadata + instructions)
├── scripts/               (optional — executable code for deterministic tasks)
├── references/            (optional — detailed docs loaded on demand)
└── assets/                (optional — templates, images, files used in output)
```

### SKILL.md Format

```markdown
---
name: skill-name
description: What the skill does and when to use it. Be specific about triggers.
---

# Skill Title

Instructions for executing the skill's workflows.
```

**Frontmatter** (YAML):
- `name` (required): kebab-case identifier
- `description` (required): What it does + when to trigger. This is the *only* thing the agent sees before activating the skill, so be comprehensive about triggers.

**Body** (Markdown): Procedural instructions, rules, and examples. Target < 500 lines.

### References (optional)

For large or multi-domain skills, split details into `references/` files and link from SKILL.md:

```markdown
For deployment details, see [references/aws.md](references/aws.md).
```

The agent loads these only when needed, keeping the context lean.

### Scripts (optional)

Include scripts in `scripts/` for tasks that need deterministic reliability or are repeatedly rewritten. Scripts can be executed without loading into context.

### Assets (optional)

Include files in `assets/` that are used in output (templates, images, boilerplate) rather than loaded into context.

## Creation Process

### 1. Understand the Goal

Ask the user:
- What should the skill do? (concrete examples of usage)
- What triggers it? (what would a user say?)
- What external tools or APIs does it use?
- Are there any credentials or secrets involved?

Don't overwhelm — start with the essentials, follow up as needed.

### 2. Plan the Skill

Identify:
- **Core workflows**: step-by-step procedures
- **Rules and constraints**: what to always/never do
- **Reference material**: schemas, API docs, domain knowledge (split into `references/` if large)

### 3. Create the Skill

Create the skill directory under `skills/` in the workspace:

```
skills/<skill-name>/SKILL.md
```

Write the SKILL.md following the format above. Key guidelines:
- Use imperative form ("Run the command", not "You should run the command")
- Include concrete examples of inputs and expected outputs
- Keep instructions concise — the agent is already smart, only add what it can't know
- Prefer examples over explanations

### 4. Test and Iterate

After creating the skill, tell the user to restart cawpilot so it picks up the new skill. Then test with real prompts and refine based on results.

## Privacy-First Rules

**Every skill must follow these rules. Enforce them during creation:**

1. **No secrets in skill files** — never embed API keys, tokens, passwords, or credentials in SKILL.md or any skill file. Reference environment variables or config instead.
2. **No user data in skill files** — skills are templates, not data stores. Never include PII, usernames, account IDs, or user-specific data.
3. **Credential handling** — if a skill needs credentials, instruct the agent to read them from environment variables or the cawpilot config at runtime. Example:
   ```markdown
   Read the API key from the `MYSERVICE_API_KEY` environment variable. Never log or display the key.
   ```
4. **Output sanitization** — instruct skills to never print secrets, tokens, or sensitive data in messages sent back to the user.
5. **Minimal permissions** — skills should request only the access they need. Don't expose broad filesystem paths or network access unnecessarily.
6. **Data locality** — keep user data within the workspace. Never instruct the agent to upload data to external services without explicit user consent.

When reviewing a skill draft, check each rule and flag violations before finalizing.

## Writing Tips

- **Description is critical** — it's the sole trigger mechanism. Include synonyms and example phrases.
- **One skill, one domain** — don't create catch-all skills. Split by domain.
- **No boilerplate files** — don't create README.md, CHANGELOG.md, or other non-essential files.
- **Progressive disclosure** — keep SKILL.md lean. Use `references/` for detailed docs, schemas, or API specs that the agent loads only when needed.

## Example

A minimal skill for interacting with a weather API:

```markdown
---
name: weather
description: Fetch weather forecasts and current conditions using the OpenWeatherMap API. Use when the user asks about weather, forecasts, temperature, or conditions for a location.
---

# Weather

Fetch weather data from the OpenWeatherMap API.

## Setup

Read the API key from the `OPENWEATHER_API_KEY` environment variable. Never log or display the key.

## Usage

When the user asks for weather information:

1. Extract the location from the request
2. Call the API:
   ```bash
   curl -s "https://api.openweathermap.org/data/2.5/weather?q=${LOCATION}&appid=${OPENWEATHER_API_KEY}&units=metric"
   ```
3. Parse the JSON response and report: temperature, conditions, humidity, wind speed
4. If the location is ambiguous, ask the user to clarify

## Rules

- Always use metric units unless the user specifies otherwise
- Never expose the API key in messages
- If the API returns an error, report it clearly without retrying
```
