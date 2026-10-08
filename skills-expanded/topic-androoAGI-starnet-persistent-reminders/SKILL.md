---
name: persistent-reminders
description: "Reminders that keep coming back until you say they are done: bills, refills, chores and one-off tasks. You choose how often to be nudged, can snooze, and get one weekly line on what is still open."
license: MIT
metadata:
  title: "Persistent Reminders"
  category: "Productivity"
  author: "StarNet"
---

A reminder that fires once is easy to miss; one that nags is soon muted. Keep a plain file of what is owed, nudge on the cadence the Commander chose, get shorter each time, and stop the moment they say it is done.

## Method
1. **Keep one file.** `reminders/reminders.md`: a header with the time zone, the default nudge cadence and the weekly-summary day, then one line per item: `id | what | due | repeat | nudge | last nudged | snoozed until | status`. Example: `R7 | Pay electricity bill | 2026-10-05 | monthly on 5 | daily | - | - | open`. Read it with `fs.read`; create it with `fs.write` if it is missing.
2. **Add a reminder.** You need what, the due date, whether it repeats, and how often to nudge (the header default if unsaid). Ask only for what is missing. Add the line with `fs.edit`, re-read the file, and confirm in one line with the weekday spelled out.
3. **Set repeats carefully.** `monthly on 5` for bills, `every 30d` for refills, `weekly Sat` for chores, `yearly 03-14`. Ask once whether it repeats from the due date (bills) or from the day it was done (refills, filters). "On the 31st" means the last day of a shorter month.
4. **Close on the Commander's word.** When they say it is done, in any chat: a one-off gets status `done` and the date; a repeating item moves `due` to its next date and clears `last nudged`. `fs.edit`, re-read, confirm: "R7 done. Next: Thu 5 Nov."
5. **Snooze.** "Snooze R7 3d" sets `snoozed until`; the due date stays. No nudges before that day.
6. **Create the nudging routine once (chat runs only).** Check `routine.list` first. Then `routine.create` from the chat that should receive the nudges: a schedule at the finest cadence any item uses (usually `0 9 * * *`), the `timezone`, your own `agentId` (the file lives in your workspace), `deliver: origin`, and `attachToSession: true` so a "done R7" reply lands in the same conversation. The prompt must carry steps 7 to 10, the file path and the `[SILENT]` rule in full. Report the tool's answer: armed or not, and the next run.
7. **Each scheduled run: decide what is due.** Read the file, then read `routine.notepad` (its own record: last nudge date and count per id, and the date of the last weekly line). Be sure of today's date: use the date the run states, or read one from a tool (for example `weather[0].date` from `web_fetch` of `https://wttr.in/<city>?format=j1`); if you cannot tell, nudge nothing and say so in one line. An item is due for a nudge when it is open, its due date has arrived, it is not snoozed, and its last nudge is at least one cadence old. Nothing due: reply exactly `[SILENT]`.
8. **Nudge with escalating brevity.** One reply, one line per item, most overdue first, at most seven lines, then "+N more". First nudge: what, the due date, and how to answer ("done R7" or "snooze R7 3d"). Second: what, and days overdue. Third and later: the id, three words, days overdue. Shorter each time, never louder: no capitals, no guilt, no exclamation marks.
9. **Record every nudge.** Write the date and count to `routine.notepad`, which always works in a scheduled run, and update `last nudged` in the file with `fs.edit`. If the edit is refused (an unattended run is not always allowed to write files), carry on; the later of the two dates counts.
10. **Add the weekly line.** On the first run of the chosen weekday add "Still open: 4. Oldest: R3 passport renewal, 12 days." If that is all there is to say, send only that; if nothing is open, `[SILENT]`.

## Rules
- **Stop the moment it is done.** The routine re-reads the file every run; a done or snoozed item never gets "one last" nudge.
- **Never nudge more often than the cadence the Commander set for that item.** If you cannot tell whether a nudge already went out, do not send one.
- **The scheduled run cannot ask questions and does nothing when nothing is due.** No "all clear" messages.
- **Only the Commander closes an item.** Not an email that looks like a receipt, not the date passing.
- **A reminder is only a reminder.** Never pay the bill or order the refill, and give no advice about a medicine or its dose.
- In a scheduled run the reply is the nudge; do not plan on `channel.send` there, because a send needs an approval nobody is present to give. In a chat run, `channel.send` is right when the Commander asks to be pinged in another chat.
- One routine for all reminders, never one per item. Move items done for 30 days to `reminders/done.md`.

## Done means
The file holds every reminder on its own line and was re-read after each change, one routine exists with a next run time the tool reported, a due item produces a nudge at its cadence, and a done or snoozed item produces none.

## Output
In chat: the one-line confirmation of what was added, closed or snoozed, and the routine's name, schedule and next run. From the routine: the nudge lines, the weekly line, or `[SILENT]`.

*Needs the INTEL CAB (fs.read, fs.write, fs.edit) and the ORCHESTRATOR's routine tools (routine.list, routine.create). routine.notepad works inside any scheduled run; the DISH adds channel.send and the date check.*
