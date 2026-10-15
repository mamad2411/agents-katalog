---
name: supabase-local-dev
description: Initialize, start, stop, and manage local Supabase development environments. Triggered by phrases like "init project", "start supabase", "stop local containers", or "supabase status".
---

# Supabase Local Development Skill

## Goal
Manage the local Supabase environment for development and testing.

## Instructions
1.  Identify the user's intent (e.g., starting the environment, checking status).
2.  Open the relevant rule file(s) for the command:
    - `supabase init` -> [.agent/rules/supabase/commands/init.md](../../rules/supabase/commands/init.md)
    - `supabase start` -> [.agent/rules/supabase/commands/start.md](../../rules/supabase/commands/start.md)
    - `supabase stop` -> [.agent/rules/supabase/commands/stop.md](../../rules/supabase/commands/stop.md)
    - `supabase status` -> [.agent/rules/supabase/commands/status.md](../../rules/supabase/commands/status.md)
    - `supabase services` -> [.agent/rules/supabase/commands/services.md](../../rules/supabase/commands/services.md)
3.  Ensure Docker is running before executing `start` or `stop`.
4.  Verify the environment state with `supabase status` after changes.

## Examples
- "Initialize a new project" -> Use `supabase init`
- "Start the local database" -> Use `supabase start`
- "Stop all containers" -> Use `supabase stop`
