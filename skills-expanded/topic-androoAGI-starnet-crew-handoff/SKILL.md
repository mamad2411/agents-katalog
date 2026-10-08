---
name: crew-handoff
description: "Hand one job to a crewmate with a brief they can finish without asking back: the right agent, settled context, a checkable definition of done, a return shape, and proof of what came back."
license: MIT
metadata:
  title: "Crew Handoff"
  category: "Station"
  author: "StarNet"
---

A delegated worker runs its own loop on your brief and nothing else. It cannot see your conversation or read your intent. Everything it needs to finish goes in the handoff — or it returns something plausible instead of something right.

## Method
1. **Pick the crewmate by what they own (team.config).** Read the candidate's Dossier — purpose and standing orders — and give the job to the specialist whose desk it is, not whoever is idle. If nobody fits, team.summon can add a specialist; the Commander confirms it in APPROVAL mode.
2. **Know what a worker can do.** A dispatched worker runs unattended with web, files, memory and studio tools, but never the shell: keep shell work for yourself. station.layout shows who sits where.
3. **Write the prompt as the job, finished.** One paragraph: the deliverable, who it is for, the scope boundary (what NOT to touch), and done stated as something checkable — "three options under $50, with links and the date checked", not "look into pricing".
4. **Put what you already know in `context`.** File paths, findings, decisions, constraints, the Commander's stated preferences. It arrives as settled starting knowledge, so the worker does not re-derive it. Do not restate the task there.
5. **Pre-answer the questions they would ask.** Walk the brief as the worker would: which source wins on conflict? what format? what if the data is missing? Answer each, or name the default to take and ask them to flag it.
6. **Fix the return shape.** Say exactly what comes back. When the result feeds code or another step, pass a `resultSchema`: the station validates the result, allows one bounded repair, and never accepts invalid output as done.
7. **Choose where it runs.** Pass `session` with an existing session's name to file the work there — session.list shows the real names, and an unknown name is refused, not guessed. Pass `background: true` when you have other work meanwhile.
8. **Dispatch (team.dispatch)** with the worker's agentId, prompt, context and schema. In APPROVAL mode the Commander is asked first.
9. **Watch without hovering.** For a background worker, team.subagents shows its status and event tail. Correct course with team.steer (id plus the current generation), stop it with team.interrupt, and restart a stale or failed one with team.resume after inspecting it.
10. **Check the return against your definition of done.** The result's artifacts list is the proof of what the worker saved. Its files live in its own workspace — you cannot fs.read them, so never "verify" by looking in yours. Refer to them as "<workerId>'s workspace: <path>".

## Rules
- **One job per handoff.** Two jobs in one brief come back half-done together.
- **Never pass off the worker's result as your own verification.** Say who did the work and what you checked.
- **A thin or failed return is a finding.** Report it by name; never paper over it with your own guess.
- **Never delegate a decision the Commander kept for themselves** — delegate the legwork, bring back the options.
- To learn what happened in another session, call session.peek; never answer from memory.

## Done means
The worker's result meets the definition of done you wrote, the artifacts list names its files, and the Commander knows who did the work and where it is.

## Output
Who got the job and why, the brief as sent (short), the result against the definition of done, the files by workspace, and anything that came back thin.

*Needs the ORCHESTRATOR (team.dispatch and the crew tools), which every run the Commander starts carries.*
