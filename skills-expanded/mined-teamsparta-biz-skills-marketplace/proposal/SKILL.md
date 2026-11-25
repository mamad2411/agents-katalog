---
name: proposal
description: 컨설턴트 인터뷰 → 커리큘럼 JSON 생성 → 제안서 PPTX 자동 생성 파이프라인을 실행한다.
argument-hint: [고객사명]
metadata:
  version: "1.0.0"
---

## 영향 폴더

| 폴더 | 역할 |
|------|------|
| CWD | curriculum.json 생성, PPTX 결과물 저장 |

## 입력

고객사명: $ARGUMENTS

예시:
- `/proposal 삼성전자` → "삼성전자" 고객 대상 제안서 생성
- `/proposal` → 고객사명을 인터뷰에서 수집

## 사전 조건

- `proposal-pipeline` 패키지가 설치되어 있어야 한다
  - 설치: `pip install "git+https://github.com/teamsparta-biz/proposal-pipeline.git#egg=proposal-pipeline[visual]"`
  - 브라우저: `proposal-install-browsers` (최초 1회)
- `.env` 파일에 `GAMMA_API_KEY` 설정 (Gamma 설득 파트 사용 시, 선택)

## 실행 단계

### 1단계: 인터뷰 (AskUserQuestion 3라운드)

**라운드 1 — 기본 정보:**
AskUserQuestion으로 다음을 수집한다:
- 고객사명 ($ARGUMENTS로 이미 있으면 스킵)
- 교육 상품/주제 (예: "Midjourney 비주얼 AI", "RAG 에이전트 구축")
- 대상 직무/부서
- 총 교육 시간

**라운드 2 — 교육 설계:**
- 사용 툴/기술 스택
- 실습 케이스 (구체적 산출물)
- 제한사항/금지사항 (예: "코딩 없음", "비개발자 대상")

**라운드 3 — 설득 파트:**
- 고객 산업
- 현재 페인포인트
- 교육 목표/기대효과
- PBL 포함 여부

### 2단계: 커리큘럼 JSON 생성

수집한 정보를 바탕으로 `curriculum_schema.md` 규칙에 따라 커리큘럼 JSON을 생성한다.

**스키마 규칙 요약 (반드시 준수):**

- `id`: kebab-case 영문
- `name`: 한글 과정명
- `total_hours`: "N시간" — rows의 hours 합계와 반드시 일치
- `table_pages`: 4행 기준 자동 분할 (4행 이하=1페이지, 5~8행=2페이지, ...)
- `rows[].subject`: 15자 내외
- `rows[].hours`: 0.5시간 단위, 합계 = total_hours
- `rows[].content`: "• " bullet point 3~4개, 각 40~80자, 구체적 실무 내용
- `rows[].exercise`: 구체적 산출물 명시 ("~제작", "~제출")
- `design_bg.purpose`: HTML 태그 허용 (`<strong>`, `<span class="highlight">`, `<br>`)
- `design_bg.steps`: 3~4단계 (이해→학습→설계→실전), title 2~4자, subtitle 영문 1단어
- `persuasion_slides`: 5종 (gap_analysis → solution → framework → roadmap → roi)

**생성할 파일:** CWD에 `curriculum.json` 저장

### 3단계: 설득 파트 5종 콘텐츠 생성

인터뷰에서 수집한 고객 정보를 바탕으로 persuasion_slides 5종을 생성한다:

1. **gap_analysis** — To-Be(4항목) / As-Is(4항목) / Gap(4항목) + summary
2. **solution** — 2~3단계 stages + 2~3개 principles
3. **framework** — objectives, highlights, deliverables, tools, keywords
4. **roadmap** — 3~4 phases (period, activities 포함)
5. **roi** — 3~4개 value cards (icon, metric, title, description)

JSON 배열의 첫 번째 모듈 객체에 `persuasion_slides` 키로 포함한다.

### 4단계: 사용자 확인

생성된 JSON을 사용자에게 보여주고 수정 사항을 확인한다:
- 커리큘럼 구성 (주제, 시간 배분)
- 설득 파트 내용
- 수정이 있으면 JSON을 업데이트

### 5단계: 파이프라인 실행

확인된 JSON으로 `proposal-generate` CLI를 실행한다:

```bash
cd [작업 디렉토리]
PYTHONIOENCODING=utf-8 proposal-generate \
  --customer "[고객사명]" \
  --title "[교육 제목]" \
  --curriculum-json curriculum.json \
  --output-dir ./output
```

### 6단계: 결과 보고

- 생성된 PPTX 파일 경로
- 슬라이드 수 (고정/동적)
- 에러 여부

## 결과 형식

```
제안서 생성 완료
- 파일: output/[팀스파르타] 삼성전자 제안서.pptx
- 슬라이드: 13장 (고정 12 + 동적 0)
- 커리큘럼 JSON: curriculum.json
```
