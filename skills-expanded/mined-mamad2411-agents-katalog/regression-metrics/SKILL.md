---
name: regression_metrics
description: Compute regression evaluation metrics
---

# Regression Metrics

## Description
Compute regression evaluation metrics

## When to Use
After regression model training

## Workflow
1. Compute MAE\n2. Compute RMSE\n3. Compute R-squared

## Tools Used
sklearn

## Examples
```python
from src.skills.evaluation.regression_metrics import Skill

skill = Skill()
result = await skill.run(SkillInput(data={"key": "value"}))
```

## Best Practices
Report all three metrics together
