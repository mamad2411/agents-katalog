---
name: rag-review
description: MUST USE for RAG pipelines — chunking, embeddings, retrieval, reranking, grounded answers, citation honesty, eval. Triggers on hallucinated docs, wrong retrieval, or new vector search feature.
---

# RAG Review

RAG connects **retrieval quality** to **generation honesty**. Audit ingest → index → query → prompt assembly → answer with metrics at each stage — bad chunks can't be prompt-engineered away.

## When This Skill Applies

- New doc corpus Q&A
- Answers cite wrong doc or hallucinate citations
- pgvector/Pinecone/Weaviate integration
- Hybrid search (BM25 + vectors)
- Enterprise PDF/HTML ingestion

## Severity Model

| Level | Signal | Gate |
|-------|--------|------|
| **R0** | Answers without retrieval on compliance topics; PII in index | Block |
| **R1** | No citation requirement; k too large; chunk splits mid-sentence tables | Fix |
| **R2** | No rerank; stale index | Sprint |
| **R3** | Embedding model undocumented | Doc |

Cross-ref: `context-engineering` for window; `eval-harness` for retrieval+gen; `prompt-engineering` for grounding instructions.

## Phase 0 — Pipeline Map

```
Source → extract → clean → chunk → embed → store
Query → embed → retrieve k → rerank → assemble context → LLM → answer + cites
```

Measure latency and token cost per stage.

## Phase 1 — Ingest & Chunking

- [ ] Extract text preserves headings/tables (not naive strip HTML)
- [ ] Chunk size 300–800 tokens with 10–20% overlap — tune per corpus
- [ ] Metadata: `source_id`, `title`, `section`, `updated_at`
- [ ] PII scrub before embed (`data-quality` rules)
- [ ] Version index on doc update — delete stale vectors

```python
# Anti-pattern: fixed char split mid-word
# Prefer structure-aware: markdown headers, page boundaries
```

## Phase 2 — Embeddings & Index (2025–2026)

- Pin embedding model version — re-embed on change
- Normalize vectors if metric requires
- HNSW params: ef_search trade recall/latency
- Hybrid: BM25 for exact SKU/legal terms + vector for paraphrase
- **Rerank** cross-encoder top 20 → final 5 — large quality lift

```bash
# pgvector sanity
psql -c "SELECT id, embedding <=> query_vec AS dist FROM docs ORDER BY dist LIMIT 5;"
```

Cross-ref: `supabase-postgres`, `postgresql` template.

## Phase 3 — Query-Time

- [ ] Query rewrite optional (HyDE) — eval before prod
- [ ] Filter metadata (tenant, product) **before** vector search
- [ ] Empty retrieval → explicit "no docs" path — no inventing
- [ ] Max context from RAG bounded (`context-engineering`)

## Phase 4 — Generation & Citations

Prompt rules:

- Answer only from provided context blocks
- Cite `[doc_id:section]` per claim
- Say insufficient context when true

Eval:

- `answer_correct` + `citation_supported` grader
- Adversarial: question not in corpus → must abstain

Cross-ref: `prompt-engineering`, `eval-harness`.

## Phase 5 — Metrics

| Metric | Target |
|--------|--------|
| Retrieval recall@k | on labeled set |
| MRR nDCG | search quality |
| Faithfulness | judge or human |
| Abstain accuracy | on OOD questions |

Log retrieval ids in production for debugging wrong answers.

## Phase 6 — Anti-Injection

- Treat retrieved text as untrusted — delimiter blocks
- Strip instruction-like lines from docs if attacker-controlled
- Cross-ref: `threat-model`, `secure-coding`

## Output Template

```markdown
## RAG Review: [corpus/app]

**Verdict:** ✅ / 🔶 / ❌

### Pipeline
- Embed model:
- k / rerank:

### Findings
| ID | Sev | Stage | Issue | Fix |

### Eval
| Metric | Value |

### Sample failures
1. Query → wrong chunk because ...

### Follow-ups
- [ ] re-chunk
- [ ] hybrid search
```

## Anti-Patterns

- **Huge k** "for recall" — drowns context
- **No metadata filters** in multi-tenant
- **Same embed model** for code and legal without testing
- **Citation string fabricated** — verify post-gen
- **Skip re-index** on doc delete

## Cross-References

| Skill | Use when |
|-------|----------|
| `sql-write` | SQL hybrid queries |
| `pipeline-review` | ingest jobs |
| `agent-design` | agent with search tool |

## Cursor Kit Templates

- `postgresql` pgvector, `ai-agents`

## Extended Reference — Operational Drill

Run this drill when the skill triggers in production (not only doc review):

1. **Capture evidence first** — commands, screenshots, log lines with timestamps; do not change prod before snapshot.
2. **Classify severity** using this skill's table; if between two levels, choose the higher until disproved.
3. **Apply the smallest fix** that addresses root cause; avoid drive-by refactors in the same change.
4. **Verify with the same command** that failed before; add automated guard (CI rule, test, alert).
5. **Record in output template** and link follow-up skills from Cross-References.

## Extended Reference — Runnable Sanity Pack

```bash
# Repository context (adapt paths)
git status -sb
git log -3 --oneline
# Replace SVC with your service name
test -f docker-compose.yml && docker compose ps
test -f package.json && npm run -s test 2>&1 | tail -5
```

## Extended Reference — Stakeholder Comms

| Severity | Who to inform | Channel | SLA |
|----------|---------------|---------|-----|
| Blocker | On-call / founder | incident chat | <15m |
| High | Team lead | ticket comment | same day |
| Medium | PR reviewer | PR description | this sprint |
| Low | backlog | deferred list | next review |

## Extended Reference — Definition of Done

- [ ] Output template filled completely
- [ ] Severity assigned per finding with fix snippet
- [ ] Cross-skill follow-ups checked or N/A with reason
- [ ] No secrets pasted into notes or tickets
- [ ] Re-run key verification command after fix

## Extended Reference — 2025–2026 Practice Notes

- Prefer **automation in CI** over manual checklist repetition for this domain.
- Pair **metrics/alerts** with any production change recommended here (`observability` where applicable).
- Document **rollback** in the same PR/issue as the forward fix.
- Keep playbooks **versioned in git** — when process changes, update this SKILL in the same PR.

## Extended Reference — Common Questions

**Q: How long should this review take?**  
A: Time-box discovery (15–30m), then fix loop. If stuck without new evidence, switch to `diagnose-bugs` or `research`.

**Q: Can we waive a blocker?**  
A: Only with written accept + expiry date + compensating control; never silent waive.

**Q: What if tools are missing locally?**  
A: Run what you can; document gaps in "Commands run" with install note — do not skip severity classification.

## Extended Reference — Finding ID Convention

Use stable IDs in reports: `[SKILL]-001`, increment per session. Refer to IDs in PR comments for traceability.

## Extended Reference — Pair Review

For S0/A0/T0 class issues, second person validates reproduction steps before merge when team size allows.

