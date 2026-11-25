---
name: deployment-explainability
description: "Use when turning a trained model into something usable (an app, an inference function, a demo) or adding explainability. Selects the RIGHT interpretability method per problem: Grad-CAM for CNN image classification, predicted boxes for detection, mask overlays for segmentation, embedding neighbors for face recognition, SHAP for tabular, attributions or attention for text, feature and temporal importance for time-series. Also covers preprocessing parity between training and inference, calibrated scores, out-of-distribution guardrails, and decision-support framing for high-stakes domains. Triggers on 'deploy', 'inference', 'Grad-CAM', 'SHAP', 'saliency', 'explainability', 'feature importance', 'build an app', 'gradio', 'streamlit'."
---

# Deployment and Explainability

## Preprocessing PARITY (the bug that silently ruins deployments)
The raw input a user uploads MUST pass through exactly the same pipeline as training (resize, crop, enhancement like CLAHE, normalization). Package it as one shared function reused by both training and inference. A mismatch produces confident but wrong predictions.

## Pick the explainability method that fits the model and task
Grad-CAM is only for convolutional image classifiers. It is not meaningful for detection, embeddings, tabular, or text. Choose by problem:

| Model or task | Explainability | Notes |
|---|---|---|
| CNN image classification | Grad-CAM, Grad-CAM++, Score-CAM | heatmap over the regions that drove the predicted class. Good for medical scans and single-object classification. |
| Vision Transformer classification | attention rollout, attention maps | more natural than Grad-CAM for pure ViTs. |
| Object detection (faces, vehicles, objects) | draw predicted boxes with class and confidence; optional D-RISE saliency | Grad-CAM is not standard for detectors. The boxes are the explanation. |
| Segmentation | overlay the predicted mask on the image, plus per-class confidence | |
| Face recognition or verification | nearest-neighbor example faces, embedding similarity score, t-SNE or UMAP of embeddings | Grad-CAM is not meaningful for metric-learning embeddings. |
| Tabular | SHAP (global summary and per-prediction), permutation importance | the standard for stakeholder trust. |
| Text or NLP | Integrated Gradients, token attributions, attention, SHAP for text | highlight the tokens that drove the decision. |
| LLM or RAG output | show the retrieved sources and the rationale; token logprobs for confidence | grounding is the explanation. |
| Time-series | feature and lag importance, temporal attention, SHAP on features | which past steps drove the forecast. |

Caption any saliency honestly: it shows where the model looked, not a ground-truth region.

## Present the result well
- Show the calibrated probability or score and the operating threshold, not just a label.
- For an ensemble, serve the single best model for a coherent prediction and explanation; show the ensemble score as a second opinion.

## Guardrails (especially high-stakes)
- Out-of-distribution check: flag inputs that do not look like the training domain (wrong modality, low confidence) instead of guessing.
- Framing: for medical or safety uses, state clearly that it is a decision-support or second-reader tool, not autonomous diagnosis. A research prototype needs validation and regulatory clearance before real use.
- Prefer a high-sensitivity operating point when a miss is far costlier than a false alarm.
- Log inputs and outputs for audit; never let the model auto-decide irreversible actions.

## Packaging
- Export the chosen model plus the shared preprocessing and an inference function `predict(raw)` that returns the label, the score, and the explanation appropriate to the task.
- A small Gradio or Streamlit app is the fastest trustworthy demo: drag-drop an input, then show the prediction, the score, the explanation, and the disclaimer. It runs on Colab, Hugging Face Spaces, or locally.
