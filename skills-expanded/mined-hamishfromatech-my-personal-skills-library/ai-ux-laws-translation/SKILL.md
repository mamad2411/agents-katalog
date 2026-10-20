---
name: ai-ux-laws-translation
description: Translate the classic UX heuristics and laws (Jakob's Law, Hick's Law, Doherty Threshold, Aesthetic-Usability Effect, Miller's Law, Fitts's Law, Tesler's Law, Postel's Law, Parkinson's Law, and the Peak-End Rule) into concrete AI-product design rules. Use when designing or auditing AI interfaces (chat assistants, coding agents, generative UI, agent dashboards, recommendation surfaces) to ensure they satisfy human cognitive constraints the AI layer tends to violate. NOT for non-AI interfaces, or for cognitive-load-reduction techniques already covered by cognitive-load-reduction-ai-scaffolding (this skill supplies the underlying laws those techniques implement).
---

# AI UX Laws Translation

## Overview

Every mature UX law was derived from the architecture of human attention, memory, and motor control — architecture that does not change because a screen now contains an AI. Yet AI interfaces systematically violate these laws: chat agents ignore Hick's Law by presenting infinite conversational paths, generative UI ignores Jakob's Law by inventing novel layouts every render, and "explainable AI" panels ignore Miller's Law by dumping 7+ reasoning steps at once. This skill is a translation layer: each classic law becomes an AI-specific design rule, an anti-pattern to avoid, and an A-Tech application.

The value: a shared, evidence-backed vocabulary for saying "no" to AI feature ideas that feel innovative but break how human cognition actually works.

## When to Use

- Designing or auditing an AI chat, agent, copilot, or generative-UI surface
- Reviewing a feature proposal that "uses AI" where the AI output adds options, steps, latency, or visual novelty
- Building an agent dashboard, recommendation panel, or explanation surface
- Deciding whether a generative UI adaptation should be allowed, frozen, or discarded
- Creating a design-review checklist for AI product teams
- Teaching developers (Be Practical) or community builders (Builder's Club) the cognitive constraints AI interfaces must respect

NOT for:
- Non-AI interface design (apply the laws directly from UX literature)
- Detailed cognitive-load scaffolding techniques (use `cognitive-load-reduction-ai-scaffolding` and `cognitive-load-reduction-for-ide`)
- Trust-calibration mechanics (use `trust-calibration-ux-pattern` and `ai-explanation-ability-cue-trap`)
- Calm-technology patterns (use `calm-technology-ai-coding`) — this skill supplies the *laws* that justify calm-technology choices

## Core Process / Workflow

### Step 1 — Learn the Ten Laws and Their AI Translations

| # | Law (classic) | What it says about humans | AI translation (the rule for AI interfaces) | Common AI anti-pattern |
|---|---------------|---------------------------|---------------------------------------------|------------------------|
| 1 | **Jakob's Law** | Users spend most of their time on *other* sites/apps; they expect yours to work the same way | An AI surface should reuse familiar interaction patterns (command palette, sidebar, inline suggestion, diff view); novelty in *output*, not in *interaction chrome* | Reinventing the chat panel, button placement, or navigation for "AI-native" reasons |
| 2 | **Hick's Law** | Decision time grows with the number of options presented | Cap AI-presented choices at 3–4; offer a default; collapse the rest behind "more" | An agent that returns 8 possible next actions and asks the user to pick |
| 3 | **Doherty Threshold** | Interaction feels instantaneous when system response is under 400 ms | AI latency must be *perceived* as instant — use streaming, skeletons, and progressive results; anything > 400 ms needs a perceived-progress signal | Blank screen while a model generates a full response |
| 4 | **Aesthetic-Usability Effect** | Perceived beauty increases perceived ease of use (and tolerance of minor flaws) | AI surfaces that look polished are trusted more and judged more usable — but this is the mechanism behind the ability-cue trap; invest in polish *and* in substance | Shipping a powerful AI feature in a crude UI, or polishing a shallow AI feature to mask its weakness |
| 5 | **Miller's Law** | Working memory holds 7 ± 2 chunks | Present AI reasoning as ≤ 7 chunks; group steps; collapse detail by default; let the user expand | Dumping a 12-step chain-of-thought trace at full depth on first render |
| 6 | **Fitts's Law** | Time to hit a target grows with distance and shrinks with target size | Accept/reject buttons for AI suggestions must be large and adjacent to the suggestion, not floating in a toolbar | Tiny "Accept" link far from the inline diff it applies to |
| 7 | **Tesler's Law** | Every process has an irreducible complexity; it must live somewhere | The complexity of verifying AI output cannot be eliminated, only relocated — move it to the *system* (automated checks) not the *user* (manual review) | "AI makes it effortless" claims that hide the verification work the human must still do |
| 8 | **Postel's Law** | Be liberal in what you accept, conservative in what you send | An AI agent should accept messy, ambiguous user intent liberally, but produce strict, well-formed, verifiable output | An agent that is strict about prompt format but loose and unverified in its generated code |
| 9 | **Parkinson's Law** | Work expands to fill the time available | AI tasks with no time bound expand; set explicit budgets (token, time, step count) and surface them | An agent that "thinks" indefinitely with no deadline or budget indicator |
| 10 | **Peak-End Rule** | Memory of an experience is dominated by its peak and its end | Engineer the AI interaction's peak (the moment of insight) and its end (a clean, confirmed, reversible close); a weak ending erases a strong middle | An agent session that ends with an ambiguous "done?" state and no clear summary |

### Step 2 — Run the AI UX Law Audit

For any AI feature or surface, walk the checklist:

```
1. Jakob  — Does it reuse a familiar interaction pattern? If not, is the novelty in the output, not the chrome?
2. Hick   — How many choices does the AI present at once? Is there a clear default? (target ≤ 4)
3. Doherty — Is the first useful signal on screen within 400 ms (real or perceived via streaming)?
4. Aesthetic — Is the surface polished? If yes, is the substance equal to the polish (no ability-cue masking)?
5. Miller  — How many chunks must the user hold in working memory to act? (target ≤ 7, collapse the rest)
6. Fitts   — Are the accept/reject/edit controls large and adjacent to the AI output they control?
7. Tesler  — Where has the irreducible verification complexity been moved — to the system or to the user?
8. Postel  — Does the agent accept messy input but produce strict, verifiable output?
9. Parkinson — Is there an explicit time/token/step budget? Is it visible to the user?
10. Peak-End — What is the engineered peak? What is the engineered ending? Is the ending clean and reversible?
```

Score: 9–10 satisfied = law-respecting AI surface; 6–8 = needs targeted fixes; ≤ 5 = redesign against the violated laws.

### Step 3 — Resolve the AI-Specific Tensions

Several laws pull in opposite directions for AI interfaces. Resolve them explicitly:

| Tension | Laws in conflict | Resolution |
|---------|------------------|------------|
| Novelty vs. familiarity | Jakob (familiarity) vs. generative UI's premise (novelty) | Keep the *interaction chrome* familiar (Jakob); let the *content* be novel. Generative UI may reflow content, not reinvent controls. |
| Polish vs. substance | Aesthetic-Usability (polish builds trust) vs. Ability-Cue Trap (polish can mask shallowness) | Invest in polish *and* in genuine depth; add uncertainty disclosure so the polish does not become an unearned ability cue. |
| Speed vs. verification | Doherty (instant) vs. Tesler (verification is irreducible) | Make *generation* feel instant (Doherty) but make *verification* explicit and system-assisted (Tesler) — the speed budget applies to the response, not to the human's check. |
| Few options vs. AI breadth | Hick (few choices) vs. agents that can do many things | Show ≤ 4 next-actions by default; gate the rest behind a "more" affordance; never present the full action space at once. |

## A-Tech Application Matrix

### A-Coder (AI Coding IDE)
- **Jakob:** Default to familiar IDE patterns (inline diff, side-by-side preview, command palette). AI novelty lives in *what* it generates, not in *how* the user accepts it.
- **Hick:** When the agent proposes next steps, show 3 with a default highlighted; never a list of 8.
- **Doherty:** Stream completions and reasoning; show a skeleton/progress indicator within 400 ms of the request.
- **Miller:** Chain-of-thought panels collapse to ≤ 7 top-level steps; deeper steps behind expand.
- **Fitts:** Accept/reject buttons are large, inline, adjacent to the diff — not in a remote toolbar.
- **Tesler:** The verification complexity is moved to adversarial agentic test layers and static analysis, not to the human reviewer's eyes.
- **Postel:** A-Coder accepts loose natural-language intent but produces strict, linted, tested, typed code.
- **Parkinson:** Every agent session has a visible token/time budget with a soft deadline; long-running sessions checkpoint and report.
- **Peak-End:** The peak is the moment the diff resolves a hard problem; the end is a clean, reviewed, reversible commit summary.

### Be Practical (Playbooks / Curriculum)
- **Curriculum module:** "The Ten Laws Your AI Interface Is Probably Breaking" — each law, the AI anti-pattern, a real screenshot to critique, and a fix.
- **Exercise:** Audit a popular AI product against the 10-point checklist; score it; propose the minimum-viable fix for each violation.
- **Case study:** A generative UI that violated Jakob's Law (users could not form a mental model) and the redesign that restored familiar chrome while keeping generative content.

### Builder's Club (Community)
- **Design-review rubric:** every community AI project is reviewed against the 10-point audit before showcase.
- **Law-of-the-month:** each month, one law is the community theme — submissions, talks, and audits focus on that law.
- **Open-source component library:** reusable UI primitives that encode the laws (chunked reasoning panel, adjacent accept/reject diff, streaming-skeleton, token-budget indicator) so community projects inherit law-respecting defaults.

## Cross-References

- `cognitive-science-and-ux/cognitive-load-reduction-ai-scaffolding` — the scaffolding *techniques* that implement Miller's and Hick's Laws for AI
- `cognitive-science-and-ux/cognitive-load-reduction-for-ide` — IDE-specific load reduction (Doherty and Tesler applied to coding tools)
- `cognitive-science-and-ux/ai-explanation-ability-cue-trap` — why the Aesthetic-Usability polish can manufacture unearned trust (the substance-vs-polish tension)
- `cognitive-science-and-ux/trust-calibration-ux-pattern` — trust escalation that respects Tesler's Law (verification is relocated, not eliminated)
- `cognitive-science-and-ux/chain-of-thought-ux-reasoning-transparency` — the reasoning-display spectrum that implements Miller's Law for explanations
- `cognitive-science-and-ux/generative-ui-dynamic-interface-design` — the "predictable dynamism" principle is Jakob's Law applied to generative UI
- `cognitive-science-and-ux/peak-end-rule-demo-design` — the Peak-End Rule skill, specialized for demos and onboarding
- `developer-experience-and-flow/calm-technology-ai-coding` — calm-technology patterns are the application of Doherty, Hick, and Tesler to AI coding tools
- `developer-experience-and-flow/devex-verification-bottleneck-framework` — the verification bottleneck *is* Tesler's Law made visible; the framework relocates the irreducible complexity to the system

## Anti-Patterns

| Anti-Pattern | Law Violated | Why It Fails |
|--------------|--------------|-------------|
| Reinventing the chat/panel chrome for "AI-native" reasons | Jakob | Users can't transfer their mental model; learning cost is imposed for no cognitive gain |
| Presenting all possible agent actions at once | Hick | Decision paralysis; the user scans instead of acting |
| Blank screen during generation | Doherty | Perceived latency feels worse than actual latency; user assumes it's broken |
| Polished UI on a shallow AI feature | Aesthetic-Usability + Ability-Cue Trap | Polish manufactures trust the substance hasn't earned |
| Full-depth reasoning trace on first render | Miller | Working-memory overflow; the user skims and misses the key step |
| Tiny remote accept/reject controls | Fitts | Slow, error-prone acceptance; users mis-click |
| "AI makes it effortless" with no verification path | Tesler | The complexity is hidden in the user's later debugging, not eliminated |
| Strict prompt format, loose generated output | Postel (inverted) | The agent is hard to use but unreliable to trust |
| Indefinite "thinking" agent with no budget | Parkinson | The user can't plan; the task expands unbounded |
| Session ends with an ambiguous "done?" | Peak-End | The strong middle is forgotten; the user remembers uncertainty |

## References

- See [references/ux-laws-evidence-base.md](references/ux-laws-evidence-base.md) for the origin citations, key studies, and AI-specific evidence for each of the ten laws, plus the resolution logic for the four AI-specific tensions.