---
name: "labeling-patterns"
description: "Annotation patterns with code: labeling guideline design, active learning sampling loops, Snorkel labeling functions, inter-annotator agreement monitoring, gold-label injection for annotator QA, and Cleanlab label error detection. Use when building or auditing a labeling pipeline."
---

# Labeling Patterns

Expert patterns for annotation pipeline design, quality assurance, and scalable labeling systems.

## Pattern 1: Annotation Guideline Design

Good guidelines are the highest-leverage investment in label quality. Bad guidelines produce high IAA on wrong labels.

### Structure
1. **Task definition**: What exactly is being labeled, and why
2. **Label taxonomy**: Exhaustive list with definitions and examples
3. **Decision tree for edge cases**: Binary yes/no questions leading to a label
4. **Boundary cases**: Examples explicitly in and explicitly out for each class
5. **Adjudication protocol**: Who resolves disagreements, how ties are broken

### Example: Sentiment Classification Guideline Snippet
```
Label: POSITIVE
Definition: Text expresses overall favorable opinion, satisfaction, or approval.
Include:
  - "The product exceeded my expectations" → POSITIVE
  - "Not bad at all, would recommend" → POSITIVE (negation of negative = positive)
Exclude:
  - "The product is fine" → NEUTRAL (neutral qualifier overrides)
  - "Great, but shipping took 3 weeks" → MIXED (not POSITIVE — mixed qualifies it)
Edge case: "I guess it works" → NEUTRAL (hedging without positive content)
```

## Pattern 2: Active Learning Sampling Loop

Implement uncertainty + diversity in two phases to maximize label efficiency.

```python
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import normalize

def uncertainty_sample(model, unlabeled_X: np.ndarray, n: int) -> np.ndarray:
    """Least confidence sampling."""
    probs = model.predict_proba(unlabeled_X)
    max_probs = probs.max(axis=1)
    # Most uncertain = lowest max probability
    indices = np.argsort(max_probs)[:n]
    return indices

def core_set_sample(embeddings: np.ndarray, labeled_indices: list, n: int) -> list:
    """Greedy k-center core-set selection in embedding space."""
    embeddings = normalize(embeddings)
    labeled = embeddings[labeled_indices]
    unlabeled_idx = [i for i in range(len(embeddings)) if i not in labeled_indices]
    unlabeled = embeddings[unlabeled_idx]

    selected = []
    for _ in range(n):
        # Distance from each unlabeled point to nearest labeled point
        dists = np.min(
            np.linalg.norm(unlabeled[:, None] - labeled[None, :], axis=2),
            axis=1
        )
        # Select the point maximally distant from labeled set
        pick = np.argmax(dists)
        selected.append(unlabeled_idx[pick])
        labeled = np.vstack([labeled, unlabeled[pick]])
        unlabeled = np.delete(unlabeled, pick, axis=0)
        unlabeled_idx.pop(pick)
    return selected

# Usage: Phase 1 uncertainty, Phase 2 diversity
phase1 = uncertainty_sample(model, X_pool, n=500)
phase2 = core_set_sample(embeddings, labeled_indices + list(phase1), n=500)
```

## Pattern 3: Snorkel Labeling Function Pipeline

Use weak supervision when annotation budget is constrained but heuristics exist.

```python
from snorkel.labeling import labeling_function, PandasLFApplier, LabelModel
from snorkel.labeling.analysis import LFAnalysis
import re

POSITIVE, NEGATIVE, ABSTAIN = 1, 0, -1

@labeling_function()
def lf_positive_keywords(x):
    keywords = ["excellent", "love", "best", "amazing", "highly recommend"]
    return POSITIVE if any(k in x.text.lower() for k in keywords) else ABSTAIN

@labeling_function()
def lf_negative_keywords(x):
    keywords = ["terrible", "worst", "broken", "waste", "never again"]
    return NEGATIVE if any(k in x.text.lower() for k in keywords) else ABSTAIN

@labeling_function()
def lf_rating_high(x):
    # If structured data has a rating field
    return POSITIVE if hasattr(x, 'rating') and x.rating >= 4 else ABSTAIN

@labeling_function()
def lf_rating_low(x):
    return NEGATIVE if hasattr(x, 'rating') and x.rating <= 2 else ABSTAIN

@labeling_function()
def lf_negation_pattern(x):
    # "not bad", "not terrible" → positive signal
    pattern = r'\bnot\s+(bad|terrible|awful|poor)\b'
    return POSITIVE if re.search(pattern, x.text.lower()) else ABSTAIN

# Apply LFs to unlabeled data
lfs = [lf_positive_keywords, lf_negative_keywords, lf_rating_high, lf_rating_low, lf_negation_pattern]
applier = PandasLFApplier(lfs=lfs)
L_train = applier.apply(df_train)

# Analyze LF quality
print(LFAnalysis(L=L_train, lfs=lfs).lf_summary())
# Check: coverage > 0.3, conflicts manageable, empirical accuracy > 0.7

# Train label model to get probabilistic labels
label_model = LabelModel(cardinality=2, verbose=True)
label_model.fit(L_train=L_train, n_epochs=500, log_freq=100, seed=42)
probs_train = label_model.predict_proba(L=L_train)
```

## Pattern 4: IAA Measurement and Monitoring

Track inter-annotator agreement per class, per annotator, per batch.

```python
import pandas as pd
from sklearn.metrics import cohen_kappa_score
from itertools import combinations

def iaa_report(annotation_df: pd.DataFrame, annotator_col: str,
               item_col: str, label_col: str) -> pd.DataFrame:
    """
    annotation_df: rows = (annotator, item, label)
    Returns pairwise kappa for all annotator pairs.
    """
    pivot = annotation_df.pivot(index=item_col, columns=annotator_col, values=label_col)
    annotators = pivot.columns.tolist()
    records = []

    for a1, a2 in combinations(annotators, 2):
        shared = pivot[[a1, a2]].dropna()
        if len(shared) < 20:
            continue
        kappa = cohen_kappa_score(shared[a1], shared[a2])
        records.append({
            "annotator_1": a1,
            "annotator_2": a2,
            "n_shared": len(shared),
            "kappa": round(kappa, 3),
            "quality": "good" if kappa > 0.8 else "marginal" if kappa > 0.6 else "poor"
        })
    return pd.DataFrame(records).sort_values("kappa")

# Thresholds
# κ > 0.80: production-ready
# κ 0.60–0.80: review guidelines, investigate disagreements
# κ < 0.60: guideline revision required, do not train on this batch
```

## Pattern 5: Gold Label Injection for Annotator QA

Seed known-answer examples into annotation queues to continuously track annotator accuracy without revealing which items are gold.

```python
import random

def inject_gold_labels(task_queue: list, gold_pool: list,
                       injection_rate: float = 0.1) -> list:
    """
    Inject gold standard items at specified rate.
    Gold items are identical to regular tasks; audited post-submission.
    """
    n_gold = int(len(task_queue) * injection_rate)
    gold_sample = random.sample(gold_pool, min(n_gold, len(gold_pool)))

    # Mark gold items internally (not visible to annotator)
    for g in gold_sample:
        g['_is_gold'] = True
        g['_gold_label'] = g['label']
        del g['label']  # Remove the answer

    combined = task_queue + gold_sample
    random.shuffle(combined)
    return combined

def compute_annotator_accuracy(submissions: list) -> dict:
    """Evaluate annotator on gold items."""
    gold_submissions = [s for s in submissions if s.get('_is_gold')]
    if not gold_submissions:
        return {}

    correct = sum(1 for s in gold_submissions if s['label'] == s['_gold_label'])
    return {
        "total_gold": len(gold_submissions),
        "correct": correct,
        "accuracy": correct / len(gold_submissions)
    }
```

## Pattern 6: Cleanlab Label Error Detection

Use confident learning to find mislabeled examples before training.

```python
from cleanlab.filter import find_label_issues
from cleanlab.rank import get_label_quality_scores
import numpy as np

# Requires out-of-sample predicted probabilities (cross-val)
# pred_probs shape: (n_samples, n_classes)
# labels shape: (n_samples,) — integer class indices

def find_label_errors(labels: np.ndarray, pred_probs: np.ndarray,
                      return_indices: bool = True):
    """
    Find likely mislabeled examples using confident learning.
    Uses cross-validation predicted probabilities.
    """
    label_issues = find_label_issues(
        labels=labels,
        pred_probs=pred_probs,
        return_indices_ranked_by="self_confidence",
        filter_by="prune_by_noise_rate"
    )

    scores = get_label_quality_scores(labels=labels, pred_probs=pred_probs)

    print(f"Estimated label error rate: {len(label_issues)/len(labels):.1%}")
    print(f"Flagged examples: {len(label_issues)}")
    return label_issues, scores

# Workflow:
# 1. Train model with cross-validation, save out-of-fold pred_probs
# 2. Run find_label_errors
# 3. Manually review top-N flagged examples
# 4. Correct or remove; retrain
```

## Anti-Patterns

### Anti-Pattern 1: High IAA ≠ High Quality
Annotators can agree on the wrong label. If your guidelines are wrong, IAA measures consistency of error, not correctness. Always validate against ground truth on a held-out gold set.

### Anti-Pattern 2: Uniform Random Sampling for Active Learning
Random sampling is the baseline. Any active learning strategy that doesn't beat random sampling on the same budget is broken. Measure and compare.

### Anti-Pattern 3: Training on Raw LF Majority Vote
Majority vote ignores LF reliability differences. Always use Snorkel's LabelModel or a weighted scheme. Majority vote can be worse than a single high-quality LF.

### Anti-Pattern 4: Static Annotation Guidelines
Guidelines should evolve as edge cases accumulate. Version your guidelines. Track which guideline version produced each batch of labels.

### Anti-Pattern 5: Ignoring Annotator Fatigue
Annotation accuracy drops after ~1 hour of continuous work. Design batches accordingly. Gold label injection rate should increase near end-of-session to detect degradation.

### Anti-Pattern 6: Imbalanced Gold Set
Gold examples must match production label distribution. A gold set that's 90% negative trains annotators to be biased toward negative labels.
