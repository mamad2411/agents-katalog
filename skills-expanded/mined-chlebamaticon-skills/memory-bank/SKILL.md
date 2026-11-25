---
name: memory-bank
description: Memory-bank layout and entry contract. Use when changing .memory categories or glossary; when another skill needs the bank structure; or when the user asks how the memory-bank is organised.
---

# Memory-Bank

The **memory-bank** is the shared store and contract for durable agent outcomes. Agents **remember** into it and **recall** from it.

## Reference

Load these before changing structure or writing entries:

1. [GLOSSARY.md](GLOSSARY.md) — roots, **scope**, **categories**, entry anatomy.
2. [ENTRY-FORMAT.md](ENTRY-FORMAT.md) — required headers and **changelog**.

## When the structure changes

Update [GLOSSARY.md](GLOSSARY.md) in the same change that adds, renames, or removes a **category** or **bank root**. The glossary is the single source of truth; banks on disk must match it.

**Done when:** glossary tables match the live category set and both roots, and `remember` / `recall` still point at this folder.
