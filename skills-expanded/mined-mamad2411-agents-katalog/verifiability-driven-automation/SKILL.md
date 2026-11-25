---
name: verifiability-driven-automation
description: Apply Andrej Karpathy's verifiability framework to identify where AI automation succeeds, where it fails, and how to build high-value agent systems. Covers the three implications for founders, engineers, and teams deploying agents. Use when evaluating automation opportunities, choosing between agentic and human workflows, or designing reinforcement learning environments for domain-specific AI.
---

# Verifiability-Driven Automation

## Overview

Andrej Karpathy — founding member of OpenAI, former Director of AI at Tesla, and the person who coined "vibe coding" — gave one of the clearest frameworks for thinking about AI automation at Sequoia's AI Ascent 2026:

**AI automates fastest in domains where output can be verified.**

This is not coincidence. It is a direct consequence of how frontier models are trained. Labs run massive reinforcement learning environments where models are rewarded for producing correct, verifiable outputs. Code and math made the training cut because they are economically valuable and easy to verify. Many other domains did not.

The result is what Karpathy calls **"jagged entities"** — models with spectacularly uneven capabilities. They can refactor 100,000-line codebases or find zero-day vulnerabilities, yet tell a user to walk to a car wash 50 meters away because they are clearly driving there to wash their car.

This skill operationalizes the verifiability lens for A-Tech's agent strategy, product design, and community education.

## The Verifiability Spectrum

Not all tasks are equally automatable. The key variable is how easily a human (or another system) can verify that the output is correct.

| High Verifiability | Low Verifiability |
|-------------------|-------------------|
| Code compilation and tests | Creative writing quality |
| Math proofs and calculations | Strategic business decisions |
| Structured data extraction | Emotional intelligence |
| Unit test generation | User experience design |
| Vulnerability scanning | Ethical judgment |
| Refactoring with type safety | Market trend prediction |

**Rule:** Agents excel where verification is cheap and unambiguous. They struggle where verification requires human judgment, domain expertise, or taste.

## Why Verifiability Matters for Training

Frontier models are trained on reinforcement learning from human feedback (RLHF) and AI feedback (RLAIF). The reward signal depends on the ability to check whether an output is correct.

- **Code:** A compiler and test suite provide instant, unambiguous feedback. The model learns fast.
- **Math:** A proof checker or symbolic solver validates steps. The model learns fast.
- **Creative writing:** No automated verifier exists for "good" prose. The model learns slowly and unevenly.
- **Strategic advice:** No verifier exists for "correct" business strategy. The model hallucinates plausible-sounding but wrong guidance.

This explains why models are jagged. It also predicts where the next breakthroughs will come: domains that someone builds a verifier for.

## The Three Practical Implications

### For Founders: Build Verifiers, Not Just Agents

The saturated opportunity is not building another coding agent or math solver. The high-value opportunity is building the verification infrastructure for underserved domains.

**Framework:**
1. Identify a high-value domain with no good automated verifier
2. Build the RL environment and training data that enables verification
3. Fine-tune or train a domain-specific model on that verifier
4. Extract dramatically better performance than frontier models achieve out-of-the-box

**Examples of verifier-building opportunities:**
- Legal contract compliance checker (verifies clauses against regulations)
- Medical diagnosis consistency validator (cross-references symptoms, tests, and literature)
- Financial model audit engine (verifies assumptions, formulas, and sensitivities)
- Supply chain risk simulator (verifies resilience against disruption scenarios)

### For Engineers: Ask "Am I in the Circuits?"

If you are hitting a wall with an LLM — slow, inconsistent, or just wrong — the first diagnostic question is: are you in a domain the model was heavily trained on?

**Diagnostic flow:**
```
Is the task in a verifiable domain?
  → Yes: Is there an automated verifier available?
    → Yes: The model should perform well. If not, check context quality.
    → No: Build the verifier first, then fine-tune.
  → No: Does the task require taste, judgment, or context?
    → Yes: Use the model for drafting, not deciding. Human must verify.
    → No: Experiment with few-shot examples and structured output formats.
```

**Action:** If you are not in the circuits, fine-tuning on domain-specific data is likely the right path — not more prompt engineering, not bigger models, not longer context windows.

### For Teams Deploying Agents: Match Guardrails to Verifiability

Human oversight should scale inversely with verifiability. The less verifiable the domain, the heavier the guardrails.

| Verifiability Level | Automation Level | Human Role |
|---------------------|------------------|------------|
| High (code, math, structured data) | Full automation with automated verification | Monitor for edge cases |
| Medium (summarization, translation, formatting) | Automated with spot-check sampling | Periodic quality audit |
| Low (strategy, design, ethics, relationships) | Assisted drafting only | Full review and decision authority |

**Guardrail design principles:**
- Never let agents make unreviewed decisions in low-verifiability domains
- Build escalation paths that surface uncertain outputs for human review
- Track "jaggedness incidents" — cases where the model is spectacularly right on one task and spectacularly wrong on another

## The Verifiability-Driven Product Roadmap

### Phase 1: Audit (Week 1)
Map every workflow in your product or organization to the verifiability spectrum.

| Workflow | Verifiability | Current Approach | Recommended Approach |
|----------|--------------|-------------------|----------------------|
| Code generation | High | AI generates, human reviews | AI generates + tests, human spot-checks |
| Documentation | Medium | AI drafts, human edits | AI drafts, human verifies accuracy |
| Architecture decisions | Low | AI suggests, human decides | AI provides options + tradeoffs, human decides |
| Security review | High | Human-led with tools | AI scans + verifies, human escalates |
| Customer strategy | Low | AI assists research | Human owns strategy; AI handles data gathering |

### Phase 2: Build Verifiers (Weeks 2–4)
For high-value, high-verifiability workflows lacking automated verification, build the verifier first.

**Verifier types:**
- **Syntactic:** Compilers, linters, schema validators
- **Semantic:** Test suites, property-based testing, fuzzing
- **Cross-reference:** RAG over trusted sources with citation requirements
- **Simulation:** Sandbox execution, Monte Carlo validation
- **Human-in-the-loop:** Structured review rubrics, comparison tasks

### Phase 3: Fine-Tune and Deploy (Weeks 5–8)
Use the verifier to generate training signal, then fine-tune a model specifically for that domain.

## A-Tech Applications

### A-Coder (IDE)
- **Verifiability Dashboard:** Tag every agent capability with its verifiability level
- **Auto-Verifier Pipeline:** Every agent-generated code change runs through compilation, tests, linting, and type-checking before human review
- **Jaggedness Alerts:** When the model produces unexpectedly low-quality output in a normally high-verifiability domain, flag for investigation

### Be Practical (Playbooks)
- **"The Verifiability Audit"** — workbook for mapping any workflow to the verifiability spectrum
- **"Building Domain Verifiers"** — guide to constructing RL environments for custom domains
- **"When to Trust the Agent"** — decision tree for delegation levels by task type

### Builder's Club
- **Verifier marketplace:** Members build and share verifiers for niche domains
- **Jaggedness journal:** Community documentation of model failures by domain, to improve collective understanding
- **Fine-tuning co-op:** Shared compute and data for domain-specific fine-tuning projects

## Ethical Guardrails

### Transparency
- Every agent output should carry a verifiability score: how easily can this be checked?
- Users must know when they are receiving low-verifiability output that requires human review

### Accountability
- In low-verifiability domains, the human who approves the output is accountable, not the agent
- Agent-generated strategic advice should never be presented as "the" answer — always as "an" option

### Anti-Deception
- Do not use high-verifiability performance to imply competence in low-verifiability domains
- Marketing that highlights coding prowess must not suggest equivalent capability in strategy, ethics, or design

## Measurement Framework

| Metric | Target | Measurement |
|--------|--------|-------------|
| Automated verification coverage | ≥ 80% of agent outputs | Verifier pipeline tracking |
| Jaggedness incident rate | < 1 per 1000 tasks | Failure logging by domain |
| Human escalation rate | Matches verifiability level | Escalation tracking |
| Fine-tuning ROI | ≥ 2× improvement over base model | A/B testing on domain tasks |
| Verifier false positive rate | < 5% | Manual audit of verifier output |

## Cross-References
- See `ai-agents-and-workflows/agentic-coding-trends-2026` for the broader organizational shift from writing code to orchestrating agents
- See `cognitive-science-and-ux/context-engineering` for curating context to improve model performance in any domain
- See `developer-experience-and-flow/agentic-coding-workflow` for the foundational workflow skill
- See `cognitive-science-and-ux/cognitive-surrender-defense` for preventing over-reliance on AI in low-verifiability domains

## Sources
- Sequoia AI Ascent 2026 — Andrej Karpathy keynote: Verifiability as the hidden organizing principle of AI automation
- Firecrawl — "Top 13 Agentic AI Trends to Watch in 2026" (Jun 2026): Verifiability trend synthesis
- The New Stack — "5 Key Trends Shaping Agentic Development in 2026" (Dec 2025): Agentic CLI and verification workflows
- Karpathy, A. — "Vibe Coding" concept origin and subsequent refinement at Sequoia 2026
