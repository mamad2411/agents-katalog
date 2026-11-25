---
name: remember
description: Remember durable outcomes into the memory-bank. Use when a decision, pattern, practice, domain fact, or session outcome crystallises; when the user asks to /remember; or when another skill needs an entry written under .memory.
---

# Remember

Write crystallised session outcomes into the **memory-bank**. Brief and precise beat complete transcripts.

Before writing, read [../memory-bank/GLOSSARY.md](../memory-bank/GLOSSARY.md) and [../memory-bank/ENTRY-FORMAT.md](../memory-bank/ENTRY-FORMAT.md).

## 1. Classify

Name the **category** (`decisions`, `patterns`, `practices`, `domains`, `sessions`) and **scope** (repo default, or global only when explicitly cross-repo). Choose a kebab-case filename for the meaning — or the existing entry to update.

**Done when:** category, scope, bank root path, and target filename are fixed.

## 2. Gather neighbours

Under that bank root, scan the category (and `decisions/` when linking) for entries that share the meaning. Collect **correlated decisions** and **derived-from** paths from this session's evidence.

**Done when:** update-vs-create is decided, and every correlated link or `_none_` is ready.

## 3. Write the entry

Create the category folder if missing. Write or update the file using [ENTRY-FORMAT.md](../memory-bank/ENTRY-FORMAT.md): headers first, body second, **changelog** last (append a dated row).

**Done when:** the file exists at the chosen path with all required sections and a changelog row for this change.

## 4. Keep the glossary honest

If this run added a **category** or **bank root**, update [GLOSSARY.md](../memory-bank/GLOSSARY.md) in the same turn. Otherwise leave it.

**Done when:** on-disk layout matches the glossary category table.

## 5. Report

Tell the user the absolute path written, category, scope, and one-line summary.

**Done when:** the user can open the entry path.
