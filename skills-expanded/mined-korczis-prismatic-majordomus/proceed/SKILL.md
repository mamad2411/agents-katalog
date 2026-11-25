---
name: proceed
description: "Proceed: the next step, as one work order. Runs the Majordomus capability proceed.step with the text you type as its `intent`."
argument-hint: "<intent>"
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: apps/majordomus-cli/src/capability/builtin/proceed.rs; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Proceed: the next step, as one work order

Invoke the Majordomus capability `proceed.step`. Its `intent` is the text below, whole and verbatim — do not rephrase, shorten, translate or complete it:

$ARGUMENTS

If no text was given, call it without `intent`; do not invent one.

- With the Majordomus MCP server attached, call the tool `majordomus_proceed_step` with that text as `intent`.
- Otherwise run `majordomus proceed step` from the repository root, giving that text as its `intent` (`majordomus proceed step --help` shows how).

Call it once and report what it answers.

Then carry the order out, once: when `done` is true, report the reason and stop. Otherwise announce `report` on the board with `peers.announce`; run `do` with its `input` exactly as given (an order repeated over the same state names the same idempotency key, so it is one execution); start each `fan_out` item in a worker of its own, on the model and effort the item names; and step again at `next_due_at`, with the same intent, until the order is done.

What `proceed.step` does, what it accepts and what it answers are defined once, in its declaration: `majordomus capabilities describe proceed.step`, or the MCP tool's own description. This file only makes it reachable by name and says nothing the declaration does not.
