# Challenge 3 — Build Your Own Skill

**Time:** ~12 min · **You'll need:** `08_SKILL_template.md`, `03_ProjectAtlas_StatusData.csv`

## Goal
Turn a task you repeat into a reusable **Skill**, so you stop re-prompting — and cut credits.

## Steps
1. Pick a task you do often (weekly report, meeting prep, a standard email).
2. Get a good result **the manual way first**. For example, upload `03_ProjectAtlas_StatusData.csv` and ask:
   ```
   Read this status CSV and write a one-page weekly status: overall RAG, done this week, up next, risks with owners, and decisions needed.
   ```
3. Once you like it, save it as a skill:
   ```
   Save this as a skill called "weekly-status-report". Trigger it when I say "run my weekly status". Keep this exact format and only use the status labels On Track, At Risk, Blocked, Complete, Not Started.
   ```
4. **Name it clearly** and give it a good description — that's what makes it fire.
5. **Test it** on fresh data: start a new chat and type `run my weekly status`.
6. Check the cost: type `/cost` to compare the skill run vs. the original prompt.

## What good looks like
Saying the trigger phrase runs the whole workflow and returns **your** format — hands-off. (Peek at the finished [`weekly-status-report.md`](../skills-starter-kit/weekly-status-report.md) example.)

## Stretch it
Add a rule: `If any milestone is Blocked, put a ⚠ at the top and list the blocker first.`

## Troubleshooting
- Skill won't fire? The **description/trigger phrases** are too vague — name the exact words you'll say.
- Doing too much? One skill = one scenario. Split a mega-skill into two.
