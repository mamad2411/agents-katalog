---
name: diagnose-reminder-delivery
description: Use when a reminder was created (add_reminder confirmed it) but never arrived in Telegram, or when reminders seem to fire late/never. Walks through the exact chain of failure points for this project's reminder pipeline, in the order most likely to be the actual cause.
---

# Diagnosing a stuck reminder

This project has two independent processes touching the reminders database:
`RemindersMcpServer` (writes, via the `add_reminder` MCP tool) and the main
web host's `ReminderPollingHostedService` (reads/delivers, every
`Reminders:PollSeconds`). A stuck reminder means one of them is looking at
different data than you'd expect. Check in this order — each step below was
a real bug found this way, not a hypothetical.

## 1. Confirm the row actually exists and isn't already fired

Query `{Claude:WorkDir}/.agent-data/reminders.db` directly (copy it first —
don't touch the live file while the host may have it open) and look at the
raw `remind_at` column as text, not through application code yet:

```sql
SELECT id, chat_id, remind_at, fired, message FROM reminders;
```

## 2. Check the timestamp format — this is the #1 real cause

`remind_at` must be a UTC timestamp ending in `Z`
(`2026-09-05T16:09:55.0000000Z`). If it has a `+03:00`-style offset instead,
the delivery query compares it as **plain text**, not as a real datetime —
and mixed offsets don't sort correctly as strings even though the underlying
instant is fine. This was a real bug: `DateTimeOffset.ToString("O")` preserves
the original offset; `DateTimeOffset.UtcDateTime.ToString("O")` normalizes to
`Z`. Both the write side (`AddAsync`) and the compare side (`PopDueAsync`'s
`@Now` parameter) must use the normalized form, or old rows written before a
fix stay permanently unfireable even after the fix lands.

## 3. Confirm the polling loop is actually running

`ReminderPollingHostedService` and `ReminderDeliveryService` should log on
every tick: `"Reminder polling tick"` and `"DeliverDueAsync at ...: N due
reminder(s)"`. If these lines never appear, the host isn't running the loop
at all (check for a crashed `BackgroundService` — remember
`HostOptions.BackgroundServiceExceptionBehavior` defaults to `StopHost`, so
one throwing background service takes the *whole* app down silently).

## 4. If it ticks but always reports 0 due — suspect the DB path, not the query

If step 2's data looks correct but `DeliverDueAsync` consistently reports `0
due reminder(s)`, the web host is very likely reading a **different**
database file than the one being written to. The classic cause in this
codebase: a config fallback written as

```csharp
var path = configuration["Reminders:DbPath"] ?? Path.Combine(workDir, ".agent-data", "reminders.db");
```

`??` only catches `null`. If `appsettings.json` ships `"DbPath": ""` (empty
string, not absent), `configuration[...]` returns `""` — which is not
null — so the fallback never triggers, and `SqliteReminderOptions("")` opens
a fresh anonymous temp database on every single connection. Every write and
every read silently operates on its own throwaway database, so nothing is
ever "missing" — everything is just always empty. Fix: check with
`string.IsNullOrWhiteSpace(...)`, not `??`, for any config value that ships
an empty-string placeholder rather than being omitted.

## 5. Verify by testing the repository directly, in-process

Don't trust console output of Cyrillic/non-ASCII text without setting
`Console.OutputEncoding = new UTF8Encoding(false)` first in whatever throwaway
test script you write — a `Console.WriteLine` showing `????` does **not**
mean the data is corrupted, it usually means your test script's own console
encoding is wrong. Confirm with a byte-level comparison
(`Encoding.UTF8.GetBytes(...)`) before concluding there's a real encoding bug
upstream.
