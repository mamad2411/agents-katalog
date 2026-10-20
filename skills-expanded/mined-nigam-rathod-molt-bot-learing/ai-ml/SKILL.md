# AI & Machine Learning Skill

Deep learning, LLM engineering, and ML systems.

## ML Frameworks

### PyTorch
```python
import torch
import torch.nn as nn

model = nn.Sequential(
    nn.Linear(784, 256),
    nn.ReLU(),
    nn.Dropout(0.2),
    nn.Linear(256, 10)
)
```

### TensorFlow/Keras
```python
import tensorflow as tf

model = tf.keras.Sequential([
    tf.keras.layers.Dense(256, activation='relu'),
    tf.keras.layers.Dropout(0.2),
    tf.keras.layers.Dense(10, activation='softmax')
])
```

## LLM Engineering

### Prompt Engineering
- Chain of Thought: "Let's think step by step"
- Few-shot: Give examples
- System prompts: Set persona/context
- Temperature: 0=deterministic, 1=creative

### RAG (Retrieval Augmented Generation)
```
Query → Embed → Search Vector DB → Get Chunks → Inject to Prompt → Generate
```

### Fine-tuning
- LoRA: Low-rank adaptation
- QLoRA: Quantized LoRA
- Full fine-tune: Requires compute

### Vector DBs
- Pinecone
- Weaviate
- Chroma
- Milvus
- pgvector

## ML Ops

### Pipeline
```
Data → Preprocess → Train → Evaluate → Deploy → Monitor
```

### Tools
- MLflow: Experiment tracking
- Weights & Biases: Logging
- Kubeflow: ML on K8s
- TFX: TensorFlow production

## Multi-Agent ML

```
Kimi: Prompt optimization, architecture
GLM5: Model research, deep analysis
MiniMax: Quick experiments, hyperparameter search
```

## Commands

- `/train` - Model training
- `/predict` - Inference
- `/rag` - RAG setup
- `/fine-tune` - Model fine-tuning
- `/embed` - Embeddings
