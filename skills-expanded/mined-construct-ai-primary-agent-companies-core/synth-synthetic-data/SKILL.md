---
name: synth-Synthetic-data
description: >
  Use when synthetic dataset generation, data augmentation, privacy-preserving data
  creation, or training data optimization is needed within DevForge AI. This agent
  generates realistic synthetic data for testing, training, and development.
---

# Synth - DevForge AI Synthetic Data Generation

## Overview
Synth generates synthetic datasets for DevForge AI, creating realistic, privacy-preserving data for testing, model training, and development. When real data is unavailable, sensitive, or insufficient, Synth produces statistically equivalent alternatives.

## When to Use
- When real data is unavailable but development/testing needs data
- When real data contains PII/sensitive information that cannot be used
- When training data is insufficient for ML model training
- When edge case data is needed that rarely occurs in production
- When data augmentation is needed to improve model robustness
- **Don't use when:** Real production data is available and approved for use

## Core Procedures

### Step 1: Analyze Data Requirements
1. What data schema is needed? (tables, fields, types, relationships)
2. What statistical properties must be preserved? (distributions, correlations)
3. What volume of data is needed? (rows, variety)
4. What edge cases must be included?
5. What privacy constraints apply? (no PII, anonymization level)

### Step 2: Design Generation Strategy
- **Statistical Modeling:** Fit distributions to known data characteristics
- **Rule-Based Generation:** Apply business rules and constraints
- **GAN/ML Generation:** Use generative models for complex data patterns
- **Hybrid Approach:** Combine methods for different data types

### Step 3: Generate Synthetic Data
- Generate data according to designed strategy
- Apply business rules and constraints
- Ensure referential integrity across related tables
- Include edge cases and boundary conditions
- Validate statistical properties match requirements

### Step 4: Validate Quality
- [ ] Statistical distributions match target (KS test, chi-square)
- [ ] Correlations preserved between related fields
- [ ] No PII or sensitive data leaked
- [ ] Business rules satisfied
- [ ] Edge cases present and correct
- [ ] Volume meets requirements

### Step 5: Deliver and Document
```
SYNTHETIC DATA DELIVERY
=======================
Dataset: [name and description]
Volume: [rows, tables, size]
Generation Method: [statistical/GAN/rule-based/hybrid]
Quality Metrics: [distribution match %, correlation preservation %]
Privacy Level: [no PII confirmed / anonymized / pseudonymized]
Edge Cases Included: [list]
Usage Guidelines: [how to use, limitations]
```

## Success Metrics
- Statistical fidelity: >=95% distribution match to target
- Privacy guarantee: 0% PII leakage in generated data
- Generation speed: <1 hour for 1M row datasets
- Edge case coverage: 100% of specified edge cases present

## Error Handling
- **Error:** Generated data doesn't match target distributions
  **Response:** Adjust generation parameters, increase sample size, try alternative generation method
- **Error:** PII detected in synthetic data
  **Response:** Immediately discard dataset, investigate source of leakage, regenerate with stricter privacy controls
- **Error:** Generation is too slow for required volume
  **Response:** Parallelize generation, reduce complexity, use simpler generation method

## Cross-Team Integration
**Related Skills:** dataforge-devforge-data-transformation, navigator-devforge-data-discovery, cortex-devforge-ai-reasoning, data-privacy-check
**Used By:** Cortex (ML training), Dataforge (pipeline testing), ALL agents needing test data