---
name: blueprint-supabase-ui
description: "Build the spec's screens in Vue, reading and writing Supabase from the browser."
---

# Screens

1. The screens in the spec, no more. Vue 3 Composition API, plain and readable; a list, a form, a detail as needed.
   Every call goes through the one client in `src/client/supabase.ts`.
2. Every error Supabase returns is shown to the user in words, not swallowed. A refusal by row level security
   (`42501`) is said as "you cannot do this", not as a crash.
3. The screen never decides who may do what: it may hide a button, but the database is what refuses.
4. Text in the language the spec says.
5. `test/ui.test.ts`: the main screens' logic works against the local stack (a list shows rows, a form adds one).
   Components that need a DOM can be tested with a second vitest project using happy-dom.

Done when the check passes: `yarn build` and `yarn test` succeed and `test/` has the ui tests.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
