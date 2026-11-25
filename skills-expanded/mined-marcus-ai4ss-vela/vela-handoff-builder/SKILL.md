---

name: vela-handoff-builder

description: Use this when turning a user request into a bounded VELA Codex handoff packet.

---



# VELA Handoff Builder



Use this skill to create or revise a `vela.codex.handoff.v1` packet.



A valid handoff must name:



- task;

- relevant files;

- excluded files or directories;

- constraints;

- expected output format and path;

- review standard;

- validation commands;

- whether human review is required.



Keep the handoff small. If the task spans too many files or goals, split it into multiple handoffs.
