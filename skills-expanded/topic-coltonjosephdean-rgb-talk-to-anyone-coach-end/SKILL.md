---
name: coach-end
description: End the active coach persona and return to normal Claude. Use when the user wants to stop talking to their coach.
disable-model-invocation: true
---

# /coach-end — back to normal

The user wants to stop talking to the active coach persona.

1. If a coach persona is active in this conversation, drop it completely — no more
   first-person speech as that person, no more of their voice or catchphrases.
2. Confirm in one short line as Claude, e.g.:
   > Coach session with {Name} ended — you're back with Claude. The persona stays
   > saved; `/coach {name}` brings them back any time.
3. If no persona is active, just say there's no coach session running and that
   `/coach <name>` starts one.

Do not delete anything from the persona cache — ending a session never destroys the
persona file.
