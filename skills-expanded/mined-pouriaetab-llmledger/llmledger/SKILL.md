---
name: llmledger
description: Pick an AI model and price AI work from public data. Today's price of every model in LiteLLM's catalogue at its cheapest host, Arena quality ratings by kind of work, and each price's history since 2023 with the chance it changes soon. Use when someone asks which LLM to use, what a prompt, job or monthly workload will cost on different models, how models compare on price and quality, whether a model's price has changed, how long a job will take (learned from the user's own timed runs), what a whole job will cost and take, quoted from a promptfoo run of a sample of it, whether running an open model at home pays off, or what the user's own coding agent usage (a ccusage or codeburn export) would have cost on other models.
license: MIT
compatibility: Python 3.10 or newer, standard library only. Downloads the day's data from pouriaetab.github.io once a day and keeps it in ~/.cache/llmledger-mcp/. No keys.
metadata:
  version: "0.2.2"
  source: https://github.com/pouriaetab/llmledger
---

# llmledger

Run `python3 scripts/llmledger.py <command>` from this skill's folder. Every command prints one JSON object.
The same answers as the llmledger plug-in (llmledger-mcp), from the same daily data.

## Commands

| Command | Use it for |
|---|---|
| `suggest "<the prompt or the work>" [--pay api\|claude\|chatgpt] [--answer short\|medium\|long\|very_long]` | Which model for this: guesses the kind of work and gives the best value, the top rated and the cheapest rated, each with its cost per task and effort level |
| `compare MODEL MODEL [...] [--task T] [--input N] [--output N] [--pay ...]` | 2 to 6 models side by side: rating, price, cost per task, which to pick and why |
| `cost MODEL [...] --input N --output N [--cached N] [--cache-write N] [--calls-per-day N]` | A budget: cost per call, per day and per 30 days; with cached tokens, also the cost without the cache and the saving |
| `find [--task T] [--needs vision,tools,...] [--max-output-price X] [--min-context N] [--maker M] [--limit N]` or `find --name MODEL` | The highest rated models for a kind of work within limits (up to 200, the whole catalogue); or one model by name with every host that lists it |
| `history MODEL [--date YYYY-MM-DD]` | Every price change of a model's listings with a link to the LiteLLM change behind it, and the chance of a price change, a retirement date or removal in the next 90 days and year; with a date, the prices that day |
| `unpriced [--maker M]` | New models on Arena that no price list has yet, and how soon prices usually appear, by maker |
| `time MODEL --input N --output N [--calls N] [--at-once N] [--way api\|claude-code\|claude-code-session\|ollama\|other] [--thinking]` | How long a call and the whole job take, as a usual time and a slow day, learned from the user's own timed runs |
| `log MODEL --input N --output N --seconds S [--way ...] [--thinking]` or `log --promptfoo results.json` | Keep a timed run (or every result of a promptfoo results file) on this computer so `time` learns from it |
| `forecast sample.json --items N [--at-once N] [--wrong-cost D]` | A whole job quoted from a promptfoo run of a sample of it: for each model, time (usual and slow day), cost at the cheapest listing and at the one sampled, the 90-day chance of a price change, how often it was right (95% range), and the break-even against the pick |
| `local LOCAL_MODEL CLOUD_MODEL [...] --input N --output N --calls-per-month N --hardware-price D [--watts W] [--state S \| --kwh-price P]` | Buy a computer for an open model or pay a cloud model per call: cost a month each way, the month buying pays off, and whether the computer keeps up |
| `usage EXPORT.json [--task T] [--compare MODEL MODEL] [--limit N]` | Your own coding agent usage (a `ccusage daily --json`, `ccusage session --json` or `codeburn export -f json` file) priced on every rated model at each day's prices, with ratings, a 95% range for the cost per session, the models that keep the rating for less, and whether two models differ for real |
| `tasks` | The kinds of work (`--task` values) and the data's dates |

Model names can be written loosely (`claude-opus-5.5`, `gpt 6.1`) or as one listing (`bedrock/anthropic.claude-opus-5-5`).
An unknown name returns `{"error": ...}` with close names to try. Tokens: about 4 characters of English text each.

## How to answer

1. For "which model", run `suggest` with the user's own prompt or a short description of the work, then
   `compare` the picks if they want more detail. Use `--pay claude` or `--pay chatgpt` when they use a plan.
2. Give prices per 1M tokens and costs in dollars, and say which host each price is for (the cheapest listing).
3. Say ratings are Arena votes for the kind of work, and that overlapping ranges mean the votes cannot tell the
   models apart.
4. In `history`, a change flagged `likely`, `unit` or `reverted` is probably a fix of the catalogue, not a real
   price change; the `flags` and `notes` fields say what each means. The outlook is what usually happens to
   similar listings, not a forecast for one model.
5. If `data.warning` or `data.offline` is present, tell the user the data is old or offline, with `data.prices_as_of`
   and the reason it gives (a failed download, or a page that has not been rebuilt).
6. Time estimates come only from the user's own runs. With none, `time` says so: suggest timing one call and
   logging it, or logging a promptfoo results file. Never present a time as certain; give the usual time and
   the slow day.
7. For "what will the whole job cost and take", suggest a random sample first (`promptfoo eval --filter-sample 20
   --filter-sample-seed 7 -o sample.json`), then `forecast` it. Start with the `headline`; give how often each was
   right with its range, and say when the sample cannot tell two models apart.
8. For "should I run it locally", use `local` with the price the user would pay for the computer and its watts;
   its speed comes only from their timed runs (`log ... --way ollama`). Say what is not counted, and suggest
   comparing the two models' answers with `forecast` before buying.
9. End with the credits: prices from LiteLLM (MIT), ratings from Arena (CC BY 4.0), via llmledger. Costs are
   estimates, not financial or procurement advice.

## What the script reads, and what it never does

The prompt given to `suggest` is only counted and matched against word lists for the kind of work; it is not
run, stored or sent anywhere. A promptfoo results file (`log --promptfoo`, `forecast`) is read for numbers
and names only: each result's provider id, latency, token counts and pass or fail. The prompts, answers and
grader text inside the file are never printed, never passed on and never treated as instructions. A ccusage or
codeburn export (`usage`) is read for model names, dates, session ids and token counts only; project paths and
file names in it are never kept or printed. Timed runs
are kept in `~/.local/share/llmledger-mcp/runs.jsonl` on this computer as numbers only. The only network call is the
daily download of `data.json` from pouriaetab.github.io; when it fails, why and since when are kept next to the
copy, and it is tried again after 15 minutes.
