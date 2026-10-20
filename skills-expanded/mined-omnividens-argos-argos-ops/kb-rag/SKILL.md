---
name: kb-rag
description: Recherche similarité dans la Knowledge Base Argos via fastembed local + pgvector cosine. Utilise ce skill quand le user demande de répondre à une question produit, de drafter un email avec contexte KB, ou de débugger pourquoi une réponse RAG escalade. Réutilisé par /run-support-tier1, /check-emails, et futurs ContentBot P9 / OutboundBot P13.
---

# kb-rag

Skill technique pour la recherche RAG (Retrieval-Augmented Generation) sur
la KB Argos. Encapsule embed + cosine top-K + filtrage seuil + formatage
prompt anti-hallucination.

> **Stack figée par D-017** : `fastembed` + `paraphrase-multilingual-mpnet-base-v2`
> 768 dims, 100 % local. Aucun appel API LLM tiers. Premier run télécharge
> ~1 GB de poids ONNX dans le cache utilisateur, ensuite tout offline.

## API Python

```python
from argos_ops.crm.db import session_scope
from argos_ops.rag.search import search_kb, build_support_prompt

async with session_scope() as session:
    result = await search_kb(
        session,
        query="combien coûte Pro Max ?",
        top_k=5,
        distance_threshold=0.85,  # default
    )

# result.hits : list[RAGHit] (doc_path, chunk_index, content, distance)
# result.is_empty : True si aucun hit < seuil → escalade Tier 2
# result.top_distance : float | None — distance du meilleur hit

prompt = build_support_prompt(result)  # prêt à coller dans un appel Claude
```

## Pipeline RAG

```
Query texte
   ↓ embed_query() — fastembed local, 768 dims
Vector 768 dims
   ↓ pgvector <=> cosine distance, top_k=5
[(KBChunk, distance)] × 5
   ↓ filter distance ≤ 0.85
[(KBChunk, distance)] × M (0 ≤ M ≤ 5)
   ↓ format_context_block() + build_support_prompt()
Prompt anti-hallucination prêt pour Claude
```

## Convention citation

Format imposé pour la traçabilité : ``[KB#N: doc.md§index]``

Exemple Claude doit produire :

> Pro Max coûte 249 €/mois [KB#1: pricing.md§3] et inclut tous les
> 139 modules [KB#2: argos_features.md§1].

L'agent-juge Tier 1 (P14) vérifiera que chaque claim factuel pointe vers
un extrait réellement fourni — anti-hallucination automatisé.

## Garde-fous (cohérent avec ARGOS_OPS_PLAN § 6.2)

Le prompt système (``build_support_prompt``) impose à Claude :

1. Réponds UNIQUEMENT à partir des extraits fournis
2. Cite tes sources avec `[KB#N: doc§index]`
3. Si la question n'est pas couverte → exactement `ESCALADE: <raison>`
4. Pas de placeholder hallucinant (« notre équipe va revenir », etc.)
5. Respecte le ton de marque (factuel, anti-FUD)

## Calibration du seuil de distance

Default : `0.85` (pgvector cosine ∈ [0, 2], 0 = identique, 1 = orthogonal).

Seuil trop bas → escalades excessives (faux négatifs). Trop haut →
hallucinations (chunks non pertinents acceptés). À calibrer en
observant ``scripts/eval_kb_rag.py`` :

- Si une question dans la KB escalade alors qu'elle a une bonne réponse
  → distance > 0.85, baisser le seuil
- Si une question hors KB répond avec confidence → distance < 0.85,
  augmenter le seuil

## Performance

- **Embed query** : ~50 ms en CPU moderne (premier appel paie ~3-5 s
  de chargement du modèle, puis singleton process-local)
- **pgvector cosine** : ~5-15 ms pour 100 chunks (sub-ms pour les hot path
  via index ivfflat à créer en P19 si volume > 1000 chunks)
- **Total RAG complet** : < 100 ms hors first-load

## Tests

Cf. ``tests/test_rag.py`` (12 tests unitaires) :

- ``test_embedding_model_is_768_dims_compatible`` — modèle figé D-017
- ``test_embed_query_rejects_empty_text`` — input validation
- ``test_rag_result_is_empty_when_no_hits`` — sémantique escalade
- ``test_format_context_block_includes_kb_citations`` — format ``[KB#N: ...]``
- ``test_support_prompt_contains_anti_hallucination_rules`` — règles strictes
- ``test_support_prompt_with_empty_hits_still_buildable`` — escalade propre

Cf. ``scripts/eval_kb_rag.py`` (10 questions golden) pour valider en
intégration : 5 questions dans la KB → réponse + citations, 5 hors KB
→ escalade.

## Limites connues

- **Pas de re-ranking** : on prend les top_k directs de pgvector. À
  améliorer en P14 (agent-juge) si besoin
- **Pas de cache** des embeddings de query : chaque ``embed_query`` paie
  les 50 ms. Pour des futurs canaux temps réel (à concevoir, hors P8 qui
  est annulée — D-019), un cache LRU sera utile
- **Modèle bloquant CPU** : pas de GPU. Acceptable pour le volume actuel
  (Sprint 1-2). À reconsidérer si > 100 queries/sec
