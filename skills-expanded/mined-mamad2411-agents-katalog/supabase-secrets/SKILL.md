---
name: supabase-secrets
description: Manage remote project secrets and environment variables. Triggered by phrases like "set secret", "list secrets", "unsert environment variable", or "supabase secrets".
---

# Supabase Secrets Skill

## Goal
Securely manage environment variables and secrets on the remote Supabase project.

## Instructions
1.  Open the relevant rule file:
    - `supabase secrets set` -> [.agent/rules/supabase/commands/secrets/set.md](../../rules/supabase/commands/secrets/set.md)
    - `supabase secrets list` -> [.agent/rules/supabase/commands/secrets/list.md](../../rules/supabase/commands/secrets/list.md)
    - `supabase secrets unset` -> [.agent/rules/supabase/commands/secrets/unset.md](../../rules/supabase/commands/secrets/unset.md)
2.  Use `secrets set KEY=VALUE` to update remote environment variables.
3.  **Security**: Avoid printing sensitive values in clear text in logs or console.
4.  Verify updates using `secrets list`.

## Examples
- "Add an API key to the project" -> Use `supabase secrets set API_KEY=...`
- "Show all configured secrets" -> Use `supabase secrets list`
- "Delete a secret" -> Use `supabase secrets unset SECRET_NAME`
