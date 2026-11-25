---
name: gtg
description: "Short name (got to go) for pause: before you restart or shut the machine down, stop new work, let running work finish, write handovers and report what remains."
disable-model-invocation: true
argument-hint: "[restart|shutdown] [--in <minutes>] | status | resume"
---

# Got to go

Dependency: `pause`. `pause` is user-only (`disable-model-invocation: true`), so the Skill tool refuses it: read `pause`'s `SKILL.md` in this plugin's skills folder and follow it with the same arguments; never call the Skill tool for it (advisory (agent judgment)).
This alias holds no rules of its own.
