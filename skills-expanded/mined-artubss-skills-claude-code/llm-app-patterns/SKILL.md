---
name: llm-app-patterns
description: "Padrões prontos para produção ao construir aplicações com LLM. Cobre pipelines RAG, arquiteturas de agentes, IDEs de prompt e monitoramento LLMOps. Use ao projetar aplicações com IA, implementar RAG, construir agentes ou configurar observabilidade de LLM."
---

# 🤖 Padrões de Aplicação LLM

> Padrões prontos para produção ao construir aplicações com LLM, inspirados por [Dify](https://github.com/langgenius/dify) e melhores práticas da indústria.

## Quando Usar Esta Skill

Use esta skill quando:

- Projetar aplicações alimentadas por LLM
- Implementar RAG (Retrieval-Augmented Generation)
- Construir agentes de IA com ferramentas
- Configurar monitoramento LLMOps
- Escolher entre arquiteturas de agentes

---

## 1. Arquitetura de Pipeline RAG

### Visão Geral

RAG (Retrieval-Augmented Generation) fundamenta respostas de LLM em seus dados.

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Ingest    │────▶│   Retrieve  │────▶│   Generate  │
│  Documents  │     │   Context   │     │   Response  │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                   │
      ▼                   ▼                   ▼
 ┌─────────┐       ┌───────────┐       ┌───────────┐
 │ Chunking│       │  Vector   │       │    LLM    │
 │Embedding│       │  Search   │       │  + Context│
 └─────────┘       └───────────┘       └───────────┘
```

### 1.1 Ingestão de Documentos

```python
# Estratégias de chunking
class ChunkingStrategy:
    # Chunks de tamanho fixo (simples mas pode quebrar contexto)
    FIXED_SIZE = "fixed_size"  # ex: 512 tokens

    # Chunking semântico (preserva significado)
    SEMANTIC = "semantic"      # Divide em parágrafos/seções

    # Divisão recursiva (tenta múltiplos separadores)
    RECURSIVE = "recursive"    # ["\n\n", "\n", " ", ""]

    # Consciente de documento (respeita estrutura)
    DOCUMENT_AWARE = "document_aware"  # Cabeçalhos, listas, etc.

# Configurações recomendadas
CHUNK_CONFIG = {
    "chunk_size": 512,       # tokens
    "chunk_overlap": 50,     # sobreposição de tokens entre chunks
    "separators": ["\n\n", "\n", ". ", " "],
}
```

### 1.2 Embedding e Armazenamento

```python
# Seleção de banco de dados vetorial
VECTOR_DB_OPTIONS = {
    "pinecone": {
        "use_case": "Produção, serviço gerenciado",
        "scale": "Bilhões de vetores",
        "features": ["Busca híbrida", "Filtragem de metadados"]
    },
    "weaviate": {
        "use_case": "Auto-hospedado, multi-modal",
        "scale": "Milhões de vetores",
        "features": ["API GraphQL", "Módulos"]
    },
    "chromadb": {
        "use_case": "Desenvolvimento, prototipagem",
        "scale": "Milhares de vetores",
        "features": ["API simples", "Opção em memória"]
    },
    "pgvector": {
        "use_case": "Infraestrutura Postgres existente",
        "scale": "Milhões de vetores",
        "features": ["Integração SQL", "Conformidade ACID"]
    }
}

# Seleção de modelo de embedding
EMBEDDING_MODELS = {
    "openai/text-embedding-3-small": {
        "dimensions": 1536,
        "cost": "$0.02/1M tokens",
        "quality": "Bom para a maioria dos casos de uso"
    },
    "openai/text-embedding-3-large": {
        "dimensions": 3072,
        "cost": "$0.13/1M tokens",
        "quality": "Melhor para queries complexas"
    },
    "local/bge-large": {
        "dimensions": 1024,
        "cost": "Gratuito (apenas computação)",
        "quality": "Comparável ao OpenAI small"
    }
}
```

### 1.3 Estratégias de Recuperação

```python
# Busca semântica básica
def semantic_search(query: str, top_k: int = 5):
    query_embedding = embed(query)
    results = vector_db.similarity_search(
        query_embedding,
        top_k=top_k
    )
    return results

# Busca híbrida (semântica + palavra-chave)
def hybrid_search(query: str, top_k: int = 5, alpha: float = 0.5):
    """
    alpha=1.0: Semântica pura
    alpha=0.0: Palavra-chave pura (BM25)
    alpha=0.5: Balanceada
    """
    semantic_results = vector_db.similarity_search(query)
    keyword_results = bm25_search(query)

    # Reciprocal Rank Fusion
    return rrf_merge(semantic_results, keyword_results, alpha)

# Recuperação multi-query
def multi_query_retrieval(query: str):
    """Gera variações de query múltiplas para melhor recall"""
    queries = llm.generate_query_variations(query, n=3)
    all_results = []
    for q in queries:
        all_results.extend(semantic_search(q))
    return deduplicate(all_results)

# Compressão contextual
def compressed_retrieval(query: str):
    """Recupera e depois comprime apenas as partes relevantes"""
    docs = semantic_search(query, top_k=10)
    compressed = llm.extract_relevant_parts(docs, query)
    return compressed
```

### 1.4 Geração com Contexto

```python
RAG_PROMPT_TEMPLATE = """
Responda a pergunta do usuário baseado APENAS no contexto a seguir.
Se o contexto não contiver informação suficiente, diga "Não tenho informação suficiente para responder isso."

Contexto:
{context}

Pergunta: {question}

Resposta:"""

def generate_with_rag(question: str):
    # Recuperar
    context_docs = hybrid_search(question, top_k=5)
    context = "\n\n".join([doc.content for doc in context_docs])

    # Gerar
    prompt = RAG_PROMPT_TEMPLATE.format(
        context=context,
        question=question
    )

    response = llm.generate(prompt)

    # Retornar com citações
    return {
        "answer": response,
        "sources": [doc.metadata for doc in context_docs]
    }
```

---

## 2. Arquiteturas de Agentes

### 2.1 Padrão ReAct (Raciocínio + Ação)

```
Pensamento: Preciso procurar por informação sobre X
Ação: search("X")
Observação: [resultados da busca]
Pensamento: Com base nos resultados, devo...
Ação: calculate(...)
Observação: [resultado do cálculo]
Pensamento: Agora tenho informação suficiente
Ação: final_answer("A resposta é...")
```

```python
REACT_PROMPT = """
Você é um assistente de IA que pode usar ferramentas para responder perguntas.

Ferramentas disponíveis:
{tools_description}

Use este formato:
Pensamento: [seu raciocínio sobre o que fazer em seguida]
Ação: [tool_name(argumentos)]
Observação: [resultado da ferramenta - será preenchido]
... (repita Pensamento/Ação/Observação conforme necessário)
Pensamento: Tenho informação suficiente para responder
Resposta Final: [sua resposta final]

Pergunta: {question}
"""

class ReActAgent:
    def __init__(self, tools: list, llm):
        self.tools = {t.name: t for t in tools}
        self.llm = llm
        self.max_iterations = 10

    def run(self, question: str) -> str:
        prompt = REACT_PROMPT.format(
            tools_description=self._format_tools(),
            question=question
        )

        for _ in range(self.max_iterations):
            response = self.llm.generate(prompt)

            if "Resposta Final:" in response:
                return self._extract_final_answer(response)

            action = self._parse_action(response)
            observation = self._execute_tool(action)
            prompt += f"\nObservação: {observation}\n"

        return "Máximo de iterações atingido"
```

### 2.2 Padrão Function Calling

```python
# Defina ferramentas como funções com schemas
TOOLS = [
    {
        "name": "search_web",
        "description": "Busca na web por informação atual",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Query de busca"
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "calculate",
        "description": "Realiza cálculos matemáticos",
        "parameters": {
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Expressão matemática a avaliar"
                }
            },
            "required": ["expression"]
        }
    }
]

class FunctionCallingAgent:
    def run(self, question: str) -> str:
        messages = [{"role": "user", "content": question}]

        while True:
            response = self.llm.chat(
                messages=messages,
                tools=TOOLS,
                tool_choice="auto"
            )

            if response.tool_calls:
                for tool_call in response.tool_calls:
                    result = self._execute_tool(
                        tool_call.name,
                        tool_call.arguments
                    )
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": str(result)
                    })
            else:
                return response.content
```

### 2.3 Padrão Plan-and-Execute

```python
class PlanAndExecuteAgent:
    """
    1. Criar um plano (lista de passos)
    2. Executar cada passo
    3. Replanejamento se necessário
    """

    def run(self, task: str) -> str:
        # Fase de planejamento
        plan = self.planner.create_plan(task)
        # Retorna: ["Passo 1: ...", "Passo 2: ...", ...]

        results = []
        for step in plan:
            # Executar cada passo
            result = self.executor.execute(step, context=results)
            results.append(result)

            # Verificar se replanejamento é necessário
            if self._needs_replan(task, results):
                new_plan = self.planner.replan(
                    task,
                    completed=results,
                    remaining=plan[len(results):]
                )
                plan = new_plan

        # Sintetizar resposta final
        return self.synthesizer.summarize(task, results)
```

### 2.4 Colaboração Multi-Agente

```python
class AgentTeam:
    """
    Agentes especializados colaborando em tarefas complexas
    """

    def __init__(self):
        self.agents = {
            "researcher": ResearchAgent(),
            "analyst": AnalystAgent(),
            "writer": WriterAgent(),
            "critic": CriticAgent()
        }
        self.coordinator = CoordinatorAgent()

    def solve(self, task: str) -> str:
        # Coordenador atribui subtarefas
        assignments = self.coordinator.decompose(task)

        results = {}
        for assignment in assignments:
            agent = self.agents[assignment.agent]
            result = agent.execute(
                assignment.subtask,
                context=results
            )
            results[assignment.id] = result

        # Crítico revisa
        critique = self.agents["critic"].review(results)

        if critique.needs_revision:
            # Iterar com feedback
            return self.solve_with_feedback(task, results, critique)

        return self.coordinator.synthesize(results)
```

---

## 3. Padrões de Prompt IDE

### 3.1 Templates de Prompt com Variáveis

```python
class PromptTemplate:
    def __init__(self, template: str, variables: list[str]):
        self.template = template
        self.variables = variables

    def format(self, **kwargs) -> str:
        # Validar todas as variáveis fornecidas
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Variáveis ausentes: {missing}")

        return self.template.format(**kwargs)

    def with_examples(self, examples: list[dict]) -> str:
        """Adicionar exemplos few-shot"""
        example_text = "\n\n".join([
            f"Entrada: {ex['input']}\nSaída: {ex['output']}"
            for ex in examples
        ])
        return f"{example_text}\n\n{self.template}"

# Uso
summarizer = PromptTemplate(
    template="Resuma o seguinte texto em estilo {style}:\n\n{text}",
    variables=["style", "text"]
)

prompt = summarizer.format(
    style="profissional",
    text="Conteúdo de artigo longo..."
)
```

### 3.2 Versionamento de Prompt e Testes A/B

```python
class PromptRegistry:
    def __init__(self, db):
        self.db = db

    def register(self, name: str, template: str, version: str):
        """Armazenar prompt com versão"""
        self.db.save({
            "name": name,
            "template": template,
            "version": version,
            "created_at": datetime.now(),
            "metrics": {}
        })

    def get(self, name: str, version: str = "latest") -> str:
        """Recuperar versão específica"""
        return self.db.get(name, version)

    def ab_test(self, name: str, user_id: str) -> str:
        """Retornar variante baseada em bucket do usuário"""
        variants = self.db.get_all_versions(name)
        bucket = hash(user_id) % len(variants)
        return variants[bucket]

    def record_outcome(self, prompt_id: str, outcome: dict):
        """Rastrear desempenho do prompt"""
        self.db.update_metrics(prompt_id, outcome)
```

### 3.3 Prompt Chaining

```python
class PromptChain:
    """
    Encadeia prompts, passando saída como entrada para o próximo
    """

    def __init__(self, steps: list[dict]):
        self.steps = steps

    def run(self, initial_input: str) -> dict:
        context = {"input": initial_input}
        results = []

        for step in self.steps:
            prompt = step["prompt"].format(**context)
            output = llm.generate(prompt)

            # Analisar saída se necessário
            if step.get("parser"):
                output = step["parser"](output)

            context[step["output_key"]] = output
            results.append({
                "step": step["name"],
                "output": output
            })

        return {
            "final_output": context[self.steps[-1]["output_key"]],
            "intermediate_results": results
        }

# Exemplo: Pesquisar → Analisar → Resumir
chain = PromptChain([
    {
        "name": "research",
        "prompt": "Pesquise sobre o tópico: {input}",
        "output_key": "research"
    },
    {
        "name": "analyze",
        "prompt": "Analise esses achados:\n{research}",
        "output_key": "analysis"
    },
    {
        "name": "summarize",
        "prompt": "Resuma essa análise em 3 pontos principais:\n{analysis}",
        "output_key": "summary"
    }
])
```

---

## 4. LLMOps e Observabilidade

### 4.1 Métricas para Rastrear

```python
LLM_METRICS = {
    # Performance
    "latency_p50": "Tempo de resposta percentil 50",
    "latency_p99": "Tempo de resposta percentil 99",
    "tokens_per_second": "Velocidade de geração",

    # Qualidade
    "user_satisfaction": "Taxa de polegar para cima/baixo",
    "task_completion": "% de tarefas completadas com sucesso",
    "hallucination_rate": "% de respostas com erros factuais",

    # Custo
    "cost_per_request": "Média R$ por chamada de API",
    "tokens_per_request": "Média de tokens usados",
    "cache_hit_rate": "% de requisições servidas do cache",

    # Confiabilidade
    "error_rate": "% de requisições falhadas",
    "timeout_rate": "% de requisições que expiraram",
    "retry_rate": "% de requisições precisando retry"
}
```

### 4.2 Logging e Rastreamento

```python
import logging
from opentelemetry import trace

tracer = trace.get_tracer(__name__)

class LLMLogger:
    def log_request(self, request_id: str, data: dict):
        """Log de requisição LLM para debug e análise"""
        log_entry = {
            "request_id": request_id,
            "timestamp": datetime.now().isoformat(),
            "model": data["model"],
            "prompt": data["prompt"][:500],  # Truncar para armazenamento
            "prompt_tokens": data["prompt_tokens"],
            "temperature": data.get("temperature", 1.0),
            "user_id": data.get("user_id"),
        }
        logging.info(f"LLM_REQUEST: {json.dumps(log_entry)}")

    def log_response(self, request_id: str, data: dict):
        """Log de resposta LLM"""
        log_entry = {
            "request_id": request_id,
            "completion_tokens": data["completion_tokens"],
            "total_tokens": data["total_tokens"],
            "latency_ms": data["latency_ms"],
            "finish_reason": data["finish_reason"],
            "cost_usd": self._calculate_cost(data),
        }
        logging.info(f"LLM_RESPONSE: {json.dumps(log_entry)}")

# Rastreamento distribuído
@tracer.start_as_current_span("llm_call")
def call_llm(prompt: str) -> str:
    span = trace.get_current_span()
    span.set_attribute("prompt.length", len(prompt))

    response = llm.generate(prompt)

    span.set_attribute("response.length", len(response))
    span.set_attribute("tokens.total", response.usage.total_tokens)

    return response.content
```

### 4.3 Framework de Avaliação

```python
class LLMEvaluator:
    """
    Avalia saídas de LLM para qualidade
    """

    def evaluate_response(self,
                          question: str,
                          response: str,
                          ground_truth: str = None) -> dict:
        scores = {}

        # Relevância: Ela responde à pergunta?
        scores["relevance"] = self._score_relevance(question, response)

        # Coerência: Está bem estruturada?
        scores["coherence"] = self._score_coherence(response)

        # Fundamentação: Está baseada em contexto fornecido?
        scores["groundedness"] = self._score_groundedness(response)

        # Precisão: Coincide com a verdade comprovada?
        if ground_truth:
            scores["accuracy"] = self._score_accuracy(response, ground_truth)

        # Segurança: Está segura?
        scores["safety"] = self._score_safety(response)

        return scores

    def run_benchmark(self, test_cases: list[dict]) -> dict:
        """Executar avaliação em conjunto de testes"""
        results = []
        for case in test_cases:
            response = llm.generate(case["prompt"])
            scores = self.evaluate_response(
                question=case["prompt"],
                response=response,
                ground_truth=case.get("expected")
            )
            results.append(scores)

        return self._aggregate_scores(results)
```

---

## 5. Padrões de Produção

### 5.1 Estratégia de Cache

```python
import hashlib
from functools import lru_cache

class LLMCache:
    def __init__(self, redis_client, ttl_seconds=3600):
        self.redis = redis_client
        self.ttl = ttl_seconds

    def _cache_key(self, prompt: str, model: str, **kwargs) -> str:
        """Gerar chave de cache determinística"""
        content = f"{model}:{prompt}:{json.dumps(kwargs, sort_keys=True)}"
        return hashlib.sha256(content.encode()).hexdigest()

    def get_or_generate(self, prompt: str, model: str, **kwargs) -> str:
        key = self._cache_key(prompt, model, **kwargs)

        # Verificar cache
        cached = self.redis.get(key)
        if cached:
            return cached.decode()

        # Gerar
        response = llm.generate(prompt, model=model, **kwargs)

        # Cache (apenas cache saídas determinísticas)
        if kwargs.get("temperature", 1.0) == 0:
            self.redis.setex(key, self.ttl, response)

        return response
```

### 5.2 Rate Limiting e Retry

```python
import time
from tenacity import retry, wait_exponential, stop_after_attempt

class RateLimiter:
    def __init__(self, requests_per_minute: int):
        self.rpm = requests_per_minute
        self.timestamps = []

    def acquire(self):
        """Aguardar se limite de taxa fosse excedido"""
        now = time.time()

        # Remover timestamps antigos
        self.timestamps = [t for t in self.timestamps if now - t < 60]

        if len(self.timestamps) >= self.rpm:
            sleep_time = 60 - (now - self.timestamps[0])
            time.sleep(sleep_time)

        self.timestamps.append(time.time())

# Retry com backoff exponencial
@retry(
    wait=wait_exponential(multiplier=1, min=4, max=60),
    stop=stop_after_attempt(5)
)
def call_llm_with_retry(prompt: str) -> str:
    try:
        return llm.generate(prompt)
    except RateLimitError:
        raise  # Acionará retry
    except APIError as e:
        if e.status_code >= 500:
            raise  # Retry erros de servidor
        raise  # Não retry erros de cliente
```

### 5.3 Estratégia de Fallback

```python
class LLMWithFallback:
    def __init__(self, primary: str, fallbacks: list[str]):
        self.primary = primary
        self.fallbacks = fallbacks

    def generate(self, prompt: str, **kwargs) -> str:
        models = [self.primary] + self.fallbacks

        for model in models:
            try:
                return llm.generate(prompt, model=model, **kwargs)
            except (RateLimitError, APIError) as e:
                logging.warning(f"Modelo {model} falhou: {e}")
                continue

        raise AllModelsFailedError("Todos os modelos esgotados")

# Uso
llm_client = LLMWithFallback(
    primary="gpt-4-turbo",
    fallbacks=["gpt-3.5-turbo", "claude-3-sonnet"]
)
```

---

## Matriz de Decisão Arquitetônica

| Padrão              | Use Quando       | Complexidade | Custo     |
| :------------------ | :--------------- | :----------- | :-------- |
| **RAG Simples**     | FAQ, busca docs  | Baixa        | Baixo     |
| **RAG Híbrido**     | Queries mistas   | Média        | Médio     |
| **Agente ReAct**    | Tarefas multi-etapa | Média     | Médio     |
| **Function Calling**| Ferramentas estruturadas | Baixa | Baixo     |
| **Plan-Execute**    | Tarefas complexas | Alta        | Alta      |
| **Multi-Agente**    | Tarefas de pesquisa | Muito Alta | Muito Alta |

---

## Recursos

- [Plataforma Dify](https://github.com/langgenius/dify)
- [Docs LangChain](https://python.langchain.com/)
- [LlamaIndex](https://www.llamaindex.ai/)
- [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)