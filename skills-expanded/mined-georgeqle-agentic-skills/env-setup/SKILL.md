---
name: env-setup
description: Scaffold the local env file with required variable stubs from .env.example and code, open it for the user to fill, and verify completeness by key names only — never reading secret values
type: execution
version: v0.0
argument-hint: "[target env file or framework hint]"
---

# Env Setup

Invoke as `$env-setup`.

Scaffold the project's local environment file with stubs for every required variable, open it so the user can fill in values, and verify completeness by key names only. This skill must never read, print, or summarize secret values from any env file.

## Process

1. **Resolve the target file** from `$ARGUMENTS`:
   - Default to `.env.local`.
   - Accept an explicit file path (e.g. `.env`, `.dev.vars`) or a framework hint (e.g. `next`, `wrangler`) and map it to that framework's convention.
   - If the repository's own convention differs from the default (e.g. plain Node projects loading `.env`, Wrangler projects using `.dev.vars`), use the detected convention and say so in the report.

2. **Discover required variables.** Build the union of:
   - Keys in `.env.example`, `.env.sample`, or equivalent template files.
   - Code references: `process.env.X`, `import.meta.env.X`, `os.environ[...]`, and framework config files.
   - Setup sections in `README.md` and project docs.
   - If the target file already exists, extract key names only (e.g. `cut -d= -f1`) to learn which keys are already present. Never read, cat, print, or summarize values from the target file or any other secret-bearing env file.

3. **Scaffold stubs:**
   - Create the target file if it does not exist.
   - Append only the missing keys as `KEY=` stubs, each with a one-line comment hint for where the value comes from (provider dashboard, teammate, generated locally).
   - Never overwrite, reorder, or rewrite existing lines in the target file.

4. **Gitignore guard:**
   - Verify the target file is covered by `.gitignore`. If it is not, add a matching ignore entry and warn the user.
   - Never remove an env file from `.gitignore`, and never commit the target env file.

5. **Open the file for the user:**
   - Open the target file in VS Code with `code <file>`.
   - Inside WSL, if `code` is unavailable, follow the AGENTS.md/CLAUDE.md Windows/WSL file-opening convention (`wslpath` + `cmd.exe /c start`).

6. **Verify by presence only.** When the user says they are done (or on a re-run):
   - Report which keys are still empty, by key name only. Never echo values.
   - For non-secret generatable keys (e.g. `AUTH_SECRET`, session salts), offer to generate a value locally with a command such as `openssl rand -base64 32` — only with user confirmation, and write it into the file without printing it back.

7. **Write forward to `.env.example`:** if discovery found required keys that are missing from `.env.example`, append them there as empty stubs so the template stays complete. This is a tracked change and ships normally.

## Output

```markdown
Env setup
- Target file: <path> [created | updated | already complete]
- Keys scaffolded: [key names | none]
- Keys still empty: [key names | none]
- Gitignore: [already covered | entry added | WARNING not covered]
- Editor: [opened in VS Code | open manually: <path>]
- .env.example: [updated with N keys | unchanged]
- **Next work:** [fill in the empty keys listed above | none]
- **Recommended next command:** [re-run $env-setup to verify completeness | none]
```

## Constraints

- Never read, print, echo, or summarize secret **values** from any env file — operate on key names only.
- Never commit the target env file, and never weaken `.gitignore` coverage of env files.
- Never overwrite or rewrite existing lines in the target env file; only append missing stubs.
- If the user pastes a secret value into the conversation, warn them that it is now in chat history and suggest rotating it if sensitive.
- Do not invent required variables that no template, code reference, or doc mentions.

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md. Only `.env.example` and `.gitignore` edits are tracked-file mutations to ship; the target env file itself is never committed.
