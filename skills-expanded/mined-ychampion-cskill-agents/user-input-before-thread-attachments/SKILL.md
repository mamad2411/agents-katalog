---
name: user-input-before-thread-attachments
description: "Resolve user-input attachment triggers before running later thread-safe attachment builders so dependent state is in place."
metadata:
  author: ychampion
---

# SKILL: User Input Before Thread Attachments
**Domain:** attachment-pipeline
**Trigger:** When attaching contextual artifacts in response to user input, run that work first so any derived triggers exist before later attachment builders execute.
**Source Pattern:** Distilled from reviewed attachment-pipeline ordering and derived-trigger dependency implementations.

## Core Method
Treat user-input-driven attachment producers as dependencies for the broader attachment phase. Start by collecting the attachments that inspect user text directly, such as file mentions, MCP references, or other explicit user-specified artifacts, and wait for that set to finish. Only then should the second-stage thread-safe attachment builders run, because they may depend on triggers or metadata harvested from the first phase. This ordering prevents downstream attachment builders from running too early against incomplete state.

## Key Rules
- Build the user-input attachment group first, including everything that inspects raw user text or explicit user references.
- Wait for the entire first-phase attachment group to complete before starting second-phase attachment logic.
- Only once the user attachment future settles should you start the second-stage attachment list (queued actions, time-based context, memory lookups, and similar follow-on builders).
- Keep the dependency notes close to the ordering boundary so future maintainers do not accidentally reorder the pipeline.

## Example Application
If a request mentions files and also triggers a secondary memory lookup, resolve the file mentions first and wait for that work to complete. Only then run the dependent memory attachment builder so it sees the full set of requested paths.

## Anti-Patterns (What NOT to do)
- Do not launch the second-phase attachment builders before the user-input phase finishes; doing so lets dependent builders execute with empty or partial triggers.
- Do not assume derived trigger state will “fill in later”; the pipeline must wait on the user-input phase to preserve the dependency ordering.
