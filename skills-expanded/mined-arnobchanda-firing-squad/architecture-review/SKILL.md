---
name: architecture-review
description: Critique an architecture document from 7 distinct expert viewpoints in parallel, then synthesize. Use when the user has an architecture.md (typically with supporting context.md and ADRs) and wants a multi-perspective review board critique. Spawns 7 isolated subagents (Doomer, Premortem, Adversary, Integrator, Performance Engineer, Pragmatist, Defender) plus a Chair synthesizer. Triggers on requests like "review this architecture", "critique my design doc", "run the architecture panel", or any time the user references an architecture.md they want challenged from multiple angles.
---

# Architecture Review Panel

You are orchestrating a synthetic architecture review board. Seven expert personas each critique the same architecture document from a non-overlapping viewpoint, in parallel. An eighth persona (the Chair) synthesizes their outputs into a ranked action list with explicit conflict resolution.

## When to use

The user has written or is iterating on an architecture document — usually `architecture.md` with supporting files like `context.md` and a directory of ADRs (Architecture Decision Records) — and wants it stress-tested from multiple expert angles before committing to the design.

## Inputs

Before dispatching, locate and read the architecture artifacts. Look in this order:

1. If the user specified a path or file, use that.
2. Otherwise, look in the current working directory for:
   - `architecture.md` (the main doc — required)
   - `context.md` (background/motivation — read if present)
   - `adr/` or `adrs/` or `decisions/` directory (read all `.md` files inside if present)
   - `scale.md` (deployment scale and threat model — read if present; otherwise elicit from the user, see Step 1.5 below)
   - `accepted-risks.md` (risks the architect has deliberately accepted — read if present; otherwise elicit, see Step 1.5)
3. If `architecture.md` doesn't exist, ask the user where the document is. Do not guess.

Read all relevant files into context before dispatching subagents.

## Workflow

### Step 1: Confirm scope

Show the user the files you found:

> Found these documents for review:
> - architecture.md (X lines)
> - context.md (X lines)
> - adr/0001-foo.md, adr/0002-bar.md, ... (N ADRs)
> - scale.md (present / missing)
> - accepted-risks.md (present / missing)

### Step 1.5: Elicit scale context and accepted risks (CRITICAL)

**This step is non-negotiable.** Personas without scale context invent their own threat models and produce miscalibrated reviews (defaulting to nation-state adversaries, hyperscale traffic, Fortune-500 compliance posture). The single biggest determinant of review quality is whether the personas know what stage and scale the system is at.

If `scale.md` is missing, ask the user this **exact prompt**, then wait for their response:

> Before dispatching the panel, I need a short scale and stage context paragraph so the personas calibrate their critiques. Please answer in 4–8 sentences:
>
> 1. **Stage:** Pre-revenue / early customers / scaling / mature. How many customers/users/sites today? How many expected at the next milestone you're designing toward?
> 2. **Threat model:** Who is the realistic adversary? (Insider, opportunistic attacker, targeted attacker, nation-state.) What is the realistic worst-case impact of compromise?
> 3. **Compliance posture:** What standards are in scope today? What standards are on the roadmap? (SOC 2, IEC 62443, ASIL, NERC CIP, HIPAA, none, etc.)
> 4. **Device/deployment class:** Where does this run? (Consumer device, customer-premises industrial enclosure, cloud-only, hybrid edge.) Who has physical access?
> 5. **Named ceilings:** Any hard limits you're designing toward? (e.g. "no more than 100 sites in next 18 months", "max 50 concurrent users", "single-region only".)
>
> If you don't know an answer, write "unknown" — that's a valid input. Skipping this step entirely is not.

If `accepted-risks.md` is missing, ask:

> Also: do you have any risks you've already deliberately accepted? (e.g. "no CRL/OCSP in v1 — known", "single VPS, no HA — known", "plaintext token at rest — known".) The personas will treat accepted risks differently from undiscovered ones. If none, write "none".

Save the user's responses verbatim. You will inject them into every persona's system prompt.

### Step 2: Confirm dispatch

> Dispatching 7-persona review panel + Chair synthesizer with this scale context:
>
> [paste scale paragraph]
>
> Accepted risks: [paste or "none stated"]
>
> This will take a few minutes. Proceed? (yes/no)

Wait for confirmation. If they want to adjust scale context, accommodate.

### Step 3: Dispatch personas in parallel

Use the Task tool to dispatch **7 subagents in parallel** (single message, multiple tool calls). Each subagent gets:

- The full content of `architecture.md`, `context.md`, and all ADRs (paste as part of the prompt, do not rely on the subagent re-reading from disk)
- The scale context paragraph (verbatim)
- The accepted-risks list (verbatim)
- The persona instructions from `personas/<persona-name>.md`
- An instruction to return its output in the exact structure defined in that persona file

The 7 personas are:

| # | Persona | File |
|---|---|---|
| 1 | Doomer (Operational) | `personas/doomer-operational.md` |
| 2 | Premortem (Strategic) | `personas/premortem-strategic.md` |
| 3 | Adversary (Red Team) | `personas/adversary.md` |
| 4 | Integrator | `personas/integrator.md` |
| 5 | Performance Engineer | `personas/performance-engineer.md` |
| 6 | Pragmatist | `personas/pragmatist.md` |
| 7 | Defender | `personas/defender.md` |

For each subagent, the prompt structure is:

```
You are acting as the following persona in an architecture review panel:

<persona_instructions>
[paste full content of personas/<name>.md here]
</persona_instructions>

<scale_context>
[verbatim user response to scale prompt — calibrate ALL findings against this]
</scale_context>

<accepted_risks>
[verbatim user response to accepted-risks prompt, or "none stated"]
</accepted_risks>

Here is the architecture documentation under review:

<architecture_md>
[full content of architecture.md]
</architecture_md>

<context_md>
[full content of context.md if present, else "Not provided"]
</context_md>

<adrs>
[concatenated content of all ADR files, each prefixed with its filename]
</adrs>

Produce your critique in the exact output structure specified in your persona instructions. Do not break character. Do not reference the other personas — you are working independently. Calibrate every severity rating against the scale context above. For each accepted risk, you may EITHER reinforce it (note an implication the architect may have missed) OR escalate it (note that the scale has changed in a way that invalidates the acceptance) — do not re-raise an accepted risk as if it were a new finding.
```

### Step 4: Collect outputs

When all 7 subagents return, collect their outputs verbatim. Do not edit or summarize them yet.

### Step 5: Dispatch the Chair synthesizer

Use the Task tool once more, dispatching the Chair subagent. Pass it:

- The original `architecture.md` (full content)
- The scale context paragraph (verbatim)
- The accepted-risks list (verbatim)
- All 7 persona outputs (verbatim, each labeled by persona name)
- The instructions from `personas/chair.md`

### Step 6: Assemble the final report

Build the final report with this exact structure:

```markdown
# Architecture Review — <date>

**Documents reviewed:** <list of files>

**Scale context:**
<verbatim scale paragraph>

**Accepted risks:**
<verbatim accepted-risks list, or "None stated">

---

## Chair's Synthesis

<output from Chair subagent>

---

## Persona Critiques

### 1. Doomer (Operational)
<verbatim output>

### 2. Premortem (Strategic)
<verbatim output>

### 3. Adversary
<verbatim output>

### 4. Integrator
<verbatim output>

### 5. Performance Engineer
<verbatim output>

### 6. Pragmatist
<verbatim output>

### 7. Defender
<verbatim output>

---

## Structured findings appendix (machine-readable)

```yaml
[Chair-emitted YAML block — one record per finding, see chair.md for schema]
```
```

The Chair's synthesis goes **first** so the user sees the ranked action list immediately. Raw persona outputs follow for drilling. The structured YAML appendix at the end is for diffing future reviews and scaffolding ADRs.

### Step 7: Save and display

1. Create directory `./reviews/` if it doesn't exist.
2. Save the report to `./reviews/YYYY-MM-DD-architecture-review.md` (use today's date; if a file with that name exists, append `-2`, `-3`, etc.).
3. Display the **full report inline** in the chat — do not just say "saved to file". The user wants both.
4. End with a one-line summary: `Saved to ./reviews/<filename>. <N> structural-critical issues, <M> contextual-critical issues, <K> convergent findings (≥3 personas).`

## Rules

- **Always elicit scale context and accepted risks** before dispatching. Skipping Step 1.5 is the single biggest quality regression possible.
- **Always run all 7 personas in parallel** in a single message with multiple Task tool calls. Sequential dispatch defeats the point.
- **Never let personas contaminate each other.** Each subagent must see only the architecture + scale + accepted risks, not other personas' outputs. Only the Chair sees everything.
- **Inject scale context verbatim** into every persona's prompt. Do not summarize or paraphrase it.
- **Do not skip the Chair.** The synthesis is what makes the panel actionable; raw outputs are too much to act on directly.
- **Preserve persona outputs verbatim** in the final report. Do not paraphrase or "clean up" their critiques.
- **The Chair recommends defaults but does not decide.** Conflicts are surfaced with a recommended default, a confidence level, the preserved dissenting view, and named flip-triggers — not arbitrated away.
