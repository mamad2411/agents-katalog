---
name: vn-tone
description: "Polishes already-translated Vietnamese text so it reads natively in a target register (báo chí, semi-casual, bro, or pop-marketing). Fixes pronoun drift, missing particles, literal idioms, passive-voice calques, typography, and corporate translationese. Post-translation polish pass only — does NOT translate from other languages. For tone work on English/other languages, see humanize. Produces `.agents/mkt/content/[slug].vn-tone.md`."
argument-hint: "[vietnamese text or file path] [--register bao-chi|semi-casual|bro|pop-marketing]"
allowed-tools: Read Grep Glob Bash WebFetch
license: MIT
metadata:
  author: hungv47
  version: "1.0.0"
  budget: standard
  estimated-cost: "$0.08-0.20"
routing:
  intent-tags:
    - vietnamese-tone
    - vn-polish
    - localization-polish
    - translation-artifact-removal
    - vietnamese-register
  position: horizontal
  produces:
    - mkt/content/[slug].vn-tone.md
  consumes:
    - mkt/content/[slug].humanized.md
    - mkt/content/[slug].md
  requires: []
  defers-to:
    - skill: humanize
      when: "source text is in English and needs AI-pattern removal or voice injection first"
    - skill: copywriting
      when: "need to write new Vietnamese copy from scratch rather than polish translated text"
  parallel-with: []
  interactive: false
  estimated-complexity: low
---

# Vietnamese Tone Polish — Orchestrator

*Communication — Horizontal. Runs a three-agent pipeline (diagnose → polish → critic) to transform translated Vietnamese into natural, register-correct prose.*

**Core Question:** "Would a native Vietnamese writer of this target register write this exact text themselves — and would a native reader stumble anywhere?"

## Critical Gates — Read First

1. **Input must be Vietnamese.** This skill does not translate. If the input is English or any other language, STOP and tell the user to translate first (using `humanize` if it needs tone work in source language, or their preferred MT).
2. **Target register must be specified.** One of `bao-chi` / `semi-casual` / `bro` / `pop-marketing`. If ambiguous from context, ask the user before dispatching.
3. **Do NOT change facts.** Polishing means form, not content. Numbers, names, dates, quoted statements, claims, and named examples must survive the rewrite intact.
4. **Register is pair-locked.** The polisher picks one pronoun pair (self ↔ reader) at the start and holds it to the end. Drift is the #1 translation giveaway — catching it is the critic's primary gate.

## Philosophy

Machine-translated and non-native Vietnamese fails in four predictable ways: wrong pronoun pair for the register, missing sentence-final particles that carry casual warmth, literal idiom calques that land as nonsense, and corporate translationese that stacks abstract nouns the way English does. This skill fixes all four through a small, focused pipeline: diagnose the gap, polish the text, verify the result. Meaning is preserved unconditionally — the polisher operates only on form.

## Inputs Required

- **Vietnamese text** (paste or file path)
- **Target register** — one of:
  - `bao-chi` — professional news, formal editorial, institutional communications
  - `semi-casual` — tech community, blogger, essayist, SaaS docs for engaged users
  - `bro` — forum casual (specify subvariant: `bro-otofun` for Hanoi cụ-mợ / `bro-voz` for Voz ae-thím)
  - `pop-marketing` — consumer marketing, lifestyle content, brand voice, viral copy

## Optional Inputs

- **Brand glossary** — terms to preserve unchanged (brand names, product names, technical terms)
- **Dialect preference** — Northern (`nhé`, `dùng`, `bác`) or Southern (`nha`, `xài`, `chú`). Default: neutral.
- **User directives** — explicit overrides ("keep `quý khách`", "audience is ≥50yo", "keep English loanwords as-is")

## Output

- `.agents/mkt/content/[slug].vn-tone.md` — polished text with change log and status

## Quality Gate

Before delivering, the **critic agent** verifies:
- [ ] Zero Hard Tells from the 28-pattern catalog in `references/translation-artifacts.md`
- [ ] Pronoun pair held throughout (no drift)
- [ ] Particle density in target range (0% for báo chí, 15–25% for casual/pop/bro)
- [ ] Every number, name, date, and named example from original is preserved
- [ ] Typography normalized (no em dashes, no Oxford comma before `và`, no title case, no smart quotes, dates in DD/MM/YYYY)
- [ ] Read-aloud: no stumbles for a native reader
- [ ] Total critic score ≥28/36

### Absolute Prohibitions (zero tolerance)
These violate core register conventions so reliably that a single instance breaks the polish:
1. **No em dashes `—`.** VN is not English. Use comma, period, parentheses, or restructure.
2. **No `quý khách` / `quý vị`** outside explicit corporate formal notices. Pop and semi-casual use `bạn`; bro uses the subvariant's pronoun; báo chí uses no reader-address.
3. **No title-case VN headlines.** Sentence case only, proper nouns capitalized.
4. **No particles in `bao-chi`.** Zero `ạ`, `nhé`, `nhỉ`, `nha`, `đấy`. Báo chí is particle-free.
5. **No pronoun pair drift.** Whatever pair opens the text must close it. Mid-text drift is auto-FAIL.
6. **No dropped facts.** If the original has a number, name, or claim, the polished version has it too.
7. **No cliché stack.** Never two of `giải pháp toàn diện`, `trải nghiệm đột phá`, `tối ưu hóa`, `chuyển đổi số`, `hành trình` in the same paragraph. The polisher's job is to delete these when stacked.
8. **No literal idiom calques.** `Vào cuối ngày`, `đi về phía trước`, `nghĩ bên ngoài chiếc hộp`, `kẻ thay đổi trò chơi` — instant FAIL if any survive.

## Chain Position

Horizontal — polishes the output of any skill that produced Vietnamese text. Typical upstream: an external translation tool, an AI translator, or a human non-native writer. Can also polish Vietnamese content written natively but needing register alignment.

**Re-run triggers:** Target register changed, brand voice updated, corpus reference refreshed with new sources.

### Skill Deference
- **Source text is in English and needs AI-pattern/voice work before translation?** Run `humanize` on the English first, translate, then run `vn-tone` on the result.
- **Need new Vietnamese copy from scratch rather than polish existing?** Use `copywriting` with Vietnamese voice directives.
- **Already well-polished but needs A/B variants?** Use `copywriting` variant agent instead.

---

## Agent Manifest

| Agent | Layer | File | Focus |
|---|---|---|---|
| Diagnostic | 1 (single) | `agents/diagnostic-agent.md` | Scans for translation artifacts, assesses register gap, produces violation log with priority fixes |
| Polisher | 2 (sequential) | `agents/polisher-agent.md` | Applies register-correct rewriting based on violation log; preserves meaning and structure |
| Critic | 2 (final) | `agents/critic-agent.md` | Three-pass audit, 36-point scoring, PASS/FAIL with specific re-dispatch feedback |

### Shared References (read by multiple agents)
- `references/vn-tone-corpus.md` — Annotated corpus of 4 primary registers (báo chí, semi-casual, bro, pop-marketing) with pronoun systems, particles, vocabulary, rhythm, typography, real examples from live-scraped sources (VnExpress, Chinhphu.vn, Tinhte, Spiderum, Otofun, Voz, Kenh14). Used by all three agents.
- `references/translation-artifacts.md` — 28 common EN→VN translation giveaways across 10 categories, ranked Hard/Soft. Used by diagnostic (detection) and polisher (fixing) and critic (verification).

---

## Routing Logic

Small skill, two routes.

### Route A: Standard Polish (default)
**When:** User provides Vietnamese text and target register.

```
1. Pre-dispatch: Gather context (Step 0 below)
2. LAYER 1 — Dispatch diagnostic-agent
3. Present diagnosis briefly to user:
   "Found [N] Hard Tells, [N] Soft Tells. Top priority: [3 bullets].
    Estimated rewrite: [light/moderate/heavy]. Proceed?"
4. LAYER 2 — Dispatch SEQUENTIALLY:
   - polisher-agent (receives diagnostic output + original text)
   - critic-agent (receives polisher output + original for comparison)
5. If critic returns FAIL → re-dispatch polisher-agent with critic feedback (max 2 cycles)
6. Deliver artifact
```

### Route B: Called by Another Skill
**When:** Invoked by `content-create`, `copywriting`, `humanize`, or any pipeline that produces Vietnamese output.

```
1. Pre-dispatch: Read context from calling skill's brief — pull target register from brand voice or user directive
2. If content passed a prior VN polish already: skip diagnostic, dispatch polisher-agent + critic-agent only
3. Otherwise: Follow Route A (full pipeline)
4. Return polished output to calling skill
```

---

## Step 0: Pre-Dispatch Context Gathering

### Register Resolution
Determine target register from (in priority order):
1. Explicit `--register` argument from user
2. Brand voice from `.agents/product-context.md` (if present) — map brand voice adjectives to register: "authoritative/institutional" → bao-chi; "warm/community" → semi-casual; "in-group/community" → bro; "young/lifestyle/consumer" → pop-marketing
3. Content type inferred from upstream artifact (news article → bao-chi; blog post → semi-casual; landing page → pop-marketing)
4. Ask the user — do not guess silently

### Product Context Check
Check for `.agents/product-context.md`. If available, read for brand voice and any dialect/register preferences. Note in pre-writing if the brand specifies Northern/Southern dialect or has a glossary of terms to preserve.

### Required Artifacts
None — polishes any Vietnamese text standalone.

### Optional Artifacts
| Artifact | Source | Benefit |
|---|---|---|
| `product-context.md` | icp-research | Brand voice for register mapping, glossary |
| `content/[slug].md` | content-create | Original Vietnamese content |
| `content/[slug].humanized.md` | humanize | Pre-humanized content to polish further |

### Pre-Writing Assembly
Compile and pass to every agent:
- **target_register** — `bao-chi` \| `semi-casual` \| `bro` \| `pop-marketing` (with optional subvariant)
- **source_language** — usually "en" or "unknown" (for diagnosis context)
- **brand_glossary** — list of terms to preserve unchanged
- **dialect_preference** — `north` \| `south` \| `neutral` (default: neutral)
- **user_directives** — explicit overrides
- **original_text** — the Vietnamese input, exactly as provided

---

## Dispatch Protocol

### How to spawn a sub-agent

For each agent below, use the **Agent tool**:

1. **Read** the agent instruction file (e.g., `agents/diagnostic-agent.md`) — include its FULL content in the Agent prompt
2. **Append** the brief and pre-writing context after the instructions
3. **Resolve reference paths to absolute** — replace relative paths with absolute paths rooted at this skill's directory (e.g., `references/vn-tone-corpus.md` becomes `/Users/you/marketing-skills/vn-tone/references/vn-tone-corpus.md`)
4. **Pass original text as `brief`**, not as a file path — the agent should operate on text directly
5. If **feedback** exists (critic FAIL cycle), append it at the end with header "## Critic Feedback — Address Every Point"

### Single-agent fallback

If multi-agent dispatch is unavailable, execute the pipeline in-context:

1. **Diagnose:** Read the target register profile in `vn-tone-corpus.md` and the violation catalog in `translation-artifacts.md`. Scan the input for Hard Tells, pronoun drift, and register gaps. Produce a violation log.
2. **Polish:** Apply the fixes from the log. Lock one pronoun pair. Walk the text sentence by sentence. Preserve all facts.
3. **Critic:** Run three passes (Hard Tells binary, register consistency, read-aloud). Score against the 36-point rubric. Re-polish once if needed.

Output quality should be equivalent — multi-agent optimizes for focus, not capability.

---

## Layer 1: Diagnosis

Spawn the diagnostic agent. Pass:
- `brief` = the Vietnamese input text
- `pre-writing` = the assembled context from Step 0
- `references` = absolute paths to `vn-tone-corpus.md` and `translation-artifacts.md`
- `upstream` = null (Layer 1)

After the agent returns, **present a brief diagnosis to the user** before proceeding:
- Hard Tell count + Soft Tell count
- Top 3 priority fixes (one line each)
- Rewrite scope estimate (light / moderate / heavy)
- Register gap summary (e.g., "currently corporate formal, needs to reach pop-marketing")

Ask: **"Proceed with the polish, or review specific flagged items first?"**

If the user wants to review, walk through each Hard Tell and confirm which to fix vs. keep (e.g., "keep `quý khách` — luxury brand directive"). Pass the user's decisions to polisher-agent as `user_directives` in pre-writing.

---

## Layer 2: Sequential Pipeline

Dispatch these agents **ONE AT A TIME, IN ORDER**:

```
polisher-agent → critic-agent
```

| Step | Agent | File | Receives |
|---|---|---|---|
| 1 | Polisher | `agents/polisher-agent.md` | Diagnostic output (upstream) + original text (brief) + user directives (pre-writing) |
| 2 | Critic | `agents/critic-agent.md` | Polisher output (upstream) + original text (brief) for side-by-side meaning check |

Each agent returns the full document + a change log. The orchestrator passes the complete polisher output to the critic.

---

## Critic Gate

The critic returns one of two verdicts:

### PASS
Text meets all quality standards. Score ≥28/36. Zero Hard Tells. Deliver the critic's approved output as the final artifact.

### FAIL
Critic returns specific failures with:
- Which text failed and on which dimension
- Specific fix instructions with rule citations
- Which agent to re-dispatch (always polisher-agent for this skill)

**Rewrite loop:**
1. Read critic's failure report
2. Re-dispatch polisher-agent with critic feedback as the `feedback` input
3. Run the modified output back through the critic
4. **Maximum 2 rewrite cycles.** After 2 failures, deliver the text with critic annotations and flag to the user: "Scored [X]/36 — manual review recommended on [specific issues]."

---

## Artifact Template

```markdown
---
skill: vn-tone
version: 1
date: [today's date]
status: done | done_with_concerns | blocked | needs_context
target_register: [bao-chi | semi-casual | bro | pop-marketing]
subvariant: [if applicable: bro-otofun | bro-voz]
dialect: [north | south | neutral]
critic_score: [N]/36
---

# VN Tone Polish: [Original Title or Slug]

## Polish Summary

| Metric | Value |
|---|---|
| Original words | [count] |
| Polished words | [count] |
| Hard Tells found | [count] |
| Hard Tells fixed | [count] |
| Soft Tells fixed | [count] |
| Pronoun pair | [self ↔ reader] |
| Particle density | [actual %] (target [range]) |
| Critic score | [N]/36 |
| Cycles used | [1 or 2] |

## Change Log

| Location | Before | After | Rule |
|---|---|---|---|
| [P-S ref] | "[original]" | "[polished]" | [rule ID] |

---

## Polished Text

[Full rewritten Vietnamese text here]

---

## Status

**[DONE | DONE_WITH_CONCERNS | BLOCKED | NEEDS_CONTEXT]**

[If DONE_WITH_CONCERNS: list the remaining Soft Tells and why they were kept. If BLOCKED: state what's missing. If NEEDS_CONTEXT: state what upstream skill would provide it.]
```

> On re-run: rename existing artifact to `[slug].vn-tone.v[N].md` and create new with incremented version.

## Next Step

Polished Vietnamese text is ready for publication. If the content is marketing copy, consider running `lp-optimization` for conversion checks on the Vietnamese landing-page version, or `attribution` to set tracking before launch.

---

## Worked Example — Standard Polish (Route A)

**Input:** A SaaS onboarding email, machine-translated from English to Vietnamese, 4 sentences, ~75 words.

### Pre-Dispatch
- **Target register:** `pop-marketing` (brand voice is "warm, young, friendly")
- **Dialect:** neutral
- **Brand glossary:** "Acme" preserved as brand name
- **Source language:** en

### Original (Input)
> "Quý khách thân mến! Chúng tôi rất hân hạnh chào đón quý khách đến với Acme — giải pháp toàn diện cho hành trình chuyển đổi số của quý khách. Trong những tuần tới, chúng tôi sẽ gửi cho quý khách một loạt các email để giúp quý khách tối ưu hóa trải nghiệm của mình. Hãy nhấp vào đây để bắt đầu!"

### Layer 1 — Diagnostic Output (abridged)

**Register gap:** Currently stiff corporate formal (`chúng tôi ↔ quý khách`, zero particles, cliché-stacked). Target is pop-marketing (`chúng mình ↔ bạn`, light particles, emotive). **Heavy rewrite needed.**

**Hard Tells:** A2 (quý khách × 5), E3 (giải pháp toàn diện, hành trình chuyển đổi số, tối ưu hóa — dead corporate clichés stacked), F1 (em dash), D7 (sẽ gửi — unnecessary future marker), B1 (bare imperative "Hãy nhấp" with no softener), D5 (một loạt các — redundant plural).

**Priority fixes:**
1. Replace `chúng tôi ↔ quý khách` with `chúng mình ↔ bạn` — fixes 5 violations in one pass.
2. Kill the cliché stack — rewrite Acme intro around what the product actually does.
3. Add softeners on the CTA.

### User Checkpoint
"Found 10 Hard Tell instances (6 rule types), 2 Soft Tells. Biggest issues: wrong pronoun pair (5×), corporate cliché stack, bare imperative CTA. Heavy rewrite recommended. Proceed?"

User confirms.

### Layer 2 — Polisher Output

**Polished Text:**
> "Bạn ơi, chào mừng bạn đến với Acme nha! Chúng mình sẽ đồng hành cùng bạn để làm việc nhanh và gọn hơn. Mấy tuần tới bạn sẽ nhận được một chuỗi email nhỏ, chỉ bạn cách khai thác hết mọi thứ hay ho của Acme. Nhấn vào đây để bắt đầu liền!"

**Change Log (abridged):**
| Before | After | Rule |
|---|---|---|
| "Quý khách thân mến!" | "Bạn ơi, ... nha!" | A2, particle add |
| "Chúng tôi rất hân hạnh chào đón quý khách" | "chào mừng bạn" | A2, I2 (throat-clearing) |
| "— giải pháp toàn diện cho hành trình chuyển đổi số của quý khách" | "Chúng mình sẽ đồng hành cùng bạn để làm việc nhanh và gọn hơn" | F1 (em dash), E3 (dead corporate cliché stack), I1 (noun stack → verb) |
| "sẽ gửi cho quý khách một loạt các email" | "bạn sẽ nhận được một chuỗi email nhỏ" | D7 (future marker kept for genuine near-future), D5 (redundant plural), pronoun pair |
| "giúp quý khách tối ưu hóa trải nghiệm của mình" | "chỉ bạn cách khai thác hết mọi thứ hay ho" | A2, E1/E4 (sinify → pop intensifier) |
| "Hãy nhấp vào đây để bắt đầu!" | "Nhấn vào đây để bắt đầu liền!" | B1 (imperative softened via native verb + urgency adverb + `!`), native `nhấn` |

### Critic Output

- **Pass 1 (Hard Tells):** All 10 instances cleared. Score: 1 (pass the gate).
- **Pass 2 (Register Consistency):** `chúng mình ↔ bạn` held across all 4 sentences. Particle density: `nha` = 1/4 sentences (25%) — at the target ceiling, within range. Note: `ơi` in `Bạn ơi` is a mid-sentence vocative, not a sentence-final particle, so it does not count toward density. Score: 10.
- **Pass 3 (Read-aloud):** No stumbles. Rhythm varied (7/12/19/10 words). One experience anchor missing ("Dùng Acme là thấy ngay..." would add warmth) — minor. Score: 9.
- **Meaning preservation:** All claims intact (welcome, email series, CTA). Score: 10.
- **Typography:** em dash removed, sentence case, no smart quotes. Score: 5.
- **Total: 35/36. PASS.**

### Final Artifact (excerpt)

```markdown
---
skill: vn-tone
version: 1
date: 2026-04-15
status: done
target_register: pop-marketing
dialect: neutral
critic_score: 35
---

# VN Tone Polish: Acme Onboarding Email

## Polish Summary
| Metric | Value |
|---|---|
| Original words | 75 |
| Polished words | 59 |
| Hard Tells fixed | 10/10 |
| Pronoun pair | chúng mình ↔ bạn |
| Particle density | 25% (1/4 sentences — at target ceiling, within range) |
| Critic score | 35/36 |

## Polished Text
Bạn ơi, chào mừng bạn đến với Acme nha! Chúng mình sẽ đồng hành cùng bạn để làm việc nhanh và gọn hơn. Mấy tuần tới bạn sẽ nhận được một chuỗi email nhỏ, chỉ bạn cách khai thác hết mọi thứ hay ho của Acme. Nhấn vào đây để bắt đầu liền!

## Status
**DONE** — Register pair `chúng mình ↔ bạn` held across all 4 sentences. Particle density at 25% (target ceiling). All 10 Hard Tell instances (6 rule types) cleared. Meaning preserved. One minor experience anchor missing (could add "Dùng thử là thấy ngay..." for warmth) — flagged but not blocking.
```

---

## Anti-Patterns

**Polishing before diagnosing.** Dispatching the polisher without a violation log. The polisher needs the diagnostic as a work order — without it, it rewrites by vibes and misses drift. INSTEAD: always run diagnostic-agent first.

**Guessing the register.** Running the pipeline without confirming target register with the user or pulling it from brand voice. The register choice determines every subsequent decision. INSTEAD: resolve register in Step 0 or ask.

**Cross-contaminating subvariants.** Polishing Otofun `em + cụ` text toward Voz `mình + ae` because "both are bro". They are distinct speech communities with non-interchangeable pronouns. INSTEAD: specify subvariant or ask.

**Particle over-injection.** Adding `nha/nhé/đấy` to every sentence in a pop rewrite. The target range is 15–25%. Every-sentence injection reads performative. INSTEAD: vary — some sentences end bare, some with particles.

**Clichés left standing.** Polishing around `giải pháp toàn diện`, `trải nghiệm đột phá`, `chuyển đổi số` instead of deleting them. These are corporate-translationese fingerprints and must go in pop/casual registers. INSTEAD: delete the phrase, rewrite around what the product actually does.

**Preserving em dashes.** Thinking em dashes are "just punctuation". They are English intrusion in VN. INSTEAD: convert every `—` to comma, period, parentheses, or restructure.

**Scope creep.** Touching facts, numbers, or named examples to "improve flow". Polish is form-only. INSTEAD: preserve every factual anchor; flag rather than cut.

**Register cosplay.** A corporate brand asking for `bro` register and the polisher dutifully producing Voz-slang output. Brands that try this register usually fail. INSTEAD: flag the register choice as risky to the user before polishing; confirm they want it.

**Ignoring the critic's FAIL.** Delivering failed text because "it's mostly good". Hard Tells are binary. INSTEAD: re-dispatch the polisher with specific feedback. Max 2 cycles, then deliver with annotations.

**One-pass polishing.** Running diagnostic, polish, and critic all in one dispatch. Each pass has a different focus (detect, fix, verify). Combining them produces worse results. INSTEAD: follow the sequential pipeline.

**Loanword overscrub.** Replacing every English loanword even in tech register where they belong. `API`, `webhook`, `gaming`, `router` are fine in semi-casual tech. INSTEAD: calibrate by register — drop loanwords in báo chí, keep them in semi-casual/pop where natural.

---

## Agent Files

### Sub-Agent Instructions (agents/)
- [agents/diagnostic-agent.md](agents/diagnostic-agent.md) — Scans for translation artifacts, assesses register gap, produces violation log
- [agents/polisher-agent.md](agents/polisher-agent.md) — Applies register-correct rewriting, preserves meaning, holds pronoun pair
- [agents/critic-agent.md](agents/critic-agent.md) — Three-pass audit, 36-point scoring, PASS/FAIL with re-dispatch feedback

### Shared References (references/)
- [references/vn-tone-corpus.md](references/vn-tone-corpus.md) — Annotated corpus of 4 VN registers with pronouns, particles, vocabulary, rhythm, typography, and real examples from live-scraped sources (VnExpress, Chinhphu.vn, Tinhte, Spiderum, Otofun, Voz, Kenh14)
- [references/translation-artifacts.md](references/translation-artifacts.md) — 28 EN→VN translation giveaways across 10 categories, Hard/Soft severity, fix rules

---

## References

| Reference | Use For |
|---|---|
| [vn-tone-corpus.md](references/vn-tone-corpus.md) | Register profiles, pronoun pair system, particle cheat sheets, real annotated examples per register |
| [translation-artifacts.md](references/translation-artifacts.md) | 28 Hard/Soft tells to detect and fix — calques, passives, corporate translationese, typography |
