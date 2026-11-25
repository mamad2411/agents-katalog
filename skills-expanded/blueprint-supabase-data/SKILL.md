---
name: blueprint-supabase-data
description: "Turn the spec's tables into Postgres migrations with row level security for every read and write, a seed, and tests per kind of user."
---

# Data and who may touch it

The browser calls the database directly with the publishable key, so everything the spec says about who may do what
is enforced HERE, in Postgres, or nowhere.

1. One migration per change in `supabase/migrations/` (`yarn supabase migration new <name>`); once one has been pushed
   to production, change things in a new one, never by editing it. Primary keys, NOT
   NULL, UNIQUE and CHECK as the spec's tables say; foreign keys as its relations say. Every table has a primary key.
2. Every table in `public`: `alter table … enable row level security;`, then one policy per operation the spec
   allows, named for what it permits, following the spec's four columns:
   - write the role: `to authenticated` or `to anon`, never leave it to default to everyone;
   - a row's owner is a column `owner uuid not null default auth.uid() references auth.users (id)`, and every
     policy on it compares `owner = (select auth.uid())` — in `using` for read, change and delete, and in
     `with check` for add and change, so nobody can add or move a row into someone else's name;
   - `using (true)` only where the spec shows the table to everyone.
3. A function the screens call (`supabase.rpc`) runs as the caller (`security invoker`, the default). If one must
   be `security definer`, it checks the caller itself and sets `set search_path = ''`.
4. `supabase/seed.sql`: at least one row in every table in `public`, owned by a seeded user, so the app can be tried
   locally and the security check has a row to try as a stranger. A seeded user is a row in `auth.users` with
   `instance_id` `00000000-0000-0000-0000-000000000000`, `aud` and `role` `authenticated`, an
   `extensions.crypt(<password>, extensions.gen_salt('bf'))` password, `email_confirmed_at`, and the empty string
   (not NULL) in `confirmation_token`, `recovery_token`, `email_change_token_new` and `email_change` — with NULL
   there, signing in as that user fails with a 500. Put the seed users' emails and passwords in the README as local
   test accounts.
5. `.blueprint/public-access.json`: everything a signed-out visitor, or any signed-in user as such, may do, and why:
   `{ "access": [{ "table": "books", "operation": "select", "who": "anyone", "reason": "…" }] }` — `operation` is
   `select`, `insert`, `update` or `delete`, `who` is `anyone` or `signed-in`. Letting signed-in people add rows
   of their own is `insert` for `signed-in`. A row that may be added naming ANOTHER user in a user column (an
   assignee, a recipient) is `insert-for-another` with that `"column"`; letting someone change a row's user column
   over to themselves (taking a task, claiming a book) is `update-owner` with that `"column"` — a plain `update` does
   not cover it. Nothing else goes in it.
6. `test/data.test.ts`, per table, through `test/local-stack.ts`: the owner adds, reads, changes and deletes a row;
   another signed-in user cannot see or change it, and cannot add one in the owner's name; a signed-out visitor
   gets only what the spec allows; every NOT NULL, UNIQUE and CHECK is refused when broken.

Done when the check passes: the migrations and the seed apply to a fresh local database, `yarn build` and `yarn test`
succeed and `test/` has the data tests.

## Always

- Read `.blueprint/spec.md` first. It is the agreed specification; do not widen it.
- When you need a decision, ask it through the blueprint question tool and stop. Do not guess.
- Do not run `git init`: a new repository loses the folder's trust and the next unattended step stops at Claude
  Code's trust prompt. The user adds git themselves after the build if they want it.
- Say you are done by stopping; the executor runs the check. Do not claim success yourself.
