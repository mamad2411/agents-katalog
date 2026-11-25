---
name: effects-as-values
description: "Refactor side-effecting TypeScript so that failure and I/O become values in the return type instead of thrown exceptions and hidden imports. Use this skill when a function throws and callers can't tell from the signature, when try/catch blocks are nested or swallow errors, when an error type is any or unknown by the time it reaches the UI, when validation stops at the first failure but the form needs every message, when a unit test can't run without stubbing fetch or mocking a module, when async work needs retry or cancellation or sequencing that promises make awkward, or when someone asks 'how do I test this without mocking', 'where should errors be handled', 'how do I return an error instead of throwing'. Provides a five-rung adoption ladder from a plain Result union up to injected interpreters, with explicit guidance on which rungs pay off in production TypeScript and which are concepts to learn from rather than build."
---

# Effects as Values

A function that **performs** an effect can't be composed, deferred, retried, reordered, or tested without the world it touches. A function that **returns a description** of the effect can be all of those things. That's the whole idea; everything below is how far up it's worth climbing.

Two symptoms say the boundary is in the wrong place:

- **A signature that lies.** `function save(u: User): Promise<User>` doesn't mention that it throws four different ways, so no caller handles them and none of them are typed.
- **A test that needs a world.** If verifying a calculation requires stubbing `fetch` or mocking a module, the calculation and the effect are in the same function.

## The ladder

Rungs 1–4 are production refactors. Rung 5 is a concept worth understanding and not worth building. Climb only as far as the problem requires — **most codebases should stop at 2 or 3.**

### 1. Put the failure in the return type

Zero dependencies, ordinary TypeScript, and this is where most of the value is.

```ts
export type Result<T, E = Error> =
    | { readonly ok: true; readonly value: T }
    | { readonly ok: false; readonly error: E };

export const ok = <T>(value: T): Result<T, never> => ({ ok: true, value });
export const err = <E>(error: E): Result<never, E> => ({ ok: false, error });
```

```ts
// BEFORE — the signature says nothing about the three failure modes
function parseConfig(raw: string): Config {
    const json = JSON.parse(raw);              // throws
    if (!json.version) throw new Error('missing version');
    return json as Config;
}

// AFTER — every failure is in the type, and the compiler forces a decision
type ConfigError = { kind: 'malformed'; detail: string } | { kind: 'missingVersion' };

function parseConfig(raw: string): Result<Config, ConfigError> {
    let json: unknown;
    try {
        json = JSON.parse(raw);
    } catch (e) {
        return err({ kind: 'malformed', detail: String(e) });
    }
    if (!isRecord(json) || !json.version) return err({ kind: 'missingVersion' });
    return ok(json as Config);
}
```

The discriminated union means `result.value` is only reachable after checking `result.ok`. A **closed** error union also means adding a failure mode breaks every incomplete `switch` at compile time — which is exactly the review you want.

Keep `try/catch` at the edges where a library throws, and convert immediately. Don't propagate exceptions through your own layers.

### 2. Defer the effect

An effect that hasn't run yet is just a function you haven't called:

```ts
export type IO<T> = () => T;                    // synchronous effect
export type Task<T> = () => Promise<T>;         // asynchronous effect
```

Deferral is what buys you retry, timeout, cancellation, ordering, and running the same description twice:

```ts
const fetchUser = (id: string): Task<Result<User, HttpError>> => () => http.get(`/users/${id}`);

const retry = <T>(attempts: number, task: Task<Result<T, HttpError>>): Task<Result<T, HttpError>> =>
    async () => {
        let last = await task();
        for (let i = 1; i < attempts && !last.ok; i++) last = await task();
        return last;
    };

// Nothing has happened yet — this is a description.
const plan = retry(3, fetchUser('42'));
const result = await plan();   // now it runs
```

A `Promise` is already running the moment you make one, so you cannot retry it — you can only retry the *function* that makes it. Naming that function `Task` makes the distinction explicit and stops "just await it" from creeping back in.

### 3. Accumulate failures instead of short-circuiting

`Result` short-circuits: the first error wins. For form validation that's the wrong answer — the user wants all six messages at once. Accumulation needs a different combine, and it's a monoid (see `algebraic-composition`):

```ts
type Validated<T> =
    | { readonly ok: true; readonly value: T }
    | { readonly ok: false; readonly errors: readonly string[] };

const both = <T>(a: Validated<T>, b: Validated<T>): Validated<T> =>
    a.ok ? b : b.ok ? a : { ok: false, errors: [...a.errors, ...b.errors] };
```

Rule of thumb: **sequential dependent steps short-circuit** (`Result` — step two needs step one's value); **independent checks accumulate** (`Validated` — every field is checked regardless).

### 4. Inject the effectful boundary

The practical way to make a whole workflow testable. Instead of importing the world, take it as a parameter:

```ts
// BEFORE — untestable without module mocks
import { db } from './db';
import { mailer } from './mailer';

export async function registerUser(input: Input) {
    const user = await db.users.insert(prepareUser(input));
    await mailer.send(welcome(user));
    return user;
}

// AFTER — the workflow is a pure function of its capabilities
export type Effects = {
    saveUser: (u: User) => Promise<Result<User, DbError>>;
    sendMail: (m: Mail) => Promise<Result<void, MailError>>;
    now: () => Date;
};

export const registerUser =
    (fx: Effects) =>
    async (input: Input): Promise<Result<User, DbError | MailError>> => {
        const saved = await fx.saveUser(prepareUser(input, fx.now()));
        if (!saved.ok) return saved;
        const sent = await fx.sendMail(welcome(saved.value));
        return sent.ok ? saved : sent;
    };
```

Production wires the real `Effects` once at the entry point. Tests pass a record of plain functions — no mock framework, no module interception, and a test can assert *which* effects were requested and in what order. Passing `now` in is what makes time-dependent logic deterministic.

This is the pragmatic form of the interpreter idea in rung 5, and in TypeScript it gets you nearly all of the benefit for a fraction of the machinery.

### 5. The program as data, run by an interpreter — learn it, don't build it

The full version describes the program as a **tree of instruction values** with no interpretation attached, then folds it with an interpreter. The same description can run against the real world, against a scripted test world, or be inspected and logged before running:

```ts
type Instruction =
    | { tag: 'Ask'; question: string }
    | { tag: 'Print'; text: string }
    | { tag: 'Save'; table: string; record: unknown };
```

The genuinely portable insight is **interpreter swapping**: one program description, several interpretations. That insight is fully realised by rung 4's `Effects` record, which is why rung 4 is where to stop.

Do **not** hand-roll a free monad, or a transformer stack like `ReaderT(EitherT(Task))`, in a production TypeScript app. TypeScript has no higher-kinded types, so the encoding needs pervasive casts, error messages become unreadable, and the next maintainer can't safely change it. If a codebase genuinely needs that much structure, adopt a library built for it — Effect, or fp-ts — as a deliberate, whole-codebase decision, not as a local refactor.

## Adoption in an existing codebase

- **Start at a leaf, not the entry point.** Convert one parser or validator to `Result`, let the call site unwrap it, and leave the rest alone. The pattern spreads outward from working code.
- **Convert at the boundary, immediately.** Wrap the throwing library call in `try/catch`, return a `Result`, and let nothing below the boundary throw.
- **Don't half-adopt a signature.** A function returning `Result` must not also throw. Callers will check one or the other, never both.
- **`unwrapOr` at the UI edge.** Somewhere the value has to become a rendered thing. That's the right place to collapse a `Result` — not three layers down.
- **Type the error union closed.** `Result<T, Error>` is barely better than throwing. `Result<T, NotFound | Forbidden | Malformed>` lets the compiler check the handling.

## Where to go next

- `references/result-and-task.md` — typed implementations of `Result`, `Task`, `Validated`, the combinators (`map`, `chain`, `mapErr`, `all`, `unwrapOr`), and conversions to and from throwing and promise-based code.
- `references/injected-effects.md` — the `Effects` record pattern end to end, test doubles that record calls, and a worked comparison against module mocking.
- Accumulating errors is a monoid — see `algebraic-composition`.
- Separating a pure core from an imperative shell in the first place is `functional-architecture`.

## When NOT to use it

- **Truly exceptional conditions.** Out of memory, a failed invariant, a bug. Those should crash; `Result` is for failures the caller is expected to handle.
- **A single call at the very edge.** One `try/catch` in a route handler is fine. Don't thread `Result` through four layers to reach it.
- **Framework-owned error paths.** Error boundaries, middleware, and validation pipelines already have a channel. Return `Result` from your logic and adapt at the seam — don't fight the framework.
- **Hot paths.** Every `Result` is an allocation. In a per-frame or per-row inner loop, use a sentinel or an out-parameter.
- **A codebase that already uses a library for this.** Use its `Either`/`Effect` type. Two competing result types is worse than either alone.
- **`unknown` errors you can't act on differently.** If every failure gets the same generic message, a boolean or `null` is honest and cheaper.
