---
name: Agent Evaluation & Benchmarking
description: Use when measuring retrieval quality, memory accuracy, consolidation effectiveness, or end-to-end pipeline performance in TheSearch. Applies when designing benchmarks, running A/B tests, or building automated regression tests for memory systems.
---

# Agent Evaluation & Benchmarking

## Overview

Avaliação de sistemas de memória é fundamentalmente diferente de avaliar LLMs ou RAGs genéricos. TheSearch precisa medir: **retrieval quality** (achou o certo?), **memory accuracy** (o que armazenou está certo?), **consolidation effectiveness** (melhorou ao longo do tempo?) e **end-to-end utility** (o usuário final ficou satisfeito?).

**Princípio:** O que não é medido não pode ser melhorado. Métricas devem ser automatizáveis e rodar continuamente.

## Quando Usar

- Ao implementar qualquer mudança no pipeline de memória
- Ao comparar estratégias de retrieval, embeddings, ou consolidação
- Ao configurar CI/CD para TheSearch (regression tests)
- Ao calibrar thresholds (similaridade, peso mínimo, etc.)
- Ao medir impacto de mudanças antes de deploy (A/B testing)

## O Que Avaliar no TheSearch

```
Pipeline TheSearch:
  Input → Extraction → Admission → Storage → Retrieval → Response
         ↕            ↕            ↕          ↕
      Extração     Qualidade    Consolidação  Ranking
```

| Componente | Métrica Principal | Métrica Secundária |
|-----------|:-----------------:|:-----------------:|
| Extraction | Precision (extrações corretas) | Recall (nada ficou de fora?) |
| Admission | False positive rate | False negative rate |
| Storage | Write latency | Consistency (Neo4j ↔ Qdrant) |
| Retrieval | Recall@k, Precision@k | MRR, NDCG |
| Consolidation | Merge accuracy | Promotion correctness |
| End-to-end | Answer correctness | User satisfaction |

## Retrieval Evaluation

### Precision@k e Recall@k

As métricas mais fundamentais para retrieval:

```python
def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    hits = len(set(retrieved_k) & relevant)
    return hits / k

def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    retrieved_k = retrieved[:k]
    hits = len(set(retrieved_k) & relevant)
    return hits / len(relevant) if relevant else 0.0
```

### MRR (Mean Reciprocal Rank)

Posição do primeiro resultado relevante — ideal para "top-1 matters":

```python
def mrr(queries: list[list[str]], relevant_sets: list[set[str]]) -> float:
    total = 0.0
    for retrieved, relevant in zip(queries, relevant_sets):
        for i, doc_id in enumerate(retrieved, 1):
            if doc_id in relevant:
                total += 1.0 / i
                break
    return total / len(queries)
```

### NDCG (Normalized Discounted Cumulative Gain)

Leva em conta o ranking e relevância graded (não apenas binary):

```python
import math

def ndcg(retrieved: list[tuple[str, float]], k: int) -> float:
    dcg = sum(
        rel / math.log2(i + 2)
        for i, (_, rel) in enumerate(retrieved[:k])
    )
    ideal = sorted([r for _, r in retrieved], reverse=True)[:k]
    idcg = sum(
        rel / math.log2(i + 2)
        for i, rel in enumerate(ideal)
    )
    return dcg / idcg if idcg > 0 else 0.0
```

## Memory Quality Metrics

### Correção (Correctness)

A memória armazenada é factualmente correta?

```python
class MemoryCorrectnessEvaluator:
    async def evaluate(self, memory: MemoryItem, source: str) -> float:
        evaluation = await self.llm.judge(
            f"Rate 0-1 how factually correct this memory summary is "
            f"given the source content:\n"
            f"Memory: {memory.summary}\n"
            f"Source: {source}",
            response_model=CorrectnessScore,
        )
        return evaluation.score
```

### Completude (Completeness)

Nada importante ficou de fora?

```python
class CompletenessEvaluator:
    async def evaluate(self, memory: MemoryItem, source: str) -> float:
        evaluation = await self.llm.judge(
            f"List key information from the source that is MISSING "
            f"from the memory summary:\n"
            f"Memory: {memory.summary}\nSource: {source}",
            response_model=MissingInfo,
        )
        return 1.0 - (len(evaluation.missing_items) / max(evaluation.total_key_points, 1))
```

### Temporalidade (Timeliness)

A memória ainda está atualizada?

```python
class TimelinessEvaluator:
    async def evaluate(self, memory: MemoryItem) -> float:
        if memory.type == "architectural_decision":
            return 1.0  # ADRs não expiram
        age_days = (datetime.utcnow() - memory.created_at).days
        half_life = CATEGORY_HALF_LIVES.get(memory.type, 180)
        return math.exp(-0.693 * age_days / half_life)

CATEGORY_HALF_LIVES = {
    "fact": 180,
    "decision": 365,
    "preference": 90,
    "insight": 120,
    "pattern": 200,
}
```

## End-to-End Evaluation

### Pipeline Score: Query → Retrieve → Synthesize → Score

```python
class EndToEndEvaluator:
    async def evaluate_single(self, test_case: E2ETestCase) -> E2EOutput:
        retrieved = await self.retriever.retrieve(
            test_case.query, test_case.project
        )
        
        response = await self.llm.synthesize(
            test_case.query, context=[r.summary for r in retrieved]
        )
        
        faithfulness = await self.measure_faithfulness(response, retrieved)
        relevance = await self.measure_relevance(response, test_case.query)
        correctness = await self.measure_correctness(response, test_case.expected_answer)
        
        return E2EOutput(
            query=test_case.query,
            response=response,
            retrieved_ids=[r.memory_id for r in retrieved],
            faithfulness=faithfulness,
            relevance=relevance,
            correctness=correctness,
            composite=0.3 * faithfulness + 0.3 * relevance + 0.4 * correctness,
        )
```

### Test Dataset Format

```python
@dataclass
class E2ETestCase:
    query: str
    project: str
    expected_answer: str
    expected_relevant_ids: list[str]
    difficulty: str  # "easy", "medium", "hard"
    category: str    # "factual", "reasoning", "temporal"

@dataclass
class E2ETestSuite:
    name: str
    cases: list[E2ETestCase]
    
    @staticmethod
    def from_jsonl(path: str) -> "E2ETestSuite":
        cases = []
        with open(path) as f:
            for line in f:
                data = json.loads(line)
                cases.append(E2ETestCase(**data))
        return E2ETestSuite(name=path, cases=cases)
```

## Custom Benchmarks para Personal Memory

### Benchmark Generation

Para sistemas de memória pessoal, golden sets devem ser gerados a partir de dados reais:

```python
async def generate_benchmark_from_history(
    interaction_log: list[Interaction], sample_size: int = 100
) -> list[E2ETestCase]:
    test_cases = []
    sampled = random.sample(interaction_log, min(sample_size, len(interaction_log)))
    
    for interaction in sampled:
        relevant_memories = await identify_relevant_memories(interaction)
        test_case = await llm.generate_test_case(
            interaction=interaction,
            relevant_context=relevant_memories,
            response_model=E2ETestCase,
        )
        test_cases.append(test_case)
    
    return test_cases
```

### LoCoMo Benchmark Adaptado

LoCoMo (Long-Term Conversational Memory) é o benchmark mais relevante para TheSearch. Adaptar:

```python
LOCOMO_ADAPTED_METRICS = {
    "session_recall": "Can the system recall facts from previous sessions?",
    "cross_session_reasoning": "Can the system connect information across sessions?",
    "temporal_awareness": "Does the system know when memories were created?",
    "preference_tracking": "Does the system track evolving user preferences?",
    "contradiction_handling": "Does the system handle updated information?",
}
```

## A/B Testing Patterns

### Estrutura de A/B Test para Memory System

```python
@dataclass
class ABTest:
    name: str
    control: PipelineConfig
    treatment: PipelineConfig
    traffic_split: float  # 0.0-1.0 for treatment
    metrics: list[str]
    min_samples: int = 100
    confidence_level: float = 0.95

async def run_ab_test(test: ABTest):
    results_control = []
    results_treatment = []
    
    for query in test_queries:
        if random.random() < test.traffic_split:
            result = await run_pipeline(test.treatment, query)
            results_treatment.append(result)
        else:
            result = await run_pipeline(test.control, query)
            results_control.append(result)
    
    return statistical_comparison(
        results_control, results_treatment,
        metrics=test.metrics,
        confidence=test.confidence_level,
    )
```

### O Que A/B Testar

| Variável | O Que Variar | Métrica Principal |
|----------|-------------|:-----------------:|
| Embedding model | Model A vs Model B | Recall@10 |
| Similarity threshold | 0.85 vs 0.90 vs 0.92 | Merge accuracy |
| Weight formula | Formula v1 vs v2 | Promotion correctness |
| Retrieval strategy | Vector-only vs Hybrid | NDCG@10 |
| Consolidation freq | 4h vs 6h vs 12h | Stale ratio |

## Automated Regression Testing

### Test Suite para CI/CD

```python
class MemoryRegressionSuite:
    def __init__(self):
        self.test_cases = load_golden_set("tests/golden/memory_v1.jsonl")
    
    async def run_all(self) -> RegressionReport:
        results = []
        for case in self.test_cases:
            result = await self.run_single(case)
            results.append(result)
            
            if result.regression_detected:
                await self.alert(
                    f"REGRESSION: {case.name} — "
                    f"{result.metric} dropped from {result.baseline} to {result.current}"
                )
        
        return RegressionReport(
            total=len(results),
            passed=sum(1 for r in results if not r.regression_detected),
            regressions=[r for r in results if r.regression_detected],
        )
    
    async def run_single(self, case: RegressionTestCase) -> RegressionResult:
        current = await self.measure(case.metric, case.input)
        baseline = case.baseline_value
        tolerance = case.tolerance or 0.05
        
        regression = current < (baseline * (1 - tolerance))
        return RegressionResult(
            name=case.name,
            metric=case.metric,
            baseline=baseline,
            current=current,
            regression_detected=regression,
        )
```

### Golden Set Management

```python
@dataclass
class GoldenTestCase:
    id: str
    input: dict
    expected_output: dict
    metric_thresholds: dict[str, float]
    last_validated: datetime
    version: str

class GoldenSetManager:
    async def validate_golden_set(self) -> ValidationReport:
        outdated = [
            case for case in self.cases
            if (datetime.utcnow() - case.last_validated).days > 30
        ]
        
        invalid = []
        for case in self.cases:
            result = await self.run_case(case)
            if not self.meets_thresholds(result, case.metric_thresholds):
                invalid.append(case)
        
        return ValidationReport(
            total=len(self.cases),
            outdated=len(outdated),
            invalid=invalid,
        )
```

## Evaluation Frameworks de Referência

| Framework | O Que Mede | Aplicável ao TheSearch |
|-----------|-----------|:---------------------:|
| **RAGAS** | Faithfulness, relevance, context precision/recall | Retrieval + synthesis |
| **ARES** | Automated evaluation via predicted rewards | Lightweight continuous eval |
| **RAGChecker** | Claim-level evaluation metrics | Fine-grained accuracy |
| **TruLens** | RAG triad (groundedness, relevance, coherence) | Quick quality checks |
| **CRAG benchmark** | 8 domains, dynamic questions | Standardized comparison |
| **LoCoMo** | Long-term conversational memory | Direct applicability |
| **AgentBench** | Comprehensive agent tasks | Agent behavior evaluation |

## Common Mistakes

| Erro | Consequência | Correção |
|------|-------------|----------|
| Avaliar só retrieval | Pipeline otimizado localmente, resultado final pior | End-to-end evaluation sempre |
| Golden set estático | Degrada com mudanças do sistema | Re-validar golden set periodicamente |
| Sem baseline | Não sabe se mudou para melhor ou pior | Sempre comparar contra baseline |
| Métricas isoladas | Otimizar precision mata recall | Otimizar métricas compostas |
| Overfitting no benchmark | Sistema bom no teste, ruim na prática | Rotacionar test cases, holdout set |
| Ignorar latência | Pipeline perfeito mas inutilizável | Incluir latency budgets |
| Sem statistical significance | Conclusões erradas de A/B tests | min_samples + confidence level |
| Não avaliar temporalidade | Memórias velhas são retornadas como atuais | Timeliness metric por categoria |

## Referências

- **RAGAS:** Es et al., "RAGAS: Automated Evaluation of RAG Systems" (2023) — knogdement/04
- **ARES:** Saad-Falcon et al., "Automated RAG Evaluation System" (2023) — knogdement/04
- **RAGChecker:** Ru et al., "Advanced RAG Evaluation Framework" (2024) — knogdement/04
- **TruLens:** TruLens RAG Triad — knogdement/04
- **CRAG:** "Comprehensive RAG Benchmark" (Meta, 2024) — knogdement/04
- **LoCoMo:** "Long-Term Conversational Memory Benchmark" (2024) — knogdement/02
- **AgentBench:** "Comprehensive LLM Agent Benchmark" — knogdement/08
- **Evaluation Repositories:** explodinggradients/ragas, microsoft/promptflow — knogdement/08
