---
name: Prompt Engineering for Agents
description: Use when writing or optimizing prompts for TheSearch MCP tools, system prompts for extraction/classification/summarization, tool descriptions, few-shot patterns, context engineering for the agent loop, or prompt testing workflows.
---

# Prompt Engineering for Agents

## Quando Usar

- Ao escrever ou otimizar prompts para tools MCP do TheSearch
- Ao criar system prompts para extração, classificação, sumarização
- Ao projetar tool descriptions que previnam uso incorreto
- Ao implementar few-shot patterns para output consistente
- Ao fazer context engineering para o agent loop (PRÉ/DURANTE/PÓS)
- Ao testar e iterar prompts sistematicamente

## Conceito Fundamental

**Prompt Engineering para Agents != Prompt Engineering para Chat.** Agents operam em loops autônomos onde cada prompt é uma instrução que afeta comportamento downstream. Um prompt mal escrito não gera apenas uma resposta ruim — gera cascata de erros em tool calls, extração incorreta, e memória corrompida.

**Context Engineering** > Prompt Engineering: o foco não é apenas o texto do prompt, mas o design, teste, e iteração de toda informação contextual que o agente recebe — system layer, task layer, tool layer, memory layer.

## Arquitetura de Contexto em Camadas

```
┌─────────────────────────────────────┐
│  System Layer   → Identidade, regras │
│  Task Layer     → Instrução atual     │
│  Tool Layer     → Descrições de tools │
│  Memory Layer   → Contexto recuperado │
└─────────────────────────────────────┘
```

Cada camada deve ser projetada independentemente e testada em composição.

## 1. System Prompts para Extração/Classificação

```python
def extraction_system_prompt(project: str, category: str | None = None) -> str:
    return f"""Você é um extrator de conhecimento durável para o projeto "{project}".

<role>
Analista de conhecimento especializado em identificar informação durável.
</role>

<task>
Extraia APENAS conhecimento que vale a pena reter a longo prazo.
</task>

<categories>
- BusinessRule: Regras de negócio, constraints, validações
- DesignPattern: Padrões arquiteturais, idioms, soluções recorrentes
- DesignRule: Convenções de código, style guides, naming conventions
- ArchitecturalDecision: Decisões de design com racional e trade-offs
</categories>

<rules>
1. Cada candidato PRECISA de pelo menos 1 evidência do texto original
2. Title em inglês técnico descritivo (ex: "Use UUID v7 for Primary Keys")
3. proposed_weight: 0.8+ para ArchitecturalDecision, 0.6+ para BusinessRule, 0.5+ para DesignPattern
4. Se não houver conhecimento durável, retorne lista vazia — NÃO force extração
5. Prefira 2-3 candidatos de alta qualidade a 10 de baixa
</rules>

<output_format>
Retorne JSON com schema: {{"candidates": [...]}}
</output_format>"""
```

**Padrões-chave:**
- XML tags (`<role>`, `<rules>`, `<categories>`) para parsing unambiguous
- Regras numeradas e prescritivas (não sugestivas)
- Explicitar o comportamento negativo ("NÃO force extração")
- Incluir formato de output no próprio prompt

## 2. Tool Descriptions que Prevêem Uso Incorreto

```python
from mcp.server.fastmcp import tool

@tool(
    name="memory_query",
    description="""Busca memórias por similaridade semântica.

USE PARA: encontrar conhecimento relevante sobre um tópico.
NÃO USE PARA: listar todas as memórias (use memory_list), 
    contar memórias (use memory_stats), ou buscar por ID exato (use memory_get).

Args:
    query_text: Pergunta ou termo de busca (mín 3 palavras para melhor resultado)
    project: Nome do projeto (obrigatório, define escopo de isolamento)
    category: Filtrar por categoria (BusinessRule, DesignPattern, etc.)
    top_k: Número de resultados (default 5, max 20)

Returns: Lista de memórias ordenadas por relevância com score de similaridade."""
)
async def memory_query(query_text: str, project: str, category: str | None = None, top_k: int = 5):
    ...
```

**Anti-patterns em tool descriptions:**
- Descrições vagas ("search memories") — agente não sabe quando usar vs outro tool
- Não documentar args obrigatórios — agente omite parâmetros críticos
- Não documentar limites — agente faz requests inválidos

## 3. Few-Shot Patterns para Output Consistente

```python
FEW_SHOT_EXTRACTION = """
<example>
<input>
Adotamos UUID v7 como padrão para primary keys em todas as novas tabelas.
A decisão foi motivada pela necessidade de ordering temporal + uniqueness.
Trade-off: storage 2x maior vs integer, mas compatível com distributed systems.
</input>
<output>
{"candidates": [{"title": "Use UUID v7 for Primary Keys", "content": "All new tables must use UUID v7 as primary key type for temporal ordering and distributed uniqueness", "category": "ArchitecturalDecision", "evidence": ["Adotamos UUID v7 como padrão para primary keys", "ordering temporal + uniqueness", "compatível com distributed systems"], "proposed_weight": 0.85}]}
</output>
</example>

<example>
<input>
Bug fix: corrigi o typo no label do botão de login.
</input>
<output>
{"candidates": []}
</output>
</example>
"""
```

**Regras:**
- 2-3 examples: 1 caso ideal + 1 caso de rejeição (output vazio)
- Examples devem refletir casos reais do domínio
- Marcar com `<example>` tags para parsing claro

## 4. Context Engineering para o Agent Loop

```python
async def build_pre_task_context(project: str) -> str:
    rules = await search("design rules", project, category="DesignRule", top_k=3)
    decisions = await search("architectural decisions", project, category="ArchitecturalDecision", top_k=3)
    
    return f"""<memory_context>
<active_rules>
{format_memories(rules)}
</active_rules>
<active_decisions>
{format_memories(decisions)}
</active_decisions>
</memory_context>

<instruction>
Antes de implementar, verifique se sua solução está alinhada com as regras e decisões acima.
Se conflitar, priorize as decisões arquiteturais memorizadas.
</instruction>"""
```

**Context dinâmico:**
- PRÉ-TAREFA: carregar regras + decisões relevantes
- DURANTE: consultar sob demanda com query contextual
- PÓS-TAREFA: prompt de extração com regras de qualidade

## 5. Prompt Testing e Otimização

### Workflow de Teste

```python
async def test_prompt_quality(prompt_fn, test_cases: list[dict]) -> dict:
    results = []
    for case in test_cases:
        prompt = prompt_fn(case["input"])
        output = await llm_call(prompt, case["input"])
        results.append({
            "input": case["input"][:100],
            "expected_type": case.get("expected_empty", False),
            "got_empty": len(output.candidates) == 0,
            "candidate_count": len(output.candidates),
            "avg_weight": sum(c.proposed_weight for c in output.candidates) / max(len(output.candidates), 1),
        })
    return results
```

### Test Cases Obrigatórios

| Tipo | Input | Expected |
|------|-------|----------|
| Conhecimento claro | Decisão arquitetural explícita | 1+ candidato com weight > 0.7 |
| Ruído | Bug fix trivial, typo | Lista vazia |
| Fronteira | Discução de abordagem sem decisão | 0-1 candidatos |
| Múltiplos | Texto com 3+ tópicos distintos | Categorização correta |

### DSPy: Otimização sem Prompt Engineering Manual

DSPy permite otimizar prompts automaticamente via bootstrapped examples:

```python
import dspy

class ExtractMemories(dspy.Signature):
    """Extract durable knowledge candidates from text."""
    text: str = dspy.InputField(desc="Raw text to analyze")
    project: str = dspy.InputField(desc="Project scope")
    candidates_json: str = dspy.OutputField(desc="JSON array of memory candidates")

optimizer = dspy.MIPROv2(metric=extraction_quality_metric, num_threads=4)
optimized = optimizer.compile(ExtractMemories, trainset=train_examples)
```

**Quando usar DSPy:** Quando o prompt manual não atinge qualidade desejada após 3+ iterações de teste.

### Meta-Prompting

Usar LLM para gerar/otimizar prompts:

```python
META_PROMPT = """Given this prompt and its failure cases, suggest improvements.

Current prompt:
{current_prompt}

Failure cases:
{failures}

Improve the prompt to address these specific failures. Output ONLY the improved prompt."""
```

## 6. Error Handling em Prompts

```python
def build_prompt_with_error_handling(task_prompt: str) -> str:
    return f"""{task_prompt}

<error_handling>
Se o texto de entrada estiver vazio ou ilegível, retorne {{"candidates": [], "error": "empty_input"}}.
Se não for possível categorizar com confiança, use category "Uncategorized" com proposed_weight 0.3.
Se o texto for muito longo (>4000 tokens), processe apenas a primeira parte e adicione "truncated": true.
NUNCA invente evidência que não está no texto original.
</error_handling>

<verification>
Antes de responder, verifique:
1. Cada candidato tem pelo menos 1 evidência extraída do texto?
2. Os proposed_weights estão dentro dos ranges definidos?
3. Nenhum candidato duplica conteúdo de outro?
</verification>"""
```

## Erros Comuns

| Erro | Correção |
|------|----------|
| Prompt vago ("extract relevant info") | Ser prescritivo: categorias, weights, regras |
| Não incluir exemplos de rejeição | Adicionar `<example>` com output vazio |
| Tool description genérica | Documentar quando USAR e quando NÃO USAR |
| Não testar prompt sistematicamente | Criar test suite com casos claros/fronteira/ruído |
| Ignorar verification loop | Adicionar seção de self-check no prompt |
| Prompt monolítico | Separar em camadas (system/task/tool/memory) |
| Não versionar prompts | Git-track de todos os prompts com test results |

## Referências

- **knogdement/05_skills_token_optimization.md** — Token optimization, prompt compression, context engineering
- **OpenAI Prompt Engineering Guide** — message roles, formatting strategies
- **Anthropic Prompting Best Practices** — XML structuring, thinking patterns
- **Context Engineering (DAIR.AI)** — layered context architecture for agents
- **DSPy** — systematic prompt optimization without manual engineering
- **Anthropic Interactive Prompting Tutorial** — examples and exercises
