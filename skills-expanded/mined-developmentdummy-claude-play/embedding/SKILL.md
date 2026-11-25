---
name: embedding
description: Use when you need to find things by meaning instead of exact words — reusing a previously generated image that fits the scene, recalling past events or notes from long sessions (RAG over memory.md / logs), looking up reference docs or cheatsheets, grouping similar items, or finding near-duplicate images. Local EmbeddingGemma 2 (multilingual text + images). Covers the four call paths (MCP vector_search / vector_upsert / vector_manage, persona tool context.vectors, panel __panelBridge.vectors), scopes, collection design, and how to read scores. Do not use for exact lookups (ids, names in a JSON file) — read the file instead.
---

# 임베딩·의미 검색 (EmbeddingGemma 2)

글이나 이미지를 768차원 벡터로 바꿔 두고, 나중에 **뜻이 가까운 것**을 찾는다.
- 다국어를 지원한다. 한글로 물어도 영어 문서를 찾고, 그 반대도 된다.
- 텍스트와 이미지가 같은 공간에 있어서 글로 이미지를 찾을 수 있다.
- 로컬 GPU에서 돌아서 호출 비용이 없다.
- 실측: 쿼리 한 건 약 0.05~0.1초, 이미지 한 장 약 0.1초. 첫 호출은 모델 로드 때문에 약 10~15초 걸린다.

**역할 분담**
- 임베딩은 "비슷한 것 찾기"만 한다.
- 찾은 결과를 읽고 판단하고 서술하는 일은 LLM(지금 이 대화)이 한다.
- 키·이름·숫자처럼 정확히 일치하는 값을 찾을 때는 파일을 직접 읽어라. 임베딩은 철자가 아니라 뜻을 본다.

## 네 가지 호출 경로

| 어디서 | 어떻게 |
|---|---|
| 세션 AI (지금 이 대화) | MCP `vector_search` · `vector_upsert` · `vector_manage` |
| 페르소나 도구 `tools/*.js` | `await context.vectors("search", { collection, query })` |
| 패널·앱 화면 JS | `await __panelBridge.vectors("search", { collection, query })` |
| HTTP | `POST /api/sessions/{id}/vectors` 본문 `{ action, ...params }` |

네 경로 모두 `src/lib/vector-index.ts`의 같은 액션을 부른다. 액션은 `search`, `upsert`, `index_dir`, `index_file`, `list`, `info`, `delete`, `drop`, `embed`, `warmup`이다.
빌더 세션에서는 MCP 도구가 동작하지 않는다(세션 전용).
`embed` 액션은 768개 숫자 배열을 그대로 돌려준다. 도구와 패널 코드용이라 세션 AI가 직접 부를 일은 없다. 검색은 `vector_search`로 해라.

⚠️ **페르소나 도구는 10초 제한이 있다.** 모델이 내려가 있으면 첫 호출이 이 제한을 넘을 수 있다.
- 패널이 열릴 때나 세션 시작 액션에서 `vectors("warmup")`을 먼저 불러 둬라. warmup은 기다리지 않고 바로 돌아온다.
- **월드 엔진 `step()` 안에서는 부르지 마라.** 200ms 월드 시계가 멈춘다.

## 스코프: 어디에 저장하나

| scope | 위치 | 쓰임 |
|---|---|---|
| `session` (기본) | `{세션}/vectors/{이름}.json` | 이 세션의 기억, 대화 기록, 세션 이미지 |
| `persona` | `{페르소나}/vectors/{이름}.json` | 그 페르소나의 모든 세션이 같이 쓰는 갤러리와 설정 문서 |
| `global` | `data/vectors/{이름}.json` | 모든 페르소나가 같이 쓰는 참조 자료(LoRA 치트시트 등) |

- 경로 파라미터(`image`, `dir`, `file`)는 **스코프 폴더 기준 상대 경로**다. `data/` 밖으로는 나갈 수 없다.
- 검색 결과의 `source`도 같은 기준이다.

## 활용 패턴

### 1. 생성 이미지 재사용 ("한번 생성한 이미지는 반드시 재사용한다")
```
vector_manage { action: "index_dir", collection: "gallery", dir: "images" }
  → remaining > 0 이면 같은 호출을 반복한다 (한 번에 200장)
vector_search { collection: "gallery", query: "비 오는 옥상에서 우산을 든 유나", topK: 3 }
  → hits[0].source = "images/yuna_rain.png" → $IMAGE:images/yuna_rain.png$
```
- **index_dir는 증분이다.** 바뀌지 않은 파일은 건너뛰고, 지워진 파일은 인덱스에서 뺀다(`prune`). 새 이미지를 만든 뒤 다시 불러도 비용이 거의 없다.
- `_`로 시작하는 파일(빌더 미리보기 등)은 건너뛴다.
- 페르소나 폴더 이미지(`scope: "persona"`)를 쓸 때 토큰은 `$IMAGE:persona:파일명$`이다. `images/`를 빼고 쓴다.
- **글로 이미지를 찾을 때는 정확도가 낮다.** 텍스트↔이미지 점수는 0.6대에 몰려 있다. 정확도를 높이려면 이미지를 생성한 직후 그 프롬프트(장면 설명)를 같은 source로 함께 넣고 `dedupeBySource: true`로 검색해라.
  ```
  vector_upsert { collection: "gallery", items: [
    { id: "images/yuna_rain.png#caption", text: "유나, 비 오는 밤 옥상, 우산, 젖은 교복", source: "images/yuna_rain.png" } ] }
  vector_search { collection: "gallery", query: "...", dedupeBySource: true }
  ```
- 비슷한 이미지 찾기(이미지↔이미지)는 정확하다. 같은 캐릭터의 다른 컷이 0.9 안팎으로 나온다. `image: "images/x.png"`로 검색하면 된다.

### 2. 긴 세션의 기억 회상 (RAG)
```
vector_manage { action: "index_file", collection: "memory", file: "memory.md", chunkChars: 500 }
vector_search { collection: "memory", query: "희명이 유나에게 했던 약속", topK: 3 }
```
- `index_file`은 파일을 제목(#)과 문단 단위로 자른다. 각 조각 앞에는 `[제목]`이 붙는다.
- 같은 파일을 다시 넣으면 그 파일의 이전 조각을 전부 갈아 끼운다. 파일이 바뀌지 않았으면 건너뛴다.
- `chunkChars`는 조각 하나의 최대 크기다. 문단을 이 크기까지 합친다.
  - 사건 로그처럼 한 줄이 한 사실인 파일은 300~500으로 작게 잡아라.
  - 설정 문서는 800~1200이 적당하다.
- 장면이 바뀔 때나 오래된 떡밥이 다시 나올 때 검색해라. 결과의 `text`를 읽고 서사에 반영하면 된다. **검색 결과를 사용자에게 그대로 보여주지 마라.**
- 직접 요약한 기억 조각을 쌓을 수도 있다. `vector_upsert { collection: "episodes", items: [{ id: "day7-goblin", text: "...", meta: { day: 7, npc: "유나" } }] }`처럼 넣고, `filter: { npc: "유나" }`로 좁혀 찾는다.

### 3. 참조 문서 조회
LoRA 치트시트, 세계관 설정집, 아이템 도감처럼 길어서 매번 통째로 읽기 부담스러운 문서에 쓴다.
`scope: "global"` 또는 `"persona"`로 한 번 `index_file` 해 두고, 필요할 때 `vector_search`로 관련 조각만 꺼낸다.

### 4. 페르소나 도구·패널에서
```js
// tools/engine.js — NPC가 비슷한 과거 사건을 떠올린다
const r = await context.vectors("search", { collection: "episodes", query: situationText, topK: 2, minScore: 0.6 });
const recalled = r.hits.map((h) => h.text);

// 패널 — 검색창
const { hits } = await __panelBridge.vectors("search", { scope: "persona", collection: "gallery", query: input.value, topK: 12, dedupeBySource: true });
```

## 컬렉션 설계 규칙

- **컬렉션 하나에는 한 종류만 넣어라.** 기억, 갤러리, 문서를 섞으면 순위가 흐려진다. 섞어야 한다면 `meta`로 구분하고 `filter`로 좁혀라.
- **id는 다시 넣었을 때 같은 값이 나오게 정해라**(파일 경로, `day7-goblin` 등). 같은 id로 다시 넣으면 교체된다.
- **dim은 컬렉션을 만들 때 한 번 정해지고 바뀌지 않는다.**
  - 기본값 768을 쓰면 된다.
  - 수천 개가 넘는데 정확도가 덜 중요하면 256이나 512를 써라.
  - 다른 dim을 섞으려 하면 409로 거부된다. 바꾸려면 `drop` 후 다시 만든다.
- **모델이 바뀌면 컬렉션도 다시 만들어야 한다.** 헤더의 model이 다르면 검색이 거부된다.

## 점수 읽는 법

- 점수는 코사인 유사도(-1~1)다.
- **같은 종류끼리만 비교해라.**
  - 텍스트↔텍스트: 관련 있으면 0.75 이상, 무관하면 0.6대.
  - 텍스트↔이미지: 전체가 0.6대에 몰려 있어서 순위만 의미가 있다.
  - 이미지↔이미지: 같은 캐릭터나 장면이면 0.85 이상.
- `minScore`는 같은 종류끼리 검색할 때만 걸어라. 텍스트 기억 검색이라면 0.65~0.7 정도에서 시작해 결과를 보며 조정해라.
- 1위만 믿지 말고 topK 3~5개를 읽은 뒤 LLM이 고르는 게 정확하다.

## task (쿼리 프롬프트)

- 텍스트에는 모델에 내장된 task 프롬프트가 붙는다. 이미지에는 붙지 않는다.
- 기본값은 넣을 때 `document`, 찾을 때 `query`다(질문으로 문서 찾기).
- 문장끼리 얼마나 비슷한지 비교할 때(중복 감지 등)는 넣을 때와 찾을 때 모두 `task: "STS"`를 줘라.
- 이 밖에 `QuestionAnswering`, `CodeRetrieval`, `Classification`, `Clustering`도 쓸 수 있다.

## 실패 처리

| 상태 | 뜻 | 대응 |
|---|---|---|
| 503 | 임베딩 서버 없음 (`gpu-manager/venv-embed` 미설치 또는 `EMBED_ENABLED=false`) | 기능을 건너뛰고 평소대로 진행한다. 사용자에게 장애처럼 알리지 마라 |
| 504 | 시간 초과 (콜드 로드 + 큰 배치) | `warmup` 후 다시 시도하거나, `limit`을 줄인다 |
| 409 | dim이나 모델 불일치 | 기존 컬렉션의 dim을 따르거나 `drop` 후 다시 만든다 |
| 404 | 컬렉션이나 파일이 없음 | `vector_manage { action: "list" }`로 확인한다 |

## 참고
- 설계: `docs/specs/2026-10-07-embedding-core-design.md`
- 서버: `gpu-manager/embed_server.py` (전용 venv, GPU Manager와 별개 프로세스. 이유는 maintenance-playbook §5.19)
