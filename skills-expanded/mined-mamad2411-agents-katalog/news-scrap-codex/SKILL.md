---
name: news-scrap-codex
description: Codex용 응급의료 AI 주간 뉴스 브리핑 스킬. Use when creating a Korean weekly emergency-medicine AI news briefing from verified domestic and overseas articles, running a required NotebookLM gate, selecting one featured article, and generating the final slide deck with NotebookLM slide-deck instead of python-pptx.
---

# 응급의료 AI 뉴스 브리핑 for Codex

모든 출력은 한국어로 작성한다.

## 언제 이 스킬을 쓰는가

- 주간 응급의료 AI 기사 브리핑을 만들어야 할 때
- 국내/해외 기사 검증 후 `verified_articles.json`을 기준점으로 삼을 때
- 논문보다 기사, 현장 도입, 운영 개선, 제품 통합/제휴 중심으로 수집해야 할 때
- NotebookLM을 필수 게이트로 써야 할 때
- 최종 슬라이드를 `python-pptx`가 아니라 NotebookLM `slide-deck`로 생성해야 할 때

## 핵심 규칙

- 이 작업은 최신 기사에 의존하므로 기사 수집 단계에서는 반드시 웹 검색과 검증을 사용한다.
- 국내 기사가 비어 보이면 바로 `0건`으로 확정하지 말고, `필수 도메인 순회`와 `119/구급/응급실 운영/병상/문서화 축 보조 검색`을 먼저 수행한다.
- 기본 수집은 기사 중심이다. 논문/프리프린트는 사용자가 명시적으로 요청할 때만 보조 후보로 포함한다.
- `트리아지`는 제외하지 않지만, 검색 단계에서 EMS/ePCR/911, 응급실 운영, 문서화, 병상·환자흐름, 상황관제, 제품 통합/상용화 축을 함께 수집한다.
- NotebookLM 단계가 실패하면 전체 작업을 실패로 간주한다.
- 새 실행마다 새 NotebookLM 노트를 만든다.
- 최종 슬라이드는 [references/slide_prompt.md](references/slide_prompt.md)의 5장 구조와 디자인 가이드를 따른다.
- 기본 경로는 `verified_articles.json -> notebook_manifest.json -> notebooklm_outputs.json -> slide_deck_artifact.json`이다.
- HTML 대시보드도 기본 산출물이다.
- 기본 슬라이드 생성 경로에서 `python-pptx`는 사용하지 않는다.

## 입력 기준

- 권장 입력: `verified_articles.json`
- 이 파일이 없으면 Codex가 먼저 기사 수집, 중복 제거, 원문 검증을 수행해 같은 스키마로 고정한다.
- 기사 수집 규칙과 건수 상한은 [references/search-rules.md](references/search-rules.md)를 따른다.
- 논문을 포함해야 할 때만 `build_search_queries.py --include-papers`를 사용한다.
- 영문 기사 제목은 가능하면 `번역제목`과 `원제목`을 함께 저장하고, HTML은 `번역제목`을 우선 노출한다.
- 스키마는 [references/output-contracts.md](references/output-contracts.md)를 따른다.

## 실행 순서

1. 기사 범위를 계산한다.
2. `python scripts/build_search_queries.py --start-date YYYY-MM-DD --end-date YYYY-MM-DD --format json --output <run_dir>/search_queries.json`으로 주차별 검색 세트를 만든다.
3. broad query, site-pass query, 수동 URL 목록 중 하나로 raw search hit JSON 또는 URL 목록을 준비한다.
4. `python scripts/scan_candidates.py <input_json> --start-date YYYY-MM-DD --end-date YYYY-MM-DD --output <run_dir>/candidates_raw.json`로 정규화한다.
5. `candidates_raw.json`의 후보 URL을 `python scripts/extract.py`로 검증한다.
6. 검증된 기사만으로 `verified_articles.json`을 준비한다.
7. `python scripts/freeze_verified_articles.py <verified_json>`로 기사 순서와 건수 상한을 고정한다.
8. `python scripts/build_notebook_sources.py <verified_json> <run_dir>`를 실행한다.
9. `python scripts/notebooklm_gate.py <run_dir>/notebook_manifest.json --output-dir <run_dir>`를 실행한다.
10. `python scripts/render_dashboard.py <verified_json> <run_dir>/notebooklm_outputs.json <run_dir>/news_<week_id>.html <run_dir>/featured_article.json`를 실행한다.
11. `python scripts/notebooklm_slide_deck.py <run_dir>/notebooklm_outputs.json <verified_json> --output-dir <run_dir>`를 실행한다.
12. 결과물이 템플릿에서 벗어나면 `notebooklm_slide_deck.py`를 다시 실행하거나 NotebookLM `revise-slide`를 추가 적용한다.

## 무엇을 읽을지

- 전체 단계와 실패 규칙: [references/workflow.md](references/workflow.md)
- 기사 검색/선정 고정 규칙: [references/search-rules.md](references/search-rules.md)
- 슬라이드 프롬프트와 수정 규칙: [references/slide_prompt.md](references/slide_prompt.md)
- 출력 파일 계약: [references/output-contracts.md](references/output-contracts.md)

## 포함 스크립트

- `scripts/build_search_queries.py`
  기간별 핵심 검색어, 보조 검색어, 필수 도메인 site-pass 쿼리를 생성한다.
- `scripts/scan_candidates.py`
  raw search hit 또는 URL 목록을 `candidates_raw.json` 형식으로 정규화하고 노이즈 도메인을 제거한다.
- `scripts/extract.py`
  후보 URL에서 본문과 발행일을 일괄 추출해 검증 단계에 사용한다.
- `scripts/freeze_verified_articles.py`
  기사 중복 제거, 점수화, 정렬, 섹션별 건수 상한 적용을 수행한다.
- `scripts/build_notebook_sources.py`
  `verified_articles.json`에서 NotebookLM 업로드용 텍스트와 manifest를 만든다.
- `scripts/notebooklm_gate.py`
  새 노트를 만들고 소스를 업로드한 뒤 Q0~Q6 분석 결과를 저장한다.
- `scripts/render_dashboard.py`
  `verified_articles.json`과 `notebooklm_outputs.json`에서 주간 HTML 대시보드를 만든다.
- `scripts/notebooklm_slide_deck.py`
  대표 기사를 선택하고 NotebookLM `slide-deck` 생성, `revise-slide`, PPTX/PDF 다운로드를 수행한다.
