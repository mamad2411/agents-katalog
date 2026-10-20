---
name: langgraph-agents
description: "Agentes y workflows con LangGraph 1.x: StateGraph, estado tipado y reducers, edges condicionales, Command, Send, checkpointers y Store, human-in-the-loop con interrupt, subgrafos, multi-agente, streaming y despliegue. Usar al crear o modificar agentes con estado o flujos multi-paso."
---

# langgraph-agents

## Objetivo
Diseñar grafos de estado explícitos y robustos: estado tipado con reducers correctos, nodos pequeños y testeables, routing claro, persistencia duradera, intervención humana segura, streaming a clientes y trazabilidad en LangSmith.

## Cuándo aplicarla
- El flujo tiene varios pasos, ramas, ciclos o paralelismo.
- Hace falta memoria por conversación (thread) o entre conversaciones (Store).
- Se requiere aprobación/edición humana en mitad de la ejecución.
- Varios agentes especializados colaboran (supervisor, handoffs, router).
- Si basta un modelo con tools en bucle, usa `create_agent` (`backend:langchain-chains`): ya es un grafo LangGraph compilado y admite checkpointer, streaming e interrupts.

## Antes de empezar
1. Carga `core:project-context`. **Verifica la versión en el manifiesto del proyecto**: esta skill apunta a `langgraph` 1.x (1.2 en sept. 2026), `langgraph-checkpoint-postgres`, `langchain` 1.x. JS: `@langchain/langgraph` 1.x.
2. Diferencias que importan: `langgraph.prebuilt.create_react_agent` está deprecado en favor de `langchain.agents.create_agent`; `stream(..., version="v2")` (formato unificado `{"type","ns","data"}`) requiere ≥ 1.1; `stream_events(version="v3")` con proyecciones tipadas llegó en 1.2 y está en **beta**; `Runtime`/`context_schema` sustituyen a `config["configurable"]` para datos de contexto.
3. Ante dudas de firmas, verifica en `docs.langchain.com/oss/python/langgraph/`.

## Estructura
```
app/agents/<nombre>/
├── state.py      # State, InputState, OutputState, Context
├── prompts.py
├── tools.py
├── nodes.py      # funciones de nodo y routing
├── graph.py      # build_graph(...) -> CompiledStateGraph; graph = build_graph() para langgraph.json
tests/agents/<nombre>/test_nodes.py, test_graph.py
```

## Estado y reducers
```python
from dataclasses import dataclass
from operator import add
from typing import Annotated, Literal
from typing_extensions import TypedDict
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list[AnyMessage], add_messages]   # agrega/actualiza por id
    documents: Annotated[list[str], add]                  # concatena (útil con nodos paralelos)
    intent: Literal["refund", "question", "other"] | None # sin reducer: último valor gana
    attempts: int

@dataclass
class Context:          # inmutable por run: no se persiste en el estado
    user_id: str
    tenant_id: str
```
- Campos que escriben varios nodos en paralelo **necesitan reducer**, si no LangGraph lanza `InvalidUpdateError`.
- `MessagesState` es un atajo con `messages` + `add_messages`; extiéndelo con tus campos.
- Para "vaciar" un campo con reducer usa `Overwrite([])` (de `langgraph.types`) en lugar de devolver `[]`, verifica disponibilidad en tu versión.
- `StateGraph(State, input_schema=InputState, output_schema=OutputState, context_schema=Context)` para contratos públicos más pequeños que el estado interno.
- Estado serializable (primitivos, Pydantic, mensajes). Nada de clientes, conexiones ni funciones.

## Nodos y routing
```python
from langgraph.runtime import Runtime
from langgraph.types import Command

async def classify(state: State, runtime: Runtime[Context]) -> dict:
    result = await classifier.ainvoke(state["messages"])
    return {"intent": result.intent}                     # actualización parcial

def route_intent(state: State) -> Literal["refund", "answer", "__end__"]:
    return {"refund": "refund", "question": "answer"}.get(state["intent"], "__end__")

async def refund(state: State, runtime: Runtime[Context]) -> Command[Literal["answer", "escalate"]]:
    ok = await refunds.try_refund(user_id=runtime.context.user_id, ...)
    return Command(update={"attempts": state["attempts"] + 1}, goto="answer" if ok else "escalate")
```
```python
from langgraph.graph import END, START, StateGraph

def build_graph(checkpointer=None, store=None):
    builder = StateGraph(State, context_schema=Context)
    builder.add_node("classify", classify)
    builder.add_node("refund", refund)
    builder.add_node("answer", answer)
    builder.add_node("escalate", escalate)
    builder.add_edge(START, "classify")
    builder.add_conditional_edges("classify", route_intent)
    builder.add_edge("answer", END)
    builder.add_edge("escalate", END)
    return builder.compile(checkpointer=checkpointer, store=store)
```
- Los nodos devuelven solo las claves que cambian; nunca mutes `state` in-place.
- Routing con función (`add_conditional_edges`) o con `Command(goto=...)` desde el nodo; no mezcles edges estáticos y `Command` desde el mismo nodo. Tipar el retorno (`Literal`/`Command[Literal[...]]`) permite dibujar el grafo.
- Map-reduce: una función de routing devuelve `[Send("worker", {"item": x}) for x in items]` y el campo resultado usa reducer `add`.
- Política de reintentos por nodo: `add_node("call_api", fn, retry_policy=RetryPolicy(max_attempts=3))` (`langgraph.types`); caché con `cache_policy=CachePolicy(ttl=...)` + `compile(cache=...)`.
- Limita ciclos con contadores en el estado y `config={"recursion_limit": 25}`.

## Tools dentro de un grafo propio
```python
from langgraph.prebuilt import ToolNode, tools_condition

model_with_tools = model.bind_tools(tools)

async def call_model(state: State) -> dict:
    return {"messages": [await model_with_tools.ainvoke(state["messages"])]}

builder.add_node("model", call_model)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "model")
builder.add_conditional_edges("model", tools_condition)   # → "tools" o END
builder.add_edge("tools", "model")
```
Si solo necesitas este bucle, `create_agent` lo hace con middleware; usa el grafo propio cuando haya pasos deterministas alrededor. Un agente de `create_agent` también puede añadirse como nodo/subgrafo.

## Persistencia
- **Checkpointer** (memoria por `thread_id`, requisito para interrupts y time travel): `InMemorySaver` en tests; `AsyncPostgresSaver` (paquete `langgraph-checkpoint-postgres`) en producción; `SqliteSaver` solo en desarrollo.
```python
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

async with AsyncPostgresSaver.from_conn_string(settings.checkpoint_db_url) as checkpointer:
    await checkpointer.setup()           # crea tablas; ejecútalo en despliegue/arranque
    graph = build_graph(checkpointer=checkpointer)
    await graph.ainvoke(inputs, {"configurable": {"thread_id": thread_id}}, context=Context(...))
```
- **Store** (memoria entre threads: preferencias, hechos del usuario): `InMemoryStore`/`PostgresStore`; en nodos vía `runtime.store`, con namespaces como `("memories", user_id)`.
- Inspección: `graph.get_state(cfg)`, `graph.get_state_history(cfg)`, `graph.update_state(cfg, values)`; reanudar desde un `checkpoint_id` concreto para time travel.
- `durability="sync" | "async" | "exit"` en invoke/stream controla cuándo se escriben checkpoints (por defecto `async`).
- `thread_id` < 255 caracteres; valida que pertenece al usuario autenticado; define retención de threads antiguos.

## Human-in-the-loop
```python
from langgraph.types import Command, interrupt

async def approve_refund(state: State) -> Command[Literal["refund", "answer"]]:
    decision = interrupt({"action": "refund", "amount": state["amount"], "question": "¿Aprobar reembolso?"})
    if decision.get("approved"):
        return Command(goto="refund")
    return Command(update={"messages": [AIMessage("Reembolso cancelado.")]}, goto="answer")

# Primera llamada: se detiene
out = await graph.ainvoke(inputs, cfg)
out["__interrupt__"]        # [Interrupt(value={...}, id=...)]
# Reanudar con la decisión humana (mismo thread_id)
out = await graph.ainvoke(Command(resume={"approved": True}), cfg)
```
Reglas: requiere checkpointer; **no envuelvas `interrupt()` en `try/except` genérico**; el nodo se re-ejecuta desde el inicio al reanudar, así que el código previo debe ser idempotente; mantén el orden de interrupts estable; con varios interrupts paralelos, reanuda con `Command(resume={interrupt_id: valor, ...})`. Para aprobar tool calls de un `create_agent`, usa `HumanInTheLoopMiddleware`.

## Streaming
```python
async for chunk in graph.astream(inputs, cfg, stream_mode=["updates", "messages", "custom"], version="v2"):
    match chunk["type"]:
        case "messages":
            token, meta = chunk["data"]          # meta["langgraph_node"] indica el nodo
        case "updates":
            ...                                   # {nodo: actualización}; "__interrupt__" si se pausa
        case "custom":
            ...                                   # datos emitidos con get_stream_writer()
```
- Emite progreso propio desde nodos/tools con `from langgraph.config import get_stream_writer; get_stream_writer()({"step": "searching"})`.
- `subgraphs=True` incluye eventos de subgrafos (con `ns` indicando la ruta).
- `stream_events(version="v3")` (beta, ≥ 1.2): `stream.messages`, `stream.values`, `stream.interrupted`, `stream.interrupts`, `stream.output`. Adóptalo solo tras verificar la API en la versión instalada.

Subgrafos, patrones multi-agente (subagentes como tools, handoffs con `Command.PARENT`, router), memoria a largo plazo, despliegue con `langgraph.json`/Agent Server, integración con FastAPI y equivalentes JS: lee [references/patterns.md](references/patterns.md).

## Antipatrones
- Compilar el grafo por request; `InMemorySaver` en producción.
- Estado con objetos no serializables o datos de contexto (user_id) que deberían ir en `context`.
- Campos escritos en paralelo sin reducer; mutar listas del estado.
- `interrupt()` dentro de `try/except Exception`; efectos no idempotentes antes del interrupt.
- Bucles sin límite; agentes multi-agente donde un flujo determinista bastaba.
- Usar `thread_id` recibido del cliente sin verificar propiedad.

## Checklist final
- [ ] Diagrama del grafo (Mermaid) y responsabilidad de cada nodo documentados.
- [ ] Estado tipado; reducers en campos compartidos; contexto separado.
- [ ] Routing tipado; límites de recursión/iteraciones.
- [ ] Checkpointer duradero en producción, creado una vez; `thread_id` validado.
- [ ] HITL con interrupt/Command idempotente y probado.
- [ ] Streaming `version="v2"` hacia SSE; desconexión manejada.
- [ ] Tracing LangSmith con `run_name`, `tags`, `metadata`.
- [ ] Tests de nodos y del grafo con modelo fake + `InMemorySaver` (`backend:backend-testing`).
