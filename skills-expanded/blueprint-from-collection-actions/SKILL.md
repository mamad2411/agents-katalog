---
name: blueprint-from-collection-actions
description: "Build the source's actions and ingests the spec decided to build as Postgres functions and Supabase Edge Functions, and write down the ones left to a person."
---

# Actions and ingests, as features

Read `.blueprint/actions.json` (written with the spec, and agreed when the spec was approved). If it does not exist, the
source had no actions or ingests: stop. Each entry names an action (`books.actions.tidy`) or an ingest (`books.ingest`),
what it was (`kind`) and what was decided (`decision`). The original instructions are in
`.blueprint/source/collections/<slug>/templates/`.

For every `feature`, build it as below, unless an earlier step already built it because a must-have needed it: then
check it against its entry and give it its test here instead of building it a second time.

- **mutate** — a Postgres function the screen calls with `supabase.rpc`, in a migration, and a button on the record's
  screen. It runs as the caller (`security invoker`), so the table's RLS still decides; its `require` is checked
  inside it, its `set` is the change it makes, its `params` are its arguments.
- **chat / agent** — read the template: it says what the agent was asked to do. Build that as the app's own logic.
  Where a step genuinely needs a language model (summarising, classifying, drafting text), call the Claude API from a
  Supabase Edge Function (`supabase/functions/<name>/`), never from the browser: the key is the function secret
  `ANTHROPIC_API_KEY` — locally in `supabase/functions/.env` (in `.gitignore`; the check fails otherwise), in
  production set by the person with `yarn supabase secrets set ANTHROPIC_API_KEY=…`. Never write the key's value
  yourself: tell the person, in the README, where to put their own key. The function checks the caller's session
  before doing anything. If the app uses functions, `db:start` must not leave out `edge-runtime`.
- **ingest** (rss / atom / http-json) — a job that fetches the source, maps each item as the ingest's `map` says, and
  inserts or updates records by the `idFrom` it names, never duplicating. Put it in an Edge Function, run it on the
  schedule the ingest declares with `pg_cron` + `pg_net` (a migration), and say in the README how to run it once by
  hand. An ingest of kind `agent` is built like an agent action.

Tests in `test/actions.test.ts`, one per `feature`, each with the entry's `name` in the title of its `it(…)` / `test(…)`
(`it("books.actions.tidy: summarises", …)`) — with `it` / `test` imported from `vitest` in that file (`import { it } from "vitest"`); the check reads titles only from
calls to those imports, so a global `it`, a helper of the same name, a comment or a title built at run time does not count, and neither does a `describe(…)` name (`it("tidy")` inside
`describe("books.actions")` is not titled `books.actions.tidy`: write the whole name in every test's own title):
walk the real flow against the local stack and read back what changed. Never call the network in a test: a model call
goes through a client the test replaces with a stand-in, and an ingest job takes the fetch it uses as an argument, so
the test hands it a fixture instead. The tests must pass with no API key set.

For every `manual`: a section in `README.md` whose heading names the entry (`## books.actions.tidy`) and which says,
step by step, what a person does instead. For every `drop`: nothing to build; the spec already says why.

Done when the check passes: `.blueprint/actions.json` matches the source, every `feature` has a test titled with its
name, every `manual` has a README heading naming it, `supabase/functions/.env` (if any) is ignored, and `yarn build`
and `yarn test` succeed.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- A screen or button you add follows `DESIGN.md`: the same classes as the screens already there.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
