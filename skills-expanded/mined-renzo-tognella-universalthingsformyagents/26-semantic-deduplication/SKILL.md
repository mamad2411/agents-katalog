---
name: Semantic Deduplication
description: Use when implementing duplicate detection, tuning similarity thresholds, building multi-level dedup pipelines, or resolving conflicts between similar memories in TheSearch admission and consolidation stages.
---

# Semantic Deduplication

## Overview

Deduplicação no TheSearch vai além de "strings iguais". Memórias podem ser duplicatas conceituais mesmo com texto diferente ("usamos Repository Pattern" vs "Repository Pattern é o padrão de acesso a dados"). O pipeline atual usa 5 gates com similaridade vetorial — esta skill expande com técnicas complementares para cada nível de granularidade.

**Princípio:** Deduplicação é uma pipeline em níveis — do mais barato (exact match) ao mais sofisticado (conceitual). Não pule níveis.

## Quando Usar

- Ao implementar ou ajustar o Gate C de deduplicação
- Ao escolher entre Jaro-Winkler, MinHash, ou vector similarity
- Ao definir estratégias de merge/refine/deprecate para duplicatas
- Ao construir pipelines de dedup escaláveis (>10K memórias)
- Na consolidação diferida (background merge de duplicatas)

## Quando NÃO Usar

- Se a collection tem <1000 memórias — vector search simples basta
- Para memórias em projetos diferentes — duplicatas cross-project são aceitáveis

## Pipeline Multi-Nível

```
Input → Level 0: Exact Match ──── HIT → Update existente
            │
            ├─ Level 1: Jaro-Winkler ──── HIT (≥0.95) → Update existente
            │
            ├─ Level 2: Vector Similarity ── HIT (≥0.92) → Merge
            │
            ├─ Level 3: Semantic Refinement ─ HIT (≥0.80) → Refine (REFINES link)
            │
            └─ Level 4: Conceptual ──────── HIT → Verificar contexto
                                                    │
                                                    ├─ Mesmo contexto → Merge
                                                    └─ Contexto diferente → Manter ambos
```

Cada nível custa mais mas detecta duplicatas mais sutis.

## Nível 0: Exact Match (O(1))

```python
import hashlib

def content_hash(title: str, summary: str) -> str:
    normalized = f"{title.strip().lower()}|{summary.strip().lower()}"
    return hashlib.sha256(normalized.encode()).hexdigest()

def exact_dedup(candidate: MemoryCandidate, existing: dict[str, str]) -> str | None:
    h = content_hash(candidate.title, candidate.summary)
    return existing.get(h)
```

**Custo:** Zero compute. Sempre fazer primeiro.

## Nível 1: Jaro-Winkler (Fast Pre-filter)

Jaro-Winkler é otimizado para strings curtas (nomes, títulos). Dá preferência a matches no início — ideal para títulos de memórias que frequentemente compartilham prefixo.

```python
from jellyfish import jaro_winkler_similarity

def jw_dedup(
    candidate_title: str,
    existing_titles: list[str],
    threshold: float = 0.92
) -> list[tuple[str, float]]:
    matches = []
    c_lower = candidate_title.strip().lower()
    for title in existing_titles:
        score = jaro_winkler_similarity(c_lower, title.strip().lower())
        if score >= threshold:
            matches.append((title, score))
    return sorted(matches, key=lambda x: x[1], reverse=True)
```

**Por que Jaro-Winkler (não Levenshtein):**
- O(N×M) vs O(N) para comparação com muitos candidatos
- Bônus para prefixo comum — "Repository Pattern" vs "Repository Pattern for Data Access" score alto
- Threshold recomendado TheSearch: **0.92** para título, **0.90** para summary curto

**Integração com pipeline:**

```python
async def gate_c_with_jw(candidate: MemoryCandidate) -> DedupResult:
    existing_titles = await neo4j.get_titles(project=candidate.project)
    jw_matches = jw_dedup(candidate.title, existing_titles, threshold=0.92)

    if jw_matches:
        best_match = jw_matches[0]
        existing = await neo4j.get_by_title(best_match[0], candidate.project)
        return DedupResult(action="update", target=existing.id, score=best_match[1])

    embedding = await embed(f"{candidate.title} | {candidate.summary}")
    return await vector_dedup(embedding, candidate.project)
```

## Nível 2: Vector Similarity (Atual)

Esta é a abordagem existente no Gate C. Apenas thresholds empíricos:

| Score | Ação | Justificativa |
|:-----:|------|---------------|
| ≥ 0.95 | Merge forçado | Quase certamente duplicata |
| 0.92-0.95 | Update (merge inteligente) | Duplicata com variação |
| 0.85-0.92 | Refine (REFINES link) | Relacionado mas complementar |
| 0.80-0.85 | Investigar contexto | Pode ser perspectiva diferente |
| < 0.80 | Novo item | Sem relação significativa |

**O que funciona empiricamente:**
- Threshold 0.92: ~5% falso negativo (deixa passar duplicatas sutis), ~1% falso positivo
- Threshold 0.85: ~2% falso negativo, ~8% falso positivo
- **Recomendação:** Manter 0.92 para MVP, baixar para 0.88 com Jaro-Winkler como pre-filter

## Nível 3: MinHash + LSH para Escala

Para >10K memórias, comparar com todas é O(N). MinHash + LSH reduz para O(1) lookup.

```python
from datasketch import MinHash, MinHashLSH

def build_minhash(text: str, num_perm: int = 128) -> MinHash:
    mh = MinHash(num_perm=num_perm)
    for token in text.lower().split():
        mh.update(token.encode())
    return mh

class DedupIndex:
    def __init__(self, threshold: float = 0.8, num_perm: int = 128):
        self.lsh = MinHashLSH(threshold=threshold, num_perm=num_perm)
        self.minhashes: dict[str, MinHash] = {}

    def add(self, memory_id: str, text: str):
        mh = build_minhash(text, self.lsh.num_perm)
        self.lsh.insert(memory_id, mh)
        self.minhashes[memory_id] = mh

    def query(self, text: str) -> list[str]:
        mh = build_minhash(text, self.lsh.num_perm)
        return self.lsh.query(mh)

    def remove(self, memory_id: str):
        if memory_id in self.minhashes:
            self.lsh.remove(memory_id)
            del self.minhashes[memory_id]
```

**Integração com consolidação em background:**

```python
async def background_dedup_scan(project: str):
    all_memories = await neo4j.get_all_memories(project)
    index = DedupIndex(threshold=0.7)

    for mem in all_memories:
        text = f"{mem.title} {mem.summary}"
        candidates = index.query(text)

        if candidates:
            for candidate_id in candidates:
                score = await vector_similarity(mem, candidate_id)
                if score >= 0.85:
                    await schedule_merge(mem.id, candidate_id, score)

        index.add(mem.id, text)
```

**Quando MinHash+LSH vale a pena:**
- >10K memórias no mesmo projeto
- Consolidação em background (não latência-sensitivo)
- Detecção de near-duplicates em batch

## Nível 4: Quando Duplicatas São OK

Nem toda similaridade é duplicata. Duas perspectivas sobre o mesmo conceito são valiosas:

```python
@dataclass
class ConflictResolution:
    action: Literal["merge", "keep_both", "refine", "deprecate"]
    reason: str

def resolve_conflict(
    existing: MemoryItem,
    candidate: MemoryItem,
    similarity: float
) -> ConflictResolution:
    same_context = (
        existing.project == candidate.project
        and existing.category == candidate.category
    )

    if similarity >= 0.95 and same_context:
        return ConflictResolution("merge", "Near-identical in same context")

    if similarity >= 0.85 and not same_context:
        return ConflictResolution("keep_both", "Same concept, different context")

    if similarity >= 0.80:
        return ConflictResolution(
            "refine",
            f"Related: {candidate.title} adds to {existing.title}"
        )

    if existing.effective_weight < 0.3 and candidate.effective_weight >= 0.5:
        return ConflictResolution("deprecate", "New item supersedes weak existing")

    return ConflictResolution("keep_both", "Distinct enough")
```

**Sinais de que duplicatas devem coexistir:**
- Projetos diferentes (context isolation)
- Categorias diferentes (insight vs design rule vs ADR)
- Evidência conflitante (duas abordagens válidas para o mesmo problema)
- Temporal evolution ("usamos X" → "migramos de X para Y" — REFINES temporal)

## Estratégias de Merge

```python
async def merge_memories(
    target: MemoryItem,
    source: MemoryItem,
    strategy: str = "enrich"
) -> MemoryItem:
    if strategy == "enrich":
        target.summary = longer_of(target.summary, source.summary)
        target.evidence = list(set(target.evidence + source.evidence))
        target.weight_confidence = min(
            target.weight_confidence + 0.1, 1.0
        )
    elif strategy == "latest_wins":
        if source.created_at > target.created_at:
            target.summary = source.summary
            target.title = source.title
    elif strategy == "union":
        target.summary = f"{target.summary} | {source.summary}"

    await neo4j.mark_deprecated(source.id, deprecated_by=target.id)
    return target
```

## Thresholds Recomendados por Técnica

| Técnica | Threshold | Falso Positivo | Falso Negativo | Custo |
|---------|:---------:|:--------------:|:--------------:|:-----:|
| Exact hash | 1.0 | 0% | Alto (não detecta parciais) | Zero |
| Jaro-Winkler | 0.92 | ~3% | ~5% | O(N) CPU |
| Vector cosine | 0.92 | ~1% | ~5% | O(N) com Qdrant |
| Vector cosine | 0.85 | ~8% | ~2% | O(N) com Qdrant |
| MinHash LSH | 0.70 | ~15% | ~2% | O(1) lookup |

**Configuração recomendada TheSearch:**

```python
DEDUP_THRESHOLDS = {
    "exact": 1.0,
    "jaro_winkler_title": 0.92,
    "jaro_winkler_summary": 0.90,
    "vector_high": 0.95,
    "vector_duplicate": 0.92,
    "vector_refine": 0.80,
    "minhash_lsh_candidate": 0.70,
}
```

## Regras

- Nunca pular níveis — exact match é gratuito, sempre testar primeiro
- Jaro-Winkler antes de vector search para títulos (evita chamada ao Qdrant)
- MinHash+LSH é para background consolidation, não para admissão em tempo real
- Merge sempre enriquece (nunca perde evidência)
- Duplicatas cross-project são aceitáveis — não merge
- Thresholds devem ser calibrados com dados reais do projeto

## Common Mistakes

1. **Usar só vector similarity** — Jaro-Winkler detecta "Repository Pattern" vs "Repository pattern" que vector pode não pegar com score alto.
2. **Merge agressivo** — duas perspectivas sobre o mesmo conceito são valiosas. Só merge se a informação é genuinamente redundante.
3. **MinHash em tempo real** — LSH é probabilístico, usar só para batch/background.
4. **Ignorar contexto** — mesma memória em projetos diferentes NÃO é duplicata.
5. **Threshold único** — títulos precisam de threshold diferente de summaries. Configurar por campo.

## Referências

- `knogdement/10_thesearch_related.md` — seção Deduplication & Similarity (Jaro-Winkler, MinHash, LSH)
- `knogdement/01_graphs_llm_memory.md` — Mem0 conflict detection, hippocampal memory indexing
- Jaro-Winkler: https://en.wikipedia.org/wiki/Jaro%E2%80%93Winkler_distance
- MinHash: https://en.wikipedia.org/wiki/MinHash
- LSH: https://en.wikipedia.org/wiki/Locality-sensitive_hashing
- Qdrant filter cardinality: https://qdrant.tech/documentation/search/search/
- Hippocampus memory module: https://arxiv.org/abs/2602.13594
