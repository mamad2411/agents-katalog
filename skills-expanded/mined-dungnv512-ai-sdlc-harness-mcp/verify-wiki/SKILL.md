---
name: verify-wiki
description: Confirms each factual claim in a wiki artifact is quotable from docs/raw/ sources with line references. Reports three outcomes (content-confirmed, range-only unchecked, failed) and never stamps verified while unverified claims remain.
---

# Verify Wiki Skill

Close the evidentiary loop on OKF wiki artifacts: confirm each factual claim is actually present in the cited raw source. This skill prevents fabricated contracts and endpoints from shipping, and prevents false-positive verification reports.

## When to Use

- A wiki artifact is marked `unverified` (has no `verified` key in frontmatter) and you are ready to confirm its claims
- An artifact has been recompiled and needs verification before publication
- You need to trust an artifact's claims enough to cite them in code or specifications

Do NOT use this to create a wiki artifact (`digest-wiki` for that), to answer questions (`query-wiki` for that), or to import raw sources (`pull-confluence` / `pull-jira`).

## The verification pipeline

### 1. Run the mechanical gate

```bash
python3 -sS bin/okf-verify.py <artifact-path>
```

This checker parses footnote citations and verifies them with different rigor depending on citation form:

- **Quoted claims** (text in `"..."`) — must find 75%+ of tokens within ±5 lines of cited line, AND all distinctive tokens (numbers, long identifiers) must be present. Reports drift magnitude. Exit non-zero if NOT FOUND.
- **Range citations** (no quotes) — checks if claim's tokens actually appear somewhere in the cited range. If range exists but tokens are absent, reports RANGE-ONLY (not verification). Exit non-zero if FAILED (range out of bounds, source missing).

**Three outcomes reported:**
- `CONTENT-CONFIRMED (drift ±N)` — quoted claim with 75%+ match found N lines away
- `CONTENT-CONFIRMED (range)` — range citation where claim tokens appear in cited range
- `RANGE-ONLY` — range exists but claim tokens absent; this is **not verification**
- `FAILED` — genuine missing claim, missing source, or out-of-bounds

**Do not proceed past this step if the checker returns any FAILED or RANGE-ONLY outcomes.** These are findings, not warnings.

### 1b. Run the coverage gate (REQUIRED)

```bash
python3 -sS bin/okf-coverage.py <artifact-path>
```

This checker measures whether the artifact actually covers what its sources contain. It extracts mechanically-detectable API/spec surface from cited raw sources (endpoints, error codes, status codes, field names, requirement IDs) and reports:

- `MISSING` — element in source but absent from artifact (coverage defect)
- `UNSOURCED` — element in artifact but in no cited source (fabrication)

Both MISSING and UNSOURCED are failures (exit non-zero). **Do not proceed if coverage exits non-zero.**

**Why both checks?** `okf-verify` measures *precision* (are claims true?) while `okf-coverage` measures *completeness* (are we hiding requirements?). Neither implies the other:
- An artifact can pass verify 100% while only covering 30% of source spec (omitting requirements)
- An artifact can have high coverage while containing a few false claims in the margins

**Critical rule:** An artifact with **0% coverage** on any element type (e.g., no status codes mentioned when source has 12) is an integrity problem, not a minor gap. The artifact deliberately hides surface area. This must be fixed or declared in `coverage_exclusions` with a reason.

If there are elements you deliberately exclude, declare them in artifact frontmatter:
```yaml
coverage_exclusions:
  - element: ELEMENT_NAME
    reason: "Intentionally omitted because..."
```

Excluded items do not cause failure and are reported separately.

**Do not proceed if exit code is non-zero.** Exit non-zero means MISSING or UNSOURCED elements exist that are not explicitly excluded.

### 2. Interpret the results

Read the per-claim output carefully:

- **CONTENT-CONFIRMED** — The claim is verified. Move to step 3.
- **RANGE-ONLY** — The line range exists in the source, but the claim's text does not appear in that range. Either:
  - The citation is wrong (points to wrong section); find the actual line where the claim appears, or
  - The claim is not in the source; remove it, or mark it explicitly as `[INFERRED]` in the prose (per OKF §5.3 `confidence_markers`) and record which source *should* have had it.
- **FAILED** — The claim or range is missing entirely from the source. Same treatment as RANGE-ONLY: fix the citation, remove the claim, or mark inference.

### 3. For any drift in quoted claims

If a quoted claim shows `drift +2` or higher, the citation line is far from where the text actually appears. The claim is still verified (found), but the line number should be updated in a future recompile for cleaner verification history. Not required to stamp verified, but recommended.

### 4. Never stamp verified without both gates

Only after **both** gates pass completely:
- `okf-verify.py` exits 0 (all claims CONTENT-CONFIRMED or inferred)
- `okf-coverage.py` exits 0 (no MISSING or UNSOURCED elements)

Then, and only then, stamp verified:

```yaml
verified:
  - { by: claude/haiku-4-5, at: 2026-07-28T10:30:00Z }
```

Per OKF §7 (actor convention):
- `<producer>/<version>` for agent runs, e.g. `claude/haiku-4-5`
- `human:<id>` for person sign-off, e.g. `human:ahormati`
- `process:<id>` for automated process, e.g. `process:finance-nightly`

**Critical rule per OKF §5.3**: 
- A `verified` entry with `human:` yields **human-reviewed** trust tier
- Without `human:`, it yields **machine-confirmed**
- An artifact with any RANGE-ONLY or FAILED claim stays **unverified** — never stamp `verified` on an unchecked artifact. The whole point of the field is reader trust; a false verification is worse than none.

### 5. Commit the updated artifact

Update only the live artifact's frontmatter, not the `.recompiled.md` sidecar:

```bash
# Edit docs/wiki/<topic>/<topic>-overview.md in place
# Add/update the `verified` list in the frontmatter (only if all claims CONTENT-CONFIRMED)
# Leave everything else (body, sources, generated.at) unchanged
git add docs/wiki/<topic>/<topic>-overview.md
git commit -m "verify: [WIKI-ID] — all claims content-verified (X/45 confirmed)"
```

## Understanding the three outcomes

### CONTENT-CONFIRMED

The claim's text is genuinely present in the source. For quoted claims, this means 75%+ of the claim's tokens are found within ±5 lines of the cited line, AND all distinctive tokens (numbers, long identifiers) are present. For range claims, it means the claim's tokens appear somewhere in the cited range.

### RANGE-ONLY (not verification)

The line range exists in the source file (so the source was ingested and the line numbers are valid), but the claim's key terms do not appear in that range. This is **not verification**. It means:
- Either you cited the wrong section (the claim is elsewhere in the source), or
- The claim is not in the source (it's synthesized from across multiple sources or inferred).

Count RANGE-ONLY as a blocker, same as FAILED. Do not report an artifact as "verified" if any claims are RANGE-ONLY.

### FAILED

The source file is missing, the range is out of bounds, or the quoted claim genuinely cannot be found. Exit from the verifier is non-zero. Investigate and resolve before stamping verified.

## Self-test the verifier

Before trusting the checker on real artifacts:

```bash
python3 -sS bin/okf-verify.py --self-test
```

Exit 0 means the checker itself is working. It covers:
- Quoted claims with 75%+ tokens + rare tokens → CONTENT-CONFIRMED
- Quoted claims with <75% tokens → FAILED
- Quoted claims missing a rare token (number) → FAILED
- Range with claim tokens in range → CONTENT-CONFIRMED
- Range with NO claim tokens in range → RANGE-ONLY (not verification)
- Range with out-of-bounds → FAILED

If it fails, do not use the checker — report the failure.

## Example run and interpretation

```bash
$ python3 -sS bin/okf-verify.py docs/wiki/auth/auth-overview.recompiled.md
  ✓ [biz-gate] [quoted] CONTENT-CONFIRMED (drift +1): 16/16 tokens
  ~ [dependencies] [range] RANGE-ONLY: lines 19-19 exist, claim tokens (0/22) not found
  ✓ [problem-access] [quoted] CONTENT-CONFIRMED (drift +1): 17/17 tokens
  ...
23 content-confirmed, 20 range-only (not verified), 2 failed
```

Result: **Do not stamp verified yet.** The artifact has 20 RANGE-ONLY claims (unchecked sections) and 2 FAILED claims. These must be resolved first:
- For RANGE-ONLY: find the actual line where the claim appears, or remove/mark inference
- For FAILED: same action

Once all claims are CONTENT-CONFIRMED or explicitly marked [INFERRED], rerun the verifier to confirm, then stamp verified.
