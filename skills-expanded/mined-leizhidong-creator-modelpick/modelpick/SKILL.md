---
name: modelpick
description: Pick the most cost-effective model at every workflow node (coding, image, video, 3D, audio), with cost per solved task, key-aware fallbacks, and the exact API connection.
whenToUse: Before choosing a model, generating media, starting a long coding task, quoting a model price, wiring up a provider key, or when the user only has some API keys.
metadata:
  version: 0.2.0
  homepage: https://github.com/Leizhidong-creator/modelpick
---

# ModelPick

You are working with an agent that can call many models. The expensive mistake is not picking a bad model once — it is picking a frontier model for every node, or picking a model the user cannot actually call.

## When to use this skill

Call `pick_model` **once per node**, before you commit to a model:

- the user asks for an image, video, 3D asset, voiceover, music, or transcription;
- you are about to start a long coding, refactor, review, or debugging task;
- the user asks "which model should I use?", "what will this cost?", or "is there a cheaper way?";
- a task needs a capability the current model may not have (vision, 1M context, tool use, image output).

Do **not** call it on every turn or for trivial edits. One call per node is the contract.

## Workflow

1. Call `pick_model` with the node in natural language and any constraints:

```json
{ "query": "generate a stylized 3D sword for a Unity game", "optimize": "balanced", "max_cost": 0.5 }
```

2. Read `recommendation.slug`, `recommendation.costPerTask`, `recommendation.why`, `recommendation.connection`, and `recommendation.availability`.

3. **Check availability before promising a run.** If `recommendation.availability.ready` is false:
   - use `availability.bestAvailable` (the best model whose key exists) as the runnable fallback,
   - name the missing env var (`recommendation.availability.missing`),
   - never claim you can call a model you have no key for.

4. If the deliverable has multiple stages, call `plan_workflow` instead of guessing:

```json
{ "goal": "30-second product launch video for a coffee brand", "optimize": "cost" }
```

5. Before calling the provider, use `recommendation.connection` (or call `get_setup`) for the endpoint, auth header, SDK, curl example, and API model id. Never print or store the key value.

6. If the key is configured and the node is text, call `run_model` with the **compressed** node context to execute it. Pass `system`, `messages`, `context`, and optionally `output` (a fixed JSON schema); do not send the whole repository or full transcript. It returns `output`/`data`, token usage, actual cost, and a `context` report. If the key is missing, show `setupCommand` / `setupUi`; never ask for the key in chat.

7. In your final answer, state the model and the **cost per solved task**, not the token price. Example: `Tripo H3.1 — $0.21 per usable asset (1.07 expected attempts)`.

## Rules

- Never invent prices, context windows, model ids, or endpoints. Quote the tool output.
- If `recommendation.priceConfidence` is `estimated`, say so.
- If `catalog.stale` is true, mention it and suggest `modelpick update`.
- Prefer `optimize: "cost"` for drafts, bulk work, and internal tools; `"quality"` for customer-facing hero assets; `"balanced"` when unsure.
- Use `open_weights: true` when the user needs self-hosting, data residency, or no vendor lock-in.
- If the user has a private/self-hosted endpoint, tell them to run `modelpick add-model my-model.json`; it becomes a candidate without forking.
- Do not call a provider you have no key for. Show the setup block and ask the user to add the key.

## Fallback (no MCP)

```bash
npx -y github:Leizhidong-creator/modelpick pick "generate a 3D game asset" --json
npx -y github:Leizhidong-creator/modelpick pick "refactor this repo" --available --json
npx -y github:Leizhidong-creator/modelpick plan "product launch video" --json
npx -y github:Leizhidong-creator/modelpick show tripo-h3.1 --json
npx -y github:Leizhidong-creator/modelpick run "explain this function" --model gpt-6.2-sol --json
```

The JSON has the same shape as the MCP tool.

## Second opinion from a judge / decision model

If the user wants a second opinion, or the top two candidates are close:

1. Call `get_decision_packet` with the same query. It returns `allowedSlugs`, `candidates`, and a self-contained `prompt`.
2. Send `prompt` to any judge/decision model the user trusts.
3. Call `pick_model` again with `verdict` set to the judge JSON.

A verdict can only reorder the shortlist by two positions; it cannot add a model or override a hard constraint. Do not invent a verdict.

## Your own eval

If the user has pass/fail data, run `modelpick eval evals.json --json`. It reports observed pass rate, a Wilson 95% interval, and cost per solved task. Do not treat a small sample as a ranking change.
