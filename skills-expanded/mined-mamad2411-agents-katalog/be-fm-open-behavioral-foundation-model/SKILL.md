---
name: be-fm-open-behavioral-foundation-model
description: Applies the Be.FM open foundation model for human behavior prediction and simulation. Use when designing behavioral interventions, predicting consumer decisions, simulating economic game behavior, or inferring personality traits from demographics.
---

# Be.FM — Open Behavioral Foundation Model

## Overview

Be.FM (Xie, Li, Wang et al., arXiv:2505.23058, May 2025) is one of the first **open foundation models purpose-built for human behavior modeling**. Rather than relying on general-purpose LLMs that happen to reason about behavior as a side effect, Be.FM is fine-tuned on a curated corpus of behavioral-science literature, incentivized economic-game experiments, and large-scale personality surveys. The result is a model that predicts, simulates, and reasons about human behavior more accurately than far larger proprietary systems — including GPT-4o — on the behavioral tasks it was trained for.

Built on Meta's open-weight **Llama 3.1** family (8B and 70B), fine-tuned via **LoRA** on all layers, Be.FM is available on request and aligns with the open-source ethos: researchers and practitioners can run, inspect, and extend it without depending on a closed API.

## When to Use

- **Designing behavioral nudges or interventions** and you need to predict how a population will distribute across response options before running a costly field experiment
- **Predicting consumer choice distributions** across product, pricing, or messaging variants (not just a single "most likely" answer, but the full behavioral distribution)
- **Simulating economic game outcomes** (Dictator, Ultimatum, Trust, Public Goods, Bomb-risk elicitation) to design experiments or calibrate expectations
- **Inferring personality traits from demographics** (Big Five from age, gender, income, education) for lightweight personalization without invasive psychometric data collection
- **Generating behavioral experiment designs** — Be.FM can suggest novel treatment conditions grounded in the behavioral-science literature it was trained on
- **Reasoning about behavioral knowledge** in context — e.g., "Given loss aversion, what happens if we frame this as a loss?"

NOT for...
- Tasks requiring deterministic factual recall (Be.FM is a behavioral simulator, not a knowledge base)
- Real-time control systems or safety-critical decisions (it is a research tool, not a deployed agent)
- Replacing human-subjects validation — Be.FM *informs* experiment design; it does not substitute for empirical confirmation

## The Be.FM Framework

Be.FM formalizes behavior prediction as:

```
y = F(K, x, c)
```

| Symbol | Meaning |
|---|---|
| **x** | Subject characteristics (demographics, traits, history) |
| **c** | Context (game rules, framing, incentives, environment) |
| **K** | Behavioral knowledge (literature, empirical regularities, theory) |
| **F** | Latent behavioral function learned during fine-tuning |
| **y** | Behavioral choice / distribution of choices |

The model is trained so that `F` internalizes `K` — the behavioral-science knowledge base — and can then generalize to new `(x, c)` pairs, producing `y` distributions that match real human populations.

## Four Demonstrated Capabilities

### 1. Predict & Simulate Behavior Across Scenarios

Be.FM generates full **distributions** of behavioral choices (not just point estimates) and matches them to empirical human data using the **Wasserstein distance** (earth-mover's distance between predicted and observed distributions). Across all five economic games tested, Be.FM variants improved Wasserstein distance over their base Llama 3.1 counterparts — meaning the fine-tuning genuinely shifted the model toward human-like behavioral distributions.

### 2. Infer Subject Characteristics

Given a subject's demographic profile, Be.FM predicts Big Five personality traits (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism). This enables lightweight personalization without administering a 50-item questionnaire.

- **MAE 7.27** (mean absolute error on the 1–100 trait scale)
- **Spearman 0.101–0.128** (rank correlation with true trait scores)

These numbers are modest in absolute terms — personality prediction from demographics is inherently hard — but they demonstrate the model can extract signal from coarse inputs, and the open architecture lets practitioners improve on this with domain-specific data.

### 3. Generate Contextual Insights

Be.FM can **suggest novel experimental treatments** grounded in the behavioral literature. In the Dictator Game, it proposed treatment variations that aligned with published findings — effectively acting as a research brainstorming partner that has "read" 2,703 American Economic Review publications.

### 4. Apply Behavioral Knowledge

On the **Individualized Educational Outcomes (IEO) contest** benchmark (predicting which intervention improves a specific student's outcomes), Be.FM improved accuracy over base Llama:

| Model | Base Accuracy | Be.FM Accuracy | Gain |
|---|---|---|---|
| Llama 3.1 8B | 48.4% | 51.3% | +2.9 pp |
| Llama 3.1 70B | 68.8% | 73.3% | +4.5 pp |

### The GPT-4o Finding

A headline result: **GPT-4o fails to outperform the smaller Be.FM models on behavioral tasks** despite having hundreds of times more parameters. This suggests that *task-specific behavioral fine-tuning* matters more than raw scale for behavioral prediction — a strong argument for open, specialized models over generic frontier APIs.

## Practical Triggers — When to Reach for Be.FM

| Trigger | What Be.FM Adds |
|---|---|
| "What distribution of choices should I expect in this game/experiment?" | Simulates the full behavioral distribution, not just a mode |
| "Can I guess a user's personality from signup demographics?" | Big Five inference from age/gender/income/education |
| "What treatment conditions should I test?" | Generates literature-grounded treatment suggestions |
| "Will loss framing / default setting / social-proof work here?" | Applies behavioral knowledge in context |
| "How do I prototype a behavioral experiment without 10k subjects?" | Simulate outcomes first, then validate with a smaller real sample |

## Core Process / Workflow

### Step 1: Frame the Behavioral Question

Express the question in `(x, c)` terms. What are the subject characteristics and what is the decision context?

```
Example:
  x = {age: 35, gender: F, income: $60k, education: BA}
  c = {game: Dictator, endowment: $10, recipient: anonymous stranger}
  → y = distribution of amounts sent ($0 … $10)
```

### Step 2: Select the Model Variant

| Variant | When to Use |
|---|---|
| Be.FM 8B | Fast iteration, local inference, limited GPU (single consumer GPU) |
| Be.FM 70B | Higher-fidelity simulation, research-grade accuracy, multi-GPU or cloud |

Both share the same fine-tuning recipe; the 70B variant shows larger gains from behavioral fine-tuning (see IEO table above).

### Step 3: Prompt for a Distribution, Not a Single Answer

Be.FM is most useful when prompted to produce a **distribution of choices** (e.g., "For 1,000 subjects with these characteristics in this game, what fraction sends $0, $1, … $10?"). Compare to empirical data via Wasserstein distance.

### Step 4: Infer Characteristics (Optional)

If you need personality proxies without a survey, prompt Be.FM with demographics and request Big Five trait estimates. Treat outputs as **ranked signals**, not precise scores (MAE 7.27 means ±7 points on a 100-point scale).

### Step 5: Generate Treatment Suggestions

Ask Be.FM to propose experimental treatment conditions for the scenario. Cross-check suggestions against the behavioral literature — the model's suggestions are grounded in its training corpus but should be validated.

### Step 6: Validate with a Real Sample

Be.FM is a **prototyping and hypothesis-generation tool**, not a replacement for empirical work. Use its simulations to:
- Pre-register expected distributions
- Narrow the treatment space before fielding
- Generate hypotheses for novel experiments

Then confirm with a real (smaller, better-targeted) subject sample.

## Data & Training Architecture

### Four Data Categories

| Category | Source | Scale |
|---|---|---|
| **Literature** | American Economic Review publications | 2,703 papers, 3.1M tokens |
| **Experimental** | MobLab economic-game platform | 68,780 subjects, 82,057 observations across 5 games |
| **Survey** | Big Five personality inventory | 17,667 subjects |
| **Observational** | (Planned future category) | Not yet incorporated |

### Economic Games Used

The five games in the experimental corpus:

1. **Dictator Game** — allocator decides how to split an endowment with a passive recipient; measures prosocial preference / altruism
2. **Ultimatum Game** — proposer offers a split; responder can accept or reject (rejection = both get nothing); measures fairness norms and strategic behavior
3. **Trust Game** — sender sends some endowment (tripled to receiver); receiver returns some; measures trust and trustworthiness
4. **Public Goods Game** — each player contributes to a common pool (multiplied and split); measures cooperation and free-riding
5. **Bomb Risk Elicitation Task** — collect boxes for money, one contains a bomb that destroys earnings; measures risk preferences

### Training Configuration

| Parameter | Value |
|---|---|
| Base models | Llama 3.1 8B, Llama 3.1 70B |
| Fine-tuning method | LoRA (all layers) |
| Training framework | LlamaFactory |
| Prompt template | Alpaca |
| Epochs | 3 |
| Precision | bf16 |
| Learning rate | 1e-4 |
| LR scheduler | Cosine |

## Deployment Guardrails

- **Distribution, not point estimate:** Always prompt for and evaluate against distributions (Wasserstein), not single answers. Behavioral heterogeneity is the signal.
- **Validate before deploying:** Be.FM simulations inform design; they do not replace human-subjects validation. Always confirm predictions with a real sample before acting on them.
- **Modest personality accuracy:** Big Five inference (MAE 7.27, Spearman 0.10–0.13) is a weak signal. Use it for ranking/segmentation, not individual-level diagnosis.
- **Open-weight responsibility:** The model is available on request. Respect the intended-use terms; behavioral simulation can be misused for manipulation — apply the same ethical scrutiny as any behavioral science tool.
- **Literature-bounded insights:** Treatment suggestions are grounded in AER-era behavioral economics. They may miss recent findings or non-economics behavioral literature. Cross-check with current sources.
- **No observational data yet:** The observational data category is planned but not yet incorporated, so real-world longitudinal behavioral prediction is out of current scope.

## A-Tech Alignment

| A-Tech Value | Alignment |
|---|---|
| **Open-source AI** | Built on Meta Llama 3.1 (open weights); models available on request; fine-tuning recipe fully documented (LoRA, LlamaFactory, Alpaca, 3 epochs, bf16, lr 1e-4 cosine) |
| **Data privacy** | Enables behavioral prediction *without* centralized data collection — infer traits from demographics, simulate populations without surveilling individuals |
| **Financial freedom** | Democratizes behavioral-science tooling; a solo researcher or small team can prototype experiments that previously required a university lab and thousands of subjects |
| **Practical implementation** | Benchmarks provided (Wasserstein, MAE, Spearman, IEO accuracy); concrete training config; runs on consumer GPU (8B) or multi-GPU (70B) |

## Cross-References

- `scaled-behavioral-measurement-targeting` — complements Be.FM by grounding simulations in incentivized measurement
- `llm-iterative-personalized-nudging` — LLM-based personalization that Be.FM could power as the behavioral-simulation engine
- `nudge-effectiveness-reality-check` — evidence on nudge heterogeneity that Be.FM's simulations should respect
- `cross-cultural-llm-personalized-nudge-design` — cultural adaptation layer for Be.FM simulations
- `digital-nudging-ethical-persuasion` — ethical framing for deploying behavioral predictions
- `behavioral-design-practical-playbooks` — intervention patterns Be.FM can help select and parameterize

## References

- See [references/evidence-base.md](references/evidence-base.md) for full experimental results tables (Wasserstein distances for all 5 games across 7 models, Big Five prediction metrics, demographics inference, IEO accuracy, research-workflow BLEURT/ROUGE scores), complete training configuration, and the full economic-game descriptions.