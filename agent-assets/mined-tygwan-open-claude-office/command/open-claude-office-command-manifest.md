# Command Manifest

> Compact routing index for 15 slash commands. Load individual command files only when matched.

## Craft Pipeline Commands (8)

| Command | Keywords (KO) | Keywords (EN) | Purpose |
|---------|--------------|---------------|---------|
| /craft | 파이프라인, 포트폴리오, 전체 빌드 | craft, pipeline, portfolio, full build | 전체 파이프라인 실행 (Phase 1→2→3→4) |
| /craft-analyze | 분석, Phase 1, 코드 분석 | analyze, phase 1, code analysis | Phase 1만 실행 (3 agents → Markdown) |
| /craft-design | 디자인, Phase 2, 프로파일 | design, phase 2, profile | Phase 2만 실행 (Markdown → design-profile.yaml) |
| /craft-preview | 미리보기, 로컬 빌드, 서빙 | preview, local build, serve | 로컬 빌드 + 서빙 |
| /craft-deploy | 배포, 디플로이, GitHub Pages | deploy, publish, github pages, vercel | 배포 (GitHub Pages / Vercel / Netlify) |
| /craft-sync | 포트폴리오 동기화, 데이터 연동 | portfolio sync, data sync | 메인 포트폴리오와 데이터 동기화 |
| /craft-state | 상태, 인스펙트, 리셋, 재개 | state, inspect, reset, resume, pause | 프로젝트 상태 조회/제어 |
| /craft-export | 내보내기, 익스포트 | export, resumely | 프로젝트 데이터 내보내기 |

## Dev Lifecycle Commands (6)

| Command | Keywords (KO) | Keywords (EN) | Purpose |
|---------|--------------|---------------|---------|
| /feature | 기능 개발, 피처, 워크플로우 | feature, develop, workflow | 기능 개발 워크플로우 (Phase + Sprint + Git + 문서) |
| /bugfix | 버그 수정, 버그픽스, 이슈 | bugfix, bug fix, issue fix | 버그 수정 워크플로우 (이슈 분석 → 수정 → PR) |
| /release | 릴리스, 버전, 배포 | release, version, publish, tag | 릴리스 관리 (버전 관리 + 문서 정리 + 배포) |
| /phase | 단계, 페이즈, 진행률 | phase, stage, progress | Phase 상태 확인/전환/진행률 |
| /dev-doc-planner | 문서 계획, PRD, 설계서 | doc plan, PRD, tech spec | 문서 계획 (PRD, TECH-SPEC, PROGRESS 템플릿) |
| /git-workflow | 깃 워크플로우, 커밋 컨벤션 | git workflow, commit convention, branch | Git 워크플로우 관리 |

## Integration Commands (1)

| Command | Keywords (KO) | Keywords (EN) | Purpose |
|---------|--------------|---------------|---------|
| /notion | 노션, 동기화, 프로젝트 관리 | notion, sync, push, pull, status | Notion 양방향 동기화 |
