---
name: mine-chat
description: Mine a Telegram/WhatsApp chat export for trading strategies using a cheap extraction agent (Haiku/Sonnet), then have the main model (Fable) codify, backtest and file the strategy into the strategy-brain vault. Use when the user says /mine-chat <export-path> or asks to analyze a trading chat export.
---

# mine-chat: two-tier chat mining (cheap extractor -> Fable reasoner)

Argument: path to a chat export folder (Telegram Desktop `result.json` export,
or a WhatsApp `_chat.txt` folder). If missing, ask for it.

## Stage 0 — prep (mechanical, no LLM)
For Telegram exports run:
`C:/Dev/elite-backtest/.venv/Scripts/python.exe C:/Dev/strategy-brain/telegram_prep.py "<export path>"`
This writes compact chunks to `C:/Dev/strategy-brain/prep/<slug>/chunk_*.txt`.
WhatsApp `_chat.txt` files are already compact — chunk mentally by line ranges.

## Stage 1 — extraction (CHEAP model, never Fable)
Spawn ONE Agent (subagent_type: general-purpose, **model: "haiku"**; use
"sonnet" only if haiku's output proves too lossy) whose prompt is:
- Read every chunk in the prep folder (list them first).
- Extract ONLY: instruments traded; timeframes; entry rules/patterns; SL/TP
  and risk statements; named levels or indicators; explicit signals with
  numbers (entry/SL/TP); win/loss admissions; anything about session timing.
- Output a structured digest: ## Instruments / ## Rules / ## Signal format
  / ## Risk / ## Timing / ## Sample signals (max 15, verbatim) / ## Red flags.
- Forbid commentary and speculation; quote message dates for every claim.
Have the agent WRITE the digest to
`C:/Dev/strategy-brain/vault/research/mined-<slug>.md` and also return it.
For very large corpora (>40 chunks) spawn 2-3 haiku agents on chunk ranges
in parallel and merge their digests yourself.

## Stage 2 — reasoning (Fable, the main session)
1. Read the digest; codify the strategy as precise, testable rules; state
   every assumption (follow the pattern of C:/Dev/elite-backtest/RULES.md).
2. File a strategy note in `C:/Dev/strategy-brain/vault/strategies/<slug>.md`
   with machine-runnable frontmatter when the rules map onto an existing
   variant engine (see variants.py: sweep, sweep-tr, pdl-sweep, trend, orb);
   otherwise status: research and describe what new variant code is needed.
3. Backtest what is mappable (train/test split, conservative fills) and
   record the honest verdict in the note + a dated changelog line.
4. Report to the user: what the chat's strategy is, verdict, red flags
   (signal-seller patterns, martingale, undisclosed losses), next steps.

## Ground rules
- Voice messages (.ogg/.opus) are NOT transcribed by default — report the
  count and offer local Whisper transcription as a separate step.
- Never present a backtest of a signals channel as validation of the
  channel's *claimed* results; test the rules, not the marketing.
