---
name: remote-event-prep
version: 0.1.0
description: |
  Prep a remote or on-site event where Eddie takes the PRESENTATION MacBook -- a cold
  machine with no session history, no repos, no id8brain. Builds the self-contained
  offline-safe kit, the run-of-day cockpit, the cold-start context file, and the iCloud
  handoff, so the cold laptop walks in warm. Locked by Eddie 2026-06-29: "this is how we
  do this always from now on when prepping a remote event where I'm taking the MBP."

  Triggers on: "/remote-event-prep", "prep the event", "I'm taking the MBP", "remote event
  prep", "workshop prep for the venue", "prep the presentation laptop", "get the talk kit
  ready", "on-site tomorrow". Use for any talk, workshop, demo, or client visit run off a
  machine that has not been in the prep sessions.

  Reads: memory feedback_remote_event_mbp_prep_protocol (the source protocol),
  feedback_log_work_as_standard_practice. Lessons baked in from the 2026-06-11 ASQ talk
  (stale browser cache, screen-share vs chromeless PWA) and the 6/29 D&B workshop prep.
---

# /remote-event-prep -- make the cold MacBook walk in warm

The presentation laptop is COLD: no memory, no repos, no connection to anything decided
during prep. Venue wifi is unreliable. SendUserFile lands wherever Eddie reads the chat,
not on the other Mac. Any Claude session opened cold there will contradict the prep unless
you hand it the context deliberately. This protocol closes all four gaps.

## Steps

1. **Build the kit** in the engagement worktree: every event deliverable (deck, handouts,
   runbooks, demo pages) finished and in one folder.

2. **Self-contained + offline-safe.** Every file inlines its assets: no external/CDN refs,
   no `@import`, no remote fonts or images. Each file must render with ZERO internet.
   Verify by actually opening the files with wifi off, not by reading the source.

3. **Run-of-day cockpit** (`INDEX-RUN-OF-DAY.html`): one entry point linking everything in
   order, with roles, operational reminders, and Eddie's human checklist. This is the only
   file he has to remember.

4. **Cold-start context file** (`CONTEXT-COLD-START.md`): a self-contained briefing
   addressed to the cold machine / a cold Claude session. Structure, in order:
   - The HARD RULES first (never email without Eddie's gate, what stays verbal, never
     live-debug in front of the room).
   - Who/what: the event, the audience, the ask.
   - Run-of-day.
   - The deliverables and where they live on this machine.
   - A "decisions made this session, do NOT contradict" section.
   Mark it INTERNAL/EDDIE ONLY if it carries pricing or strategy.

5. **Sync via a clearly-named iCloud Drive folder**
   (`~/Library/Mobile Documents/com~apple~CloudDocs/<event>/`): the unzipped files (so he
   opens them directly) PLUS a zip. iCloud is fine for documents; never for code/deployment.

6. **Tell Eddie to download the cloud files locally on the MBP tonight** (click any
   cloud-icon file so iCloud materializes it). A cloud placeholder that never downloaded is
   a blank screen at the venue.

7. **Validate before the day, and log it.** Run/test everything that can be tested cold and
   write the result into the cockpit's readiness section. Known traps from the field:
   - Browser cache lives OUTSIDE the project folder -- a reinstalled/updated deck can still
     serve stale from Chrome's cache. Validate in a fresh browser profile or with a hard
     reload, on the MBP itself if possible.
   - Screen-share tools (Webex etc.) may not see chromeless/PWA windows. Decide the share
     mode in advance (share the SCREEN, not the window) and put a fallback in the cockpit
     (phone-as-prompter worked at ASQ).

Done means: kit built, everything opens offline, cockpit indexed, cold-start file present,
iCloud synced, Eddie reminded to materialize locally, validation logged.
