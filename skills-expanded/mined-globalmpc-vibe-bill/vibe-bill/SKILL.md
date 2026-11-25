---
name: vibe-bill
description: Estimate what this app will cost to run at 100 / 1k / 10k / 100k users (LLM APIs, Supabase, Vercel, Clerk, Resend, Stripe), flag code patterns that inflate the bill, and render a shareable receipt image plus a report. Use when the user asks what their app will cost to run, about API/hosting/LLM bills at scale, or runs /vibe-bill.
argument-hint: "[path] [--no-questions]"
allowed-tools: Bash(node ${CLAUDE_SKILL_DIR}/scripts/vibe-bill.mjs *)
---

# vibe-bill

Estimate the running cost of the app in the project directory and produce a receipt plus a report. Follow steps 0 to 6 in order.

## 0. Setup and hard rules

- `P` = the first token of `$ARGUMENTS` that does not start with `--`, else `.`.
- `V` = `node ${CLAUDE_SKILL_DIR}/scripts/vibe-bill.mjs`. Every command is exactly `V <cmd> P ...`: unquoted, one command per Bash call, no `&&`, pipes or redirects.
- Unattended = `$ARGUMENTS` contains `--no-questions`, or AskUserQuestion is unavailable.

Rules:
- Never Read, Grep, Glob-with-content or `cat` a file whose basename starts with `.env`. Only `.env.example`, `.env.sample` and `.env.template` are allowed.
- Every Grep call sets `type` (js, ts, py, php) or a `glob` of source files such as `**/*.{ts,tsx,js,jsx,mjs,cjs,py,php}`.
- No Bash except the `V` commands.
- Env variable names come from `P/.vibe-bill/out/detect.json` only. Never print or write env values.
- Write files only under `P/.vibe-bill/`. Never edit `pricing.json` or the bundle.
- Never invent dollar amounts. The scripts compute every number; you only copy their output.

## 1. Detect

Run `V detect P`, then Read `P/.vibe-bill/out/detect.json` (services, unknown_services, flags).

**No LLM service in detect.json?** The app may still call an LLM through a proxy, gateway or CLI that leaves no SDK or env name. Run the Grep from step 3.1 once.
- No call sites: continue; the bill will have no LLM line.
- Call sites found and attended: make one AskUserQuestion: "Which AI provider's models does this app use?" with options `OpenAI`, `Anthropic`, `Google AI`, `OpenRouter` (`multiSelect: true`). Read `P/.vibe-bill/config.json` if it exists, write it back with `llm_providers` set to the lowercase ids picked (`openai`, `anthropic`, `google`, `openrouter`) and every other key unchanged (new file: `{"schema":1,"llm_providers":[...]}`), then run `V detect P` again and Read detect.json.
- Call sites found and unattended: stop. Tell the user: `LLM calls found but no provider detected. Add "llm_providers": ["anthropic"] (or openai, google, openrouter) to .vibe-bill/config.json and rerun.` Do not produce a receipt without the LLM line.

## 2. Questions (one batch)

Skip this step when unattended (go to step 3).

1. Run `V questions P`. If `questions` is empty, go on.
2. Make exactly one AskUserQuestion call with one question per entry:
   - `question` = `prompt`, plus ` (` + `note` + `)` when `note` is not null.
   - `header` = `Model`, `Provider` or `Plan` by `type` (model, base_url_provider, plan_tier). If two get the same header, append ` 2`.
   - `options` = each option's `label` and `description`. `multiSelect: false`.
   - Do not add an "Other" option yourself. Do not ask a question that has fewer than 2 options.
3. Map each picked label back to its option `value`. A free-text "Other" answer: for a model, map it to an OpenRouter id `provider/model`; for a provider, to a lowercase provider id. If it cannot be mapped, leave it unanswered.
4. Write `{"<question id>": "<value>"}` to `P/.vibe-bill/out/answers.json`, then run `V answer P P/.vibe-bill/out/answers.json`.

Unanswered or overflow questions are assumed from defaults by step 5 and asked on the next run.

## 3. Code analysis: write `P/.vibe-bill/out/usage.json`

1. Find LLM call sites with Grep: `chat.completions.create|responses.create|messages.create|generateContent|generateText|streamText|generateObject|streamObject|embeddings.create|->chat\(\)->create|->responses\(\)->create|->messages\(\)->create|api\.openai\.com|api\.anthropic\.com`, plus the client names found in the code. Read each call site and its caller to find what triggers it.
2. Write the file:

```json
{
  "schema": 1,
  "call_sites": [
    { "service": "openai", "feature": "chat reply", "file": "app/chat/page.tsx", "line": 42,
      "trigger": "per_message", "est_input_tokens": 800, "est_output_tokens": 300, "notes": "sends full history" }
  ],
  "traps": [
    { "id": "keystroke_llm_call", "call_site": 0, "fix": "Call the API on submit or debounce typing" }
  ],
  "per_user": { "emails_per_month": 4, "storage_mb": 20 }
}
```

Rules:
- `service` must be an LLM service listed in detect.json (`openai`, `anthropic`, `google`, `openrouter`). Max 100 call sites.
- `feature`: at most 40 characters from `[A-Za-z0-9 ,'()&+-]`, starting with a letter or digit. No `/`, `.` or `_`.
- `fix`: at most 100 characters from `[A-Za-z0-9 ,;:'()&+%-]`, starting with a letter or digit. No `/`, `.` or `_`.
- `file` is relative to the project; `line` is optional. `notes` is free text and never leaves the file.
- Tokens: `est_input_tokens` is (system prompt + typical user text + included context) characters divided by 4. `est_output_tokens` is `max_tokens` if set, else about 300. Omit a value you cannot tell (defaults 800 / 300). For embeddings or other non-chat calls use `est_output_tokens: 0`.
- `per_user`: only `emails_per_month` (email sends per user lifecycle) and `storage_mb`. Omit both when the code gives no evidence.

Triggers (one per call site):
- `per_message`: the user sends a chat message or form.
- `per_keystroke`: onChange or onInput handlers.
- `per_page_view`: the call runs when a page loads.
- `per_render`: the call sits in a component body or effect that re-runs on render.
- `per_poll`: a timer or interval.
- `per_cron_run`: a scheduled job.
- `per_webhook`: an incoming webhook.
- `per_signup`: once per new user.

Traps (`call_site` is the index into `call_sites`; no duplicate id + call site):
- `keystroke_llm_call`: the LLM is called from a keystroke handler.
- `render_loop_llm_call`: the call re-runs on every render.
- `unbounded_history`: the whole chat history is sent on every turn.
- `top_model_for_trivial_task`: a flagship model does a simple job (classify, summarize, rewrite).
- `no_prompt_cache`: identical requests repeat and nothing caches them.
- `public_ai_endpoint_no_rate_limit`: an unauthenticated route calls the LLM with no rate limit.
- `aggressive_polling`: an LLM call on a short timer.
- `image_optimization_on_uploads` (`call_site: null`): every upload is resized into many variants.
- `select_all_egress` (`call_site: null`): queries select all columns or rows without limits.
- `files_in_db` (`call_site: null`): files or base64 blobs are stored in database rows.

## 4. Unknown services

Run `V price P`. It prints `pending` hints and `cached` entries.

- If `pending` is empty, do not search: cached prices are reused.
- For each pending hint (at most 5 per run): WebSearch `<vendor> pricing`, then WebFetch the vendor's own pricing page. Record the published pay-as-you-go unit price, or the entry paid plan's base fee, and one usage guess `units_per_user_per_month` with a one-line reason that you tell the user. `source_url` is the page the number came from, `checked_at` is today (YYYY-MM-DD).
- If you find no usable number, set `base_monthly`, `unit`, `unit_price_usd` and `units_per_user_per_month` all to null.
- Write `P/.vibe-bill/out/price-input.json`:

```json
{ "replicate": { "hints": ["env:REPLICATE_API_TOKEN"], "name": "Replicate", "source_url": "https://replicate.com/pricing",
  "checked_at": "2026-11-11", "base_monthly": 0, "unit": "image", "unit_price_usd": 0.004, "units_per_user_per_month": 5 } }
```

  The id is lowercase letters, digits and `-`. `name` is at most 30 characters from `[A-Za-z0-9 &+-]`. `unit` is lowercase, such as `image` or `sms`. The three unit fields are all set or all null. Do not include `unverified`.
- Then run `V price P P/.vibe-bill/out/price-input.json`.
- If web tools are denied or unavailable, skip. The report lists the service as not priced.

## 5. Calculate and render

If the user asks for specific user counts (for example "1M users"), first Read `P/.vibe-bill/config.json` if it exists, then write it back with `assumptions.tiers` set to a list of 1 to 6 whole numbers (the user's counts, plus 10000 and the usual ones only if they asked for them) and every other key unchanged. If it does not exist, write `{"schema":1,"assumptions":{"tiers":[...]}}`.

Run `V calc P --no-questions`, then `V render P`. Use `--live-prices` on calc only if the user asks for fresh prices.

If calc or render reports a validation error, fix the named field in `usage.json` or `price-input.json` and retry, at most 2 times. Then stop and show the error.

## 6. Reply (under 8 lines)

- Copy the two summary lines that `render` printed (`total at ...` and `top fix: ...` or `top risk: ...`) verbatim.
- `Receipt: P/.vibe-bill/out/receipt.png` (use `receipt.svg` if render printed `receipt.png skipped`) and `Report: P/.vibe-bill/out/report.md`.
- If `P/.vibe-bill/config.json` has `assumed` keys: `Some answers were assumed; edit .vibe-bill/config.json or rerun /vibe-bill to answer them.`
- If unverified web-searched prices were used: `Unverified prices (web search): <names>; check the report.`
- No env names, no code, no other dollar figures.
