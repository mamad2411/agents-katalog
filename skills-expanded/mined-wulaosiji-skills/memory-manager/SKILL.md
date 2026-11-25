---
name: memory-manager
description: |
  Persist and retrieve user preferences, task history, and daily notes across sessions — so the
  agent remembers context, avoids repeating questions, and improves over time. Use when: "记住",
  "记忆", "用户偏好", "memory", "preferences", "历史任务", "之前做过", "跨会话记忆",
  "长期记忆", "remember this". The skill that turns stateless conversations into cumulative
  collaboration. Part of the UniqueSkills platform toolkit.
---
# Memory Manager
> Remember what matters, forget what doesn't — and never ask the same question twice.

## When to Use
Use this skill when:
- The user expresses a **stable preference** (language, style, tools, role) that applies across tasks
- The user says **"记住"** or explicitly asks to persist something
- You notice a **pattern** across multiple turns (repeated corrections, recurring requirements)
- The user refers to **"以前"、"上次"、"之前"** and you need to recover past work
- You're starting a new session and want to **load relevant context** before acting
- A task produces a **deliverable or decision** worth recalling later

Do NOT use this skill if:
- The information is a one-time instruction (e.g., "帮我写封邮件")
- The fact is temporary or session-specific (e.g., "今天用这个文件")
- The information is unconfirmed speculation
- The user explicitly says not to remember something

Typical triggers:
- 「记住我喜欢...」「以后都用中文」「上次那个方案」「帮我回忆一下之前的项目」
- "remember this", "my preference is", "what did we do last time", "recall the previous task"
- 「用户画像」「个人化设置」「历史记录」

## Workflow

### Step 1: 探查 — Identify Memorizable Signals
- Scan the conversation for stable, cross-task facts: language preferences, code style, tech stack, job role, industry, recurring projects, persistent constraints
- Distinguish **preferences** (always true) from **task context** (only this session) from **speculation** (unconfirmed)
- Check existing memory to avoid duplicates

### Step 2: 约束 — Define Memory Rules
- Only record facts stated in **affirmative sentences**, ≤50 characters each
- Never record one-time task instructions, temporary context, or unconfirmed guesses
- If a new preference conflicts with an existing one, update (don't add a contradictory entry)
- Mark the memory type: preference, task_history, or daily_memory

### Step 3: 证据 — Verify Before Persisting
- Confirm the fact is genuinely stable (appeared more than once, or user explicitly said "记住")
- For task history, capture: task description, key steps, deliverables and links, final status
- For daily notes, capture date and salient events

### Step 4: 执行 — Write or Update Memory
- Add new preferences with `action: add`
- Update conflicting preferences with `action: update` (deactivates old, writes new)
- Deactivate stale preferences with `action: deactivate`
- Batch multiple independent memory operations in parallel

### Step 5: 验证 — Check Retrieval
- After writing, search memory with a relevant query to confirm it's retrievable
- Verify the preference injects into the system prompt for future sessions
- Confirm no duplicate or contradictory entries exist

### Step 6: 交付 — Acknowledge Concisely
- Tell the user what was remembered (one sentence)
- Don't dump memory IDs or internal details
- If retrieving, present the relevant context and cite it as "from memory"

## Output
- For writes: brief confirmation of what was persisted
- For retrievals: structured context with source type and date
- For updates: note the old value being replaced

## Guardrails
- **Never record one-time task instructions** as preferences
- **Never add a contradictory entry** — update or deactivate the old one first
- **Preferences must be affirmative statements**, not questions or possibilities
- **Memory is private** — never expose another user's memory
- **Don't over-record** — only facts that will genuinely improve future interactions
- **When retrieving**, distinguish "from memory" from current-session facts; if memory is stale, verify with the user

## Related Skills
- **agent-orchestrator** — Pass relevant memory context to sub-agents via hints
- **skill-discovery** — Remember which skills work well for which task types
- **cron-scheduler** — Schedule periodic memory reviews and cleanup
- **enterprise-knowledge** — Cross-reference personal memory with company knowledge

## About
Part of the UniqueSkills platform toolkit — capabilities extracted from the Doubao agent runtime.
🌐 https://uniqueclub.ai | 📂 https://github.com/wulaosiji/skills
