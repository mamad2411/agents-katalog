---
name: llamaindex
description: Framework de dados para construir aplicações LLM com RAG. Especializado em ingestão de documentos (300+ conectores), indexação e consultas. Inclui índices vetoriais, mecanismos de consulta, agentes e suporte multimodal. Use para perguntas sobre documentos, chatbots, recuperação de conhecimento ou construção de pipelines RAG. Ideal para aplicações LLM centradas em dados.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Agentes, LlamaIndex, RAG, Ingestão de Documentos, Índices Vetoriais, Mecanismos de Consulta, Recuperação de Conhecimento, Framework de Dados, Multimodal, Dados Privados, Conectores]
dependencies: [llama-index, openai, anthropic]
---

# LlamaIndex - Framework de Dados para Aplicações LLM

O framework líder para conectar LLMs com seus dados.

## Quando usar LlamaIndex

**Use LlamaIndex quando:**
- Construir aplicações RAG (geração aumentada por recuperação)
- Precisar responder perguntas sobre documentos sobre dados privados
- Ingerir dados de múltiplas fontes (300+ conectores)
- Criar bases de conhecimento para LLMs
- Construir chatbots com dados empresariais
- Precisar extrair dados estruturados de documentos

**Métricas**:
- **45.100+ estrelas no GitHub**
- **23.000+ repositórios** usam LlamaIndex
- **300+ conectores de dados** (LlamaHub)
- **1.715+ contribuidores**
- **v0.14.7** (estável)

**Use alternativas em vez disso**:
- **LangChain**: Mais propósito geral, melhor para agentes
- **Haystack**: Pipelines de busca em produção
- **txtai**: Busca semântica leve
- **Chroma**: Apenas armazenamento vetorial

## Início rápido

### Instalação

```bash
# Pacote iniciante (recomendado)
pip install llama-index

# Ou núcleo mínimo + integrações específicas
pip install llama-index-core
pip install llama-index-llms-openai
pip install llama-index-embeddings-openai
```

### Exemplo RAG em 5 linhas

```python
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader

# Carrega documentos
documents = SimpleDirectoryReader("data").load_data()

# Cria índice
index = VectorStoreIndex.from_documents(documents)

# Consulta
query_engine = index.as_query_engine()
response = query_engine.query("O que o autor fez crescendo?")
print(response)
```

## Conceitos principais

### 1. Conectores de dados - Carrega documentos

```python
from llama_index.core import SimpleDirectoryReader, Document
from llama_index.readers.web import SimpleWebPageReader
from llama_index.readers.github import GithubRepositoryReader

# Diretório de arquivos
documents = SimpleDirectoryReader("./data").load_data()

# Páginas web
reader = SimpleWebPageReader()
documents = reader.load_data(["https://example.com"])

# Repositório GitHub
reader = GithubRepositoryReader(owner="user", repo="repo")
documents = reader.load_data(branch="main")

# Criação manual de documento
doc = Document(
    text="Este é o conteúdo do documento",
    metadata={"source": "manual", "date": "2025-01-01"}
)
```

### 2. Índices - Estrutura de dados

```python
from llama_index.core import VectorStoreIndex, ListIndex, TreeIndex

# Índice vetorial (mais comum - busca semântica)
vector_index = VectorStoreIndex.from_documents(documents)

# Índice de lista (varredura sequencial)
list_index = ListIndex.from_documents(documents)

# Índice de árvore (resumo hierárquico)
tree_index = TreeIndex.from_documents(documents)

# Salva índice
index.storage_context.persist(persist_dir="./storage")

# Carrega índice
from llama_index.core import load_index_from_storage, StorageContext
storage_context = StorageContext.from_defaults(persist_dir="./storage")
index = load_index_from_storage(storage_context)
```

### 3. Mecanismos de consulta - Faça perguntas

```python
# Consulta básica
query_engine = index.as_query_engine()
response = query_engine.query("Qual é o tópico principal?")
print(response)

# Resposta em streaming
query_engine = index.as_query_engine(streaming=True)
response = query_engine.query("Explique computação quântica")
for text in response.response_gen:
    print(text, end="", flush=True)

# Configuração personalizada
query_engine = index.as_query_engine(
    similarity_top_k=3,          # Retorna top 3 chunks
    response_mode="compact",     # Ou "tree_summarize", "simple_summarize"
    verbose=True
)
```

### 4. Recuperadores - Encontra chunks relevantes

```python
# Recuperador vetorial
retriever = index.as_retriever(similarity_top_k=5)
nodes = retriever.retrieve("aprendizado de máquina")

# Com filtragem
retriever = index.as_retriever(
    similarity_top_k=3,
    filters={"metadata.category": "tutorial"}
)

# Recuperador customizado
from llama_index.core.retrievers import BaseRetriever

class CustomRetriever(BaseRetriever):
    def _retrieve(self, query_bundle):
        # Sua lógica de recuperação customizada
        return nodes
```

## Agentes com ferramentas

### Agente básico

```python
from llama_index.core.agent import FunctionAgent
from llama_index.llms.openai import OpenAI

# Define ferramentas
def multiply(a: int, b: int) -> int:
    """Multiplica dois números."""
    return a * b

def add(a: int, b: int) -> int:
    """Adiciona dois números."""
    return a + b

# Cria agente
llm = OpenAI(model="gpt-4o")
agent = FunctionAgent.from_tools(
    tools=[multiply, add],
    llm=llm,
    verbose=True
)

# Usa agente
response = agent.chat("Quanto é 25 * 17 + 142?")
print(response)
```

### Agente RAG (busca em documentos + ferramentas)

```python
from llama_index.core.tools import QueryEngineTool

# Cria índice como antes
index = VectorStoreIndex.from_documents(documents)

# Envolve mecanismo de consulta como ferramenta
query_tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(),
    name="python_docs",
    description="Útil para responder perguntas sobre programação Python"
)

# Agente com busca em documentos + calculadora
agent = FunctionAgent.from_tools(
    tools=[query_tool, multiply, add],
    llm=llm
)

# Agente decide quando buscar docs vs calcular
response = agent.chat("De acordo com os docs, para que o Python é utilizado?")
```

## Padrões RAG avançados

### Mecanismo de chat (conversacional)

```python
from llama_index.core.chat_engine import CondensePlusContextChatEngine

# Chat com memória
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",  # Ou "context", "react"
    verbose=True
)

# Conversa de múltiplas rodadas
response1 = chat_engine.chat("O que é Python?")
response2 = chat_engine.chat("Pode dar exemplos?")  # Lembra do contexto
response3 = chat_engine.chat("E sobre frameworks web?")
```

### Filtragem por metadados

```python
from llama_index.core.vector_stores import MetadataFilters, ExactMatchFilter

# Filtra por metadados
filters = MetadataFilters(
    filters=[
        ExactMatchFilter(key="category", value="tutorial"),
        ExactMatchFilter(key="difficulty", value="beginner")
    ]
)

retriever = index.as_retriever(
    similarity_top_k=3,
    filters=filters
)

query_engine = index.as_query_engine(filters=filters)
```

### Saída estruturada

```python
from pydantic import BaseModel
from llama_index.core.output_parsers import PydanticOutputParser

class Summary(BaseModel):
    title: str
    main_points: list[str]
    conclusion: str

# Obtém resposta estruturada
output_parser = PydanticOutputParser(output_cls=Summary)
query_engine = index.as_query_engine(output_parser=output_parser)

response = query_engine.query("Resuma o documento")
summary = response  # Modelo Pydantic
print(summary.title, summary.main_points)
```

## Padrões de ingestão de dados

### Múltiplos tipos de arquivo

```python
# Carrega todos os formatos suportados
documents = SimpleDirectoryReader(
    "./data",
    recursive=True,
    required_exts=[".pdf", ".docx", ".txt", ".md"]
).load_data()
```

### Web scraping

```python
from llama_index.readers.web import BeautifulSoupWebReader

reader = BeautifulSoupWebReader()
documents = reader.load_data(urls=[
    "https://docs.python.org/3/tutorial/",
    "https://docs.python.org/3/library/"
])
```

### Banco de dados

```python
from llama_index.readers.database import DatabaseReader

reader = DatabaseReader(
    sql_database_uri="postgresql://user:pass@localhost/db"
)
documents = reader.load_data(query="SELECT * FROM articles")
```

### Endpoints de API

```python
from llama_index.readers.json import JSONReader

reader = JSONReader()
documents = reader.load_data("https://api.example.com/data.json")
```

## Integrações de armazenamento vetorial

### Chroma (local)

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

# Inicializa Chroma
db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("my_collection")

# Cria armazenamento vetorial
vector_store = ChromaVectorStore(chroma_collection=collection)

# Usa em índice
from llama_index.core import StorageContext
storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
```

### Pinecone (nuvem)

```python
from llama_index.vector_stores.pinecone import PineconeVectorStore
import pinecone

# Inicializa Pinecone
pinecone.init(api_key="your-key", environment="us-west1-gcp")
pinecone_index = pinecone.Index("my-index")

# Cria armazenamento vetorial
vector_store = PineconeVectorStore(pinecone_index=pinecone_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
```

### FAISS (rápido)

```python
from llama_index.vector_stores.faiss import FaissVectorStore
import faiss

# Cria índice FAISS
d = 1536  # Dimensão dos embeddings
faiss_index = faiss.IndexFlatL2(d)

vector_store = FaissVectorStore(faiss_index=faiss_index)
storage_context = StorageContext.from_defaults(vector_store=vector_store)

index = VectorStoreIndex.from_documents(documents, storage_context=storage_context)
```

## Customização

### LLM customizado

```python
from llama_index.llms.anthropic import Anthropic
from llama_index.core import Settings

# Define LLM global
Settings.llm = Anthropic(model="claude-sonnet-4-5-20250929")

# Agora todas as consultas usam Anthropic
query_engine = index.as_query_engine()
```

### Embeddings customizados

```python
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

# Usa embeddings HuggingFace
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-mpnet-base-v2"
)

index = VectorStoreIndex.from_documents(documents)
```

### Templates de prompt customizados

```python
from llama_index.core import PromptTemplate

qa_prompt = PromptTemplate(
    "Contexto: {context_str}\n"
    "Pergunta: {query_str}\n"
    "Responda a pergunta baseado apenas no contexto. "
    "Se a resposta não estiver no contexto, diga 'Não sei'.\n"
    "Resposta: "
)

query_engine = index.as_query_engine(text_qa_template=qa_prompt)
```

## RAG multimodal

### Imagem + texto

```python
from llama_index.core import SimpleDirectoryReader
from llama_index.multi_modal_llms.openai import OpenAIMultiModal

# Carrega imagens e documentos
documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".jpg", ".png", ".pdf"]
).load_data()

# Índice multimodal
index = VectorStoreIndex.from_documents(documents)

# Consulta com LLM multimodal
multi_modal_llm = OpenAIMultiModal(model="gpt-4o")
query_engine = index.as_query_engine(llm=multi_modal_llm)

response = query_engine.query("O que está no diagrama na página 3?")
```

## Avaliação

### Qualidade da resposta

```python
from llama_index.core.evaluation import RelevancyEvaluator, FaithfulnessEvaluator

# Avalia relevância
relevancy = RelevancyEvaluator()
result = relevancy.evaluate_response(
    query="O que é Python?",
    response=response
)
print(f"Relevância: {result.passing}")

# Avalia fidelidade (sem alucinação)
faithfulness = FaithfulnessEvaluator()
result = faithfulness.evaluate_response(
    query="O que é Python?",
    response=response
)
print(f"Fidelidade: {result.passing}")
```

## Melhores práticas

1. **Use índices vetoriais na maioria dos casos** - Melhor desempenho
2. **Salve índices em disco** - Evita re-indexação
3. **Divida documentos corretamente** - Ótimo entre 512-1024 tokens
4. **Adicione metadados** - Habilita filtragem e rastreamento
5. **Use streaming** - Melhor UX para respostas longas
6. **Ative verbose durante desenvolvimento** - Veja o processo de recuperação
7. **Avalie respostas** - Verifique relevância e fidelidade
8. **Use chat engine para conversas** - Memória integrada
9. **Persista armazenamento** - Não perca seu índice
10. **Monitore custos** - Rastreie uso de embeddings e LLM

## Padrões comuns

### Sistema de perguntas sobre documentos

```python
# Pipeline RAG completo
documents = SimpleDirectoryReader("docs").load_data()
index = VectorStoreIndex.from_documents(documents)
index.storage_context.persist(persist_dir="./storage")

# Consulta
query_engine = index.as_query_engine(
    similarity_top_k=3,
    response_mode="compact",
    verbose=True
)
response = query_engine.query("Qual é o tópico principal?")
print(response)
print(f"Fontes: {[node.metadata['file_name'] for node in response.source_nodes]}")
```

### Chatbot com memória

```python
# Interface conversacional
chat_engine = index.as_chat_engine(
    chat_mode="condense_plus_context",
    verbose=True
)

# Chat de múltiplas rodadas
while True:
    user_input = input("Você: ")
    if user_input.lower() == "sair":
        break
    response = chat_engine.chat(user_input)
    print(f"Bot: {response}")
```

## Benchmarks de desempenho

| Operação | Latência | Notas |
|-----------|----------|-------|
| Indexar 100 docs | ~10-30s | Uma única vez, pode ser persistido |
| Consulta (vetorial) | ~0.5-2s | Recuperação + LLM |
| Consulta em streaming | ~0.5s primeiro token | Melhor UX |
| Agente com ferramentas | ~3-8s | Múltiplas chamadas de ferramenta |

## LlamaIndex vs LangChain

| Recurso | LlamaIndex | LangChain |
|---------|------------|-----------|
| **Ideal para** | RAG, perguntas sobre documentos | Agentes, apps LLM gerais |
| **Conectores de dados** | 300+ (LlamaHub) | 100+ |
| **Foco RAG** | Recurso principal | Um de muitos |
| **Curva de aprendizado** | Mais fácil para RAG | Mais íngreme |
| **Customização** | Alta | Muito alta |
| **Documentação** | Excelente | Boa |

**Use LlamaIndex quando:**
- Seu caso de uso principal é RAG
- Precisa de muitos conectores de dados
- Quer API mais simples para perguntas sobre documentos
- Construindo sistema de recuperação de conhecimento

**Use LangChain quando:**
- Construindo agentes complexos
- Precisa de ferramentas mais gerais
- Quer mais flexibilidade
- Workflows multi-etapa complexos

## Referências

- **[Guia de Mecanismos de Consulta](references/query_engines.md)** - Modos de consulta, customização, streaming
- **[Guia de Agentes](references/agents.md)** - Criação de ferramentas, agentes RAG, raciocínio multi-etapa
- **[Guia de Conectores de Dados](references/data_connectors.md)** - 300+ conectores, carregadores customizados

## Recursos

- **GitHub**: https://github.com/run-llama/llama_index ⭐ 45.100+
- **Docs**: https://developers.llamaindex.ai/python/framework/
- **LlamaHub**: https://llamahub.ai (conectores de dados)
- **LlamaCloud**: https://cloud.llamaindex.ai (empresarial)
- **Discord**: https://discord.gg/dGcwcsnxhU
- **Versão**: 0.14.7+
- **Licença**: MIT