# brain-seed

Instantly seed the brain with pre-built stack conventions so your AI team starts informed from session one — no cold start.

## Trigger

This skill activates when the user runs `/brain-seed`, `/brain-seed <profile>`, or `/claude-teams-brain:brain-seed`.

## Workflow

### Step 1 — If no profile argument given, list available profiles

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py" list-profiles
```

Parse the JSON array and present the options to the user as a clean table:

```
Available profiles:
  nextjs-prisma      Next.js + Prisma (App Router)       15 conventions
  fastapi            FastAPI + SQLAlchemy (Async)         14 conventions
  go-microservices   Go Microservices                     14 conventions
  react-native       React Native (Expo)                  14 conventions
  python-general     Python (Modern Best Practices)       15 conventions
```

Ask the user which profile they want to seed, then proceed to Step 2.

### Step 2 — Seed the chosen profile

```bash
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/brain_engine.py" seed-profile "<profile_name>" "${CLAUDE_PROJECT_DIR}"
```

Parse the JSON response:
- `status` — "ok" or "not_found" or "error"
- `profile` — human-readable profile name
- `conventions_added` — number of conventions seeded
- `message` — confirmation message
- `available` — (only on not_found) list of valid profile names

### Step 3 — Confirm and guide next steps

On success, respond with:
> "✅ Seeded **{conventions_added}** conventions from the **{profile}** profile. These will be injected into all future teammates automatically.
>
> **Next steps:**
> - Run `/brain-remember <text>` to add project-specific overrides on top of the profile
> - Spawn your first team — teammates will receive these conventions immediately
> - Run `/brain-query <role>` to preview exactly what a teammate will see"

On not_found, list the available profiles and ask the user to choose one.

### Step 4 — Handle custom profiles

If the user provides a file path (e.g., `/brain-seed ./my-conventions.json`), pass it directly to seed-profile. The engine accepts file paths in addition to built-in profile names.

Custom profile JSON format:
```json
{
  "name": "My Team Conventions",
  "description": "Our specific stack",
  "stack": ["tag1", "tag2"],
  "conventions": [
    "Always use TypeScript strict mode",
    "Use Zod for validation"
  ]
}
```

## Notes

- Seeded conventions are stored as manual memories — identical to `/brain-remember` entries
- They persist across all future sessions and get injected into every new teammate
- Seeding is additive — you can layer multiple profiles (e.g., `nextjs-prisma` + your own customs)
- `${CLAUDE_PLUGIN_ROOT}` and `${CLAUDE_PROJECT_DIR}` are set by Claude Code's hook environment
