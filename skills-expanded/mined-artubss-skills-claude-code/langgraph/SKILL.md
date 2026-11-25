---
name: langgraph
description: "Expert em LangGraph - o framework de nível produção para construir aplicações de IA com múltiplos atores e estado. Aborda construção de grafos, gerenciamento de estado, ciclos e ramificações, persistência com checkpointers, padrões human-in-the-loop e o padrão ReAct. Usado em produção no LinkedIn, Uber e 400+ empresas. Esta é a abordagem recomendada pelo LangChain para construir agentes. Use quando: langgraph, langchain agent, stateful agent, agent graph, react agent."
source: vibeship-spawner-skills (Apache 2.0)
---

# LangGraph

**Role**: Arquiteto de Agentes LangGraph

Você é um especialista na construção de agentes de IA de nível produção com LangGraph. Você compreende que agentes precisam de estrutura explícita - grafos tornam o fluxo visível e depurável. Você projeta o estado cuidadosamente, usa redutores apropriadamente e sempre considera persistência para produção. Você sabe quando ciclos são necessários e como prevenir loops infinitos.

## Capabilities

- Construção de grafos (StateGraph)
- Gerenciamento de estado e redutores
- Definições de nós e arestas
- Roteamento condicional
- Checkpointers e persistência
- Padrões human-in-the-loop
- Integração de ferramentas
- Execução com streaming e async

## Requirements

- Python 3.9+
- Pacote langgraph
- Acesso a API de LLM (OpenAI, Anthropic, etc.)
- Compreensão de conceitos de grafos

## Patterns

### Basic Agent Graph

Agente estilo ReAct simples com ferramentas

**Quando usar**: Agente único com chamada de ferramentas

```python
from typing import Annotated, TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool

# 1. Define State
class AgentState(TypedDict):
    messages: Annotated[list, add_messages]
    # add_messages reducer appends, doesn't overwrite

# 2. Define Tools
@tool
def search(query: str) -> str:
    """Search the web for information."""
    # Implementation here
    return f"Results for: {query}"

@tool
def calculator(expression: str) -> str:
    """Evaluate a math expression."""
    return str(eval(expression))

tools = [search, calculator]

# 3. Create LLM with tools
llm = ChatOpenAI(model="gpt-4o").bind_tools(tools)

# 4. Define Nodes
def agent(state: AgentState) -> dict:
    """The agent node - calls LLM."""
    response = llm.invoke(state["messages"])
    return {"messages": [response]}

# Tool node handles tool execution
tool_node = ToolNode(tools)

# 5. Define Routing
def should_continue(state: AgentState) -> str:
    """Route based on whether tools were called."""
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

# 6. Build Graph
graph = StateGraph(AgentState)

# Add nodes
graph.add_node("agent", agent)
graph.add_node("tools", tool_node)

# Add edges
graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", should_continue, ["tools", END])
graph.add_edge("tools", "agent")  # Loop back

# Compile
app = graph.compile()

# 7. Run
result = app.invoke({
    "messages": [("user", "What is 25 * 4?")]
})
```

### State with Reducers

Gerenciamento de estado complexo com redutores personalizados

**Quando usar**: Múltiplos agentes atualizando estado compartilhado

```python
from typing import Annotated, TypedDict
from operator import add
from langgraph.graph import StateGraph

# Custom reducer for merging dictionaries
def merge_dicts(left: dict, right: dict) -> dict:
    return {**left, **right}

# State with multiple reducers
class ResearchState(TypedDict):
    # Messages append (don't overwrite)
    messages: Annotated[list, add_messages]

    # Research findings merge
    findings: Annotated[dict, merge_dicts]

    # Sources accumulate
    sources: Annotated[list[str], add]

    # Current step (overwrites - no reducer)
    current_step: str

    # Error count (custom reducer)
    errors: Annotated[int, lambda a, b: a + b]

# Nodes return partial state updates
def researcher(state: ResearchState) -> dict:
    # Only return fields being updated
    return {
        "findings": {"topic_a": "New finding"},
        "sources": ["source1.com"],
        "current_step": "researching"
    }

def writer(state: ResearchState) -> dict:
    # Access accumulated state
    all_findings = state["findings"]
    all_sources = state["sources"]

    return {
        "messages": [("assistant", f"Report based on {len(all_sources)} sources")],
        "current_step": "writing"
    }

# Build graph
graph = StateGraph(ResearchState)
graph.add_node("researcher", researcher)
graph.add_node("writer", writer)
# ... add edges
```

### Conditional Branching

Rotear para caminhos diferentes baseado em estado

**Quando usar**: Múltiplos workflows possíveis

```python
from langgraph.graph import StateGraph, START, END

class RouterState(TypedDict):
    query: str
    query_type: str
    result: str

def classifier(state: RouterState) -> dict:
    """Classify the query type."""
    query = state["query"].lower()
    if "code" in query or "program" in query:
        return {"query_type": "coding"}
    elif "search" in query or "find" in query:
        return {"query_type": "search"}
    else:
        return {"query_type": "chat"}

def coding_agent(state: RouterState) -> dict:
    return {"result": "Here's your code..."}

def search_agent(state: RouterState) -> dict:
    return {"result": "Search results..."}

def chat_agent(state: RouterState) -> dict:
    return {"result": "Let me help..."}

# Routing function
def route_query(state: RouterState) -> str:
    """Route to appropriate agent."""
    query_type = state["query_type"]
    return query_type  # Returns node name

# Build graph
graph = StateGraph(RouterState)

graph.add_node("classifier", classifier)
graph.add_node("coding", coding_agent)
graph.add_node("search", search_agent)
graph.add_node("chat", chat_agent)

graph.add_edge(START, "classifier")

# Conditional edges from classifier
graph.add_conditional_edges(
    "classifier",
    route_query,
    {
        "coding": "coding",
        "search": "search",
        "chat": "chat"
    }
)

# All agents lead to END
graph.add_edge("coding", END)
graph.add_edge("search", END)
graph.add_edge("chat", END)

app = graph.compile()
```

## Anti-Patterns

### ❌ Infinite Loop Without Exit

**Por que é ruim**: O agente faz loop infinito. Queima tokens e custa caro. Eventualmente gera erro.

**Ao invés disso**: Sempre tenha condições de saída:
- Contador de iterações máximas no estado
- Condições END claras no roteamento
- Timeout no nível da aplicação

```python
def should_continue(state):
    if state["iterations"] > 10:
        return END
    if state["task_complete"]:
        return END
    return "agent"
```

### ❌ Stateless Nodes

**Por que é ruim**: Perde os benefícios do LangGraph. Estado não é persistido. Não consegue retomar conversas.

**Ao invés disso**: Sempre use estado para fluxo de dados. Retorne atualizações de estado dos nós. Use redutores para acumulação. Deixe LangGraph gerenciar o estado.

### ❌ Giant Monolithic State

**Por que é ruim**: Difícil de raciocinar. Dados desnecessários no contexto. Overhead de serialização.

**Ao invés disso**: Use input/output schemas para interfaces limpas. Estado privado para dados internos. Separação clara de responsabilidades.

## Limitations

- Apenas Python (TypeScript em estágio inicial)
- Curva de aprendizado para conceitos de grafos
- Complexidade no gerenciamento de estado
- Depuração pode ser desafiadora

## Related Skills

Funciona bem com: `crewai`, `autonomous-agents`, `langfuse`, `structured-output`