---
name: verify-seira
description: "Prove that a Seira server, conversation, or chat UI change works, against an isolated fake-engine fixture, before you say it works. Use after a change to the server, the bots, the headless verbs, or the chat renderer, and before you open or merge a pull request that claims a user-visible result."
---

# Verify Seira

The full guide is [`docs/verification/README.md`](../../../docs/verification/README.md).
Read it, and read the recipe for your area in its map, before you start.
This skill holds the rules that you must not break.

## Rules

- Use only an isolated fixture. Never drive a Seira app that a person uses,
  and never read or change its data folder (`~/.seira` or `SEIRA_DATA_DIR`).
- Use only the shared control surface: `scripts/control-seira.ts` and
  `pnpm control:seira`. Do not send raw API calls that the surface does not have.
- Give every verb an explicit `--url`. Do not set `SEIRA_URL` or
  `SEIRA_PORT` in the shell: a mutating verb uses them, and port 8799 is the
  default port of an installed app.
- Use only flows that the map in the guide lists. If the surface cannot drive
  your flow, say so. Then use the smoke test or the recipe that the guide names
  for it, and state what it does not prove.

## Steps

1. Start the fixture in its own terminal. Start the script directly, not
   through `pnpm`, so that Ctrl-C reaches it:

   ```sh
   node --experimental-strip-types scripts/control-seira.ts launch
   ```

   It prints the URL, the PID, the temporary data folder, and the log path.
   Only `FAKE_CLAUDE_*` variables go to the fixture. Use them to script the
   fake engine.
2. Check the fixture from a second terminal:

   ```sh
   pnpm control:seira doctor --url http://127.0.0.1:PORT
   ```

3. Drive the flow with the commands of your recipe. `pnpm control:seira help`
   lists every verb. For the chat UI, use `control-seira ui launch` and the `ui`
   verbs ([chat-ui.md](../../../docs/verification/chat-ui.md)).
4. Keep the evidence: the exact command sequence, the JSON from `wait` and
   `messages`, and the log path of the fixture. The evidence must show the
   action and the state that comes after it. A passing unit test alone does
   not prove a user workflow.
5. Stop the fixture with Ctrl-C in its terminal. It stops only its own child
   and removes only its temporary data folder. Do not stop processes by name,
   and do not delete a shared temporary folder.

## Report

Write what you proved, with the evidence, and what you did not prove.
For example: the fake engine proves the command line and the server state,
not real model behaviour.
