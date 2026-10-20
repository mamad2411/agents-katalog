---
name: llm-cost
description: "Control what an LLM feature or agent pipeline costs without degrading it: fetch today's prices and count tokens against the exact model rather than from memory, attribute token spend to a prompt path before changing anything, judge prompt caching on reads per write rather than hit rate because a cache write carries a premium, route cheap steps to a small model against a measured quality bar, retrieve instead of stuffing, batch what nobody waits on, and set per-request and per-tenant ceilings with degrade, queue or refuse decided in advance. Use whenever someone says \"our OpenAI bill tripled this month\", \"how do I use prompt caching\", \"should this call a cheaper model\", \"our agent loop is burning tokens\", or \"cap what a single request can spend\". Not for the cloud bill (cost-review), load testing (capacity-planning), application CPU time (profiling) or telemetry design (instrumentation)."
allowed-tools: "Read, Write, Edit, Grep, Glob, Bash(jq:*), Bash(python:*), Bash(curl:*)"
---

# LLM Cost

This is finished when you can name the prompt path that holds the spend, state a unit cost — per request, per task, per tenant — computed from prices you fetched today, and say what quality bar each change was measured against and what the system now does when a budget runs out.

Token spend goes wrong in a way that cloud spend does not. The bill arrives as one number per model per month, the fix is always in one prompt path, and the gap between those two facts is where the effort gets wasted: the team optimises the call it remembers writing rather than the call that runs on every request, trims a system prompt while output tokens hold the bill, or swaps in a cheaper model and converts a cost problem into a quality problem that nobody is measuring.

Three mechanisms make the loss non-linear, and none of them is visible in a per-call view. The first is that prompt caching can cost more than not caching: a cache write is charged at a premium over ordinary input, so traffic that does not come back to the same prefix inside the cache lifetime pays that premium on every call and never reads an entry. Teams watch a hit rate climb and conclude they are saving money while the bill rises, because hit rate is the wrong metric — the metric is reads per write. The second is that an agent loop resends its whole growing history at every step, so cost per task climbs faster than steps, and an unbounded loop is the LLM equivalent of a runaway query: one task can spend more than a day of normal traffic. The third is that the numbers themselves move. Per-token prices, cache multipliers, context limits and even the tokenizer change under a running system, so an analysis built on remembered figures is wrong by a multiple and says nothing about it. The order below exists to make each of those hard to do by accident.

## Scope

Use for: a token or inference bill that grew and nobody can say which feature caused it; deliberately reducing what an LLM feature or agent pipeline costs; prompt caching design and debugging a cache that is not paying; routing steps between a cheap and an expensive model with a measured quality bar; context-window discipline, retrieval and truncation policy; batch and streaming decisions; per-request and per-tenant budget ceilings and what happens when one is exhausted; retry and agent-loop caps; reporting cost per unit of work for an AI feature.

Do not use for: the cloud bill — compute, storage, transfer, commitments — which is `cost-review` and has different signals and different fixes; whether a system survives a launch or a peak, which is `capacity-planning`; application CPU time and slow functions, which is `profiling`; deciding what telemetry answers a question in general, which is `instrumentation` (this skill says what to record about cost, and cedes the rest); rolling out AI tooling to a team, which is `ai-enablement`; choosing between model vendors on a scorecard, which is `vendor-evaluation`.

GPU spend for self-hosted inference sits on the boundary: the utilisation and purchase-model half of it is `cost-review`, and the tokens-per-request half is here.

## Two gates

**Attribution gate.** No model change, no prompt edit, no caching work until every call is tagged and the top three prompt paths have a measured share of token spend. Spend is calls multiplied by cost per call, and those two factors fail in opposite directions: the expensive-looking prompt that runs fifty times a day is rarely the answer, and the small classification call on the request path usually is. A team that starts optimising before it has this table optimises what it can remember, which is why the same bill keeps coming back.

**Quality gate.** No routing change, no truncation rule and no context reduction ships without a stated bar and the eval set it was measured on. "Cheaper and it looked fine on three examples" is the failure that costs most, because a model that fails a few per cent more often pays that back in retries, escalations to a human, and support load — none of which appear on the model bill. If there is no eval set for the path you want to make cheaper, building one is the first deliverable.

## Workflow

### 1. Fetch today's prices, and count tokens against the model you will deploy

A cost number has two halves and both go stale on their own. Do this first, because every later step multiplies by it.

- **Fetch the vendor's current published pricing at the moment of the analysis**, and record the figure with the page and the date you fetched it in whatever you write. A cost analysis with no fetch date cannot be checked later, and a price recalled from memory — including a model's memory — is a guess that looks like a fact.
- **Take four prices, not one**: uncached input, cache write, cache read, and output, plus the batch multiplier. Collapsing them into one blended rate is what makes caching and batching look like they did nothing.
- **Confirm the denominator.** Prices are published per million tokens by some vendors and per thousand by others, and the error is a factor of a thousand.
- **Price the exact model version you call**, not the family alias. A dated identifier and its successor are commonly priced differently, and an alias can move under you without a deploy on your side.
- **Enumerate the billing dimensions that are not tokens.** Per-session-hour charges, data-residency multipliers and prepaid consumption-unit currencies now sit alongside per-token pricing at some vendors, and a model of tokens multiplied by a price cannot express any of them. Read the whole pricing page before building the spreadsheet.
- **Count tokens with the provider's token-counting endpoint, against the exact model you will deploy.** Tokenizers change between generations inside a single family, and a newer generation has produced materially more tokens for identical text — so an estimate carried across a model migration is wrong even when the price table is right. "About four characters to a token" is a rule of thumb for one tokenizer, not a cross-model constant, and estimating cost from character counts or from another model's counts is how a migration arrives with a bill nobody forecast.

Then compute, per prompt path, `calls x (input_tokens x price_input + output_tokens x price_output + cache_read_tokens x price_cache_read + cache_write_tokens x price_cache_write)` and divide by the unit the business runs on — per request, per resolved ticket, per document processed, per active tenant per day. Report that unit and its trend beside the total. A total that grows while unit cost falls is a product working; a unit cost that grows is the alarm, and it is the only number that says whether a re-architecture is worth funding.

Treat every multiplier in this skill as a shape to substitute current figures into, never a number to carry. The churn is real and it runs in both directions: a top tier has fallen several-fold, a published increase has been announced and then withdrawn, the cache-read multiplier has forked per model rather than staying one constant across a lineup, and models have been retired out from under callers. Anything you write down that you did not fetch should say so.

Output tokens cost more than input tokens everywhere, and the reason is worth holding onto because it says which lever is large. Input is processed in one parallel prefill pass over the whole prompt; output is generated one token at a time, each pass reading the entire model state, so hardware produces output far more slowly than it consumes input. That asymmetry means an explicit output cap, a tight response schema and an instruction to answer without preamble are frequently a bigger saving than anything done to the prompt — and that a long static prompt is cheaper than it looks, especially once it is genuinely being read from cache.

### 2. Attribute spend to a prompt path

Tag at the call site, not in a dashboard afterwards. The minimum set of fields on every call record:

| Field | Why it has to be there |
| --- | --- |
| `prompt_path` | A stable identifier per template, versioned when the template changes. This is the unit every later decision is made on |
| `feature` and `tenant` | The bill is read by feature; the abuse and the outlier are found by tenant |
| `model` | Routing changes are unreadable without it, and a fallback that quietly promoted every call to the expensive model is a common surprise |
| `step` and `task_id` | Which agent step this was, and which task it belonged to. Cost per task is the number that matters for a loop; cost per call hides it |
| Cached input, written and read | Kept apart from uncached input, because all three are priced differently and a cache that is not paying is invisible in a single input total |
| `outcome` | Success, retry, fallback, refusal. A retried call is billed twice and must be countable |

Record the token counts the provider returns rather than a local estimate. Confirm the field names against the provider's current API reference before writing the recorder — they differ between vendors and have changed as caching and reasoning billing were added — but expect four distinct quantities: uncached input, cache writes, cache reads, and output. Reasoning or thinking tokens are billed as output at most vendors even though you never see them in the response text, which is why a reasoning model's cost per call can be several times what the visible answer suggests.

Aggregate from the structured call log:

```bash
set -Eeuo pipefail

# Token spend by prompt path. Sort by whichever column today's price list makes
# dominant, which is usually output.
jq -rs '
  group_by(.prompt_path)
  | map({
      path:       .[0].prompt_path,
      calls:      length,
      input:      (map(.input_tokens)       | add),
      cache_read: (map(.cache_read_tokens   // 0) | add),
      output:     (map(.output_tokens)      | add),
      retries:    (map(select(.outcome == "retry")) | length)
    })
  | sort_by(-.output)' calls.jsonl
```

Then read the shape of the growth rather than the total. An LLM bill grows in exactly four ways and the fix differs for each:

| Shape | Usual cause | Where the fix is |
| --- | --- | --- |
| More calls, tokens per call flat | A feature shipped, traffic grew, or something now calls the model per row rather than per batch | Step 8 (loops and fan-out), or accept it as growth and check unit cost |
| Input per call climbing over weeks | Context stuffing: retrieval returning more chunks, history never summarised, a tool list that keeps growing | Steps 3 and 4 |
| Output per call climbing | A schema that grew, a "be thorough" instruction, reasoning enabled, no output cap | Step 3, and the output cap in step 7 |
| Tokens per task climbing while calls per task climb too | An agent loop taking more steps and resending more history each time | Step 8 |

`references/token-accounting.md` has the call-record schema, the derivation of cost per unit of work, and the break-even arithmetic with every multiplier left symbolic. Read it when the attribution gate fails or before computing any break-even.

### 3. Cut the input before you change the model

Context is the cheapest thing to fix and the first thing to grow. Work down this list before touching the model choice:

- **Retrieve rather than stuff.** Selecting the few passages that decide the answer costs a retrieval call and saves the rest of the corpus on every request. Stuffing a whole document set into every prompt is paying to re-read it each time.
- **Cap the retrieval fan-out and measure it.** Top-k crept from 5 to 20 because someone was debugging a recall miss; check what k currently is and what accuracy it actually buys, because the token cost is linear in k and the accuracy usually is not.
- **Summarise history at a threshold rather than carrying it.** A conversation that resends every turn grows quadratically in tokens over the session. Roll turns older than a threshold into a summary and keep the last few verbatim.
- **Prune few-shot examples by contribution.** Drop each example and measure. Examples are often kept long after the instruction that replaced them landed.
- **Count the tool schemas.** Every tool definition is input tokens on every call in the loop. A twenty-tool agent pays for twenty schemas at every step; give each step only the tools it can use.
- **Truncate on what decides the answer, not on position.** When something must be cut, keep the instruction, the question, the most recent turn and the retrieved evidence, and cut the middle of long documents first — retrieval accuracy over a long context is weakest in the middle, so those tokens are paying least. Measure it on your own data before trusting it as a rule; the size of the effect varies by model and by task.
- **Truncate deterministically and tell the model you did.** A silent truncation produces a confident answer from a document whose second half was dropped. A marker saying content was elided is a few tokens and prevents an answer nobody can explain.

`references/caching-and-context.md` covers prefix design, the invalidation checklist and truncation policies in full. Read it before designing a cache or a truncation rule.

### 4. Judge caching on reads per write, not on hit rate

Prompt caching writes a prefix once at a premium over ordinary input, then charges a small fraction of the input rate to re-read it on a later call that begins with exactly the same bytes. The premium is the half that gets forgotten, and forgetting it inverts the result: caching traffic that does not return to the same prefix inside the cache lifetime costs strictly more than not caching at all.

**The metric is reads per write.** Divide cache-read tokens by cache-write tokens on one prompt path, over a window longer than the cache lifetime, and compare the ratio against the break-even implied by today's multipliers. With a read discount of roughly an order of magnitude and a write premium of a modest fraction over standard input, the break-even lands near one read per write for a short cache lifetime and near two for a long one. Take the current multipliers off the pricing page and recompute rather than adopting those two numbers; the read multiplier has already forked per model. The formula is in `references/token-accounting.md`.

The failure this names is specific and common: a system prompt marked cacheable on every request, served to traffic that arrives further apart than the cache lifetime. Every call pays the write premium, no call ever reads a live entry, and a hit rate computed as "calls with caching enabled" climbs toward 100% while the bill goes up. Reads per write on that path is zero, and it is the only number that says so.

Three mechanical facts decide whether a cache can hit at all. Look each up for the model you call — they are per-model and version-specific — and check yours against them:

- **A minimum cacheable prefix length, which differs per model** and is not ordered by model tier, so it cannot be guessed from price or size; published values have spanned several hundred to a few thousand tokens. Below the threshold the cache marker is ignored silently and no error is returned, which is the worst shape this failure can take: the configuration is present, the code is correct, and nothing is cached.
- **A strict prefix hierarchy** where tool definitions come first, then the system block, then messages. A change at any level invalidates that level and everything after it, so editing one tool description invalidates the entire cache for that path, while changing a message-level parameter or attaching an image invalidates only the message blocks.
- **A bounded lookback over how many blocks are checked for a cache match**, so a conversation that keeps growing silently stops matching — again with no error. Check the limit and design the history to stay inside it.

Two timing traps sit on top of those. The cache lifetime is commonly measured from the start of the request that writes the entry rather than from the end of its response, so a slow generation eats part of the window it just created. And the lifetime is refreshed by a hit at most vendors, which means a path either stays warm under steady traffic or never warms up at all — there is little middle ground, and the bimodality is why an aggregate hit rate across paths describes none of them.

Then make the prefix stable. Order the prompt most-stable-first — system instructions, tool definitions, static corpus, per-tenant context, retrieved chunks, history, the current turn — and put the breakpoint at the end of the stable region rather than the end of the prompt. The invalidators that hide longest:

| Invalidator | Why it is easy to miss |
| --- | --- |
| A timestamp, "today's date", or a request id near the top | Looks like context, changes every call, invalidates everything after it |
| Per-user or per-tenant text spliced in early | Shrinks the cache to one user, so reads per write collapses under real traffic |
| Tool definitions or JSON serialised with unstable key order | Several languages do not guarantee ordering; identical objects, different bytes, no cache and no error |
| Non-deterministic float or whitespace formatting | Same content when printed, different when hashed |
| Retrieved chunks placed before static instructions | The most volatile content sits where the most stable should |
| A model alias that moved, or a parameter change | Commonly invalidates as a matter of course; check the provider's rules |

Verify with the returned counts, never by inspection:

```bash
set -Eeuo pipefail

# Reads per write on one path. Below the break-even, caching is costing money.
jq -rs --arg path "support.triage.classify" '
  map(select(.prompt_path == $path))
  | {calls: length,
     write: (map(.cache_write_tokens // 0) | add),
     read:  (map(.cache_read_tokens  // 0) | add),
     plain: (map(.input_tokens) | add)}
  | . + {reads_per_write: (if .write > 0 then (.read / .write) else null end)}' calls.jsonl
```

Per path and per tenant, not in aggregate. An aggregate averages a warm path against a cold one and reports a figure that describes neither.

### 5. Route by difficulty, against a measured bar

Split the pipeline into steps and ask what each one actually requires. Classification, extraction, routing, reformatting, tagging and short-answer lookups are usually within reach of a small model. Synthesis, ambiguous judgement, multi-constraint planning and anything a user reads verbatim usually are not. Some steps need no model at all, and removing a call beats making it cheaper.

- Route on the task, not on the input. Prompt length is not difficulty, and routing on it produces a system whose behaviour changes when someone pastes a long email.
- Build the eval set from production traffic with labelled outcomes before you switch anything. Twenty hand-picked examples measure nothing; a few hundred sampled cases with the distribution's hard tail in them measure the decision.
- State the bar as a tolerance on the metric that matters — "extraction F1 within one point, refusal rate unchanged" — and accept the cheap model only if it clears it. Write the bar down before running the comparison, because a bar chosen afterwards is chosen to fit the answer.
- For a cascade, where a cheap model runs first and escalates on low confidence, the saving depends entirely on the escalation rate: every escalated request pays for both models and both latencies. Measure the rate on real traffic and recompute — a cascade that escalates often is more expensive than going straight to the large model.
- Fine-tuning or distilling a small model onto a narrow step is the lever when a routing split fails its bar, but price the training, the labelled data and the re-evaluation on every base-model change alongside the inference saving.
- Check what the fallback path does. A fallback that promotes to the expensive model on any error turns a bad afternoon upstream into a bill nobody predicted; cap it.

`references/routing-and-budgets.md` has the routing evaluation procedure, the cascade arithmetic, and the budget and loop controls that follow. Read it when planning a routing split or designing budget enforcement.

### 6. Batch where nobody is waiting, stream where they are

Asynchronous batch endpoints trade latency for a materially lower price at most vendors. Check the current discount and the completion window in the provider's documentation, then apply the obvious rule: anything a user is waiting on stays synchronous, and anything that runs on a schedule should not be. Backfills, nightly enrichment, bulk classification, evaluation runs, document ingestion and offline scoring are all batch work that is commonly paying interactive prices for no reason. Do not batch anything whose result feeds a page, an alert, or a decision with a deadline shorter than the window.

Streaming does not reduce the price of a token. What it buys is the ability to stop, which is only a saving if something actually stops:

- Terminate on stop sequences and on a structurally complete response rather than generating to the cap.
- Propagate user cancellation all the way to the provider request. A client that disconnects while the upstream stream continues bills every remaining token to no one's benefit, and this is a common defect because nothing user-visible goes wrong.
- Set a max output length per prompt path. The cap is a cost ceiling, not a quality setting, and a path without one has no upper bound on what a single call can spend.

### 7. Put a ceiling on one request, and decide exhaustion behaviour in advance

Budgets belong in the client wrapper every call goes through, not in each call site, because the call site that skips the check is the one that runs away.

| Level | Ceiling | Enforced by |
| --- | --- | --- |
| Single request | Max input tokens, max output tokens, max steps, max wall clock, max cost | The wrapper, before the call is made |
| Task or session | Total tokens and total cost across all steps of one task | A counter carried with the task, checked between steps |
| Tenant | Cost per tenant per day, with a separate ceiling for trial accounts | The wrapper, from a shared counter |
| Feature | Cost per feature per month, tracked against a projection | A dashboard and an alert, not a hard stop |
| Global | A kill switch that stops non-essential LLM traffic | One flag, tested, with a named owner |

What happens when a ceiling is reached is a product decision, and it has to be made before the day it happens. There are three answers and the right one differs per feature:

| Behaviour | When it fits | What the user sees |
| --- | --- | --- |
| **Degrade** | The feature has a cheaper form: a smaller model, less context, a cached or templated answer, or a non-LLM heuristic | A result, with a note that it is a reduced one |
| **Queue** | The work is not interactive, or is tolerable later | An acknowledgement and a time |
| **Refuse** | Correctness matters more than availability, or the spend is likely abuse | An explicit, explained error — not a silent failure, and not a degraded answer presented as a full one |

Write the choice per feature into the runbook and make the message text a reviewed artefact. Deciding this during an incident produces either an outage or an invoice nobody signed off.

Alert on rate rather than on the monthly total. A monthly threshold trips after the money is spent; spend per hour against the same hour last week catches a loop the morning it ships. Route it to the team that can act, with the prompt path in the alert — `alert-design` covers why an unactioned cost alert decays exactly like an unactioned page. Keep the API key out of command lines, URLs and logs: read it from the environment inside the process, and redact request headers before anything is stored, because an argument list is readable by every process on the host and a log outlives the incident.

### 8. Bound the loop, and count the retries

An agent loop is the largest cost risk in the system because its spend is unbounded by construction. Each step commonly resends the whole accumulated history, so tokens per task grow with the square of the steps rather than linearly, and a loop that cannot make progress will happily spend until something external stops it.

- **Cap the steps** and make the cap a hard stop with a defined outcome, not a warning.
- **Cap total tokens and total cost per task.** The step cap alone does not bound spend, because one step can carry an enormous context.
- **Detect no progress.** The same tool call with the same arguments twice, or a repeated assistant turn, means the loop is not converging. Stop and return what it has rather than paying for the next twelve identical steps.
- **Memoise tool results within a task.** Re-reading the same file three times costs the tokens three times.
- **Keep the per-step context bounded.** Summarise or drop old tool output rather than carrying every result forward; a tool that returns a large payload should return a summary and a handle to the rest. This is also what keeps a growing conversation inside the cache lookback limit from step 4.
- **Bound fan-out.** Sub-agents multiply: five sub-agents each given the full context cost five times the context plus their own work. Give a sub-agent the narrowest brief that lets it answer.

Retries are the quiet version of the same problem, because a retried call pays for the whole input again.

- Cap attempts, and back off with jitter.
- Retry only what can succeed on a second attempt — a timeout, a rate limit, an overloaded response, a truncated stream. A schema violation, a refused request or a context-length error is deterministic and will fail identically at full price.
- Count retried and fallback calls separately in the cost report. A path whose retry rate quietly doubled is a cost regression and usually an upstream reliability signal as well.
- Watch retries in a loop: a retry inside a step inside a fan-out multiplies three ways, and that combination is what turns a bad hour into a month's budget.

## Output format

```markdown
## Prices used
[Vendor page, date fetched, the four token prices and any non-token dimensions.]
[Token counts measured against which exact model.]

## Attribution
[Share of token spend mapped to prompt paths; anything unattributed and why.]

## Unit cost
[Cost per request / task / tenant now, its trend, and the total beside it.]

## Top paths
| Path | Calls | Input | Cache read | Reads per write | Output | Cost | Share |

## Changes
### C1 — [what it is]
Saving:     [figure per month, and the unit cost it moves]
Measured:   [the eval set and the bar it cleared, or "not yet measured"]
Degrades:   [latency, accuracy, coverage, freshness — or "nothing, and why"]
Effort:     [config / prompt change / engineering work]
Verify on:  [date, and the number that has to move]

## Caps and exhaustion behaviour
[Per-request, per-task, per-tenant ceilings; degrade, queue or refuse per feature.]

## Not recommended
[What was considered and rejected, with the quality reason.]
```

## Anti-patterns

**Quoting a per-token price, a cache multiplier or a context limit from memory.** All of them move, in both directions, on models you are already running, and a stale figure produces a confident analysis wrong by a multiple. Fetch them, write down the date, and check whether the vendor has added a billing dimension that is not tokens at all.

**Estimating tokens from character counts or from another model's tokenizer.** Tokenizers change between generations within one family, so the same text can cost materially more after a migration that changed nothing else. Count against the model you will actually deploy.

**Reporting cache hit rate.** It can climb to 100% on a path that has never once read a live cache entry, because every call is writing one at a premium. Reads per write is the number, per path, against a break-even computed from today's multipliers.

**Caching a prefix below the model's minimum length.** The marker is ignored, no error is returned, the code review passes, and the cache never existed. The minimum differs per model and is not ordered by tier, so look it up rather than reasoning about it.

**Changing the model first.** It is the most visible lever and the one most likely to be wrong, because it changes every path including the ones that were not expensive. Attribute first; the answer is frequently a retrieval fan-out or a retry loop, and swapping the model would have hidden it behind a quality regression.

**A cheaper model with no quality bar.** The saving is immediate and the cost arrives as retries, escalations, support tickets and a churned customer — none of which land on the model bill, so the change looks like a win in the only place anyone is looking.

**An agent loop with no step or token cap.** One malformed input, one tool that always errors, and a single task spends more than a normal day. This is the runaway query of this discipline, and the fix is the same: a ceiling that stops it, not a dashboard that watches it.

**Trimming the system prompt while output holds the bill.** Output is the more expensive side and a cached prefix is cheap, so hours spent compressing static instructions frequently save a rounding error. Check which side the spend is on before optimising either.

**A budget with no defined exhaustion behaviour.** The ceiling is reached at 02:00 and the system does whichever of degrade, queue and refuse the code happens to imply — usually an unhandled exception in the user's face. Decide it per feature, in advance, and write the message.

**Reporting a monthly total instead of a unit cost.** A bill that grew with a product that grew is not a problem, and cutting it may be the wrong move. Without a denominator nobody can tell growth from waste, and the argument goes to whoever is loudest.

## Reference files

- `references/token-accounting.md` — read when the attribution gate fails, or before computing any break-even: the call-record schema and what each field is for, aggregation queries, deriving cost per unit of work, and the break-even arithmetic for caching, batching and a cheap-model cascade, with every multiplier left symbolic so it survives a price change.
- `references/caching-and-context.md` — read before designing a cache or a truncation rule: the prefix hierarchy and what each level invalidates, minimum length and lookback limits and how they fail silently, reads-per-write diagnosis, prompt ordering by volatility, the full invalidation checklist, retrieval fan-out tuning, history summarisation, and truncation that keeps the deciding content.
- `references/routing-and-budgets.md` — read when planning a routing split or building budget enforcement: choosing the eval set and the bar, the per-step difficulty classification, cascade and fallback arithmetic, the wrapper that enforces ceilings, degrade, queue and refuse policies with what the user sees, and the agent-loop and retry caps.
