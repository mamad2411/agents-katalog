---
title: "AI/ML Development — v1"
description: "AI and Machine Learning development best practices"
globs: ["**/*.py", "**/*.ipynb", "src/**/*.py", "notebooks/**/*.ipynb"]
alwaysApply: false
priority: medium
---

# AI/ML Development Rules

## Technology Stack
- **Language**: Python 3.8+
- **Frameworks**: TensorFlow, PyTorch, Scikit-learn
- **Build Tool**: pip, conda
- **Package Manager**: pip, conda
- **Notebooks**: Jupyter, Colab

## Core Principles
- Follow data science best practices
- Implement proper data validation
- Use reproducible research methods
- Follow ML model development lifecycle
- Implement proper testing and validation

## Project Structure
src/
├─ data/              # Data processing
├─ models/            # ML models
├─ training/          # Training scripts
├─ evaluation/        # Model evaluation
└─ utils/             # Utility functions
notebooks/            # Jupyter notebooks
├─ exploration/       # Data exploration
├─ modeling/          # Model development
└─ evaluation/        # Model evaluation

## Coding Standards
- Use snake_case for variables and functions
- Use descriptive names for variables and functions
- Follow PEP 8 conventions
- Use proper indentation (4 spaces)
- Use type hints when possible

## Best Practices
- Implement proper data validation
- Use reproducible random seeds
- Implement proper model validation
- Use cross-validation techniques
- Implement proper error handling

## Common Patterns
- Data preprocessing pipelines
- Model training workflows
- Hyperparameter tuning
- Model evaluation and comparison
- Production model deployment

## Testing Strategy
- Write unit tests for data processing
- Implement model validation tests
- Use proper test data
- Test model performance metrics
- Maintain high test coverage
