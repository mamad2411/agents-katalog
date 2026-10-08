# Genex models at play time in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's card on calling a
model from a running game, unchanged. Where it disagrees with this preface, this preface wins.

## Commands, as Studio tools

- `npx genex llm models`, `llm status` and `llm cancel <id>`: `genex__cli`, for example
  `genex__cli {"command":"llm models","options":{"all":true}}` or
  `genex__cli {"command":"llm cancel","args":"<id>"}`.
- `npx genex llm bench "<prompt>" --samples 3 --max-coins <n>`: `genex__cli-paid`, with the
  prompt in `args` and whole-number flags in `options`:
  `{"command":"llm bench","args":"<prompt>","options":{"samples":3,"max-coins":5}}`. The user
  approves each bench because it spends their coin; Studio adds the approval flag itself, so never
  pass `user-approved`.
- The CLI runs in a folder of Studio's own, not the game, so a flag that names a game file (such as
  `--schema ./answer.schema.json`) cannot be read. `llm price` is not available.
- Project commands (`llm bench`, `llm status`, `llm cancel`) need the game's hosted project:
  publish a draft with `genex__publish {"operation":"draft"}` first. `init --convert` does not
  apply in Studio.

## Reading the reference

Read the pricing reference with
`genex__skill {"name":"genex-llm-in-games","file":"skills/genex-llm-in-games/references/pricing.md"}`.

Other commands map onto Studio tools as the `genex` skill describes (`genex__skill {"name":"genex"}`).

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-llm-in-games/SKILL.md v1.35.0 sha256 08b998c09b88a188a9bfe055fa4e3c904bd1ba4fcb20e7700a4b6204e27540b9 -->
---
name: genex-llm-in-games
description: Call a language model from inside a running game — an NPC that answers in its own words, a quest written for this save, a judge that reads what the player typed. The PLAYER pays and approves, on a Genex surface the game cannot forge. Covers the two modes (a popup per call, or one standing budget then many silent calls), benchmarking the price before declaring it, the receiver pattern, and honest handling of every refusal.
---

# Genex LLM in Games

A Genex game can call a language model **while the player is playing** and get
back text or JSON. Nothing else: no images, no code execution, no tools.

**The player pays, and the player approves.** Funding is coin from their Genex
wallet or their own Claude / ChatGPT plan, chosen on a Genex-drawn surface your
game cannot render, skin or bypass. The game holds no provider key, sees no
credential, and never talks to a model vendor.

Two modes. Picking the wrong one is the most expensive mistake on this lane:

| | One-time | Standing budget |
| --- | --- | --- |
| Shape | `generate()` — one approval popup per call | `requestSpendGrant()` once, then `generate({ grantId })` many times, no popup |
| Fits | a rare, deliberate moment the player asked for | a loop — NPCs thinking, a director reacting, anything per-wave or per-minute |
| Ends | when that call settles | at the player's limit, a Stop, or 24h |
| Gesture | must run inside a click handler | none needed once the grant is active |

A popup per NPC turn is not a feature, it is an interruption. More than a call
or two per session means a grant.

## Step 0 — is the lane live on this stand?

```bash
npx genex llm models
```

- **live** — it prints the FEATURED models this stand serves, and how many more
  there are. Build the feature.
- **off on this stand** — the routes answer 404. Build the feature behind a
  graceful `unavailable` state (the NPC uses its authored lines, the quest falls
  back to the written one) and **say so plainly in the handoff**. Never promise
  the player something that 404s.
- **misconfigured** — say that too; it is an operator fix, not a game bug.

The stand's catalog is synced and filtered, so it can hold far more rows than
anyone wants to read. **Offer the featured set. Run `npx genex llm models --all`
only when the user asks for more**, and put the full list in front of them
rather than picking an obscure row for them.

Model ids come from that command and from `getGenerationModels()` at runtime.
Never write one into the game's source: they differ per stand, and a hardcoded
id is a feature that dies on somebody else's environment. **A picker's label
must be the model's own `label`** — a name you invent for a row ("Fast", "Smart")
is a label that differs from the model the player is billed for.

## The SDK surface (exact — do not invent methods)

From `@genex-ai/embed-sdk`, already installed. `initEmbed()` must have run and
identity must be resolved first — `$genex-threejs-embed-auth`.

- `getGenerationModels()` — `{ models, featuredCount, … }`, featured first. Any
  picker renders from this, never from a list you wrote: show the rows where
  `featured` is true (or all of them when `featuredCount` is 0) and offer the
  rest only if the player asks. Each row carries `label`, `vendor`,
  `contextLength`, `personalPlan` and `structuredOutputs`; render `label`
  verbatim, so the name on screen is the model that gets billed.
- `generate({ modelId, prompt, outputFormat, schema?, estimateCoins,
  allowExternal?, idempotencyKey?, grantId?, timeoutMs? })` →
  `{ status, generationId, output, source, error }` plus billing fields
  (`billingStatus`, `reservedCoins`, `chargedCoins`, their display-USD twins).
- `requestSpendGrant({ models, perCallMaxCoins, perCallEstimateCoins,
  disclosure: { periodLabel, estimatedCallsPerPeriod, estimatedCoinsPerPeriod },
  maxConcurrent?, maxCallsPerMinute?, allowExternal?, idempotencyKey? })` →
  `{ status, grantId, … the limits the player approved }`; status is `active` |
  `canceled` | `expired` | `failed` | `pending`.
- `getSpendGrant(grantId)` — live state and counters; the ONE source for an
  in-game budget readout.
- `stopSpendGrant(grantId)` — the game's own stop door. Prospective: no further
  calls are admitted, anything in flight drains and settles.
- `waitForGeneration(id)` / `getGeneration(id)` — re-attach to a call already
  started, including after a reload.
- `generationErrorMessage(code)` — one player-facing sentence for an error code.

```ts
askButton.addEventListener('click', async () => {   // a real click
  const res = await generate({                      // FIRST statement, no await before it
    modelId, outputFormat: 'json', schema: ANSWER_SCHEMA,
    prompt: askPrompt(npc, playerLine),
    estimateCoins: NPC_CALL_PRICE,                  // benchmarked — see below
    idempotencyKey: `npc:${npc.id}:${turnId}`,
  });
  applyGeneration(res);                             // the one writer — see below
});
```

**`generate()` and `requestSpendGrant()` are the first statement of the click
handler, before any `await`.** The approval popup is reserved synchronously off
the gesture; an `await` in front of it loses the gesture and nothing opens.
`generate({ grantId })` needs no gesture at all — that is what a grant buys.

## `estimateCoins` is a price, not an estimate

You declare it; the platform charges it. Declare 5 and 5 is charged — on a
success, a failure, a cancel, and when the model stops at its budget. Only an
attempt with no model work at all costs nothing. A number picked by feel is
money taken from your players for nothing, or a call that cannot fund itself.

**Benchmark, then declare:**

```bash
npx genex llm bench "<the real prompt, with a real example filled in>" \
  --schema ./answer.schema.json --samples 3 --max-coins <n> --user-approved
```

It runs on **your own coins**, on the development lane, and prints what each
sample actually charged plus the recommendation to declare: p95 of the charged
coins with the server's own recommended headroom already applied. Declare that
printed number. Never guess it, never work it out from a vendor's price list,
never add a margin of your own. For a standing budget the run prints a second
line, `Grant perCallMaxCoins`, and that one is `perCallMaxCoins` — declare it
verbatim as well rather than deriving a ceiling from `max`, which lands under
the price and makes `requestSpendGrant()` refuse before it reaches the network. Full procedure — reading p50/p95, turning the
loop into disclosure numbers, re-benchmarking after a prompt change — is in
[references/pricing.md](references/pricing.md).

**The declared price also decides how long the answer may be.** Each call's
room to answer is funded from the price it declares, so a price that covers
what an answer cost can still cut it off. The bench's recommendation already
leaves that room — always declare what it prints, never the bare charged
number. A sample cut off at your `--max-coins` is not a sample: re-run with a
higher one. When the bench says the answer is longer than one call on this
stand may produce, ask for a shorter answer.

Only samples that **succeeded and settled** are priced from. A sample the
provider refused at its door (`provider_http_<status>`) ran no inference and
cost nothing; the bench prints the code, the provider's own message and, for a
401 or 403, that this is the stand's provider configuration refusing the model
— an operator's problem, never something to fix in the game. A sample refused
as `generation_limit` never started: you already have the lane's three ad-hoc
calls open, or recently stopped with their bill still pending. The bench says
how many slots are held and stops. Do not re-run it into the same refusal —
read `npx genex llm status`, then wait for a bill to resolve or
`npx genex llm cancel <id>` an active call.

```bash
npx genex llm status        # this project's open calls: active, or awaiting their bill; N of 3 slots held
npx genex llm cancel <id>   # stop an ACTIVE call; a stopped one is reported, not cancelled
```

## The schema dialect (exact — anything else is refused)

`schema` is validated by the platform before the call, and a refused schema is
`invalid_schema` at the door — nothing is charged, nothing runs. The accepted
subset, and it is the whole subset:

- `type`: `object`, `array`, `string`, `number`, `integer`, `boolean`, `null`
- objects: `properties`, `required`, and `additionalProperties: false` on
  **every** object (required, not optional)
- arrays: `items`
- `enum` (strings, numbers, booleans, `null`)
- `minimum` / `maximum`, `minLength` / `maxLength`, `minItems` / `maxItems`
- `description` and `title`, on any node

Everything else is refused, including `$schema`, `default`, `examples`,
`pattern`, `format`, `anyOf` / `oneOf` / `allOf` and `$ref`. Keep the schema
in one file (`./answer.schema.json`), benchmark with that file, and ship the
same object — a schema that passed the bench passes the game.

## Standing budgets

```ts
const grant = await requestSpendGrant({          // inside the click handler
  models: [modelId],
  perCallMaxCoins: NPC_CALL_CEILING,
  perCallEstimateCoins: NPC_CALL_PRICE,
  disclosure: {
    periodLabel: 'minute',
    estimatedCallsPerPeriod: 10,                 // 5 NPCs, one decision each per 30s
    estimatedCoinsPerPeriod: 10 * NPC_CALL_PRICE,
  },
  maxConcurrent: 2,
  maxCallsPerMinute: 30,
});
if (grant.status !== 'active') { runWithAuthoredLines(); return; }
await savePlayerState({ ...state, grantId: grant.grantId });
```

**The disclosure is computed from this game's own loop, never wished for.** Five
NPCs deciding once every thirty seconds is ten calls a minute — write that
arithmetic into `DESIGN.md` beside the feature. The player sees your estimate
attributed to the game, beside the platform's own worst case; an estimate that
is transparently low is a grant that dies mid-session.

**Then keep the burn low, because you wrote the loop:** batch those five NPCs
into ONE call returning five decisions, cache a decision until the situation
that caused it changes, pick the cheapest model that passes your own check, and
never fire on a timer the player cannot see.

Grant endings are ordinary game states with in-fiction copy, never an error toast:

| code | what happened | what the game does |
| --- | --- | --- |
| `grant_limit_reached` | the approved limit is spent | authored behaviour returns; a button offers to re-request |
| `grant_stopped` | the player pressed Stop | accept silently, keep playing |
| `grant_expired` | 24h passed, or the session ended | as stopped; re-request on the next deliberate click |
| `waiting_for_plan` | their own plan is rate-limited | wait out the stated time — not a failure, and there is no paid fallback |
| `grant_insufficient_funds` | the wallet cannot fund the next call | pause the thinking NPCs, say it once, stay playable |

Draw the readout from `getSpendGrant(grantId)` — calls made, coins settled, what
remains — never from a counter the game keeps itself. A finished grant may be
re-requested, but only from a **fresh deliberate click**: a silent auto-renew is
the exact shape a standing approval exists to prevent.

## The receiver pattern — one writer, two entry points

A generation outlives the frame that asked for it; reloads and closed tabs land
in the middle of one.

```ts
function applyGeneration(res) {     // THE only place output becomes game state
  if (res.status !== 'succeeded') return showLine(generationErrorMessage(res.error));
  const parsed = ANSWER.safeParse(res.output);   // validated against YOUR expectation
  if (!parsed.success) return showLine("The voice trails off.");
  speak(parsed.data.line);
  savePlayerState({ ...state, pendingGenerationId: null });
}
```

- The click path writes `generationId` into player state **before** awaiting.
- Boot reads any stored id, calls `waitForGeneration(savedId)`, and passes the
  result to the **same** `applyGeneration`. One writer, two entry points, is the
  difference between "works once" and "survives a reload".
- Output is **data, never authority**: it may not grant coin, items,
  entitlements, scores or progression by saying so. `source: 'external'` carries
  `modelProvenance: 'unverified'` because it is user-supplied — check it exactly
  as you would check typed player input.

## Errors land on the player's wallet

There is no compensation lane, so this is all work you do before the call:

- **Validate inputs first** — a malformed prompt is still charged.
- **Always set `schema` for `outputFormat: 'json'`** — unschema'd JSON is the
  commonest way a call is charged and the result is unusable. Write it in the
  accepted dialect above; a refused schema is `invalid_schema` and costs
  nothing, but it is a feature that never runs.
- **Keep prompts short.** Long context is the price.
- **Never loop `generate()` without a grant**, and never retry in a loop — each
  attempt is a separate charge.
- **Map every code through `generationErrorMessage(code)`** into in-fiction
  copy. A player should never read a raw error code inside your game.
- **`status: 'unknown'` is not a failure.** It means the charge is not known
  yet, billing pending. Say "still settling", keep the reserved figure in the
  readout, re-read with `getGeneration(id)` — never call it failed, never retry.

## What the Genex side already does — do not rebuild it

The approval sheet shows the model, the prompt, the price and the terms; the
game renders no price sheet. **Subscription funding is chosen only there** —
never add a "Your plan" row to the game's model picker, because a game cannot
offer a funding source. When the player's own watcher is online the personal-plan
answer arrives by itself and the game just waits, exactly as it waits for a
coin-funded call. The Genex dashboard header shows progress, active grants with
their spend, and a Stop; a Stop pressed there reaches the game as `grant_stopped`.

## Never

- **Never execute returned output** — no `eval`, no dynamic import, no scene
  graph or shader built from model text, no URL fetched because the output said so.
- **Never bundle a creator credential in a game.** Benchmarking is a CLI action
  on your machine, never something a shipped build does.
- **Never hand-roll fetch to the runtime API** — the SDK owns the approval
  handshake, and a hand-rolled call cannot obtain one.
- **Never hardcode a price, a model id, a stand URL, or a margin.**
- **Never let the model be an authority over money, items or rewards**
  (`$genex-monetization` owns what may move a wallet).

These are source contracts, not a claim that every stand runs this lane —
`npx genex llm models` is what tells you.

## Checklist

- [ ] `npx genex llm models` was run and its verdict is in the handoff
- [ ] Model ids come from `getGenerationModels()`, never from source
- [ ] The picker offers the featured set, labelled with the server's own `label`
- [ ] `estimateCoins` is the figure `npx genex llm bench` printed, verbatim — never the bare charged number
- [ ] The schema uses only the accepted dialect (no `$ref`, `pattern`, `format`, `anyOf`, `default`)
- [ ] A bench refused as `generation_limit` was answered with `npx genex llm status`, never a retry
- [ ] `generate()` / `requestSpendGrant()` is the first statement of a click handler
- [ ] A repeated-call feature uses a grant; a one-off uses `generate()`
- [ ] Disclosure numbers derive from the real loop and are written in `DESIGN.md`
- [ ] Calls are batched and cached; nothing fires on an invisible timer
- [ ] Every grant-ending code has in-fiction copy and a playable fallback
- [ ] The in-game readout comes from `getSpendGrant()`
- [ ] Exactly one `applyGeneration()` writer; boot re-attaches with `waitForGeneration()`
- [ ] `generationId` is saved BEFORE the await
- [ ] Output is schema-validated and grants nothing by itself
- [ ] `unknown` reads as "still settling", never as a failure
- [ ] The game renders no price sheet and no funding picker

## Troubleshooting

**Everything on this lane 404s** — runtime generation is off on this stand.
Nothing to fix in the game: ship the fallback and say so.

**Nothing opens when the player clicks** — an `await` ran before `generate()`
and the gesture was lost. Move the call to the first line of the handler.

**`player_wallet_required`** — ONE code for the two early dead ends: the lane
refuses a guest and a PREVIEW build on the same line. `waitForPlayer()` tells
them apart. `guest: true` — guests play but hold no wallet, so show the feature
as sign-in-to-use rather than hiding it (`$genex-threejs-embed-auth`). Signed
in and still refused — this is a `genex preview` draft, which never spends:
check the layout there, and the call itself only after `genex promote`. The
SDK's stock sentence for this code is "Sign in to Genex to use this", which is
right for the guest and wrong on a draft, so write the in-fiction line per
cause rather than showing it for both.

**`grant_price_unreasonable`** — the declared per-call price is far above what
that prompt can cost on that model. Re-benchmark and declare what it prints.

**`generation_limit`** — three ad-hoc calls are already in flight for this
account, or recently stopped with their bill still pending; a pending call
stops counting ten minutes after it was dispatched. From the bench: run
`npx genex llm status`, then wait or `npx genex llm cancel <id>` an active one —
never re-run into the same refusal. In the game: the player is clicking faster
than one-off calls are meant for, which is the signal that this feature wants a
grant.

**`provider_http_<status>`** — the provider refused the call at its door, before
any inference: it cost nothing and is not a sample. Read the provider's own
message (`npx genex llm status` prints it under the row). A 401 or 403 is this
stand's provider configuration refusing the model — tell the operator, and
build nothing around it in the game.

**`provider_token_limit`** — the answer was cut off: the model ran out of room
before it finished, and the attempt is still charged. The declared price is too
low for the answer's length — re-benchmark and declare what the bench prints,
never the bare charged number — or the answer is longer than one call on this
stand may produce, and the fix is a shorter answer (fewer fields, shorter
strings, a length the prompt states).

**`invalid_schema`** — the schema uses a keyword outside the accepted dialect
(`$ref`, `pattern`, `format`, `anyOf`, `default`, `examples`, `$schema`), or an
object without `additionalProperties: false`. Nothing was charged. Rewrite it in
the subset above; `description` and `title` are allowed.

**`grant_concurrency` / `grant_rate_limited`** — the game calls faster than the
grant's own limits. Batch and cache; do not raise the limits to hide it.

**`grant_not_active`** — the saved `grantId` is finished. Clear the stored id
and re-request from a fresh click.

**`external_request_active`** — that player already has one personal-plan
request running. Wait for it; never fall back to charging coin instead.

**The call is charged but the result is unusable** — `outputFormat: 'json'`
without a `schema`. Add one; the charge already happened.

**A reload lost the answer** — `generationId` was not saved before the await, or
boot never calls `waitForGeneration()`. Both halves are required.

**The in-game readout disagrees with the Genex header** — the game is counting
calls itself. Read `getSpendGrant()` instead.
