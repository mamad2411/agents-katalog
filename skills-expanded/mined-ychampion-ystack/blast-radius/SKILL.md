---
name: blast-radius
description: >-
  Before a change ships, find what it can break outside the diff, and prove the riskiest spot is safe
  by running code rather than arguing it. Use for "blast radius", "what could this break", "is this
  safe to merge", "who else uses this", before changing a shared function, type, config key, file
  format, API route, CLI flag or default, and before deleting or renaming anything.
---

# Blast radius

A diff shows what changed. It doesn't show who depended on the old behaviour. This skill finds those
dependents, sorts them by risk, and settles the riskiest one with a real run.

## When it applies

- A change touches something other code reads: a function signature or return value, a type, a
  default, an error it throws, a config or env key, a file or wire format, a route, a CLI flag, a
  database column, an event name.
- Something is deleted, renamed or moved.
- Someone asks "is this safe?" and the honest answer is "probably".

Skip it for changes nothing else can observe: a private helper's internals with unchanged behaviour,
comments, tests only.

## Procedure

### 1. Name the behaviour change, not the code change

Write one line per observable difference, old → new. "Renamed `parse` to `parseConfig`" is a code
change; "`parse` no longer exists; `parseConfig` throws on an empty file where `parse` returned `{}`"
is two behaviour changes. Everything after this step works from these lines.

### 2. Find every consumer, including the ones grep misses

Static references first: callers, importers, subclasses, type users. Then the dynamic ones, which are
where breakage hides:

- names held as strings: config keys, route paths, event names, feature flags, reflection, `getattr`,
  dependency-injection tokens, SQL column names;
- data already on disk or in flight: saved files, caches, queues, database rows, cookies, other
  services' payloads, written in the old format;
- other repos, scripts, CI jobs, cron jobs, docs and READMEs that show the old usage;
- generated code and the generator's templates.

For a wide search, split it by area across parallel subagents; locating is cheap work, so use a cheap
model for it if your setup routes by task. Each returns paths and line numbers, not opinions.

### 3. Sort each consumer into one of three

| Bucket | Meaning |
| --- | --- |
| unaffected | It doesn't use the changed behaviour. Say why in a few words. |
| safe | It uses it, and you can point at the line that makes it fine. |
| unknown | It uses it and you can't show it's fine by reading alone. |

Be strict: "the tests pass" doesn't move a consumer to safe unless a test covers that consumer's path.

### 4. Prove the riskiest unknown by running something

Pick the unknown whose failure would cost most (data loss, a broken deploy, a silent wrong answer
beats a loud crash). Write the single fact that would make it safe, then run code that shows it:

- call it with old-format data and the new code;
- run the consumer's own test, or write a ten-line script that exercises the path;
- replay a saved real input, request or file through old and new and diff the outputs;
- for a migration, run it on a copy of real data and count rows before and after.

One run beats a page of reasoning. If the fact turns out false, you found the bug before users did.
Repeat for the next unknown while the cost of being wrong justifies it.

### 5. Report

```
Change: <the behaviour lines from step 1>

| Consumer | Bucket | Evidence |
| path:line | safe | reads only .name, unchanged |
| path:line | PROVEN SAFE | ran <command>: <result> |
| path:line | unknown | <why it can't be shown; suggested guard> |

Verdict: ship / ship with <guard> / don't ship until <fix>
```

An unknown you couldn't settle stays visible in the report with a suggested guard (a compatibility
shim, a migration, a feature flag, a loud error instead of a silent default). Never round an unknown
up to safe.

## Rules

- The proof is a command and its output, quoted. "I checked and it's fine" is not a proof.
- Data outlives code. Old-format data on disk is the most-missed consumer.
- If the change is a deletion, search for the name as a string too.
- With ystack's `verify` mod installed, the step-4 run counts as the real check it asks for.
