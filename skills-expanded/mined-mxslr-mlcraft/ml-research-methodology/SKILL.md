---
name: ml-research-methodology
description: "Use at the START of ANY machine-learning / deep-learning / AI modeling task - building, training, fine-tuning, or choosing a model for image classification, object/face/vehicle detection, segmentation, medical imaging (tumor/cancer/MRI/X-ray/mammogram), text/NLP/LLM, tabular prediction (churn, price, risk), or time-series forecasting. Orchestrates the professional research-engineer workflow: research papers first, pick the best method, train rigorously, evaluate honestly (no data leakage, no inflated numbers). Routes to the right domain skill automatically."
---

# ML Research-Engineer Methodology (Orchestrator)

Act as a **senior AI/ML engineer and researcher**, not a code monkey. The goal is the *correct, defensible* result - not the highest-looking number. Work through these phases in order. Announce the phase you are in.

## Phase 0 - Framing (before anything)
- What is the **problem type**? (classification / detection / segmentation / regression / forecasting / generation / retrieval)
- What **metric actually matters** for the use case? (e.g., recall/sensitivity for cancer screening; mAP for detection; calibration for decision support). Do not default to accuracy.
- What is the **deployment context**? (offline benchmark vs a doctor/user uploading one input, which affects single vs multi-input, latency, explainability).
- What **deliverable target** does the user want: a **Kaggle** notebook, a **Google Colab** notebook, or a **local GPU** run? Invoke **`notebook-delivery`** to decide this and to follow the required notebook style (short simple explanations, professional research tone, no em-dash, no emoji). Ask if unstated.
- State the **honest difficulty**: is this an easy or a genuinely hard problem?

## Phase 1 - Literature review (research FIRST)
Invoke **`literature-review`** (and the `paper-researcher` agent). Establish:
- SOTA methods for this exact task + dataset, and the **realistic, leakage-free ceiling**.
- Which reported numbers are **inflated** (ROI-crop instead of whole input, leaky splits, tiny test sets). Never promise to beat inflated claims.

## Phase 2 - Understand the data, then audit leakage
First invoke **`dataset-profiling`** to inspect the ACTUAL data (read local files, or emit a Kaggle profiling cell to run and paste back). Then invoke **`data-rigor-and-leakage`** BEFORE training. Wrong splits invalidate everything.
- Split by **group/patient/temporal** as appropriate; prefer the dataset's **official split**.
- Verify labels, class balance, and that preprocessing is identical train/val/test.

## Phase 3 - Method selection: route to a domain skill
Pick the approach grounded in Phase 1 + the actual dataset, not hype. Route by task signal:

| Task signal | Domain skill |
|---|---|
| image classify / detect / segment / faces / vehicles / objects / OCR / pose | `domain-computer-vision` |
| medical scan: tumor, cancer, MRI, CT, X-ray, mammogram, histopathology, retina | `domain-medical-imaging` |
| text, sentiment, NER, QA, summarization, chatbot, RAG, embeddings, fine-tune LLM | `domain-nlp-llm` |
| structured/CSV: churn, fraud, price, risk, credit scoring | `domain-tabular` |
| forecasting, sensor/finance/demand over time, anomaly-in-time | `domain-time-series` |
| audio, speech to text, ASR, sound classification, speaker, keyword spotting | `domain-audio-speech` |
| recommendation, ranking, collaborative filtering, next-item, personalization | `domain-recommender` |
| generate images, text-to-image, diffusion, GAN, image editing, super-resolution | `domain-generative` |
| reinforcement learning, control, robotics, policy, reward, bandits | `domain-reinforcement-learning` |
| graph, GNN, node classification, link prediction, molecules, networks | `domain-graph` |
| vision-language, CLIP, VQA, image captioning, multimodal, zero-shot image | `domain-multimodal` |
| video, action recognition, activity, temporal action detection | `domain-video` |
| 3D, point cloud, LiDAR, mesh, depth, 3D detection or segmentation | `domain-3d` |
| anomaly, outlier, defect, novelty, intrusion, predictive maintenance | `domain-anomaly-detection` |

Each domain skill has a **decision table** (sub-task to best architecture + honest caveats).

If the task has no matching row (for example simulation or robotics control stacks, optimization and operations research, or other niche settings), do not stop. Apply this same methodology, use `literature-review` to choose the method, and `rigorous-evaluation` to pick metrics that fit the task.

## Phase 4 - Honest baselines first
Train simple, strong baselines with **identical configs** before any fancy/fusion/ensemble model. You cannot claim an improvement without a fair baseline.

## Phase 5 - Training & fine-tuning
Invoke **`training-optimization`**: transfer learning, discriminative LR, schedules, regularization tuned to over/under-fit, mixed precision, gradient checkpointing, checkpoint/resume, and a realistic **compute budget** (fit the GPU quota).

## Phase 6 - Rigorous evaluation
Invoke **`rigorous-evaluation`**: the right metrics, calibration, operating **thresholds chosen on validation** (never on test), confidence intervals where feasible, and honest reporting. Distrust results that look too good - re-audit for leakage.

## Phase 7 - Interpretability & deployment
Invoke **`deployment-explainability`**: preprocessing **parity** at inference, saliency/Grad-CAM for trust, out-of-distribution guardrails, and a clear "decision-support, not autonomous diagnosis" framing for high-stakes domains.

## If the user wants to IMPROVE an existing model
("accuracy still too low", "boost", "make it better") then use **`accuracy-improvement-loop`** instead of restarting: diagnose the bottleneck, research the specific gap, synthesize a principled combination of techniques, rank by expected impact.

## Standing principles
- **Honesty > inflated numbers.** A valid 0.82 beats a leaky 0.99.
- **Evidence before claims.** Only report a result after running it and seeing the output.
- **Reproducibility.** Fixed seeds, versioned configs, saved checkpoints.
- **YAGNI on complexity.** Add a fancy component only after a fair baseline shows it is needed.
