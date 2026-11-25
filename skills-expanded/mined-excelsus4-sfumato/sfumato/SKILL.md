---
name: sfumato
description: >-
  Sfumato — Dual-Track Cross-Domain Ideation (Direct Anchor + Explicit Analogy + Blind Isomorphic Reframing)
  using isolated parallel subagents, shared structural-skeleton masking, and a clean-context red-team selector to
  erase domain boundaries, break LLM homogenization, and widen exploration diversity without regressing below baseline.
  Trigger explicitly when the user invokes `/sfumato`, `/sfm`, or asks to run Sfumato.
  Trigger autonomously ONLY when the user asks for high-ceiling, non-obvious brainstorming on
  hard open-ended problems (new product strategy, game mechanics, system breakthroughs, escaping
  AI clichés) — do NOT auto-trigger on trivial naming, minor copy tweaks, or closed-ended tasks.
---

# Sfumato (`/sfumato`, `/sfm`) — Cross-Domain Ideation

Named after Leonardo da Vinci's *sfumato* technique (dissolving rigid borders to let new forms emerge), this skill dissolves a problem's domain borders to escape LLM mode collapse (*Artificial Hivemind*), expand structural mechanism diversity, and raise the **peak creativity ceiling (Top-1)** without dropping below a strong direct baseline.

## Core Principle: The Domain-Masking Trade-Off

- **Direct Anchor** *(default in `dual-track` & `deep`)*: 1 isolated native-domain baseline solver placed in the unlabeled pool so `max(Direct, Explicit, Blind) ≥ Direct` — locking the quality floor on tightly coupled engineering/systems loops.
- **Track A — Explicit Analogy** *(original problem visible + assigned remote domain)*: High hit-rate and surgical precision against domain-specific attack surfaces, though vulnerable to partial homogenization back toward industry clichés.
- **Track B — Blind Isomorphic Reframing** *(original domain vocabulary erased via a shared structural skeleton → solved blind in an isolated session → back-translated)*: Lower hit-rate (some abstractions won't translate cleanly), but **zero cliché gravity**, producing heavy-tail outlier mutations impossible in Track A.
- **Stage 2a/2b — Clean-Context Red-Team Triage & Selective Hardening**: A fresh, uncontaminated evaluator classifies candidates (`PASS / HARDEN / KILL`), selects Top-1, and hardens *only* Top-1's single biggest operational weakness.

---

## Step-by-Step Procedure

### 1. Frame the Problem (Neutral, Compact & Language-Matched)
Record `{USER_LANGUAGE}` (matching the user's request language) and distill the request into a crisp 3–5 bullet problem brief:
- **Core Goal** (what must change)
- **Structural Constraints & Incentive Polarity** (hard limits + primary polarity: `adversarial`, `cooperative`, `physical_loop`, `human_ux`, or `systems_ops`)
- **Why Obvious Fixes Fail** (explicitly ban the top 2–3 clichés so no track wastes budget on them)

### 2. Sample Truly Distant Domains (Single Command — Never LLM Choice)
Never ask an LLM to "pick random domains" (it repeats ants, jazz, and chess). Run the bundled stratified sampler directly in a single shell call:

- **Available macro-clusters (11):** `biology_ecology`, `physics_engineering`, `history_institutions`, `intelligence_conflict`, `markets_law`, `craft_operations`, `art_performance`, `social_anthropology`, `cognition_pedagogy`, `materials_chemistry`, `earth_navigation_grids`
- **Polarity-aware soft weighting (`--polarity`):** Pass `--polarity <adversarial|cooperative|physical_loop|human_ux|systems_ops>` (or `any` if mixed) so at least half of sampled remote domains share structural affinity with the problem while still spanning disjoint clusters.
- **No hint priming by default:** `sample_domains.py` omits `mechanisms` hints by default so solvers don't collapse onto 4–5 pre-written keywords (pass `--include-hints` only if you intentionally want mechanism cues).
- **Claude Code Safety Profile:** When running on **Claude / Claude Code**, always append `--safe-profile claude` to exclude 8 sensitive bio/CBRN/cyber/espionage domains — leaving **66 Claude-safe domains (exactly 6 per cluster across all 11 clusters)** with 0 safety refusals. On Antigravity/Codex, omit it for the full 74-domain pool across 11 clusters.

```bash
# Default dual-track: 3 remote domains (2 Explicit + 1 Blind) + 1 Direct Anchor = 4 isolated solvers
python "<skill_dir>/scripts/sample_domains.py" --k 3 --mode dual-track --polarity <polarity> --exclude-clusters <same_cluster_if_any>

# On Claude Code:
python "<skill_dir>/scripts/sample_domains.py" --k 3 --mode dual-track --polarity <polarity> --safe-profile claude --exclude-clusters <same_cluster_if_any>

# Deep mode: 6 remote domains (3 Explicit + 3 Blind) + 1 Direct Anchor = 7 isolated solvers
python "<skill_dir>/scripts/sample_domains.py" --k 6 --mode dual-track --polarity <polarity> --exclude-clusters <same_cluster_if_any>

# Opt-in sweep (11 clusters; add --safe-profile claude on Claude Code) or max (/sfm-max, 2-round tournament):
python "<skill_dir>/scripts/sample_domains.py" --k 11 --mode dual-track --polarity <polarity> [--safe-profile claude]
python "<skill_dir>/scripts/sample_domains.py" --all --safe-profile claude
```

### 3. Prepare Track B Isomorphic Masks via Shared 3-Line Structural Skeleton + Whole-Prompt Reread
Before spawning Track B subagents, do **NOT** jump straight from the original problem to a remote-domain story. Use a 2-step masking pass:
1. **Extract ONE Shared Private 3-Line Structural Skeleton (Check Polarity First):**
   - `Actors, Cost-Bearer & Incentive Polarity:` (who acts, who bears the downside, and whether actors are zero-sum/adversarial, cooperative, physical-loop, or platform-refereed)
   - `Core Asymmetry / Bottleneck:` (exact cost, information, physics, or cognitive imbalance)
   - `Why Static Controls Fail:` (exact failure mode of obvious rules, filters, or tutorials)
   - Check this skeleton against the original brief **before fanning out**: a mistaken polarity or cost-bearer spoils every Blind domain in the run.
2. **Map Skeleton → Native Target-Domain Scenario + Whole-Prompt Reread:**
   - For each Blind domain, rewrite the skeleton into a standalone problem in `{USER_LANGUAGE}` that a practitioner in `{DOMAIN_NAME}` could plausibly pose, using 100% native nouns of `{DOMAIN_NAME}`.
   - **Fold failed fixes into native constraints:** Express why the banned clichés fail as natural physical, economic, or institutional constraints *inside* the scenario itself (do not append a separate banned-cliché list).
   - **Strict Polarity Preservation:** Never map zero-sum enemies onto a cooperative central authority (and vice versa).
   - **Whole-Prompt Reread:** Reread the entire outgoing Blind prompt once before spawning: *(a) would a practitioner in `{DOMAIN_NAME}` find it natural, (b) did any source-domain jargon or proper nouns slip in, and (c) does the same actor still bear the same downside cost?* Repair any mismatch in place.

See [prompt_templates.md](./references/prompt_templates.md) for the exact templates.

### 4. Launch Isolated Parallel Subagents (Zero Cross-Talk!)
Spawn all Stage 1 solvers (Direct Anchor + Track A + Track B) **in parallel in separate, clean-context subagents**:
- **Antigravity (`agy`):** `invoke_subagent` with `TypeName: "self"`, `Model: "inherit"`
- **Claude Code:** `Agent` tool (fresh context per solver)
- **Codex CLI:** Use parallel isolated subagents if enabled; otherwise execute each solver in an isolated `codex exec` call (or isolated clean turn) without passing any previous solver's output.
- **Hard Rule 1 (Zero Cross-Talk):** Divergent solvers must NEVER see each other's outputs (prevents *Diversity Collapse*).
- **Hard Rule 2 (Pure Internal Knowledge):** Forbid tool calls, file reads, and web searches inside solvers; request exactly 2 concrete structural mechanisms in `{USER_LANGUAGE}`.
- **UX Hygiene:** While waiting for parallel subagents, keep intermediate status notes to 1 short line and never analyze partial results before all solvers return.

### 5. Back-Translate Track B (Mechanism Only, Never Cosplay)
For each Track B output:
- Extract ONLY the **causal mechanism + trade-off** and translate it cleanly into the original problem's concrete primitives.
- **Be ruthless:** If a Track B idea only maps via a strained pun or breaks under the problem's real polarity, discard it cleanly and log it as a translation loss.

### 6. Clean-Context Red-Team Triage (Stage 2a) & Selective Hardening (Stage 2b)
Normalize surviving Direct Anchor + Track A + translated Track B candidates into an identical, unlabeled format (`Candidate 1..N`) and run **Stage 2a** (1 fresh clean-context evaluator subagent) using [prompt_templates.md](./references/prompt_templates.md):
1. **Cut Surface Metaphors (`KILL`):** Reject any idea whose causal mechanism is identical to a banned cliché with fancy domain jargon pasted on top.
2. **Red-Team Flaw Triage (`PASS` / `HARDEN` / `KILL`):** Screen for Adverse Selection, Sybil/Wash-Trading exploits, and Feasibility/Premise violations. Disqualify unfixable flaws (`KILL`); promote fixable high-ceiling gems (`HARDEN`) with 1 explicit diagnosed flaw.
3. **Select Top-1 Champion + 2 Distinct Runners-Up (+ Optional Wildcard).**
4. **Stage 2b — Clean-Context Hardening & Selective Grafting *(skipped in `fast` or if Top-1 is already `PASS`)*:**
   - Take ONLY the winning Top-1 candidate (whether Cross-Domain or Direct Anchor — **never force-graft a polarity-mismatched cross-domain seed over a stronger Direct Anchor**) + its single biggest Red-Team flaw (and optionally 1 practical primitive from a passing runner-up).
   - Run 1 fresh clean-context engineering pass to repair that weakness without diluting the core non-obvious mechanism.
5. **Report Conclusion-First in `{USER_LANGUAGE}`:** Lead with the hardened Top-1 Champion + 2 Runners-Up (+ Wildcard if any), showing Mechanism, Why It's Hard to Defeat/Copy, Concrete Trade-Off, and Source Track/Domain, plus compact Red-Team triage notes.

---

## Modes, Composition & Compute Budget

| Mode | Stage 1 Solvers | Total Isolated Subagent Calls | Relative Token Cost (vs. 1 Direct Call) | When to Use |
|---|---|---:|---:|---|
| `fast` | `3 Explicit` (`--k 3 --mode explicit-only`) | `4` (3 solvers + Stage 2a) | ~4–5× | Quick non-obvious ideas under tight token/latency budgets |
| `dual-track` *(default)* | `1 Direct Anchor + 2 Explicit + 1 Blind` (`--k 3`) | `5–6` (4 solvers + Stage 2a + optional Stage 2b) | ~6–8× | Standard high-ceiling brainstorming (matches primary benchmark composition; guarantees `≥ Direct` floor) |
| `deep` | `1 Direct Anchor + 3 Explicit + 3 Blind` (`--k 6`) | `8–9` (7 solvers + Stage 2a + optional Stage 2b) | ~10–12× | High-stakes strategic/architecture breakthroughs requiring maximum exploration breadth |
| `sweep` *(opt-in only)* | `1 Direct Anchor + 11 domains` (`--k 11`, 1 per macro-cluster) | `13–14` (12 solvers + Stage 2a + opt. 2b) | ~15–18× | Full 11-cluster coverage in one wave without selector overload |
| `max` (`/sfm-max`, *opt-in only*) | **All 66 (Claude) / 74 domains** (`--all`) + **1 Direct Anchor** → **2-Round Tournament** | `79–80` (Claude) / `87–88` (full) | ~80–90× | Exhaustive high-budget brainstorming (*mandatory pre-flight user confirmation*) |

> **Why `Direct Anchor` is on by default in `dual-track` / `deep` / `sweep` / `max`:** Benchmarks across 9 runs showed that on tightly coupled engineering/physics loops (`DOC-ROT`, `GAME-SNOWBALL`), unlucky domain draws can underperform a strong Direct Baseline. Including 1 isolated Direct Anchor in the unlabeled Stage 2a pool keeps exploration diversity high while protecting your floor (`max(Direct, Explicit, Blind) ≥ Direct`).

### Opt-In `max` (`/sfm-max`) Tournament Protocol & Guardrails
- **NEVER auto-trigger `max` or `sweep`.** Run ONLY when the user explicitly requests `sweep`, `max`, or `/sfm-max`.
- **Mandatory Pre-Flight Confirmation (`max`):** Before spawning any subagents in `max` mode, display the exact session count (**79–80 sessions** on `--safe-profile claude`: `66 remote + 1 Direct Anchor + 11 Cluster Judges + 1 Grand Final + opt. Stage 2b`; or **87–88 sessions** on `full`: `74 + 1 + 11 + 1 + opt. 2b`) and wait for explicit user confirmation.
- **Why 2-Round Tournament (Never Dump 148 Ideas into 1 Selector):** Dumping 130+ raw ideas into one Stage 2 evaluator degrades judgment (*Lost-in-the-Middle*). Instead:
  1. **Round 1 — Cluster Playoffs (11 waves):** Run `sample_domains.py --all` (with `--safe-profile claude` on Claude). Execute in cluster waves (6–8 concurrent subagents per wave). After each cluster finishes, 1 fresh Cluster Red-Team Judge picks that cluster's **Top-1 Champion** (plus optional Wildcard).
  2. **Round 2 — Grand Final:** Pass the **11 unlabeled Cluster Champions + 1 Direct Anchor (12 finalists)** into 1 fresh Clean-Context Grand Final Red-Team Triage (Stage 2a) + Selective Hardening Pass (Stage 2b).

## Validation Checklist
- [ ] Domains were sampled via `scripts/sample_domains.py` in a single call (with `--polarity` and, on Claude Code, `--safe-profile claude`).
- [ ] Shared 3-line Track B skeleton was checked against the brief for cost-bearer & polarity fidelity, failed fixes were folded into native scenario constraints, and each outgoing Blind prompt was reread end-to-end for plausibility and zero pasted source jargon.
- [ ] All Stage 1 solvers ran isolated with zero shared conversation history and zero tool calls.
- [ ] Every prompt specified `{USER_LANGUAGE}` matching the user's request.
- [ ] Stage 2a produced explicit `PASS / HARDEN / KILL` triage in a clean context, and Stage 2b hardened only the winning Top-1 without forcing polarity-mismatched grafts.
