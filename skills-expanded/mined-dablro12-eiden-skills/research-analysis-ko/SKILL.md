---
name: research-analysis-ko
description: Use this skill when the user asks for Korean research analysis, data analysis, statistical analysis, regression analysis, p-value interpretation, model performance interpretation, table interpretation, experiment design, or report-ready analysis writing. Trigger for requests mentioning 분석, 데이터, 회귀분석, p-value, 통계, 성능지표, AUROC, AUPRC, 결과해석, 실험설계, 연구결과, 보고서 문장.
---

# Research Analysis Korean Skill

## Purpose

Support research-oriented data analysis in Korean.

The goal is not only to produce code, but also to connect the analysis to research questions, statistical validity, report writing, and practical interpretation.

## Default Response Structure

Use this structure unless the user requests another format:

## 결론
State the key analytical conclusion first.

## 분석 목적
Explain what the analysis is trying to verify.

## 필요한 데이터
List required columns, units, time range, inclusion/exclusion criteria, and expected data format.

## 전처리 계획
Explain missing values, outliers, scaling, categorical encoding, label definition, and split strategy.

## 분석 방법
Recommend the appropriate method, such as:
- descriptive statistics
- t-test
- chi-square test
- correlation analysis
- linear regression
- logistic regression
- panel regression
- time-series analysis
- classification model evaluation
- survival analysis
- ablation study
- error analysis

## 코드
Provide executable Python code when relevant.

## 결과 해석
Write Korean report-ready interpretation sentences.

## 한계
State what cannot be concluded and what assumptions were made.

## 다음 액션
Suggest the next practical step.

## Analysis Principles

Always check:

- Is the research question clear?
- Are the variables properly defined?
- Is the sample size sufficient?
- Are there missing values?
- Are there outliers?
- Is the statistical method appropriate?
- Is the p-value interpreted correctly?
- Are effect size and direction explained?
- Are results overinterpreted?
- Can the result be written into a report or paper?

## Medical AI / Healthcare Data Checks

For medical or healthcare data, additionally check:

- patient-level split
- data leakage
- class imbalance
- missing value pattern
- external validation possibility
- label definition
- temporal leakage
- PHI/PII masking
- subgroup performance
- calibration
- human review requirement

## Model Evaluation

For classification tasks, consider:

- AUROC
- AUPRC
- accuracy
- sensitivity
- specificity
- precision
- recall
- F1-score
- confusion matrix
- calibration curve
- decision threshold

For regression tasks, consider:

- MAE
- RMSE
- R²
- adjusted R²
- residual analysis
- confidence interval

## Report-Ready Writing Style

Use concise academic Korean.

Preferred expressions:

- “분석 결과, …한 경향이 확인되었다.”
- “이는 …와 관련될 가능성을 시사한다.”
- “다만, 본 분석은 …라는 한계를 가진다.”
- “따라서 추가적으로 …를 검증할 필요가 있다.”

Avoid:

- unsupported certainty
- exaggerated claims
- vague interpretation
- code without explanation
- p-value-only interpretation

## Final Output Standard

Every analysis answer should help the user move directly to one of the following:

- report paragraph
- paper draft
- slide copy
- experiment plan
- reproducible code
- next statistical test
