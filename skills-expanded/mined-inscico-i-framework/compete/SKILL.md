---
name: compete
description: Stage-3 companion for the I-Framework. Research the competitive landscape with live web search and build a sourced product comparison matrix in Product/competition.md, then read off the whitespace, the table-stakes, and where rivals beat you. Optionally invoked by /innovate; can also run standalone to refresh the matrix.
allowed-tools: Read, Write, Edit, Glob, WebSearch, WebFetch, AskUserQuestion, Task
---

# /compete — competitor research & product comparison matrix

You replace the founder's *assertion* of differentiation with *sourced evidence*. You research real competitors on the live web and render a comparison matrix that grounds the UVP and the innovation-vs-implementation classification.

**Live web research carries hallucination and staleness risk. Two non-negotiables:** (1) every factual cell traces to a source URL; (2) anything you can't source is marked `?` and listed for the founder to verify. Never present an unsourced guess as fact.

## Procedure

### 1. Load context
Read `Product/intent.md` (the problem, target user, and the **status quo / DIY alternative**), `Product/ideation.md` (the bet), and `Product/innovation.md` (the **UVP elements — UVP-1, UVP-2… become the must-have rows** of the matrix). If `innovation.md` is missing, ask the founder for the differentiators before proceeding.

### 2. (Optional) seed
Ask if the founder already knows key rivals. Accept a seed list — but still search for the ones they *don't* know about. Unknown competitors are often the most useful finding.

### 3. Discover competitors (web search)
Search the live web from several angles: the problem/category, "alternatives to <known tool>", "<category> tools/software", "<rival> vs", review roundups. Classify what you find into **direct**, **indirect / adjacent**, and the **status-quo / DIY** alternative (pulled from intent.md — often a spreadsheet, a manual process, or "nothing"). Shortlist the **3–5 most relevant** rivals so the matrix stays readable.

### 4. Research each rival (fan-out)
For thoroughness, spawn one subagent per shortlisted rival via the Task tool. Each gathers: positioning, key capabilities, pricing, target segment, strengths, weaknesses — **and returns source URLs**. Use `WebFetch` to read product/pricing pages directly rather than trusting search snippets.

### 5. Verify & source
Every factual claim cites a source. For each capability you can confirm from a source, mark the cell `✓` / `~` / `✗`. For anything you cannot source, mark it `?` and add it to the verification list. Marketing pages overstate — prefer docs, pricing pages, and third-party reviews over a vendor's own superlatives.

### 6. Build the matrix
Rows = the **UVP dimensions** (UVP-1…n) + the key **table-stakes** + **≥1 dimension a rival is strong on**. Columns = **Us** + each shortlisted rival + **Status quo (DIY)**. Cells: `✓` strong · `~` partial · `✗` absent · `?` unverified.

### 7. Honesty guardrail (enforce)
If the **"Us" column is `✓` on every row, STOP and push back** — that is a cherry-picked marketing matrix, not analysis. Require at least one row where a rival matches or beats you (add the dimension where they're genuinely strong). This is the competitive analog of the "everything is innovation" red flag. Call it out explicitly if the founder resists.

### 8. Read off the implications
- **Whitespace** — rows where no rival (or only the DIY) is strong → the opening. Map these to UVP ids.
- **Table-stakes** — rows where *everyone* is `✓` → these capabilities should be classified **implementation** downstream.
- **Threats** — rows where rivals beat us → risks to close or concede.

### 9. Write `Product/competition.md`
Use the structure from the plugin's `templates/competition.md`: scope, per-rival profiles **with sources**, the comparison matrix, the whitespace/threats read-out, and a **Confidence & verification** section listing every `?` cell plus the **snapshot date**.

### 10. Feed back & hand off
Summarize, for `/innovate` and `/classify`: which capabilities are table-stakes (→ implementation) and which whitespace items map to which UVP id (→ innovation). When classification runs next, this matrix is the **evidence behind each `classification_rationale`**.

Remind the founder: `competition.md` is a **point-in-time snapshot from public sources** — verify the `?` cells and refresh it as rivals evolve. It's an optional companion artifact: it *deepens* the market/value & moat burndown but is not itself a Stage-3 gate.
