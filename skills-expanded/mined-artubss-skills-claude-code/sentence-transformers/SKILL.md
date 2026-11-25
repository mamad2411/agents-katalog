---
name: sentence-transformers
description: Framework para embeddings de última geração em sentenças, textos e imagens. Oferece 5000+ modelos pré-treinados para similaridade semântica, clustering e retrieval. Suporta modelos multilíngues, específicos de domínio e multimodais. Use para gerar embeddings para RAG, busca semântica ou tarefas de similaridade. Melhor para geração de embeddings em produção.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Sentence Transformers, Embeddings, Similaridade Semântica, RAG, Multilíngue, Multimodal, Modelos Pré-Treinados, Clustering, Busca Semântica, Produção]
dependencies: [sentence-transformers, transformers, torch]
---

# Sentence Transformers - Embeddings de Última Geração

Framework Python para embeddings de sentenças e textos usando transformers.

## Quando usar Sentence Transformers

**Use quando:**
- Precisa de embeddings de alta qualidade para RAG
- Similaridade semântica e busca
- Clustering e classificação de textos
- Embeddings multilíngues (100+ idiomas)
- Executar embeddings localmente (sem API)
- Alternativa econômica aos embeddings do OpenAI

**Métricas**:
- **15.700+ estrelas no GitHub**
- **5000+ modelos pré-treinados**
- **100+ idiomas** suportados
- Baseado em PyTorch/Transformers

**Use alternativas em vez disso**:
- **OpenAI Embeddings**: Quando precisa de API, qualidade máxima
- **Instructor**: Instruções específicas de tarefa
- **Cohere Embed**: Serviço gerenciado

## Início rápido

### Instalação

```bash
pip install sentence-transformers
```

### Uso básico

```python
from sentence_transformers import SentenceTransformer

# Carregar modelo
model = SentenceTransformer('all-MiniLM-L6-v2')

# Gerar embeddings
sentences = [
    "This is an example sentence",
    "Each sentence is converted to a vector"
]

embeddings = model.encode(sentences)
print(embeddings.shape)  # (2, 384)

# Similaridade por cosseno
from sentence_transformers.util import cos_sim
similarity = cos_sim(embeddings[0], embeddings[1])
print(f"Similarity: {similarity.item():.4f}")
```

## Modelos populares

### Uso geral

```python
# Rápido, boa qualidade (384 dim)
model = SentenceTransformer('all-MiniLM-L6-v2')

# Melhor qualidade (768 dim)
model = SentenceTransformer('all-mpnet-base-v2')

# Melhor qualidade (1024 dim, mais lento)
model = SentenceTransformer('all-roberta-large-v1')
```

### Multilíngue

```python
# 50+ idiomas
model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

# 100+ idiomas
model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
```

### Específicos de domínio

```python
# Domínio jurídico
model = SentenceTransformer('nlpaueb/legal-bert-base-uncased')

# Artigos científicos
model = SentenceTransformer('allenai/specter')

# Código
model = SentenceTransformer('microsoft/codebert-base')
```

## Busca semântica

```python
from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer('all-MiniLM-L6-v2')

# Corpus
corpus = [
    "Python is a programming language",
    "Machine learning uses algorithms",
    "Neural networks are powerful"
]

# Codificar corpus
corpus_embeddings = model.encode(corpus, convert_to_tensor=True)

# Query
query = "What is Python?"
query_embedding = model.encode(query, convert_to_tensor=True)

# Encontrar mais similar
hits = util.semantic_search(query_embedding, corpus_embeddings, top_k=3)
print(hits)
```

## Computação de similaridade

```python
# Similaridade por cosseno
similarity = util.cos_sim(embedding1, embedding2)

# Produto escalar
similarity = util.dot_score(embedding1, embedding2)

# Similaridade por cosseno em pares
similarities = util.cos_sim(embeddings, embeddings)
```

## Codificação em batch

```python
# Processamento eficiente em batch
sentences = ["sentence 1", "sentence 2", ...] * 1000

embeddings = model.encode(
    sentences,
    batch_size=32,
    show_progress_bar=True,
    convert_to_tensor=False  # ou True para tensores PyTorch
)
```

## Fine-tuning

```python
from sentence_transformers import InputExample, losses
from torch.utils.data import DataLoader

# Dados de treinamento
train_examples = [
    InputExample(texts=['sentence 1', 'sentence 2'], label=0.8),
    InputExample(texts=['sentence 3', 'sentence 4'], label=0.3),
]

train_dataloader = DataLoader(train_examples, batch_size=16)

# Função de perda
train_loss = losses.CosineSimilarityLoss(model)

# Treinar
model.fit(
    train_objectives=[(train_dataloader, train_loss)],
    epochs=10,
    warmup_steps=100
)

# Salvar
model.save('my-finetuned-model')
```

## Integração com LangChain

```python
from langchain_community.embeddings import HuggingFaceEmbeddings

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

# Usar com armazenamentos de vetores
from langchain_chroma import Chroma

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=embeddings
)
```

## Integração com LlamaIndex

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

from llama_index.core import Settings
Settings.embed_model = embed_model

# Usar no índice
index = VectorStoreIndex.from_documents(documents)
```

## Guia de seleção de modelos

| Modelo | Dimensões | Velocidade | Qualidade | Caso de Uso |
|-------|------------|---------|---------|----------|
| all-MiniLM-L6-v2 | 384 | Rápido | Boa | Geral, prototipagem |
| all-mpnet-base-v2 | 768 | Médio | Melhor | RAG em produção |
| all-roberta-large-v1 | 1024 | Lento | Melhor | Alta precisão necessária |
| paraphrase-multilingual | 768 | Médio | Boa | Multilíngue |

## Boas práticas

1. **Comece com all-MiniLM-L6-v2** - Boa linha de base
2. **Normalize embeddings** - Melhor para similaridade por cosseno
3. **Use GPU se disponível** - 10× codificação mais rápida
4. **Codificação em batch** - Mais eficiente
5. **Cache de embeddings** - Caro recalcular
6. **Fine-tune para domínio** - Melhora qualidade
7. **Teste diferentes modelos** - Qualidade varia por tarefa
8. **Monitore memória** - Modelos grandes precisam mais RAM

## Performance

| Modelo | Velocidade (sentenças/seg) | Memória | Dimensão |
|-------|----------------------|---------|-----------|
| MiniLM | ~2000 | 120MB | 384 |
| MPNet | ~600 | 420MB | 768 |
| RoBERTa | ~300 | 1.3GB | 1024 |

## Recursos

- **GitHub**: https://github.com/UKPLab/sentence-transformers ⭐ 15.700+
- **Modelos**: https://huggingface.co/sentence-transformers
- **Docs**: https://www.sbert.net
- **License**: Apache 2.0