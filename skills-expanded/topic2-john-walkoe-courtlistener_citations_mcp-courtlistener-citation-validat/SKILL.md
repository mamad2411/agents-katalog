---
name: courtlistener-citation-validator
description: Validates legal citations in documents using the CourtListener MCP to detect AI-generated hallucinations and citation errors. Use when user uploads a legal brief, motion, or document and asks to validate, check, audit, or verify case citations. Triggers on phrases like "validate citations", "check for hallucinated citations", "audit this brief", "verify case law", "find fake citations", "check citation errors", or "are these citations real". Requires CourtListener citations MCP to be connected.
metadata:
  author: CourtListener MCP
  version: 1.0.0
  mcp-server: courtlistener
---

# CourtListener Citation Validator

Validates every case citation in a legal document against the CourtListener database using a 3-tool fallback chain. Detects AI-generated hallucinations, wrong citation numbers, and completely fabricated cases.

## When This Skill Applies

- User uploads or pastes text from a legal brief, motion, or memo
- User asks to "validate", "check", "verify", or "audit" citations
- User asks if citations are real or if an AI hallucinated cases
- User asks to find citation errors in a document

## Tool Hierarchy (Always Follow This Order)

Use tools in this exact sequence. Never skip to a later tool without trying earlier ones first.

### Tool 0: courtlistener_extract_citations (DISCOVERY — run first, always)

```
courtlistener_extract_citations(text=<full document text>)
```

Runs locally — no API key, no rate limit, instant. Returns a complete census of ALL citation
types in the document:
- **case_citations** → proceed to Tool 1 for validation
- **statutory_citations** → cannot be validated; report as "not validatable"
- **law_journal_citations** → cannot be validated; report as "not validatable"
- **id_citations** → resolved to antecedents; include in report
- **supra_citations** → resolved where possible; include in report

Use `inventory["summary"]` counts to populate the top section of your validation summary.
If `case_citations == 0`, skip Tools 1–3 and report that no validatable case citations were found.

### Tool 1: courtlistener_validate_citations (PRIMARY - for case citations)

```
courtlistener_validate_citations(text=<full document text>)
```

Process each result by status code:
- **200** → Citation found. Check that the returned `case_name` matches what the document says. If it matches → ✅ VERIFIED. If names differ significantly → ⚠️ MISMATCH.
- **300** → ✅ VERIFIED (ambiguous, review clusters list)
- **404** → Citation not in database → proceed to Tool 2
- **400** → Invalid reporter format (not a real citation format)
- **429** → Overflow (250+ citations) → re-submit in smaller chunks

**For every 200/300 result:** Call `courtlistener_get_cluster(cluster_id)` to retrieve the `courtlistener_url` for inclusion in your response. Also check `citation_count` alongside `date_filed` — a supposedly landmark case with `citation_count=0` is a ⚠️ hallucination signal, **but only if the case is more than ~1 year old**. Recent decisions (< 12 months) naturally have low citation counts regardless of significance.

### Tool 2: courtlistener_search_cases (FALLBACK - for every 404)

Extract the case name from the citation string. Example: `"Alice Corp. v. CLS Bank, 573 U.S. 208 (2014)"` → `case_name = "Alice Corp v CLS Bank"`, `court = "scotus"`

```
# Attempt 1 - full name + court
courtlistener_search_cases(case_name="Alice Corp v CLS Bank", court="scotus")

# Attempt 2 - strip Inc./LLC/Corp./Ltd.
courtlistener_search_cases(case_name="Alice v CLS Bank", court="scotus")

# Attempt 3 - first party only
courtlistener_search_cases(case_name="Alice", court="scotus")

# Attempt 4 - drop court filter
courtlistener_search_cases(case_name="Alice Corp v CLS Bank")
```

Found → ⚠️ PARTIAL MATCH (note it was found by name, not direct citation lookup).
Still not found → proceed to Tool 3.

**Reporter → court mapping** (infer court from citation format):
- `U.S.` / `S. Ct.` / `L. Ed.` → `scotus`
- `F.3d` / `F.4th` / `F. App'x` → circuit court (`cafc`, `ca1`–`ca11`, `cadc`)
- `F. Supp.` / `F. Supp. 2d` / `F. Supp. 3d` → district court (`dcd`, etc.)

### Tool 3: courtlistener_lookup_citation (LAST RESORT)

```
courtlistener_lookup_citation(citation="573 U.S. 208")
```

Found → ⚠️ PARTIAL MATCH. Compare `case_name` in result against what the document claims — if they differ it is a ⚠️ MISMATCH.
Not found → ❌ NOT FOUND (likely hallucination — mark clearly).

## Output Format

Always structure your response in this exact order:

### 1. Summary Statistics

```
📊 VALIDATION SUMMARY
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
All Citations Identified:    X  (courtlistener_extract_citations)
  Case citations:            X  (validated against CourtListener)
  Statutory citations:       X  (not validatable)
  Law journal citations:     X  (not validatable)
  Id. / supra references:    X  (resolved to antecedents where possible)

Case Citation Results:
✅ Verified:                 X  (via courtlistener_validate_citations)
⚠️ Partial Matches:          X  (via fallback search)
⚠️ Mismatches:               X  (citation exists, wrong case)
❌ Not Found:                X  (likely hallucinations)
```

### 2. Verified Citations

```
✅ VERIFIED: Alice Corp. v. CLS Bank Int'l, 573 U.S. 208 (2014)
Court: Supreme Court | Filed: 2014-06-19 | Cited by: 847 later opinions
🔗 https://www.courtlistener.com/opinion/2679558/alice-corp-v-cls-bank/
```

### 3. Partial Matches

```
⚠️ PARTIAL MATCH: KSR Int'l Co. v. Teleflex Inc., 550 U.S. 398 (2007)
Found via: case name search (courtlistener_validate_citations returned 404)
🔗 https://www.courtlistener.com/opinion/145658/ksr-v-teleflex/
Note: Citation verified by case name only — confirm citation number independently.
```

### 4. Mismatches (citation real, wrong case)

```
⚠️ MISMATCH: eBay Inc. v. MercExchange, 646 F.3d 869 (Fed. Cir. 2011)
Cited as: eBay Inc. v. MercExchange (injunction standard case)
Actual case at 646 F.3d 869: TiVo Inc. v. EchoStar Corp.
🔗 Actual case: https://www.courtlistener.com/opinion/215085/tivo-v-echostar/
Note: Correct eBay citation is 547 U.S. 388 (2006). AI combined real case name with wrong citation.
```

### 5. Not Found

```
❌ NOT FOUND: DABUS v. Vidal, 985 F.3d 1234 (Fed. Cir. 2021)
Tried: courtlistener_validate_citations → 404 | courtlistener_search_cases → no results | courtlistener_lookup_citation → 404
Status: LIKELY HALLUCINATION — no record in CourtListener database.
Note: Real case is Thaler v. Vidal (wrong party name — AI used AI system name instead of inventor).
```

### 6. Risk Assessment (always last)

```
🚨 RISK ASSESSMENT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Overall Risk: [CRITICAL / HIGH / MEDIUM / LOW]

CRITICAL: 3+ citations not found OR mismatched
HIGH:     1-2 citations not found or mismatched
MEDIUM:   All found but some via fallback only
LOW:      All citations verified directly

Recommended Actions:
- Replace ❌ citations immediately
- Confirm ⚠️ MISMATCH citations point to intended cases
- Verify ⚠️ PARTIAL MATCH citation numbers independently
- Use provided 🔗 CourtListener links to manually confirm all cases
```

## Common AI Hallucination Patterns

Watch for these patterns when reviewing results:

1. **Real name + wrong number** — AI combines a real case name with a citation from a different case on the same topic
2. **Fabricated name + real number** — the number points to a real case but the name is invented
3. **Plausible case that doesn't exist** — all three tools return nothing
4. **Party name confusion** — e.g., "DABUS v. Vidal" should be "Thaler v. Vidal"
5. **Wrong court/reporter** — SCOTUS case cited as Federal Circuit, or vice versa
6. **Zero citation count on an older landmark case** — `citation_count=0` on a case claimed to be foundational is a strong hallucination signal, but only when `date_filed` is more than ~12 months ago. New decisions (< 1 year) will always have low counts regardless of importance.

## Tool Limitations

- CourtListener covers federal courts and major state appellate courts
- Best coverage for reported decisions; thinner for recent (last 6 months) or unpublished opinions
- These tools verify citation *existence*, not whether the case supports the legal argument
- Does not check if the case is still good law (use Westlaw/Lexis Shepard's/KeyCite for that)
- For state court cases, coverage varies — a not-found result is less conclusive
