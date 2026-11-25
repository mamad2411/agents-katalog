---
name: clip
description: Modelo da OpenAI que conecta visão e linguagem. Permite classificação de imagens com zero-shot, correspondência imagem-texto e recuperação cross-modal. Treinado em 400M pares imagem-texto. Use para busca de imagens, moderação de conteúdo ou tarefas visão-linguagem sem fine-tuning. Melhor para compreensão geral de imagens.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Multimodal, CLIP, Vision-Language, Zero-Shot, Image Classification, OpenAI, Image Search, Cross-Modal Retrieval, Content Moderation]
dependencies: [transformers, torch, pillow]
---

# CLIP - Contrastive Language-Image Pre-Training

Modelo da OpenAI que compreende imagens a partir de linguagem natural.

## Quando usar CLIP

**Use quando:**
- Classificação de imagens com zero-shot (nenhum dado de treinamento necessário)
- Similaridade/correspondência imagem-texto
- Busca semântica de imagens
- Moderação de conteúdo (detectar NSFW, violência)
- Resposta a perguntas visuais
- Recuperação cross-modal (imagem→texto, texto→imagem)

**Métricas**:
- **Mais de 25.300 stars no GitHub**
- Treinado em 400M pares imagem-texto
- Equivalente ao ResNet-50 no ImageNet (zero-shot)
- Licença MIT

**Considere alternativas quando**:
- **BLIP-2**: Melhor para legendagem
- **LLaVA**: Chat visão-linguagem
- **Segment Anything**: Segmentação de imagens

## Início rápido

### Instalação

```bash
pip install git+https://github.com/openai/CLIP.git
pip install torch torchvision ftfy regex tqdm
```

### Classificação com zero-shot

```python
import torch
import clip
from PIL import Image

# Carregar modelo
device = "cuda" if torch.cuda.is_available() else "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

# Carregar imagem
image = preprocess(Image.open("photo.jpg")).unsqueeze(0).to(device)

# Definir rótulos possíveis
text = clip.tokenize(["a dog", "a cat", "a bird", "a car"]).to(device)

# Computar similaridade
with torch.no_grad():
    image_features = model.encode_image(image)
    text_features = model.encode_text(text)

    # Similaridade cosseno
    logits_per_image, logits_per_text = model(image, text)
    probs = logits_per_image.softmax(dim=-1).cpu().numpy()

# Exibir resultados
labels = ["a dog", "a cat", "a bird", "a car"]
for label, prob in zip(labels, probs[0]):
    print(f"{label}: {prob:.2%}")
```

## Modelos disponíveis

```python
# Modelos (ordenados por tamanho)
models = [
    "RN50",           # ResNet-50
    "RN101",          # ResNet-101
    "ViT-B/32",       # Vision Transformer (recomendado)
    "ViT-B/16",       # Melhor qualidade, mais lento
    "ViT-L/14",       # Melhor qualidade, mais lento
]

model, preprocess = clip.load("ViT-B/32")
```

| Modelo | Parâmetros | Velocidade | Qualidade |
|--------|-----------|-----------|----------|
| RN50 | 102M | Rápido | Bom |
| ViT-B/32 | 151M | Médio | Melhor |
| ViT-L/14 | 428M | Lento | Melhor |

## Similaridade imagem-texto

```python
# Computar embeddings
image_features = model.encode_image(image)
text_features = model.encode_text(text)

# Normalizar
image_features /= image_features.norm(dim=-1, keepdim=True)
text_features /= text_features.norm(dim=-1, keepdim=True)

# Similaridade cosseno
similarity = (image_features @ text_features.T).item()
print(f"Similarity: {similarity:.4f}")
```

## Busca semântica de imagens

```python
# Indexar imagens
image_paths = ["img1.jpg", "img2.jpg", "img3.jpg"]
image_embeddings = []

for img_path in image_paths:
    image = preprocess(Image.open(img_path)).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(image)
        embedding /= embedding.norm(dim=-1, keepdim=True)
    image_embeddings.append(embedding)

image_embeddings = torch.cat(image_embeddings)

# Buscar com query de texto
query = "a sunset over the ocean"
text_input = clip.tokenize([query]).to(device)
with torch.no_grad():
    text_embedding = model.encode_text(text_input)
    text_embedding /= text_embedding.norm(dim=-1, keepdim=True)

# Encontrar imagens mais similares
similarities = (text_embedding @ image_embeddings.T).squeeze(0)
top_k = similarities.topk(3)

for idx, score in zip(top_k.indices, top_k.values):
    print(f"{image_paths[idx]}: {score:.3f}")
```

## Moderação de conteúdo

```python
# Definir categorias
categories = [
    "safe for work",
    "not safe for work",
    "violent content",
    "graphic content"
]

text = clip.tokenize(categories).to(device)

# Verificar imagem
with torch.no_grad():
    logits_per_image, _ = model(image, text)
    probs = logits_per_image.softmax(dim=-1)

# Obter classificação
max_idx = probs.argmax().item()
max_prob = probs[0, max_idx].item()

print(f"Category: {categories[max_idx]} ({max_prob:.2%})")
```

## Processamento em lote

```python
# Processar múltiplas imagens
images = [preprocess(Image.open(f"img{i}.jpg")) for i in range(10)]
images = torch.stack(images).to(device)

with torch.no_grad():
    image_features = model.encode_image(images)
    image_features /= image_features.norm(dim=-1, keepdim=True)

# Texto em lote
texts = ["a dog", "a cat", "a bird"]
text_tokens = clip.tokenize(texts).to(device)

with torch.no_grad():
    text_features = model.encode_text(text_tokens)
    text_features /= text_features.norm(dim=-1, keepdim=True)

# Matriz de similaridade (10 imagens × 3 textos)
similarities = image_features @ text_features.T
print(similarities.shape)  # (10, 3)
```

## Integração com bancos de dados vetoriais

```python
# Armazenar embeddings CLIP em Chroma/FAISS
import chromadb

client = chromadb.Client()
collection = client.create_collection("image_embeddings")

# Adicionar embeddings de imagens
for img_path, embedding in zip(image_paths, image_embeddings):
    collection.add(
        embeddings=[embedding.cpu().numpy().tolist()],
        metadatas=[{"path": img_path}],
        ids=[img_path]
    )

# Consultar com texto
query = "a sunset"
text_embedding = model.encode_text(clip.tokenize([query]))
results = collection.query(
    query_embeddings=[text_embedding.cpu().numpy().tolist()],
    n_results=5
)
```

## Melhores práticas

1. **Use ViT-B/32 na maioria dos casos** - Bom balanço
2. **Normalize embeddings** - Necessário para similaridade cosseno
3. **Processamento em lote** - Mais eficiente
4. **Armazene embeddings em cache** - Custoso para recalcular
5. **Use rótulos descritivos** - Melhor desempenho com zero-shot
6. **GPU recomendada** - 10-50× mais rápido
7. **Pré-processe imagens** - Use a função preprocess fornecida

## Desempenho

| Operação | CPU | GPU (V100) |
|----------|-----|-----------|
| Codificação de imagem | ~200ms | ~20ms |
| Codificação de texto | ~50ms | ~5ms |
| Cálculo de similaridade | <1ms | <1ms |

## Limitações

1. **Não é para tarefas granulares** - Melhor para categorias amplas
2. **Requer texto descritivo** - Rótulos vagos têm desempenho ruim
3. **Viés em dados web** - Pode conter vieses do dataset
4. **Sem caixas delimitadoras** - Apenas imagem inteira
5. **Compreensão espacial limitada** - Fraco em posição/contagem

## Recursos

- **GitHub**: https://github.com/openai/CLIP ⭐ 25.300+
- **Paper**: https://arxiv.org/abs/2103.00020
- **Colab**: https://colab.research.google.com/github/openai/clip/
- **Licença**: MIT