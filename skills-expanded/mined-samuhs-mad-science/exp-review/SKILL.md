---
name: exp-review
description: "Review experiment code and Jupyter notebooks on two axes in parallel sub-agents: standards (does the code follow the repo's documented coding standards?) and quality (reproducibility, fixed seeds, data leakage, security, scalability, error handling). Use when the user wants to review an experiment, notebook or ML pipeline before moving on."
---

Check whether the code follows the quality rules.

### 1. Reproducibility
* **Clean Execution:** Can the code run end-to-end without failing if the kernel is restarted? 
* **Dependency Management:** Are the libraries and exact versions documented (e.g., `requirements.txt`, `Pipfile`)?
* **Artifact & Data Versioning:** Are data paths and model artifacts versioned (e.g., DVC, MLflow, immutable S3 URIs) rather than relying on local, hardcoded paths (`C:/user/data.csv`)?
* **Fixed Seeds:** Is the `random_state` or `seed` fixed for all stochastic processes (data splits, weight initializations, ML algorithms) to guarantee deterministic results?

### 2. Security
* **Credential Leakage:** Are there any hardcoded passwords, API keys, access tokens, or DB URIs? Instruct the user to move these to environment variables or secret managers.
* **Sensitive Data (PII):** Is the model exposing or directly logging Personally Identifiable Information (e.g., SSN, names, emails)? Ensure data is anonymized or hashed.
* **Query Sanitization:** If the code dynamically queries databases, is it protected against SQL injection?

### 3. Scalability
* **Memory Optimization:** Are data types optimized (e.g., using `float32` instead of `float64`, or `category` instead of `object` in Pandas)? Will the code break if data volume doubles?
* **Vectorization:** Flag any iterative loops (like `for` loops or `iterrows`) over datasets. Suggest vectorized operations using NumPy/Pandas.
* **Framework Suitability:** Does the data volume require distributed processing (e.g., Spark/Dask) instead of in-memory processing (e.g., Pandas/Scikit-learn)?

### 4. Code Quality & Refactoring
* **Modularization:** Identify feature engineering and training steps that should be extracted into modular `.py` scripts. 
* **Dead Code Removal:** Point out and request the removal of scratchpad cells, raw Exploratory Data Analysis (EDA) plots, and stray prints (`df.head()`, `df.describe()`) that do not belong in a final pipeline.
* **Standards & Typing:** Ensure the code follows standard styling conventions (PEP8) and encourage the use of type hints for better maintainability.

### 5. Robustness & Error Handling
* **Edge Cases & Exceptions:** Does the inference pipeline have clear rules to handle null values (`NaN`), infinite values, or new categorical levels not seen during training?
* **Logging vs. Printing:** Flag any loose `print()` statements. Suggest replacing them with a properly configured `logging` module (INFO, WARNING, ERROR) for traceability.

### 6. Model Efficiency
* **Artifact Size:** Is the saved model file (`.pkl`, `.joblib`, `.onnx`) optimized for the deployment environment?
* **Inference Latency:** Does the prediction function contain unnecessary overhead that would bottleneck real-time API requirements?

**Output Format:**
For every code review, structure your response using the following sections:
1. **Executive Summary:** A brief assessment of the code's production readiness.
2. **Critical Issues (Blockers):** Security flaws, data leakage, or major reproducibility issues.
3. **Refactoring Suggestions:** Specific recommendations for scalability, code quality, and robustness, including code examples.
4. **Approval Status:** State clearly whether the code is "Approved for Production", "Requires Minor Revisions", or "Needs Major Refactoring".