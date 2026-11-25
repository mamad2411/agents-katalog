---
name: recall
description: Recall memory-bank entries before acting. Use when starting a task that may have prior decisions, patterns, practices, or domains; when the user asks to /recall; or when another skill needs memory-bank context loaded.
---

# Recall

Load applicable **memory-bank** entries so this run inherits prior crystallised outcomes.

Before searching, read [../memory-bank/GLOSSARY.md](../memory-bank/GLOSSARY.md).

## 1. Frame the need

From the user task (or `/recall` argument), name which **categories** matter and any topic keywords. Default: check `decisions` plus any other category the task clearly touches.

**Done when:** the category set and search terms are explicit.

## 2. Scan banks

Search the **repo** bank (`<project>/.memory/`) first, then the **global** bank (`$HOME/.memory/`). List candidate entry paths by filename and title match; skip empty or missing roots.

**Done when:** every matching path under both roots for the chosen categories is listed (or confirmed none).

## 3. Read and follow links

Read each candidate. Follow **correlated decisions** and reopen **derived-from** paths when they change what applies. Prefer the newest **changelog** row when two entries conflict; surface the conflict to the user instead of silently picking.

**Done when:** every candidate is read or explicitly skipped with a one-line reason, and conflicts are named.

## 4. Apply

State the applicable entries in brief bullets (path + constraint). Carry those constraints through the rest of the task; do not re-litigate a **decision** entry unless the user asks to change it (then **remember** the supersession).

**Done when:** the user (and the rest of this run) can see which memory constrains the work.
