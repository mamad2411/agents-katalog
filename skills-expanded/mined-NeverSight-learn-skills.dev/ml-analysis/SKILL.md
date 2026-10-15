---
name: ml-analysis
description: "End-to-end machine learning and deep learning analysis skill. Automatically detects data types, selects appropriate models, executes analysis, and delivers results. Use this skill whenever the user wants to: (1) Analyze data with ML/DL methods — classification, regression, clustering, anomaly detection, NLP, computer vision, time series, (2) Build or train models on their data, (3) Perform exploratory data analysis (EDA) with statistical rigor, (4) Use AutoML to find the best model, (5) Set up ML pipelines or MLOps workflows, (6) Evaluate, explain, or audit model performance, (7) Process or engineer features from raw data. Trigger on keywords like: predict, classify, cluster, train, model, regression, neural network, deep learning, feature engineering, hyperparameter, cross-validation, SHAP, EDA, anomaly detection, time series forecast, image classification, text classification, NLP, AutoML, deploy model, ML pipeline."
---

# ML Analysis Skill

An end-to-end machine learning and deep learning analysis engine. This skill guides you through a five-stage pipeline — from raw data to deployed model — adapting its depth and complexity to the user's expertise and task scale.

## Core Principles

1. **Always start with data understanding** — never jump to modeling before EDA
2. **Baseline first** — run the simplest viable model before anything complex
3. **Prevent data leakage** — all preprocessing must be fit on training data only
4. **Right-size execution** — run small tasks directly, generate code for large ones
5. **Explain decisions** — tell the user why you chose a specific approach
6. **Adapt to user level** — detect expertise from their language and adjust detail accordingly

## User Level Detection

Pay attention to how the user describes their task:
- **Beginner signals**: "I have some data", "can you predict", vague about metrics, no mention of validation
- **Intermediate signals**: mentions train/test split, specific algorithms, knows their metric
- **Expert signals**: discusses regularization, architecture choices, distribution assumptions, asks about specific hyperparameters

Adjust your responses:
- Beginners: explain each step, use analogies, show visualizations, recommend safe defaults
- Intermediate: explain key decisions, offer options, show trade-offs
- Expert: be concise, offer advanced options, skip basics, discuss nuances

## Execution Mode Decision

Before any computation, assess scale:

| Factor | Direct Execution | Generate Code |
|--------|-----------------|---------------|
| Data size | <100MB, <100K rows | >100MB or >100K rows |
| Model complexity | sklearn, small NNs | Large transformers, distributed training |
| Training time | <5 minutes estimated | >5 minutes estimated |
| GPU required | No | Yes |
| User environment | Local Python available | Needs cloud/cluster |

For borderline cases, prefer direct execution with sampling strategies.

## The Five-Stage Pipeline

### Stage 1: Perceive — Understand the Data and Task

Before anything else, understand what you're working with.

**Step 1.1: Data Profiling**

Run `scripts/data_profiler.py` on the user's data to get:
- Data type detection (tabular / text / image / audio / mixed)
- Shape, memory footprint, column types
- Missing value rates per column
- Cardinality of categorical features
- Target variable distribution (if supervised task)
- Basic statistics (mean, median, std, skew, kurtosis)

```bash
python <skill-path>/scripts/data_profiler.py <data-path> [--target <column>]
```

**Step 1.2: Task Inference**

From the user's description and data profile, determine:
- **Task type**: classification, regression, clustering, anomaly detection, time series, NLP, CV, recommendation
- **Target variable** (if supervised)
- **Evaluation metric** (infer from task type if user doesn't specify)
- **Constraints**: latency, interpretability, fairness requirements

**Step 1.3: Route to Reference**

Based on data type, read the appropriate reference:
- Tabular data → `references/structured-data.md`
- Text / Image / Audio → `references/unstructured-data.md`
- Mixed → read both, design a multi-modal pipeline

### Stage 2: Prepare — Data Engineering and Feature Engineering

**Step 2.1: Data Cleaning**
- Handle missing values (strategy depends on mechanism: MCAR/MAR/MNAR)
- Remove or flag duplicates
- Fix data type issues (strings that should be numbers, etc.)
- Handle outliers (detect with IQR/Z-score, decide to clip/remove/keep based on domain)

**Step 2.2: Train/Test Split — DO THIS BEFORE ANY FITTING**

This is critical to prevent data leakage:
```python
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
# All subsequent preprocessing is fit ONLY on X_train
```

For time series: use temporal split, never random split.

**Step 2.3: Feature Engineering**

Read `references/structured-data.md` or `references/unstructured-data.md` for domain-specific guidance.

General principles:
- Encode categoricals: ordinal encoding for tree models, one-hot for linear models
- Scale numerics: StandardScaler for linear models, not needed for tree models
- Create interaction features only when domain knowledge suggests them
- For text: TF-IDF for baselines, embeddings for deep learning
- For images: use pretrained model features (transfer learning)

**Step 2.4: Pipeline Construction**

Always wrap preprocessing in sklearn Pipelines to prevent leakage:
```python
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer

pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('model', model)
])
```

### Stage 3: Model — Selection, Training, and Tuning

**Step 3.1: Baseline Model**

Always start with a simple baseline. This is non-negotiable:
- Classification → LogisticRegression or DummyClassifier
- Regression → Ridge or mean predictor
- Clustering → K-Means
- NLP → TF-IDF + LogisticRegression
- CV → Pretrained ResNet + linear head

The baseline establishes a performance floor and often reveals data issues.

**Step 3.2: Model Selection**

Consult `references/model-catalog.md` for the decision tree. Key heuristics:
- Tabular data → gradient boosting (LightGBM/XGBoost) almost always wins
- Small tabular (<1K rows) → regularized linear models or small ensembles
- Text classification → fine-tuned transformer if data >5K samples, else TF-IDF + classical ML
- Image → transfer learning from pretrained CNN/ViT
- Time series → start with statistical (ARIMA/Prophet), add ML if needed

**Step 3.3: AutoML Option**

When the user wants automatic model selection, or says "find the best model":
- Read `references/automl-guide.md`
- Recommend AutoGluon (most general), H2O (enterprise), or Optuna (flexible tuning)
- Set appropriate time budget based on data size

**Step 3.4: Hyperparameter Tuning**

- Use Optuna or sklearn's RandomizedSearchCV (not GridSearchCV — too slow)
- For deep learning: learning rate is the most important hyperparameter
  - Use learning rate finder (fast.ai style) when training neural networks
  - Apply one-cycle learning rate policy
- Always tune with cross-validation, not a single validation split

**Step 3.5: Deep Learning Specifics**

When using PyTorch/TensorFlow:
- Start with a pretrained model when possible (transfer learning)
- Use early stopping to prevent overfitting
- Monitor both training and validation loss
- For small datasets: heavy augmentation + dropout + weight decay
- Architecture choice: consult `references/model-catalog.md`

### Stage 4: Evaluate — Rigorous Assessment

Read `references/evaluation-guide.md` for full details. Summary:

**Step 4.1: Metrics**
- Classification: accuracy (only if balanced), F1, precision, recall, AUC-ROC, AUC-PR
- Regression: RMSE, MAE, R², MAPE
- Clustering: silhouette score, calinski-harabasz, domain-specific metrics
- Always report confidence intervals via cross-validation

**Step 4.2: Diagnostic Plots**
- Learning curves (training size vs. score) — detect underfitting/overfitting
- Validation curves (hyperparameter vs. score)
- Confusion matrix heatmap (classification)
- Residual plots (regression)
- Calibration curves (probability calibration)

**Step 4.3: Model Comparison**

Build a comparison table:
```
| Model          | CV Mean ± Std | Train Score | Test Score | Fit Time |
|----------------|---------------|-------------|------------|----------|
| Baseline       | ...           | ...         | ...        | ...      |
| Random Forest  | ...           | ...         | ...        | ...      |
| LightGBM       | ...           | ...         | ...        | ...      |
```

**Step 4.4: Explainability**
- SHAP values for feature importance (works for any model)
- Partial Dependence Plots for key features
- For deep learning: Grad-CAM (images), attention visualization (text)

**Step 4.5: Fairness Audit**
- If sensitive attributes exist (gender, race, age), evaluate metrics per group
- Check for disparate impact
- Report and flag any significant performance gaps

**Step 4.6: Error Analysis**
- Examine worst predictions — what do they have in common?
- Check for systematic patterns in errors
- Feed insights back to feature engineering if needed

### Stage 5: Deliver — Output Results

**Step 5.1: Determine Output Format**

| Task Complexity | Output |
|----------------|--------|
| Quick question ("is this data normally distributed?") | Inline text + plot |
| Single analysis ("classify these customers") | Results + key visualizations + brief report |
| Full project ("build me a churn prediction system") | Complete project directory |

**Step 5.2: For Inline Results**
- Print key metrics clearly
- Save plots as PNG files, display inline
- Provide actionable interpretation

**Step 5.3: For Notebook Output**
Run `scripts/report_generator.py` to create a Jupyter notebook with:
- Markdown explanations between code cells (tutorial style, inspired by Hands-On ML)
- All visualizations embedded
- Reproducible: random seeds set, data paths relative

**Step 5.4: For Full Project**
Generate the standard ML project structure:
```
project-name/
├── data/raw/              # Original data (never modified)
├── data/processed/        # Cleaned, feature-engineered data
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   └── 03_evaluation.ipynb
├── src/
│   ├── data.py            # Data loading and preprocessing
│   ├── features.py        # Feature engineering
│   ├── model.py           # Model definition and training
│   └── evaluate.py        # Evaluation utilities
├── models/                # Saved model artifacts
├── reports/
│   ├── figures/           # Saved plots
│   └── metrics.json       # Final metrics
├── configs/
│   └── config.yaml        # Hyperparameters and settings
├── requirements.txt
├── Dockerfile             # (if deployment requested)
└── README.md
```

**Step 5.5: For Deployment**
When the user wants to deploy, read `references/mlops-deploy.md` for:
- Model serialization (joblib/pickle for sklearn, torch.save for PyTorch, ONNX for cross-framework)
- REST API wrapping (FastAPI/Flask)
- Docker containerization
- Monitoring and drift detection

## Data Engineering Tasks

When the user needs ETL pipelines, data quality management, or large-scale processing:
- Read `references/data-engineering.md`
- Design pipelines with clear extraction → transformation → loading stages
- For large data: recommend Spark/Dask with code generation

## Key Reminders

- **Never skip EDA** — even if the user asks to "just train a model", at least run basic profiling
- **Always set random seeds** — reproducibility is non-negotiable
- **Document assumptions** — in comments or markdown cells
- **Version control data and models** — suggest DVC for large artifacts
- **Test the pipeline end-to-end** — before declaring victory, verify the full flow works
