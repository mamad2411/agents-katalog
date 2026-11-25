---
name: remember-this
description: Persist a specific fact, preference, or decision the user just stated using CogmemAi, so it carries across all future sessions. Use the moment the user says "remember this", "remember that", "don't forget", "make a note", "keep this in mind for next time", "from now on", "going forward", or states a personal/project preference you should apply later. Save immediately, do not defer to end of session.
metadata:
  author: HiFriendbot
  version: 1.0.0
  mcp-server: cogmemai
  category: developer-tools
  tags: [remember, save, memory, mcp, preference, developer-tools]
---

# Remember This with CogmemAi

When the user explicitly tells you to remember something, save it to CogmemAi immediately. Don't wait until the end of the session, don't paraphrase loosely, and don't ask for confirmation. The user has done the hard work of identifying what matters; your job is to persist it correctly.

## Trigger Phrases

Save the moment you hear any of:

- "Remember this"
- "Remember that I prefer X"
- "Don't forget X"
- "Make a note that X"
- "Keep this in mind"
- "From now on, X"
- "Going forward, X"
- "Always do X" / "Never do X"
- "Save this for next time"

Also trigger when the user states a stable preference even without an explicit "remember" phrase. For example: "I always use Bun instead of npm" is a preference worth saving even though they didn't say "remember".

## How to Save

Use `save_memory` with:

- `content` — restate the user's fact in one or two complete sentences. Include the *why* if they gave one. Concrete and self-contained.
- `memory_type` — usually `preference` for user preferences, `decision` for project decisions, `identity` for facts about the user, `architecture` for tech-stack facts.
- `importance` — usually 7-9 for explicit "remember this" requests. The user flagged it as important, respect that signal.
- `scope` — `global` if the fact applies across all projects (user preference, identity, tool choice). `project` if it's specific to the current codebase.
- `tags` — short labels so related memories cluster (e.g., `["coding-style"]`, `["deployment"]`, `["communication"]`).

## Examples

### "Remember I'm allergic to em dashes"

```
save_memory({
  content: "User has a strict no-em-dash rule. Never use the em dash character (—, U+2014) in any output: chat replies, code comments, docs, commit messages, marketing copy. Use a comma, parentheses, period and new sentence, colon, or semicolon instead.",
  memory_type: "preference",
  importance: 9,
  scope: "global",
  tags: ["writing-style", "punctuation"]
})
```

### "From now on, deploy via Cloud Run not Lambda"

```
save_memory({
  content: "Deploy target for this project is Google Cloud Run, not AWS Lambda (decided 2026-05-13). Switch was driven by per-request billing simplicity and easier local testing with Docker.",
  memory_type: "decision",
  importance: 9,
  scope: "project",
  tags: ["deployment", "infrastructure"]
})
```

### "I always use Conventional Commits"

```
save_memory({
  content: "Always format git commit messages using Conventional Commits (feat:, fix:, chore:, docs:, refactor:, test:). Subject under 72 characters. Body wrapped at 72.",
  memory_type: "preference",
  importance: 8,
  scope: "global",
  tags: ["git", "commits"]
})
```

## What NOT to Do

- Do not paraphrase so loosely that the rule loses its bite. "User wants concise commits" is too vague to act on.
- Do not save without including the *why* if the user gave one. The why is what lets future sessions handle edge cases.
- Do not deduplicate by deleting older preferences — call `update_memory` instead so version history is preserved.
- Do not ask "do you want me to save that?" — the user already told you to save it.
- Do not wait. Save the moment the trigger fires.

## After Saving

Briefly confirm so the user knows it was captured. One short line. For example: "Saved as a global preference."

## Related Skills

- `cogmemai-memory` — full reference for memory management, types, and importance scoring
- `save-context` — capture multi-fact context vs. a single explicit instruction
- `session-start` — these saved memories surface again via `get_project_context`
