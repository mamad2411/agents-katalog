---
name: matilha-compose
description: "You MUST use this skill before any software-construction work — planning, designing, researching, building, reviewing, dispatching, merging, or modifying features/systems/products/components/agents/workflows — whenever matilha is installed (this skill is visible in your ambient skill list). Matilha is a methodology wrapper around superpowers:* skills; compose routes user intent to the right matilha phase (scout/plan/design/hunt/gather/review/howl) or dispatches to superpowers:brainstorming with pack-aware preamble. Runs standalone when superpowers is absent. Detects companion packs (matilha-*-pack namespace) as optional enrichment. Lazy-bootstraps matilha project structure on demand."
category: matilha
version: "1.0.0"
optional_companions: ["superpowers:brainstorming", "matilha-plan", "matilha-design"]
---

## When this fires

Fires BEFORE any creative-work or software-construction skill (including `superpowers:brainstorming`, `superpowers:writing-plans`) when BOTH conditions hold:

1. **Matilha is installed** — this skill (`matilha:matilha-compose`) is visible in the ambient skill list. This is implicit: if you are reading this body, matilha is loaded for the current workspace.

2. **Software-construction intent** — the user prompt signals any of:
   - Planning / spec authoring ("plan this", "write a spec", "lay out phases")
   - Designing / UX / UI ("how should this look", "which UI", "what component")
   - Researching / discovery ("what are the options for...", "investigate...")
   - Building / implementing ("I'm building...", "adding...", "construindo...")
   - Reviewing / quality ("review this PR", "check this code")
   - Dispatching waves / parallel work ("split this into SPs", "dispatch waves")
   - Status / next action ("where am I?", "what's next?")
   - General creative exploration ("I'm thinking about...", "exploring...")

Project-context signals (`docs/matilha/` directory, `project-status.md` file, any `matilha-*-pack` skill visible) are **supplementary context for routing decisions**, not activation gates. Matilha methodology applies broadly whenever the plugin is installed — these signals only shift how compose dispatches (to which specific matilha phase skill vs. superpowers skill).

**Positive examples (compose fires):**
- "Estou construindo MVP de 4 semanas... Como estruturo os agents?" → general creative → brainstorming with pack preamble (harness-pack if visible)
- "Quero planejar a feature de export CSV" → planning intent → matilha-plan (may lazy-bootstrap docs/matilha/)
- "What's the current phase?" → status intent → matilha-howl
- "Review my code changes" → quality intent → superpowers:brainstorming or matilha-review depending on what matilha finds

**Negative examples (compose does NOT fire):**
- Compose is NOT installed (different workspace) → this skill is absent from ambient list
- Prompt is pure factual / non-construction ("what's the capital of France?") → no software-construction signal
- User invokes a specific skill directly via slash command (e.g., `/matilha-howl`) → direct invocation bypasses compose

## Preconditions

- Ambient skill list available (primary signal source).
- Matilha project context verifiable via one of the three signals above.

## Execution Workflow

Six steps, executed in order — one preflight step followed by five routing steps:

**Step 0 — Preflight dependency check (lightweight, advisory).**

Before routing, silently check the workspace for matilha harness dependencies. The goal: surface fixable gaps (missing `CLAUDE.md`, missing priority-rule block) that would otherwise cause compose to lose activation on subsequent turns — the sigil and phase routing only work when the priority rule is ambient in the session.

The check is **always advisory, never blocking**. Compose continues to Step 1 regardless of outcome.

1. **Check `./CLAUDE.md`** via the Read tool.
   - Read fails / file does not exist → flag `claude_md_missing`.
   - Read succeeds, content lacks the literal string `<!-- matilha-start v` → flag `claude_md_no_marker`.
   - Read succeeds, marker present → no flag (healthy state).

2. **Soft-check multi-harness config files** (best effort, only if file exists — do not create noise for users who don't use these harnesses):
   - `./AGENTS.md` (Codex / OpenAI agentic CLIs): if present without `<!-- matilha-start v` → flag `agents_md_no_marker`. Absent file → skip silently.
   - `./GEMINI.md` (Gemini CLI): if present without `<!-- matilha-start v` → flag `gemini_md_no_marker`. Absent file → skip silently.
   - `./.cursor/rules/` directory: if present and no file under it references matilha → flag `cursor_no_rule`. Absent directory → skip silently.

3. **Emit a ONE-LINE preflight notice to the user per flag set**, in this order of priority. Use the exact formats below (friendly, actionable, non-blocking):
   - `claude_md_missing`:
     ```
     ⚠️ Matilha preflight: no CLAUDE.md in this workspace. The activation priority rule is not ambient — compose may lose activation on future turns. Run `/matilha-install` to bootstrap, or copy `docs/matilha/templates/claude-matilha-snippet.md` manually.
     ```
   - `claude_md_no_marker`:
     ```
     ⚠️ Matilha preflight: CLAUDE.md exists but lacks the matilha priority-rule block. Run `/matilha-install` and accept the "Bootstrap CLAUDE.md" option to merge the block idempotently.
     ```
   - `agents_md_no_marker` / `gemini_md_no_marker` / `cursor_no_rule`: emit only if the corresponding file/dir is present AND no `claude_md_*` flag fired (to avoid notice storm). Format:
     ```
     ℹ️ Matilha preflight: <file> present without matilha block — if you use <harness> alongside Claude Code, bootstrap via `/matilha-install` for cross-harness parity.
     ```

4. **Emit, then continue.** Do not wait for user confirmation. Do not repeat the notice within the same turn. Proceed immediately to Step 1 (Pack detection). If the user acts on the notice (runs `/matilha-install`), subsequent compose invocations pass the check silently and the notice stops — natural self-healing, no state to maintain.

**What this step does NOT do:**
- Does NOT write any file. Bootstrap is the user's explicit action via `/matilha-install`.
- Does NOT block or delay routing. Advisory only.
- Does NOT check companion-pack installation state (that's Step 1's job).
- Does NOT check `project-status.md` or `docs/matilha/` — those are lazy-bootstrapped by downstream phase skills, not prerequisites for compose.

**Rationale**: a user who installs matilha-skills via `/plugin install` on a fresh project never triggers `matilha-init`. Without CLAUDE.md, the priority rule is not loaded → compose may fail to win activation against `superpowers:brainstorming` → the sigil never appears → user assumes matilha "doesn't work". Step 0 surfaces this gap on first fire and points to the fix.

**Step 1 — Pack detection.**

Inspect the ambient skill list visible in the current session. Identify skills whose plugin namespace matches the literal pattern `matilha-*-pack` (for instance, `matilha-harness-pack:harness-architecture`, `matilha-ux-pack:ux-reservatorio-boa-vontade`, `matilha-growth-pack:growth-aarrr`). Group identified skills by plugin namespace. For each pack, note:

- Plugin name (derived from namespace, e.g., `matilha-harness-pack`).
- Pack-scoped skill names and their descriptions (visible in the ambient list).

Do NOT maintain any hardcoded list of skill prefixes or pack names in this skill body. The ambient skill list is the sole source of truth — packs uninstalled disappear from it; new packs appear automatically. No edits to this skill are required to pick up new packs, new skills within a pack, or skill removals.

If no skills match the `matilha-*-pack` namespace pattern, proceed to Step 3 with zero packs detected.

**Step 2 — Intent classification (routing-table first, then prose semantic).**

**Step 2a — Routing table lookup (deterministic).**

Read `routing-table.md` co-located with this skill (same directory: `skills/matilha-compose/`). Parse each non-comment line as `keyword | pack-namespace`. For each entry, check case-insensitively whether the user prompt contains the keyword. If it does, mark that pack as `relevant` immediately — no LLM inference needed for this pack.

Fallback: if the file is unavailable or unreadable, skip 2a and proceed to 2b.

**Step 2b — Prose semantic classification (for packs not matched by 2a).**

For each detected pack, decide whether the user prompt touches its domain in ANY way. Use the pack's shipped skill descriptions (visible in the ambient list) to inform the decision. Binary output per pack: `relevant` | `off-topic`.

**Strongly bias toward `relevant`**: if the pack touches ANY aspect of the user's prompt (even a minor one), classify it `relevant`. The preamble serves brainstorming by surfacing the pack's vocabulary — even a tangential pack is more useful than no pack context. Only mark `off-topic` when the pack's domain is clearly unrelated (e.g., growth-pack for a pure-infrastructure prompt with zero product/user-experience dimension).

When in doubt, classify `relevant`. The brainstorming downstream will naturally skip irrelevant skills during exploration — the cost of including a marginal pack is low; the cost of omitting a relevant one is a missed aha moment.

Do NOT use hardcoded keyword maps. Rely on semantic judgment based on skill descriptions.

**Step 3 — Dispatch decision.**

Choose the terminal destination based on intent-to-phase classification. Matilha phase skills handle their own pack-aware enrichment — compose routes without emitting preamble for them. Only the `superpowers:brainstorming` path gets preamble emission.

| Intent signal | Dispatch target | Preamble emitted by compose? | Notes |
|---|---|---|---|
| Planning / spec authoring | `matilha:matilha-plan` | No | matilha-plan runs own pack logic; lazy-bootstraps docs/matilha/specs/ if missing |
| Design / UX / UI | `matilha:matilha-design` | No | matilha-design runs own pack logic |
| Discovery / research | `matilha:matilha-scout` | No | matilha-scout dispatches research subagents; lazy-bootstraps docs/matilha/research/ |
| Status / next action | `matilha:matilha-howl` | No | Read-only; lazy-bootstraps project-status.md stub if missing |
| Dispatch waves / parallel SPs | `matilha:matilha-hunt` | No | Requires existing plan.md — if absent, fall back to matilha-plan first |
| Merge / regression / wave integration | `matilha:matilha-gather` | No | Requires active wave status |
| Quality review | `matilha:matilha-review` | No | (Wave 3c runtime pending — currently stub) |
| Deploy / production gate | `matilha:matilha-den` | No | Phase 60 |
| Teammate onboarding | `matilha:matilha-pack` | No | Phase 70 |
| General creative exploration ("I'm building", "exploring", "thinking about") | `superpowers:brainstorming` | **Yes** (if ≥1 pack classified relevant) | Only terminal-brainstorming path gets enrichment |
| Implementation plan authoring (existing spec in context) | `superpowers:writing-plans` | No | Superpowers handles craft; matilha tracks phase advancement via plan status |
| Ambiguous | `superpowers:brainstorming` with preamble | Yes | Default — brainstorming explores intent, may surface need for phase-specific skill |

**Lazy bootstrap rule**: if the chosen matilha phase skill needs filesystem structure that doesn't yet exist (e.g., matilha-plan writes to `docs/matilha/specs/<slug>-spec.md`), the skill itself creates the directory on first write. Compose does not pre-create — that's delegated to the downstream skill's body. This keeps compose stateless.

**Superpowers fallback**: if the chosen matilha phase skill delegates to a superpowers skill (e.g., matilha-plan delegates to `superpowers:brainstorming` during clarifying questions), that delegation is the matilha phase skill's responsibility, not compose's.

**Step 4 — Build preamble (if terminal is brainstorming AND ≥1 pack classified `relevant`).**

**Default is EMIT.** If any installed pack is relevant (by the bias-inclusive rule from Step 2), build the preamble. Skip only when:
- Zero companion packs installed (ambient list contains no `matilha-*-pack` namespaces), OR
- All installed packs are clearly off-topic (e.g., only growth-pack installed, and prompt is pure DevOps/infrastructure with zero product dimension).

In any other case — especially when the prompt is technical/creative/software-construction-shaped and at least one pack is installed — EMIT the compact sigil + atmospheric + pack lines + closing. This is the matilha signature and the user's aha moment; withholding it when a pack is available wastes the harness.

Use this canonical template. The goal combines three purposes at once: (a) signal to the user that matilha's methodology layer activated, (b) make the "aha" moment visible (LLM mirroring domain-specific language proves it *read* the prompt), (c) inject pack context for brainstorming to weave skills naturally.

```text

matilha
                 _   _ _ _
 _ __ ___   __ _| |_(_) | |__   __ _
| '_ ' _ \ / _' | __| | | '_ \ / _' |
| | | | | | (_| | |_| | | | | | (_| |
|_| |_| |_|\__,_|\__|_|_|_| |_|\__,_|

You lead. Agents hunt.

The pack sensed familiar territory: <specific domain phrase mirroring
the user's prompt — e.g., "event orchestration with Lambda, EventBridge
and DynamoDB" or "signup flow focused on activation" or "agent
architecture with planner/executor">.

  ▸ <pack-short-1>   <skill-short-1> · <skill-short-2> · <skill-short-3>
                     <skill-short-4> · <skill-short-5>

  ▸ <pack-short-2>   <skill-short-1> · <skill-short-2> · <skill-short-3>
                     <skill-short-4> · <skill-short-5>

[repeat per pack classified yes]

Brainstorming ahead. Skills enter as topics surface.
```

**Semiotics of the sigil** (why this matters, not just decoration):
- **Compact wordmark** — keeps the activation marker readable in chat transcripts and terminal recordings.
- **Tagline** — `You lead. Agents hunt.` grounds the harness promise without flooding the session.
- Emitted inline from the canonical template above. Do not call shell hooks or scripts to render it.

**Language rules for the atmospheric paragraph** (line starting "The pack sensed familiar territory"):
- The domain phrase MUST mirror concrete language from the user's prompt (technology names, specific nouns). This is the aha-moment trigger — the user sees "oh, it actually understood what I'm asking about, not generic help."
- Keep it to one sentence maximum.
- Do not summarize the prompt — name the *territory* (the domain / problem space).

**Pack lines** — visual format:
- One entry per pack classified yes.
- `▸ <pack-short>` — strip `matilha-` prefix and `-pack` suffix from pack name. Examples: `matilha-sysdesign-pack` → `sysdesign`, `matilha-software-arch-pack` → `sw-arch`, `matilha-software-eng-pack` → `sw-eng`, `matilha-security-pack` → `security`, `matilha-ux-pack` → `ux`, `matilha-growth-pack` → `growth`, `matilha-harness-pack` → `harness`.
- Skill names: strip the domain prefix (e.g., `sysdesign-`, `swarch-`, `swsec-`, `sweng-`, `ux-`, `cog-`, `growth-`, `harness-`). Skill `sysdesign-nfr-clarification` → `nfr-clarification`. This avoids redundancy since the pack name already declares the domain.
- Max 3 skills per line. Overflow wraps to the next line, indented to align with the first skill (pack name column is 16 chars, padded with spaces).
- `·` (middle dot, U+00B7) as separator between skills on the same line.
- One blank line between packs.
- Skill names only, no inline descriptions. Brainstorming invokes skills via Skill tool for detail.

**Example rendered output** (for reference, not to copy verbatim):
```
  ▸ sysdesign    nfr-clarification · latency-targets · scalability-h-vs-v
                 consistency-cap · rate-limiting · monitoring-4-golden

  ▸ sw-arch      lambda-chain-shape · handler-as-adapter · measure-before-scale
                 dual-store-source-of-truth · dependency-direction

  ▸ security     lgpd-operational · backend-auth-layer · rate-limiting-defense
                 iam-least-privilege · encryption · secrets-manager
```

**Closing line** (`Brainstorming ahead. Skills enter as topics surface.`):
- Signals to user that the conversation flow continues; establishes anticipation without listing all skills upfront.

**If zero packs classified yes**: skip preamble entirely, including the sigil. The pack doesn't howl when there's no territory to hunt (silent pass-through Case C). The user just sees brainstorming running directly.

**Step 5 — Emit + invoke (storytelling mode, not debug mode).**

Emit the complete preamble as regular assistant text, then invoke the target skill via the Skill tool.

The preamble is the canonical text block built in Step 4:

1. Sigil ASCII art.
2. Atmospheric paragraph.
3. Pack lines.
4. Closing transition.

Do not use Bash, shell hooks, plugin-root paths, or external renderer scripts for the sigil. Shell permission prompts break the flow and reduce cross-CLI compatibility.

Example sequence the user sees:

```
⏺ matilha:matilha-compose
[inline compact sigil from Step 4]
The pack sensed familiar territory: <domain phrase mirroring user prompt>.

<pack-name> at your side → <skill-1>, <skill-2>, <skill-3>, <skill-4>, <skill-5>.

Brainstorming ahead. Skills enter as topics surface.

⏺ superpowers:brainstorming
```

After emitting the preamble, invoke the target skill via the Skill tool. Then stop — let the target skill take over.

**Do NOT narrate your internal steps** ("Step 1 — Pack detection...", "Step 2 — Intent classification...") in the user-facing output. Those steps happen inside your reasoning; only the inline sigil + atmospheric text + skill invocation should reach the user. Exception: if the user explicitly asks you to explain what compose did (e.g., `/matilha-compose --debug` or "explain your routing"), then show the steps.

**Silent pass-through exception**: when zero packs are classified relevant (Case C), skip both the sigil AND the preamble text. The pack does not howl without territory.

Goal: the user experiences compose as an atmospheric opening — the pack's presence acknowledged with the inline sigil, then the language-mirroring atmospheric text reinforces domain understanding, then brainstorming begins.

If no preamble (pass-through or routing to plan/design): invoke target skill via Skill tool directly.

## Rules: Do

- Always include the guidance paragraph in the preamble when emitted.
- Always include skill names (backtick-quoted) in per-pack skill lists.
- Prefer false-positive pack inclusion over missing a pack.
- Cite pack origin ("from matilha-harness-pack") only when ambiguity arises about which pack a skill belongs to.
- Trust the ambient skill list as the sole detection signal.

## Rules: Don't

- Don't hardcode pack names or skill prefixes in detection logic. Prefixes like those used by companion packs may appear in this skill body only inside examples or illustrative contexts — never inside detection instructions. Use the `matilha-*-pack` namespace pattern as the sole detection mechanism.
- Don't fire when matilha plugin is not installed (this skill is absent from the ambient list). No self-check needed — if you are reading this body, matilha is loaded.
- Don't duplicate brainstorming's clarifying-questions flow when `superpowers:brainstorming` is available — dispatch to it.
- Don't inject full skill bodies into the preamble — descriptions only.
- Don't emit empty preambles ("no packs detected...") — if pack list is empty, just pass through.
- Don't emit a preamble when routing to matilha-plan or matilha-design — those skills handle their own enrichment.

## Expected Behavior

With matilha-compose in the activation loop, software-construction prompts flow:

1. User writes any software-construction prompt (planning, designing, building, reviewing, exploring).
2. matilha-compose wins activation over `superpowers:brainstorming` and other creative-work skills (description gate + CLAUDE.md ambient priority).
3. Compose classifies intent into a matilha phase (or "general creative") and detects installed companion packs.
4. Compose routes to the appropriate matilha phase skill (no preamble — they run their own enrichment) OR to `superpowers:brainstorming` (with pack preamble if packs are relevant).
5. The terminal skill runs — matilha phase skills persist artifacts to `docs/matilha/` (lazy-bootstrapping as needed); brainstorming explores intent with pack-aware context.
6. User gets methodology-guided output whether the workspace was pre-bootstrapped as a matilha project or not.

The user's experience: methodology guidance everywhere matilha is installed, with pack enrichment where packs are installed, without any need to run matilha-init explicitly. Matilha project structure (docs/matilha/, project-status.md) materializes on demand when matilha phase skills need it.

## Quality Gates

- If ≥1 pack classified `yes`, preamble contains at least one per-pack section when terminal is brainstorming.
- Preamble always contains the final Guidance paragraph when emitted.
- Target skill invoked via the Skill tool (not narrated in prose).
- Detection logic contains no hardcoded pack names or skill prefixes.

## Companion Integration

`matilha-compose` is the methodology orchestrator and companion-pack-aware gateway. Relationships:

**Superpowers (craft layer):**
- **superpowers:brainstorming** — common dispatch target for general creative exploration. Compose emits pack preamble before invoking when packs are relevant.
- **superpowers:writing-plans** — invoked when user has an existing spec and wants an implementation plan; compose routes without preamble (superpowers handles the craft, matilha tracks phase advancement).
- **superpowers:*** other skills — compose generally hands off craft concerns (TDD, debugging, verification) to superpowers without interference.

**Matilha phase skills (methodology layer):**
- **matilha-scout** — research dispatch for discovery-intent prompts. Lazy-bootstraps `docs/matilha/research/`.
- **matilha-plan** — spec + plan authoring for planning-intent prompts. Lazy-bootstraps `docs/matilha/specs/` and `docs/matilha/plans/`.
- **matilha-design** — UX/UI guidance for design-intent prompts.
- **matilha-hunt / matilha-gather / matilha-review / matilha-den / matilha-pack** — later-phase skills (dispatch, merge, quality, deploy, onboarding).
- **matilha-howl** — status reporter for "where am I?" prompts. Lazy-bootstraps `project-status.md`.

**Companion packs (domain knowledge layer):**
- **Any skill with plugin namespace `matilha-*-pack`** (e.g., `matilha-harness-pack:harness-architecture`, `matilha-ux-pack:ux-reservatorio-boa-vontade`) — detected at runtime via ambient skill list; referenced by name in the emitted preamble when compose dispatches to brainstorming; available for direct invocation by the downstream skill via the Skill tool.

**Standalone mode**: when `superpowers:*` skills are absent, compose and matilha phase skills implement inline fallback flows (clarifying questions, spec drafting, etc.) using matilha's own methodology content. Matilha is never hostage to superpowers — it enhances superpowers when present and runs independently when absent.

The detection pattern here is canonical for Matilha. When `matilha-plan` or `matilha-design` perform their own pack-aware enrichment (delegating to brainstorming with preamble), they reference this skill as the template source.

## Pack awareness

This section documents the detection + classification contract in auditable prose. Validator enforces the invariants below.

**Detection contract:**
- Signal: ambient skill list, inspected for plugin namespaces matching the literal pattern `matilha-*-pack`.
- Excluded: hardcoded skill prefixes in any form. Prefixes from companion packs may appear in this skill body only inside examples or illustrative contexts — never inside detection instructions.
- Self-healing: pack uninstalled → disappears from ambient list → not detected. Pack added → appears → detected. New pack with fresh domain → author names plugin `matilha-<domain>-pack` → detected without editing this skill.

**Classification contract:**
- Method: prose semantic classification by the LLM executing this skill.
- Output: per-pack `yes` | `no` | `partial`.
- Bias: err inclusive.
- Do not use hardcoded keyword maps or subagent dispatch.

**Cross-reference guarantee:**
- `matilha-plan` and `matilha-design` reference this skill's preamble template. When the template evolves, propagate via grep and edit.

## Fallback semantics

Cases are organized along two axes: (a) superpowers availability, (b) pack availability. Applied AFTER intent classification in Step 2 when the dispatch target (Step 3) resolves to `superpowers:brainstorming` specifically — matilha phase skill routes use their own downstream logic.

**Case A — happy path (superpowers present, ≥1 relevant pack)**: Detect → classify → preamble → emit → invoke brainstorming. Terminal skill surfaces pack skills during exploration.

**Case B — matilha standalone with packs (superpowers absent, ≥1 pack)**: Run matilha-internal clarifying flow inline using the built preamble as context guide. Steps:
1. Ask the user ONE clarifying question at a time, drawing on the most-relevant pack skill's domain.
2. After 3–5 clarifying questions, summarize intent and propose 2–3 approaches drawing on pack skills.
3. On approach approval, invoke an appropriate matilha phase skill (matilha-plan if planning-shaped, matilha-design if design-shaped) or output inline guidance.

**Case C — silent pass-through (superpowers present, zero packs)**: Skip preamble construction → invoke `superpowers:brainstorming` directly without any preamble. Output is indistinguishable from brainstorming-without-compose. Do NOT emit "no packs detected" notice. Matilha methodology value still lands via the routing itself (compose fired, observed intent was general creative, correctly handed off).

**Case D — matilha methodology standalone (both absent)**: Run matilha-internal clarifying flow inline using methodology core (phases from `methodology/`, design heuristics from matilha-design, etc.). Equivalent to "matilha works when nothing else is installed".

**Invariants across all cases:**
- Never crash on absent dependencies.
- Empty preamble never emitted.
- Matilha methodology guidance is always accessible — activation gate is plugin-installed, not project-configured.
- Project structure (`docs/matilha/`, `project-status.md`) is created lazily by downstream phase skills when they need to write artifacts — not a prerequisite for compose firing.

**What compose does NOT fallback**: intent-classification logic is always prose-semantic. No alternate keyword-map path. No "simple mode" for quick dispatch. The classification is cheap (LLM already running) and the correctness is worth the consistency.

## Output Artifacts

None. Compose is a dispatcher, not a writer.

Optional: emit a log line to `docs/matilha/compose-log.md` capturing (timestamp, detected packs, classified intent per pack, routing decision). Opt-in, not required for Wave 5d ship.

## Example Constraint Language

- **Must**: detect packs via `matilha-*-pack` namespace inspection (no other detection mechanism permitted); emit guidance paragraph in every emitted preamble; invoke target skill via Skill tool.
- **Should**: err inclusive in classification; cap per-pack skill list at ~8.
- **May**: emit an optional log entry to `docs/matilha/compose-log.md` for observability.

## Troubleshooting

- **"superpowers:brainstorming still wins activation"** → Description strength alone does not reliably win activation. The primary mechanism is the `CRITICAL — activation priority in matilha projects` section in the plugin's CLAUDE.md, which is loaded ambiently. Verify that CLAUDE.md contains the priority instruction and the user's session loaded it. Description gate is a secondary reinforcement.
- **"Preamble too large (> 60 lines)"** → Trim per-pack skill lists to top 5 most intent-relevant. Drop packs classified `partial` if preamble remains over budget.
- **"Pack detected but its skills don't surface in downstream exploration"** → Strengthen the guidance paragraph with a concrete example of how to reference a pack skill during clarifying questions.
- **"Compose fires in a non-matilha project"** → Verify none of the three matilha-project signals present (docs/matilha/, project-status.md, matilha-*-pack namespace in skill list). If all absent, treat this as a description-gate false-positive — immediately invoke `superpowers:brainstorming` without preamble and exit.

## CLI shortcut (optional)

No CLI equivalent in Wave 5d. The matilha CLI has filesystem access and is deterministic by construction — composition logic is redundant in CLI mode. A future `matilha compose --detect-packs` subcommand could expose deterministic detection for power-user introspection, but is out of scope for this wave.
