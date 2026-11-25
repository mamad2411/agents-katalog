---
name: data-science
description: Data science and ML pipeline development from exploration to production.
---

# Data Science & Machine Learning

Complete ML lifecycle from data to production.

## Data Exploration
- **Pandas/Polars**: DataFrames, lazy evaluation, memory efficiency
- **Visualization**: Matplotlib, Seaborn, Plotly, D3.js
- **Statistics**: Hypothesis testing, distributions, correlation
- **Feature Analysis**: Mutual information, feature importance, SHAP values

## ML Frameworks
- **Scikit-learn**: Classical ML, pipelines, cross-validation
- **PyTorch**: Tensors, autograd, custom datasets, distributed training
- **TensorFlow/Keras**: Sequential, functional, subclassed models
- **Hugging Face**: Transformers, datasets, tokenizers, PEFT/LoRA

## Model Training
1. Data splitting (train/val/test, time-series split, stratified)
2. Hyperparameter tuning (Optuna, Ray Tune, grid/random/Bayesian)
3. Cross-validation (k-fold, LOOCV, time-series CV)
4. Early stopping, learning rate scheduling, gradient clipping
5. Distributed training (DDP, FSDP, DeepSpeed)

## MLOps
- **Experiment Tracking**: MLflow, Weights & Biases, Neptune
- **Model Registry**: Versioning, staging, approval workflows
- **Serving**: TorchServe, TF Serving, Triton, BentoML
- **Monitoring**: Drift detection, data quality, model performance

## Deep Learning Patterns
- **Computer Vision**: CNN, ViT, YOLO, segmentation, detection
- **NLP**: BERT, GPT, T5, RAG, embeddings, fine-tuning
- **Time Series**: LSTM, Transformer, Prophet, seasonal decomposition
- **Reinforcement Learning**: PPO, DQN, SAC, environment design

## Production Best Practices
1. Reproducible experiments (seed everything, log params)
2. Data versioning (DVC, LakeFS, Delta Lake)
3. Model testing (unit tests for data, integration tests for pipelines)
4. A/B testing for model deployment
5. Shadow mode before full rollout
