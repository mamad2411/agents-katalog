---
name: notion-lookup
description: >
  Notion 강의 대시보드를 조회·검수하고 Markdown으로 변환합니다.
  MCP 서버를 통해 lecture_search, lecture_detail, lecture_proposals,
  lecture_workbook, analyze_images, review_content 도구를 제공합니다.
metadata:
  author: yunseokchoi-teamsparta
  version: "3.2.0"
---

## 사전 준비

PDF 보고서 생성을 위해 아래 패키지가 필요합니다 (최초 1회):
```bash
pip install fpdf2
```

## 실행 방법

이 스킬은 MCP 서버(`notion-lecture`)로 제공됩니다. Bash 실행이 아닌 **MCP 도구 호출**로 사용합니다.

### 사용 가능한 도구

| 도구 | 설명 |
|------|------|
| `lecture_search` | 강의 목록 검색 (필터 조합 가능) |
| `lecture_detail` | 강의 상세 조회 (속성 + 본문 마크다운 + 제안서 파일) |
| `lecture_proposals` | 제안서 PDF 텍스트 추출 |
| `lecture_workbook` | 교안(workbook) 일차별 교육자료 조회 |
| `analyze_images` | 마크다운 내 이미지 Vision API 분석·캡션 삽입 |
| `review_content` | 교안 콘텐츠 품질 LLM 검수 (9개 규칙) |

### lecture_search

강의 목록을 검색합니다. 모든 파라미터는 선택입니다.

| 파라미터 | 설명 |
|----------|------|
| `search` | 제목 키워드 |
| `status` | 강의 상태 (쉼표 구분 복수 가능) |
| `manager` | 강의 담당자(lecture_PIC) 이름 |
| `sales` | 영업 담당자(sales_PIC) 이름 |
| `target` | 교육 타겟 (실무자, 신입사원, 임원 등) |
| `job` | 직무 (마케터, 개발, 엔지니어 등) |
| `tool` | 사용 툴 (ChatGPT, Python, Excel 등) |
| `topic` | 주제 (데이터 분석, 업무 자동화 등) |
| `product` | 상품명 (AI Literacy, PBL 등) |
| `database` | 데이터베이스 이름 (기본: lecture_dashboard) |
| `limit` | 반환 최대 건수 (기본 50) |

### lecture_detail

`lecture_search` 결과의 `id`를 입력하면 속성, 본문 마크다운, 제안서 파일 목록을 반환합니다.

| 파라미터 | 설명 |
|----------|------|
| `page_id` | 강의 페이지 ID (필수) |

### lecture_proposals

강의의 제안서 PDF에서 텍스트를 인메모리로 추출합니다.

| 파라미터 | 설명 |
|----------|------|
| `page_id` | 강의 페이지 ID (필수) |

### lecture_workbook

강의에 연결된 교안(workbook)의 일차별 교육자료를 조회합니다.
`lecture_search` 결과의 `id`를 입력하면 workbook_dashboard → workbook_card → child_database(일차별 DB) → 챕터 페이지들의 본문 마크다운을 반환합니다.

| 파라미터 | 설명 |
|----------|------|
| `page_id` | 강의 페이지 ID (필수) |

반환: `{lecture_id, workbook_name, workbook_url, sections: [{title, database_id, pages: [{id, title, content_markdown}]}]}`

### analyze_images

마크다운 내 HTTP 이미지를 Vision API로 분석하여 캡션을 삽입합니다.
각 이미지 아래에 `> [이미지 설명] ...` 캡션을 추가합니다.

| 파라미터 | 설명 |
|----------|------|
| `markdown` | 이미지 URL이 포함된 마크다운 텍스트 (필수) |
| `model` | Vision API 모델명 (기본: `gpt-5.2`) |
| `max_workers` | 병렬 처리 스레드 수 (기본: 4) |

반환: `{markdown, image_count, caption_count, errors}`

### review_content

교안 콘텐츠 품질을 LLM으로 검수합니다. 7개 규칙을 기반으로 지적 사항을 반환합니다.

| 파라미터 | 설명 |
|----------|------|
| `markdown` | 검수 대상 마크다운 텍스트 (필수) |
| `title` | 강의 제목 — 고객사명 추출용, 예: `[LG생활건강] AI 활용 교육` (필수) |
| `client_name` | 고객사명 (미입력 시 title의 `[...]`에서 자동 추출) |
| `model` | LLM 모델명 (기본: `gpt-4.1`) |

반환: `{lecture_title, client_name, findings: [{rule_id, severity, location, excerpt, description, suggestion}], summary, model, errors}`

**검수 규칙 (9개):**

| ID | 심각도 | 규칙 |
|----|--------|------|
| NM-01 | critical | 타 고객사명 잔존 — 다른 기업명이 교안 수혜자 맥락에서 등장 |
| NM-02 | critical | 고객사명 오표기 — 유사하지만 다른 이름으로 잘못 표기 |
| EX-01 | critical | 타 고객사 맥락 잔존 — 이전 고객사용 예시/실습이 수정 없이 남음 |
| EX-02 | warning | 업종 불일치 예시 — 고객사 업종과 동떨어진 예시 사용 |
| EX-03 | warning | 경쟁사 긍정 언급 — 직접 경쟁사를 모범 사례로 부각 |
| SP-01 | warning | 명백한 오타 — 글자 누락, 오입력, 자모 오류 |
| SP-02 | info | 맞춤법 오류 — 한글 맞춤법 위반 (고유명사·도구명 제외) |
| IMG-01 | critical | 이미지에 타 고객사/경쟁사 요소 — 이미지 설명에 경쟁사·이전 고객사 로고/UI/제품 포함 |
| IMG-02 | warning | 이미지-내용 불일치 — 이미지 설명이 해당 섹션 교육 내용과 명백히 무관 |

## 교안 검수 워크플로우

사용자가 "검수", "검사", "리뷰", "품질 확인" 등을 요청하면 아래 워크플로우를 실행합니다.

### 워크플로우 절차

1. **강의 검색** — `lecture_search`로 대상 강의를 검색하여 `page_id`를 확보
2. **교안 취합** — `lecture_workbook`으로 교안 마크다운을 취합. 각 섹션·챕터의 `content_markdown`을 하나의 텍스트로 연결
3. **이미지 분석** (선택) — 교안에 이미지가 포함된 경우 `analyze_images`로 캡션 생성. 캡션이 포함된 마크다운을 다음 단계에 전달하면 이미지도 함께 검수됨. 이미지가 없거나 분석 실패 시 스킵
4. **검수 실행** — `review_content`에 (캡션 포함) 마크다운과 강의 제목을 전달하여 검수 수행
5. **보고서 생성** — 검수 결과(JSON)를 아래 보고서 포맷으로 변환. 지적 사항의 `location`을 `lecture_workbook` 결과의 sections/pages와 대조하여 해당 페이지 URL을 매칭:
   - 매칭된 page의 URL: `https://www.notion.so/{page_id에서 하이픈 제거}`
   - 매칭 불가 시 workbook 최상위 URL(`workbook_url`) 사용
6. **파일 저장** — **현재 작업 디렉토리**에 `{고객사명}_검수보고서_{YYYY-MM-DD}.md`로 저장
7. **PDF 변환** — 저장된 마크다운 보고서를 PDF로 변환
   이 스킬의 Base directory에 포함된 `report2pdf.py`를 사용합니다.
   ```bash
   PYTHONIOENCODING=utf-8 python "{이 스킬의 base directory}/report2pdf.py" "{보고서.md}" -o "{고객사명}_검수보고서_{YYYY-MM-DD}.pdf"
   ```

### 보고서 마크다운 포맷

```markdown
# 교안 검수 보고서

| 항목 | 내용 |
|------|------|
| 강의 | {lecture_title} |
| 고객사 | {client_name} |
| 검수일 | {YYYY-MM-DD} |
| 모델 | {model} |

## 요약

{summary}

| 심각도 | 건수 |
|--------|------|
| critical | N건 |
| warning | N건 |
| info | N건 |

## 지적 사항

### [{rule_id}] {severity} — {location}
- **페이지**: [{page_title}]({notion_url})
- **발췌**: {excerpt}
- **설명**: {description}
- **제안**: {suggestion}
```

> 지적 사항이 없으면 "지적 사항 없음 — 교안 품질이 양호합니다." 로 표기합니다.

## 자연어 해석 규칙

사용자가 자연어로 요청하면 아래 규칙에 따라 적절한 MCP 도구를 호출하세요.

**의도 판별:**
- "목록", "조회", "보여줘", "몇 개" → `lecture_search` 호출
- "상세", "내용", "본문", "마크다운" → `lecture_search`로 ID 확인 후 `lecture_detail` 호출
- "제안서", "proposal", "PDF" → `lecture_search`로 ID 확인 후 `lecture_proposals` 호출
- "교안", "workbook", "교육자료" → `lecture_search`로 ID 확인 후 `lecture_workbook` 호출
- "이미지 분석", "캡션", "이미지 설명" → `analyze_images` 호출
- "검수", "검사", "리뷰", "품질 확인" → **교안 검수 워크플로우** 실행 (위 섹션 참조)
- 의도가 불분명하면 `lecture_search`로 목록을 먼저 보여주세요

**키워드 매핑:**
- 회사명/교육명 언급 → `search` 파라미터
- 사람 이름 + "담당" → `manager` 파라미터
- 사람 이름 + "영업" → `sales` 파라미터
- 상태 관련 표현 → `status` 파라미터 (워크플로우 매핑 참조)
- 대상 언급 → `target`, 직무 → `job`, 툴 → `tool`, 주제 → `topic`, 상품 → `product`

### 상태값 워크플로우 (lecture_state)

```
① manager_assignment  매니저 배정
② client_call         고객사 컨택
③ draft_workbook      교안 초안
④ final_workbook      최종 교안
⑤ lecture_setting     교육 세팅
⑥ lecture_in_progress 교육 진행 중
⑦ lecture_finish      교육 종료
⑧ result_report       결과보고서
⑨ tax_invoice         세금계산서
※ lecture_stop        교육 중단 (예외)
```

### 자연어 → 상태 매핑 (lecture_state)

| 자연어 표현 | status 값 | 범위 |
|-------------|-----------|------|
| 완료, 종료, 끝난, 마무리 | `"lecture_finish,result_report,tax_invoice"` | ⑦⑧⑨ 전부 |
| 진행 중 | `"lecture_in_progress"` | ⑥만 |
| 준비 중, 진행 전, 교육 전 | `"manager_assignment,client_call,draft_workbook,final_workbook,lecture_setting"` | ①~⑤ 전부 |
| 교안 단계 | `"draft_workbook,final_workbook"` | ③④ |
| 매니저 배정, 담당자 배정 | `"manager_assignment"` | ①만 |
| 고객 연락, 영업 단계 | `"client_call"` | ②만 |
| 교안 초안, 워크북 작성 | `"draft_workbook"` | ③만 |
| 교안 완성, 최종 교안 | `"final_workbook"` | ④만 |
| 세팅 | `"lecture_setting"` | ⑤만 |
| 결과보고서, 결과 보고 | `"result_report"` | ⑧만 |
| 세금계산서, 정산 | `"tax_invoice"` | ⑨만 |
| 중단, 취소 | `"lecture_stop"` | 예외 |

### 자연어 → 타겟 매핑 (target_name)

| 자연어 표현 | target 값 |
|-------------|-----------|
| 실무자, 현업, 직원 | `"실무자"` |
| 신입, 신입사원 | `"신입사원"` |
| 임원, 직책자, 리더 | `"임원/직책자"` |
| 전사, 전직원, 전체 | `"전사"` |
| 고위 임원, C레벨, 사장 | `"고위급 임원"` |

### 자연어 → 직무 매핑 (job_name)

| 자연어 표현 | job 값 |
|-------------|--------|
| 사무직, 공통, 일반 | `"일반 사무직"` |
| 마케팅, 마케터, 홍보 | `"마케터"` |
| 엔지니어, 기술직 | `"엔지니어"` |
| 개발, 개발자 | `"개발"` |
| 연구, R&D, 연구직 | `"R&D/연구직"` |
| 인사, HR, 노무 | `"인사/노무(HR)"` |
| PM, PO, 기획 | `"PM/PO"` |
| 재무, 회계, 경리 | `"재무/회계"` |
| 디자인, 디자이너 | `"디자이너"` |

### 자연어 → 주제 매핑 (topic_name)

| 자연어 표현 | topic 값 |
|-------------|----------|
| AI 기초, 리터러시, AI 입문 | `"AI 리터러시 기초"` |
| 데이터, 데이터 분석, 분석 | `"데이터 분석"` |
| 이미지, 영상, 콘텐츠 제작 | `"이미지/영상 제작"` |
| 자동화, RPA, 업무 자동화 | `"업무 자동화"` |
| AI 심화, 고급 | `"AI 리터러시 심화"` |
| AI 리더십, 리더 | `"AI 리더십"` |
| 보안 | `"AI 보안"` |

### 자연어 → 툴 매핑 (using_tools_name)

| 자연어 표현 | tool 값 |
|-------------|---------|
| GPT, ChatGPT | `"ChatGPT"` |
| 엑셀, Excel, VBA | `"Excel VBA"` |
| 제미나이, Gemini | `"Gemini"` |
| 파이썬, Python | `"Python"` |
| 젠스파크, Genspark | `"Genspark"` |
| 소라, Sora | `"Sora"` |
| 런웨이, Runway | `"Runway"` |
| 미드저니, Midjourney | `"Midjourney"` |
| 클로드, Claude | `"Claude"` |
| 구글 워크스페이스 | `"google workspace"` |
| Copilot, 코파일럿 | `"Copilot"` |
| LangChain, 랭체인 | `"LangChain"` |
| N8N | `"N8N"` |
| Streamlit | `"Streamlit"` |
| Gradio | `"Gradio"` |
| 커서, Cursor | `"커서"` |

### 자연어 → 상품 매핑 (product)

| 자연어 표현 | product 값 |
|-------------|------------|
| 리터러시, AI Literacy | `"AI Literacy"` |
| PBL 라이트, 미니 PBL | `"PBL Lite"` |
| PBL 프로, PBL | `"PBL Pro"` (또는 `"PBL"`로 Lite+Pro 모두 매칭) |
| 세미나, 특강 | `"Seminar"` |
| 아카데미 해커톤 | `"Academy_해커톤"` |
| 아카데미 장기 | `"Academy_장기"` |
| 온라인 기존 | `"Online_기존"` |
| 온라인 제작 | `"Online_제작"` |

## 실행 후

1. 실행 결과를 사용자에게 보고하세요 (검색된 건수, 주요 필드 등)
2. 에러가 발생하면 에러 내용을 보고하세요
