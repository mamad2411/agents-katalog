# routine-templates — Claude Code skill

Scaffolds a new Claude Code Routine from one of the five production templates in this repo.

## When to trigger

- `/routine-templates`
- "make me a reading triage routine"
- "daily handoff routine"
- "morning flame brief routine"
- "github pr triage routine"
- "weekly vault harvest routine"

## Flow

1. Ask which template (1–5)
2. Ask the user for the required placeholder values (priorities / org / delivery channel)
3. Print the filled-in Prompt + the setup checklist
4. User pastes into claude.ai/code/routines

## Templates index

| # | File | Schedule | Connectors |
|---|---|---|---|
| 1 | `templates/01-daily-reading-triage.md` | daily 09:00 | Burn / Raindrop / Readwise |
| 2 | `templates/02-weekly-vault-harvest.md` | Sunday 20:00 | Burn |
| 3 | `templates/03-morning-flame-brief.md` | daily 08:00 | Burn |
| 4 | `templates/04-github-pr-triage.md` | weekday 17:00 | GitHub |
| 5 | `templates/05-focus-block-handoff.md` | daily 18:30 | Burn + Slack/Email |

## Rules

- Don't invent new templates on the fly — if user asks for something not in the 5, offer the closest match + say "PR a new one at https://github.com/Fisher521/routine-templates"
- Always show the **rules** section of the picked template to the user so they know what the routine won't do
- If user lacks the required connector, link to setup docs, don't skip it

## Links

- Repo: https://github.com/Fisher521/routine-templates
- Claude Code Routines: https://www.anthropic.com/news/claude-code-routines
- Pairs with: [Burn](https://burn451.cloud?ref=routine-templates)
