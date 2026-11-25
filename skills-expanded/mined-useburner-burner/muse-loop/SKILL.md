---
name: muse-loop
description: Test burner end to end through Muse in Zach's browser - send Muse a command, watch its activity timeline while it runs, fix what it shows, push, repeat. Use when debugging setup or a "use my burner to..." task through Muse.
---

# Testing burner through Muse

Muse (an AI assistant) is the real user of burner. This loop issues a
command to Muse, reads exactly what Muse ran, fixes burner, and repeats.
Fix only the interface between the assistant and the phone (burner's
commands, recipes, setup and SKILL.md). Muse's own judgement ("the
strongest margin play") is not ours to fix.

## Where Muse is

- Zach's **Mac** Chrome, **personal** profile. Not the Windows machine and
  not the PP profile (Muse won't load there).
- If the browser tools only see your own tab group, ask Zach to open the
  Muse tab in that group, or ask for the chat URL.
- Muse often runs in a **side chat**: open the "Chats" menu (three lines)
  and pick the right one. Don't reload the main chat.
- Keep the tab open between rounds. Zach wants it left open.

## Each round

1. Push the fix (from the device folder, as useburner, straight to master).
2. Make Muse pick it up:
   - Tell Muse "update my burner". `burner update` prints "Re-read SKILL.md";
     make sure Muse does.
   - The site caches skill.md for 10 minutes. For a fresh copy, point Muse
     at `https://useburner.si/skill.md?v=<commit>` or
     `https://raw.githubusercontent.com/useburner/burner/<commit>/SKILL.md`.
   - Check: `burner version` prints `burner <commit> (skill rev <rev>)`. The
     commit must be the one you pushed, and the rev must match the
     "Skill rev" in the header of the skill.md Muse read. If they differ,
     Muse is on the old copy, and the round proves nothing.
3. Send Muse one concrete command, like a user would ("use my burner to…").
4. **While it runs**, open the activity block on the right under "Today",
   then its **timeline**. Each step shows the exact bash command, duration,
   exit code and screenshots. The panels scroll. This is the source of
   truth, not Muse's chat summary. Never ask Zach to paste logs.
5. Paste the timeline's commands into `python3 tools/offburner.py`. Each
   hit is somewhere Muse went around burner: a missing command or skill row.
6. **Pause and assess** after each use case: what was slow (durations),
   what failed (exit codes), what Muse improvised, and what Muse got wrong
   because SKILL.md misled it. Then fix, push, and go back to step 1.

## Gotchas

- First-run questions (which device, Tailscale) only show in a **fresh**
  chat. Re-runs skip finished steps.
- Muse reads roughly the first 60 lines of SKILL.md closely. Put what
  matters in Common requests (tests/test_skill_lint.py enforces this).
- Muse starts each command in a fresh shell, so it should call
  `~/burner/bin/burner` by full path.
- A new Muse workspace may need its Tailscale approval again; `burner setup
  --step tailnet` prints the link.
- Never sign in, sign up or pick an account for Zach. Stop and ask.
- Zach and Muse can share one phone. If Zach is testing too, pause.
