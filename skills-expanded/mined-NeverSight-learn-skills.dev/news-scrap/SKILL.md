---
name: news-scrap
description: '응급의료 AI 관련 주간 뉴스 스크랩. 매주 일주일간(토~금) 기간의 기사/논문을 수집·분석·정리. Keywords: 뉴스, news, 스크랩, scrap, 응급, emergency, AI 뉴스'
---

# 응급의료 AI 주간 뉴스 스크랩

## Purpose

매주 금요일 실행하여, 해당 주에 발행된 응급실/응급의학과 AI 관련 뉴스 기사 및 학술 논문을 자동 수집·분석·정리하고 대시보드 스타일 HTML 파일로 저장한다.

**IMPORTANT: 모든 출력은 한국어로 작성한다.**

## Trigger Conditions

### When to activate:

- /news-scrap, 뉴스 스크랩, 뉴스 수집, 주간 뉴스
- "이번 주 응급의료 뉴스 정리해줘"
- "뉴스 스크랩 돌려줘"

### When NOT to activate:

- 단순 뉴스 검색 질문 (e.g., "최근 AI 뉴스 뭐 있어?")
- 응급의료와 무관한 뉴스 요청

---

## Workflow

### Step 1: 날짜 범위 계산

1. 오늘 날짜를 기준으로 **직전 7일간(전주 토요일 ~ 이번 주 금요일)** 범위를 계산한다.
   - 시작일: 전주 토요일
   - 종료일: 이번주 금요일 (= 오늘이 금요일이면 오늘)
   - 금요일이 아닌 날 실행해도 가장 최근 금요일을 종료일로 계산
2. 날짜 형식: `YYYY년 MM월 DD일` (한국어), `YYYY-MM-DD` (파일명용)
3. 사용자에게 수집 기간을 안내한다:
   ```
   수집 기간: 2026년 3월 8일(토) ~ 2026년 3월 14일(금) - 3월 2주차
   ```

---

### Step 2: 팀 생성 및 병렬 수집

#### 2-1. TeamCreate로 수집 팀 생성

**TeamCreate 도구**를 호출하여 뉴스 수집 팀을 생성한다:

| 파라미터      | 값                              |
| ------------- | ------------------------------- |
| `team_name`   | `news-scrap`                    |
| `description` | `응급의료 AI 주간 뉴스 수집 팀` |

**팀 멤버:**

| 에이전트   | 역할                                     |
| ---------- | ---------------------------------------- |
| `국내기사` | 국내 응급의료 AI 뉴스 검색·수집·원문추출 |
| `해외기사` | 해외 응급의료 AI 뉴스 검색·수집·원문추출 |
| `학술논문` | 응급의료 AI 학술 논문 검색·수집·원문추출 |

#### 2-2. SendMessage로 작업 지시

TeamCreate 완료 후, **하나의 메시지에서 SendMessage 3회를 병렬 호출**한다:

> **IMPORTANT:** 반드시 3개 SendMessage를 **하나의 메시지에서 동시에** 실행하여 병렬 처리한다. 순차 호출 금지.

각 에이전트에게 전달하는 message는 **해당 에이전트 고유 프롬프트 + 공통 수집 지침**을 합쳐서 전달한다.

---

#### 공통 수집 지침

아래 내용을 **모든 에이전트 프롬프트 뒤에 붙여서** SendMessage의 message로 전달한다:

````
## 원문 추출 및 발행일 확인 (필수)

WebSearch로 URL을 수집한 후, **Bash 도구**로 `trafilatura` 스크립트를 실행하여 원문+발행일을 일괄 추출한다.

### 실행 방법

수집한 URL 목록을 JSON 배열로 만들어 스크립트에 전달:

```bash
echo '["https://url1", "https://url2", ...]' | python {이 스킬의 scripts/extract.py 절대경로}
````

스크립트가 반환하는 JSON:

```json
[
  {
    "url": "...",
    "text": "본문",
    "date": "YYYY-MM-DD",
    "title": "제목",
    "success": true
  },
  { "url": "...", "text": "", "date": null, "title": "", "success": false }
]
```

### 결과 처리

1. `success: true` + `date`가 {시작일}~{종료일} 범위 내 → **포함**
2. `success: true` + `date`가 null → URL 경로나 WebSearch 스니펫에서 날짜 추출 시도. 실패 시 **제외**
3. `success: false` → WebSearch 스니펫에서 날짜 추출 시도. 날짜 확인되면 **포함** (원문은 빈 문자열)
4. 발행일이 범위 밖 → **제외**. "추정" 날짜 금지.

> **핵심:** 원문 추출 실패해도 발행일만 확인되면 기사를 포함한다. 원문이 없는 기사는 `원문` 필드를 빈 문자열로 설정.

## 반환 형식

중복 제거 후, 아래 JSON 배열만 출력하라 (설명 텍스트 없이 JSON만):

```json
[
  {
    "기관매체": "출처 매체명 또는 저널명",
    "관련기관": "기사에 등장하는 병원/기업/기관",
    "활용분야": "트리아지, 영상판독 등",
    "구분": "연구|도입|정책|트렌드",
    "제목": "기사/논문 제목 (해외 기사는 한국어 번역)",
    "원문": "trafilatura로 추출한 본문 (추출 실패 시 빈 문자열)",
    "날짜": "YYYY-MM-DD",
    "링크": "원문 URL"
  }
]
```

모든 출력은 한국어로 작성한다. 수집된 기사가 없으면 빈 배열 []을 반환한다.

```

---

#### 에이전트 1 프롬프트 (국내기사)

```

너는 국내 응급의료 AI 뉴스 수집 전문가다. {시작일}~{종료일} 기간에 발행된 국내 기사를 수집하라.

## 검색 실행

아래 키워드마다 WebSearch 도구를 호출한다 (blocked_domains: ["youtube.com", "blog.naver.com", "tistory.com", "brunch.co.kr", "medium.com", "velog.io", "reddit.com"]):

1. 응급실 AI 인공지능 {시작일}~{종료일}
2. 응급의학 인공지능 병원 도입 {시작일}~{종료일}
3. 응급환자 AI 트리아지 분류 {시작일}~{종료일}
4. 응급의료 AI 정책 정부 {시작일}~{종료일}
5. 응급실 과밀 AI 병상 배정 {시작일}~{종료일}
6. 119 AI 시스템 구급 {시작일}~{종료일}
7. 중증환자 AI 분류 예측 {시작일}~{종료일}
8. 의료 AI 인공지능 병원 도입 {시작일}~{종료일} (와일드카드)

우선 도메인: medigatenews.com, dailymedi.com, mdtoday.co.kr, amedinews.com, pharm.edaily.co.kr, mohw.go.kr, yna.co.kr, medicaltimes.com

## 와일드카드 필터링

키워드 8번처럼 "응급"이 포함되지 않은 키워드로 수집된 기사는, 응급실·응급의학·중환자·구급·이송과 직접 관련이 있는 경우에만 포함한다. 순수 일반 의료 AI(피부과 AI, 안과 AI 등)는 제외한다.

```

---

#### 에이전트 2 프롬프트 (해외기사)

```

너는 해외 응급의료 AI 뉴스 수집 전문가다. {시작일}~{종료일} 기간에 발행된 해외 기사를 수집하라.

## 검색 실행

아래 키워드마다 WebSearch 도구를 호출한다 (blocked_domains: ["youtube.com", "blog.naver.com", "tistory.com", "brunch.co.kr", "medium.com", "velog.io", "reddit.com"]):

1. emergency department AI triage {시작일}~{종료일}
2. emergency medicine artificial intelligence {시작일}~{종료일}
3. emergency room AI clinical decision support {시작일}~{종료일}
4. emergency department overcrowding AI patient flow {시작일}~{종료일}
5. prehospital AI EMS prediction {시작일}~{종료일}
6. ambulance AI routing dispatch real-time {시작일}~{종료일}
7. hospital AI clinical workflow automation {시작일}~{종료일} (와일드카드)

우선 도메인: healthcareitnews.com, beckershospitalreview.com, medpagetoday.com, statnews.com, fiercehealthcare.com, mobihealthnews.com

## 와일드카드 필터링

키워드 7번처럼 "emergency"가 포함되지 않은 키워드로 수집된 기사는, emergency department·emergency medicine·critical care·EMS·prehospital과 직접 관련이 있는 경우에만 포함한다. 일반 의료 AI(dermatology AI, ophthalmology AI 등)는 제외한다.

```

---

#### 에이전트 3 프롬프트 (학술논문)

```

너는 응급의료 AI 학술 논문 수집 전문가다. {시작일}~{종료일} 기간에 발행된 학술 논문을 수집하라.

## 검색 실행

아래 키워드마다 WebSearch 도구를 호출한다 (blocked_domains: ["youtube.com", "blog.naver.com", "tistory.com", "brunch.co.kr", "medium.com", "velog.io", "reddit.com"]):

1. emergency triage AI machine learning site:pubmed.ncbi.nlm.nih.gov {시작일}~{종료일}
2. emergency medicine artificial intelligence peer-reviewed {시작일}~{종료일}
3. emergency department AI clinical trial {시작일}~{종료일}
4. emergency department crowding AI resource allocation {시작일}~{종료일}
5. prehospital emergency AI prediction model {시작일}~{종료일}

우선 도메인: pubmed.ncbi.nlm.nih.gov, pmc.ncbi.nlm.nih.gov, medinform.jmir.org, jmir.org, annemergmed.com, emj.bmj.com, ai.nejm.org, nature.com, frontiersin.org, mdpi.com, sciencedirect.com

````

---

#### 에이전트 결과 수신

각 에이전트는 텍스트로 결과를 반환한다. 반환된 텍스트에서 JSON 배열 부분(`[` ~ `]`)을 추출하여 파싱한다.

- JSON 파싱 실패 시: 해당 에이전트 결과를 빈 배열 `[]`로 처리하고 계속 진행한다
- 3개 에이전트 결과를 각각 `국내_결과`, `해외_결과`, `학술_결과` 변수로 보관한다

---

### Step 3: 결과 통합 및 중복 제거

3개 에이전트의 결과 JSON 배열을 합친 후 아래 처리를 수행한다:

1. **URL 기준 중복 제거** — 같은 URL이 여러 에이전트에서 수집된 경우 1건만 남긴다
2. **같은 내용의 다른 매체 보도** — 대표 1건만 남긴다
3. **섹션 분류:**
   - 에이전트 1(국내) 결과 → **국내 기사** 섹션
   - 에이전트 2(해외 기사) + 에이전트 3(학술 논문) 결과 → **해외 기사 / 학술 논문** 섹션
4. **응급의료와 직접 관련 없는 일반 AI/헬스케어 기사는 제외**한다

---

### Step 4: NotebookLM 업로드 및 AI 분석

`notebooklm-py` 패키지를 사용하여 수집된 기사 원문을 NotebookLM에 업로드하고, AI 분석을 수행한다.

> **사전 조건:** `pip install notebooklm-py` 설치 완료

#### 4-0. NotebookLM 인증 확인

NotebookLM API 호출 전에 인증 상태를 확인한다. 아래 Bash 명령으로 간단한 API 호출을 시도한다:

```bash
python -c "
import asyncio
from notebooklm import NotebookLMClient

async def main():
    try:
        async with await NotebookLMClient.from_storage() as client:
            await client.notebooks.list()
            print('AUTH_OK')
    except Exception as e:
        print(f'AUTH_FAIL:{e}')

asyncio.run(main())
"
```

- `AUTH_OK` 출력 → 정상, Step 4-1 진행
- `AUTH_FAIL` 출력 → `notebooklm login` 실행 후 사용자에게 브라우저 로그인 안내:
  ```bash
  notebooklm login
  ```
  ```
  ⚠️ NotebookLM 인증이 만료되었습니다. 브라우저에서 Google 로그인을 완료해주세요.
  ```
  로그인 완료 후 인증 확인을 재시도한다. 재시도 실패 시 NotebookLM 관련 Step(4~8)을 건너뛰고 HTML 대시보드(Step 6)만 생성한다.

#### 4-1. 월간 노트북 확보

**월 단위로 노트북을 관리한다.** 같은 월의 노트북이 이미 존재하면 재사용하고, 없을 때만 새로 생성한다.

노트북 이름 규칙: `응급의료_AI_월간브리핑_{년}_{월}` (예: `응급의료_AI_월간브리핑_2026_03`)

```bash
python -c "
import asyncio
from notebooklm import NotebookLMClient

NOTEBOOK_NAME = '응급의료_AI_월간브리핑_{년}_{월}'

async def main():
    async with await NotebookLMClient.from_storage() as client:
        notebooks = await client.notebooks.list()
        for nb in notebooks:
            if nb.title == NOTEBOOK_NAME:
                print(nb.id)
                return
        notebook = await client.notebooks.create(
            title=NOTEBOOK_NAME,
            description='{년}년 {월}월 응급의료 AI 뉴스 아카이브'
        )
        print(notebook.id)

asyncio.run(main())
"
````

출력된 `notebook_id`를 이후 단계에서 사용한다.

#### 4-2. 주차별 합본 소스 업로드

Step 3에서 중복 제거된 기사 중 **원문(`원문` 필드)이 있는 기사만** 하나의 텍스트로 합쳐 `add_text` 1회 호출로 업로드한다. 원문이 빈 문자열인 기사는 합본에서 제외한다.

합본 소스 텍스트 형식:

```
=== 응급의료 AI 주간 뉴스 — {시작일}~{종료일} ({월} {주차}) ===

--- 기사 1 ---
제목: {제목}
매체: {기관매체} | 관련기관: {관련기관} | 분야: {활용분야} | 구분: {구분}
날짜: {날짜} | 원문링크: {링크}

{원문}

--- 기사 2 ---
...
```

- `client.sources.add_text()` **1회** 호출 → `wait_until_ready(timeout=300)`
- 업로드 완료를 출력한다 (기사 N건, 합본 소스 1개)

#### 4-3. NotebookLM AI 질의

모든 소스 업로드 완료 후, NotebookLM에 아래 4개 질문을 순차 실행하고 답변을 수집한다. 모든 질문에 `response_length="LONGER"` 옵션을 사용한다.

**Q0 — 기사별 상세 요약 (HTML 대시보드용):**

```
업로드된 각 기사/논문에 대해 개별적으로 상세 요약을 한국어로 작성해줘.
반드시 업로드된 소스의 본문 내용만을 근거로 요약하고, 본문이 없거나 제목만 있는 기사는 "원문 미확보"로만 표기해줘. 절대로 추측하거나 지어내지 마.
각 기사마다 아래 형식으로 출력해줘:

[기사 제목 그대로]

**기사 요약:**
이 기사의 핵심 내용을 5~8문장으로 요약해줘. 누가, 무엇을, 왜, 어떻게 했는지를 중심으로 기사의 전체 흐름을 파악할 수 있도록 작성해줘.

**세부 분석:**
- 관련 기업/기관: 기사에 등장하는 기업이나 기관이 어떤 곳인지 간략 소개
- 기술/제품: 어떤 기술이나 제품인지, 어떻게 작동하는지
- 핵심 수치: 정확도, AUC, 비용 절감, 도입률 등 기사에 나온 구체적 숫자
- (연구/논문인 경우) 연구 방법과 결과: 대상 수, 연구 설계, 주요 결과, 한계점
```

Q0 답변 파싱: `[기사 제목]`으로 매칭하여 해당 기사 JSON에 `핵심내용` 추가. 매칭 실패 시 원문 첫 3문장을 대체.

**Q1 — 핵심 동향:** "수집된 모든 소스를 바탕으로 이번 주 응급의료 AI 분야의 3대 핵심 동향을 뽑아줘. 각 동향마다 근거가 되는 기사 제목을 인용해줘."

**Q2 — 주목할 기관:** "가장 혁신적인 기술 도입 사례나 주목해야 할 기업/기관 2곳을 선정하고, 왜 주목할 만한지 구체적으로 설명해줘."

**Q3 — 시사점:** "이 소스들이 시사하는 응급의료 AI의 임상적 가치와 향후 발전 방향을 3~5문장으로 정리해줘."

답변 활용:

- Q0 → 각 기사의 **핵심내용** (HTML 아코디언 본문에 **기사 요약 + 세부 분석** 모두 포함)
- Q1 → **이번 주 핵심 동향** (Step 5)
- Q2 → **주목할 기관/기업** (Step 5)
- Q3 → **시사점** (Step 5)

---

### Step 5: 주간 요약 작성

Step 4-3의 NotebookLM 답변을 기반으로 주간 요약을 구성한다:

1. **이번 주 핵심 동향** (3~5개 bullet point) — Q1 답변
2. **주목할 기관/기업** — Q2 답변
3. **시사점** (2~3문장) — Q3 답변

NotebookLM 답변이 한국어가 아닌 경우 한국어로 번역하여 사용한다.

---

### Step 6: HTML 대시보드 파일 저장

1. 저장 경로: `news_output/` 폴더 (프로젝트 루트 기준, 없으면 생성)
2. 파일명: `news_{해당년도월주차}.html` (예: `news_26년 3월 2주차.html`)
   - **같은 파일명이 이미 존재하면 삭제 후 새로 작성한다**
3. 템플릿 파일 `templates/dashboard.html`을 읽어서 실제 데이터로 채운다.
   - 템플릿 내 `<!--ARTICLE_TEMPLATE: ... -->` 주석과 플레이스홀더(`{시작일}`, `{종료일}`, `{총건수}` 등)를 참고하여 치환
   - `구분` 값에 따라 태그 클래스 적용: `tag-연구`, `tag-도입`, `tag-정책`, `tag-트렌드`
   - Q0 답변을 파싱하여 `article-summary`(기사 요약)와 `article-detail`(세부 분석 dl/dt/dd)에 각각 매핑
   - 세부 분석 항목 중 해당 없는 것은 생략 (예: 연구/논문이 아니면 "연구 방법/결과" dt/dd 제거)
   - 주간 요약 섹션도 실제 분석 결과로 채운다

4. 저장 완료 후 안내:
   ```
   저장 완료: news_output/news_26년 3월 2주차.html (국내 X건, 해외 Y건)
   ```

---

### Step 7: NotebookLM 주간 리포트 노트 생성

Step 4-1에서 확보한 노트북에 **'주간 리서치 리포트'** 노트를 생성한다.

```bash
python -c "
import asyncio
from notebooklm import NotebookLMClient

NOTEBOOK_ID = '{notebook_id}'

async def main():
    async with await NotebookLMClient.from_storage() as client:
        await client.notes.create(
            notebook_id=NOTEBOOK_ID,
            title='주간 리서치 리포트 — {시작일}~{종료일}',
            content='''{리포트_내용}'''
        )
        print('NOTE_CREATED')

asyncio.run(main())
"
```

`{리포트_내용}`에는 Step 5의 주간 요약 전체 + 수집 건수를 포함한다.

완료 후 안내:

```
NotebookLM 노트북: 응급의료_AI_월간브리핑_{년}_{월}
- {월} {주차} 합본 소스 업로드 완료 (기사 {N}건)
- 주간 리서치 리포트 노트 생성 완료
```

---

### Step 8: 주간 주목 기사 슬라이드 생성

수집된 기사 중 **가장 중요한 1건**을 선정하여 2장짜리 발표 슬라이드를 생성한다.

#### 8-1. 주목 기사 선정

NotebookLM에 아래 질의를 실행하여 기사를 선정한다:

```
이번 주 수집된 기사/논문 중에서 응급의료 AI 분야에서 가장 중요하고 혁신적인 기사 1건을 선정해줘.
선정 기준: 기술적 혁신성, 임상 영향력, 산업 파급력을 종합 고려.
선정한 기사의 제목을 정확히 알려줘.
```

- `client.chat.ask(notebook_id, question=...)` 사용
- 답변에서 기사 제목을 추출하여 Step 3의 기사 목록과 매칭

#### 8-2. 슬라이드 생성

Bash 도구로 `scripts/slide.py`를 실행한다:

```bash
python {이 스킬의 scripts/slide.py 절대경로} {notebook_id} news_output/slide_{해당년도월주차}.pdf "{instructions}"
```

`{instructions}`에는 아래 내용을 전달한다:

```
한국어로 작성해줘. 2장짜리 슬라이드를 만들어줘.

슬라이드 1 — 이번 주 주목 기사:
- 기사 제목: {선정된 기사 제목}
- 매체/날짜
- 핵심 내용 요약 (누가, 무엇을, 왜, 어떻게)
- 주요 수치/성과

슬라이드 2 — 우리 프로젝트 적용 가능성:
우리는 "119 구급차 ↔ 병원 응급실을 연결하는 AI 기반 응급환자 최적 이송 플랫폼"을 개발 중이다.
핵심 기능: AI 최적 이송병원 추천, 실시간 이송 모니터링(MQTT), 응급실 상황판(병상 포화도), 환자 상세정보(4대 중증질환 판정, WebRTC 영상), 병원 수용 관리 워크플로우.
AI 서비스: 119aisystem.com (환자 긴급도 분류 및 병원 추천).
이 기사의 기술/접근법을 우리 플랫폼에 어떻게 적용할 수 있는지 구체적 아이디어 2~3개를 제시해줘.

반드시 소스 내용만 근거로 하고 추측하지 마.
```

- 출력 파일: `news_output/slide_{해당년도월주차}.pdf`
- 같은 파일이 있으면 덮어쓴다

#### 8-3. 완료 안내

```
슬라이드 생성 완료:
- 주목 기사: {선정된 기사 제목}
- 파일: news_output/slide_{해당년도월주차}.pdf
```

---

## Error Handling

- WebSearch 결과가 0건인 키워드는 건너뛴다
- 해당 주 기사가 전혀 없는 경우: "이번 주 수집된 기사가 없습니다"로 안내
- 발행일을 확인할 수 없는 기사는 제외한다
- `trafilatura` 추출 실패 시에도 발행일만 확인되면 기사 포함 (원문은 빈 문자열)
- `notebooklm-py` 오류 시: 에러 메시지를 출력하고 HTML 대시보드 생성은 정상 진행 (NotebookLM 연동은 선택적)
- 슬라이드 생성 실패 시: 에러 메시지 출력 후 나머지 워크플로우는 정상 진행

## Notes

- 이 스킬은 Claude Code의 WebSearch, `trafilatura`(원문 추출), `notebooklm-py`(분석/아카이브) 연동으로 동작한다
- **사전 설치 필요:** `pip install trafilatura notebooklm-py`
- 결과물의 품질은 검색 시점의 웹 인덱싱 상태에 따라 달라질 수 있다
- 중복 기사는 제거하고, 같은 내용의 다른 매체 보도는 대표 1건만 남긴다
- NotebookLM은 월간 노트북 + 주차별 합본 소스 구조로 운영 (무료 플랜 50소스 한도 내 약 10~12개월 운영 가능)
