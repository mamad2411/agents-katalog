---
name: search-recommend
category: business
description: 사용자 노출용 검색 + 추천 — Elasticsearch/OpenSearch/Algolia/Typesense Provider, 한국어 형태소 분석(nori), Saga 기반 인덱스 sync, BM25+벡터 하이브리드, 협업 필터링/content-based 추천. ai/vector-db(RAG/임베딩)와 별개. SearchGateway 추상화.
license: MIT
---

# Search & Recommend — 사용자 노출용 검색 + 추천

신규 SaaS에서 **사용자가 직접 사용하는 검색 + 추천**을 0에서 만들지 않도록 검증된 패턴 모음. RAG/임베딩 검색은 [`ai/vector-db.md`](../vector-db/SKILL.md) + [`ai/rag-patterns.md`](../rag-patterns/SKILL.md) 분담.

> 핵심 결정: (1) 검색 엔진 (관리형 vs self-host), (2) 한국어 토크나이저 (nori vs mecab), (3) DB↔Index 일관성 (Saga vs CDC), (4) 추천 알고리즘 (CF vs content vs hybrid).

## When to Use

- 신규 SaaS에 사용자용 검색 기능 추가 (상품/문서/콘텐츠)
- "추천" 기능 (관련 상품, 다음 시청, 사용자별 피드)
- 자동 완성 (typeahead/instant search)
- 한국어 검색 (형태소 분석, 동의어, 자모 분리)
- 멀티 필드 검색 (title boost, category filter, geo radius)
- 인덱스 일관성 문제 (DB는 update됐는데 search는 stale)
- 외부 SaaS vs self-host 결정
- 검색 분석 (no-result 쿼리, click-through rate)
- B2B 검색 (tenant-scoped, 권한 필터)

**관련 skill (cross-link)**:
- `ai/vector-db.md` — 벡터 DB / ANN / RAG 임베딩 검색 (이 skill과 별개)
- `ai/rag-patterns.md` — LLM context retrieval (사용자 검색과 다름)
- `observability/logging-elk.md` — Elasticsearch 운영 공통점 (클러스터, alias, reindex)
- `messaging/kafka-connect-cdc.md` — DB → Search 인덱스 sync
- `business/multi-tenancy.md` — tenant-scoped 검색
- `business/media-handling.md` — 이미지/비디오 메타데이터 검색
- `business/feature-flags.md` — 검색 알고리즘 A/B 실험
- `business/audit-log.md` — 검색 쿼리 로그 (PII 주의)

---

## 검색 엔진 선택 결정 트리

```
검색 엔진?
    │
    ├─ 관리형 SaaS, 빠른 시작 ────> Algolia / Typesense Cloud
    │   - Algolia: 글로벌 표준, $1/1K search 단위, 한국어 OK
    │   - Typesense Cloud: 가성비, search-only 단순 워크로드
    │
    ├─ 오픈소스 + 자체 운영 ──────> OpenSearch / Elasticsearch
    │   - OpenSearch: AWS 친화, 라이센스 free
    │   - Elasticsearch 8.x: ELK 통합, security 내장 (Apache 2.0 → SSPL → 다시 AGPL/Elastic 2.0 분기 주의)
    │
    ├─ 한국 클라우드 ─────────────> Naver Cloud Search Service / KT
    │   - 망내 latency 이점
    │   - PIPA 데이터 영토 요구 시
    │
    ├─ 가벼운 단일 노드 ──────────> Meilisearch / Typesense (self-host)
    │   - < 10M 문서, 단일 서버
    │
    └─ DB에 그대로 ───────────────> PostgreSQL FTS (tsvector) + pg_trgm
        - < 1M 문서, ops 단순화 우선
        - 한국어는 mecab-ko 또는 GIN+trigram 조합
```

| Provider | 월 비용 (1M docs) | 한국어 | tenant 격리 | Geo | Vector | 운영 부하 |
|---|---|---|---|---|---|---|
| **Algolia** | $500 | ✅ | API key per tenant | ✅ | $$$ | 무 (관리형) |
| **Typesense Cloud** | $80 | ✅ basic | scope keys | ✅ | ✅ | 낮음 |
| **OpenSearch (AWS managed)** | $250 | nori plugin | index per tenant | ✅ | ✅ k-NN | 중 |
| **Elasticsearch (self-host)** | $150 | nori | document/field-level | ✅ | ✅ | 높음 |
| **Naver Cloud Search** | ₩200K | ✅ Naver tokenizer | ✅ | ✅ | — | 무 |
| **Meilisearch** | $50 (self) | ✅ basic | API keys | — | ✅ | 낮음 |
| **PostgreSQL FTS** | (DB만) | mecab-ko | row-level | PostGIS | pgvector | DB와 동일 |

---

## SearchGateway 추상화 (Provider 교체 대비)

`SubscriptionGateway` / `CreditGateway` / `StorageGateway` 패턴 4번째 정착. 비즈니스 로직은 Gateway 인터페이스만 알아야 한다.

```
interface SearchGateway {
    index(tenantId, doc) -> Promise
    search(tenantId, query, opts) -> SearchResult
    delete(tenantId, docId)
    bulk(tenantId, docs[])
    autocomplete(tenantId, prefix) -> Suggestion[]
}

implementations:
    AlgoliaSearchGateway
    OpenSearchGateway
    TypesenseGateway
    PostgresFTSGateway  // 부트스트랩 단계
```

**부트스트랩 흐름**: PostgresFTSGateway로 시작 (≤100K docs) → 트래픽 증가 시 OpenSearch 또는 Algolia로 교체. Gateway 인터페이스는 동일.

---

## 한국어 형태소 분석

한국어는 교착어 + 조사/어미 변형이 많아 **형태소 분석 필수**. 영어 lowercase + stem만으로는 0% recall 가능.

| 분석기 | 라이센스 | 특징 |
|---|---|---|
| **nori** (Elasticsearch/OpenSearch 공식) | Apache 2.0 | mecab-ko-dic 기반, 가장 검증된 표준 |
| **mecab-ko** | GPL/LGPL | 사전 풍부, 한국어 NLP 표준, GPL 주의 |
| **arirang** | Apache 2.0 | 오래됨, 신규 권장 X |
| **OpenKoreanText** | Apache 2.0 | 트위터 출신, neologism 강점 |

### nori 설정 예시 (OpenSearch / Elasticsearch)

```json
{
  "settings": {
    "analysis": {
      "tokenizer": {
        "ko_tokenizer": {
          "type": "nori_tokenizer",
          "decompound_mode": "mixed"
        }
      },
      "filter": {
        "ko_synonym": {
          "type": "synonym_graph",
          "synonyms_path": "synonyms/ko.txt"
        },
        "ko_stop": {
          "type": "stop",
          "stopwords_path": "stopwords/ko.txt"
        }
      },
      "analyzer": {
        "korean": {
          "tokenizer": "ko_tokenizer",
          "filter": ["lowercase", "ko_synonym", "ko_stop", "nori_part_of_speech"]
        }
      }
    }
  }
}
```

### decompound_mode

| 모드 | 동작 | 예시 ("아이폰15프로") |
|---|---|---|
| `none` | 분해 안 함 | "아이폰15프로" |
| `discard` | 원형 버리고 분해만 | "아이폰", "15", "프로" |
| `mixed` | **둘 다 보존 (권장)** | "아이폰15프로", "아이폰", "15", "프로" |

→ recall ↑ precision ↓. mixed가 검색에 유리.

### 동의어 사전 운영

```
# synonyms/ko.txt
아이폰, 아이폰15, iphone15
노트북, 랩탑, laptop
서울, 서울시, seoul
```

- 사용자 검색 로그 분석 → no-result 쿼리 → 동의어 후보
- 분기마다 갱신 (한국 신조어 빠름)

---

## 인덱싱 패턴 (DB ↔ Search 일관성)

### 패턴 1: Synchronous (단순, ≤ 10K docs/day)

```
Application
   │
   ├─ DB write
   └─ Search index (sync)
```

**문제**: search 다운 시 DB write도 실패 (가용성 ↓). 양 시스템 트랜잭션 불가능. **부트스트랩 외 비권장**.

### 패턴 2: Outbox + Worker (권장)

```
Application → DB (transaction) ──> outbox table
                                       │
                            Worker (poll) ──> Search index
```

`subscription-billing-flows.md` Saga 패턴 재사용. outbox는 `business/audit-log.md`와도 짝.

```
1. App: DB.transaction:
       UPDATE products SET name=?, ...
       INSERT INTO outbox (event_type, payload, status='pending')
2. Worker: SELECT * FROM outbox WHERE status='pending' LIMIT 100
3. Worker: search.index(payload)
4. Worker: UPDATE outbox SET status='sent', sent_at=NOW()
5. 실패 시: retry_count++, status remains 'pending', max_retries 후 'failed'
```

**장점**: DB 트랜잭션 일관성, search 다운 영향 없음, replay 가능.

### 패턴 3: CDC (Kafka Connect / Debezium)

```
DB binlog ──> Debezium ──> Kafka ──> ES Sink Connector ──> Elasticsearch
```

`messaging/kafka-connect-cdc.md` 참조. 트래픽 큰 환경에서 권장. 단점: 운영 복잡도 ↑, 스키마 변경 시 sink 재설정.

### Reindex 전략 (alias 활용)

```
1. 새 인덱스 생성: products_v2 (새 schema)
2. 백필: products_v1 → products_v2 (bulk reindex API)
3. Dual write: outbox worker가 v1, v2 모두 인덱싱
4. Validation: 일정 기간 결과 비교 (rate of mismatch < 0.1%)
5. Alias 전환: products → products_v2 (atomic)
6. v1 인덱스 보관 (1주일) → 삭제
```

**필수**: alias 사용 (`products`라는 별칭). 코드는 alias만 알아야 함. 인덱스 직접 참조 금지.

---

## 쿼리 패턴

### Multi-match (BM25 기반)

```json
{
  "query": {
    "multi_match": {
      "query": "아이폰 케이스",
      "fields": ["title^3", "description", "tags^2", "brand"],
      "type": "best_fields",
      "fuzziness": "AUTO",
      "operator": "and"
    }
  }
}
```

- `title^3`: title 매치는 3배 boost
- `fuzziness: AUTO`: 1~2자 차이 허용 (오타)
- `operator: and`: 모든 토큰 매치 (default or는 noisy)

### 자동 완성 (instant search)

```json
// 인덱스 매핑에 edge_ngram 또는 search_as_you_type
{
  "title_suggest": {
    "type": "search_as_you_type",
    "max_shingle_size": 3
  }
}

// 쿼리
{
  "query": {
    "multi_match": {
      "query": "아이폰",
      "type": "bool_prefix",
      "fields": ["title_suggest", "title_suggest._2gram", "title_suggest._3gram"]
    }
  }
}
```

### Filter (정확 매칭, score 무관)

```json
{
  "query": {
    "bool": {
      "must": [{ "multi_match": { "query": "아이폰", "fields": ["title"] } }],
      "filter": [
        { "term": { "tenant_id": "abc" } },
        { "term": { "category": "electronics" } },
        { "range": { "price": { "gte": 10000, "lte": 100000 } } },
        { "geo_distance": { "distance": "5km", "location": "37.5,127.0" } }
      ]
    }
  }
}
```

→ filter는 캐싱 + score 계산 skip → 성능 ↑.

### Hybrid 검색 (BM25 + Vector reranking)

```json
{
  "query": {
    "hybrid": {
      "queries": [
        { "match": { "title": "아이폰 케이스" } },
        { "knn": { "field": "embedding", "query_vector": [...], "k": 50 } }
      ]
    }
  }
}
```

- BM25로 키워드 매치 → top 100
- Vector로 의미 검색 → top 100
- RRF (Reciprocal Rank Fusion)로 결합

세부 ANN 운영은 [`ai/vector-db.md`](../vector-db/SKILL.md) §HNSW.

---

## 추천 시스템 (3 패턴)

### 패턴 1: Co-occurrence (item-to-item)

```
"이 상품을 본 사람이 본 다른 상품"

1. Event log: user X viewed item A → viewed item B
2. Co-occurrence matrix: count(A, B)
3. Recommend: input item A → top N by count(A, *)
```

- 가장 단순, **부트스트랩 첫 추천**
- 콜드 스타트 약함 (새 item)
- SQL/Spark 야간 배치로 충분

### 패턴 2: Collaborative Filtering (user-to-user)

```
"비슷한 사용자가 좋아한 상품"

ALS (Alternating Least Squares) 또는 implicit feedback
- input: user-item interaction matrix (sparse)
- output: user latent vector + item latent vector
- recommend: nearest items in user's vector space
```

- Spotify, Netflix 표준
- Spark MLlib, implicit (Python) 활용
- 콜드 스타트는 content-based로 보완

### 패턴 3: Content-based (embedding)

```
"이 상품과 비슷한 상품"

1. Item description → embedding (Sentence-Transformers, OpenAI)
2. Vector DB 저장 (pgvector / Qdrant)
3. ANN 검색으로 유사 item top N
```

- 콜드 스타트 강함 (임베딩만 있으면 OK)
- LLM provider 비용 의존 (`business/credit-system.md` 패턴 적용)
- 자세한 운영: [`ai/vector-db.md`](../vector-db/SKILL.md), [`ai/rag-patterns.md`](../rag-patterns/SKILL.md)

### 하이브리드 (실전)

```
Real-time: co-occurrence (Redis sorted set, click stream)
Batch (1d): CF + content-based ALS
Reranking: business rule (재고, prom, 광고)
```

---

## 검색 분석 (no-result + CTR)

```sql
-- no-result 쿼리 (검색 갭)
SELECT query, COUNT(*) AS searches
FROM search_logs
WHERE result_count = 0
  AND searched_at >= NOW() - INTERVAL '7 days'
GROUP BY query
ORDER BY searches DESC
LIMIT 100;

-- CTR (위치별 클릭률)
SELECT position, COUNT(*) AS impressions,
       SUM(CASE WHEN clicked THEN 1 ELSE 0 END) AS clicks,
       100.0 * SUM(CASE WHEN clicked THEN 1 ELSE 0 END) / COUNT(*) AS ctr_pct
FROM search_results
GROUP BY position
ORDER BY position;
```

**no-result top 100** → 동의어 사전 보강 / 인덱스 누락 / spelling.

분석 결과는 [`dx/quarterly-review.md`](../quarterly-review/SKILL.md)에 통합 권장.

---

## 한국 시장 깊이

### 한국어 검색 특수성

- **형태소 분석 필수** — 영어식 stem(ing)은 0% recall
- **자모 분리 검색** — 사용자가 "아이ㅍ"까지 입력해도 "아이폰" suggest. nori는 미지원, custom analyzer 필요
- **로마자 검색** — "iphone"으로도 "아이폰" 매치. romanization filter
- **한자 변환** — 국립중앙도서관/사주/한의학 도메인은 한자 ↔ 한글 매핑 필요
- **신조어 빠름** — "찐", "갓생", "레전드" 등. 동의어 사전 분기마다 갱신
- **띄어쓰기 다양** — "아이폰 케이스" vs "아이폰케이스" 모두 매치 (decompound_mode mixed)

### 한국 사용자 검색 행태

- 평균 쿼리 길이 짧음 (2~3 어절)
- 네이버 검색에 익숙 — 정확도 > recall
- 자동 완성 의존도 높음 (모바일 60%+)
- 카테고리 필터 활발 사용

### Provider 한국어 지원 현실

| Provider | nori | 자모 분리 | 동의어 | 한글 자동완성 |
|---|---|---|---|---|
| Elasticsearch + nori | ✅ | custom | ✅ | edge_ngram |
| OpenSearch + nori | ✅ | custom | ✅ | search_as_you_type |
| Algolia | basic | ❌ | ✅ | ✅ |
| Typesense | basic | ❌ | ✅ | ✅ |
| **Naver Cloud Search** | ✅ Naver tokenizer | ✅ | ✅ | ✅ |
| Meilisearch | basic | ❌ | ✅ | ✅ |

→ **고품질 한국어 검색 필요시 nori 기반 (OpenSearch/ES) 또는 Naver Cloud Search**.

### 법령

- **PIPA (개인정보보호법)** — 검색 쿼리는 PII 가능 (이름/전화번호/주소 입력 사례). 로그 저장 시 마스킹 필수
- **위치정보법** — geo radius 검색 시 위치 동의 의무
- 자세한 법령 추적: [`legal/data-subject-rights.md`](../data-subject-rights/SKILL.md), [`legal/kr-location-info-act.md`](../kr-location-info-act/SKILL.md)

---

## 보안 + 안티패턴

### 보안

- **tenant 격리**: 모든 쿼리에 `term: tenant_id` filter 강제. 누락 시 cross-tenant data leak
- **권한 필터**: ACL 필드를 인덱스에 포함, 쿼리 시 user의 role과 매칭
- **검색 쿼리 로그 PII**: 마스킹 또는 hash 후 저장. 30일 retention
- **rate limiting**: 검색 API에 [`business/rate-limiting.md`](../rate-limiting/SKILL.md) 적용 (DDoS, scraping 방지)
- **인덱스 노출 금지**: ES/OS 공개 endpoint 금지. VPC + auth + IP allowlist

### 안티패턴

| 안티패턴 | 왜 나쁜가 | 대신 |
|---|---|---|
| 인덱스 직접 참조 (alias 미사용) | reindex 불가능, 다운타임 | alias 필수 |
| `query_string` 사용자 입력 직접 | 쿼리 인젝션 (`field:value AND ...`) | `match` / `multi_match` parameterized |
| `_search?size=10000` | 메모리 폭발, deep pagination 비효율 | `search_after` / `scroll` API |
| nori 없이 한국어 인덱싱 | recall 0% 가까움 | nori 또는 Naver tokenizer |
| Synchronous DB+Search write | search 다운 → DB write 실패 | Outbox 패턴 |
| `refresh_interval: 1s` (default) | 색인 부하 ↑ | 5~30s, bulk index 시 -1 후 재설정 |
| `_all` field (Elasticsearch < 6.0) | 비효율, deprecated | multi-field copy_to |
| Filter 대신 Query로 정확 매칭 | score 계산 낭비 | bool filter |
| 인덱스 mapping dynamic | field explosion (1000+ fields) | `dynamic: strict` 또는 `false` |
| 단일 인덱스에 모든 tenant | 격리 어려움, scale 한계 | tenant 큰 경우 index per tenant, 작으면 routing |
| 검색 결과 캐싱 안 함 | 인기 쿼리 재계산 | Redis with TTL (1~10분) |
| Recommend를 단일 알고리즘으로 | 콜드 스타트 / diversity 약함 | hybrid (real-time + batch + reranking) |
| 검색 분석 (no-result, CTR) 안 함 | 검색 품질 정체 | 분기마다 분석 + 동의어 보강 |
| `nested` 남용 | 쿼리 복잡, 인덱싱 비용 | 가능하면 flatten 또는 join 분리 |
| Reindex downtime | 사용자 검색 실패 | dual write + alias swap |

---

## ADR 템플릿

### ADR: 검색 엔진 선택

```markdown
## Context
- 트래픽: N MAU, 검색 query M/day
- 도메인: 한국어 우선, 카테고리 필터
- 팀: ops 인력 X
- 예산: $Y/월

## Options
A. Algolia (관리형, 비용 ↑, 빠른 시작)
B. OpenSearch managed (AWS, 한국어 nori, 운영 적당)
C. Typesense Cloud (가성비, 단순)
D. PostgreSQL FTS (DB만, ≤100K)

## Decision
[선택] 이유: ...

## Consequences
- 비용: ...
- ops 부담: ...
- migration cost (Provider 교체): SearchGateway 추상화로 ...
- 한국어 품질: ...

## Predicted Outcomes (6개월)
- 검색 p95 latency < 200ms
- no-result rate < 5%
- CTR @1 > 35%
- 비용 < $X/월

## Review Schedule
- Tier 1 (인프라급) — 6개월 review
- Auto-trigger: 트래픽 5x, no-result 10%+, 비용 1.5x
```

자세한 retrospective 흐름은 [`dx/adr-retrospective.md`](../adr-retrospective/SKILL.md).

---

## Quick Start (3시간 부트스트랩)

```
1. PostgresFTSGateway로 시작 (≤ 100K docs)
   - tsvector + GIN index
   - mecab-ko 또는 pg_trgm trigram
2. SearchGateway 인터페이스 정의 (5 메서드)
3. Outbox 테이블 + Worker (5분 polling)
4. Multi-match + filter 쿼리 (tenant_id, category)
5. 자동 완성: pg_trgm 또는 trigram_similarity
6. 검색 로그 테이블 (query, result_count, clicked)
7. Grafana: query latency p50/p95/p99, no-result rate
8. 트래픽 50K MAU 도달 시 OpenSearch 또는 Algolia로 교체
```

---

## 다음 단계 (After Adoption)

- 추천 시스템: co-occurrence batch (Spark / Airflow)
- A/B 실험: ranking 알고리즘 비교 ([`business/feature-flags.md`](../feature-flags/SKILL.md))
- 검색 품질 메트릭: NDCG@10, MRR, no-result rate
- Personalized search: user vector + item vector dot product
- LLM 기반 query understanding (typo, intent, entity extraction)
- 한국어 spell correction (한컴 사전 + 사용자 로그 기반)
- Vector reranking (BM25 top 100 → embedding rerank top 10)
- 검색 분석을 분기 회고에 통합 ([`dx/quarterly-review.md`](../quarterly-review/SKILL.md))

---

## 관련 자원

- Elasticsearch: The Definitive Guide (O'Reilly) — BM25, relevance tuning
- Sebastian Raschka, "Machine Learning Q and AI" — CF / content-based 비교
- Algolia "Building Search Experiences" — UX 가이드
- nori plugin docs (Apache Lucene 한국어 분석)
- 네이버 검색 기술 블로그 — 한국어 검색 행태 데이터
- "Recommender Systems Handbook" (Springer)
