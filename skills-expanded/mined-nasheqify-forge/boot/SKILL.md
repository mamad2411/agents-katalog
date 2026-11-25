---
name: boot
description: >
  Start Buddy, Forge's orchestrator, in a session that loads Forge as a
  plugin. Use when the project's or the user's AGENTS.md asks for the
  forge:boot skill before the first answer.
status: active
invocation:
  primary: user-facing
  trigger_patterns:
    - "run the forge:boot skill"
    - "Forge: start Buddy"
disable-model-invocation: false
cc_wrapper: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: boot

The project's or the user's `AGENTS.md` asks for this skill with the line
"Forge: start Buddy. Before the first answer, run the forge:boot skill and
follow the boot entry it returns."

1. If this session's context already holds the `BUDDY-BOOT REQUIRED` entry,
   the boot is running: do not start it again, follow that entry.
2. The framework root `<root>` is the directory that holds `.claude-plugin/`,
   two levels above this skill's folder (`<root>/skills/boot`). Take the
   absolute folder from the skill listing the host shows.
3. Run, as its own call:
   `python3 <root>/scripts/user_scope.py --framework-root <root> --boot-entry`
4. Follow the printed entry before the first answer: it names the soul, the
   user scope, the files to read and the boot sequence. If the command fails,
   say so first in your first answer and follow `<root>/agents/buddy/boot.md`.
