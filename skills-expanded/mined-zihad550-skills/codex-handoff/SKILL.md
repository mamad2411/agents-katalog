---
name: codex-handoff
description: Resume a Codex CLI session in this agent. Use when asked to continue from where a Codex session left off, given its session id.
---

# Codex handoff

Pick up a Codex session's work as if you had been in it: know the goal, what is done, what was in flight, and what the user last asked.

## Steps

1. **Read the transcript.** Run the script that ships with this skill, from the skill's directory (`~/.agents/skills/codex-handoff` when installed globally):

   ```bash
   python3 scripts/codex-transcript.py <session-id>
   ```

   When it reports several matches, pass more of the id. When the output is long, read the whole user side first, then the last 40 entries with `--tail 40`. Done when you have read every user prompt and the final stretch of assistant messages and tool calls.

2. **Check the ground truth.** Work in the transcript's `cwd`. Compare its claims with the repo as it is now: `git status --short`, `git log --oneline -10`, and the files the last tool calls edited. Codex may have stopped mid edit, or the user may have changed things since. Done when every "done" claim you rely on is confirmed in the working tree or the log.

3. **Brief the handoff.** Print, in a few lines each: the goal, what is done (with the evidence from step 2), what was in flight when the session stopped, and the user's last request. Done when the brief names the next concrete action.

4. **Continue.** Carry on with the user's last request under the instructions of the repo you are in. When that request is already finished, or the transcript leaves the next step ambiguous, ask the user instead. Done when you are working on the next action, or have asked.
