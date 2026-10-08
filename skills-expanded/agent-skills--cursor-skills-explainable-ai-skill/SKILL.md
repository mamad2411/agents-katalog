# Explainable AI (XAI)

## Description

Feature attribution, concept-based explanations, saliency maps, and interpretability for black-box models.

## When to use

You need to explain why a model made a particular prediction to users, regulators, or domain experts.

## Key concepts

- **Feature attribution**: SHAP, LIME, Integrated Gradients, permutation importance.
- **Saliency maps**: Grad-CAM, SmoothGrad, attention visualization.
- **Concept-based explanations**: TCAV, concept activation vectors.
- **Global vs local**: explanations for single instances or model behavior overall.

## Code pattern

```python
import shap
import xgboost as xgb

model = xgb.XGBClassifier().fit(X_train, y_train)
explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_test)
shap.summary_plot(shap_values, X_test)
```

## Tuning notes

- Explanations must be faithful to the model, not just plausible.
- Be cautious with correlated features; attribution can be unstable.
- Use multiple explanation methods and compare them.

## Verification

1. Explain a model on a tabular dataset and compare SHAP and LIME.
2. Generate Grad-CAM maps for an image classifier and sanity-check.
3. Measure explanation stability under small input perturbations.

## References

- https://advanced.onlinelibrary.wiley.com/doi/10.1002/aisy.202400304
- https://arxiv.org/abs/2503.24365
- https://www.nature.com/articles/s41598-025-25839-y
- https://christophm.github.io/interpretable-ml-book/
