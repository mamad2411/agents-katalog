---
name: proof-engine
description: >
  Create formal, verifiable proofs of claims with machine-checkable reasoning.
  Use when asked to prove, verify, fact-check, or rigorously establish whether
  a claim is true or false — mathematical, empirical, or mixed. Trigger phrases:
  "is it really true", "can you prove", "verify this", "fact-check this",
  "prove it", "show me the logic". Do NOT use for opinions, essays, or
  questions with no verifiable answer.
license: MIT
metadata:
  author: Yaniv Golan
  version: "1.45.0"
compatibility: >
  Requires Python 3, `requests`, and the `proof-citations` PyPI package
  (`pip install proof-citations` — the scripts/ entries are thin shims
  over it). Optional: `pdfplumber` (PDF citations), `sympy` (symbolic math).
  Outbound HTTP needed for Type B (empirical) proofs. Works on Claude Code,
  ChatGPT, Cursor, and other AI coding environments.
---

# Proof Engine

LLMs hallucinate facts and make reasoning errors. This skill overcomes both by offloading all verification to **code** and **citations**. Every fact is either computed by Python code anyone can re-run (Type A) or backed by a specific source, URL, and exact quote (Type B).

Produces four outputs: a re-runnable `proof.py` script, a reader-facing `proof.md`, a `proof_audit.md` with full verification details, and a `proof_narrative.md` plain-language narrative.

## Setup

The bundled `scripts/` are thin shims over the `proof-citations` PyPI package, which carries the real verify/fetch/normalize implementations. Install it before running any Type B proof: `pip install proof-citations`. A `requirements.txt` next to this file lists the same dependency for hosts that auto-install. If you see `ModuleNotFoundError: No module named 'proof_citations'`, the scripts will now raise an actionable error pointing at this install command — run it and retry.

### Beyond the bundled scripts: structured citation verification

For empirical proofs that cite identifier-bearing sources (PMID, DOI, arXiv, …), the `proof-citations` package ships higher-level APIs the bundled `scripts/` shims don't expose. Reach for these when the citation has a structured identifier AND the claim makes specific bibliographic assertions (journal, year, volume, DOI). They catch the "real paper, forged journal/year" fraud class — sometimes called metadata-chimera fraud — that pure quote-on-page verification can't see:

- **`verify_citation(url, quote, fact_id, expected_metadata={...})`** — combined quote-on-page + metadata-chimera check in one call. The same flow `scripts/verify_citations.py` already does, plus a per-field metadata comparison against the authoritative registry (NCBI E-utilities for PMIDs, Crossref for DOIs, etc.). Result dict gains a `metadata_result` key with the per-field verdict; top-level `status` continues to reflect the quote-on-page outcome only.
- **`verify_citation_record((type, value), expected)`** — pure metadata-check, no page fetch. Useful when you have the identifier but no specific quote to verify, or when you want to audit a bibliography without re-checking every quoted passage.
- **`proof-citations verify-records --input refs.json` CLI** — batch metadata audit over a list of references. The canonical entry point for manuscript / reference-list audits.

When the URL has no structured identifier (e.g., a generic blog page), `metadata_result["status"]` is `"skipped_no_structured_identifier"` — OG-extraction from arbitrary pages is too noisy to compare against claimed bibliographic fields.

See the [`proof-citations` README on GitHub](https://github.com/yaniv-golan/proof-engine/blob/main/packages/proof-citations/README.md) (or the PyPI page at <https://pypi.org/project/proof-citations/>) for the full API, the registered identifier types, and worked examples. See [`references/scripts-api.md`](references/scripts-api.md) for signatures.

## Gotchas

The highest-value lessons from field testing, grouped by area. Read before writing any proof code.

### By proof type

| Proof type | What to read |
|---|---|
| Empirical (any Type B fact, including Type S proofs with B-type corroboration) | All subsections below |
| Pure math (Type A only) | Skip "Citation handling" and "Source behavior & fetch failures". In "Methodology pitfalls," skip the `verify_extraction()` / `data_values` item. |
| Absence of evidence (Type S, no Type B corroboration) | Skip "Citation handling". In "Source behavior & fetch failures," only the blocked-domains item applies (search URLs can also be blocked). Pay particular attention to "Absence claims need search documentation" under "Verdict semantics." |

### Citation handling

- **Handle Unicode in citations**: Real web pages use en-dashes, curly quotes, ring-above vs degree, non-breaking spaces. `verify_citations.py` handles this automatically.
- **WebFetch/WebSearch return summaries, not verbatim text** — Never use text from WebFetch/WebSearch directly as the `quote` field in `empirical_facts`. Use these tools to identify sources, then obtain verbatim quotes via Python `requests.get()`, browser-captured `snapshot`, or Wayback archive. See [environment-and-sources.md](${CLAUDE_SKILL_DIR}/references/environment-and-sources.md) for the full workflow. If a citation returns `partial`/`not_found` on a source you know contains the finding, suspect paraphrasing — obtain raw page text and update the quote.
- **Quotes must be VERBATIM, never paraphrased**: The `quote` field in `empirical_facts` must be an exact substring copied from the source page — not recalled from memory, rephrased, condensed, or "cleaned up." If the page says "16 study participants" do not write "Sixteen participants." Paraphrased quotes are the #1 cause of citation verification failures (14 of 25 in field testing). When in doubt, copy a shorter exact substring rather than a longer paraphrased one. Workflow: fetch the URL via `requests.get()`, find the relevant sentence in the response, copy it character-for-character into `quote`.
- **PDF sources need snapshots**: When citing a PDF, use your native PDF reading (or PyMuPDF/pdfplumber) to extract the text during Step 2. Copy the verbatim quote and include the full extracted text as `snapshot` in `empirical_facts`. Without a snapshot, re-run verification requires `pdfplumber` to be installed — which is an optional dependency. The snapshot makes the proof self-contained.
- **Quote selection for qualitative claims**: Pick quotes that directly state the claim's core assertion, not tangential mentions. A source that says "the brain is remarkable" does not support "adult neurogenesis occurs." The quote must be specific enough that citation verification confirms the source actually addresses the claim.
- **Citation presence ≠ citation entailment**: `verify_all_citations()` confirms a quote exists on the page — not that it supports the claim's conclusion. Each Type B quote must name or describe the specific subject of the claim. A quote stating a generic principle (e.g., "falsifiability is a hallmark of science") does not entail a conclusion about a specific subject (e.g., "math washing is not valid science") without author reasoning to bridge the gap. If the bridge requires inference, document it in `operator_note` and note it as an entailment gap in proof.md's Claim Interpretation section.

### Source behavior & fetch failures

- **Handle `verify_data_values()` failures**: If `verify_data_values()` returns `found: false` for a source (common with JS-rendered pages), do not use that source's `data_values` as the primary computation input. Use a verified source as primary, and note the unverified source's data as corroborating only. If both sources fail verification, search for a third source with static HTML. A cross-check between two unverified `data_values` sources is circular — it compares your authored strings against each other.
- **Dynamic/JS-rendered sites**: Many aggregators (officialdata.org, in2013dollars.com, inflationdata.com) render page chrome via JavaScript. Live fetch gets raw HTML — data tables may be static but page titles, headings, and navigation are often JS-rendered. Quote verification on page titles commonly fails even when data is correct. Use `verify_data_values()` as the primary verification for table data; treat quote verification as a bonus, not a requirement.
- **Academic HTML degrades citation matches**: PMC and journal pages embed inline reference markers (`[1]`, superscripts) that inject noise after HTML stripping. If a real verbatim quote gets `partial` status, check whether the source is academic HTML before suspecting the quote itself. Use `snapshot` to capture clean text if needed.
- **Domains that commonly block automated fetches**: The following domains frequently return blocked, captcha, or degraded content for automated HTTP requests. Plan to use `snapshot` or `snapshot_file` for sources from these domains: `pmc.ncbi.nlm.nih.gov` (PubMed Central), `nature.com`, `link.springer.com`, `sciencedirect.com` (Elsevier), `wiley.com`, also `pubmed.ncbi.nlm.nih.gov` (use `eutils.ncbi.nlm.nih.gov` E-utilities for programmatic access). See the snapshot fallback pattern in the proof templates. The live→snapshot→Wayback fallback chain in `verify_citations.py` handles this automatically when a snapshot is provided.

  **Skip slow defaults for all-snapshot proofs**: when every citation in your proof has a snapshot and the live domain is known to block, pass `skip_live_fetch=True, oa_lookup=False` to `verify_all_citations()` — this bypasses the doomed live-fetch + OA-lookup attempts that otherwise add 30-45s per blocked fact. See [scripts-api.md "Snapshot-only fast path"](references/scripts-api.md#snapshot-only-fast-path) for the full kwarg menu (`skip_live_fetch`, `prefer_snapshot`, `oa_lookup`, `oa_lookup_budget_seconds`).

### JSON summary & FACT_REGISTRY

- **Never create pseudo-quote fields for table data**: Don't store table cell values in fields like `cpi_1913_quote: "9.883"`. If the source evidence is a table cell or numeric grid, store it under `data_values` and verify with `verify_data_values()`. The validator will reject pseudo-quote fields containing bare numeric or date literals that are parsed as evidence.
- **`FACT_REGISTRY` entries must be dicts, not strings**: B/S-type: `{"key": "source_a", "label": "..."}`. A-type: `{"label": "...", "method": None, "result": None}`. Plain strings like `{"B1": "source_a"}` crash `build_citation_detail()` which calls `.get("key")` on each entry.
- **JSON summary key is `claim_natural`, not `claim`**: The publish toolchain reads `proof_data.get("claim_natural")`. Using `"claim"` as the key silently drops the claim text from the published proof.
- **Use LaTeX delimiters for math in `claim_natural` and markdown sections**: When the claim contains mathematical notation, use `\(...\)` for inline math and `\[...\]` for display math. Write `\(\alpha_i\)` not `alpha_i`, `\(\pi^2/6\)` not `pi^2/6`. Do NOT use `$...$` delimiters — they collide with currency dollar signs in claims. Non-math claims need no delimiters. The same convention applies to proof.md, proof_audit.md, and proof_narrative.md.
- **Use `ProofSummaryBuilder` for the JSON summary**: Import from `scripts.proof_summary` — it builds v3 format with `format_version: 3`, validates against the JSON schema, and emits the `=== PROOF SUMMARY (JSON) ===` marker. See any template file for usage. The older `emit_proof_summary()` in `computations.py` is a legacy fallback that produces v2-shape JSON — do not use it for new proofs.

### Computation API

- **`explain_calc()` vs `compute_*()`**: Use named functions (`compute_percentage_change()`, `compute_age()`) when they match your computation — they self-document. Use `explain_calc()` for ad-hoc expressions. Don't wrap a `compute_*()` call in `explain_calc()`.
- **`cross_check()` mode and tolerance**: Use `mode="absolute"` for computed results that should match closely. Use `mode="relative"` for source-to-source comparisons. Tolerance heuristics for government statistics: expect 1-5% variation across aggregators due to rounding, month selection (annual avg vs December), and base-period differences. If sources disagree by more than 5%, investigate: find a third source, check if they use different base periods or date ranges, and document the discrepancy in adversarial checks. Don't silently ignore large disagreements — they may indicate one source is wrong.
- **`compute_percentage_change(mode="decline")` is for purchasing-power decline only**: It computes `(1 - old/new) * 100` — the denominator is the new value. For standard year-over-year decline, use the default `mode="increase"` with `(old_value, new_value)` — the result will be negative when new < old.
- **`parse_percentage_from_quote(quote, fact_id)` has no `pattern` kwarg**: For pattern-based extraction, use `parse_number_from_quote(quote, pattern, fact_id)` instead. The two functions have different signatures — check the Bundled Scripts table.

### Verdict semantics & claim formalization

- **Don't conflate source count with evidence strength**: 5 news articles citing the same study count as 1 independent source, not 5. For qualitative consensus proofs, check whether sources trace to independent primary research. Document the independence rationale in the cross-checks section.
- **Absence claims need search documentation**: For "no evidence exists" claims, use the Absence-of-Evidence template. Document what was searched (databases, query terms, date ranges), not just what was found. The `search_registry` structure makes this machine-checkable.
- **Don't weaken causal claims to prove them**: If the claim says X "causes" Y, you cannot redefine it to X "is associated with" Y in `operator_note` and then PROVE the weaker version. Decompose into SC-association + SC-causation sub-claims using the compound claim template. If only observational evidence exists without causal inference methods (Bradford Hill, Mendelian randomization, natural experiments), the result is PARTIALLY VERIFIED (association confirmed, causation not established), not PROVED.
- **Don't rank from point estimates when the source says they overlap**: If Our World in Data says "nuclear: 0.07/TWh, solar: 0.05/TWh" but also says "the uncertainties mean these values are likely to overlap," you cannot conclude solar is safer than nuclear. Set `uncertainty_override = True` and return UNDETERMINED.
- **Don't hardcode decisive variables**: Any variable assigned `True` or `False` that is later passed to `compare()` circumvents evidence-based verdict computation. The validator catches `*_holds` names, but other names (e.g., `rh_is_solved = False`) must also be computed from evidence. Use `compare()` or derive from `verify_*()` / `extract_*()` results.
- **Verdict qualifier suffix**: `PARTIALLY VERIFIED` and `UNDETERMINED` never get `(with unverified citations)`. Always use `apply_verdict_qualifier(base_verdict, any_unverified)` — never `verdict +=` or manual if/elif chains for the suffix. The function validates the base verdict string and only applies the suffix to PROVED, DISPROVED, and SUPPORTED.

### Methodology pitfalls

- **Don't use `int()` truncation as a cross-check**: `int(days / 365.2425) == calendar_years` is not independent — both are functions of the same input.
- **Don't restate the proof as an adversarial check**: "70 years after 1948 is 2018, and 2026 > 2018" catches nothing. Search for counter-evidence.
- **Don't call `verify_extraction()` on data_values**: It's circular. Instead, call `verify_data_values(url, data_values, fact_id)` to confirm each value string appears on the source page, then cross-check across sources (Rule 6).
- **Adversarial evidence is prose-only, not citation-verified**: Sources in `adversarial_checks` are documented as prose in `verification_performed` — they are not machine-verified by `verify_all_citations()`. For contested qualifier proofs, this means the strongest counter-evidence (e.g., independent reviews rejecting a qualifier) is only as trustworthy as the proof author's characterization. Mitigate by: (1) quoting specific findings verbatim in `verification_performed`, (2) citing the source URL so reviewers can check, and (3) using multiple adversarial sources that independently reach the same conclusion.

### Paths & imports

- **Don't inline verification logic**: Import the bundled scripts. Rewriting `normalize_text()` inline risks garbling the HTML-stripping logic.
- **Index base mismatches**: Economic data from different aggregators may use different base periods. If `cross_check()` flags a large disagreement, check whether sources use different scaling. Document the base period in source_name.
- **`PROOF_ENGINE_ROOT` uses env-var override with a walk-up + sibling-search fallback** (see [scripts-api.md](references/scripts-api.md#import-pattern) for the exact snippet). Resolution order: (1) env var if set — Binder and site-publishing tools set it explicitly; (2) walk up from proof.py's directory checking each ancestor for `proof-engine/skills/proof-engine/` (dev-repo layout) or `skills/proof-engine/` (plugin install layout); (3) bounded sibling search at each walk-up step — descends non-excluded siblings to depth 2, handling Cowork (`.remote-plugins/<plugin_id>/skills/proof-engine`), Codespaces, and other host layouts where `proof.py` and the skill sit in sibling trees; (4) raise `RuntimeError` with explicit `export PROOF_ENGINE_ROOT=...` instructions if nothing matches. Candidates must contain BOTH `scripts/verify_citations.py` AND `SKILL.md` (sentinel check makes broad descent safe). Do NOT hardcode an absolute path as the fallback — it leaks the generating agent's filesystem and breaks for every other re-runner. Copy the block from the relevant template verbatim; do not collapse, shorten, or replace with `__file__` dirname traversal.

## Reference Files

Read these on demand, not all upfront.

| File | Read when |
|------|-----------|
| [hardening-rules.md](${CLAUDE_SKILL_DIR}/references/hardening-rules.md) | **Step 3** — the 9 rules with bad/good examples |
| [proof-templates.md](${CLAUDE_SKILL_DIR}/references/proof-templates.md) | **Step 3** — read this index to choose a template, then read the specific template file it directs you to |
| [scripts-api.md](${CLAUDE_SKILL_DIR}/references/scripts-api.md) | **Step 3** — exact function signatures and import pattern |
| [research-workflow.md](${CLAUDE_SKILL_DIR}/references/research-workflow.md) | **Step 2** — recency check, academic-paper deep dives, snapshot pre-fetching, quote harvesting, verify-as-you-go |
| [output-specs.md](${CLAUDE_SKILL_DIR}/references/output-specs.md) | **Step 5** — proof.md, proof_audit.md, and proof_narrative.md structure |
| [self-critique-checklist.md](${CLAUDE_SKILL_DIR}/references/self-critique-checklist.md) | **Step 7** — before presenting results |
| [agents/theorem-grader.md](${CLAUDE_SKILL_DIR}/agents/theorem-grader.md) | **Step 7** — spawn-as-subagent prompt; required for `claim_type: "theorem"`, never for other claim types |
| [advanced-patterns.md](${CLAUDE_SKILL_DIR}/references/advanced-patterns.md) | When encountering complex quotes or table-sourced data |
| [environment-and-sources.md](${CLAUDE_SKILL_DIR}/references/environment-and-sources.md) | When facing fetch failures, paywalls, or .gov 403s |

## Bundled Scripts

Import these instead of re-implementing verification logic.

| Script | Purpose | Key functions |
|--------|---------|---------------|
| `scripts/extract_values.py` | Parse values FROM quote strings (Rule 1) | `parse_date_from_quote()`, `parse_number_from_quote()`, `parse_percentage_from_quote()` |
| `scripts/smart_extract.py` | Unicode normalization + extraction utilities | `normalize_unicode()`, `verify_extraction()`, `diagnose_mismatch()` |
| `scripts/verify_citations.py` | Fetch URLs, verify quotes (Rule 2) | `verify_citation()`, `verify_all_citations()`, `build_citation_detail()`, `verify_data_values()` |
| `scripts/computations.py` | Verified constants, formulas, self-documenting output (Rule 7) | `compute_age()`, `compare()`, `explain_calc()`, `cross_check()`, `compute_percentage_change()` |
| `scripts/source_credibility.py` | Domain credibility from URL (offline). Called automatically by `verify_all_citations()`. | `assess_credibility(url)` |
| `scripts/validate_proof.py` | Static analysis for rule compliance | `ProofValidator(filepath).validate()` |
| `scripts/proof_summary.py` | Build v3 proof.json summary (primary path) | `ProofSummaryBuilder` |

For exact function signatures, modes, and the standard import pattern, see [scripts-api.md](${CLAUDE_SKILL_DIR}/references/scripts-api.md). Read at Step 3.

## Environment

Full Type B verification requires **outbound HTTP** from Python. Fallback chain: live fetch -> snapshot -> Wayback Machine (opt-in). Type A proofs run entirely offline.

For environment-specific details (Claude Code, ChatGPT, sandboxed), paywalled sources, and .gov workarounds, see [environment-and-sources.md](${CLAUDE_SKILL_DIR}/references/environment-and-sources.md). When a source is paywalled, use `snapshot_file` (not inline `snapshot`) to keep copyrighted content out of the committed `proof.py` — see the "Handling Paywalled Sources" section in that reference.

The `agents/openai.yaml` file in this skill directory is a small UX adapter for OpenAI-hosted environments: it sets the display name, brand color, and `allow_implicit_invocation: true`. No proof logic lives there; it's purely cosmetic / discovery metadata for hosts that read it.

## Core Concepts

**Type A facts (Pure)**: Established entirely by code. The computation IS the verification.

**Type B facts (Empirical)**: Established by citation. Each MUST have: source name, working URL, exact quote. Reputable sources only.

**Type S facts (Search)**: For absence-of-evidence proofs. Each database search is documented with a clickable `search_url`. The tool confirms the URL is accessible but cannot verify the result count — that's author-reported and reproducible by a human reviewer. This weaker trust boundary is reflected in the SUPPORTED verdict (never PROVED).

**Every proof has three parts**: (1) Fact Registry — numbered facts tagged Type A, B, or S, (2) Proof Logic — a self-contained Python script, (3) Verdict — one of the levels below.

## The 10 Hardening Rules

| Rule | Closes failure mode | Enforced by |
|------|-------------------|-------------|
| 1. Never hand-type values | LLM misreads dates/numbers from quotes | `scripts/extract_values.py` |
| 2. Verify citations by fetching | Fabricated quotes/URLs | `scripts/verify_citations.py` |
| 3. Anchor to system time | LLM wrong about today's date | `date.today()` |
| 4. Explicit claim interpretation | Silent ambiguity | `CLAIM_FORMAL` dict with `operator_note` |
| 5. Independent adversarial check | Confirmation bias | Counter-evidence web searches |
| 6. Independent cross-checks | Shared-variable bugs | Multiple sources parsed separately |
| 7. Never hard-code constants/formulas | LLM misremembers values | `scripts/computations.py` |
| 8. Evidence relevance for rejection | Weak/off-subject rejection sources | `adversarial_checks` documentation |
| 9. Prose references mechanically resolvable | Hand-typed attribution hallucinations; raw tokens archived | `{{cite:...}}` markers expanded by repo tooling (dev-repo: `tools/lib/proof_cache.py` + `prose_reference_scan.py` + `cite-expand`) |
| 10. Quantifier–domain match | Sampling treated as load-bearing evidence for "for all" claims | `claim_type: "theorem"` + `template-deductive-theorem.md` + `validate_proof.py` regression-role check |

See [hardening-rules.md](${CLAUDE_SKILL_DIR}/references/hardening-rules.md) for detailed examples of each.

## Workflow

### Step 1: Analyze the Claim
Classify: mathematical (Type A), empirical (Type B), or mixed. Identify ambiguous terms. Determine what constitutes proof AND disproof. For compound claims (X AND Y, X BECAUSE Y), decompose into sub-claims. Write a brief proof strategy and share with the user before proceeding.

**Deductive theorems are a distinct branch.** If the claim is universally quantified over an unbounded (or arbitrarily-finite) domain — phrasings like *"every finite ..."*, *"for all finite-strategy ..."*, *"Let G be a finite ..."* — then sampling cannot be load-bearing; the verdict has to come from a deductive argument. Use [template-deductive-theorem.md](${CLAUDE_SKILL_DIR}/references/template-deductive-theorem.md) and declare `claim_type: "theorem"` in `CLAIM_FORMAL`. See also [Hardening Rule 10](${CLAUDE_SKILL_DIR}/references/hardening-rules.md#rule-10-quantifier-domain-match).

If the claim is an opinion or has no verifiable answer, do NOT attempt a proof. Offer a related factual claim instead.

Normative claims ("X is valid," "X is ethical," "X is proper scientific practice") that can only be operationalized by counting authorities who agree must be declined or explicitly disclosed as proxy operationalizations in `operator_note`. If the proof's supporting citations state generic principles (e.g., Popper on falsifiability) without naming the specific subject of the claim, the entailment gap must be disclosed in `operator_note` and in proof.md's Claim Interpretation section.

Guiding questions:
- Crisp true/false threshold? Extractable facts? Canonical sources? Clear disproof condition?
- If fewer than 3 are true, consider a simpler factual summary instead.
- For consensus claims, see [template-qualitative.md](${CLAUDE_SKILL_DIR}/references/template-qualitative.md).

### Step 2: Gather Facts (Both Directions)

**Use your environment's web search tool — do not rely on memory for source selection.** LLM training data has a cutoff; sources recalled from memory may be outdated. At minimum, run three core searches:

1. **The claim itself** — authoritative sources that address it directly
2. **Recent data** — latest benchmarks, studies, or statistics
3. **Counter-evidence** — sources that contradict, debunk, or criticize the claim ("[claim] debunked", "[claim] wrong", "[claim] criticism")

For the full workflow — recency check, academic-paper deep dives (follow-up authors, broader phenomenon, full-paper read, citation network), real-world demonstrations, snapshot pre-fetching, quote harvesting from rendered pages, and the `verify_citation()` pre-flight loop — read **[research-workflow.md](${CLAUDE_SKILL_DIR}/references/research-workflow.md)**.

If web search is unavailable in your environment, note this limitation in the proof audit under adversarial checks and flag that sources may not reflect the latest data.

Find at least two independent sources (Rule 6). For math claims, plan two independent computation approaches.

**Adversarial work happens once, here.** Use web search for counter-evidence — do not rely on memory. The `adversarial_checks` list in proof code records what you found — it's documentation of Step 2 research, not code that runs searches at proof execution time. Use past tense in `verification_performed` (e.g., "Searched for counter-evidence...") to make this clear.

**Adversarial sources belong in `adversarial_checks`, not `empirical_facts`.** Sources that argue *against* your proof's conclusion go in `adversarial_checks`'s `verification_performed` field; only sources that *support* your proof's conclusion go in `empirical_facts`. The placement rules:

- **Affirmative proofs** (default): sources that contradict the claim → `adversarial_checks`. Sources that confirm → `empirical_facts`.
- **Disproof proofs** (`proof_direction: "disprove"`): the adversarial direction reverses. Search for sources that *support* the claim being disproven — i.e., evidence it might be true. Sources that *reject* the claim (your proof's conclusion) go in `empirical_facts`.
- **Disproof exception — fabricated premise:** if adversarial investigation produces a verifiable rejection source (e.g., the claim's stated empirical origin is demonstrated to be fabricated or non-existent), include that finding in `empirical_facts` as a rejection source AND document the investigation in `adversarial_checks`. Dual role is fine; the test is whether the finding supports the proof's conclusion, and exposing a fabricated premise IS supporting evidence for a disproof. This also prevents adversarial citation failures from degrading the verdict via `any_unverified`.
- **Contested-qualifier claims (compound, SC1+SC2):** sources that reject the qualifier (e.g., "claims not substantiated," "allegations not verified") are adversarial to SC2 — put them in `adversarial_checks`, not SC2's `empirical_facts`. SC2 with zero `empirical_facts` is normal and expected when no independent body has confirmed the qualifier.

Do not proceed to Step 3 with fixable `not_found` or `partial` citation results — these usually mean the quote was paraphrased and can be corrected. However, `fetch_failed` from known-unfetchable sources (403, JS-rendered, paywalled) is expected — document these and proceed. The "with unverified citations" verdict exists for exactly this case.

**If a quote must be paraphrased** (e.g., the verbatim text is unwieldy or the source is paywalled and a snapshot is unavailable), declare `"verbatim": False` on the `empirical_facts` entry. The validator will warn and the proof report will note the reduced evidentiary weight. Do not omit this field silently — an undeclared paraphrase is harder to audit than a declared one.

### Step 3: Write the Proof Code
Read [hardening-rules.md](${CLAUDE_SKILL_DIR}/references/hardening-rules.md) for the 9 rules. Then read [proof-templates.md](${CLAUDE_SKILL_DIR}/references/proof-templates.md) to identify which template matches your claim type. Then read the specific template file it directs you to (e.g., `template-qualitative.md`, `template-compound.md`). Do not skip the second read — the index contains only the decision table, not the template code. **If the claim uses an epistemic qualifier** ("verified," "confirmed," "proven," "established"), **use the compound claim template** (`template-compound.md`) with the contested qualifier pattern: SC1 (provenance — do the numbers come from a credible source?) + SC2 (epistemic warrant — has the qualifier been independently confirmed?). **If the claim uses causal language** ("causes," "leads to," "promotes," "damages," "prevents"), **use the compound claim template** (`template-compound.md`) with SC-association + SC-causation sub-claims — see "Causal vs. associational claims" in the Verdicts section. For claims where the *primary* answer is absence of supporting evidence (and no authoritative sources actively debunk the claim), use `template-absence.md`. If authoritative sources actively reject the claim — even if absence language also appears — use `template-qualitative.md` with `proof_direction: "disprove"`; this produces a DISPROVED verdict rather than the weaker SUPPORTED. The proof script must be self-contained: `python proof.py` produces the full output.

Required elements:
- `CLAIM_FORMAL` dict with `operator_note` (Rule 4)
- `empirical_facts` dict (empirical proofs) or pure-math template (math proofs)
- `compare()` for claim evaluation, `explain_calc()` for computation traces (Rule 7)
- Adversarial checks with `verification_performed` field (Rule 5)
- Cross-checks from independent sources/methods (Rule 6)
- `FACT_REGISTRY` mapping report IDs to proof-script keys
- JSON summary block in `__main__` preceded by the marker line `=== PROOF SUMMARY (JSON) ===` (the marker introduces the JSON, it does not close it)

**Pre-flight citation check (before Step 4):** Run `verify_all_citations(empirical_facts, wayback_fallback=True)` interactively and inspect the results. Fix any `not_found`, `partial`, or `fetch_failed` entries. Use `closest_passage` as a diagnostic hint to locate the right region, then copy the visible rendered text from the page. Do not proceed to Step 4 with known citation failures that are fixable.

**Formalization fidelity check (before Step 4):** Re-read the natural-language claim and `CLAIM_FORMAL` side by side. Confirm each element of the natural claim is captured in the formal spec. If any aspect is narrowed, excluded, or operationalized by proxy, it must be documented in `operator_note` and the proof.md Claim Interpretation section's formalization scope note. Flag unresolvable divergences to the user before continuing.

### Step 4: Validate
Run `python ${CLAUDE_SKILL_DIR}/scripts/validate_proof.py proof_file.py` and fix issues.

### Step 5: Execute and Report
Run the proof script. Write four files: proof.py, proof.md, proof_audit.md, proof_narrative.md.

For detailed output specifications, see [output-specs.md](${CLAUDE_SKILL_DIR}/references/output-specs.md).

### proof_narrative.md — Reader-Facing Narrative

The fourth and final output file. Written AFTER proof.py, proof.md, proof_audit.md, and proof.json are complete. This is a **presentation** of the proof you already built — do not re-derive or reinterpret findings.

**Structure (all sections required, use these exact headings):**

1. Title line: `# Proof Narrative: <claim_natural>`
2. Section `Verdict` — contains `**Verdict: <exact verdict from proof.json>**` followed by 1-2 sentence hook with verdict-adapted tone
3. Section `What Was Claimed?` — plain-language restatement, why someone might care, do NOT copy CLAIM_FORMAL
4. Section `What Did We Find?` — 3-6 paragraphs walking through evidence as a story, not a table. Verdict-adapted: PROVED/DISPROVED = linear strongest-first; SUPPORTED = evidence then gaps; PARTIALLY VERIFIED = what held then what didn't; UNDETERMINED = what was tried and why insufficient
5. Section `What Should You Keep In Mind?` — mandatory caveats, edge cases, what evidence doesn't address, what surprised, limitations
6. Section `How Was This Verified?` — 2-3 sentences naming the process, with these links: `[the structured proof report](proof.md)`, `[the full verification audit](proof_audit.md)`, `[re-run the proof yourself](proof.py)`

**Constraints:**
- 200-800 words total
- No fact IDs (A1, B1, S1, etc.)
- No jargon — accessible to a general audience
- No tables — prose only
- No CLAIM_FORMAL reproduction
- Purpose-based language with explicit markdown links for formal outputs
- Verdict declaration must use the EXACT full verdict string from proof.json (including qualifiers like "with unverified citations")

### Step 6: Citation Recovery

After executing proof.py, check the citation verification output. If any citation has status `not_found` or `partial`:

1. **Diagnose:** Fetch the failing URL with `requests.get()` (not WebFetch — it returns summaries) and search the raw response text for your attempted quote. Common causes:
   - (a) WebSearch summary was paraphrased, not verbatim — the #1 failure cause
   - (b) Case mismatch (e.g., `gsm8k` vs `GSM8K`, `PaLM-540b` vs `PaLMB`)
   - (c) LaTeX/Unicode artifacts on academic pages (`$\Lambda$CDM`, MathML whitespace)
   - (d) Abstract page cited instead of full paper HTML (use ar5iv instead of arxiv.org/abs)
   - (e) Page content has drifted since you last checked — find the current wording

2. **Fix the quote:** Use `closest_passage` from the verification result as a diagnostic hint to locate the right region on the page — it shows approximately where your quote might be, but do NOT copy it directly (it uses simplified cleaning that may introduce artifacts). Instead, locate the passage on the rendered page and copy the visible text into `empirical_facts`. The verifier strips HTML tags and decodes entities before matching, so your quote should be plain text matching what a reader sees. If the page doesn't contain any relevant text (JS-rendered, paywall), try the Wayback archive (`wayback_fallback=True`) or find an alternative URL for the same source.

3. **Re-run:** Execute proof.py again and verify the citation now passes.

4. **Iterate:** Repeat until all citations are `verified`, or until you've exhausted recovery options. If a citation remains `not_found` after recovery attempts, document why in `proof_audit.md`'s Citation Verification Details (Impact field).

Do not skip this step. The difference between `PROVED` and `PROVED (with unverified citations)` is often a fixable quote mismatch, not a genuinely missing source. A 5-minute recovery loop is almost always worth the verdict upgrade.

### Step 7: Self-Critique
Before presenting results, run through the checklist in [self-critique-checklist.md](${CLAUDE_SKILL_DIR}/references/self-critique-checklist.md).

**Strict rule for theorem proofs.** When `CLAIM_FORMAL.claim_type == "theorem"`, this inline checklist is necessary but not sufficient — author self-blindness on prose and code style is documented (an external reviewer caught chatty/exploratory comments that the author and inline self-critique both missed). After completing the inline checklist, the grader rubric in [agents/theorem-grader.md](${CLAUDE_SKILL_DIR}/agents/theorem-grader.md) MUST be applied to the artifact, in one of two ways:

**Path 1 (preferred): grader as a separate subagent.** If a subagent dispatcher is available in your host (the `Agent` or `Task` tool), spawn a fresh general-purpose subagent with the grader prompt:
- **Subagent type:** general-purpose.
- **Prompt:** point the subagent at [agents/theorem-grader.md](${CLAUDE_SKILL_DIR}/agents/theorem-grader.md) plus the absolute path to the proof's working directory; tell them to read the grader prompt and return its structured report verbatim.
- **What to do with the report:** if the subagent returns FAIL on any Section A or Section B item, fix the failures and re-spawn the grader to confirm. Section C failures are strong recommendations to fix. Section D is advisory.

**Path 2 (fallback): grader inline.** If your host does not expose a subagent dispatcher (e.g., you are yourself running as a subagent and recursive dispatch is restricted, or the grader-rubric environment is constrained), execute the grader rubric inline against the artifact, with the same evidence-and-remediation discipline. State at the start of your inline grading that a subagent was unavailable. The rubric still applies; only the dispatch mechanism changes.

The strict rule is: **the grader rubric is applied for every theorem proof, no exceptions.** Whether it runs in a separate subagent or inline depends on host capabilities, not on author judgment. Path 1 is preferred because it gives the grader fresh context and reduces author self-rationalization; Path 2 is the legitimate fallback when Path 1 is unavailable, not when the author thinks the artifact looks fine.

For ANY OTHER value of `claim_type` (`"open_problem"`, `"compound_empirical"`, absent, etc.), do NOT apply the grader rubric. The inline self-critique checklist is sufficient. The grader exists specifically because canonical-citation-target theorems have a higher polish bar that author self-review reliably misses; for empirical/computation/absence proofs the inline checks are well-defined and a separate grader pass adds no marginal signal.

This is a strict IF/ELSE on `claim_type`, not a judgment call: theorem → always apply the grader rubric; everything else → never.

## Publishing

After a proof passes validation, it can be published to the site and archived as a citable research object.

> **Plugin install note.** The publishing commands below ship with the [proof-engine repo](https://github.com/yaniv-golan/proof-engine) — they are not part of the plugin/skill distribution because they're tied to the proofengine.info site infrastructure. If you generated a proof from a plugin install and want it published on proofengine.info, open a PR to the repo with the four proof artifacts; if you're hosting your own catalog, see `proof-engine-registry serve` in the [proof-engine-registry package](https://pypi.org/project/proof-engine-registry/).

**Publish to the site** (dev-repo):
```bash
python tools/proof-site.py publish <proof-dir> --site-dir site
```

**Mint a Zenodo DOI** (dev-repo; archives the proof as a citable research object; requires `ZENODO_TOKEN`):
```bash
# Build the site first so machine-readable artifacts are generated
python tools/build-site.py --site-dir site --output-dir _site --base-url / --site-url https://proofengine.info --design-md docs/DESIGN.md --hardening-rules-md proof-engine/skills/proof-engine/references/hardening-rules.md

# Mint DOI — pass --output-dir to include provenance.json, proof.ipynb, ro-crate-metadata.json
source .env
python tools/proof-site.py mint-doi <slug> --site-dir site --output-dir _site
```

The deposit includes all five proof artifacts plus, when `--output-dir` is supplied: the W3C PROV-JSON provenance chain, the Jupyter Notebook (interactive re-verification), and the RO-Crate 1.1 manifest — making the deposit a standards-compliant research object discoverable by Linked Data clients and research registries.

When the notebook is included, `doi.json` gains a `binder_url` field (`https://mybinder.org/v2/zenodo/{zenodo_id}/?filepath=proof.ipynb`) that lets anyone re-run the proof in a browser with one click. The Binder URL is printed to the console after minting.

## Verdicts

| Verdict | Meaning |
|---------|---------|
| **PROVED** | All facts verified, logic valid, conclusion follows |
| **PROVED (with unverified citations)** | Logic valid but some citation URLs couldn't be fetched |
| **SUPPORTED** | Absence-of-evidence threshold met, no counter-evidence found |
| **SUPPORTED (with unverified citations)** | Absence threshold met but corroborating citations couldn't be fetched |
| **DISPROVED** | Verified counterexample or contradiction found |
| **DISPROVED (with unverified citations)** | Counterexample found but some citations couldn't be fetched |
| **PARTIALLY VERIFIED** | Some sub-claims met threshold, others did not — Conclusion states whether each failing SC lacked evidence or was contradicted |
| **UNDETERMINED** | Insufficient evidence either way |

**Verdict establishment for deductive theorems (`claim_type: "theorem"`):** When `CLAIM_FORMAL.claim_type == "theorem"`, the verdict is established by the deductive argument written in proof.md's `## Proof` section, not by computation. Computational checks attached to a theorem proof are *implementation regression checks* — they spot-check the code that decides whether a given instance satisfies the formal hypotheses, not the theorem itself.

**Re-exposition vs. novel claim — set `attribution` honestly.** The common case in this engine is theorem proofs of *known results* (textbook theorems, classical results from the literature). For those, the artifact is a verifiable companion to a published proof — not the source of mathematical authority. Set `CLAIM_FORMAL.attribution` to a string identifying the primary source (e.g., `"Monderer & Shapley (1996), 'Potential Games,' Games and Economic Behavior 14(1), 124–143"`). The site renders this prominently next to the verdict so readers see at a glance that the result is being re-presented, not originated. The `## Proof` heading should be `## Proof (after <Author Year>)`, the `## Conclusion` should attribute the result to the cited source, and the artifact's contribution should be framed as "verifiable presentation + regression-clean implementation," not "established by us." Without `attribution`, the artifact reads as a novel claim and a careful external reviewer will hold it to that bar — a 2026-04-28 reviewer correctly flagged exactly this issue when an earlier framing of a Monderer–Shapley re-exposition implied the artifact had established the result independently.

Only omit `attribution` when the result is genuinely novel and you are confident it has not appeared in the literature. This is rare. If you are tempted to use this engine to publish a new mathematical result, prefer submitting a paper first; come back here when you want the published result archived as a verifiable companion.

**Declare `purpose` so the artifact's value-proposition is explicit.** Phase 2 Path 3 of the deductive-theorem plan adds a `CLAIM_FORMAL.purpose` field that names what the artifact actually delivers. Five values:

- **`fact_verification`** — empirical claim with citations (the bulk of the corpus). The artifact's value is verifying the fact; cite the artifact as evidence of the fact-check.
- **`computation`** — closed-form math; the computation is the proof.
- **`absence_search`** — "no published evidence that..." claims backed by reproducible search.
- **`consensus_review`** — multi-source qualitative claims.
- **`methodology_demonstration`** — theorem-shape artifacts as verifiable companions to a published result. The citation target for the *math* is the cited primary source (`attribution`); the artifact itself is citable only as evidence of the proof-engine framework's behavior on a known theorem. Always paired with `attribution`.

For theorem proofs (`claim_type: "theorem"`), `purpose` should almost always be `methodology_demonstration` — the engine cannot independently establish a "for all" mathematical claim, and the prior reviewer feedback established that artifacts overstating this are correctly rejected. The site renders the purpose label next to the verdict chip so readers see at a glance whether they are looking at a verified empirical claim, a closed-form computation, or a methodology demonstration.

If `purpose` is omitted, it defaults from `claim_type` via [`default_purpose_for_claim_type` in `tools/lib/proof_loader.py`](https://github.com/yaniv-golan/proof-engine/blob/main/tools/lib/proof_loader.py): theorem and open_problem default to `methodology_demonstration`; everything else defaults to `fact_verification`. Set explicitly to override.

See [template-deductive-theorem.md](${CLAUDE_SKILL_DIR}/references/template-deductive-theorem.md) §"What this template produces — and what it does NOT produce" and [Hardening Rule 10](${CLAUDE_SKILL_DIR}/references/hardening-rules.md#rule-10-quantifier-domain-match).

**Threshold guidance for source-counting proofs:** The default `threshold: 3` means 3 independently verified sources must confirm the claim. Never set `threshold: 1` — a single source is not consensus.

**Reducing to `threshold: 2`** is permitted only when ALL of the following are met:
1. **Domain scarcity**: Fewer than 3 independent authoritative sources exist. Document the search that established this (databases queried, terms used, why results are insufficient).
2. **Source quality adequate for domain**: Each threshold source must meet the minimum quality standard for its domain:
   - *Human/clinical studies*: n >= 30 participants (or justify smaller n for rare conditions)
   - *Physical/mathematical*: peer-reviewed or established reference (textbook, standards body)
   - *Economic/statistical*: government or intergovernmental data source, or peer-reviewed analysis
   - *Other domains*: tier >= 3 credibility (no unclassified or flagged sources)
3. **No majority COI**: No more than half of the threshold sources may have a conflict of interest (per Rule 6's COI taxonomy: organizational, funding dependency, institutional co-benefit, competitive antagonism, revolving door, or advocacy/ideological) on the same side of the claim.
4. **Documented in `operator_note`**: State why 3 sources are unavailable, confirm source quality, and disclose any known COI.

If these conditions are not met, keep `threshold: 3`. If fewer than 3 qualifying sources exist and the quality gates are not met, the verdict should be **UNDETERMINED** (insufficient evidence), not PROVED at a lowered threshold.

**Causal vs. associational claims:** When the claim uses causal language — "causes," "leads to," "promotes," "triggers," "results in," "damages," "prevents" — the proof must decompose it into at least two sub-claims using the **compound claim template**:
- **SC-association**: "X is associated with Y" — satisfiable by observational cohorts, cross-sectional studies, epidemiological correlations.
- **SC-causation**: "The association is causal (not confounded)" — satisfiable by:
  - RCTs or controlled experiments (gold standard)
  - Established causal inference methods where RCTs are impractical: Bradford Hill criteria assessment, Mendelian randomization, natural experiments, dose-response with adequate confounding control
  - Converging mechanistic evidence (biological pathway) + longitudinal outcome data from independent studies

Verdict outcomes:
- **SC-association holds + SC-causation holds** -> **PROVED**
- **SC-association holds + SC-causation fails** -> **PARTIALLY VERIFIED** (association confirmed, causation not established)
- **SC-association fails** -> use `proof_direction: "disprove"` in CLAIM_FORMAL, which maps to **DISPROVED** when disproof sub-claims hold
- **Insufficient evidence for SC-association** -> **UNDETERMINED**

The `operator_note` must NOT redefine a causal claim as associational to avoid this decomposition. This rule does not apply to claims already phrased associationally ("is correlated with," "is associated with").

## Limitations

Strong for crisp, auditable, bounded claims; weak for open-ended, normative, or predictive claims. The key limit is **formalizable vs fuzzy** — a claim works if it decomposes into extractable facts and a clear rule for proof/disproof.

Disproof is often easier (single counterexample suffices). The engine struggles with: deep original mathematics beyond sympy, broad causal inference, competing definitions, and large literature synthesis. Citation verification confirms quote presence, not semantic entailment — the adversarial check (Rule 5) mitigates this.

## Edge Cases

**Fictitious source attributions — distinguish load-bearing from appended.** Two shapes share the surface form "the claim mentions a source that turns out not to exist" but warrant different proof structures:

- **Load-bearing attribution** — the source identity *is* part of the claim's meaning. Form: "per [Source], value is X" / "[Source] reported Y in 2023" / "according to [Author]'s [Year] study." If [Source] doesn't exist, the claim's authority chain breaks; PROVED would be misleading. Treat as a compound: (SC1) the numeric value or factual proposition is correct, (SC2) the stated source contains/asserts it. The compound verdict reflects both — typically PARTIALLY VERIFIED if SC1 holds and SC2 fails, or DISPROVED with `proof_direction: "disprove"` if the claim *is* the attribution.

- **Appended reference list** — the proposition stands on its own literature; the citations are apparatus, not authority. Form: "Adult neurogenesis occurs in the dentate gyrus (Eriksson 1998; Spalding 2013; Chen 2023)." The proposition is supported by the cited literature taken collectively; one fabricated reference doesn't undo the proposition if the surviving citations independently establish it. Prove the proposition itself in the normal Type B way, and document each broken citation in `adversarial_checks` (with the citation-audit verdict — `unresolvable`, `metadata_chimera`, etc.). The verdict reflects whether the proposition holds; the citation-defect disclosure goes in adversarial checks AND a note in `proof.md`'s Conclusion section AND the audit doc's Citation Verification Details.

**Which shape is it?** Apply the substitution test: if you remove the named source from the claim text, does the claim still make a checkable assertion? "per Smith 2023, the value is 5" → without Smith, no claim remains → load-bearing. "Adult neurogenesis occurs (Smith 2023)" → without Smith, "adult neurogenesis occurs" is still a checkable proposition → appended. When ambiguous, prefer the load-bearing reading — it is the more conservative call.

**Partial-period data:** If a claim covers a time range but the best sources only cover part of it (e.g., claim says 1994-2023, sources cover 1994-2020), document the gap in `operator_note`. For **cumulative nonnegative totals** (e.g., total aid disbursed, cumulative emissions), if the partial-period sum already exceeds the claim's threshold, prove it with a logical extension: "If S₂₀ > T and the quantity is monotonically nondecreasing (cumulative total cannot shrink), then S₂₃ ≥ S₂₀ > T." State the monotonicity assumption explicitly using `explain_calc()`. This shortcut does NOT apply to averages, rates, percentages, or rolling metrics — for those, the missing-period values could decrease the aggregate, and you must either find full-period sources or return `UNDETERMINED` with an explanation of what data is missing.

**Source doesn't contain claimed constant:** If a claim says "per [Source]" but that source doesn't publish the specific constant (e.g., "CODATA values for solar mass" when CODATA doesn't list solar mass), document the substitution in `operator_note`: which source you actually used, why it's authoritative, and how it relates to the claimed source.

**Comparative claims with source-acknowledged uncertainty:** When a claim uses a superlative or comparative — "the safest," "the lowest," "the most," "better than" — and the source used to evaluate the comparison explicitly states that the compared values have overlapping uncertainty ranges, confidence intervals, or error bars: set `uncertainty_override = True` in the verdict section (date/age or numeric template). The verdict will be **UNDETERMINED**, not PROVED or DISPROVED. Point estimates alone cannot resolve a ranking when the source itself flags that the estimates are not statistically distinguishable. Document in `operator_note`: "Source [name] states [exact quote about uncertainty overlap]." This applies when the source providing the data also flags the uncertainty, or when the caveat comes from a source analyzing the same underlying dataset.
