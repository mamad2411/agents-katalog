---
name: building-with-decision-models
description: Use when code needs a judgment about natural language that rules or regex cannot make (classify, route, triage, moderate, score, rank, match, dedupe, filter, extract, verify, or gate an action), when brainstorming where AI could fit in an app, when an LLM call exists only to pick a label, score, or yes/no, or when code uses a decision model or System One model such as TypeSafe Jev, Cloudflare Clef, Perplexity pplx-decider, Microsoft-Decision-1 on Microsoft Foundry, Databricks ai_decide, Ollama's /v1/systemone (Nimble, Tev1, Kev), Laya, Strands Decider, CLM, typesafe-sdk, or @typesafe-ai/sdk.
---

# Building with Decision Models

## Overview

A **decision model** (also called a System One model) takes a `state` plus named, typed questions and returns typed answers with probabilities. It never generates text. **Code owns the workflow. The model supplies narrow snap judgments.** It is not a chat or coding LLM and cannot power a coding agent.

TypeSafe's Jev started the category on 2026-09-15 with the `POST /v1/systemone` contract and three question types: `noul`, `choice`, and `score`. Every provider since uses the same three question types, so the rules below hold for all of them. Many accept Jev's body unchanged (Ollama, Kev, Laya, Strands Decider, gateways, and Microsoft-Decision-1 under an Azure path and auth). Others keep the ideas but change the wire format: Clef REST wraps the answers in `result`, Databricks renames the Noul answer `probability`, and OpenAI and Perplexity serve their own paths with their own field names. What also differs is the model names, the limits, the price, and **how well the probabilities match reality**.

**Before you design anything new, check prior art:** open `prior-art/INDEX.md`. It maps intents (control loop, gate, rerank, stream filter, incremental, agent memory, LLM pairing, and more) to shape files. Each shape file has a code sketch, field lessons, and a few flagship community projects, with the model each one used. The full project lists are in `prior-art/projects/`. Or grep `prior-art/` (recursively) for a domain word. It also lists the known bad fits as one-line headlines. The evidence and links are in `prior-art/bad-fits.md`. Notes for one model other than Jev (limits, calibration, failures, per-shape lessons) are in `models/<name>.md`; `models/INDEX.md` lists them.

Exact request and response shapes: `providers/jev.md` is the reference contract. Each other file in `providers/` lists how that provider differs. Patterns and the cookbook index: see `patterns.md`. A provider's live docs win on conflict. Do not guess field names. Check them there. If the docs cannot be reached, read the installed SDK's types, tell the user you did, and do not invent details that depend on the version.

**Open-ended request** ("where could AI help in this app?"): work backward from what the app should show, select, change, or hand off. Offer two or three directions from `prior-art/INDEX.md` and recommend one. **Concrete request:** pick the shape and build. Either way, keep the user's stack and scope, and add a decision model only where code needs a judgment.

## Pick the provider

Use the one the project already uses. If there is none, pick by the constraint that matters most, then open its file in `providers/`.

| Need | Start with | File |
|---|---|---|
| Best measured accuracy and calibration, lowest hosted price | TypeSafe Jev | `providers/jev.md` |
| Already on Cloudflare Workers, or the state includes images | Cloudflare Clef / Clef-flash | `providers/clef.md` |
| Very long state (whole documents, long transcripts) | Perplexity pplx-decider | `providers/perplexity.md` |
| Azure shop, Entra auth, or US/EU data-zone processing | Microsoft-Decision-1 on Microsoft Foundry (Jev body, Azure path, deployment name as `model`) | `providers/microsoft-foundry.md` |
| Decisions over rows already in a warehouse | Databricks `ai_decide()` | `providers/databricks.md` |
| Data must not leave the machine, offline, or free tests | Ollama: Nimble, Tev1, Kev | `providers/ollama.md` |
| Data must stay in the EU | System1 Models (1 question per request), Strom | `providers/eu-hosts.md` |
| One key for several providers, or switching between them | OpenRouter, Vercel AI Gateway, LLM Gateway, pydantic-ai | `providers/gateways.md`, `providers/pydantic-ai.md` |
| Smallest possible model, CPU, or a model you will fine-tune | Laya, Strands Decider, CLM-8B, SemIf, NanoJev | `providers/open-weights.md` |
| OpenAI shop, or images in the state | OpenAI Decisions API (`gpt-6-luna`, public beta, its own request format) | `providers/openai-decisions.md` |

"Accepts the Jev request" means the code runs. It does not mean the answers are as good. Open models trail Jev by a wide margin on out-of-domain tasks, and some are weak on large option sets. Measure on the user's own labeled cases before you commit (see "Changing models").

## Test against the live API when you can

You get better results when you check a design against a real endpoint. A live call catches a wrong field name, and it shows when the model reads a question differently than you meant. Run a small probe before the code reaches the project:

- **Hosted provider:** only if its key is already set in your shell (the provider file names the variable, such as `TYPESAFE_API_KEY`). One call usually costs a fraction of a cent.
- **Local model:** if Ollama is running (`curl -s localhost:11434/api/version`), a probe is free and needs no key. A local model's answers are not a stand-in for a hosted model's accuracy, but they do check the request shape.

If no endpoint is available, design from the provider file and say that you did. Do not go looking for keys in `.env` files, shell profiles, or key files. Point the user to the README section "If the agent cannot see the key".

**Rules for any key:**
- Do not print, echo, log, or commit it.
- Do not hardcode it or pass it as a literal in code. Let the SDK or the code read the environment variable. Keep it server-side.
- Debug logging can print request bodies unredacted (`TYPESAFE_LOG_LEVEL=debug` does). Turn it off before real data flows.
- A `401` means the key is wrong or rotated. Ask the user to replace it where they stored it, never in the chat.
- Keep a task to about 10 test calls, and keep probe loops to about 8 workers or fewer. Rate limits are shared across the account.

## Pick the primitive

| Answer shape | Primitive | Returns | Branch on |
|---|---|---|---|
| One of an unordered set | `Choice` (a map of options) | `choice`, `probabilities`, `confidence` | `choice`; gate with `confidence` |
| Position on a spectrum you can describe | `Score` (an ordered list of levels) | `score` (0…n-1, can be fractional), `legend`, `probabilities`, `confidence` | threshold or sort `score` |
| Yes/no | `Noul` (optional `true`/`false` criteria) | P(yes), **no `confidence`** | P(yes) > threshold |

A Noul of 0.5 means "unsure", never "medium". Degree questions ("how strong in Python") need a Score. Several labels that can apply at once need one Noul per label, not a Choice.

Limits depend on the provider. The Jev contract allows up to 255 Choice options and 2–10 Score levels, and most copies match. Check the provider file before you rely on a large option list, a long list of questions, or a long state. Context windows vary even more: CLM-8B silently cuts the state at 2,048 tokens, and Tev1 and Laya are also small. Open the provider file before you send a long transcript.

## Rules

1. **One snap judgment per question.** Pose something a knowledgeable person decides in a second. Split "angry AND wants refund" into two questions and combine them in code. Atomic does not mean trivial: picking one bounded action or reading one message in context is a single judgment. Do not split apart a relationship the question is about (does this passage support that claim?).
2. **Put every question for one state in one request**, including speculative ones. They run in parallel and in isolation. Extra questions add almost no latency, but each one adds input tokens, so check `usage.input_tokens` on a real request. Write the premise into the text: `"If this is a technical problem, how severe is it?"`. Code ignores the answers on branches it does not take.
3. **A second request only when the first answer is needed to build it**: to fetch more state, to build new state, or to pick the next options (hierarchical walk, shortlist then full text).
4. **Question IDs are never sent to the model.** Write the full question in `instructions`.
5. **Write the exact condition.** Decision models read literally: they answer the question you wrote, not the one you meant. Scope words, negations, and implied conditions count at face value. When a wrong answer makes you explain what you really meant, that explanation is the missing half of the instruction. Put boundary cases in the criteria. Avoid double negatives and property-of-a-property hops. Name the state path instead.
6. **Structure state as a named JSON object.** Point at parts with backticked paths: ``"Does `ticket.messages[0].text` request a refund?"``. Send only what the question needs. Irrelevant state lowers accuracy. Include metadata (plan, timestamps) only when a question refers to it.
7. **Score levels describe situations, not degrees.** Write `"Broken feature, workaround exists"`, not `"moderate"` or `"2"`. Each level is judged alone, so "worse than the previous level" means nothing. Give each level one dimension.
8. **Choice: give the full option list plus `other` / `none_of_the_above`**. When two options get confused, make each value an object: `{"what": ..., "not_for": ..., "examples": [...]}`. Use the same keys on every option. Name options with words, not codes: renaming options from `0`/`1` to `no`/`yes` with the same rubric flipped about 70 answers in 100 in one study ([arXiv:2609.26758](https://arxiv.org/abs/2609.26758)).
9. **Phrase a Noul so that high = yes.** Keep criteria aligned with the instruction. Never map `true` to a "no" meaning.
10. **Keep math, counting, dates, and exact lookups in code.** To count, ask one Noul per candidate and sum. For dates, extract the parts with Choices (include `not_stated`) and compare in code. For extraction, find candidates with regex or an LLM, then let the model pick among them. To count distinct items, split into candidates in code (sentences, lines). Ask two Nouls per candidate: "is this an X?" and "is this X different from those in `items[0..i-1]`?". Sum the answers in code. Turn hex colors, RGB triples, and raw codes into a computed number or a named bucket before the model sees them. The same goes for a safety condition you can write exactly, when a miss cannot be undone: a denylist of destructive commands, a spending limit, a protected branch. Check it in code before the model runs. The model may make that decision stricter, never looser.
11. **Put questions, thresholds, weights, the provider, and the model ID in one constants module.** Those are what humans review and tune, and what changes when you change models.

## Using the numbers

- **Only picking the best option?** Use `choice` (the argmax). A confidence threshold is not needed.
- **Acting on it?** Split into three bands: act / confirm or review / escalate to a human or a reasoning LLM. Scale each threshold to what a wrong action costs. A read-only action can take a lower bar than a money-moving one.
- **Escalate only on uncertainty that feeds an action.** Report uncertainty on informational outputs, and ignore it on branches the code does not take.
- **Belongs to two categories?** Route to `choice`, and notify a second option whose probability is above about 0.25. Do not force a single label.
- **Confidence of 1.0 is normal** when all the probability sits on one option. It is not a bug.
- **Composite judgment?** Normalize each Score with `score / (len(criteria) - 1)`, weight the results in code, and keep the raw answers.
- **A fractional `score` works for thresholds and sorting only.** Do not read an exact magnitude off it by interpolating between two levels.
- **A Choice always has a winner**, even when nothing fits. Add an absolute Noul (`exists`, `stated`, `fits`) in the same request to decide whether to act at all.
- **Combine parts with the minimum** (a date from its parts, a call from its arguments). **Combine "something is wrong" flags with the maximum**, not the average.
- **Confidence is not the top probability.** It measures how peaked the distribution is, and each provider computes it its own way (Jev's formulas are in `providers/jev.md`). It is not proof of correctness: typed output guarantees the interface, not the truth.
- **Calibration belongs to one model version on one serving stack.** A probability of 0.9 can mean 95% right on one model and 75% on another. Reported calibration error (ECE) on one shared index was 0.074 for Jev 1.13, 0.024 for Nimble v2, and 0.018 for pplx-decider ([source](https://laurencemoroney.com/2026/10/02/decision-models-explained.html)). The same Nimble weights scored 0.022 behind a server that applies a fitted temperature and 0.122 on raw Ollama ([source](https://pyshine.com/Ollaya-Run-Open-Decision-Models-Locally/)). It also varies by question type: on Jev, Noul 0.012, Choice 0.086, Score 0.254 ([source](https://primeline.cc/blog/typesafe-jev-pre-registered-test)).
- **So tune every threshold on labeled data from the user.** Plot confidence against accuracy to check it, and treat every cookbook or prior-art threshold as an example only. Fit Platt scaling or isotonic regression when the curve is off. On RAGTruth, Jev at the default 0.5 cutoff trailed Opus 5 (76% vs 83%), and at a tuned 0.80 it matched (87%) ([source](https://arize.com/blog/jev-as-a-judge/)). Calibrated single answers do not make a calibrated pipeline: check the end-to-end decision too.
- **Providers round.** Jev returns every number rounded to 0.01, so Nouls, probabilities, and confidence tie often. Give any sort on them a tiebreaker, whatever the provider.
- Do not carry a threshold from a Noul to a Choice. Do not expect `P(q) + P(not q) = 1` across separate questions.
- Pin a versioned model ID when thresholds were tuned against it, and log the ID the response reports. An alias such as `jev-latest` moves on a new release.

## Changing models

On a model other than Jev, read `models/<name>.md` first (index: `models/INDEX.md`). It holds the limits, calibration, and failures people reported, which the shape files leave out.

The request often ports by changing the base URL, the key, and the model. The thresholds do not port, and "compatible" servers are less alike than they look. A conformance suite run against 8 open `/v1/systemone` servers found only 2 passing every required check. Four of them capped Choice at 26 to 128 options instead of 255. `confidence` meant top probability on some, the top-two margin on another, and one minus normalized entropy on a third ([jevcompat](https://github.com/mandu5/jevcompat)). Before you switch providers or versions in code that acts on the answers:

1. Collect labeled cases from the user's real traffic, including the hard ones near each threshold.
2. Run the old and the new model side by side on the same requests. Compare accuracy and the Brier score per question, not one overall number.
3. Re-fit every threshold on the new model's answers. Check large option lists and long states on their own: open models drop fastest there.
4. Ship behind the constants module (rule 11), log both models during a shadow period, and keep the old model ID until the new one has run on live traffic.

A worked sketch of this comparison, the field lessons from people who switched, and the benchmarks that exist are in `choosing-and-switching-models.md`.

## When an answer is wrong

Look at the exact state, questions, candidates, answers, and the code that combined them, next to what actually happened. Then name the cause before you change anything:

- **Missing evidence**: the state lacked what the question needed, or a candidate was never offered.
- **Model error**: the state held the answer. Rewrite the question (rule 5) and re-test on the same case, or route cases like it to review. If a stronger model gets it right, the fix may be the model, not the question.
- **Code error**: wrong path, inverted Noul, bad threshold, wrong combination, or a field name copied from another provider.
- **Service failure**: a timeout, a 429, or a 5xx. Handle it with the SDK's retry policy, not by rewording the question.

Known weak spots for each model are in its `models/` file and linked from its provider file.

## Common mistakes

| Mistake | Fix |
|---|---|
| One API call per question | Put all questions for one state in one request |
| Treating the top probability as confidence | Use `confidence` where the provider returns it. Noul has none: P(yes) is the answer. |
| Guessing the `score` scale | It is 0 to n-1, weighted by level probability. Check how the provider keys `legend`/`probabilities` (Jev HTTP uses strings, its Python SDK uses ints). |
| Copying field names or paths across providers | Read the provider file. Paths, envelopes, and field names differ: Clef REST (`result`), Databricks and OpenAI (Noul as `probability`), OpenAI and Perplexity (own paths), Vercel's native API (`boolean`). |
| Carrying thresholds to a new model | Re-fit them on labeled cases (see "Changing models") |
| Assuming every "compatible" model supports every primitive or limit | Check the provider file for option, level, question, and context limits |
| Numeric or vague Score levels | Use concrete situations, one dimension each |
| "Analyze this and decide what to do" | Split into atomic questions and combine in code |
| Asking the model to count, do date math, or compare hex colors | Do it in code. Ask per-item Nouls. |
| Double negatives, or "does the thing it refers to have..." | Ask directly about a named state path |
| Speculative question with no stated premise | `"If X, then ...?"` |
| Hand-rolled 429 retry loop around an SDK | SDKs retry 429/5xx with backoff. Tune their retry policy. Raw HTTP callers need their own backoff. |
| 16+ worker thread pool on one key | Use about 8 workers or fewer unless the provider documents more |
| Holistic "is this record good?" judge | Use per-field checks, one flaw per Noul |
| API key in browser code | Keep it server-side |
| A decision model as the only check before a destructive or money-moving action | Put a code rule first: a known-bad pattern blocks whatever the model says. The model judges only what the rule does not decide. |
| Hostile text in state | Decision models do not treat state as adversarial. Keep untrusted text in its own named field. Point questions at it by path. Add an injection Noul. Never let a model answer alone authorize a side effect. |
