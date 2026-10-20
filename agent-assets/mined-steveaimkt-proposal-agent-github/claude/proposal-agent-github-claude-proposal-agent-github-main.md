# 제안서 자동 생성 에이전트 (v9.0)

입찰 제안서(RFP) + 마케팅 제안서 + 캠페인 브레인스토밍 통합 에이전트.
SPARK-6 프레임워크, S-E-P 설득 구조, **8-Step 팀 기반 파이프라인**.
**v9.0**: 출력 형식 분기 + 4개 병렬 리서치 + 7개 전문 QA + 캠페인 브레인스토밍.

---

## 제안서 유형

| 유형 | 입력 | 분석 대상 |
|------|------|---------|
| **입찰 제안서** | `제안요청서/테스트 XX/*.pdf` | RFP (제안요청서) |
| **마케팅 제안서** | PDF 또는 구두 브리핑 | 마케팅 플랜 |
| **캠페인 제안서** | `/brainstorm` → `campaign_brief.md` | 캠페인 브리프 |

---

## 제안서 팀 구성

- **PM (오케스트레이터)**: 단계 관리, 체크리스트, 컨펌 관리, 출력 형식 분기
- **분석팀**: Analyst (RFP/마케팅 분석)
- **리서치팀**: 4개 병렬 리서처 (시장환경 / 경쟁벤치마킹 / 타겟인사이트 / BP·KPI)
- **기획팀**: Planner = `script` 스킬 (SPARK-6 콘텐츠 기획)
- **디자인팀**: Design Analyzer (레퍼런스 분석) + Visualizer (도식화 전략)
- **제작팀**: Converter (JSON→HTML) + Designer (PPTX 직접 모드)
- **검수팀**: 7개 전문 QA (layout/shape/diagram/typography/color/content/interaction)
- **브레인스토밍팀**: Strategist + Creator + Data Analyst (캠페인 모드)

---

## 8-Step 파이프라인

| Step | 담당 | 출력 | 사용자 확인 |
|------|------|------|-----------|
| 0 | PM | **출력 형식 선택** (HTML→Figma / PPTX) | ✅ 선택 |
| 1 | 분석팀 | `rfp_analysis.md` 또는 `mkt_analysis.md` | ✅ 체크리스트+컨펌 |
| 2 | 리서치팀 | `research_brief.md` (4개 병렬 리서치 통합) | ✅ 체크리스트+컨펌 |
| 3 | 기획팀 | `proposal_script.md` | **★ 필수 승인** |
| 4 | 디자인팀 | `design_analysis.md` + `visualization_strategy.md` | ✅ 체크리스트+컨펌 |
| 5 | 제작팀 | `proposal_slides.json` + `preview.html` 또는 `.pptx` | ✅ 체크리스트+컨펌 |
| 6 | 검수팀 | QC 검수 리포트 (7개 전문 QA × 2라운드) | ✅ 수정여부 컨펌 |
| 7 | PM | 최종본 | ✅ 완료 컨펌 |

캠페인 모드: `/brainstorm` → `campaign_brief.md` 생성 시 **Step 1-2 건너뜀** → Step 3부터 시작.

---

## 핵심 개념

- **SPARK-6**: 6-Part 제안서 구조 (SPARK → PROBLEM→OPP → SOLUTION → EXECUTION → PROOF → RETURN)
- **S-E-P**: Story(공감) → Evidence(신뢰, 출처 필수) → Promise(행동 유도)
- **Win Theme**: Pain Point에 대응하는 3대 수주 전략 메시지, 모든 슬라이드에 태깅
- **Action Title**: Topic Title 금지, 인사이트+데이터 기반 문장형 (15~35자)
- **40종 레이아웃**: 기본 14 + 확장 14 + v3.0 추가 10종

---

## 커맨드 체계 (14종)

### 파이프라인 전체

| 커맨드 | 동작 |
|--------|------|
| `/start 테스트 XX` | 유형 + 출력 형식 선택 → 8-Step 전체 |
| `/p 테스트 XX` | 입찰 모드 고정, HTML→Figma 기본 (`--format pptx` 로 전환) |
| `/pf 테스트 XX` | HTML→Figma 모드 고정 |

### Step 단독 실행

| 커맨드 | Step | 동작 |
|--------|------|------|
| `/analyze 테스트 XX` | 1 | RFP·마케팅 플랜 분석 |
| `/research 테스트 XX` | 2 | 4개 병렬 리서치 |
| `/script 테스트 XX` | 3 | SPARK-6 콘텐츠 기획 ★필수 승인 |
| `/design 테스트 XX` | 4 | 레퍼런스 분석 + 도식화 전략 |
| `/convert 테스트 XX` | 5 | JSON 변환 + HTML 렌더링 |
| `/r 테스트 XX` | 6 | QC 검수 — 7개 전문 QA × 2라운드 |

### 보조

| 커맨드 | 동작 |
|--------|------|
| `/status 테스트 XX` | 진행 상황 확인 → 다음 Step 안내 (읽기 전용) |
| `/brainstorm 테스트 XX` | 캠페인 브레인스토밍 → `campaign_brief.md` |
| `/e 테스트 XX` | `proposal_script.md` 편집 (3뷰 분석) |
| `/run 테스트 XX` | PPTX 스크립트 실행 (PPTX 모드 전용) |
| `/open 테스트 XX` | 산출물 열기 |

모든 커맨드는 frontmatter(`description` / `argument-hint`)를 가진다.
새 커맨드를 추가하면 **이 표와 frontmatter를 함께** 갱신할 것.

---

## 스마트 시작

기존 산출물을 감지해 해당 Step부터 재개한다.

**정의는 `.claude/rules/smart-start.md` 한 곳에만 둔다.** 여기에 표를 복사하지 말 것 —
과거 4곳에 복붙돼 있다가 서로 어긋난 적이 있다.

---

## 폴더 규칙

- RFP/마케팅 플랜 입력: `제안요청서/테스트 XX/`
- 디자인 레퍼런스: `디자인 레퍼런스/` (PDF, JPG, PPTX)
- 출력: `output/테스트 XX/`
- 레거시/아카이브: `_archive/`

---

## GitHub 업로드 (⚠️ 기밀 주의)

공개 저장소: https://github.com/steveaimkt/proposal-agent-github

**이 프로젝트 폴더를 직접 GitHub에 올리지 말 것.** RFP 원문·디자인 레퍼런스·
생성 산출물·회사 프로필이 섞여 있다. 반드시 `_github/` 미러를 경유한다.

```bash
python3 sync_github.py          # 안전한 파일만 _github/ 로 동기화 + 안전검사
cd _github && git add -A && git commit -m "..." && git push
```

- `sync_github.py` 는 **화이트리스트 방식** — `ALLOW_DIRS`/`ALLOW_FILES` 에
  명시된 것만 복사한다. 새 폴더는 기본 제외이므로, 공개할 파일이 늘면
  화이트리스트에 직접 추가해야 한다.
- 자동으로 치환: `/Users/…` 개인 경로 → `<PROJECT_ROOT>`, 자사명 → `[자사명]`
- 안전검사에서 기밀 확장자(pdf/pptx/key/docx/hwp)·시크릿·개인정보가 걸리면
  **종료코드 1** 로 중단된다. 검사 실패 상태로 푸시 금지.
- `python3 sync_github.py --check` 로 복사 없이 검사만 가능.

**절대 업로드 금지**: `제안요청서/` · `디자인 레퍼런스/` · `output/` ·
`company_data/` · `input/` · `_archive/` · `.env` · `.claude/settings*.json`

---

## 상세 규칙 참조

규칙 상세는 `.claude/rules/` 에서 자동 로드:
- SPARK-6 구조 · 프로젝트 유형별 가중치 → `spark6-framework.md`
- S-E-P · Win Theme · Action Title → `components.md`
- 디자인 팔레트 · 타이포 · 레이아웃 → `design-style.md`
- 40종 레이아웃 JSON 스펙 · design_intent → `layouts.md`
- HTML→Figma 파이프라인 · 실행 방법 → `html-figma-mode.md`
- PPTX 모드 (slide_kit.py) → `pptx-rules.md` (경로 조건부 로드)
- 8-Step 체크리스트 (MUST/SHOULD/NICE) → `step-checklists.md`
- 스마트 시작 감지 순서 (단일 출처) → `smart-start.md`

도식화 패턴 40종 → `.claude/skills/visualizer/references/diagram-patterns.md`
