---
name: distill
description: Knowledge pipeline (LLM-Wiki). Capture a URL, file, or pasted text as an immutable raw source with brain_distill, compile it into a knowledge page, update index and log, propagate facts, and give a Brain Impact verdict. Use for "/distill <source>", "--refresh <page>", "--lint".
---

## /distill — capture → compile → propagate

```
/distill <url|path>             web page, GitHub repo, YouTube, PDF, local file
/distill --text "<pasted>"      pasted content (ask $user for a source name)
/distill --file "<title>"       file the answer you just gave as a knowledge page
/distill --refresh <slug>       recompile one page from its raw sources
/distill --lint                 wiki health: brain_status → knowledge
```

### Step 1 — Capture (tool)

`brain_distill(source=<url|path>)` or `brain_distill(source="<name>", text="…")`. It writes `vault/raw/YYYY-MM-DD-<slug>.md` with frontmatter (source, title, author, published, sha256, words, `compiled_into: []`). `status: exists` → already captured, stop unless `--refresh`. A `note` about a thin capture → open the page in the browser, copy the text, call again with `text=`.

### Step 2 — Locate the topic

Read `vault/knowledge/_index.md`; `brain_recall("<title> <main concepts>")` for prior discussion. One page per topic, never per source. Merge into an existing page when the topic exists.

### Step 3 — Compile (you are the compiler)

Read the whole raw file. Tell $user the 3–5 takeaways and which page changes; silence or ok → write.

Page `vault/knowledge/<slug>.md`: frontmatter (`type: knowledge`, `owner`, `domain`, `status`, `updated`, `last_validated`, `sources: [raw/…]`), then `# Topic`, `## Core Concepts`, `## Practical Rules`, `## Common Mistakes`, `## Decision Framework`, `## Contradictions & Open Questions`, `## Brain Impact`, `## Sources`. Date every perishable claim `(as of YYYY-MM, source)`. No claim without a raw source. Then set `compiled_into:` in the raw file's frontmatter (the only edit a raw file ever gets).

### Step 4 — Index and log

Add or update the row in `_index.md` (`| [[page]] | domain | updated | summary |`); append `## [date] ingest | <title> → <pages>` to `_log.md`.

### Step 5 — Propagate

3–5 operational facts: `brain_remember(kind='fact', domain=…, source='raw/<file>')`. New relationships: `kind='relation'`. A change in how you work: `kind='pattern'`. One summary line: `brain_remember(kind='note', extra={section: 'What We Discussed'})`.

### Step 5b — Brain Impact (hard rule)

Does this change a rule, skill, hook, script, or tool? Rules gap or technology gap? Context cost in tokens (prefer script → skill → rule line)? Verdict: **ADOPT** (reversible, zero or negative context cost → do it now, log it), **PROPOSE** (needs $user: adds context, a dependency, or money → one line with the cost), **NO-OP**. Write it into the page and the log line.

### Report

```
Distilled: <title> (<source>)
Raw: vault/raw/<file> (<n> words)
Pages: <created|merged> <page>
Facts: <n> · Relations: <n>
Brain impact: <ADOPT what | PROPOSE what (cost) | NO-OP>
Open: <contradictions or follow-ups, or "none">
```

### Rules

Raw is immutable. One page per topic. Cite or omit. Date the perishable. Lean guard: no distill grows always-loaded context without a stated cost and $user's ok.
