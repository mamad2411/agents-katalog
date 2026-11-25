---
name: langchain
description: Framework para construir aplicações com LLM usando agentes, chains e RAG. Suporta múltiplos provedores (OpenAI, Anthropic, Google), 500+ integrações, agentes ReAct, tool calling, gerenciamento de memória e recuperação de vector stores. Use para construir chatbots, sistemas de perguntas e respostas, agentes autônomos ou aplicações RAG. Ideal para prototipagem rápida e deployments em produção.
version: 1.0.0
author: Orchestra Research
license: MIT
tags: [Agents, LangChain, RAG, Tool Calling, ReAct, Memory Management, Vector Stores, LLM Applications, Chatbots, Production]
dependencies: [langchain, langchain-core, langchain-openai, langchain-anthropic]
---

# LangChain - Construa aplicações com LLM, agentes e RAG

O framework mais popular para construir aplicações powered por LLM.

## Quando usar LangChain

**Use LangChain quando:**
- Construir agentes com tool calling e reasoning (padrão ReAct)
- Implementar pipelines RAG (retrieval-augmented generation)
- Precisar trocar provedores de LLM facilmente (OpenAI, Anthropic, Google)
- Criar chatbots com memória de conversa
- Prototipagem rápida de aplicações com LLM
- Deployments em produção com observabilidade LangSmith

**Métricas**:
- **119.000+ stars no GitHub**
- **272.000+ repositórios** usam LangChain
- **500+ integrações** (modelos, vector stores, tools)
- **3.800+ contribuidores**

**Use alternativas em vez disso**:
- **LlamaIndex**: focado em RAG, melhor para Q&A de documentos
- **LangGraph**: workflows stateful complexos, mais controle
- **Haystack**: pipelines de busca em produção
- **Semantic Kernel**: ecossistema Microsoft

## Início rápido

### Instalação

```bash
# Biblioteca principal (Python 3.10+)
pip install -U langchain

# Com OpenAI
pip install langchain-openai

# Com Anthropic
pip install langchain-anthropic

# Extras comuns
pip install langchain-community  # 500+ integrações
pip install langchain-chroma     # Vector store
```

### Uso básico de LLM

```python
from langchain_anthropic import ChatAnthropic

# Inicializar modelo
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")

# Conclusão simples
response = llm.invoke("Explain quantum computing in 2 sentences")
print(response.content)
```

### Criar um agente (padrão ReAct)

```python
from langchain.agents import create_agent
from langchain_anthropic import ChatAnthropic

# Definir tools
def get_weather(city: str) -> str:
    """Get current weather for a city."""
    return f"It's sunny in {city}, 72°F"

def search_web(query: str) -> str:
    """Search the web for information."""
    return f"Search results for: {query}"

# Criar agente (<10 linhas!)
agent = create_agent(
    model=ChatAnthropic(model="claude-sonnet-4-5-20250929"),
    tools=[get_weather, search_web],
    system_prompt="You are a helpful assistant. Use tools when needed."
)

# Executar agente
result = agent.invoke({"messages": [{"role": "user", "content": "What's the weather in Paris?"}]})
print(result["messages"][-1].content)
```

## Conceitos principais

### 1. Models - abstração de LLM

```python
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

# Trocar provedores facilmente
llm = ChatOpenAI(model="gpt-4o")
llm = ChatAnthropic(model="claude-sonnet-4-5-20250929")
llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")

# Streaming
for chunk in llm.stream("Write a poem"):
    print(chunk.content, end="", flush=True)
```

### 2. Chains - operações sequenciais

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Definir template de prompt
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Write a 3-sentence summary about {topic}"
)

# Criar chain
chain = LLMChain(llm=llm, prompt=prompt)

# Executar chain
result = chain.run(topic="machine learning")
```

### 3. Agents - reasoning com tools

**Padrão ReAct (Reasoning + Acting):**

```python
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.tools import Tool

# Definir tool customizada
calculator = Tool(
    name="Calculator",
    func=lambda x: eval(x),
    description="Useful for math calculations. Input: valid Python expression."
)

# Criar agente com tools
agent = create_tool_calling_agent(
    llm=llm,
    tools=[calculator, search_web],
    prompt="Answer questions using available tools"
)

# Criar executor
agent_executor = AgentExecutor(agent=agent, tools=[calculator], verbose=True)

# Executar com reasoning
result = agent_executor.invoke({"input": "What is 25 * 17 + 142?"})
```

### 4. Memory - histórico de conversa

```python
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Adicionar memória para rastrear conversa
memory = ConversationBufferMemory()

conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True
)

# Conversa multi-turno
conversation.predict(input="Hi, I'm Alice")
conversation.predict(input="What's my name?")  # Remembers "Alice"
```

## RAG (Retrieval-Augmented Generation)

### Pipeline RAG básico

```python
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain.chains import RetrievalQA

# 1. Carregar documentos
loader = WebBaseLoader("https://docs.python.org/3/tutorial/")
docs = loader.load()

# 2. Dividir em chunks
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
splits = text_splitter.split_documents(docs)

# 3. Criar embeddings e vector store
vectorstore = Chroma.from_documents(
    documents=splits,
    embedding=OpenAIEmbeddings()
)

# 4. Criar retriever
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# 5. Criar chain de QA
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# 6. Consultar
result = qa_chain({"query": "What are Python decorators?"})
print(result["result"])
print(f"Sources: {result['source_documents']}")
```

### RAG conversacional com memória

```python
from langchain.chains import ConversationalRetrievalChain

# RAG com memória de conversa
qa = ConversationalRetrievalChain.from_llm(
    llm=llm,
    retriever=retriever,
    memory=ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
)

# RAG multi-turno
qa({"question": "What is Python used for?"})
qa({"question": "Can you elaborate on web development?"})  # Remembers context
```

## Padrões avançados de agentes

### Saída estruturada

```python
from langchain_core.pydantic_v1 import BaseModel, Field

# Definir schema
class WeatherReport(BaseModel):
    city: str = Field(description="City name")
    temperature: float = Field(description="Temperature in Fahrenheit")
    condition: str = Field(description="Weather condition")

# Obter resposta estruturada
structured_llm = llm.with_structured_output(WeatherReport)
result = structured_llm.invoke("What's the weather in SF? It's 65F and sunny")
print(result.city, result.temperature, result.condition)
```

### Execução paralela de tools

```python
from langchain.agents import create_tool_calling_agent

# Agente paraleliza automaticamente tool calls independentes
agent = create_tool_calling_agent(
    llm=llm,
    tools=[get_weather, search_web, calculator]
)

# Isso chamará get_weather("Paris") e get_weather("London") em paralelo
result = agent.invoke({
    "messages": [{"role": "user", "content": "Compare weather in Paris and London"}]
})
```

### Streaming de execução de agente

```python
# Fazer stream dos passos do agente
for step in agent_executor.stream({"input": "Research AI trends"}):
    if "actions" in step:
        print(f"Tool: {step['actions'][0].tool}")
    if "output" in step:
        print(f"Output: {step['output']}")
```

## Padrões comuns

### QA multi-documento

```python
from langchain.chains.qa_with_sources import load_qa_with_sources_chain

# Carregar múltiplos documentos
docs = [
    loader.load("https://docs.python.org"),
    loader.load("https://docs.numpy.org")
]

# QA com citações de fontes
chain = load_qa_with_sources_chain(llm, chain_type="stuff")
result = chain({"input_documents": docs, "question": "How to use numpy arrays?"})
print(result["output_text"])  # Inclui citações de fontes
```

### Tools customizadas com tratamento de erros

```python
from langchain.tools import tool

@tool
def risky_operation(query: str) -> str:
    """Perform a risky operation that might fail."""
    try:
        # Your operation here
        result = perform_operation(query)
        return f"Success: {result}"
    except Exception as e:
        return f"Error: {str(e)}"

# Agente trata erros com graça
agent = create_agent(model=llm, tools=[risky_operation])
```

### Observabilidade LangSmith

```python
import os

# Habilitar tracing
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "your-api-key"
os.environ["LANGCHAIN_PROJECT"] = "my-project"

# Todos os chains/agentes são rastreados automaticamente
agent = create_agent(model=llm, tools=[calculator])
result = agent.invoke({"input": "Calculate 123 * 456"})

# Ver traces em smith.langchain.com
```

## Vector stores

### Chroma (local)

```python
from langchain_chroma import Chroma

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)
```

### Pinecone (cloud)

```python
from langchain_pinecone import PineconeVectorStore

vectorstore = PineconeVectorStore.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    index_name="my-index"
)
```

### FAISS (busca de similaridade)

```python
from langchain_community.vectorstores import FAISS

vectorstore = FAISS.from_documents(docs, OpenAIEmbeddings())
vectorstore.save_local("faiss_index")

# Carregar depois
vectorstore = FAISS.load_local("faiss_index", OpenAIEmbeddings())
```

## Document loaders

```python
# Páginas web
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader("https://example.com")

# PDFs
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("paper.pdf")

# GitHub
from langchain_community.document_loaders import GithubFileLoader
loader = GithubFileLoader(repo="user/repo", file_filter=lambda x: x.endswith(".py"))

# CSV
from langchain_community.document_loaders import CSVLoader
loader = CSVLoader("data.csv")
```

## Text splitters

```python
# Recursivo (recomendado para texto geral)
from langchain.text_splitter import RecursiveCharacterTextSplitter
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=["\n\n", "\n", " ", ""]
)

# Code-aware
from langchain.text_splitter import PythonCodeTextSplitter
splitter = PythonCodeTextSplitter(chunk_size=500)

# Semântico (por significado)
from langchain_experimental.text_splitter import SemanticChunker
splitter = SemanticChunker(OpenAIEmbeddings())
```

## Melhores práticas

1. **Comece simples** - Use `create_agent()` na maioria dos casos
2. **Habilite streaming** - Melhor UX para respostas longas
3. **Adicione tratamento de erros** - Tools podem falhar, trate com graça
4. **Use LangSmith** - Essencial para debugar agentes
5. **Otimize tamanho de chunk** - 500-1000 caracteres para RAG
6. **Versionize prompts** - Rastreie mudanças em produção
7. **Cache de embeddings** - Caro, cache quando possível
8. **Monitore custos** - Rastreie uso de tokens com LangSmith

## Benchmarks de performance

| Operação | Latência | Notas |
|----------|----------|-------|
| Simple LLM call | ~1-2s | Depende do provedor |
| Agent with 1 tool | ~3-5s | Overhead de reasoning ReAct |
| RAG retrieval | ~0.5-1s | Vector search + LLM |
| Embedding 1000 docs | ~10-30s | Depende do modelo |

## LangChain vs LangGraph

| Feature | LangChain | LangGraph |
|---------|-----------|-----------|
| **Ideal para** | Quick agents, RAG | Workflows complexos |
| **Nível de abstração** | Alto | Baixo |
| **Código para começar** | <10 linhas | ~30 linhas |
| **Controle** | Simples | Total |
| **Workflows stateful** | Limitado | Nativo |
| **Grafos cíclicos** | Não | Sim |
| **Human-in-loop** | Básico | Avançado |

**Use LangGraph quando:**
- Precisar de workflows stateful com ciclos
- Exigir controle refinado
- Construir sistemas multi-agente
- Aplicações em produção com lógica complexa

## Referências

- **[Agents Guide](references/agents.md)** - ReAct, tool calling, streaming
- **[RAG Guide](references/rag.md)** - Document loaders, retrievers, QA chains
- **[Integration Guide](references/integration.md)** - Vector stores, LangSmith, deployment

## Recursos

- **GitHub**: https://github.com/langchain-ai/langchain ⭐ 119.000+
- **Docs**: https://docs.langchain.com
- **API Reference**: https://reference.langchain.com/python
- **LangSmith**: https://smith.langchain.com (observabilidade)
- **Version**: 0.3+ (estável)
- **License**: MIT