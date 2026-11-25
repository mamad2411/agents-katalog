---
name: throwaway-scripts
description: >-
  For repetitive or bulk work that a short script can do in one shot, write the
  script, run it, and delete it, instead of grinding through many manual tool
  calls. Use this WHENEVER a task scales with N: renaming or transforming many
  files, extracting or reshaping data, bulk edits across a pattern, generating
  boilerplate, or any mechanical loop. Doing it by hand burns tokens and turns; a
  script does it deterministically and cheaply. Check which runtimes the system
  actually has (bun or node, python, powershell, bash), pick one that is present,
  write the smallest script that works, run it, verify, then clean it up.
---

# Throwaway scripts

Some work is mechanical and scales with N: rename 200 files, pull a field out of
50 JSON blobs, rewrite every import path, generate a table from a list. Doing that
through one tool call per item is slow and burns a lot of tokens for something a
five-line script would finish in one run. When the task is a loop, write the loop.

The rule: if a job is repetitive, deterministic, and scales with N, prefer a short
script over N manual steps. Write it just in time, run it, and remove it when done.

## When to script

- The same operation repeats over many files, rows, or items.
- The work is mechanical: no per-item judgment, just a transform or a count.
- A script expresses it more cheaply than the equivalent pile of tool calls.
- You need a deterministic, repeatable result (a sweep you can rerun and trust).

## When not to

- A one-off small edit. Just make the edit.
- A task that needs human judgment on each item.
- Something a dedicated tool already does cleanly (a search, a single
  find-and-replace). Do not script what the right tool handles in one call. This
  is `use-your-skills` and the right-tool judgment applied to scripting.

## Pick a runtime that exists

Do not assume. Check what the system actually has, then choose, just in time:

- JavaScript or TypeScript: `bun` if present (fast, no install), otherwise `node`.
- `python` for data wrangling and text.
- `powershell` on Windows, `bash` on Unix, for filesystem and glue work.

Match the language to the task and to what is installed. A two-line shell loop
beats a Python project for a rename; Python beats shell for parsing structured
data.

## Write small, run, verify

- Write the smallest script that does the job. No scaffolding, no project, no
  dependencies you do not need.
- For anything that mutates files or data, look before you leap: print what it
  would do first, or operate on a copy, then run for real. Destructive sweeps
  deserve a dry run.
- Run it and check the result actually matches what you intended.

## Clean up

The script is scaffolding, not a deliverable. When it has done its job, delete it
so it does not litter the repo or get committed by accident. Keep it only if the
user wants it as a reusable tool, in which case put it somewhere sensible and say
so. Never commit a throwaway script as a side effect.

## Before you proceed

Before grinding through a repetitive task by hand, ask: would a short script do
this in one run for fewer tokens and less time? If yes, check the available
runtimes, write the minimal script, run it, verify the output, and remove it. If
the task is small or needs judgment per item, do it directly instead.
