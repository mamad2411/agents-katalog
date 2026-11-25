---
name: clip
description: Zero-shot image classification and image-text search.
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [transformers, torch, pillow]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [Multimodal, CLIP, Vision-Language, Zero-Shot, Image Classification, OpenAI, Image Search, Cross-Modal Retrieval, Content Moderation]

---

# CLIP —— 对比学习语言-图像预训练模型

OpenAI开发的能够通过自然语言理解图像的模型。

## 何时使用CLIP

**适用场景：**
- 零样本图像分类（无需训练数据）
- 图像与文本的相似度/匹配检测
- 语义图像搜索
- 内容审核（识别不当内容及暴力画面）
- 视觉问答
- 跨模态检索（图像→文本，文本→图像）

**核心指标：**
- **GitHub星标数超过25,300个**
- 基于4亿组图像-文本对进行训练
- 在ImageNet零样本任务上的表现可与ResNet-50相媲美
- 采用MIT许可证

**可选替代方案：**
- **BLIP-2**：更出色的图像描述功能
- **LLaVA**：视觉语言对话模型
- **Segment Anything**：图像分割工具

## 快速入门

### 安装指南

```bash
pip install git+https://github.com/openai/CLIP.git
pip install torch torchvision ftfy regex tqdm
```

### 零样本分类

```python
import torch
import clip
from PIL import Image

# Load model
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Load image
image = preprocess(Image.open("photo.jpg")).unsqueeze(0).to(device)

# Define possible labels
text = clip.tokenize(["a dog", "a cat", "a bird", "a car"]).to(device)

# Compute similarity
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

    # Cosine similarity
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

# Print results
labels = ["a dog", "a cat", "a bird", "a car"]
for label, prob in zip(labels, probs[0]):
    print(f"{label}: {prob:.2%}")
```

## 可用模型

```python
# Models (sorted by size)
models = [
    "RN50",           # ResNet-50
    "RN101",          # ResNet-101
    "ViT-B/32",       # Vision Transformer (recommended)
    "ViT-B/16",       # Better quality, slower
    "ViT-L/14",       # Best quality, slowest
]

model, preprocess = clip.load("ViT-B/32")
```

| 模型 | 参数量 | 处理速度 | 质量表现 |
|-------|--------|----------|----------|
| RN50 | 1.02亿 | 快 | 较好 |
| ViT-B/32 | 1.51亿 | 中等 | 更优 |
| ViT-L/14 | 4.28亿 | 慢 | 最佳 |

## 图像与文本相似度检测

```python
# Compute embeddings
image_features = model.encode_image(image)
text_features = model.encode_text(text)

# Normalize
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)

# Cosine similarity
similarity = (image_features @ text_features.T).item()
print(f"Similarity: {similarity:.4f}")
```

## 语义图像搜索

```python
# Index images
image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
image_embeddings = []

for img_path in image_paths:
    image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)
    image_embeddings.append(embedding)

image_embeddings = torch.cat(image_embeddings)

# Search with text query
query = "a sunset over the ocean"
text_input = clip.tokenize([query]).to(device)
with torch.no_grad():
    text_embedding = model.encode_text(text_input)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)

# Find most similar images
similarities = (text_embedding @ image_embeddings.T).squeeze(0)
top_k = similarities.topk(3)

for idx, score in zip(top_k.indices, top_k.values):
    print(f"{image_paths[idx]}: {score:.3f}")
```

## 内容审核

```python
# Define categories
categories = [
    "safe for work",
    "not safe for work",
    "violent content",
    "graphic content"
]

text = clip.tokenize(categories).to(device)

# Check image
with torch.no_grad():
    logits_per_image, _ = model(image, text)
    probs = logits_per_image.softmax(dim=-1)

# Get classification
max_idx = probs.argmax().item()
max_prob = probs[0, max_idx].item()

print(f"Category: {categories[max_idx]} ({max_prob:.2%})")
```

## 批量处理

```python
# Process multiple images
images = [preprocess(Image.open(f"img{i}.jpg")) for i in range(10)]
images = torch.stack(images).to(device)

with torch.no_grad():
    image_features = model.encode_image(images)
    image_features /= image_features.norm(dim=-1, keepdim=True)

# Batch text
texts = ["a dog", "a cat", "a bird"]
text_tokens = clip.tokenize(texts).to(device)

with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)

# Similarity matrix (10 images × 3 texts)
similarities = image_features @ text_features.T
print(similarities.shape)  # (10, 3)
```

## 与向量数据库的集成

```python
# Store CLIP embeddings in Chroma/FAISS
import chromadb

client = chromadb.Client()
collection = client.create_collection("image_embeddings")

# Add image embeddings
for img_path, embedding in zip(image_paths, image_embeddings):
    collection.add(
        embeddings=[embedding.cpu().numpy().tolist()],
        metadatas=[{"path": img_path}],
        ids=[img_path]
    )

# Query with text
query = "a sunset"
text_embedding = model.encode_text(clip.tokenize([query]))
results = collection.query(
    query_embeddings=[text_embedding.cpu().numpy().tolist()],
    n_results=5
)
```

## 最佳实践

1. **大多数场景下使用 ViT-B/32**——性能与效率平衡良好  
2. **对嵌入向量进行归一化处理**——这是计算余弦相似度的必要步骤  
3. **采用批量处理方式**——效率更高  
4. **缓存嵌入向量**——重新计算成本极高  
5. **使用描述性标签**——能提升零样本任务的性能  
6. **推荐使用 GPU**——处理速度可提升 10 到 50 倍  
7. **对图像进行预处理**——请使用提供的预处理函数  

## 性能表现

| 操作类型 | CPU | GPU（V100） |
|----------|-----|------------|
| 图像编码 | 约 200 毫秒 | 约 20 毫秒 |
| 文本编码 | 约 50 毫秒 | 约 5 毫秒 |
| 相似度计算 | 小于 1 毫秒 | 小于 1 毫秒 |

## 局限性

1. **不适用于精细任务**——更适合处理大类别场景  
2. **需要描述性文本**——模糊的标签会导致性能不佳  
3. **基于网络数据存在偏差**——可能存在数据集偏差  
4. **不支持边界框识别**——仅能处理整幅图像  
5. **空间理解能力有限**——对位置和数量的分析能力较弱  

## 相关资源

- **GitHub 仓库**：https://github.com/openai/CLIP ⭐ 25,300+ 次点赞  
- **论文链接**：https://arxiv.org/abs/2103.00020  
- **Colab 实验环境**：https://colab.research.google.com/github/openai/clip/  
- **许可证**：MIT 许可证


