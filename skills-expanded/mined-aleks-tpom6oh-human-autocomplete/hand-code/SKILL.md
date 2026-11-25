---
name: hand-code
description: Hands the user one real, well-specified piece of production code to write by hand, LeetCode-style (signature, inputs/outputs, examples, failing tests) but for a function the current task actually needs, then keeps working and writes it itself if the user doesn't pick it up within ~20 minutes. Rate-limited across every Claude Code session on the machine (one request at a time, at most one per hour). Use proactively during implementation whenever a "hand-code: a slot is open" note is in context and you are about to write a self-contained function with real logic. Also use when the user asks for something to write themselves ("give me something to code", "let me write this one", "hand-code", "kata", "I want to write this part by hand").
---

# Hand-code

The user likes writing code by hand, and running many agents in parallel means they rarely get to. This skill gives them back a small, steady trickle of it: now and then, instead of writing a function yourself, you set it up as a crisp problem in the real codebase and hand it over. Their attention is the scarce resource, so one well-chosen problem an hour beats many mediocre ones, and the work must never stall waiting on them.

A machine-wide coordinator enforces the limits so parallel sessions don't pile on. It is `scripts/handcode` inside this skill's base directory, which is shown above when the skill loads:

```bash
HC=<this skill's base directory>/scripts/handcode
```

Bash calls don't share variables, so spell the full path out in each command. Every agent-facing command prints JSON.

## Quick exits

Most invocations should end here, silently, without mentioning the skill to the user:

- You are a subagent, a workflow step, or running headless: nobody is there to write code. Skip.
- The code lives somewhere the user can't open locally (cloud or remote session). Skip.
- `$HC check` says `"open": false`. Skip; the limit is doing its job.
- Nothing in the current task fits the bar below. Skip. No request is far better than a dull one.

If the slot was open and you had a specific candidate in mind but passed on it, leave a one-line note so the user can see why nothing reached them and tune this skill: `$HC decline --title "mapWithConcurrency" --reason "<why>"`.

When the user explicitly asks for something to write, the cooldown doesn't apply: use `claim --force` (it still refuses if another request is in flight).

## What makes a good request

Pick something the task needs right now, that you would otherwise write in the next few minutes. It should feel like a good interview problem that happens to ship:

- **Clear contract.** Inputs and outputs fit in a typed signature plus three or four examples. Ideally pure, or with side effects pushed to the edges (inject `now`, pass data in, return data out).
- **Real logic.** Parsing, normalising, validating, diffing or merging, state transitions, retry and backoff, pagination, batching, scheduling, ranking, a reducer, a gnarly query. Something with edge cases worth thinking about.
- **Right size.** Roughly 10–60 lines, 15–40 minutes for a strong engineer.
- **Little context needed.** Five lines of "why this exists and who calls it" should be enough. If they'd need to read ten files first, it's the wrong pick.
- **Something you can build around.** A function the next step calls is fine: write the callers against the stub's signature and keep going while they work on it. Pass only when you'd have nothing useful to do until it's filled in.

Skip: glue and wiring, config, migrations, renames, types-only changes, generated code, UI layout and styling, security-critical code (auth, crypto, permission checks), and invented algorithm puzzles. `check` lists recent titles; avoid handing over the same kind of problem twice in a row.

Good: `parseRetryAfter(header, now)` (two header formats, clamping), `diffSchemas(before, after)` returning added/removed/changed, `nextRunAt(schedule, after, tz)`, a batching queue that flushes on size or age, a reducer for a four-state upload flow.
Bad: "add the route for the new endpoint", "rename `userId` to `accountId`", "write the TypeScript types for this payload", "implement binary search".

## Flow

### 1. Claim

```bash
$HC claim --title "parseRetryAfter: Retry-After header → delay"
```

Not `ok`? Carry on normally. `ok` gives you an `id` (like `hc-7f3a`) and its marker `HAND-CODE(hc-7f3a)`. If you then decide the candidate doesn't work after all, `$HC release <id>` gives the slot back untouched.

### 2. Set up the problem in the codebase

- **Stub** with the real signature and types, and a body that fails loudly (`throw new Error("not implemented")`, `raise NotImplementedError`, `todo!()`, `failwith`). Wire call sites so the rest of the code compiles and you can keep working.
- **Brief** as the doc comment right above the stub, in the project's comment style, with the marker on its first line. This is where the user will be looking, so it is the problem statement. Keep it under ~25 lines:

  ```
  HAND-CODE(hc-7f3a) — your turn. Delete this line when you're done.

  parseRetryAfter: turn a Retry-After header into a delay in ms.

  Context: the webhook sender retries 429/503 responses. Called from
  sendWithRetry() (src/webhooks/sender.ts:88) with the raw header value.

  Input:
    header: string | undefined. Either delta-seconds ("120") or an HTTP-date.
    now: Date. Current time, injected for tests.
  Output:
    number | null. Delay in ms clamped to [0, 1h]; null if missing or unparseable.

  Examples:
    parseRetryAfter("120", now)                           → 120000
    parseRetryAfter("Wed, 21 Oct 2026 07:28:00 GMT", now) → ms until then, 0 if past
    parseRetryAfter("soon", now)                          → null

  Constraints: no new dependencies; never throws.
  Tests: src/webhooks/__tests__/retryAfter.test.ts · run: yarn jest retryAfter
  Estimate: ~20 min · medium
  ```

- **Tests** in the project's framework that pin the contract: the examples, plus the edge cases the brief promises. Run them. They should all fail with "not implemented" and nothing else; a test that fails for another reason, or a compile error, makes the problem unfair. If the project limits where tests may go (only through certain public entry points, say), pin the contract through a test the project does allow, or check the brief's examples with a scratch script. A testing rule is a reason to adapt the tests, not to skip the request.

### 3. Post and tell the user

```bash
$HC post <id> --file <absolute path> --symbol parseRetryAfter \
  --summary "Retry-After header → delay in ms" --test-cmd "yarn jest retryAfter" --estimate 20
```

This shows a pop-up with Take it / Skip / Later that stays on screen until answered (a plain notification instead where pop-ups are off); Take it opens the stub in their editor. If you have the PushNotification tool, send one line through it too (for example "✋ your turn: parseRetryAfter, ~20 min, 20 min to pick up"); it goes through the Claude app, so it still arrives when the script's notification is blocked, and reaches their phone when Remote Control is on. Then say it in chat, short and scannable, with the absolute path as a link (sessions often run in worktrees, so the path tells them which checkout):

> ✋ **Your turn:** `parseRetryAfter(header, now)` · ~20 min · medium
> [src/webhooks/retryAfter.ts:12](/abs/path/src/webhooks/retryAfter.ts:12) · tests: `yarn jest retryAfter` (7 red)
> Start editing within 20 min (or hit Take it on the pop-up) and it's yours; otherwise I'll write it. Delete the `HAND-CODE` line when you're done.
> Meanwhile I'm carrying on with the sender wiring.

### 4. Wait without blocking

Start `$HC wait <id>` with the Bash tool's `run_in_background`. It exits when the request resolves, and that wakes you up. Don't use AskUserQuestion here: it has no timeout and would freeze the session until they answer.

While it runs, keep doing the parts of the task that don't need the function. Leave the stub file alone: any change to it on disk counts as the user picking it up. Don't commit while the request is open either, or you'd capture their half-written code. If nothing else is left, end your turn with one line saying you're waiting.

If the user writes in chat meanwhile, map it: "on it" → `$HC accept`, "skip" / "you do it" → `$HC skip`, "done" → `$HC done`. Questions about the problem: answer them like an interviewer would (clarify the contract, give a hint if asked) without writing the code for them.

### 5. Handle the outcome

`wait` prints JSON with a `status`:

- **done**: run the tests.
  - **Pass**: remove the marker and turn the brief into a normal, concise doc comment that matches the codebase. Leave their code as written. Then give a short review, two to four concrete points, the way a good senior reviewer would: an edge case, a simpler idiom, a performance note, or plainly that it's solid. Suggest changes; don't make them. `$HC close <id> --result pass`.
  - **Fail, first time**: put the marker line back, run `$HC reopen <id> --reason "2/7 failing: HTTP-date in the past, empty string"`, tell them which cases fail and why in a sentence (a hint, not the fix), and wait again in the background. A test can be what's wrong: if their reading of the brief is reasonable and the test is too strict, fix the test, own it, and treat it as a pass.
  - **Fail after a reopen**, or the reopen expires: make the smallest fix yourself, show the diff of exactly what you changed, then `$HC close <id> --result fixed`.
- **expired** or **skipped**: write it yourself, clean up the marker and brief, `$HC close <id> --result agent`. One line to the user is plenty; no guilt-tripping.
- **abandoned**: they started but ran past the work window. Finish it on top of their code rather than replacing it, say so, `$HC close <id> --result fixed`.
- **lost** or **gone**: the file or the request disappeared. Close if you can and carry on.

## Commands the user can run

Mention these when they're useful, not every time (they may alias `hc` to the script):

| Command | Effect |
|---|---|
| `handcode status` | what's going on, time left |
| `handcode show` / `open` | print the brief / open the stub in the editor |
| `handcode accept` / `skip` / `done` | take it / pass / mark finished |
| `handcode test` | run the request's tests |
| `handcode extend 20` | 20 more minutes on the current window |
| `handcode pause 2h` / `off` / `on` | quiet for a while / until turned back on |
| `handcode reset` | clear the cooldown so a request can come right away |
| `handcode stats` | history |

Limits live in `~/.claude/hand-code/config.json` (`cooldown_min` 60, `accept_min` 20, `dialog` true, `work_min` 90, `editor`). The cooldown counts from when the previous request ended.
