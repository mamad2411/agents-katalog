---
name: cli-watermark
metadata:
  author: clement
description: >
  Steganographic code watermarking for IP defense. Generates multi-layered fingerprints
  that survive AI rewrites, language changes, renaming, and clean-code passes. Produces
  timestamped cryptographic commitments for legal proof of authorship. Use when the user
  wants to watermark a codebase, protect IP, prove code ownership, detect code copying,
  add steganographic markers, generate proof-of-authorship, or says 'watermark', 'fingerprint',
  'steganography', 'IP protection', 'code ownership proof', 'anti-copy', 'prove authorship',
  'detect copy', 'canary'. Also triggers on 'paper town', 'CFG watermark', 'code provenance'.
argument-hint: "[project-path-or-file]"
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
  - Agent
---

> **Optimization:** Heavy content lives in `references/`. Load on demand.

> **Language rule:** Skill instructions are written in English. When generating user-facing output, detect the project's primary language (from README, comments, docs, commit messages) and produce the output in that language. If the project is bilingual, ask the user which language to use before proceeding.

> **SECURITY:** This skill generates PRIVATE artifacts. NEVER commit watermark secrets, codebooks, or proof files to a public repo. All secrets go in `{project}/.watermark/` (gitignored) or in a separate private repo.

# CLI Watermark — Steganographic Code Fingerprinting

> *"Cartographers insert fictional towns to catch map plagiarists. We insert fictional decisions to catch code plagiarists."*

## Rules for the Watermarker

1. **L8 first, always.** Generate the timestamped commitment BEFORE applying any code-level layer. Anteriority is your strongest asset — if you apply L4 without L8, you have a clever trick but no legal proof.
2. **Never publish secrets.** `secret.env` and `codebook.json` are PRIVATE. Only `PROOF.md`, `vectors.json`, and `.ots` files can be shared.
3. **Derive, don't invent.** Every watermark value (constant, canary, ordering) must be deterministically derivable from the master secret. Ad-hoc choices are indefensible — "I just picked that number" loses in court.
4. **Watermark the behavior, not the syntax.** After 2 rewrites + clean code, only L4/L5/L7/L8 survive. Invest there first; L1/L2/L3 are supplementary signal.
5. **Defense in depth.** No single layer is proof. The legal argument is combinatorial: "What is the probability that N independent signals all match by coincidence?"
6. **Keep the code clean.** Watermarks must be invisible to code review. If a reviewer can spot a canary, an adversary can remove it. The best watermarks look like normal engineering decisions.
7. **Re-watermark on release.** Constants drift, APIs evolve, test vectors need updating. Each release = new L8 commitment + refresh of degraded layers.
8. **Always have a Plan D².** Assume every layer will be attacked. Know in advance which layers survive which attacks, and what your minimum viable proof is when half the layers are gone.
9. **Protect to defend, never to trap.** Watermarks prove authorship — they don't sabotage the adversary's code, don't phone home, don't create legal risk for you. Ethical watermarking = forensic evidence, not DRM.
10. **Anticipate the adversary's evolution.** The threat is not static. Today it's a single AI rewrite; tomorrow it's a specialized de-watermarking tool. Design for the adversary 2 years from now, not today's.

## Contingency matrix — Plan D²

Assume layers WILL be destroyed. Know your minimum viable proof at each degradation level.

| Scenario | Layers destroyed | Surviving proof | Legal strength | Action |
|---|---|---|---|---|
| **Green** — No attack | None | All 8 layers | Fortress (A) | Normal re-watermarking schedule |
| **Yellow** — Casual rewrite | L1, L2, L3 gone | L4 + L5 + L7 + L8 | Strong (B) | Sufficient. Behavioral + algorithmic + timestamps hold. No action needed |
| **Orange** — Aggressive rewrite + lang change | L1-L3 + L6 gone | L4 + L5 + L7 + L8 | Strong (B) | L4 is the firewall. If the adversary copied the algorithm, the Fermat prime travels |
| **Red** — Complete code rewrite + new architecture | L1-L6 all gone | L7 + L8 only | Moderate (C) | Test vectors + timestamps are your last stand. If their API matches your published vectors at 5 decimals, that's your proof |
| **Black** — Code AND behavior rewritten | L1-L7 gone | L8 only | Weak (D) | Timestamp proves you existed first, but no behavioral match. Need supplementary evidence (prod logs, git history, witnesses) |
| **Extinction** — Everything destroyed, no timestamps | All gone | Nothing | None (F) | You didn't follow Rule #1. Learn for next time |

**Key insight:** the Green→Black degradation is monotonic. You can NEVER go from Red to Green without re-watermarking. But you can always add layers on top of what remains.

**Minimum viable watermark:** L4 + L8 (algorithmic fingerprint + timestamp). If you have nothing else, at least have those two. They survive everything except a total algorithm rewrite.

## Adversary evolution model

The threat is not static. Design for the adversary 2 years ahead.

| Adversary generation | Capability | What they break | What still holds |
|---|---|---|---|
| **Gen 0** — Copy-paste | Takes your code verbatim | Nothing (trivial diff) | Everything — this is not a real adversary |
| **Gen 1** — AI rewrite (2024)| "Rewrite this in Go" | L1, L2, L3 | L4, L5, L6, L7, L8 |
| **Gen 2** — AI rewrite + clean code (2025) | "Rewrite, rename, optimize" | L1, L2, L3, partial L6 | L4, L5, L7, L8 |
| **Gen 3** — Targeted de-watermarking (2026-27?) | Specialized tools that detect and remove common watermark patterns | L1-L3 dead, L4 at risk if pattern-matched, L6 at risk | L5 (behavior is external), L7 (published, immutable), L8 (blockchain) |
| **Gen 4** — Algorithm reimplementation (future) | Adversary understands the algorithm and reimplements from spec | L1-L6 all dead | L7 + L8 + production logs |
| **Gen 5** — Full clean-room (theoretical) | Independent implementation from public docs only | Everything except anteriority | L8 timestamp + prod logs. But if truly independent, they're not copying |

**Design principle:** invest in layers that survive Gen 3+. Today that means L4 (rare primes are hard to pattern-match), L5 (behavior lives outside the code), L7 (published facts), L8 (blockchain-immutable).

**When the adversary reaches Gen 3:** the pre-commit hooks and entangled tests from `references/lifecycle.md` are your internal defense. The adversary attacks from outside; the lifecycle defense protects from inside (your own dev + AI rewrites). Both threats must be covered.

## Threat model

An adversary:
1. Takes your open-source code
2. Asks an AI to rewrite it in the same or different language
3. Applies clean-code conventions, renames everything
4. Claims independent authorship

**Goal:** prove prior authorship despite 2+ rewrites + language change + clean-code normalization.

## What survives what

| Technique | Survives rename | Survives restructure | Survives lang change | Survives 2 rewrites | Legal strength |
|-----------|----------------|---------------------|---------------------|---------------------|----------------|
| L1: Magic constants | ✅ | ⚠️ | ⚠️ | ❌ | Medium |
| L2: Synonym encoding | ⚠️ | ✅ | ❌ | ❌ | Low |
| L3: Structural canaries | ✅ | ⚠️ | ⚠️ | ⚠️ | Medium |
| L4: Algorithmic fingerprint | ✅ | ✅ | ✅ | ✅ | High |
| L5: Observable behavior | ✅ | ✅ | ✅ | ✅ | Very high |
| L6: CFG topology watermark | ✅ | ⚠️ | ✅ | ✅ | High |
| L7: Published test vectors | — | — | — | ✅ | Very high (legal) |
| L8: Timestamped commitment | — | — | — | ✅ | Very high (legal) |

**Key insight:** after 2 rewrites + clean code, proof cannot live in the code. It must live in:
- **Anteriority** — your production logs showing behavior before them
- **Observable behavior** — their binary behaves like yours on your test vectors
- **Spec** — they implemented a protocol you published first

## Mitosis — Scale to project size

| Signal | Tier | Layers | Effort |
|--------|------|--------|--------|
| Single file / small lib (< 500 LOC) | **S** | L4 + L8 only | 15 min |
| Standard project (500-10K LOC) | **M** | L1 + L3 + L4 + L7 + L8 | 1h |
| API / service with observable behavior | **L** | L1 + L3 + L4 + L5 + L6 + L7 + L8 | 2-3h |
| Protocol / spec (highest value IP) | **XL** | All 8 layers + ZKP commitment | Half-day |

For tier **S**: skip the full workflow. Generate L4 fingerprint + L8 commitment. Done.

## Input

`$ARGUMENTS` is the target project or file to watermark.

- **Project path** → full watermark suite (all applicable layers)
- **File** → targeted watermark on specific functions
- **Empty** → current working directory

## Workflow

### Phase 0 — Pre-flight diagnostic

Before watermarking, verify:

```
[ ] Project has original code (not a fork without modifications)
[ ] .gitignore exists and can be extended (for .watermark/)
[ ] openssl available (for HMAC derivation)
[ ] ots-cli available (for OpenTimestamps — optional but recommended)
[ ] No existing .watermark/ directory (or confirm overwrite)
[ ] Project has at least 1 algorithmic decision worth fingerprinting (L4 target)
[ ] If public API: at least 1 observable endpoint (L5 target)
```

If the project is a pure fork with no original logic → STOP. Watermarking someone else's code is both useless and dishonest.

### Phase 0.5 — Assess the project

1. Read the project: language, architecture, key algorithms, public API surface
2. Identify **watermark-worthy targets**: functions with algorithmic choices, configurable constants, protocol specs, observable behavior
3. Determine the tier (S/M/L/XL) and applicable layers
4. Count the surface area: how many L1 constants? How many L4 candidates? How many L5 endpoints?

| Project type | Recommended layers |
|---|---|
| Library with public API | L4 + L5 + L7 + L8 |
| CLI tool | L1 + L3 + L4 + L7 + L8 |
| Protocol/spec | L5 + L6 + L7 + L8 (strongest) |
| Web service | L5 + L7 + L8 |
| Algorithm-heavy | L4 + L6 + L7 + L8 |

### Phase 1 — Generate the secret seed

Read `references/crypto-layer.md` for details.

```bash
MASTER_SECRET=$(openssl rand -hex 32)
L1_KEY=$(echo "L1:${MASTER_SECRET}" | openssl dgst -sha256 | awk '{print $2}')
L4_KEY=$(echo "L4:${MASTER_SECRET}" | openssl dgst -sha256 | awk '{print $2}')
```

Store in `{project}/.watermark/secret.env` (gitignored).

### Phase 2 — Apply layers (IMPLEMENTATION)

For each applicable layer, read the corresponding reference file, then **actually modify the code**. Each layer follows the same cycle: **identify targets → derive values → edit the code → write an entangled test → record in codebook**.

| Layer | Reference file | What it produces |
|---|---|---|
| L1 — Magic constants | `references/layer-constants.md` | HMAC-derived constants replacing arbitrary values |
| L2 — Synonym encoding | `references/layer-synonyms.md` | Codebook + systematically chosen identifiers |
| L3 — Structural canaries | `references/layer-canaries.md` | Paper-town patterns in code structure |
| L4 — Algorithmic fingerprint | `references/layer-algorithm.md` | Non-standard but correct algorithmic choices |
| L5 — Observable behavior | `references/layer-behavior.md` | Timing padding, field ordering, response fingerprints |
| L6 — CFG topology | `references/layer-cfg.md` | Graph-theoretic watermark in control flow |
| L7 — Test vectors | `references/layer-vectors.md` | Published input/output pairs with precise values |
| L8 — Timestamped commitment | `references/layer-commitment.md` | RFC 3161 / OpenTimestamps / GPG-signed proofs |

**Mandatory implementation cycle per layer:**

```
FOR EACH applicable layer:
  1. READ the reference file (references/layer-{name}.md)
  2. IDENTIFY targets in the code:
     - L1: grep for numeric constants (buffer sizes, timeouts, capacities)
     - L3: find functions with match/if chains where a guard clause is defensible
     - L4: find formulas with normalization, scoring, or arithmetic
     - L5: find API endpoints returning JSON, headers, or numeric values
     - L6: find match arms or if/else chains whose order is arbitrary
  3. DERIVE the watermark value from the layer key:
     - L1: HMAC(L1_KEY, constant_name) mod range
     - L3: choose canary pattern from the catalog in the reference
     - L4: select a rare prime or mathematical constant
     - L5: define field ordering, precision, header format
     - L6: derive branch ordering from HMAC(L6_KEY, function_name)
  4. EDIT the source code:
     - Replace the original value with the derived one
     - Ensure the code still compiles and all existing tests pass
  5. WRITE an entangled test (references/lifecycle.md):
     - A test whose expected value depends on the watermark
     - The test MUST look like a normal functional/capacity test
     - Place it in the existing test file for that module, not in a watermark-specific file
  6. RECORD in codebook.json:
     - Layer, file, line, original value, watermarked value, derivation formula
  7. VERIFY: run the test suite — if anything breaks, fix before proceeding
```

**After all layers are applied:** run the full test suite once. If green, proceed. If red, debug — a watermark that breaks the build is useless.

### Phase 2.5 — Red team + honey tokens (MANDATORY for tiers L/XL)

Before generating proof artifacts, **attack your own watermarks**. The INTJ builds the fortress; this phase is where you think like the attacker who tries to breach it.

#### Step 1 — Smoke test (all tiers)

Pick your strongest layer (usually L4) and try to break it yourself:

```
1. Copy the watermarked file to /tmp/
2. Ask an AI to rewrite it: "Rewrite this function in clean, idiomatic [language]"
3. Check: is the watermark signal still present in the rewrite?
   - L4 prime: grep for the constant → still there? ✅
   - L5 behavior: run the test vector → same output? ✅
4. If the smoke test fails on your strongest layer → your watermark scheme is too weak.
   Go back to Phase 2 and choose a more resilient technique.
```

**Do NOT skip this.** A watermark you haven't tried to break is a watermark you don't know the strength of.

#### Step 2 — Red team (tiers L/XL)

Systematically attack every layer:

```
FOR EACH applied layer:
  1. ATTACK: attempt to remove or neutralize the watermark
     - L1: replace the constant with a round number (512, 1024, 4096)
     - L3: remove the "redundant" guard clause
     - L4: replace the rare prime with a common one (try 2, 10, 100)
     - L5: alphabetize the JSON field ordering
     - L6: sort the match arms alphabetically
  2. CHECK: does the entangled test catch the removal?
     - YES → layer is protected. Record: "L4: entangled test caught removal ✅"
     - NO → entangled test is too weak. Strengthen it before proceeding.
  3. RESTORE: revert the attack (git checkout the file)
```

**The red team produces a resilience report** recorded in the codebook:

```json
{
  "red_team": {
    "date": "2026-04-10",
    "layers_tested": 5,
    "layers_caught_by_tests": 4,
    "weakest_layer": "L3 — canary removed, no test caught it",
    "action_taken": "Added entangled test for L3 canary"
  }
}
```

#### Step 3 — Honey tokens (tiers L/XL)

Plant 1-2 **decoy watermarks** that are slightly easier to spot than the real ones. The adversary finds them, removes them, and thinks they're done — while the deep layers (L4/L5) stay hidden.

Good honey tokens:
- A suspiciously round constant that looks like a watermark but isn't (e.g., `0xDEAD` in a debug path)
- A comment that says `// WM` near dead code (the adversary greps for "WM", finds this, removes it, misses the real watermarks)
- An unusual variable name in a test file that looks like a fingerprint

**Rules for honey tokens:**
1. Max 2 honey tokens per project — more looks like noise
2. They must be in non-critical code (dead paths, debug, tests)
3. They must be plausible enough that the adversary believes they found "the" watermark
4. Document them in the codebook as `"type": "honey"` — you need to know which are real and which are bait
5. Never rely on honey tokens for proof — they are distractions, not evidence

#### Step 4 — Adversary profiling (tier XL)

Before finalizing, profile the specific adversary if known:

```
1. What language will they rewrite to? → prioritize layers surviving that transition
2. Do they have their own test suite? → if yes, L7 vectors are powerful (they might run yours)
3. Do they have a public API? → if yes, L5 behavioral markers are extractable
4. Are they technically sophisticated? → if yes, skip L1/L2 (waste of time), focus L4/L5/L8
5. Are they legally sophisticated? → if yes, L8 (timestamps) is your primary weapon
```

### Phase 3 — Generate proof artifacts

Read `references/proof-bundle.md`.

**Generate these files:**

1. `{project}/.watermark/secret.env` — master secret + derived keys (GITIGNORED)
2. `{project}/.watermark/codebook.json` — per-layer watermark details (GITIGNORED)
3. `{project}/.watermark/PROOF.md` — commitment hashes, timestamps, verification instructions
4. `{project}/.watermark/vectors.json` — canonical test vectors (can be published)
5. `{project}/.watermark/commitment.ots` — OpenTimestamps proof (if ots-cli available)
6. `{project}/.watermark/hooks/check-watermarks.sh` — pre-commit integrity hook
7. `{project}/.github/workflows/watermark-verify.yml` — hidden CI job (if GitHub Actions)

**Add to `.gitignore`:**
```
.watermark/secret.env
.watermark/codebook.json
.watermark/releases/
```

**Install the pre-commit hook** (read `references/lifecycle.md` for integration with husky/pre-commit frameworks).

### Phase 4 — Verification guide

Generate `{project}/.watermark/VERIFY.md`:
- How a forensic examiner would verify each layer
- How to reveal the secret to a judge
- What evidence to collect from the suspect's code
- Statistical argument for why the coincidence is improbable

### Phase 5 — Score, verify, and report

**After all layers are applied and artifacts generated, compute the WDS.**

Scoring is procedural — verify each layer was actually applied, not just planned:

```
FOR EACH layer in codebook.json:
  1. READ the codebook entry (file, line, expected value)
  2. GREP the source code for the expected value at the expected location
     - FOUND → layer is INTACT, score the points
     - NOT FOUND → layer is MISSING or DEGRADED, score 0
  3. For L5 (behavior): run the test vectors and compare output
     - All vectors match at 5-decimal → INTACT
     - Some differ → DEGRADED (partial score)
  4. For L8 (commitment): verify the .ots or .tsr file exists
     - OTS file exists → 10 points
     - RFC 3161 file exists → 7 points
     - GPG-signed commit exists → 3 points
     - Nothing → 0 points
  5. RECORD the per-layer status: INTACT / DEGRADED / MISSING
```

**The score reflects what IS, not what was planned.** A layer that was applied but later removed by a dev scores 0.

## Watermark Defensibility Score (WDS)

Each layer contributes to a combined score:

| Layer | Max points | Scoring criteria |
|---|---|---|
| L1 | 5 | +1 per HMAC-derived constant (max 5) |
| L2 | 3 | +1 per 10 systematically named functions (max 3) |
| L3 | 5 | +2 per canary that passes code review undetected |
| L4 | 15 | +5 per algorithmic fingerprint surviving cross-language test |
| L5 | 20 | +5 per behavioral marker measurable externally |
| L6 | 10 | +5 per CFG watermark documented with graph evidence |
| L7 | 15 | +5 per published test vector with 5-decimal precision |
| L8 | 20 | +10 OTS on Bitcoin, +7 RFC 3161, +3 GPG-signed |

**Score capped at 100.**

| WDS | Grade | Legal readiness |
|-----|-------|-----------------|
| 80-100 | **A** — Fortress | Multiple independent proofs, blockchain-timestamped. Ready for litigation. |
| 60-79 | **B** — Strong | Good layer coverage. Would stand up to expert scrutiny. |
| 40-59 | **C** — Moderate | Enough for a cease-and-desist. Weak against determined adversary. |
| 20-39 | **D** — Weak | Deterrent only. Would not survive expert cross-examination. |
| 0-19 | **F** — Decorative | No real legal value. Mostly psychological. |

## Output format

```markdown
# Watermark Report — {project}

**Date:** {date}
**Tier:** {S/M/L/XL}
**Layers applied:** {N}/8
**WDS:** {score}/100 ({grade})

## Layer Summary

| Layer | Applied | Targets | Resilience | Points |
|-------|---------|---------|------------|--------|
| L1 — Constants | ✅ | 4 constants | Rename only | 4/5 |
| L2 — Synonyms | ❌ | — | — | 0/3 |
| L3 — Canaries | ✅ | 2 paper towns | Rename + partial restructure | 4/5 |
| L4 — Algorithm | ✅ | 1 fingerprint (Fermat F4) | All transforms | 5/15 |
| L5 — Behavior | ✅ | 3 markers (ordering, precision, header) | All transforms | 15/20 |
| L6 — CFG | ❌ | — | — | 0/10 |
| L7 — Vectors | ✅ | 5 canonical vectors | Legal proof | 15/15 |
| L8 — Commitment | ✅ | OTS on Bitcoin | Legal proof | 10/20 |
| **Total** | **5/8** | | | **53/100 (C)** |

## Artifacts Generated

| File | Visibility | Content |
|------|-----------|---------|
| .watermark/secret.env | PRIVATE | Master secret + derived keys |
| .watermark/codebook.json | PRIVATE | Layer details, locations, values |
| .watermark/PROOF.md | Shareable | Commitment hashes + verification |
| .watermark/vectors.json | Publishable | Canonical test vectors |
| .watermark/commitment-v{X}.ots | Shareable | OpenTimestamps proof |
| .watermark/VERIFY.md | Shareable | Forensic verification guide |

## Recommendations

- {specific recommendations based on gaps}

## Re-watermarking Schedule

| Event | Action |
|---|---|
| New release | Re-derive L1 constants, update L8 commitment, run `--audit` |
| New public API | Add L5 behavioral markers + L7 vectors |
| Protocol change | Update L4 algorithmic fingerprint + L7 vectors |
| AI-assisted refactor | Run entangled tests immediately, check CI artifact |
| Suspected copying | Extract L5 evidence from suspect's API |
```

## Watermark Preservation — Surviving Dev + AI Rewrites

Read `references/lifecycle.md` for the full preservation architecture.

### 5-layer defense against degradation

| Defense | When | Blocks? | Detects |
|---|---|---|---|
| **Pre-commit hook** | Every commit | No (warning) | L1/L3 constants changed by a dev |
| **Hidden CI job** | Every push | No (silent artifact) | Any watermark layer regression |
| **Entangled tests** | Test suite | Yes (test fails) | L1/L4/L5 constants changed |
| **Guard network** | Test suite | Yes (assertion fails) | Distributed cross-verification |
| **Release audit** | Before each tag | Manual gate | Full 8-layer integrity check |

### The Collberg/Thomborson technique: entangled constants

Write tests whose expected values **derive from** watermark constants. If someone (human or AI) changes the constant, the test fails — but the test looks perfectly normal:

```rust
#[test]
fn test_cache_eviction_boundary() {
    let cache = RouteCache::new(); // uses ROUTE_CACHE_CAPACITY = 6735
    for i in 0..(6735 * 9 / 10) { cache.insert(i, Route::default()); }
    assert_eq!(cache.len(), 6061); // 6735 * 0.9 — depends on exact capacity
}
```

An AI seeing this test cannot know that 6061 is a watermark-derived value. If it "optimizes" the capacity to 8192, the test breaks, the dev investigates, and the watermark is restored.

### What survives an AI rewrite of YOUR code

| Layer | Survives Copilot/Claude rewriting your code | Protection mechanism |
|---|---|---|
| L1 constants | ⚠️ AI may "round" to power-of-two | Entangled tests catch this |
| L3 canaries | ⚠️ AI may remove "redundant" guard | Guard network catches this |
| L4 algorithm | ✅ AI preserves the formula | Fermat primes are already "clean" |
| L5 behavior | ✅ AI doesn't change API output | Behavioral test locks |
| L7 vectors | ✅ external, not in the code | Published, immutable |
| L8 commitment | ✅ external, not in the code | Blockchain-timestamped |

## Anti-patterns — What NOT to do

| # | Anti-pattern | Problem | Fix |
|---|---|---|---|
| W1 | **Obvious Canary** | Canary is too unusual, spotted in code review | Make it look like a defensible engineering choice |
| W2 | **Secret in Public** | Committing secret.env or codebook.json to a public repo | .gitignore from day 1, pre-commit hook |
| W3 | **Single Layer Reliance** | Relying on L1 alone (dies after 1 rewrite) | Always combine with L4+L7+L8 minimum |
| W4 | **Watermark Without Timestamp** | Clever fingerprint but no L8 → no anteriority proof | L8 is mandatory, not optional |
| W5 | **Over-Watermarking** | 50 canaries in 200 LOC → code smells, reviewer suspicion | Max 3 canaries per 1000 LOC, focus on L4/L5 |
| W6 | **Stale Proof** | Published vectors no longer match the code (API changed) | Re-watermark on every release |
| W7 | **Watermarking Forks** | Applying watermarks to code you didn't write | Only watermark YOUR original code |
| W8 | **Magic Number Cargo Cult** | Changing 512→6735 without HMAC derivation → "I just picked it" | Every value must be derivable from the secret |

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|---|---|---|
| Code quality issues found during assessment | `/cli-audit-code` first | Clean code before watermarking — don't watermark bugs |
| Complex call graph worth fingerprinting | `/cli-audit-tangle` | Map the CFG topology for L6 |
| Protocol/spec exists | `/cli-forge-doc` | Document the spec BEFORE watermarking it (L7 needs published docs) |
| Existing test suite | `/cli-audit-test` | Verify test coverage — L7 vectors should complement, not duplicate |
| Observable API endpoints | `/cli-audit-sync` | Verify docs match behavior before defining L5 markers |

**Rule:** Recommend, don't auto-execute.

## Integration with other cli-* skills

| Skill | Relationship |
|---|---|
| `/cli-audit-code` | Run before watermarking — ensure code quality first |
| `/cli-audit-tangle` | Extract call graph for L6 CFG topology watermark |
| `/cli-audit-test` | L7 test vectors complement the existing test suite |
| `/cli-audit-drift` | Watermarks in CONTRACTS.md constants survive drift detection |
| `/cli-forge-doc` | Document the protocol/spec — L7 vectors go in public docs |
| `/cli-cycle` | Post-release: verify watermarks haven't degraded |
| `/cli-git-conventional` | Commit watermark code changes with conventional style |

## Legal framework

The legal strength comes from **combination**:
- Improbable constants + timestamp prior to competitor + ability to reveal the generating secret
- A judge understands: "I can prove I chose these values before you existed, using a secret only I possess"

This maps to:
- **French law**: droits d'auteur on original algorithmic work (Code de la propriété intellectuelle, L112-2)
- **US law**: copyright on original expression in code + trade secret on the watermark scheme
- **Both**: prior art established by timestamped commitments

## What this skill does NOT do

- **Does not obfuscate code** — watermarks are invisible, code stays clean and readable
- **Does not add DRM** — no runtime enforcement, purely forensic
- **Does not guarantee legal victory** — provides evidence, not a verdict
- **Does not watermark third-party dependencies** — only your original code
- **Does not replace patents** — covers authorship proof, not functional claims

## Advanced reading

Read `references/academic.md` for:
- SIR (Semantic Invariant Robust) — ICLR 2024: watermark in embedding space
- Venkatesan et al.: graph-theoretic CFG watermarking
- RoSeMary 2025: ZKP-based ownership proof
- CodeMark-LLM 2025: cross-language watermarking via LLM transformations
