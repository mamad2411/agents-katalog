---
name: calendar-event-manager
description: user wants to create a macOS Calendar event with sound alarms and paired Reminders, schedule a meeting, RSVP to an invitation, or set reminders.
allowed-tools: Bash, Read, AskUserQuestion
---

# Calendar Event Manager

Create macOS Calendar events with **tiered sound alarms** and **paired Reminders** so events are never missed across Mac and iOS.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## CRITICAL RULES (Hard-Learned Truths 2026-02-12)

> **These rules are NON-NEGOTIABLE. Violating any of them defeats the purpose of this skill.**

### 1. Calendar + Reminders ALWAYS Together

Every event MUST create BOTH:

- **Calendar event** with multiple `sound alarm` entries (custom sound per tier)
- **Reminders** (3 minimum) as a separate notification channel

Never create one without the other.

### 2. Use `sound alarm`, NOT `display alarm`

```applescript
-- CORRECT: audible alert with custom sound
make new sound alarm at end of sound alarms with properties {trigger interval:-60, sound name:"Glass"}

-- WRONG: silent visual banner only
make new display alarm at end of display alarms with properties {trigger interval:-60}
```

Each alarm supports its own `sound name` property. Use DIFFERENT sounds for different tiers so the user knows which alert level it is by sound alone.

### 3. ONLY Long Sounds (>= 1.4 seconds)

Short sounds get missed and ignored. NEVER use sounds under 1.4 seconds.

**APPROVED sounds only:**

| Sound     | Duration | Use For                   |
| --------- | -------- | ------------------------- |
| Funk      | 2.16s    | At event time (loudest)   |
| Glass     | 1.65s    | 1 hour before             |
| Pop       | 1.63s    | Morning-of / 3 hrs before |
| Sosumi    | 1.54s    | Day-before                |
| Ping      | 1.50s    | 30 min before             |
| Submarine | 1.49s    | Alternative               |
| Blow      | 1.40s    | Gentle early reminder     |

**BANNED sounds:** Hero, Basso, Bottle, Purr, Frog, Morse, Tink (all < 1.4s)

### 4. Multiple Early Reminders Are Mandatory

**Calendar accepts at most 5 alarms per event** (verified 2026-08-17 on a CalDAV
calendar: adding a 6th silently evicts an earlier one, with no error). Budget the
5 slots deliberately and do NOT spend one duplicating a Reminder that already
fires at the same moment.

Default alarm tiers:

| Tier          | Trigger   | Calendar Sound | Reminder          |
| ------------- | --------- | -------------- | ----------------- |
| 1 day before  | -1439 min | Blow           | "TOMORROW: ..."   |
| Night before  | -720 min  | Sosumi         | —                 |
| 1 hour before | -60 min   | Glass          | (via Calendar)    |
| 30 min before | -30 min   | Ping           | (via Calendar)    |
| At event time | 0 min     | Funk           | Due-time reminder |

Plus 3 Reminders: "TOMORROW:" (day before, 9 AM), "TODAY:" (morning-of), and the
due-time one.

> **Use -1439, never -1440.** An exact 1440-minute (24 h) offset is silently
> dropped by Calendar — the alarm simply does not appear on read-back. Verified
> twice on 2026-08-17. `-1439` persists.

#### Early-morning events (before ~9:30 AM)

The default tiers misfire for early events. Adjust:

- The **morning-of 9 AM** Reminder fires _after_ an 08:30 event. Move it to
  ~90 min before the event instead.
- A **-180 min** tier on an 08:30 event rings at **05:30**, waking the user three
  hours early. Drop it; use the night-before **-720** tier instead.

### 5. macOS Notification Settings Prerequisite

Calendar notifications must be enabled in System Settings:

- System Settings > Notifications > Calendar > Allow Notifications = ON
- Alert style = Banners or Alerts
- Play sound = ON

Open with: `open "x-apple.systempreferences:com.apple.Notifications-Settings.extension"`

---

## TodoWrite Task Templates

### Template A: Create Event from Invitation

```
1. Extract event details (title, date, time, location, notes, RSVP)
2. Create Calendar event with 5-tier sound alarms (Blow, Sosumi, Glass, Ping, Funk)
3. Create 3 Reminders (TOMORROW, TODAY morning, due-time)
4. Verify event and reminders created
5. Report full schedule to user
```

### Template B: Create Event from User Description

```
1. Ask user for: event name, date/time, duration, location
2. Create Calendar event with 5-tier sound alarms (max Calendar allows)
3. Create 3 Reminders
4. Verify event and reminders created
5. Report full schedule to user
```

### Template C: Test Notification Setup

```
1. Create test Calendar event 3 min in future with sound alarms (1 min, 2 min tiers)
2. Create test Reminder 2 min in future
3. Wait for user confirmation of notifications
4. Clean up test event and reminders
```

---

## AppleScript Date Construction (CRITICAL)

**NEVER use `date "STRING"` in AppleScript.** String-based date parsing is locale-dependent and silently produces wrong results:

| Anti-pattern                         | What happens                                  | Example                      |
| ------------------------------------ | --------------------------------------------- | ---------------------------- |
| `date "April 1, 2026 at 6:00:00 PM"` | On 24h systems, "PM" is ignored → 06:00       | 4 failures in amonic session |
| `date "2026-04-01 18:00:00"`         | ISO parsed as individual numbers → year 12169 | 1 failure                    |
| `set month` before `set day to 1`    | Day 31 + April (30 days) → rolls to May 1     | 1 failure                    |

**ALWAYS use programmatic date construction:**

```applescript
-- Build date safely: day-first-then-month prevents rollover
set d to current date
set day of d to 1           -- safe floor FIRST (prevents month rollover)
set month of d to April
set year of d to 2026
set day of d to 1           -- now set actual target day
set hours of d to 18        -- 24h format, no AM/PM ambiguity
set minutes of d to 0
set seconds of d to 0
```

### Calendar Discovery (run first)

```applescript
tell application "Calendar"
    set output to ""
    repeat with c in calendars
        set output to output & name of c & " (writable:" & writable of c & ")" & linefeed
    end repeat
    output
end tell
```

Use the first `writable:true` calendar. Never assume "Home" or "Calendar" exists.

### Full Event Creation (Copy-Paste Ready)

```applescript
tell application "Calendar"
    -- Build start date programmatically
    set startDate to current date
    set day of startDate to 1
    set month of startDate to MONTH_CONSTANT
    set year of startDate to YEAR_INT
    set day of startDate to DAY_INT
    set hours of startDate to HOUR_24
    set minutes of startDate to 0
    set seconds of startDate to 0

    -- Build end date (1 hour later)
    set endDate to startDate + 1 * hours

    tell calendar "WRITABLE_CALENDAR_NAME"
        set newEvent to make new event with properties {summary:"EVENT_NAME", start date:startDate, end date:endDate, location:"LOCATION", description:"NOTES"}
        tell newEvent
            -- EXACTLY 5 alarms: a 6th silently evicts one of these.
            -- -1439 not -1440: an exact 24h offset is silently dropped.
            make new sound alarm at end of sound alarms with properties {trigger interval:-1439, sound name:"Blow"}
            make new sound alarm at end of sound alarms with properties {trigger interval:-720, sound name:"Sosumi"}
            make new sound alarm at end of sound alarms with properties {trigger interval:-60, sound name:"Glass"}
            make new sound alarm at end of sound alarms with properties {trigger interval:-30, sound name:"Ping"}
            make new sound alarm at end of sound alarms with properties {trigger interval:0, sound name:"Funk"}
        end tell
    end tell
    reload calendars
end tell
```

### Verification (always run after creation)

Verification is NOT optional. Every failure logged in this file was silent —
the create step returned success in all of them.

```applescript
tell application "Calendar"
    tell calendar "WRITABLE_CALENDAR_NAME"
        set e to first event whose summary contains "EVENT_NAME"
        set out to (summary of e) & " | " & (start date of e) & " -> " & (end date of e) & linefeed
        -- Read BOTH classes: Calendar reports sound alarms back as display alarms.
        set out to out & "alarms=" & ((count of display alarms of e) + (count of sound alarms of e)) & linefeed
        repeat with a in display alarms of e
            set out to out & "  " & (trigger interval of a) & linefeed
        end repeat
        repeat with a in sound alarms of e
            set out to out & "  " & (trigger interval of a) & linefeed
        end repeat
        return out
    end tell
end tell
```

Confirm the alarm COUNT and every trigger interval — do not just confirm the
event exists. Dropped alarms are the most common silent failure.

### Calendar AppleScript bridge limitations (verified 2026-08-17)

| Attempt                                          | Result                                      | Do this instead                                                                   |
| ------------------------------------------------ | ------------------------------------------- | --------------------------------------------------------------------------------- |
| `repeat with e in (every event whose summary …)` | error -1728, "Can't get item 1"             | Collect `uid of (every event whose …)` first, then delete/act per uid             |
| `count of (every alarm of e)`                    | syntax error -2741, no `alarm` class exists | Count `display alarms` + `sound alarms` separately                                |
| `delete (first display alarm whose …)`           | error -10000, AppleEvent handler failed     | Individual alarms cannot be deleted — recreate the whole event                    |
| `delete display alarm <index>`                   | error -10000                                | Same: recreate the event                                                          |
| Read back `sound name` of a created alarm        | Reports 0 sound alarms, N display alarms    | Expected. `sound name` persists at the EventKit level; create sound alarms anyway |

### Paired Reminders Creation

> **NEVER use `default list`.** On this machine it resolves to an empty
> placeholder list literally named `DEFAULT_TASK_CALENDAR_NAME` (an
> unsubstituted template string). `make new reminder in (default list)`
> returns success and writes **nothing** — a total silent failure. Discover
> the real list by name first and target it explicitly.

```applescript
-- Discover lists FIRST; never assume.
tell application "Reminders"
    set out to ""
    repeat with l in lists
        set out to out & name of l & " count=" & (count of reminders in l) & linefeed
    end repeat
    return out
end tell
```

```applescript
tell application "Reminders"
    -- Target the real list BY NAME (usually "Reminders"), not `default list`.
    set targetList to list "Reminders"

    -- Build date programmatically (same pattern as Calendar)
    set eventDate to current date
    set day of eventDate to 1
    set month of eventDate to MONTH_CONSTANT
    set year of eventDate to YEAR_INT
    set day of eventDate to DAY_INT
    set hours of eventDate to HOUR_24
    set minutes of eventDate to 0
    set seconds of eventDate to 0

    -- CRITICAL: `copy`, not `set`. `set x to eventDate` ALIASES the same date
    -- object, so mutating x silently rewrites eventDate too (this corrupted a
    -- due-time reminder to 07:00 on 2026-08-17). `copy` makes a real clone.
    copy eventDate to morningDate
    set hours of morningDate to 7
    set minutes of morningDate to 0
    set seconds of morningDate to 0

    copy eventDate to dayBefore
    set dayBefore to dayBefore - 1 * days
    set hours of dayBefore to 9
    set minutes of dayBefore to 0
    set seconds of dayBefore to 0

    make new reminder in targetList with properties {name:"NOW: EVENT_NAME", due date:eventDate, body:"LOCATION" & linefeed & "NOTES"}
    make new reminder in targetList with properties {name:"TOMORROW: EVENT_NAME", due date:dayBefore, body:"Event tomorrow! LOCATION"}
    make new reminder in targetList with properties {name:"TODAY: EVENT_NAME", due date:morningDate, body:"Today! LOCATION"}
end tell
```

Note `body:` must use `& linefeed &` — a literal `\n` inside an AppleScript
string is the two characters backslash-n, not a newline.

---

## Post-Change Checklist

After modifying this skill:

1. [ ] Sound reference table matches [sound-reference.md](./references/sound-reference.md)
2. [ ] All 5 alarm tiers documented with correct sounds (Calendar caps at 5)
3. [ ] BANNED sounds list is complete
4. [ ] Hook file (`hooks/calendar-reminder-sync.ts`) aligned with skill rules
5. [ ] AppleScript examples use `sound alarm` not `display alarm`

---

## References

- [Sound Reference](./references/sound-reference.md) - Full sound duration data and approved/rejected lists
- [Apple Calendar Scripting Guide](https://developer.apple.com/library/archive/documentation/AppleApplications/Conceptual/CalendarScriptingGuide/Calendar-AddanAlarmtoanEvent.html)

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
