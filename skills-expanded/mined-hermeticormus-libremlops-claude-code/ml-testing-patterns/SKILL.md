---
name: "ml-testing-patterns"
description: "ML testing patterns with code: pytest fixtures for models and data, data quality tests, CheckList-style behavioral tests, and performance regression gates in CI. Use when adding tests to an ML codebase."
---

# ML Testing Patterns

Expert patterns for data quality tests, model unit tests, behavioral tests, and performance regression gates.

## Pattern 1: pytest Fixtures for ML

Shared fixtures that load model and data once per test session.

```python
# conftest.py
import pytest
import pandas as pd
import numpy as np
import joblib
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

@pytest.fixture(scope="session")
def model():
    """Load model once for entire test session."""
    m = joblib.load("models/sentiment_model.pkl")
    return m

@pytest.fixture(scope="session")
def tokenizer():
    return AutoTokenizer.from_pretrained("models/tokenizer/")

@pytest.fixture(scope="session")
def transformer_model(tokenizer):
    m = AutoModelForSequenceClassification.from_pretrained("models/bert-sentiment/")
    m.eval()
    return m

@pytest.fixture(scope="session")
def test_data():
    return pd.read_parquet("data/test_v3.parquet")

@pytest.fixture
def sample_positive():
    return ["This product is absolutely fantastic!", "Exceeded all my expectations", "Would buy again 10/10"]

@pytest.fixture
def sample_negative():
    return ["Worst purchase ever", "Complete waste of money", "Broke after one day"]

@pytest.fixture
def sample_neutral():
    return ["The product arrived on time", "It works as described", "Nothing special"]
```

## Pattern 2: Data Quality Tests

Test dataset schema, distributions, and quality before training.

```python
# tests/test_data_quality.py
import pytest
import pandas as pd
import numpy as np
from pandera import DataFrameSchema, Column, Check

FEATURE_SCHEMA = DataFrameSchema({
    "user_id": Column(str, nullable=False),
    "purchase_count_30d": Column(float, [
        Check.greater_than_or_equal_to(0),
        Check.less_than(10000),
    ], nullable=False),
    "avg_order_value_30d": Column(float, [
        Check.greater_than_or_equal_to(0),
    ], nullable=True),
    "label": Column(int, Check.isin([0, 1]), nullable=False),
})

class TestDataQuality:
    def test_schema_valid(self, test_data):
        """Feature schema matches expected types and ranges."""
        FEATURE_SCHEMA.validate(test_data)

    def test_no_duplicate_user_ids(self, test_data):
        n_dupes = test_data['user_id'].duplicated().sum()
        assert n_dupes == 0, f"Found {n_dupes} duplicate user_ids"

    def test_label_distribution(self, test_data):
        """Labels must not be too imbalanced (< 95:5 ratio)."""
        value_counts = test_data['label'].value_counts(normalize=True)
        min_class_pct = value_counts.min()
        assert min_class_pct >= 0.05, (
            f"Minority class is only {min_class_pct:.1%}. "
            f"Distribution: {value_counts.to_dict()}"
        )

    def test_null_rate_below_threshold(self, test_data):
        """No feature exceeds 10% null rate."""
        required_cols = ['purchase_count_30d', 'user_id', 'label']
        for col in required_cols:
            null_rate = test_data[col].isna().mean()
            assert null_rate == 0, f"Required column '{col}' has {null_rate:.1%} nulls"

        for col in test_data.columns:
            null_rate = test_data[col].isna().mean()
            assert null_rate <= 0.10, (
                f"Column '{col}' has {null_rate:.1%} nulls (threshold: 10%)"
            )

    def test_feature_ranges(self, test_data):
        """Feature values are within expected production ranges."""
        assert (test_data['purchase_count_30d'] >= 0).all()
        assert (test_data['avg_order_value_30d'].dropna() >= 0).all()
        assert (test_data['avg_order_value_30d'].dropna() < 100_000).all(), \
            "avg_order_value_30d has suspicious outliers"

    def test_train_test_split_no_leakage(self):
        """Verify no user_id overlap between train and test splits."""
        train = pd.read_parquet("data/train_v3.parquet")
        test = pd.read_parquet("data/test_v3.parquet")
        overlap = set(train['user_id']) & set(test['user_id'])
        assert len(overlap) == 0, f"Train/test overlap: {len(overlap)} user_ids"
```

## Pattern 3: Model Behavioral Tests (CheckList)

Test minimum functionality, invariance, and directional expectations.

```python
# tests/test_model_behavior.py
import pytest
import numpy as np

POSITIVE, NEGATIVE, NEUTRAL = 1, -1, 0

def classify_text(model, tokenizer, texts: list[str]) -> list[int]:
    """Helper: batch inference → class labels."""
    # Implement for your model/tokenizer
    pass

class TestMinimumFunctionality:
    """Model must handle these clear-cut cases correctly."""

    def test_clearly_positive_texts(self, transformer_model, tokenizer, sample_positive):
        preds = classify_text(transformer_model, tokenizer, sample_positive)
        accuracy = sum(p == POSITIVE for p in preds) / len(preds)
        assert accuracy >= 0.9, (
            f"Only {accuracy:.0%} of clearly positive texts classified as POSITIVE. "
            f"Predictions: {preds}"
        )

    def test_clearly_negative_texts(self, transformer_model, tokenizer, sample_negative):
        preds = classify_text(transformer_model, tokenizer, sample_negative)
        accuracy = sum(p == NEGATIVE for p in preds) / len(preds)
        assert accuracy >= 0.9, f"Only {accuracy:.0%} of clearly negative texts classified as NEGATIVE"

    def test_negation_handled(self, transformer_model, tokenizer):
        """'not bad' should be classified as positive, not negative."""
        texts = ["not bad", "not terrible", "not the worst"]
        preds = classify_text(transformer_model, tokenizer, texts)
        # Allow 2/3 correct — negation is hard
        assert sum(p == POSITIVE for p in preds) >= 2, \
            f"Negation handling poor. Predictions for {texts}: {preds}"


class TestInvariance:
    """Output should NOT change for semantically irrelevant perturbations."""

    def test_name_substitution_invariant(self, transformer_model, tokenizer):
        """Changing the name should not change sentiment."""
        original = "John loved this product and would recommend it"
        substituted = "Sarah loved this product and would recommend it"
        pred_original = classify_text(transformer_model, tokenizer, [original])[0]
        pred_substituted = classify_text(transformer_model, tokenizer, [substituted])[0]
        assert pred_original == pred_substituted, (
            f"Name substitution changed prediction: "
            f"'{original}' → {pred_original}, '{substituted}' → {pred_substituted}. "
            f"Possible gender bias."
        )

    def test_punctuation_invariant(self, transformer_model, tokenizer):
        """Adding/removing trailing punctuation should not change sentiment."""
        base = "This is a great product"
        variants = [base, base + ".", base + "!", base + "?"]
        preds = classify_text(transformer_model, tokenizer, variants)
        assert len(set(preds)) == 1, \
            f"Punctuation changed prediction: {list(zip(variants, preds))}"


class TestDirectionalExpectation:
    """Output should change in the expected DIRECTION with specific perturbations."""

    def test_adding_negation_makes_more_negative(self, transformer_model, tokenizer):
        """Adding 'not' before a positive word should make sentiment more negative."""
        positive = "This is good"
        negated = "This is not good"
        pred_pos = classify_text(transformer_model, tokenizer, [positive])[0]
        pred_neg = classify_text(transformer_model, tokenizer, [negated])[0]
        assert pred_neg <= pred_pos, \
            f"Negation did not shift sentiment negative: '{positive}'={pred_pos}, '{negated}'={pred_neg}"
```

## Pattern 4: Performance Regression Gate in CI

Lock baseline metrics; fail CI if new model regresses.

```python
# tests/test_model_performance.py
import pytest
import json
import os
from sklearn.metrics import f1_score, roc_auc_score

BASELINE_METRICS_FILE = "tests/baselines/model_metrics.json"

@pytest.fixture(scope="session")
def baseline_metrics():
    if not os.path.exists(BASELINE_METRICS_FILE):
        pytest.skip("No baseline metrics file. Run with --update-baseline to create.")
    with open(BASELINE_METRICS_FILE) as f:
        return json.load(f)

class TestPerformanceRegression:
    """New model must not regress from baseline metrics."""

    TOLERANCE = 0.01  # Allow 1% regression from baseline

    def test_f1_no_regression(self, model, test_data, baseline_metrics):
        X_test = test_data.drop("label", axis=1)
        y_test = test_data["label"]
        y_pred = model.predict(X_test)
        current_f1 = f1_score(y_test, y_pred, average="weighted")
        baseline_f1 = baseline_metrics["val_f1_weighted"]
        threshold = baseline_f1 - self.TOLERANCE

        assert current_f1 >= threshold, (
            f"F1 regression: current={current_f1:.4f} < "
            f"baseline={baseline_f1:.4f} (threshold={threshold:.4f})"
        )

    def test_auc_no_regression(self, model, test_data, baseline_metrics):
        X_test = test_data.drop("label", axis=1)
        y_test = test_data["label"]
        proba = model.predict_proba(X_test)[:, 1]
        current_auc = roc_auc_score(y_test, proba)
        baseline_auc = baseline_metrics["val_auc"]
        threshold = baseline_auc - self.TOLERANCE

        assert current_auc >= threshold, (
            f"AUC regression: current={current_auc:.4f} < "
            f"baseline={baseline_auc:.4f} (threshold={threshold:.4f})"
        )

    def test_inference_latency(self, model, test_data):
        """p99 latency must be under 50ms per sample."""
        import time
        X_test = test_data.drop("label", axis=1).head(1000)
        latencies = []
        for i in range(len(X_test)):
            t0 = time.perf_counter()
            model.predict(X_test.iloc[[i]])
            latencies.append((time.perf_counter() - t0) * 1000)

        p99_ms = sorted(latencies)[int(len(latencies) * 0.99)]
        assert p99_ms <= 50, f"p99 latency = {p99_ms:.2f}ms (threshold: 50ms)"

# CLI to update baseline after intentional improvement:
# python -c "
# import json, joblib, pandas as pd
# from sklearn.metrics import f1_score, roc_auc_score
# model = joblib.load('models/model.pkl')
# test = pd.read_parquet('data/test_v3.parquet')
# X, y = test.drop('label', axis=1), test['label']
# metrics = {'val_f1_weighted': f1_score(y, model.predict(X), average='weighted'),
#             'val_auc': roc_auc_score(y, model.predict_proba(X)[:,1])}
# json.dump(metrics, open('tests/baselines/model_metrics.json', 'w'), indent=2)
# print(metrics)
# "
```

## Anti-Patterns

### Anti-Pattern 1: Only Testing the Happy Path
Testing that model.predict() returns something is not a test. Tests must assert specific values, shapes, types, and behavioral properties. A test that never fails provides no safety net.

### Anti-Pattern 2: Loading the Model in Every Test
`model = load_model()` in each test function multiplies cold-start time across hundreds of tests. Use `@pytest.fixture(scope="session")` to load once per test run.

### Anti-Pattern 3: No Behavioral Tests
Unit tests on transforms + accuracy on held-out data are necessary but not sufficient. Behavioral tests catch biases and capability gaps that aggregate metrics hide. Include at least MFT, INV, and DIR tests for every model.

### Anti-Pattern 4: Soft Assertions in CI
`if current_f1 < baseline_f1: print("WARNING")` doesn't fail the build. Use `assert` with clear error messages. The CI gate must be a hard failure to have any enforcement value.

### Anti-Pattern 5: Testing on Training Data
Using the training set for performance regression tests measures memorization, not generalization. Always test on a held-out set that is never used for hyperparameter tuning.
