---
name: core-schedule
description: "Work process. The main agent's own clock (node step 558-3). Load it when the person asks to do something on a schedule, every day or week, at a time, to remind, or to automate a recurring job of the node."
---

# Your schedule

**Process: work** — the schedule is data in `data/cron.json` of this folder, never code; no commit, no build.

The core wakes you on a clock: entries in `data/cron.json`, event `agent-task`; an entry's `message` is your task when it fires
(ordered by the owner, step 558-3).

- Fields: `time` HH:MM, `repeat` once | daily | weekdays | weekly | monthly, `start` YYYY-MM-DD, `enabled`, `message`.
- Write the entry only after the person's «yes» to one line: what, when, how often.
- When it fires, the work goes to the element that does it (`npm run task -- <id> "<task>"`), not to you.
- The core shows it in «Automated management → Cron events».
- No personal data in git — the schedule file is outside it.

## Reminders — the deep memory's (steps 630, 636)

«Напомни мне через неделю про день рождения мамы», «напомни завтра в 10», «напоминай каждый год …» — a reminder, not a question to
the memory («напомни о …» without a time is `npm run remind`). A reminder is the deep memory's own essence (the owner, 2026-11-03:
«сейчас мы говорим о памяти у которой напоминания являются её собственной сутью»), so it goes there:
1. Count the date and time yourself from today on this computer (`date`); no time named — 09:00.
2. `npm run remember -- "<the person's words>" --remind-at "<YYYY-MM-DD HH:MM>" [--repeat yearly|…] --remind-text "<what to remind,
   in the person's language — «Сегодня день рождения мамы»>"`. The memory keeps the phrase (the fact: mum's birthday) and puts the
   reminder into its own calendar; the memory element stays on while a reminder waits in it.
3. Answer with the receipt it prints (`===REMINDER_SET===`), in words, and the calendar's link: «Напомню во вторник, 10 ноября, в 09:00:
   день рождения мамы — видно в календаре памяти: <link>. Если не так — поправлю». A model turning «завтра в десять» into a date is
   wrong about once in twenty (the former Telegram Desk) — the receipt is where the person catches it. Ambiguous («на следующей
   неделе», «вечером») — ask one question first.
4. At that minute the reminder surfaces in your main chat by itself — «⏰ Напоминание · Глубокая память» and the words as a quote: the
   memory's clock calls the core's notice door, no model, no agent woken (the owner, 2026-11-03: «события крон должны приходить не
   затрагивая искусственный интеллект»). You do nothing then.
5. `===REMINDER_FAIL===` or the memory off — your own calendar instead, and say so: `npm run reminder -- add "<YYYY-MM-DD HH:MM>"
   "<the words>" [--repeat …]` (event `telegram-message`: «⏰ Напоминание · Главный агент» from your bot, no agent woken; `list` /
   `cancel <id>`).
Every reminder is visible in a calendar — the memory's (Память → Крон события) or yours (Главный агент → Автоматизированное
управление → Крон события); never a reminder nobody can see (the owner, 2026-11-03). A computer off at that minute misses it.
