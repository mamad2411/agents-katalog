---
name: pinecone-research
description: Agent RAG and long-term memory with Pinecone.
version: 1.0.0
author: immuhammadfurqan
license: MIT
dependencies: [pinecone-client, langchain-pinecone]
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [RAG, Pinecone, Memory, Research, Vector Database, Agent, Retrieval]

---

# Pinecone Research — Agent RAG与长期记忆功能

可将Pinecone用作Agent对话的检索增强生成（RAG）后端：用于存储嵌入向量、从过往会话中检索相关上下文，以及构建长期记忆体系。

## 何时使用此技能

**适用场景：**
- 使用Pinecone作为向量存储来构建Agent RAG流程
- 需要在不同Agent会话之间保持长期记忆的连续性
- 将检索功能与Agent工具的使用相结合
- 研究或开发语义搜索工作流

**如需通用Pinecone参考信息（索引管理、CRUD操作、混合搜索等），请改用mlops/pinecone技能：**
- 需要处理无需Agent集成的生产级基础设施时

## 快速入门

### 设置步骤

```bash
pip install pinecone-client langchain-pinecone langchain-openai
```

设置您的 API 密钥：
```bash
export PINECONE_API_KEY="your-api-key"
```

### 基础 RAG 流程

```python
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

# Initialize Pinecone
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])

# Create or connect to index
index_name = "agent-memory"
if index_name not in [i.name for i in pc.list_indexes()]:
    pc.create_index(
        name=index_name,
        dimension=1536,
        metric="cosine",
        spec=ServerlessSpec(cloud="aws", region="us-east-1"),
    )

# Build vector store
vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    index_name=index_name,
)

# Retrieve relevant context
retriever = vectorstore.as_retriever(search_kwargs={"k": 5})
results = retriever.invoke("What did the agent discuss yesterday?")
```

### 基于命名空间的会话内存

```python
# Store per-session memory
vectorstore = PineconeVectorStore(
    index=pc.Index(index_name),
    embedding=OpenAIEmbeddings(),
    namespace=f"session-{session_id}",
)

# Query across all sessions (no namespace filter)
all_memory = PineconeVectorStore(
    index=pc.Index(index_name),
    embedding=OpenAIEmbeddings(),
)
results = all_memory.similarity_search("relevant query", k=10)
```

## 最佳实践

1. **按会话或用户划分命名空间** —— 为多租户代理实现数据隔离  
2. **批量插入/更新** —— 每批处理100–200个向量以提高效率  
3. **元数据过滤** —— 用会话ID、时间戳和主题对向量进行标记  
4. **清理旧数据** —— 删除过时的命名空间以控制成本  
5. **采用无服务器架构** —— 支持自动扩展及按使用量计费  

## 资源链接

- **Pinecone官方文档**：https://docs.pinecone.io  
- **LangChain集成指南**：https://python.langchain.com/docs/integrations/vectorstores/pinecone  
- **免费套餐**：1个索引，100,000个向量（1536维）
