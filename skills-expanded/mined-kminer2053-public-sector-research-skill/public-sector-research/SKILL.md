---
name: public-sector-research
description: Evidence-first public-sector research with official-source planning, bounded collection, passage-level citations, explainable scoring, local SQLite memory, and readable Korean Markdown plus interactive HTML reports. Use when an agent must investigate laws, government policy, public services, procurement, privacy, standards, evaluation, strategy, or institutional guidance while preserving reviewable source snapshots and separating verified facts, inference, recommendations, gaps, and failures.
---

# 공공복리 · BOKRI

공공복리(복리)는 공공업무 질문을 바로 요약하지 않고, 공식 원문을 확보한 뒤 근거 구간과 한계를 검토 가능한 형태로 남긴다. 이 Skill은 특정 AI 서비스의 검색 기능에 종속되지 않는다. 호스트가 제공하는 웹 검색·브라우저·커넥터로 공식 출처를 찾고, bundled Python CLI로 계획·수집·저장·점수화·보고서 생성을 수행한다.

## 실행 진입점

Skill 폴더의 `scripts/psr.py`를 사용한다.

```bash
python3 <skill-directory>/scripts/psr.py --version
```

설치형 CLI가 있으면 같은 계약의 `psr` 명령을 사용해도 된다.

## 기본 워크플로

1. 사용자의 업무 목적, 기준일, 관할, 산출물을 확인한다.
2. 프로젝트에 `.psr/`가 없으면 로컬 저장소를 초기화한다.
3. `research plan`을 실행하고 생성된 `plan.json`의 활성 track을 검토한다. 질문과 무관한 track은 `--exclude-track`, 반드시 필요한 track은 `--include-track`으로 조정한다.
4. 각 track의 query와 preferred domain을 사용해 공식 원문을 우선 탐색한다.
5. 선택한 출처를 JSONL manifest에 기록한다. 출처 등급을 추측하지 말고 확인 가능한 범위에서 지정한다.
6. `research run`으로 출처를 병렬 수집·파싱하고 보수적인 초안 보고서를 생성한다.
7. `result.json`의 citation을 검토한 뒤 [reporting.md](references/reporting.md)에 따라 `brief.json`을 작성한다.
8. `report build --brief-file <path> --format all`로 Markdown과 HTML을 함께 생성한다.
9. `PARTIAL`, gap, failure, 발행일 미확인, `UNVERIFIED_WEB` 항목을 먼저 검토한다.
10. 사용자에게 핵심 내용과 함께 HTML·Markdown 경로, 핵심 citation ID, 공식 원문 미확보 범위를 알린다.

## 빠른 시작

```bash
python3 <skill-directory>/scripts/psr.py project init . --name "AI 구매원칙"

python3 <skill-directory>/scripts/psr.py --project . research plan \
  "공공기관 생성형 AI 구매 시 데이터 권리와 업체 종속 방지 원칙을 조사하라"
```

계획 출력의 `run_id`와 query를 사용해 출처를 찾은 뒤 `sources.jsonl`을 만든다.

```json
{"track_id":"law-regulation","url":"https://official.example/law","title":"공식 법령","publisher":"공식기관","source_tier":"OFFICIAL_PRIMARY","published_at":"2026-01-01"}
{"track_id":"privacy","url":"https://official.example/privacy.pdf","title":"개인정보 안내서","publisher":"공식기관","source_tier":"OFFICIAL_PRIMARY","published_at":"2025-08-07"}
```

```bash
python3 <skill-directory>/scripts/psr.py --project . research run <run-id> \
  --sources-file sources.jsonl
```

## 재사용과 오프라인 작업

동일 출처의 최근 snapshot은 기본 7일 동안 재사용한다. 최신성 확인이 필요하면 `--refresh`를 사용한다.

```bash
python3 <skill-directory>/scripts/psr.py --project . memory search "학습 재사용"
python3 <skill-directory>/scripts/psr.py --project . evidence list --run-id <run-id>
python3 <skill-directory>/scripts/psr.py --project . report build <run-id> \
  --brief-file brief.json --format all
```

네트워크 접근이 없으면 기존 Evidence Memory를 먼저 검색하고, 새 원문을 확인하지 못했다는 사실을 결과에 표시한다.

## 판단 원칙

- 법령·정부·공공기관·국제표준·학술 원문을 우선한다.
- 검색 결과 페이지, 기사, 블로그가 원문을 재인용하면 원 출처를 별도로 찾는다.
- `OFFICIAL_PRIMARY`는 발행 주체와 원문성을 확인한 경우에만 사용한다.
- 사실은 citation passage가 직접 지지하는 범위까지만 표현한다.
- 출처에 없는 해석은 `INFERENCE`, 정책 제안은 `RECOMMENDATION`으로 별도 표시한다.
- `FACT`와 `INFERENCE`는 하나 이상의 유효한 citation ID에 연결한다.
- 메뉴·푸터·쿠키·로그인 등 페이지 공통 문구를 업무 근거로 채택하지 않는다.
- 로그인, CAPTCHA, paywall, 접근제한을 우회하지 않는다.
- robots.txt의 명시적 차단을 우회하지 않는다.
- 보고서를 자동 법률판단이나 최종 결재자료로 표현하지 않는다.

## 필요한 참고자료

- 전체 실행 순서와 복구: [workflow.md](references/workflow.md)
- 출처 등급과 Evidence Score: [evidence-policy.md](references/evidence-policy.md)
- source manifest 계약: [source-manifest.md](references/source-manifest.md)
- Research Profile 확장: [research-profiles.md](references/research-profiles.md)
- 한국어 Markdown·HTML 보고서와 `brief.json`: [reporting.md](references/reporting.md)
- Codex·Claude·기타 호스트 사용: [portability.md](references/portability.md)
