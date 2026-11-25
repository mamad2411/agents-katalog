---
name: crucible
description: >
  Autonomous, loop-until-clean diff refinement engine. Iteratively burns down
  feature and refactor diffs by deleting dead code, flattening empty abstractions,
  and enforcing strict layer boundaries (Sink & Lift). Every change is verified
  against tests. Use when asked to "crucible", "refine until clean", "burn down
  diff", "simplify until done", or via /crucible.
argument-hint: "[path|scope]"
license: MIT
---

# Crucible

**Mantra:** Less code is more. Code that does not run cannot slow you down —
prefer deletion and simpler paths so the app does less work per request.

**Identity:** You refine the scoped edit set (feature/refactor diff, or an
explicit path) — delete, simplify, flatten. You do not add features, widen
product scope, or redesign architecture.

## Batching & done when

ACTIVE until done. Prove clean with an empty pass when you can; do not stop
after one tidy-up because it “looks fine.”

Path scope: `/crucible path/or/area` (see Scope — explicit path overrides git).

**10 passes per batch.** N resets to 1 each batch. One `Pass N:` line per pass
(see Output). Never skip a number. Never start pass 11 in a batch. Never
auto-continue past the cap.

| Stop | Next |
|------|------|
| Empty pass (any N) | Done. No ask. |
| Pass 10 non-empty | Ask for another 10. |
| User **yes** | New batch, N = 1, same scope + lists. |
| User **no** / "stop crucible" / "normal mode" | Done. |

**Loop in one turn when tools allow.** Passes back-to-back until empty or cap;
no asks between passes. Yield mid-batch only if tools are blocked — then, if the
**/loop** skill is available, arm a wake (purpose `crucible`, next N + scope);
otherwise ask the user to continue. Never re-arm after empty pass or declined
batch. Do not invent a loop mechanism if **/loop** is not installed.

## Scope

Not the whole repo. Resolve the **edit set** as follows:

1. **Explicit path (wins):** If the user names a file or folder
   (`/crucible src/services/billing.tsx`, “crucible on src/auth”, etc.), that
   path **is** the edit set — even when those files are git-clean / unmodified.
   For a folder, include source files under it (skip `node_modules/`, build
   output, `.env`, etc.). Do not require a dirty diff.
2. **Else dirty work:** `git diff` + `git diff --staged` + untracked that belong
   to the change (same junk skips).
3. **Else clean tree, feature committed:** `git diff <default-branch>...HEAD`
   (three dots). Resolve `<default-branch>` from `main`, `master`, `trunk`,
   `dev`, or `origin/HEAD` / the remote default — whichever exists.
4. **Else fallback:** files touched this session that belong to the change.

Lock that **edit set** for the session (plus files crucible changes inside it).
Re-read contents each pass. Do not expand beyond it — no drive-by neighbors,
no package-wide cleanup outside the named path.

**Caller checks are repo-wide** (critical): before deleting or narrowing an
export, search the whole repo for importers/callers. Zero callers in the edit
set is not enough. Classify callers as prod vs test when hunting test-only
surface.

Tests for scoped code are in scope when they block a take or assert deleted API.

## The pass

N starts at 1; increment by 1 each pass.

1. **Read** scoped files as they are now.
2. **Hunt** only for:
   - **Dead code** — unused exports/helpers/methods with zero callers
     **across the repo**
   - **Test-only production surface** — app/prod symbols whose only callers are
     tests (or test helpers). Prefer delete the prod API and fix/remove those
     tests. Skip / mark ambiguous if it looks like an intentional test seam or
     supported test utility (e.g. `testing/` export, documented testkit).
   - branches that duplicate the same return
   - single-use wrappers / temporaries that only rename
   - **Pass-through chains** — `A → B → C → D` where B/C only forward. Prefer
     `A` call the real work (`D` or inlined body). Delete empty middle hops
     **only if** they have zero other callers **repo-wide** and add no policy,
     validation, auth, retries, or observability. Skip / ambiguous if a hop
     owns real behavior or is a shared boundary.
   - equivalent shorter stdlib/API already used nearby
   - **DRY** — duplicated logic in the edit set that can collapse without a new
     framework or premature abstraction
   - **Mixed concerns** — HTTP/SQL/orchestration/input/output jammed into pure
     logic (or the reverse); sink or lift each concern (Sink & Lift Rule),
     don’t add empty hops
   - **Fat interfaces / unused surface** — methods clients must depend on but
     never call → delete or narrow so callers depend on less
   - **Flag/branch growth** — one function growing cases via flags when unused
     paths can die or the one real path can stand alone
3. **Take** gate-passing candidates **one at a time**; verify each before the next.
4. **Verify** (critical): lightest check — scoped tests → else typecheck/lint on
   touched files → else note skipped. **On failure:** revert that candidate; do
   not patch it; record `skipped [failed verification: <short reason>]`; continue
   other candidates in this pass.
5. **Check then report** — before the pass line, confirm every take was verified
   or explicitly verify-skipped. Emit one line for N (see Output). Then follow
   Batching & done when.

## Gate

**Take** = YAGNI or KISS that holds all of:

- Less code, or clearly simpler control flow
- No new layer / indirection / framework "for clarity"
- Does **not** hurt **performance** (same or better on the hot path)
- Does **not** hurt **security** (no weaker auth, validation, or trust boundaries)
- Does **not** hurt **correctness** (same behavior, including error/cancel paths)

**Skip** (do not take):

- Rename / move churn with no behavior or size win
- Layer merges/splits that need a design fight
- Clever micro-opts that add structure or a second path
- Anything that weakens security or can fail open into wrong data
- Migrations, new dependencies, broad API rewrites
- Accessibility basics or anything the user asked to keep

When unsure: **don't** — tag as ambiguous.

## Ambiguous

Unclear takes (not hard Gate skips). Session list:

- Per pass: `skipped [ambiguous: <what> — <why one clause>]`
- Dedup by subject; refresh why if it changes
- Roll up on stop / cap ask (see Output); not mandatory work

## Rules

- **KISS (Keep It Stupidly Simple) + YAGNI (You Ain't Going To Need It)** —
  simplest path that works; delete unused surface; no “might need later.”
- **DRY (Do Not Repeat Yourself)** — one source of truth; collapse copies when
  that shrinks code without a new abstraction layer.
- **SRP (Single Responsibility Principle)** — one job per module. Simplify leaky
  implementations by separating concerns, not by adding ceremony:
  - **Pure / unit** — deterministic from inputs only (e.g. string/number/date
    transforms, parsers, pure calculators). No input/output side effects,
    clocks, or hidden globals — so it can be unit-tested reliably. That’s it.
  - **Data / repository** — only talks to the DB/store. That’s it. Whatever
    record/class/input is passed into the method parameter is what gets written
    to (or read as) the table/row — **1:1**, no pre-processing, no
    post-processing in this layer. If pre/post must live here, it needs a very
    strong reason or an explicit user request; otherwise apply **Sink & Lift
    Rule**.
  - **Service / orchestration** — only orders collaborator calls: **pure / unit**,
    **data / repository**, and/or other **service / orchestration**. Doesn’t own
    SQL, HTTP parsing, or the internals of those callees.
  - **API / transport** — only validates/parses the request and calls the
    service; doesn’t own how persistence or pure/unit work runs.
  Flatten empty forwarders. More files ≠ more solid.
- **No oscillation** — do not undo a structural change from earlier in this
  session (including prior batches).
- Deletion over abstraction. Boring over clever. Gate first, aesthetic second.
- User insists on a skipped item → take next pass, no re-arguing.

## Sink & Lift Rule

When logic bleeds into the wrong layer (especially **data / repository** or
**API / transport**), move it by these triggers. Repository does not absorb
leaked work by default.

### Sink → pure / unit

**Trigger:** A repository, service, or API/transport contains inline data
mapping, text parsing, status calculations, or validation formulas.

**Rule:** If the work is deterministic (same inputs → same output) and has
**zero** store/HTTP side effects and **zero** collaborator calls, **sink** it
to a pure / unit helper.

```ts
// before — repository formats inline
class UserRepository {
  async create(data: UserInput) {
    const cleanEmail = data.email.trim().toLowerCase()
    return db.users.insert({ ...data, email: cleanEmail })
  }
}

// after — pure / unit owns the transform; service applies it; repo stays 1:1
export const normalizeEmail = (email: string) => email.trim().toLowerCase()

class UserService {
  async create(data: UserInput) {
    return this.users.create({ ...data, email: normalizeEmail(data.email) })
  }
}

class UserRepository {
  async create(data: UserInput) {
    return db.users.insert(data)
  }
}
```

### Lift → service / orchestration

**Trigger:** A repository or API/transport contains multi-step control flow,
preconditions across tables/services, or coordinates calls between components.

**Rule:** If the work sequences actions, decides execution flow, or combines
results from multiple sources, **lift** it into service / orchestration.

```ts
// ❌ BEFORE: OrderRepository executes SQL for the 'users' table & enforces business policy
class OrderRepository {
  async createOrder(userId: string, item: string) {
    // 🛑 LEAK 1: SQL query touching a DIFFERENT table ('users') inside OrderRepository
    const userResult = await db.query('SELECT is_blocked FROM users WHERE id = $1', [userId])
    
    // 🛑 LEAK 2: Business policy decision inside database layer
    if (userResult.rows[0]?.is_blocked) {
      throw new Error("Blocked user cannot place order")
    }

    // Actual order query
    return db.query('INSERT INTO orders (user_id, item) VALUES ($1, $2) RETURNING *', [userId, item])
  }
}

// ✅ AFTER: Each repository owns SQL for 1 table; Service lifts the workflow & business rule
class UserRepository {
  async findById(userId: string) {
    const res = await db.query('SELECT is_blocked FROM users WHERE id = $1', [userId])
    return res.rows[0]
  }
}

class OrderRepository {
  async insert(userId: string, item: string) {
    const res = await db.query('INSERT INTO orders (user_id, item) VALUES ($1, $2) RETURNING *', [userId, item])
    return res.rows[0]
  }
}

class OrderService {
  constructor(private userRepo: UserRepository, private orderRepo: OrderRepository) {}

  async createOrder(userId: string, item: string) {
    const user = await this.userRepo.findById(userId)
    if (user?.is_blocked) throw new Error("Blocked user cannot place order") // Business rule lifted here
    return this.orderRepo.insert(userId, item)
  }
}
```

## Take vs skip

### Take (dead code / test-only production surface)

Zero actual callers across the repo. Example report:

`Pass 1: took [dead formatId]. skipped [].`

### Take (flatten forwarders / KISS)

Middle hop that only forwards arguments with zero behavior. Do **not** make
API / transport call data / repository directly — keep SRP layers; delete the
empty middle hop only.

```ts
// before — OrderGateway only forwards
class OrderGateway {
  findById(id: string) { return this.orders.findById(id) }
}
class OrderService {
  get(id: string) { return this.gateway.findById(id) }
}

// after — service calls repository; dead pure-forwarder gateway gone
class OrderService {
  get(id: string) { return this.orders.findById(id) }
}
```

`Pass 1: took [flatten OrderService→OrderRepository; dead OrderGateway]. skipped [].`

### Take (Sink & Lift Rule)

Leaked mapping/formatting/orchestration — apply **Sink & Lift Rule** (complete
before/after there). Example report:

`Pass 1: took [sink email normalization to pure normalizeEmail]. skipped [].`

### Skip (do not take)

```ts
// skip — forwarder owns behavior (auth, validation, retries, …)
async getUser(id: string) {
  await this.auth.checkPermissions(id)
  return this.userRepo.findById(id)
}

// skip — intentional testkit / supported test utility
export function createTestDatabase() { /* … */ }

// skip — rename churn with no size/behavior win
const userRecord = await db.get(id) // renaming to `user` alone = aesthetic
```

```
Pass 1: took []. skipped [ambiguous: getUser auth check — not a pure forwarder].
Pass 1: took []. skipped [ambiguous: createTestDatabase — supported testkit].
Pass 1: took []. skipped [rename churn].
Pass 1: took [dead formatId]. skipped [failed verification: typecheck — inline fetchUser].
```

## Output

Every pass: exactly one numbered line. No essays. No silent passes.

Pattern: `Pass N: took […]. skipped […].`

Tag skips when useful: plain gate skip, `ambiguous: …`, `failed verification: …`.

After empty / cap ask / decline: emit `Leftover ambiguous: […]; […].` if the
list is non-empty (omit if empty). Keep the list across yes-batches.

```
Pass 1: took [dead formatId]. skipped [rename churn, ambiguous: ErrorCode map — might be public API].
Pass 2: took [inline fetchUser]. skipped [].
Pass 3: nothing worth taking. Crucible done.
Leftover ambiguous: [ErrorCode map — might be public API].
```

Cap ask form: `Pass 10: took […]. skipped […]. Cap reached. Continue for another 10 passes?`

## Boundaries

Governs deletes/simplifies in the edit set, not how you talk.

If the /ponytail skill is available, use its ladder for take vs skip,
merged with Crucible's Sink & Lift Rule (since ponytail does not include
Sink & Lift). Crucible retains ownership of the repeat-until-clean loop. No
/ponytail? The gate is enough.

If the /loop skill is available, use it only to wake the next pass when the
turn must yield mid-batch (see Batching & done when). No /loop? Ask the
user to continue — do not fake a wake.
