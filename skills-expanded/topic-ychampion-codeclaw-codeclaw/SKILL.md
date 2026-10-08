---
name: codeclaw
description: >
  Export Claude Code conversation history to Hugging Face as structured training data.
  Use when the user asks about exporting conversations, uploading to Hugging Face,
  configuring CodeClaw, reviewing PII/secrets in exports, or managing their dataset.
allowed-tools: Bash(codeclaw *), Bash(huggingface-cli login *), Bash(pip install codeclaw*), Bash(grep *)
---

<!-- codeclaw-begin -->

# CodeClaw Skill

## THE RULE

**Every `codeclaw` command outputs `next_steps`. FOLLOW THEM.**

Do not memorize the flow. Do not skip steps. Do not improvise.
Run the command → read the output → follow `next_steps`. That's it.

The CLI tracks your stage (1-4: auth → configure → review → done).
`codeclaw export` (push) is **gated** — you must run `codeclaw confirm` first or it will refuse.

## Getting Started

Run `codeclaw status` (or `codeclaw prep` for full details) and follow the `next_steps`.

## Output Format

- `codeclaw prep`, `codeclaw config`, `codeclaw status`, and `codeclaw confirm` output pure JSON
- `codeclaw export` outputs human-readable text followed by `---CODECLAW_JSON---` and a JSON block
- Always parse the JSON and act on `next_steps`

Key fields:
- `stage` / `stage_number` / `total_stages` — where you are
- `next_steps` — follow these in order
- `next_command` — the single most important command to run next (null if user input needed first)

## PII Audit (Stage 3)

After `codeclaw export --no-push`, follow the `next_steps` in the JSON output. The flow is:

1. **Ask the user their full name** — then grep the export for it
2. **Run the pii_commands** from the JSON output and review results with the user
3. **Ask the user what else to look for** — company names, client names, private URLs, other people's names, custom domains
4. **Deep manual scan** — sample ~20 sessions (beginning, middle, end) and look for anything sensitive the regex missed
5. **Fix and re-export** if anything found: `codeclaw config --redact "string"` then `codeclaw export --no-push`
6. **Run `codeclaw confirm`** — this runs its own PII scan, shows the project breakdown and session counts, and unlocks pushing. Walk through results with the user.
7. **Push only after explicit user confirmation**: `codeclaw export`

## Commands Reference

```bash
codeclaw status                            # Show current stage and next steps (JSON)
codeclaw prep                              # Discover projects, check HF auth (JSON)
codeclaw confirm                           # Scan PII, summarize export, unlock pushing (JSON)
codeclaw confirm --file /path/to/file.jsonl # Confirm a specific export file
codeclaw list                              # List all projects with exclusion status
codeclaw config                            # Show current config
codeclaw config --repo user/my-personal-claude-code-data  # Set HF repo
codeclaw config --exclude "a,b"            # Add excluded projects (appends)
codeclaw config --redact "str1,str2"       # Add strings to redact (appends)
codeclaw config --redact-usernames "u1,u2" # Add usernames to anonymize (appends)
codeclaw config --confirm-projects         # Mark project selection as confirmed
codeclaw export                            # Export and push (requires codeclaw confirm first)
codeclaw export --no-push                  # Export locally only
codeclaw export --all-projects             # Include everything (ignore exclusions)
codeclaw export --no-thinking              # Exclude extended thinking blocks
codeclaw export -o /path/to/file.jsonl     # Custom output path
codeclaw update-skill claude               # Install/update the codeclaw skill for Claude Code
```

## Gotchas

- **Never run bare `huggingface-cli login`** — it's interactive and will hang. Always use `--token`.
- **`--exclude`, `--redact`, `--redact-usernames` APPEND** — they never overwrite. Safe to call repeatedly.
- **`codeclaw prep` outputs pure JSON** — parse it directly.
- **Always export with `--no-push` first** — review before publishing.
- **`codeclaw export` (push) requires `codeclaw confirm` first** — it will refuse otherwise. Re-exporting with `--no-push` resets this.
- **PII audit is critical** — automated redaction is not foolproof.
- **Large exports take time** — 500+ sessions may take 1-3 minutes. Use a generous timeout.

## Prerequisite

`command -v codeclaw >/dev/null 2>&1 && echo "codeclaw: installed" || echo "NOT INSTALLED — run: pip install codeclaw"`

<!-- codeclaw-end -->

