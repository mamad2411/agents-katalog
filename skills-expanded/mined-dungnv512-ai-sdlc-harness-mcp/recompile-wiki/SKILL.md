---
name: recompile-wiki
description: Refreshes a stale docs/wiki/**/*.md artifact by re-reading and synthesizing its sources, stamping generated/at to mark the recompile. Always writes to a .recompiled.md sidecar first. Prefers quoted citations (verifiable) over range citations (which must have tokens in the range to verify).
---

# Recompile Wiki Skill

Refresh a stale `docs/wiki/**/*.md` artifact by re-reading its `upstream_refs` sources and synthesizing the body faithfully. Write to a sidecar file for human review before overwriting the live artifact. This is an LLM-curated recompile, not a regex extraction — the artifact's analysis and structure must be preserved through the refresh.

When writing citations, **strongly prefer quoted citations** (verifiable). Range citations are acceptable only when:
1. The citation describes a structural container (a whole table, a whole section)
2. The claim's distinctive terms actually appear somewhere in the cited range
3. Verification via `bin/okf-verify.py` confirms the tokens are present

## When to Use

- `bin/okf-freshness.py` reports an artifact as "stale by provenance"
- User explicitly asks to refresh a specific artifact
- An upstream source has been re-ingested and the wiki artifact needs to catch up

Do NOT use this to create a new artifact (`digest-wiki`), to answer questions (`query-wiki`), or to import raw sources (`pull-confluence` / `pull-jira`).


## Step 0: Generate Citation Index with okf-cite.py

Before writing any artifact body or citations, generate a deterministic citation index:

```bash
python3 -sS bin/okf-cite.py --footnotes docs/wiki/TOPIC/TOPIC-overview.md > /tmp/citations.txt
```

Output is a list of ready-to-paste footnotes: `[^cite-N]: SOURCE-ID line L — "claim"`

**Why this matters:** Three consecutive recompile attempts failed because agents hand-wrote line numbers, resulting in:
- Fabricated line numbers (off by 10s of lines)
- Section headings cited instead of actual content
- Wide ranges containing HTML markup that failed token checks

okf-cite deterministically extracts all citable elements, picks the most specific line (prefers table cells, short lines), and formats claims for okf-verify compatibility. **Use the emitted index as your citation reference.** Do not hand-write line numbers.

**Workflow:**
1. okf-cite emits: `[^cite-5]: CONF-XX-nnnnn line 319 — "BIO TOO LONG"`
2. You write prose: "An error, BIO_TOO_LONG[^cite-5], indicates…"
3. You paste the footnote into your artifact
4. okf-verify confirms the citation is CONTENT-CONFIRMED

If an element is missing from okf-cite output, it means it doesn't appear in the cited sources—skip it.

## Step 1: Read Sources and Build Coverage Map

## Citation Strategy — Quoted First, Range Last

The verifier `bin/okf-verify.py` reports three outcomes:

- **CONTENT-CONFIRMED** — claim verified in source (quoted with 75%+ tokens, or range with tokens found)
- **RANGE-ONLY** — range exists but claim tokens absent; NOT verification
- **FAILED** — source missing or claim genuinely not found

An artifact carrying any RANGE-ONLY or FAILED claims cannot be marked verified. Therefore:

1. **Prefer quoted citations** — they are verifiable and account for most content-confirmed claims
2. **Use range citations sparingly** — only for structural containers where no specific quotable claim applies
3. **Every range citation must have its tokens in the range** — if the range exists but claim terms are absent, the verifier reports RANGE-ONLY and the artifact is blocked

## Citation Forms — Two Machine-Checkable

Every footnote MUST use one of these forms. The verifier routes by form and applies appropriate rigor.

### Form 1: Quoted Claim (Preferred)

Use whenever the artifact states a specific, quotable fact from the source:

```markdown
Users register via a four-step wizard with age verification (≥16 years).[^us1-outline]

[^us1-outline]: CONF-SN-405143554 line 578 — "wizard 4 bước, tuổi ≥ 16"
```

Rules:
- Description text must start with a `"` (opening quote)
- Cite the **line containing the quoted text** itself, not the heading above it
- Verifier searches ±5 lines; drift up to ±5 is acceptable
- Requires: 75%+ of tokens AND all rare tokens (numbers, identifiers) present

**Form requirement:** Exact tokens from your claim must appear in source.

### Form 2: Range/Descriptive Citation (Structural Only)

Use only for structural references where the claim's tokens actually appear in the range:

```markdown
US1 contains 44 acceptance criteria spanning four steps.[^us1-ac]

[^us1-ac]: CONF-SN-405143554 lines 578-707 — US1 Acceptance Criteria (four steps)
```

Rules:
- Description text starts without a `"` (no opening quote)
- Must be a valid line range in the raw file
- **The claim's distinctive tokens must appear somewhere in the cited range**
- Verifier checks: range exists AND tokens found in range
- If tokens are absent from range, outcome is RANGE-ONLY (not verified, blocks artifact)

**Do not use range as a shortcut.** If you cannot verify that tokens appear in the range, use a quoted citation instead or remove the claim.

## Critical Rules

1. **NEVER cite a section heading as quoted text.**  
   Bad: `line 19 — "### Business Value"`  
   Good: `line 20 — "actual content text"`

2. **Every range citation is an assertion that tokens are in the range.**  
   Bad: `lines 2740-2768 — "email not found… redirect"` (if those words don't appear in lines 2740-2768)  
   Good: Same tokens, same lines, but only if `bin/okf-verify.py` confirms they're there

3. **Verify before handing off.**  
   Before moving the sidecar to live, run `bin/okf-verify.py` and iterate until all outcomes are CONTENT-CONFIRMED or the artifacts are explicitly marked [INFERRED]. A sidecar with RANGE-ONLY or FAILED claims is not ready.

## When Each Form Is Right

| What you're citing | Form | Example |
|---|---|---|
| Specific sentence, claim, or requirement | **Quoted** | `line 19 — "OAuth2/OIDC + PKCE per NFR-004"` |
| A number, date, code value | **Quoted** | `line 85 — "24 hours expiry"` |
| A feature or concept | **Quoted** | `line 130 — "wizard 4 bước"` |
| **Full table** (can't pick one line) | **Range** | `lines 42-127 — Capability table` (only if "Capability" or similar tokens appear in 42-127) |
| **Whole section** (structural container) | **Range** | `lines 3391-3463 — US6 (Logout) definition` (only if "Logout" or similar tokens appear in range) |
| Anything else | **Quoted** | Quote the actual text |

**The bias is toward quoted.** If you can quote it, quote it.

## Steps

### 1. Identify the artifact and its sources

```bash
# Locate the artifact file
ls -l docs/wiki/<topic>/<name>-overview.md

# Read its frontmatter
head -50 docs/wiki/<topic>/<name>-overview.md

# Find its upstream_refs (list of sources.json keys)
python3 -c "
import re
with open('docs/wiki/<topic>/<name>-overview.md') as f:
    text = f.read()
    match = re.search(r'upstream_refs:\s*\n((?:\s*-\s*.+\n)*)', text)
    if match:
        print('upstream_refs:')
        print(match.group(0))
"
```

### 2. Check staleness and gather the sources

```bash
# Check if the artifact is stale
python3 -sS bin/okf-freshness.py

# For each upstream_ref, verify the raw file exists and is up-to-date
jq '.CONF_SN_123456' sources.json | head
# Confirm: raw_file path exists, stale flag is "current"
```

### 3. Re-read the sources and synthesize the body

Open each raw file and re-synthesize the artifact's body faithfully. Read the upstream page as the primary source of truth. Keep the artifact's existing structure (headings, tables, code blocks) unless the source contradicts it.

**Attach footnotes with correct form** (quoted or range, per §Citation Forms above). For every factual claim pulled from the source:
- If quoting specific text verbatim, use **quoted form** with the line containing that text
- If describing a section structure, use **range form** — but only if the claim's tokens actually appear in that range

### 4. Write to sidecar and preview

```bash
# All output to <artifact>.recompiled.md, never overwrite the live file yet
cat docs/wiki/<topic>/<topic>-overview.recompiled.md | head -50
diff -u docs/wiki/<topic>/<topic>-overview.md docs/wiki/<topic>/<topic>-overview.recompiled.md | head -100
```

### 5. Verify with both okf-verify.py AND okf-coverage.py — MANDATORY

Run **both** checkers on the recompiled artifact. Recompile is incomplete until both exit 0.

```bash
# Test citations for precision
python3 -sS bin/okf-verify.py docs/wiki/<topic>/<topic>-overview.recompiled.md

# Test completeness against sources
python3 -sS bin/okf-coverage.py docs/wiki/<topic>/<topic>-overview.recompiled.md
```

**Example output from okf-verify:**
```
  ✓ [claim-1] [quoted] CONTENT-CONFIRMED (drift +0): 8/8 tokens found in line 42
  ✓ [claim-2] [range] CONTENT-CONFIRMED: 5/9 tokens found in lines 100-150
  ~ [claim-3] [range] RANGE-ONLY: lines 85-90 exist, but 0/5 tokens found in range
  ✗ [claim-4] [quoted] FAILED: claim not found within ±5 lines

content-confirmed: 23
range-only (not verified): 2
failed: 1
total claims: 26
```

**Do not proceed if okf-verify exits non-zero.** Non-zero exit means there are RANGE-ONLY or FAILED claims:

- **RANGE-ONLY** — range exists but claim tokens are not there. Either:
  - Find the actual line(s) where tokens appear and cite that instead, or
  - Change to quoted form if a specific line has the content, or
  - Remove the claim
- **FAILED** — claim is not in source. Remove it or mark [INFERRED] (and record which source should have had it)

**Iterate until okf-verify exits 0.** Then run okf-coverage:

```bash
python3 -sS bin/okf-coverage.py docs/wiki/<topic>/<topic>-overview.recompiled.md
```

If coverage shows MISSING or UNSOURCED items:
- Add content to cover missing elements (e.g., missing status codes, requirement IDs, endpoints, error codes)
- If elements genuinely don't apply to this artifact, declare them in `coverage_exclusions` with a reason
- Recompile and re-check both tools

**The recompile is not done until both okf-verify exits 0 AND okf-coverage exits 0.** Making fewer claims must never be a way to pass coverage — cover the elements honestly or exclude them with stated reasons.

Only then move to step 6.

### 6. Move to live artifact and update generated.at

```bash
# Once verified and manually reviewed, move sidecar to live
cp docs/wiki/<topic>/<topic>-overview.recompiled.md docs/wiki/<topic>/<topic>-overview.md

# Update generated.at in frontmatter to mark the recompile timestamp
# Format: ISO 8601, e.g., 2026-07-28T10:30:00Z
```

### 7. Commit

```bash
git add docs/wiki/<topic>/<topic>-overview.md
git commit -m "refactor: recompile WIKI-ID from latest sources (okf-verify exit 0, okf-coverage exit 0)"
```

## Example: profile-api-overview.recompiled.md

The live `docs/wiki/profile/profile-api-overview.md` shows 58.5% coverage because it aggregates 19 endpoints across API pages but only claims 18 items, omitting 34 status codes and 3 endpoints that exist in its sources. When recompiling, every such omission must be either:
1. **Added to the artifact** with proper citations, or
2. **Declared in `coverage_exclusions`** with a reason (e.g., "deprecated endpoint", "client never encounters this code")

Recompiling to 9.1% coverage by dropping more claims is not a fix — it's a failure. Both gates must exit 0 before declaring the recompile done.

## Citation-checking tools

Before committing:
- `bin/okf-verify.py` validates footnote citations against source text
  - Reports: CONTENT-CONFIRMED, RANGE-ONLY, FAILED
  - Exit non-zero if any RANGE-ONLY or FAILED (artifact is unverified)
  - Only use quotes where tokens are actually present
  - Only use ranges where tokens are actually in the range
- `bin/check-links.sh` validates all file paths (not line accuracy)
- `bin/okf-freshness.py` checks if sources have drifted

If verification reports RANGE-ONLY or FAILED, fix the citations and re-run. An artifact with unverified claims cannot be marked verified per OKF §5.3.
