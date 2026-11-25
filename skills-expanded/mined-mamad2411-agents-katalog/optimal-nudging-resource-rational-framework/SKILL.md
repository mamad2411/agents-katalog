---
name: optimal-nudging-resource-rational-framework
description: A computational framework for modeling, predicting, and automatically constructing optimal nudges by treating nudges as modifications to the meta-level problem a resource-rational agent faces. Models decision-making as meta-level Markov decision processes where nudges change the cost of computations or the agent's initial beliefs, enabling quantitative predictions, formal goal specification, and automated nudge design via optimization. Use when designing choice architectures, predicting nudge effects across contexts, constructing personalized or self-nudges, building AI choice-architecture systems, or needing a formal (non-ad-hoc) model of how a nudge will change deliberation and choice. NOT for purely economic-utility models of nudges or for nudge typology classification (use bottom-nudge-analysis-framework for the latter).
---

# Optimal Nudging for Cognitively Bounded Agents: A Resource-Rational Framework

## Overview

This framework models nudges as modifications to the meta-level problem a resource-rational decision-maker faces — that is, the problem of *how* to decide, not *what* to decide. Using meta-level Markov decision processes (meta-level MDPs), it provides a common formal language that accounts for default options, suggested alternatives, and information highlighting within one theory, enables quantitative predictions without fitting parameters, formalizes nudge goals (ease, decision quality, probability of a specific choice), and can automatically construct optimal nudges via optimization algorithms — outperforming heuristic and random nudge design in controlled experiments.

## When to Use

- Designing choice architecture and needing to predict the effect of a specific nudge across new contexts
- Building an AI choice-architecture system that personalizes nudges in real time
- Constructing self-nudges or citizen-choice-architect tools that require transparent, user-specified goals
- Formalizing nudge goals beyond "encourage a specific choice" (e.g., making decisions easier, improving decision quality)
- Designing digital nudging systems with ethical compliance as a structural constraint
- Unifying multiple verbal nudge theories (cognitive-effort, recommendation, loss-aversion) in a single computational model
- NOT for nudge typology or mechanism classification — use bottom-nudge-analysis-framework
- NOT for pure welfare/taxation economic models that abstract away the choice architecture

## Core Process / Workflow

### 1. Model the decision as a meta-level MDP

The framework distinguishes the **object-level problem** (which option to choose) from the **meta-level problem** (how to decide — which information to consider, which to ignore). A nudge changes the meta-level problem, not the object-level problem.

A meta-level MDP is defined by:
- **States** S: the true state of the world (e.g., feature values of each option)
- **Actions** A: the object-level choices (select option a)
- **Object-level reward** r_object(s, a): the utility of choosing a in state s
- **Beliefs** B: distributions over states (the agent's current knowledge)
- **Computations** C: cognitive operations (consider one feature of one option) + a termination operation ⊥
- **Meta-level transition** T_meta: how computations update beliefs
- **Meta-level reward** r_meta: cost of computation + object-level reward at termination

The key insight: thinking is itself a sequential decision problem. At each moment the agent chooses to continue deliberating (executing a computation that updates a belief and incurs a cost) or to terminate (choose the option with highest expected utility given current beliefs and receive the object-level reward).

### 2. Model nudges as meta-level modifications

Three canonical nudge types map to three meta-level modifications:

| Nudge | Meta-level modification | Formal effect |
|---|---|---|
| Default option | Changes initial belief state (agent treats default as a recommendation about what's best for the average person) | μ_default features get higher prior mean μ+, lower variance σ+ |
| Suggested alternative | Adds a new option + reveals its best feature for free | Initial belief updated: μ_suggested,best_feature = true value, σ = 0 |
| Information highlighting | Reduces the cost of considering certain features | λ_highlighted_feature reduced (e.g., 3 → 1) |

Critically, none of these change the object-level problem (the options, their true utilities, or the economic incentives). They change only the meta-level problem — the cost of computations or the initial beliefs — which changes the optimal sequence of cognitive operations a resource-rational agent executes, which in turn changes the belief at the time of choice and the choice itself.

### 3. Predict nudge effects with the meta-greedy policy

Computing the exact optimal policy for a meta-level MDP is intractable for realistic problem sizes. The framework uses a **meta-greedy policy** — a one-step lookahead approximation that selects the computation with maximal expected value assuming termination on the next step. This produces quantitative predictions without fitting parameters to data.

The meta-greedy value of a computation c (considering feature f of option a) is:

```
Q_greedy(b, c) = E[max(V_considered_option, V_best_alternative)] − cost(c)
```

where V_considered_option is Normally distributed with mean = current expected value of the option and standard deviation = w_feature × σ_feature (the feature's importance × the agent's uncertainty about it). The expected maximum of a Normal and a constant is computed with the Normal CDF and truncated-Normal expectation.

Predictions validated in five experiments (N=400, 272, 88, 250, 250):
- Defaults increase selection of the default option (89.8% vs 55.7%); effect larger for complex problems and smaller for idiosyncratic preferences.
- Early suggestions outperform late suggestions (pre-choice vs post-choice).
- Information highlighting increases consideration of the highlighted feature (3.20 vs 1.89 values revealed) and shifts choices toward options high on that feature.
- Optimal nudges (constructed by optimization) outperform random and heuristic (extreme-value) nudges on both decision quality and decision ease.

### 4. Construct optimal nudges automatically

The five-step method:

1. **Model the decision** as a meta-level MDP M.
2. **Specify the nudge space** — a set of possible modified meta-level MDPs M̃ (e.g., reveal 3 feature values, or reduce cost of 3 features).
3. **Specify the objective** g(M̃, s) — what the nudge should accomplish:
   - g_action: probability the agent chooses a specific action a
   - g_utility: expected utility of the agent's choice
   - g_meta: cumulative meta-level reward (decision quality − computational cost) — recommended
4. **Specify the architect's belief** b_arch — what the choice architect knows about the world (may differ from the agent's initial belief; integrates over unknown preferences).
5. **Optimize** — find M̃* = argmax E[g(M̃, s)] via exhaustive enumeration or hill climbing.

This whole procedure runs automatically, without supervision or human data. It can:
- Personalize nudges by inferring preferences from observable decision-making operations (mouse/eye-tracking) and updating b_arch
- Construct self-nudges by letting individuals specify the objective or the nudge space
- Operate without user data by integrating over all possible preferences — privacy-preserving by design

### 5. Design AI choice-architecture systems with structural ethics

For digital nudging systems, ethics and fairness must be architectural guardrails, not implementation details. The framework maps to a software architecture with:

- **Sequential processing layers:** Data Capture → User Modeling (Cognitive Mode, Behavioral Stage, Attention Capacity) → Nudge Intelligence (Strategy Optimizer, Nudge Generator, UI Adaptation)
- **Cross-cutting evaluation modules:** Fairness Monitor (bias detection), Ethics Compliance (GDPR/AI Act/DSA enforcement), Explainability (transparency reports), Outcome Tracker (execution traces)
- **Ethics as interceptor:** No nudge reaches users without validation — the ethics module sits between nudge generation and delivery, enforcing constraints structurally

Eleven quality attributes for digital nudging: acceptability, awareness, effectiveness, fairness, healthfulness, helpfulness, intrusiveness, motivation, transparency, trustworthiness, user impact. Four are non-functional requirements (ethics compliance, fairness, transparency, adaptivity); the rest are evaluation metrics.

### 6. A-Tech applications

- **A-Coder:** Model the developer's meta-level problem (which files to read, which functions to inspect, which tests to run). AI suggestions that reduce the cost of the right computations (highlight the relevant test, surface the right file) are information-highlighting nudges. Defaults (the suggested fix) are default nudges. The framework predicts which nudge type works for which cognitive state.
- **Be Practical:** Each learning module is a choice architecture. Default option = the recommended next lesson. Suggestion = the "you might also try" prompt. Information highlighting = the emphasized practice exercise. The framework predicts that early suggestions outperform late ones, so surface the next-best path before the learner commits.
- **Builder's Club:** The community feed is a choice architecture. Defaults (sort order, visible categories), suggestions ("trending contributions"), and highlighting (pinned posts) are all meta-level modifications. Use the framework to optimize for engagement quality (g_utility), not just engagement quantity (g_action).
- **Privacy-first personalization:** The framework can operate without user data by integrating over all possible preferences. This is A-Tech's privacy-first differentiator: personalized nudges that require no behavioral surveillance.

## References

- See [references/optimal-nudging-evidence-base.md](references/optimal-nudging-evidence-base.md) for the full formal framework, experimental results, mathematical derivations, and cross-references to adjacent skills.
- Complements `bottom-nudge-analysis-framework` (mechanism-analysis typology)
- Complements `digital-nudging-ethical-persuasion` (ethical nudging principles)
- Complements `ai-behavioral-loop-design` (AI behavioral loop design)
- Complements `nudge-disclosure-transparency-effectiveness` (transparency of nudges)