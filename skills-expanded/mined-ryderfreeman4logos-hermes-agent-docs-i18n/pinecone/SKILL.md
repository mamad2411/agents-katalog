---
name: pinecone
description: Managed vector DB for production RAG and search.
version: 1.0.1
author: Orchestra Research
license: MIT
dependencies: [pinecone]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [RAG, Pinecone, Vector Database, Managed Service, Serverless, Hybrid Search, Production, Auto-Scaling, Low Latency, Recommendations]

---

# Pinecone - 托管向量数据库

专为生产级 AI 应用打造的向量数据库。

## 何时选择 Pinecone

**适用场景：**
- 需要托管式、无服务器架构的向量数据库
- 生产环境中的 RAG 应用
- 需要自动扩展能力
- 对低延迟有严格要求（<100毫秒）
- 不愿自行管理基础设施
- 需要混合搜索功能（密集向量与稀疏向量）

**核心优势：**
- 全面托管的 SaaS 服务
- 可支持数十亿级向量数据自动扩展
- **p95 延迟低于 100毫秒**
- 99.9% 的正常运行时间服务等级协议

**可选择的其他替代方案：**
- **Chroma**：开源、自托管版本
- **FAISS**：离线使用、纯相似度搜索工具
- **Weaviate**：功能更丰富的自托管版本

## 快速入门

### 安装指南

```bash
pip install pinecone
```

> 注意：旧的 `pinecone-client` 包已不再维护。请安装 `pinecone`（版本 5 及以上，当前为 9.x 版）。导入语句仍需保持为 `from pinecone import Pinecone`。

### 基本用法

```python
from pinecone import Pinecone, ServerlessSpec

# Initialize
pc = Pinecone(api_key="your-api-key")

# Create index
pc.create_index(
    name="my-index",
    dimension=1536,  # Must match embedding dimension
    metric="cosine",  # or "euclidean", "dotproduct"
    spec=ServerlessSpec(cloud="aws", region="us-east-1")
)

# Connect to index
index = pc.Index("my-index")

# Upsert vectors
index.upsert(vectors=[
    {"id": "vec1", "values": [0.1, 0.2, ...], "metadata": {"category": "A"}},
    {"id": "vec2", "values": [0.3, 0.4, ...], "metadata": {"category": "B"}}
])

# Query
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    include_metadata=True
)

print(results["matches"])
```

## 核心操作

### 创建索引

```python
# Serverless (recommended)
pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",
    spec=ServerlessSpec(
        cloud="aws",         # or "gcp", "azure"
        region="us-east-1"
    )
)

# Pod-based (for consistent performance)
from pinecone import PodSpec

pc.create_index(
    name="my-index",
    dimension=1536,
    metric="cosine",
    spec=PodSpec(
        environment="us-east1-gcp",
        pod_type="p1.x1"
    )
)
```

### 向量插入/更新操作

```python
# Single upsert
index.upsert(vectors=[
    {
        "id": "doc1",
        "values": [0.1, 0.2, ...],  # 1536 dimensions
        "metadata": {
            "text": "Document content",
            "category": "tutorial",
            "timestamp": "2025-01-01"
        }
    }
])

# Batch upsert (recommended)
vectors = [
    {"id": f"vec{i}", "values": embedding, "metadata": metadata}
    for i, (embedding, metadata) in enumerate(zip(embeddings, metadatas))
]

index.upsert(vectors=vectors, batch_size=100)
```

### 查询向量

```python
# Basic query
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=10,
    include_metadata=True,
    include_values=False
)

# With metadata filtering
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    filter={"category": {"$eq": "tutorial"}}
)

# Namespace query
results = index.query(
    vector=[0.1, 0.2, ...],
    top_k=5,
    namespace="production"
)

# Access results
for match in results["matches"]:
    print(f"ID: {match['id']}")
    print(f"Score: {match['score']}")
    print(f"Metadata: {match['metadata']}")
```

### 元数据过滤

```python
# Exact match
filter = {"category": "tutorial"}

# Comparison
filter = {"price": {"$gte": 100}}  # $gt, $gte, $lt, $lte, $ne

# Logical operators
filter = {
    "$and": [
        {"category": "tutorial"},
        {"difficulty": {"$lte": 3}}
    ]
}  # Also: $or

# In operator
filter = {"tags": {"$in": ["python", "ml"]}}
```

## 命名空间

```python
# Partition data by namespace
index.upsert(
    vectors=[{"id": "vec1", "values": [...]}],
    namespace="user-123"
)

# Query specific namespace
results = index.query(
    vector=[...],
    namespace="user-123",
    top_k=5
)

# List namespaces
stats = index.describe_index_stats()
print(stats['namespaces'])
```

## 混合搜索（密集型 + 稀疏型）

```python
# Upsert with sparse vectors
index.upsert(vectors=[
    {
        "id": "doc1",
        "values": [0.1, 0.2, ...],  # Dense vector
        "sparse_values": {
            "indices": [10, 45, 123],  # Token IDs
            "values": [0.5, 0.3, 0.8]   # TF-IDF scores
        },
        "metadata": {"text": "..."}
    }
])

# Hybrid query
# NOTE: index.query() does NOT accept an `alpha` kwarg. Pinecone stores a
# single sparse-dense vector, so weighting must be applied by pre-scaling the
# query vectors before sending them. Use the hybrid_score_norm helper below
# (alpha * dense + (1 - alpha) * sparse; alpha=1 → pure dense, 0 → pure sparse).

def hybrid_score_norm(dense, sparse, alpha: float):
    """Scale dense/sparse query vectors for weighted hybrid search."""
    if not 0 <= alpha <= 1:
        raise ValueError("alpha must be between 0 and 1")
    scaled_sparse = {
        "indices": sparse["indices"],
        "values": [v * (1 - alpha) for v in sparse["values"]],
    }
    return [v * alpha for v in dense], scaled_sparse

hdense, hsparse = hybrid_score_norm(
    dense=[0.1, 0.2, ...],
    sparse={"indices": [10, 45], "values": [0.5, 0.3]},
    alpha=0.5,  # 0=sparse, 1=dense, 0.5=balanced
)

results = index.query(
    vector=hdense,
    sparse_vector=hsparse,
    top_k=5,
)
```

## 与 LangChain 的集成

```python
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

# Create vector store
vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    index_name="my-index"
)

# Query
results = vectorstore.similarity_search("query", k=5)

# With metadata filter
results = vectorstore.similarity_search(
    "query",
    k=5,
    filter={"category": "tutorial"}
)

# As retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
```

## 与 LlamaIndex 的集成

```python
from llama_index.vector_stores.pinecone import PineconeVectorStore

# Connect to Pinecone
pc = Pinecone(api_key="your-key")
pinecone_index = pc.Index("my-index")

# Create vector store
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)

# Use in LlamaIndex
from llama_index.core import StorageContext, VectorStoreIndex

storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
```

## 索引管理

```python
# List indices
indexes = pc.list_indexes()

# Describe index
index_info = pc.describe_index("my-index")
print(index_info)

# Get index stats
stats = index.describe_index_stats()
print(f"Total vectors: {stats['total_vector_count']}")
print(f"Namespaces: {stats['namespaces']}")

# Delete index
pc.delete_index("my-index")
```

## 删除向量

```python
# Delete by ID
index.delete(ids=["vec1", "vec2"])

# Delete by filter
index.delete(filter={"category": "old"})

# Delete all in namespace
index.delete(delete_all=True, namespace="test")

# Delete entire index
index.delete(delete_all=True)
```

## 最佳实践

1. **使用无服务器架构**——具备自动扩展能力，更具成本效益  
2. **批量插入/更新数据**——效率更高（每批处理100-200条记录）  
3. **添加元数据**——便于后续数据筛选  
4. **使用命名空间**——按用户或租户隔离数据  
5. **监控使用情况**——查看Pinecone控制面板  
6. **优化筛选条件**——对频繁被筛选的字段建立索引  
7. **利用免费套餐进行测试**——可创建1个索引，存储10万条向量  
8. **采用混合搜索方式**——提升搜索质量  
9. **设置合适的维度参数**——与嵌入模型相匹配  
10. **定期备份数据**——导出重要数据  

## 性能表现

| 操作类型 | 延迟时间 | 备注 |
|---------|---------|------|
| 插入/更新数据 | 约50-100毫秒 | 每批处理量对应此延迟 |
| 查询（p50分位值） | 约50毫秒 | 取决于索引规模 |
| 查询（p95分位值） | 约100毫秒 | 符合服务等级协议要求 |
| 元数据筛选 | 约+10-20毫秒 | 额外的处理开销 |

## 定价方案（2025年数据）

**无服务器架构**：
- 每百万次读取操作费用：0.096美元  
- 每百万次写入操作费用：0.06美元  
- 每GB存储空间每月费用：0.06美元  

**免费套餐**：
- 提供1个无服务器索引
- 支持存储10万条向量（1536个维度）
- 非常适合原型开发  

## 相关资源

- **官网**：https://www.pinecone.io  
- **文档**：https://docs.pinecone.io  
- **控制台**：https://app.pinecone.io  
- **定价页面**：https://www.pinecone.io/pricing


