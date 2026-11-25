---
name: llm-evaluation
description: "Domine estratégias abrangentes de avaliação para aplicações LLM, desde métricas automatizadas até avaliação humana e testes A/B."
risk: unknown
source: community
date_added: "2026-02-27"
---

# Avaliação de LLM

Domine estratégias abrangentes de avaliação para aplicações LLM, desde métricas automatizadas até avaliação humana e testes A/B.

## Não use essa habilidade quando

- A tarefa não está relacionada a avaliação de LLM
- Você precisa de um domínio diferente ou ferramenta fora do escopo

## Instruções

- Esclareça objetivos, restrições e inputs necessários.
- Aplique as melhores práticas relevantes e valide resultados.
- Forneça passos acionáveis e verificação.
- Se exemplos detalhados forem necessários, abra `resources/implementation-playbook.md`.

## Use essa habilidade quando

- Medindo desempenho de aplicação LLM sistematicamente
- Comparando diferentes modelos ou prompts
- Detectando regressões de desempenho antes do deploy
- Validando melhorias a partir de mudanças de prompt
- Construindo confiança em sistemas de produção
- Estabelecendo linhas de base e rastreando progresso ao longo do tempo
- Depurando comportamento inesperado do modelo

## Tipos de Avaliação Principais

### 1. Métricas Automatizadas
Avaliação rápida, repetível e escalável usando pontuações computadas.

**Geração de Texto:**
- **BLEU**: Sobreposição de n-gramas (tradução)
- **ROUGE**: Orientada a recall (sumarização)
- **METEOR**: Similaridade semântica
- **BERTScore**: Similaridade baseada em embedding
- **Perplexity**: Confiança do modelo de linguagem

**Classificação:**
- **Accuracy**: Percentual de acertos
- **Precision/Recall/F1**: Desempenho específico da classe
- **Confusion Matrix**: Padrões de erro
- **AUC-ROC**: Qualidade de ranking

**Retrieval (RAG):**
- **MRR**: Mean Reciprocal Rank
- **NDCG**: Normalized Discounted Cumulative Gain
- **Precision@K**: Relevantes nos top K
- **Recall@K**: Cobertura nos top K

### 2. Avaliação Humana
Avaliação manual para aspectos de qualidade difíceis de automatizar.

**Dimensões:**
- **Accuracy**: Correção factual
- **Coherence**: Fluxo lógico
- **Relevance**: Responde a pergunta
- **Fluency**: Qualidade de linguagem natural
- **Safety**: Sem conteúdo prejudicial
- **Helpfulness**: Útil ao usuário

### 3. LLM-as-Judge
Use LLMs mais fortes para avaliar saídas de modelos mais fracos.

**Abordagens:**
- **Pointwise**: Pontuar respostas individuais
- **Pairwise**: Comparar duas respostas
- **Reference-based**: Comparar com padrão ouro
- **Reference-free**: Julgar sem ground truth

## Início Rápido

```python
from llm_eval import EvaluationSuite, Metric

# Define evaluation suite
suite = EvaluationSuite([
    Metric.accuracy(),
    Metric.bleu(),
    Metric.bertscore(),
    Metric.custom(name="groundedness", fn=check_groundedness)
])

# Prepare test cases
test_cases = [
    {
        "input": "What is the capital of France?",
        "expected": "Paris",
        "context": "France is a country in Europe. Paris is its capital."
    },
    # ... more test cases
]

# Run evaluation
results = suite.evaluate(
    model=your_model,
    test_cases=test_cases
)

print(f"Overall Accuracy: {results.metrics['accuracy']}")
print(f"BLEU Score: {results.metrics['bleu']}")
```

## Implementação de Métricas Automatizadas

### Pontuação BLEU
```python
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

def calculate_bleu(reference, hypothesis):
    """Calculate BLEU score between reference and hypothesis."""
    smoothie = SmoothingFunction().method4

    return sentence_bleu(
        [reference.split()],
        hypothesis.split(),
        smoothing_function=smoothie
    )

# Usage
bleu = calculate_bleu(
    reference="The cat sat on the mat",
    hypothesis="A cat is sitting on the mat"
)
```

### Pontuação ROUGE
```python
from rouge_score import rouge_scorer

def calculate_rouge(reference, hypothesis):
    """Calculate ROUGE scores."""
    scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True)
    scores = scorer.score(reference, hypothesis)

    return {
        'rouge1': scores['rouge1'].fmeasure,
        'rouge2': scores['rouge2'].fmeasure,
        'rougeL': scores['rougeL'].fmeasure
    }
```

### BERTScore
```python
from bert_score import score

def calculate_bertscore(references, hypotheses):
    """Calculate BERTScore using pre-trained BERT."""
    P, R, F1 = score(
        hypotheses,
        references,
        lang='en',
        model_type='microsoft/deberta-xlarge-mnli'
    )

    return {
        'precision': P.mean().item(),
        'recall': R.mean().item(),
        'f1': F1.mean().item()
    }
```

### Métricas Personalizadas
```python
def calculate_groundedness(response, context):
    """Check if response is grounded in provided context."""
    # Use NLI model to check entailment
    from transformers import pipeline

    nli = pipeline("text-classification", model="microsoft/deberta-large-mnli")

    result = nli(f"{context} [SEP] {response}")[0]

    # Return confidence that response is entailed by context
    return result['score'] if result['label'] == 'ENTAILMENT' else 0.0

def calculate_toxicity(text):
    """Measure toxicity in generated text."""
    from detoxify import Detoxify

    results = Detoxify('original').predict(text)
    return max(results.values())  # Return highest toxicity score

def calculate_factuality(claim, knowledge_base):
    """Verify factual claims against knowledge base."""
    # Implementation depends on your knowledge base
    # Could use retrieval + NLI, or fact-checking API
    pass
```

## Padrões de LLM-as-Judge

### Avaliação de Saída Única
```python
def llm_judge_quality(response, question):
    """Use GPT-5 to judge response quality."""
    prompt = f"""Rate the following response on a scale of 1-10 for:
1. Accuracy (factually correct)
2. Helpfulness (answers the question)
3. Clarity (well-written and understandable)

Question: {question}
Response: {response}

Provide ratings in JSON format:
{{
  "accuracy": <1-10>,
  "helpfulness": <1-10>,
  "clarity": <1-10>,
  "reasoning": "<brief explanation>"
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

### Comparação Pairwise
```python
def compare_responses(question, response_a, response_b):
    """Compare two responses using LLM judge."""
    prompt = f"""Compare these two responses to the question and determine which is better.

Question: {question}

Response A: {response_a}

Response B: {response_b}

Which response is better and why? Consider accuracy, helpfulness, and clarity.

Answer with JSON:
{{
  "winner": "A" or "B" or "tie",
  "reasoning": "<explanation>",
  "confidence": <1-10>
}}
"""

    result = openai.ChatCompletion.create(
        model="gpt-5",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(result.choices[0].message.content)
```

## Frameworks de Avaliação Humana

### Diretrizes de Anotação
```python
class AnnotationTask:
    """Structure for human annotation task."""

    def __init__(self, response, question, context=None):
        self.response = response
        self.question = question
        self.context = context

    def get_annotation_form(self):
        return {
            "question": self.question,
            "context": self.context,
            "response": self.response,
            "ratings": {
                "accuracy": {
                    "scale": "1-5",
                    "description": "Is the response factually correct?"
                },
                "relevance": {
                    "scale": "1-5",
                    "description": "Does it answer the question?"
                },
                "coherence": {
                    "scale": "1-5",
                    "description": "Is it logically consistent?"
                }
            },
            "issues": {
                "factual_error": False,
                "hallucination": False,
                "off_topic": False,
                "unsafe_content": False
            },
            "feedback": ""
        }
```

### Concordância Entre Anotadores
```python
from sklearn.metrics import cohen_kappa_score

def calculate_agreement(rater1_scores, rater2_scores):
    """Calculate inter-rater agreement."""
    kappa = cohen_kappa_score(rater1_scores, rater2_scores)

    interpretation = {
        kappa < 0: "Poor",
        kappa < 0.2: "Slight",
        kappa < 0.4: "Fair",
        kappa < 0.6: "Moderate",
        kappa < 0.8: "Substantial",
        kappa <= 1.0: "Almost Perfect"
    }

    return {
        "kappa": kappa,
        "interpretation": interpretation[True]
    }
```

## Testes A/B

### Framework de Testes Estatísticos
```python
from scipy import stats
import numpy as np

class ABTest:
    def __init__(self, variant_a_name="A", variant_b_name="B"):
        self.variant_a = {"name": variant_a_name, "scores": []}
        self.variant_b = {"name": variant_b_name, "scores": []}

    def add_result(self, variant, score):
        """Add evaluation result for a variant."""
        if variant == "A":
            self.variant_a["scores"].append(score)
        else:
            self.variant_b["scores"].append(score)

    def analyze(self, alpha=0.05):
        """Perform statistical analysis."""
        a_scores = self.variant_a["scores"]
        b_scores = self.variant_b["scores"]

        # T-test
        t_stat, p_value = stats.ttest_ind(a_scores, b_scores)

        # Effect size (Cohen's d)
        pooled_std = np.sqrt((np.std(a_scores)**2 + np.std(b_scores)**2) / 2)
        cohens_d = (np.mean(b_scores) - np.mean(a_scores)) / pooled_std

        return {
            "variant_a_mean": np.mean(a_scores),
            "variant_b_mean": np.mean(b_scores),
            "difference": np.mean(b_scores) - np.mean(a_scores),
            "relative_improvement": (np.mean(b_scores) - np.mean(a_scores)) / np.mean(a_scores),
            "p_value": p_value,
            "statistically_significant": p_value < alpha,
            "cohens_d": cohens_d,
            "effect_size": self.interpret_cohens_d(cohens_d),
            "winner": "B" if np.mean(b_scores) > np.mean(a_scores) else "A"
        }

    @staticmethod
    def interpret_cohens_d(d):
        """Interpret Cohen's d effect size."""
        abs_d = abs(d)
        if abs_d < 0.2:
            return "negligible"
        elif abs_d < 0.5:
            return "small"
        elif abs_d < 0.8:
            return "medium"
        else:
            return "large"
```

## Testes de Regressão

### Detecção de Regressão
```python
class RegressionDetector:
    def __init__(self, baseline_results, threshold=0.05):
        self.baseline = baseline_results
        self.threshold = threshold

    def check_for_regression(self, new_results):
        """Detect if new results show regression."""
        regressions = []

        for metric in self.baseline.keys():
            baseline_score = self.baseline[metric]
            new_score = new_results.get(metric)

            if new_score is None:
                continue

            # Calculate relative change
            relative_change = (new_score - baseline_score) / baseline_score

            # Flag if significant decrease
            if relative_change < -self.threshold:
                regressions.append({
                    "metric": metric,
                    "baseline": baseline_score,
                    "current": new_score,
                    "change": relative_change
                })

        return {
            "has_regression": len(regressions) > 0,
            "regressions": regressions
        }
```

## Benchmarking

### Executando Benchmarks
```python
class BenchmarkRunner:
    def __init__(self, benchmark_dataset):
        self.dataset = benchmark_dataset

    def run_benchmark(self, model, metrics):
        """Run model on benchmark and calculate metrics."""
        results = {metric.name: [] for metric in metrics}

        for example in self.dataset:
            # Generate prediction
            prediction = model.predict(example["input"])

            # Calculate each metric
            for metric in metrics:
                score = metric.calculate(
                    prediction=prediction,
                    reference=example["reference"],
                    context=example.get("context")
                )
                results[metric.name].append(score)

        # Aggregate results
        return {
            metric: {
                "mean": np.mean(scores),
                "std": np.std(scores),
                "min": min(scores),
                "max": max(scores)
            }
            for metric, scores in results.items()
        }
```

## Recursos

- **references/metrics.md**: Guia métrica abrangente
- **references/human-evaluation.md**: Melhores práticas de anotação
- **references/benchmarking.md**: Benchmarks padrão
- **references/a-b-testing.md**: Guia de testes estatísticos
- **references/regression-testing.md**: Integração com CI/CD
- **assets/evaluation-framework.py**: Harness de avaliação completo
- **assets/benchmark-dataset.jsonl**: Datasets de exemplo
- **scripts/evaluate-model.py**: Runner de avaliação automatizada

## Melhores Práticas

1. **Múltiplas Métricas**: Use métricas diversas para visão abrangente
2. **Dados Representativos**: Teste em exemplos reais e diversos
3. **Linhas de Base**: Sempre compare contra desempenho de baseline
4. **Rigor Estatístico**: Use testes estatísticos apropriados para comparações
5. **Avaliação Contínua**: Integre ao pipeline de CI/CD
6. **Validação Humana**: Combine métricas automatizadas com julgamento humano
7. **Análise de Erros**: Investigue falhas para entender fraquezas
8. **Controle de Versão**: Rastreie resultados de avaliação ao longo do tempo

## Armadilhas Comuns

- **Obsessão com Métrica Única**: Otimizar uma métrica à custa de outras
- **Tamanho de Amostra Pequeno**: Tirar conclusões de poucos exemplos
- **Contaminação de Dados**: Testar em dados de treinamento
- **Ignorar Variância**: Não considerar incerteza estatística
- **Desalinhamento de Métrica**: Usar métricas não alinhadas com objetivos de negócio