---
name: medical-ai-code-review
description: Use this skill when reviewing, debugging, or improving medical AI, healthcare data, EMR, clinical NLP, medical imaging, multimodal AI, or model evaluation code. Trigger for requests mentioning 의료AI, EMR, 병원 데이터, patient-level split, data leakage, AUROC, AUPRC, validation, train, test, model, evaluation.
---

# Medical AI Code Review Skill

## Purpose

Review medical AI and healthcare data code with a focus on reproducibility, data leakage, patient safety, privacy, and research validity.

## Review Order

1. Summarize what the code is trying to do.
2. Identify critical bugs.
3. Check data leakage.
4. Check patient-level split.
5. Check missing values and class imbalance.
6. Check preprocessing consistency.
7. Check model training logic.
8. Check evaluation metrics.
9. Check reproducibility.
10. Check privacy and logging risks.
11. Provide corrected code.
12. Provide verification steps.

## Required Checks

Always check:

- Are train, validation, and test sets separated correctly?
- If multiple samples belong to the same patient, is patient-level split used?
- Are preprocessing steps fit only on training data?
- Are labels generated without future leakage?
- Are missing values handled explicitly?
- Is class imbalance reported?
- Are metrics appropriate for the clinical task?
- Are AUROC and AUPRC both considered for imbalanced classification?
- Are sensitivity and specificity reported when clinically relevant?
- Are PHI/PII values excluded from logs and outputs?
- Are random seeds set?
- Are results saved reproducibly?

## Output Format

## 결론
State the most important issue or recommendation first.

## 주요 문제
List bugs, risks, and methodological concerns.

## 수정 코드
Provide corrected or improved code.

## 수정 이유
Explain why each change matters.

## 검증 방법
Provide commands or manual checks.

## 연구적 의미
Explain how the change affects research validity.
