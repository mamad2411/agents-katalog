---
name: intent
description: "Propose an intent: what must become true. Runs the Majordomus capability intents.propose with the text you type as its `statement`."
argument-hint: "<statement>"
disable-model-invocation: true
---
<!-- GENERATED FILE — DO NOT EDIT DIRECTLY
     Source: apps/majordomus-cli/src/capability/builtin/intents.rs; regenerate with `majordomus generate`
     Generator: majordomus-cli 1.2.0 -->

# Propose an intent: what must become true

Invoke the Majordomus capability `intents.propose`. Its `statement` is the text below, whole and verbatim — do not rephrase, shorten, translate or complete it:

$ARGUMENTS

If no text was given, ask for it and stop; do not invent one.

- With the Majordomus MCP server attached, call the tool `majordomus_intent_propose` with that text as `statement`.
- Otherwise run `majordomus intent propose` from the repository root, giving that text as its `statement` (`majordomus intent propose --help` shows how).

Call it once. It changes the repository: if the call is refused or its outcome is not known, report that as it is and do not try again by another way.

Then report what the capability answered, as it answered.

What `intents.propose` does, what it accepts and what it answers are defined once, in its declaration: `majordomus capabilities describe intents.propose`, or the MCP tool's own description. This file only makes it reachable by name and says nothing the declaration does not.
