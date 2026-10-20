---
name: anchor-prototype-wave
version: 3.0.0
status: stable
promoted_date: 2026-05-17
supersedes: v2.1.0
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
description: >-
  Take a visual anchor (chassis tokens + page list) and produce a reviewable hi-fi prototype wave in ONE shot — a master gallery `index.html` plus one `index.html` per surface. All verification (deterministic validators, LLM grader, cross-AI review, fix-on-fail loop) runs inside the pipeline; no modes, no flags. Stops to ask only when page content is ambiguous or a surface escalates after 3 retries. Pairs upstream with `prototyping-ui-directions`, downstream with frontend build. Triggers: "用这个 anchor 出一波 prototype / generate the wave from this anchor / 把这些页面照这个 anchor 全生成 / take this chassis and produce N hi-fi mocks".
---

# Anchor Prototype Wave — v3.0.0

> **v3.0.0 reset (2026-05-17)**: v2.1's 4-mode design (AUDIT_ONLY /
> FIX_SELECTED / FULL_WAVE / SKILL_UPGRADE_PROPOSAL) is collapsed into a
> single end-to-end pipeline. The pipeline is conversational, not
> CLI-flag-driven. All verification cadences from v2.1 (validators +
> LLM grader + cross-AI review + fix loop) remain — they run silently
> inside the wave, not as separate user-invoked modes. The user describes
> what they want; the skill returns a reviewable artifact.
>
> Naming compatibility: file path stays `anchor-prototype-wave` so old
> prompts and skill routing keep working. Public/reporting name in
> this-style projects is **Track B Visual Research Run**. Older v2.0
> wording like "Stage 0-12", "Gate 12", "Wave plan", "_context.md"
> remains as internal orchestration vocabulary, not user-facing.

---

## §0 — What the user gives (once, conversationally)

The skill needs three things. If any are missing or ambiguous, it stops
and asks; it never silently invents.

```
1. Visual anchor (the chassis)
   - typography (sans family + weights + mono family)
   - radius scale (card / chip / pill)
   - border hairline value
   - accent color (single; secondary requires explicit declaration)
   - banned tokens (e.g. glass, blur, aurora, dark-by-default, decorative gradient)
   - status colors (amber / blue / green / red — bg + fg)
   - surface colors (page / card / sunken / muted)
   - text colors (primary / secondary / tertiary / mono-label)
   - spacing scale (e.g. 4/8/12/16/20/24/32/40/48)
   - micro shadow + hairline values

2. Page list
   Each page entry:
   - slug (kebab-case directory name)
   - display title (zh + en sub-line allowed)
   - one-line description / intent
   - route (e.g. /cases/:id, /me/work)
   - group (free-form; default groups used by v2: 顶层 / Case / Marketplace
     / Settings / Inspector / Global / Elements)
   - status hint (updated / review / retain / rebuild / parked)
   - risk hint (low / medium / high)
   - (optional) explicit content brief if the page is non-obvious

3. Output directory
   Default: `ui-lab/<date>-<anchor-slug>-anchor-prototypes/`
```

When all three are present, the pipeline runs end-to-end without further
checkpoints. The user only sees the wave plan summary in the skill's
opening message and the final report at the end.

---

## §1 — What the skill produces

```
<output-dir>/
├── index.html                            ← master gallery (mirrors v2)
│                                            see references/master-gallery-structure.md
├── <slug-1>/index.html                   ← hi-fi surface page
├── <slug-2>/index.html
│   ...
├── <slug-N>/index.html
├── elements/<atom>.html  (optional)      ← element-foundation surfaces if requested
└── audits/
    ├── _context.md                       ← chassis contract subagents read
    ├── manifest.json                     ← wave metadata + per-surface verdicts
    ├── contracts/<slug>.contract.json    ← preflight SurfaceContract (§2)
    ├── audits/<slug>.audit.json          ← validator + grader + scorer JSON
    ├── audits/<slug>.audit.md            ← human-readable derived view
    ├── cross-review/<slug>.codex.json    ← Codex review (when §6 triggers)
    ├── cross-review/<slug>.codex.md
    └── closeout.md                       ← wave summary for Gate 12 reviewer
```

JSON is source of truth; .md files are derived. Schemas in
`references/output-schema.md`.

---

## §2 — Pipeline (one shot, all stages automatic)

```
Stage 0  Anchor doc author        opus / main thread       writes audits/anchor-decl.md
Stage 1  Element index freeze     opus / main thread       writes audits/element-index.md
Stage 2  Context author           main thread              writes audits/_context.md
Stage 3  Surface classification   main thread              per-page: mature | creative | marquee
                                                            + form-type (12 morphology types)
Stage 4  Surface contracts        main thread              writes audits/contracts/<slug>.contract.json
                                                            (per references/output-schema.md SurfaceContract)
Stage 5  Spawn N surface subagents in PARALLEL (≤10 per batch; >10 auto-split)
          mature   surface  →  sonnet
          creative surface  →  opus
          marquee  surface  →  opus
          tools per subagent: Read, Write, Edit, Grep, Glob
          each subagent writes ONLY <slug>/index.html (+ optional writeup)
Stage 6  Deterministic validator (per surface)   scripts/validate_surface.py
          checks: scaffold_leak, decorative_gradient, pill_mono_drift,
                  surface_morphology (+ sub_cause), forbidden_write_path,
                  production_source_grounding, accessibility_minimum,
                  output_schema_validity
Stage 7  LLM grader (per surface)                sonnet
          fills soft_scores (6 dims) per references/scoring-rubric.md anchors
Stage 8  Scorer (per surface)                    scripts/score_audit_json.py
          composite + maturity-aware floor + verdict
          (PASS_9PLUS | FIX_NEEDED | REDO | ESCALATE_HUMAN)
Stage 9  Cross-AI review (per §6 trigger matrix below)    Codex (gpt-5.5 default)
          required for REDO / FIX_NEEDED / known-risk surfaces
          15% sampling on PASS_9PLUS
Stage 10 Fix-on-fail loop (per failing surface; ≤3 retries)
          REDO        → re-spawn fresh write subagent (no diff context)
          FIX_NEEDED  → re-spawn patch subagent (surgical, preserve untouched)
          Each retry's prompt must verbatim quote the failing gate + evidence
          After 3 retries still failing → ESCALATE_HUMAN (no silent auto-PASS)
Stage 11 Master gallery aggregation              main thread
          writes <output-dir>/index.html mirroring v2 structure
          (references/master-gallery-structure.md is the locked spec)
Stage 12 Manifest + closeout                     main thread
          updates audits/manifest.json with all verdicts
          appends new failure patterns to references/failure-patterns.md
          writes audits/closeout.md
Stage 13 Report to user                          main thread
          surface count + PASS / FIX / REDO / ESCALATE breakdown
          master gallery file URL
          list of ESCALATE_HUMAN surfaces with evidence
          (Gate 12 human approval is the user's job, post-skill)
```

---

## §3 — When the skill stops to ask the user

Only three situations cause the pipeline to pause:

1. **Inputs incomplete or ambiguous** at §0 (missing anchor field, page
   list missing route/intent, output dir conflicts with existing wave).
2. **ESCALATE_HUMAN after Stage 10** — any surface that fails 3 fix
   retries. Skill reports the failing gates + evidence selectors and
   asks the user to decide (manual edit / drop the surface / continue
   anyway).
3. **User asked to modify this skill itself** — any write that would
   touch `.claude/skills/anchor-prototype-wave/**` or
   `~/.claude/skills/anchor-prototype-wave/**`. Skill writes a proposal
   under `<output-dir>/audits/<date>-skill-vX.Y-spec/` and waits for
   explicit "yes change the skill files" before promoting.

No other approval gates. No "plan ratification" step for routine wave
generation. The skill assumes that when the user gave a complete
anchor + page list, they want the wave produced.

---

## §4 — Non-negotiable boundaries (HARD_DENY, all stages)

```
❌ workspace/src/**          (Track A production frontend)
❌ backend/src/**            (Track A production backend)
❌ workspace/src/styles/globals.css
❌ tailwind.config.*  /  vite.config.*  /  root package.json
❌ _reference/**             (vendor refs are read-only study material)
❌ vault/raw/**              (immutable raw archive)
❌ docker-compose*.yml
❌ migrations/**  /  drizzle/**
❌ .claude/skills/**         (unless §3 case 3 — explicit user request)
❌ ~/.claude/skills/**       (unless §3 case 3)
```

Subagent write scope is the surface's own `<slug>/index.html` + nothing
else. Main thread writes `_context.md` once + `manifest.json` + master
gallery `index.html` + `closeout.md`. Subagents never write shared files
(prevents race conditions).

Validator enforces `forbidden_write_path` automatically. Boundary
violations are reverted via `git checkout` and the subagent is
re-spawned with a stricter scope prompt.

---

## §5 — Skills this skill depends on

> **For users cloning this from GitHub**: this skill orchestrates
> subagents that consume other Claude Code skills. The other skills are
> NOT copied into this directory — you install them separately. Below is
> the dependency map; full per-stage consumption in
> `references/skills-dependencies.md`.

### Required (skill will not run end-to-end without)

| Dependency | Used by | Why |
|---|---|---|
| Codex official plugin (`codex@openai-codex`) | Stage 9 (cross-AI review) | External Codex reviewer via `/codex:adversarial-review` (or `/codex:review`); model picked with `--model`, env-var routing still applies. If Codex quota is exhausted, fall back to a second Claude subagent reviewer. Without Codex, cross-AI review stage can't fire. |

### Strongly recommended (output quality drops a lot without)

| Skill | Used by | Why |
|---|---|---|
| `ux-principles` | Stages 0, 5, 7 | Stage 0 anchor uses MODE A (which Laws of UX to honor / avoid for the chassis). Stage 5 surface subagents use MODE B (tactical numbers — spacing / hierarchy / contrast / typography). Stage 7 LLM grader uses MODE C (NN 10 heuristic + Built-for-Mars 5-lens audit). |
| `taste-skill` | Stages 0, 2, 5, 11 | Anti-AI-slop tokens + single-page craft rules. Applies to anchor declaration, `_context.md` writing, every surface subagent, and the master gallery aggregator. |

### Recommended (improves specific stages)

| Skill | Used by | Why |
|---|---|---|
| `prototyping-ui-directions` | Stage 5 (creative + marquee surfaces) | Multi-variant exploration patterns when a surface is genuinely novel and not anchored on a mature reference. Skip for mature surfaces. |
| `ai-regression-testing` | Stage 7 (LLM grader) | Regression detection patterns — catches "same model wrote it and reviewed it" blind spots. Improves grader independence. |
| `luxury-editorial-site-builder` | Stage 5 (marquee, brand-style only) | Only when the marquee surface is a brand/marketing landing page, not a product UI. Domain-specific. |
| `grill-with-docs` | Stage 0 (anchor terminology) | If the user's anchor description uses ambiguous terms (e.g. "more editorial", "feel premium"), this skill clarifies terms into committed tokens before Stage 0 commits the chassis. |

### Installation (for downstream GitHub users)

```bash
# Stage 9 cross-AI review = Codex official plugin (install via marketplace):
#   /plugin install codex@openai-codex
#
# Option A — copy skills into your project's .claude/skills/
mkdir -p .claude/skills
cp -r ~/.claude/skills/{ux-principles,taste-skill,prototyping-ui-directions,ai-regression-testing,grill-with-docs,luxury-editorial-site-builder} .claude/skills/

# Option B — install from the Claude Code skills marketplace (when available)
#   /plugin install ux-principles
#   /plugin install taste-skill
#   ... etc.

# Option C — symlink from your global skills directory (single source of truth)
ln -s ~/.claude/skills/ux-principles .claude/skills/ux-principles
# ... etc.
```

This skill itself contains no source code from the dependency skills.

---

## §6 — Cross-AI review trigger matrix (Stage 9, automatic)

```
REDO surface              → cross-AI review: REQUIRED
FIX_NEEDED surface        → cross-AI review: REQUIRED
PASS_9PLUS surface        → cross-AI review: sample 15% (rounded up)
known-risk surface        → cross-AI review: REQUIRED
  - overlay/drawer/fullpage morphology ambiguity in contract
  - any surface matching a pattern in references/failure-patterns.md
```

Cross-AI dispatcher uses `references/model-policy.md` (env-var driven,
no hardcoded model). Prompt template in
`ASSETS/codex-review-prompt.md`. Reviewer must cite which gate from §4
of `references/gates.md` it disputes, not vague "looks off".

---

## §7 — Hard gates and soft scores (Stages 6-8, automatic)

### Hard gates (BLOCK short-circuits any soft score)

```
gate_0_intent_alignment             — morphology matches claimed_surface_type
                                       sub_cause: form_mismatch | missing_scrim |
                                                  threshold_only | inner_widget_missing
gate_1_production_source_grounding  — production source read (or research_only_reason)
gate_2_boundary_compliance          — wrote only inside allowlist
gate_3_no_scaffold_leak             — no marketplace tokens outside marketplace surfaces
gate_4_accessibility_minimum        — buttons named, inputs labeled, focus + reduced-motion
```

### Verdict rule (gate-driven, not avg-driven)

```python
if gate_0 == BLOCK and sub_cause in (threshold_only, inner_widget_missing):
    verdict = FIX_NEEDED       # surgical patch
elif gate_0 == BLOCK:
    verdict = REDO             # form-level rewrite
elif gate_1 == BLOCK:
    verdict = REDO             # fundamental — never read source
elif any other gate == BLOCK:
    verdict = FIX_NEEDED
elif maturity-aware floor fails:
    verdict = FIX_NEEDED
elif weighted_score >= 9.0:
    verdict = PASS_9PLUS
else:
    verdict = FIX_NEEDED
```

### Soft scores (6 dims, 0-10, only when all hard gates PASS)

```
chassis_consistency       weight 0.20
mvp_coverage              weight 0.20
visual_quality            weight 0.15
interaction_quality       weight 0.15
consistency_with_siblings 0.15
innovation                0.15
```

Maturity-aware innovation floor (from contract `surface_innovation_target`):
mature ≥ 5, creative ≥ 7.5, marquee ≥ 8.5. Other 5 dims floor 8.5.

Full rubrics: `references/gates.md` + `references/scoring-rubric.md`.

---

## §8 — Anti-patterns (enforced)

- **A1** Treating `composite avg ≥ 9` as PASS while a hard gate is BLOCK.
- **A2** Subagent writes outside its `<slug>/index.html`.
- **A3** Hardcoding a Codex or Claude model name; always cite
  `references/model-policy.md`.
- **A4** Spawning subagents without a SurfaceContract JSON in place.
- **A5** Auto-PASS after `max_retries`. ESCALATE_HUMAN is mandatory.
- **A6** Running cross-AI review on every surface; use §6 trigger matrix.
- **A7** Skipping the closeout / regression-dataset update.
- **A8** Treating all morphology mismatches as REDO. Use
  `gate_0_sub_cause`: `threshold_only` and `inner_widget_missing` are
  FIX_NEEDED (surgical), not REDO (form-level rewrite).
- **A9** (v3.0.0) Re-introducing CLI flags or asking the user to pick a
  "mode". The pipeline is conversational and stateful; the skill infers
  what to do from the user's request, not from a flag.
- **A10** (v3.0.0) Stopping for plan ratification on routine wave
  generation. Only stop per §3.

---

## §9 — Reference layout

```
SKILL.md                            (this file)
CHANGELOG.md                        (version history)
references/
  master-gallery-structure.md       v3.0.0 — locked v2 layout spec for Stage 11
  skills-dependencies.md            v3.0.0 — per-stage external skill consumption map
  surface-taxonomy.md               12 morphology types
  gates.md                          5 hard gates + 6 soft scores
  scoring-rubric.md                 weights, min-floor, verdict, maturity-aware
  failure-patterns.md               regression cases (expandable)
  model-policy.md                   env-var driven, no hardcoded models
  output-schema.md                  JSON schemas + examples
scripts/
  validate_surface.py               deterministic checks, JSON out, stdlib only
  score_audit_json.py               composite + maturity-aware floor + verdict
ASSETS/                             (preserved from v2.0, still valid)
  anchor-doc-template.md
  codex-review-prompt.md
  element-prompt-template.md
  master-gallery-template.html      ← Stage 11 starts here, then customizes per anchor
  orchestration-decision-matrix.md
  planning-doc-template.md          (internal; the skill emits this implicitly)
  quality-gate-checklist.md
  shared-context-template.md
  surface-prompt-template.md
  vault-sync-template.md
  writeup-template.md
examples/
  2026-05-12-track-b-v2-wave.md     pilot example
  template-blank-project.md         blank shape for a new project
```

Removed in v3.0.0:
- `references/mode-resolution.md` — no modes to resolve any more.

---

## §10 — What carries over from v2.1

All v2.1.0 internal mechanics are kept; only the user-facing surface
changed:

| v2.1 mechanic | v3.0.0 status |
|---|---|
| Surface Contract preflight (§2) | kept, fully automatic; user never writes it |
| Deterministic validators (§3) | kept, automatic, Stage 6 |
| Hard gates + soft scores (§4) | kept, automatic, Stages 7-8 |
| Maturity-aware innovation floor (§4.4) | kept |
| Morphology sub-cause REDO vs FIX_NEEDED (§4.3) | kept |
| Fix-on-fail loop with quoted prior evidence (§5) | kept, automatic, Stage 10 |
| Cross-AI review trigger matrix (§6) | kept, automatic, Stage 9 |
| Machine-readable JSON output (§7) | kept |
| Closeout + regression-dataset update (§8) | kept, automatic, Stage 12 |
| Anti-patterns A1-A8 | kept; A9 + A10 added in v3.0.0 |
| ASSETS/ templates | preserved unchanged |
| examples/ | preserved unchanged |
| scripts/ (validate_surface.py + score_audit_json.py) | preserved unchanged |
| references/{gates,scoring-rubric,failure-patterns,model-policy,output-schema,surface-taxonomy}.md | preserved unchanged |

Removed (user-facing only — internal behavior stays):
- §0 Invocation Modes (4 modes collapsed into one pipeline)
- All `--mode=` / `--from=` / `--max-retries=` / `--quality-bar=` /
  `--surfaces=` / `--max-parallel=` / `--edit-skill=true` CLI flags
- `references/mode-resolution.md`
- "Plan-then-execute" stop for routine generation (still stops per §3)
- Two-key rule for skill self-edit (replaced by §3 case 3 plain language
  trigger)

---

## Cross-link

- Upstream:   `prototyping-ui-directions` (variant exploration before anchor lock)
- Downstream: `frontend-design` (Stage 4 merge into production-ready code)
- Sibling craft: `taste-skill` (single-page craft applied throughout)
- Foundation: `grill-with-docs` (anchor terminology clarification)
- Internal-pipeline siblings: see `references/skills-dependencies.md`
- v2.1 reference: see `CHANGELOG.md`
