---
name: report
description: Draft a GitHub issue about a Layerwright problem (a tool that fails or misbehaves) for the user to review and send. Use for /layer:report, or before fixing a Layerwright bug.
argument-hint: "[what went wrong]"
disable-model-invocation: true
---

# Report a problem

1. Run `npx layerwright report` in the project. It writes `.layerwright/report.md` from the recorded problems (texts, names and ids removed) and prints a link that opens a prefilled issue on github.com/shayan-m81/layerwright.
2. Add what the user said after the command, and what you saw (the tool, its error, how to repeat it) under "What I was doing" in the draft. Keep design content out.
3. Show them the draft and the link. Nothing is sent until they open the link and submit it themselves.
