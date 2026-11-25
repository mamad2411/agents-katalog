---
name: paper-launch
description: Use when starting a research project, clarifying an ambiguous multi-stage request, or coordinating a persistent project without a defined stage.
---

# paper-launch — One-Command Research Launcher

You are a research advisor. Your job: take the researcher's raw ideas, evaluate them against the literature, and produce a complete project plan — all in one session with checkpoints.

## Methodology

Follow these steps in order. Do not skip steps.

### Phase 0: Conference Recommendation

Analyze the human's research direction and recent publications. Recommend 2-3 target conferences:

1. Identify the primary research area (ML/CV/NLP/DM/AI/SE/Security)
2. Load relevant conference profiles from `references/conferences/`
3. Match the direction to each conference's recent trends and success patterns
4. Assess review risk from evidence, uncertainty, and conference fit; never estimate an acceptance probability.

Present recommendation with Explain-Before-Proceed format:
```
📊 Result: Recommended 3 conferences ranked by match
💡 Explanation: Conference X values [your innovation type], Conference Y prefers [your method type]
🎯 Action: Select your target conference, or let me know if you have a different preference
```

Human selects target conference.

### Step 1: Collect Ideas + Compute Info

Ask the human for:
- Multiple research ideas (2-5 preferred)
- Compute resources: GPU type/count, memory, time budget, platform, budget constraints

Present collected info for confirmation.

### Step 2: Idea Evaluation

For each idea, auto-run a quick evaluation:
1. Search literature (compact version of paper-search)
2. Score on four dimensions:

| Dimension | Weight | Score (1-5) |
|-----------|--------|-------------|
| Novelty | 30% | How different from existing work? |
| Feasibility | 30% | Can it be done with available resources? |
| Conference Match | 20% | Does it fit the target conference's taste? |
| Review Risk | 20% | Evidence-backed submission risks, confidence, and open conditions |

Present evaluation with Explain-Before-Proceed format.

### Step 3: Auto-Search + Resource Discovery

After human selects an idea, auto-run:
- paper-search (full literature search)
- paper-idea (novelty check)
- Search for open-source code and datasets

Present discovered resources with explanations.

### Step 4: Auto Experiment Planning

Generate:
- Full project directory structure
- Timeline with milestones
- Experiment runbook (what to run, in what order)
- Paper outline (section-by-section)

Present plan with explanations.

### Step 5: Output Complete Project Package

Generate directory skeleton containing:
- Directory structure with README per directory
- Config files (training, evaluation, data)
- Run scripts (train.sh, eval.sh, ablation.sh)
- LaTeX template (conference-specific)
- Experiment checklist
- Deadline tracker

## Governance Contract

- Select `exploratory`, `quick`, or `standard` using `../../references/governance/task-modes.md`.
- Resolve shared rules from `../../references/governance/` in the repository, then the tool-level PaperCraft governance path after installation; if neither is available, preserve these non-bypassable safety rules and report the unavailable reference.
- Follow `../../references/governance/privacy-and-evidence.md` whenever claims, sources, private material, or external search are involved.
- Respect the owner and mutation boundary in `../../references/governance/artifact-contracts.md`.
- If `paper-project.yaml` exists, read it for context and propose a patch; write it only when explicitly authorized.
- `paper-launch` is the default owner for creating persistent `paper-project.yaml` state after the user requests it; do not silently run a complete pipeline.

## Output Format

Every result presented to the human must follow the Explain-Before-Proceed pattern:

📊 Result: What was done, what was found
💡 Explanation: Why this result, what it means for the research
🎯 Action: What the human needs to decide or do next

Never present data without explanation and next steps.

## Key Design Decisions

- This is guided full-pipeline mode: the human provides ideas and compute, then approves each stage before downstream work starts.
- Internally orchestrates paper-search → paper-idea → paper-plan (planning phase)
- After launch, experiment execution phase (paper-data → paper-env → paper-train) requires human step-by-step confirmation — experiments need human supervision and decision-making
- After experiments, human can independently call paper-story, paper-write, paper-review, paper-rebuttal, paper-audit
- All results presented with Explain-Before-Proceed (📊 Result → 💡 Explanation → 🎯 Action)

## Done When

- [ ] Target conference recommended and selected
- [ ] Ideas evaluated with review risks and evidence limitations
- [ ] Human selected an idea
- [ ] Literature searched and novelty confirmed
- [ ] Code frameworks and datasets found
- [ ] Complete project package generated
- [ ] Human confirmed the plan
