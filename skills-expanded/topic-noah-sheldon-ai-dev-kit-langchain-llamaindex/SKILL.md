---
name: langchain-llamaindex
description: LangChain and LlamaIndex patterns for RAG pipelines, agent workflows, retrieval strategies, and cost-optimized LLM chains. Covers advanced RAG, multi-hop retrieval, reranking, and structured output.
origin: AI Dev Kit
---
# LangChain & LlamaIndex

Use this skill when building RAG pipelines, LangChain agent workflows, or LlamaIndex retrieval systems. Covers document processing, vector store integration, advanced retrieval strategies, and cost optimization.

## When to Use

- Building RAG (Retrieval-Augmented Generation) pipelines
- Creating LangChain chains or agents with tool calling
- Setting up LlamaIndex document indexes and query engines
- Implementing advanced retrieval: hybrid search, reranking, multi-hop
- Optimizing LLM token costs and response patterns

## Core Concepts

### LangChain Core Building Blocks
```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser

# Basic chain
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Answer based on context:\n{context}"),
    ("human", "{question}")
])
model = ChatOpenAI(model="gpt-4o-mini", temperature=0)
chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | model
    | StrOutputParser()
)
result = chain.invoke("What is the RAG evaluation strategy?")
```

### LangChain Agent with Tool Calling
```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.tools import tool

@tool
def search_database(query: str) -> str:
    """Search the knowledge base for relevant information."""
    return retriever.invoke(query)

tools = [search_database]
agent = create_tool_calling_agent(model, tools, prompt)
executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
```

### LlamaIndex RAG Pipeline
```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.node_parser import SentenceSplitter

# Load and parse documents
documents = SimpleDirectoryReader("data/").load_data()

# Chunking strategy
node_parser = SentenceSplitter(chunk_size=512, chunk_overlap=50)
nodes = node_parser.get_nodes_from_documents(documents)

# Build index with custom settings
index = VectorStoreIndex(
    nodes,
    llm=OpenAI(model="gpt-4o-mini"),
    embed_model=OpenAIEmbedding(model="text-embedding-3-small"),
)

# Query engine with retrieval configuration
query_engine = index.as_query_engine(
    similarity_top_k=5,
    response_mode="compact",  # compact, refine, tree_summarize
)
```

### Text Splitting Strategies
| Strategy | Use Case | Chunk Size | Overlap |
|----------|---------|-----------|---------|
| Character split | Simple text | 500-1000 chars | 50-100 chars |
| Token split | LLM-aligned boundaries | 256-512 tokens | 25-50 tokens |
| Semantic split | Meaning-preserving | Variable | N/A |
| Recursive character | Code, markdown | 512-1024 | 50-100 |
| Structure-aware | HTML, JSON, code blocks | Per-block | 0-25 |

### Vector Store Comparison
| Store | Best For | Filtering | Cost | Ops Overhead |
|-------|---------|-----------|------|-------------|
| Pinecone | Managed, scale | Metadata + namespace | $$/M queries | Low |
| Weaviate | GraphQL, hybrid | Rich filters + generative | $$ | Medium |
| Qdrant | Performance, quantization | Payload filtering | $ | Medium |
| pgvector | PostgreSQL-native | Full SQL + vector | $ (infra) | Low (if PG exists) |
| FAISS | Local, offline | Basic | Free (local) | Low |
| Chroma | Rapid prototyping | Metadata | Free (local) | Low |

### Advanced RAG Patterns

#### Hybrid Search (Dense + Sparse)
```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

dense_retriever = vector_store.as_retriever(search_kwargs={"k": 5})
bm25_retriever = BM25Retriever.from_texts(texts)
bm25_retriever.k = 5

ensemble = EnsembleRetriever(
    retrievers=[dense_retriever, bm25_retriever],
    weights=[0.7, 0.3],  # Weight dense higher for semantic, sparse for keyword
)
```

#### Multi-Query Retrieval
```python
from langchain.retrievers.multi_query import MultiQueryRetriever

retriever = MultiQueryRetriever.from_llm(
    retriever=vector_store.as_retriever(),
    llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
)
# Generates multiple query variations, deduplicates results
```

#### Contextual Compression
```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor

compressor = LLMChainExtractor.from_llm(model)
compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vector_store.as_retriever(),
)
# Retrieves broadly, then uses LLM to extract only relevant portions
```

#### Cross-Encoder Reranking
```python
from langchain.retrievers.document_compressors import CrossEncoderReranker
from langchain_community.cross_encoders import HuggingFaceCrossEncoder

model = HuggingFaceCrossEncoder(model_name="cross-encoder/ms-marco-MiniLM-L-6-v2")
reranker = CrossEncoderReranker(model=model, top_n=3)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=reranker,
    base_retriever=ensemble_retriever,
)
```

#### Query Rewriting + Multi-Hop
```python
from langchain_core.prompts import PromptTemplate

rewrite_prompt = PromptTemplate.from_template(
    "Given this question and retrieved context, generate a follow-up question "
    "that would help answer the original question more completely.\n"
    "Question: {question}\nContext: {context}\nFollow-up:"
)

# Chain: Query → Retrieve → Rewrite → Retrieve again → Generate
```

### Retrieval-Time Prompt Guards
```python
def sanitize_retrieved_context(context: str) -> str:
    """Remove potential injection vectors from retrieved content."""
    # Strip system prompt patterns
    context = re.sub(r'(?i)ignore previous instructions', '', context)
    context = re.sub(r'(?i)you are now', '', context)
    # Truncate to prevent context window overflow
    return context[:4000]
```

### Memory Patterns
```python
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory

# Buffer memory (full conversation history)
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

# Summary memory (condenses conversation for long sessions)
summary_memory = ConversationSummaryMemory(
    llm=ChatOpenAI(model="gpt-4o-mini"),
    memory_key="chat_history",
    return_messages=True,
)

# Vector store-backed memory (for very long conversations)
from langchain.memory import VectorStoreRetrieverMemory
vector_memory = VectorStoreRetrieverMemory(
    retriever=vector_store.as_retriever(search_kwargs={"k": 3}),
)
```

## Anti-Patterns

- **Sending entire document as context**: Use retrieval with top-k, not dump-everything
- **No chunking strategy**: Default character splitting breaks semantic units; use structure-aware splitting
- **Skipping reranking**: Top-k by embedding similarity alone misses keyword matches; add cross-encoder reranking
- **Hardcoding temperature**: Use temperature=0 for factual RAG, 0.3-0.7 for creative generation
- **No token budgeting**: Track token usage per chain; implement early exit for simple queries
- **Storing embeddings without metadata**: Always store document source, chunk index, and metadata for filtering
- **Ignoring rate limits**: Implement exponential backoff for API calls; use batch processing where possible

## Best Practices

- Chunk at semantic boundaries (paragraph breaks, code function boundaries) with 10% overlap
- Use `text-embedding-3-small` for most tasks; upgrade to `text-embedding-3-large` only if retrieval quality demands it
- Always add a reranking step (cross-encoder or Cohere rerank) between retrieval and generation
- Implement response validation: check that answers are grounded in retrieved context (faithfulness scoring)
- Cache frequent query results with semantic similarity matching to reduce API costs
- Use `gpt-4o-mini` for chain orchestration and extraction; reserve `gpt-4o` for final generation
- Log all chain executions with LangSmith for debugging and cost tracking
- Implement fallback: if retrieval returns low-confidence results, acknowledge uncertainty rather than hallucinate

## Related Skills

- `mlops-rag` — RAG evaluation, model versioning, observability
- `data-pipelines-ai` — Document ingestion pipelines, chunking strategies
- `openai-api` — Model selection, cost optimization, API patterns
- `eval-harness` — RAG evaluation with RAGAS, DeepEval, LangSmith
