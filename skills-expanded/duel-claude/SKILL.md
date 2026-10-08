# Claude Code — Duel Project Rules

## Ground rules

- Minimal changes only — don't touch unrelated code
- No fake UUIDs or silent error swallowing
- Never use window.history.back() — always use explicit navigate()
- Supabase returns PromiseLike not Promise — use try/catch not .catch()
- Always run npm run build to verify before committing
- Before any changes: show files to touch, flag risks, wait for confirmation
- After editing any navigation call, re-read the exact line with grep
  and confirm the path is a valid string with correct syntax before committing
- After every fix: commit, push, and remind me to create a PR
- Always run git fetch origin && git log --oneline origin/main before
  starting work to confirm what's on main
- Before writing any code that reads from or writes to Supabase,
  run SELECT queries against the live DB to confirm every table
  column, constraint, and RPC function actually exists with the
  expected names and types. Never assume schema.sql matches the
  live DB.

## Git & deploy workflow

- Push directly to `main` — no branch/PR pipeline required
- Verify fix is on main before closing a bug — git log main must contain the commit
- Check Netlify deploy hash matches latest main commit before testing on playduel.app
- QA against main/production only

## Tech stack

- React + Vite + TypeScript + Tailwind
- Zustand (persisted to localStorage)
- Supabase (auth, database, realtime) — project: maqjhjvgfvomslktfznz
- Netlify (auto-deploys from main) — live URL: playduel.app
- Supabase requires legacy JWT anon key (eyJ... format)
- RLS is ENABLED on all public app tables (profiles through moves); rollout SQL in `supabase/phase8_rls_rollout/`

## RPC surface area (frontend callers)

- Core gameplay:
  - `submit_move`
  - `set_player_ready`
  - `set_player_present`
  - `abandon_game`
- Guess Who:
  - `check_guess`
  - `reveal_secrets`
- Chat:
  - `mark_messages_read`
- Word Blitz:
  - `update_word_blitz_player_slice`
  - `finish_word_blitz_game`

## Render (DotDash server)

- `render.yaml` service name is `duel-game`
- Deployed Render URL is `duel-fast.onrender.com`

## Key files

- src/lib/database.ts
- src/store/authStore.ts
- src/store/onboardingStore.ts
- src/pages/DiscoverScreen.tsx
- src/pages/ProfileScreen.tsx

## Agent Working Rules

These rules apply to all agents working on the Duel project.

### A (Architect) Rules

- When diagnosing a bug, do not stop at the first problem
  found. Always ask: is this the root cause, or a symptom?
  Trace the full chain before reporting.
- When a fix is proposed, explicitly state what else could
  still be broken even after the fix lands.
- Before closing a bug as fixed, verify the fix commit is
  on main — not just on a feature branch.
- When multiple files share the same pattern, check all
  of them. A bug in one is likely a bug in all.
- Always verify live DB state before assuming schema.sql
  or DATABASE_AUTHORITY.md reflects reality.

### B (Builder) Rules

- "Build passed" is not done. After every implementation,
  manually trace through the code and confirm each feature
  is actually reachable and triggered correctly. Dead code
  that builds clean is still dead code.
- Before implementing any feature that calls a Supabase
  RPC, verify the RPC is deployed to the live DB. If
  not confirmed, flag it before implementing.
- When a spec includes a trigger condition, verify it is
  explicitly defined. If it is not, ask before building.
- When a change touches multiple files with different
  architectures, read all of them before writing any code.
- Never assume a merged branch means the fix is live.
  Netlify deploys from main — confirm the deploy hash.

### QA Rules

- Always check that new state variables are actually
  mutated somewhere — not just initialized and read.
- When a change touches multiple files, review all of
  them not just the primary file.
- Explicitly verify that RPC calls in frontend code match
  functions that are confirmed deployed on the live DB.
- Check that every new feature has a reachable trigger —
  trace the code path from user action to state change.
- "Build passed" is not a quality signal. Ignore it.
  Focus on logic, wiring, and reachability.
- Flag dead code explicitly — code that is written but
  can never be reached is a blocking issue.

### DBA Rules

- Before any frontend feature is implemented that calls
  an RPC, confirm whether that RPC exists on the live DB.
- After every migration is written, produce a minimum
  deployment SQL block that can unblock frontend work
  immediately, separate from the full migration.
- Always distinguish between what is in migration files
  vs what is actually deployed to the live DB. These
  are not the same thing.
- Never assume constraints match documentation. Always
  verify live constraints before writing RPCs that depend
  on them.

### UX Rules

- Always review failure states and unhappy paths, not
  just the happy path. For every flow, ask: what does
  the user see when something goes wrong?
- When reviewing a feature spec, explicitly flag any
  trigger conditions that are ambiguous or missing.
- Flag edge cases that could create confusing UX even
  if they are not bugs — confusion is a UX bug.
- When multiple screens share a pattern (e.g. result
  screens across 6 games), flag inconsistencies between
  them explicitly.

### RM (Release Manager) Rules

- Never declare a fix live until Netlify deploy hash
  matches the expected main HEAD commit.
- QA runs on the branch. Nothing is declared fixed until
  it is on main AND Netlify shows the correct commit hash.
- No frontend feature that calls an RPC should be merged
  until DBA has confirmed the RPC is deployed to the
  live DB.
- After every merge, immediately verify the Netlify
  deploy hash and report it.
- Track what is on each branch vs main at all times.
  Flag diverged branches before they cause merge conflicts.

### General Rules

- No frontend feature that calls an RPC should be merged
  until DBA confirms the RPC exists on the live DB.
- Specs must include exact trigger conditions, not just
  desired outcomes. If a trigger is ambiguous, stop and
  clarify before implementing.
- A fix is not done until it is on main, deployed, and
  verified on the live site. Branch-only fixes do not count.
- When in doubt about live DB state, query it directly.
  Documentation lies. The DB does not.
