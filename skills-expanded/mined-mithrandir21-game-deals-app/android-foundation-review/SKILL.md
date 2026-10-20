---
name: android-foundation-review
description: >
  Deep architectural review of an Android (or KMP) project by spawning parallel specialist
  sub-agents. Produces a senior-engineer-grade written report covering architecture,
  layering & separation, modern patterns/tooling, testing, performance, and security.
  Use this skill whenever the user asks to "review", "audit", "assess", or "critique" an
  Android or Kotlin Multiplatform project — even if they phrase it casually like "take a
  look at my Android app and tell me what you think". Also trigger on requests for an
  "architecture review", "code quality check", "tech debt assessment", "performance audit",
  "security review", or "modernization audit" when the repo contains Android/Gradle/Kotlin
  artifacts.
---

# Android Project Review Skill

## Purpose

Perform a thorough, opinionated architectural review of an Android (or KMP) project by
dispatching six specialist sub-agents in parallel, then synthesizing their findings into
a single, cohesive report written for an audience of senior Android engineers.

The review is NOT a line-by-line code review. It is a structural and strategic assessment:
does the project have a sound architecture, does it leverage the modern Android ecosystem,
and is it built to be safe, fast, and maintainable as the team scales?

---

## Step 0 — Locate the project and capture shared context

Identify the project root. Look for `settings.gradle.kts` (or `.gradle`), the top-level
`build.gradle.kts`, and the `app/` module. If the repo is a multi-module project, every
Gradle module is a first-class input to the review.

Run a structural scan before spawning agents. Every agent receives this output as shared
context so they don't duplicate the discovery work.

```bash
# Prefer ripgrep if available — it's faster and respects .gitignore by default.
RG=$(command -v rg || true)
SEARCH() { if [ -n "$RG" ]; then rg "$@"; else grep -rn "$@"; fi }

# Module list
echo "=== Modules ==="
find . -name "build.gradle.kts" -o -name "build.gradle" 2>/dev/null \
  | grep -v "/build/" | sort

# Source tree shape
echo "=== Source set layout (sample) ==="
find . -path "*/src/*/kotlin/*" -o -path "*/src/*/java/*" 2>/dev/null \
  | grep -v "/build/" | head -60

# Top-level config
echo "=== settings.gradle ==="
cat settings.gradle.kts 2>/dev/null || cat settings.gradle 2>/dev/null

echo "=== Version catalog ==="
cat gradle/libs.versions.toml 2>/dev/null | head -120

echo "=== Root build script ==="
cat build.gradle.kts 2>/dev/null | head -60 || cat build.gradle 2>/dev/null | head -60

echo "=== gradle.properties (perf flags) ==="
cat gradle.properties 2>/dev/null | grep -Ei "cache|parallel|configuration|jvmargs|kotlin\." || true

echo "=== Gradle/AGP versions ==="
cat gradle/wrapper/gradle-wrapper.properties 2>/dev/null | grep distributionUrl

# KMP detection — surface this for every agent, even though we don't elevate KMP.
echo "=== KMP signals ==="
grep -l "kotlin(\"multiplatform\")\|org.jetbrains.kotlin.multiplatform" \
  $(find . -name "build.gradle.kts" 2>/dev/null) 2>/dev/null | head -10

# Quick size estimate
echo "=== Approx LOC (Kotlin) ==="
find . -path "*/src/main/*" -name "*.kt" 2>/dev/null \
  | xargs wc -l 2>/dev/null | tail -1
```

Save the output. It becomes the `{SHARED_CONTEXT}` block in every agent prompt.

---

## Step 1 — Spawn the six specialist agents

Launch all six agents **in the same turn** so they run in parallel. Each agent receives:

1. The **shared context** from Step 0 (module list, version catalog, KMP signals, etc.).
2. A directive to read its dedicated reference file under `references/`.
3. A workspace path to write its findings to.

| Agent | Reference file | Focus |
|-------|---------------|-------|
| Architecture | `references/architecture-agent.md` | Module graph, dependency direction, DI strategy, navigation, error handling, observability |
| Layering & Separation | `references/layering-and-separation-agent.md` | Data → Domain → Presentation discipline, ViewModel responsibility, mapper hygiene, feature boundaries |
| Modern Patterns & Tooling | `references/modern-patterns-agent.md` | Compose, coroutines/Flow, Gradle/KSP, networking, storage, accessibility, release health, KMP idioms |
| Testing | `references/testing-agent.md` | Test pyramid shape, doubles strategy, coroutine/Flow testing, Compose UI testing, CI signals |
| Performance | `references/performance-agent.md` | Startup, Compose stability & recomposition, Baseline Profiles, Macrobenchmark, R8, jank, memory |
| Security & Privacy | `references/security-agent.md` | Sensitive data storage, network security, secrets, permissions, manifest hardening, dependency hygiene |

**Cross-cutting concerns that don't get their own agent:**
- **Accessibility** — covered inside Modern Patterns (Compose semantics) and Layering & Separation (UI responsibility).
- **Observability** — covered inside Architecture (logging/crash reporting as cross-cutting concerns) and Testing (CI signals).
- **KMP** — covered as a subsection inside the relevant agents (Modern Patterns for libraries, Layering for source-set discipline, Testing for `commonTest`). Not elevated to its own agent.

### Agent prompt template

Use this as the base prompt for each sub-agent (fill in the placeholders):

```
You are a specialist Android reviewer focusing exclusively on **{FOCUS_AREA}**.

Read the reference file at {SKILL_PATH}/references/{REFERENCE_FILE} for your
detailed review checklist and grading rubric.

## Shared project context
{SHARED_CONTEXT}

## Your task
1. Explore the codebase to gather evidence for every item in your checklist.
   Use ripgrep (`rg`) if available, otherwise `grep -rn`. Use `find`, `cat`,
   and `head`/`tail` liberally. Read actual source files — do not guess from
   file names alone.
2. For each checklist item, record:
   - **Verdict**: STRONG, ADEQUATE, WEAK, MISSING, or N/A
   - **Evidence**: concrete file paths, class names, and code snippets (≤15 lines each).
   - **Impact**: why this matters to maintainability, scalability, or correctness.
   - **Recommendation** (if WEAK or MISSING): specific, actionable next step naming
     the file or module to change.
3. If something falls outside your remit, note it as `OUT_OF_SCOPE: see {other_agent}`
   and move on — don't try to cover everything yourself.
4. Write your findings to: {WORKSPACE}/findings-{AGENT_SLUG}.md
5. **Hard cap: keep the entire findings file under 800 words.** Be terse — one or two
   sentences per checklist item is enough. Prioritize concrete `file:line` evidence
   and a specific recommendation over prose. The synthesizer needs signal, not essays.

Format findings as Markdown with H2 headings per checklist item.
Be blunt and precise. Your audience is a staff-level Android engineer who has seen
everything — skip the preamble, lead with the verdict. Stay pragmatic: when a
project chose Koin over Hilt or Compose-only over Views, evaluate whether the
choice is consistent and well-executed, not whether it matches your default.
```

---

## Step 2 — Synthesize the report

Once all six agents have completed, read every `findings-*.md` file and produce the
final report. The report follows the structure in `references/report-template.md`.

### Synthesis rules

1. **De-duplicate.** With six parallel agents, the same observation will surface from
   multiple angles — that's expected and load-bearing (multiple confirmations strengthen
   a finding). In the final report, merge them into a single coherent finding and cite
   each agent that flagged it.

2. **Resolve conflicts explicitly.** When agents disagree (e.g., Architecture says DI is
   STRONG because Hilt is wired up, but Layering says ViewModels bypass DI with manual
   construction), the synthesis should:
   - State both observations.
   - Determine which is correct by spot-checking the evidence yourself.
   - Record the resolved verdict in the scorecard with a note explaining the disagreement.

3. **Prioritize.** Rank findings into three tiers:
   - **Critical** — architectural flaws, security holes, or performance traps that will
     compound as the team or user base scales (wrong dependency direction, no DI, secrets
     in source, untestable ViewModels, no Baseline Profile on a slow-starting app).
   - **Significant** — patterns that slow the team or risk users but don't block them
     (inconsistent error handling, missing mapper layer, no UI testing, kapt instead of KSP,
     no certificate pinning on a finance app).
   - **Refinement** — polish items (naming conventions, Gradle hygiene, stability annotations
     on hot Composables, edge-case accessibility).

4. **Be specific.** Every finding must reference at least one concrete file or class.
   "Consider adding tests" is worthless. "`PaymentViewModel` has 14 public functions, none
   tested, and directly calls `RetrofitService.charge()` — extract `ProcessPaymentUseCase`
   and write unit tests covering success/decline/network-failure paths" is useful.

5. **Acknowledge strengths.** If the project does something well, say so and say why it
   matters. Engineers reading the review should know what to protect, not just what to fix.

6. **Tone.** Direct, pragmatic, peer-to-peer. No corporate fluff. When the project chose
   Koin over Hilt, evaluate whether it's well-applied — don't reflexively mark it down
   for not matching a default.

---

## Step 3 — Deliver

Write the final report to `{WORKSPACE}/android-review-report.md` and present it.

For large projects (10+ modules, 50k+ LOC) also produce a one-page executive summary
with the top 5 findings and a recommended action sequence.

---

## Notes

- **KMP projects.** When KMP signals are present (`kotlin("multiplatform")` plugin,
  `commonMain` source sets), every agent should additionally evaluate the relevant KMP
  dimension: source-set boundaries (Layering), `expect`/`actual` usage and Swift interop
  hygiene (Modern Patterns), `commonTest` coverage (Testing), and cross-platform library
  choices (Modern Patterns: Ktor, SQLDelight, Kotlinx Serialization, Koin/Kotlin Inject).
- **Single-module monoliths.** The Architecture agent should flag this and the report
  should include a suggested modularization roadmap.
- **Build files are first-class.** Dependency versions, plugin configuration, R8 setup,
  and convention plugins are review targets, not background noise.
- **When agents need to coordinate** (e.g., Performance wants R8 detail and Security
  also wants R8 detail), each agent reviews its own angle. The synthesizer merges.
