---
name: cutroom-edit
description: Edit a whole recorded talk (lecture, keynote, workshop, panel) into a finished long video, fully local. Syncs every camera, the microphone and the screen recording; cuts fillers, restarts and dead air on word boundaries; proposes section cuts (demos, chatter, weak or failed parts) for approval and marks removed parts on screen; directs a multicam edit that always shows the best angle (speaker, room and audience, the screen, 4K punch-ins); switches to the room mic when the audience speaks; grades the cameras to match; adds an opening title behind the speaker, chapter titles, motion-graphics B-roll and burned-in subtitles; exports YouTube chapters and an .srt. Use when the user says "edit my lecture / talk / keynote", "cut this recording", "multicam edit", "sync my cameras and mic", "make the full video", "remove the filler words", "cut the demo part". For short clips from a talk use the cutroom skill instead.
---

A full edit of a whole recorded talk is the `edit` job of the one cutroom skill, whose `SKILL.md` is in the folder above this one.
Read that page first: it checks the machine with `cutroom doctor` and writes the brief with `cutroom brief`.
Then follow [`workflows/edit.md`](../workflows/edit.md) from its first step; each step names the reference to read.
Its commands are verbs of `cutroom`; `cutroom path` prints the tool's folder, which holds the workflow and `references/`.
For short clips from a talk the same skill's `workflows/cut.md` is the page.
