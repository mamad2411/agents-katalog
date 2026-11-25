# Genex models at play time in AI Game Studio

You are building inside AI Game Studio. Below the upstream marker is Genex's card on calling a
model from a running game, with the passages of advice Studio does not ship taken out. Where it
disagrees with this preface, this preface wins.

## Commands, as Studio tools

- `npx genex llm models`, `llm status` and `llm cancel <id>`: `genex__cli`, for example
  `genex__cli {"command":"llm models","options":{"all":true}}` or
  `genex__cli {"command":"llm cancel","args":"<id>"}`.
- `npx genex llm bench "<prompt>" --samples 3 --max-coins <n>`: `genex__cli-paid`, with the
  prompt in `args` and whole-number flags in `options`:
  `{"command":"llm bench","args":"<prompt>","options":{"samples":3,"max-coins":5}}`. The user
  approves each bench because it spends their Nex (the flag keeps its old name); Studio adds the approval flag itself, so never
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

<!-- upstream @genex-ai/cli-demo/templates/skills/genex-llm-in-games/SKILL.md v1.40.0 sha256 5049cd58a6cd1ceb43ceef71fd583fe7efa31a2030c0d2a3f41473ed8aed30d8 -->
---
name: genex-llm-in-games
description: Call a language model from inside a running game — an NPC that answers in its own words, a quest written for this save, a judge that reads what the player typed. The PLAYER pays and approves, on a Genex surface the game cannot forge. Covers the two modes (a popup per call, or one standing budget then many silent calls), benchmarking the per-call ceiling before declaring it, the receiver pattern, and honest handling of every refusal.
---

# Genex LLM in Games

A Genex game can call a language model **while the player is playing** and get
back text or JSON. Nothing else: no images, no code execution, no tools.

**The player pays, and the player approves.** Funding is their Genex credits —
billed as used, never past the per-call ceiling your game declares — or their
own Claude / ChatGPT plan, chosen on a Genex-drawn surface your game cannot
render, skin or bypass. The game holds no provider key, sees no credential, and
never talks to a model vendor.

Two modes. Picking the wrong one is the most expensive mistake on this lane:

| | One-time | Standing budget |
| --- | --- | --- |
| Shape | `generate()` — one approval popup per call | `requestSpendGrant()` once, then `generate({ grantId })` many times, no popup |
| Fits | a rare, deliberate moment the player asked for | a loop — NPCs thinking, a director reacting, anything per-wave or per-minute |
| Ends | when that call settles | at the player's limit, a Stop, or 24h |
| Gesture | must run inside a click handler | none needed once the grant is active |

A popup per NPC turn is not a feature, it is an interruption. More than a call
or two per session means a grant.

**Deciding, not writing? Use the judge.** When the game needs to KNOW something
— is this NPC lying, which of five moods is the player in, how threatening is
the scene on a scale — and not to produce words, ask the grant's classifier with
`judge()` instead of asking `generate()` for a label. It answers typed questions
(`choice`, `score`, `noul`) with calibrated probabilities in about a third of a
second, writes no prose and cannot drift out of your options. It is grant-only
and billed as used: each call is a small fraction of a credit and accrues on the
budget, so a check every turn is affordable where a generate every turn is not.
`generate()` for words, `judge()` for decisions; a feature often wants both —
the judge picks the branch, generate writes the line.

**Words the player watches appear? Stream them.** Dialogue, narration, an NPC's
reply in a speech bubble: under a grant, `generateStream()` is the same call as
`generate({ grantId })`, but the text arrives while the model writes it instead
of all at once after it. Keep `generate()` for answers the game only uses whole
(a quest object, a list of decisions) — nobody watches those being written.

## Step 0 — is the lane live on this stand?

```bash
npx genex llm models
```

- **live** — it prints the FEATURED models this stand serves, and how many more
  there are.
- **off on this stand** — the routes answer 404.
- **misconfigured** — an operator fix, not a game bug.

The stand's catalog is synced and filtered, so it can hold far more rows than
anyone wants to read. `npx genex llm models --all` lists every
row.

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
- `generate({ modelId, prompt, outputFormat, schema?, maxCredits,
  allowExternal?, idempotencyKey?, grantId?, timeoutMs? })` →
  `{ status, generationId, output, source, error }` plus billing fields
  (`billingStatus`, `maxCredits`, `reservedCredits`, `chargedCredits`, their
  display-USD twins). `maxCredits` is the call's CEILING, never a price.
- `requestSpendGrant({ models, perCallMaxCredits, perCallEstimateCredits?,
  disclosure: { periodLabel, estimatedCallsPerPeriod, estimatedCreditsPerPeriod },
  maxConcurrent?, maxCallsPerMinute?, allowExternal?, judge?: { enabled,
  estimatedCallsPerPeriod }, idempotencyKey? })` →
  `{ status, grantId, … the limits the player approved }`; status is `active` |
  `canceled` | `expired` | `failed` | `pending`. `perCallEstimateCredits` is the
  honest per-call figure the disclosure is built on; left out, it is the
  ceiling.
- `judge({ grantId, state, questions, idempotencyKey?, timeoutMs? })` →
  `{ status, generationId, answers, error, billing }` — the grant's classifier,
  answered in the same response. `questions` is 1–64 named `choice`
  (`{ instructions, criteria: { option: description } }`), `score`
  (`{ instructions, criteria: [levels, lowest first] }`) or `noul`
  (`{ instructions }`); each answer has its question's type, and `noul` is a
  probability — pick your own threshold. Needs a budget requested with `judge`.
- `generateStream({ …the generate() options, grantId, onDelta?(text, soFar),
  onPartialField?(name, partialText), signal? })` → the same result as
  `generate()`. Grant-only. `onDelta` hands over each piece and all the text so
  far; for `outputFormat: 'json'`, `onPartialField` reports the schema's FIRST
  top-level string property as far as it is written — put the spoken line first
  in the schema. `signal` stops the reading, never the call (it still finishes
  and is charged).
- `getSpendGrant(grantId)` — live state and counters; the ONE source for an
  in-game budget readout.
- `stopSpendGrant(grantId)` — the game's own stop door. Prospective: no further
  calls are admitted, anything in flight drains and settles.
- `waitForGeneration(id)` / `getGeneration(id)` — re-attach to a call already
  started, including after a reload.
- `generationErrorMessage(code)` — one player-facing sentence for an error code.
- `requestWorkflow(…)` — a registered workflow's own door, unchanged: keep
  sending what that workflow's offerings ask for.

The credit names arrived in `@genex-ai/embed-sdk` 0.27.0. On `generate()`,
`generateStream()` and `requestSpendGrant()` the coin spellings —
`estimateCoins`, `perCallMaxCoins`, `perCallEstimateCoins` and
`disclosure.estimatedCoinsPerPeriod` — are deprecated: still accepted, and read
as the same numbers in credits. Write the credit names in anything new, and
rename them when you touch old code.

```ts
askButton.addEventListener('click', async () => {   // a real click
  const res = await generate({                      // FIRST statement, no await before it
    modelId, outputFormat: 'json', schema: ANSWER_SCHEMA,
    prompt: askPrompt(npc, playerLine),
    maxCredits: NPC_CALL_MAX,                       // benchmarked — see below
    idempotencyKey: `npc:${npc.id}:${turnId}`,
  });
  applyGeneration(res);                             // the one writer — see below
});
```

**`generate()` and `requestSpendGrant()` are the first statement of the click
handler, before any `await`.** The approval popup is reserved synchronously off
the gesture; an `await` in front of it loses the gesture and nothing opens.
`generate({ grantId })` needs no gesture at all — that is what a grant buys.

**Two shells have no approval surface, and say so before anything is asked or
charged.** Inside the Genex app every call on this lane resolves
`{ status: 'failed', error: 'native_unsupported' }`; on a dev server in local
test mode it is `local_test_unsupported`. Neither is a fault in the game. `getShell()`
from `@genex-ai/embed-sdk` names the shell. Which
shell draws what is in `$genex-threejs-embed-auth` (`references/shells.md`).

## `maxCredits` is a ceiling, not a price

The player is billed **as used**: the call's real provider cost plus the
platform fee, in credits. A one-time call is captured rounded UP to a whole
credit when it settles; a call under a budget adds its exact fraction to the
budget, and the player's credits move one whole credit at a time. A failed or
canceled attempt is billed the work the model did; one with no model work at
all costs nothing.

So the game declares no price. It declares a per-call **ceiling** — `maxCredits`
on `generate()`, `perCallMaxCredits` on a budget — and no call is ever billed
past it. The ceiling has a second job: **it also decides how long the answer
may be**, because each call's room to answer is funded from it. A number picked
by feel either cuts answers off or asks the player to approve far more than a
call ever costs.

**Benchmark, then declare:**

```bash
npx genex llm bench "<the real prompt, with a real example filled in>" \
  --schema ./answer.schema.json --samples 3 --max-credits <n> --user-approved
```

It runs on **your own credits**, on the development lane, and prints what each
sample really cost and was charged, then the numbers to declare:

- `Declare maxCredits` — the p95 real cost with the platform fee and the
  server's own recommended headroom applied, never below the room the answer's
  length needs. That is `maxCredits` on every call of this prompt.
- `Grant perCallMaxCredits` — the same over the worst sample. That is a
  budget's `perCallMaxCredits`; declare it verbatim rather than deriving a
  ceiling from the charged `max`, which carries neither the headroom nor the
  answer's length and gets the budget's calls refused.
- `Per-call estimate: about … credits per call` and
  `Grant perCallEstimateCredits` — the measured average, fee included, and that
  average rounded up to a whole credit: the honest figures a budget's disclosure
  is built on.

Declare the printed numbers. Never guess them, never work them out from a
vendor's price list, never add a margin of your own. Full procedure — reading
p50/p95, turning the loop into disclosure numbers, re-benchmarking after a
prompt change — is in [references/pricing.md](references/pricing.md).

A sample cut off at your `--max-credits` is not a sample: re-run with a higher
one. When the bench says the answer is longer than one call on this stand may
produce, ask for a shorter answer. `--max-coins` is the old name of
`--max-credits` and still works, with a line saying so.

Only samples that **succeeded and settled** are measured. A sample the
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
  perCallMaxCredits: NPC_GRANT_MAX,              // the bench's "Grant perCallMaxCredits"
  perCallEstimateCredits: NPC_CALL_ESTIMATE,     // its "Grant perCallEstimateCredits"
  disclosure: {
    periodLabel: 'minute',
    estimatedCallsPerPeriod: 10,                 // 5 NPCs, one decision each per 30s
    estimatedCreditsPerPeriod: Math.ceil(10 * NPC_CALL_AVERAGE),  // calls × the measured average
  },
  maxConcurrent: 2,
  maxCallsPerMinute: 30,
});
if (grant.status !== 'active') { runWithAuthoredLines(); return; }
await savePlayerState({ ...state, grantId: grant.grantId });
```

**The disclosure is computed from this game's own loop, never wished for.** Five
NPCs deciding once every thirty seconds is ten calls a minute. The player sees your estimate
attributed to the game, beside the platform's own worst case built from
`perCallMaxCredits`; an estimate that is transparently low is a grant that dies
mid-session. Each call under the budget still declares its own `maxCredits`,
and it may not be above the budget's `perCallMaxCredits`:

```
perCallEstimateCredits  ≤  perCallMaxCredits  ≤  the limit the player approves
maxCredits on each call  ≤  perCallMaxCredits
```

**Using the judge too?** Add `judge: { enabled: true, estimatedCallsPerPeriod }`
to the same request — the checks you really expect per `periodLabel`, from the
same loop arithmetic. The sheet tells the player the game also uses a fast
classifier billed as used, with the platform's own worst case beside your count.
A judge-only feature passes `models: []`. A budget with the judge is paid from
the player's credits only, and judge calls share the budget's `maxConcurrent` and
`maxCallsPerMinute`: batch questions into one call (up to 64) rather than one
call per question.

**Streaming a reply under the budget:**

```ts
const res = await generateStream({
  grantId, modelId, outputFormat: 'json', schema: LINE_SCHEMA,   // `line` is its first property
  prompt: npcPrompt(npc, playerLine), maxCredits: NPC_CALL_MAX,
  idempotencyKey: `npc:${npc.id}:${turnId}`,
  onPartialField: (_name, soFar) => npc.bubble.show(soFar),     // provisional
});
applyGeneration(res);                                            // the answer is THIS
```

The pieces are provisional: a call can still fail after text has shown (the
model broke off, the JSON missed the schema), so the bubble shows them and
`applyGeneration` decides what the game keeps — the same one writer as always.
Ceiling, benchmark and receipt are `generate()`'s: a started stream is billed the
work it did even when the player walks away mid-sentence. A stream holds one
of the budget's `maxConcurrent` slots until it has settled. Sometimes the reply
arrives whole — a busy stand, a retried call, a budget on the player's own plan —
and `onDelta` then gets the whole text once; the game needs no second path.

What each grant-ending code means:

| code | what happened |
| --- | --- |
| `grant_limit_reached` | the approved limit is spent |
| `grant_stopped` | the player pressed Stop |
| `grant_expired` | 24h passed, or the session ended |
| `waiting_for_plan` | their own plan is rate-limited for the stated time: not a failure, and there is no paid fallback |
| `grant_insufficient_funds` | the player's credits ran out before the next call |

Draw the readout from `getSpendGrant(grantId)` — calls made, credits settled,
what remains — never from a counter the game keeps itself. A finished grant may be
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
- Output is **data, never authority**: it may not grant Nex, items,
  entitlements, scores or progression by saying so. `source: 'external'` carries
  `modelProvenance: 'unverified'` because it is user-supplied — check it exactly
  as you would check typed player input.

## Errors land on the player's credits

There is no compensation lane, so this is all work you do before the call:

- **Validate inputs first** — a malformed prompt is still billed.
- **Always set `schema` for `outputFormat: 'json'`** — unschema'd JSON is the
  commonest way a call is charged and the result is unusable. Write it in the
  accepted dialect above; a refused schema is `invalid_schema` and costs
  nothing, but it is a feature that never runs.
- **Keep prompts short.** Long context is most of the bill.
- **Never loop `generate()` without a grant**, and never retry in a loop — each
  attempt is a separate charge, and a one-time call is at least one whole credit.
- **`generationErrorMessage(code)`** turns every code into words a player can
  read.
- **`status: 'unknown'` is not a failure.** It means the charge is not known
  yet, billing pending. Say "still settling", keep the reserved figure in the
  readout, re-read with `getGeneration(id)` — never call it failed, never retry.

## What the Genex side already does — do not rebuild it

The approval sheet shows the model, the prompt, the ceiling and the terms; the
game renders no price sheet. **Subscription funding is chosen only there** —
never add a "Your plan" row to the game's model picker, because a game cannot
offer a funding source. When the player's own watcher is online the personal-plan
answer arrives by itself and the game just waits, exactly as it waits for a
credit-funded call. The Genex dashboard header shows progress, active grants with
their spend, and a Stop; a Stop pressed there reaches the game as `grant_stopped`.

## Never

- **Never execute returned output** — no `eval`, no dynamic import, no scene
  graph or shader built from model text, no URL fetched because the output said so.
- **Never bundle a creator credential in a game.** Benchmarking is a CLI action
  on your machine, never something a shipped build does.
- **Never hand-roll fetch to the runtime API** — the SDK owns the approval
  handshake, and a hand-rolled call cannot obtain one.
- **Never hardcode a ceiling the bench did not print, a model id, a stand URL,
  or a margin.**
- **Never let the model be an authority over money, items or rewards**
  (`$genex-monetization` owns what may move a wallet).

These are source contracts, not a claim that every stand runs this lane —
`npx genex llm models` is what tells you.

## Checklist

- [ ] `npx genex llm models` says the lane is live
- [ ] Model ids come from `getGenerationModels()`, never from source
- [ ] The picker offers the featured set, labelled with the server's own `label`
- [ ] `maxCredits` — and a budget's `perCallMaxCredits` / `perCallEstimateCredits` — are the figures `npx genex llm bench` printed, verbatim — never a charged number
- [ ] No coin spelling (`estimateCoins`, `perCallMaxCoins`, `estimatedCoinsPerPeriod`) in new code
- [ ] The schema uses only the accepted dialect (no `$ref`, `pattern`, `format`, `anyOf`, `default`)
- [ ] A bench refused as `generation_limit` was answered with `npx genex llm status`, never a retry
- [ ] `generate()` / `requestSpendGrant()` is the first statement of a click handler
- [ ] A repeated-call feature uses a grant; a one-off uses `generate()`
- [ ] A decision (a label, a yes/no, a level) is a `judge()` question under the grant, not a `generate()` asked for a word
- [ ] Dialogue the player watches appear uses `generateStream()` under the grant; the resolved result, not the pieces, goes to `applyGeneration()`
- [ ] Disclosure numbers derive from the real loop and the bench's measured average
- [ ] Every grant-ending code is handled
- [ ] The in-game readout comes from `getSpendGrant()`
- [ ] Exactly one `applyGeneration()` writer; boot re-attaches with `waitForGeneration()`
- [ ] `generationId` is saved BEFORE the await
- [ ] Output is schema-validated and grants nothing by itself
- [ ] `unknown` reads as "still settling", never as a failure
- [ ] The game renders no price sheet and no funding picker

## Troubleshooting

**Everything on this lane 404s** — runtime generation is off on this stand.
Nothing to fix in the game.

**Nothing opens when the player clicks** — an `await` ran before `generate()`
and the gesture was lost. Move the call to the first line of the handler.

**`player_wallet_required`** — ONE code for the two early dead ends: a guest on
any build, and anyone but the game's OWNER on a `genex preview` test build.
`waitForPlayer()` tells them apart. `guest: true` — guests play but have no
credits to spend. Signed in and still refused on a test build —
that account does not own the game. Open the preview signed in as the owner and
the call works there, before any player sees it: the same sheet, the same
terms, billed to the owner's own credits or plan, marked "test build" on Genex.
Everyone else can use it after `genex promote`. The SDK's stock sentence for
this code covers both causes.

**`grant_price_unreasonable`** — a call under the budget declared a `maxCredits`
above the budget's `perCallMaxCredits` (or a judge call's worst case is above
it). Declare the bench's `Declare maxCredits` on each call and its
`Grant perCallMaxCredits` on the budget — the second is never below the first.

**`insufficient_credits`** — the player's credits cannot cover this one-time
call's ceiling. Say it once in-fiction, keep the authored fallback, and never
retry in a loop; the Genex sheet already offers them a top-up. From
`npx genex llm bench` it is YOUR balance: the bench prints what it can spend.

**`credits_unverified`** — the player's Genex email is not verified, and credits
pay only for a verified account. Show the feature as verify-to-use rather than
hiding it; nothing was charged.

**`generation_paused`** — the platform has paused paid generation for now. Not
the game's fault and not the player's: keep the authored fallback, try again
on a later deliberate click, never in a loop.

**`judge_not_enabled`** — the budget was approved without the judge. Request a
new one with `judge` from the next deliberate click; never auto-renew.
**`judge_requires_grant`** — the judge's model was sent to `generate()` with no
budget; the judge is grant-only and is called with `judge()`.
**`judge_requires_credits`** — a judge call under a budget that is not paid
from the player's credits (their own plan cannot pay the judge). Request the
budget with `judge` and let it be credit-funded; keep the authored branch.
**`judge_period_limit`** — the checks reached the ceiling the player approved for
the period (your own `estimatedCallsPerPeriod` at the largest size): wait, and
if it keeps happening your declared rate is too low — fix the loop or the
estimate, never retry in a tight loop.

**`stream_requires_grant`** — `generateStream()` was called without a
`grantId`. Streaming is grant-only: a one-time call waits on the player's
approval popup, so use `generate()` for it.

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
before it finished, and the attempt is still billed. The declared `maxCredits`
is too low for the answer's length — re-benchmark and declare what the bench
prints, never a charged number — or the answer is longer than one call on this
stand may produce, and the fix is a shorter answer (fewer fields, shorter
strings, a length the prompt states).

**`invalid_schema`** — the schema uses a keyword outside the accepted dialect
(`$ref`, `pattern`, `format`, `anyOf`, `default`, `examples`, `$schema`), or an
object without `additionalProperties: false`. Nothing was charged. Rewrite it in
the subset above; `description` and `title` are allowed.

**`grant_concurrency` / `grant_rate_limited`** — the game calls faster than the
grant's own limits.

**`payer_busy`** — the player's account was busy on Genex for a moment and
nothing was charged or started. Retry once after a short pause, from the same
action; it is not a refusal.

**`grant_not_active`** — the saved `grantId` is finished. Clear the stored id
and re-request from a fresh click.

**`external_request_active`** — that player already has one personal-plan
request running. Wait for it; never fall back to charging credits instead.

**The call is billed but the result is unusable** — `outputFormat: 'json'`
without a `schema`. Add one; the charge already happened.

**A reload lost the answer** — `generationId` was not saved before the await, or
boot never calls `waitForGeneration()`. Both halves are required.

**The in-game readout disagrees with the Genex header** — the game is counting
calls itself. Read `getSpendGrant()` instead.
