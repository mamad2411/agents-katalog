---
name: productivity
description: ADHD-friendly productivity systems — 3-level task breakdown (Project → Milestone → Task), focus techniques, priority frameworks, and beating procrastination with systems instead of willpower. Use when the user feels overwhelmed, has too many unclear tasks, can't focus, is procrastinating, or asks "how do I organize this work". Focused on solo developer workflows, not team PM processes.
---

# Skill: Productivity

> **Purpose**: Get more done with less mental effort. Systems beat willpower.

## When to Use
- Feeling overwhelmed or scattered
- Too many tasks, unclear priorities
- Struggling to focus
- Procrastinating on important work

---

## Task Breakdown Method

### The 3-Level Breakdown
Every big task becomes small, doable steps:

```
Level 1: Project      → "Build user authentication"
Level 2: Milestones   → "Login page", "Session handling", "Password reset"
Level 3: Tasks        → "Create login form HTML", "Add validation", "Call API"
```

**Rule**: If a task takes more than 30 minutes, break it down further.

### Example Breakdown
```markdown
## Build Task Manager CLI (Java)

### Milestone 1: Basic Structure ✅
- [x] Create Main.java with menu loop
- [x] Add Task class with title and status
- [x] Implement "add task" command

### Milestone 2: Core Features (Current)
- [x] Implement "list tasks" command
- [/] Implement "complete task" command
- [ ] Implement "delete task" command

### Milestone 3: Persistence
- [ ] Save tasks to file on exit
- [ ] Load tasks from file on start
- [ ] Handle corrupted file gracefully
```

### The Next Action Rule
Always know: "What is the VERY NEXT physical action?"
- ❌ "Work on project" → vague, causes paralysis
- ✅ "Open TaskService.java and add deleteById method" → clear, doable

---

## Deep Work System

### The Focus Block
```
1. Pick ONE task (not two, not three — ONE)
2. Set a timer: 25 minutes (or 15 if ADHD is strong today)
3. Close everything unrelated (Slack, email, social media)
4. Work ONLY on that task
5. When timer rings: stop, take 5-min break
6. Repeat 2-4 times, then take 15-30 min break
```

### Environment Setup
- **Noise**: Use brown noise, lo-fi beats, or silence. No podcasts.
- **Phone**: Face down, silent, in another room if possible.
- **Desk**: Only what you need for the current task.
- **Water**: Full glass on desk. Dehydration kills focus.

### Energy Mapping
Track when you're most focused for one week:

| Time | Energy Level | Best For |
|------|-------------|----------|
| 8-10 AM | 🟢 High | Hard coding, debugging, learning |
| 10-12 PM | 🟡 Medium | Code reviews, documentation |
| 1-2 PM | 🔴 Low | Easy tasks, email, admin |
| 2-4 PM | 🟡 Medium | Feature implementation |
| 4-6 PM | 🟢 High | Focused problem-solving |

Schedule deep work during green blocks. Never waste them on email.

---

## Focus Loops

### The Focus Loop Pattern
```
DO:
  1. Choose smallest meaningful task
  2. Set timer (15-25 min)
  3. Work without interruption
  4. Mark task done ✅
  5. Take 5-min break (move your body)
UNTIL: daily goal is met OR energy is depleted
```

### When Focus Breaks
If you catch yourself distracted:
1. **Don't judge yourself** — just notice it
2. **Write down** the distracting thought (parking lot)
3. **Return** to the task
4. If it happens 3+ times in one session, take a real break

---

## Daily Workflow Template

```markdown
## Morning (5 min)
- [ ] Review yesterday's progress
- [ ] Pick today's 3 most important tasks (MITs)
- [ ] Time-block the MITs into your calendar

## Work Blocks
- [ ] MIT #1 (deep work, 1-2 focus blocks)
- [ ] MIT #2 (deep work, 1-2 focus blocks)
- [ ] MIT #3 (can be lighter)

## End of Day (5 min)
- [ ] Mark completed tasks
- [ ] Write tomorrow's MITs
- [ ] Close all tabs and apps (clean shutdown)
```

### The 3 MIT Rule
**Most Important Tasks** — pick exactly 3 each morning.
- If you finish all 3, the day is a success regardless of what else happens.
- If you only finish 1, that's still better than doing 10 low-value tasks.

---

## Anti-Procrastination Techniques

### 1. The 2-Minute Rule
If it takes less than 2 minutes, do it now. Don't add it to a list.

### 2. The "Just Open the File" Trick
Don't commit to working. Just open the file. Read one line. The hardest part is starting — once you're in, momentum takes over.

### 3. Reward Stacking
Pair a task you dislike with something you enjoy:
- Write tests → then 10 min of something fun
- Fix bugs → then listen to a favorite song
- Document code → then get coffee

---

## Best Practices
1. **Systems > goals** — "code for 30 min daily" > "build an app by June"
2. **Protect your peak hours** — don't waste high-energy time on low-value tasks
3. **Batch similar tasks** — reply to all messages in one block, not throughout the day
4. **Say no to low-priority requests** — your time is finite
5. **Review weekly** — what worked? What didn't? Adjust.

## Common Mistakes
| Mistake | Fix |
|---------|-----|
| No clear priorities | Pick 3 MITs every morning |
| Working when exhausted | Stop. Rest. Resume at peak energy. |
| Multitasking | Single-task. Context switching destroys productivity. |
| Perfect planning, no execution | Plan for 5 min, then execute |
| Ignoring breaks | Breaks are part of the system, not laziness |
