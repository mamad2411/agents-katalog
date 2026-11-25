---
name: live-runs
description: Rules for any step that starts a real agent CLI (claude, codex, agy, opencode) or a model outside the test suite, such as re-recording fixtures or checking a change by hand. Read it before the first call.
---

# Live runs

Tests never call a model: they replay recordings and use the fakes in `crates/testkit`. A live run is only for recording a CLI's output or checking something by hand, and it spends the plan of whoever is logged in to that CLI.

## Before the first call

- **Ask.** Start a CLI with a prompt only when the person you work for asked for this run.
- **Use the cheapest model, checked today.** List what each CLI offers now (`codex debug models`, `agy --output-format json models`, Claude Code's model aliases) and compare prices. A newer model is often the cheaper one. The recording script's choices are a starting point, not a promise:
  - Claude Code: `--model haiku --effort low`
  - Codex: `-m gpt-6-luna -c model_reasoning_effort="low"`
  - agy: `--model gemini-3.8-flash-low --effort low`
  - A local model server: a model that's already installed. Never pull, delete or unload one.
- **Set one spending cap for the whole job.** For an Argonauts crew run, set `limits.spend_per_run` at or below what's left of it, so the run pauses itself. Add up what each run spent and stop at the cap.

## While it runs

- **Work only in throwaway git repos** outside this repository, never in this repo or a real project.
- **Give Argonauts a scratch home:** point `ARGONAUTS_HOME` at a new temp folder, never at a real `~/.argonauts`.
- **Never read credentials or tokens,** or a CLI's session, history or stats files.
- **Driving an interactive CLI in a terminal driver:** turn its vim mode off for that process, check its bottom line before you type, and stop at any sign of a history search. A key typed into a history search can resend an old prompt.

## After

Say what ran, on which models, and what it cost. Anything you keep from it follows `recording-a-cli`.
