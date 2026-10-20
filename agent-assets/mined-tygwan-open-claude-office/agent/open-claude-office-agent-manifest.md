# Agent Manifest

> Compact routing index for 47 agents. Load individual agent files only when matched.

| Agent | Keywords (KO) | Keywords (EN) | Purpose |
|-------|--------------|---------------|---------|
| progress-tracker | 진행상황, 진척, 완료율, 진행률, 현황 | progress, status, completion, remaining | Phase+Sprint 통합 진행률 추적 |
| phase-tracker | phase, 단계, 페이즈, 단계 전환 | phase, current phase, next phase, phase transition | Phase별 진행 추적, 전환, 체크리스트 검증 |
| dev-docs-writer | 개발 문서, 문서 생성, PRD, 기술 설계, 설계서 | create docs, documentation, spec, tech spec, write docs | DISCOVERY.md 기반 PRD/TECH-SPEC/PROGRESS/CONTEXT 생성 |
| project-discovery | 프로젝트 시작, 새 프로젝트 | /init --full, /init --discover | 대화 기반 프로젝트 요구사항 파악 → DISCOVERY.md |
| doc-splitter | 문서 분할, phase 구조 | document, split, phase structure, organize | Phase 폴더/문서 구조 생성 |
| github-manager | 이슈, CI, 워크플로우, 릴리스, 액션 | github, gh, issue, CI, workflow, release, actions | gh CLI 기반 이슈/PR/CI/CD/릴리스 관리 |
| analytics-reporter | 통계, 사용량, 성과, 리포트, 메트릭 | analytics, metrics, statistics, report, usage | Agent/Skill 사용 통계 CLI 시각화 |
| config-validator | 설정 검증 | config check, validate | settings.json/hooks/agents/skills 검증 |
| commit-helper | 커밋, 커밋해, 변경사항 저장 | commit, commit message, save changes, staged | Conventional Commits 커밋 메시지 작성 |
| pr-creator | PR, PR 생성, 풀리퀘, 머지 요청 | PR, pull request, merge request, create PR | PR 생성 및 설명 작성 |
| branch-manager | 브랜치, 브랜치 생성, 브랜치 삭제 | branch, checkout, switch, remote, fetch, push | GitHub Flow 브랜치/Remote 관리 |
| code-reviewer | 리뷰, 코드 리뷰, 검토, 코드 확인 | review, PR review, audit, check code, inspect | 코드 품질/보안/성능/컨벤션 리뷰 |
| test-helper | 테스트, 테스트 작성, 커버리지 | test, unit test, coverage, TDD, jest, pytest | 단위/통합/E2E 테스트 작성 보조 |
| refactor-assistant | 리팩토링, 코드 개선, 중복 제거 | refactor, clean up, restructure, simplify, DRY, SOLID | 코드 구조 개선, 디자인 패턴 적용 |
| git-troubleshooter | 충돌, git 에러, 복구, 되돌려 | conflict, revert, reset, undo, rollback, git error | Git 충돌 해결, 히스토리 복구, 문제 진단 |
| doc-generator | README, API 문서, 사용자 가이드 | README, API docs, user guide | 기술/사용자 문서 생성 |
| doc-validator | 문서 검증, 완성도, 품질 체크 | doc validation, completeness, quality check | 문서 완성도 검증, 누락 확인 |
| readme-helper | README, 리드미, 배지 | readme, badge, documentation, project intro | README 작성/개선, 배지 생성 |
| agent-writer | 에이전트 작성, agent 생성 | create agent, write agent, agent template | Agent 작성, Frontmatter 검증, 트리거 제안 |
| project-analyzer | 프로젝트 분석, 구조 분석, 기술 스택 | analyze project, project structure, tech stack, architecture | 프로젝트 구조/기술스택/패턴 분석 |
| prd-writer | PRD, 요구사항, 기능 정의 | PRD, requirements, user story | PRD(제품 요구사항 문서) 전문 작성 |
| tech-spec-writer | 기술 설계, API 설계, 데이터 모델 | tech spec, architecture, API design, data model | 기술 설계서 전문 작성 |
| work-unit-manager | 세션, 그룹화, 작업 단위 | work unit, session, changes, grouping | 세션 변경사항 추적, 원자적 커밋 단위 제안 |
| file-explorer | 파일 분석, 정리, .gitignore | file analysis, cleanup, .gitignore | 프로젝트 파일 구조 분석, 불필요 파일 식별 |
| google-searcher | 검색, 찾아봐, 구글 | search, google, find | 웹 검색 및 기술 정보 수집 |
| experience-interviewer | 경험 인터뷰, 6블록, 의사결정, 판단 기준 | experience, interview, 6-block, decision rule, gap analysis | Phase 1 갭 분석 후 사용자 인터뷰 |
| code-analyst | 코드 분석, 아키텍처 | code analysis, architecture, metrics | Phase 1 코드 아키텍처 분석 (Codex) |
| story-analyst | 내러티브, 스토리, 마일스톤 | narrative, story, milestone, impact | Phase 1 프로젝트 내러티브 추출 |
| stack-detector | 스택 감지, 프레임워크 | stack, framework, template, detect | Phase 1 프레임워크 감지, 템플릿 추천 (Codex) |
| design-agent | 디자인, 팔레트, UI, 레이아웃 | design, palette, UI, visual, layout | Phase 2 디자인 프로파일 생성 (Gemini) |
| page-writer | 사이트, 빌드, 페이지, 콘텐츠 | site, build, page, content, tokens | Phase 3 사이트 빌드, content.json 생성 |
| figure-designer | 다이어그램, SVG, 시각화 | diagram, figure, mermaid, SVG | Phase 3 Mermaid/SVG 시각화 (Gemini) |
| validation-agent | 검증, 스키마, 품질, 빌드 검증 | validate, schema, quality, build check | Phase 3.5 빌드 검증 (Codex) |
| scaffolder | 프로젝트 구조, 스캐폴딩, 초기 설정 | scaffold, project structure, boilerplate, setup | MVP/PoC/Prod 단계별 프로젝트 구조 생성 |
| api-designer | API 설계, 엔드포인트, OpenAPI | API design, endpoint, OpenAPI, REST, route | API 엔드포인트 설계 및 OpenAPI spec |
| db-architect | DB 설계, 스키마, 마이그레이션, ERD | database, schema, migration, ERD, prisma | DB 스키마 설계, 마이그레이션, ERD |
| auth-builder | 인증, 인가, 로그인, JWT, OAuth | auth, authentication, authorization, JWT, OAuth, login | 인증/인가 시스템 구축 |
| container-builder | 도커, 컨테이너, K8s | docker, container, kubernetes, k8s, compose | Docker/K8s 컨테이너 환경 구축 |
| ci-generator | CI/CD, 파이프라인, 깃허브 액션 | CI, CD, pipeline, GitHub Actions, workflow | GitHub Actions CI/CD 파이프라인 |
| env-manager | 환경변수, 시크릿, .env | env, environment, secret, .env, config | 환경변수/Secret 관리 |
| security-scanner | 보안 검사, 취약점, SAST | security scan, vulnerability, SAST, DAST, audit | 보안 취약점 검사 및 자동 수정 |
| test-strategist | 테스트 전략, 커버리지 계획 | test strategy, coverage plan, test plan | 단계별 테스트 전략 수립 |
| lint-configurator | 린트, ESLint, Prettier, 코드 포맷 | lint, ESLint, Prettier, format, TypeScript strict | ESLint/Prettier/TypeScript 설정 |
| lifecycle-gate | 게이트, 단계 전환, 승격 | gate, stage transition, promote, MVP to PoC | MVP→PoC→Prod 게이트 검증 |
| migration-planner | 마이그레이션, 전환 계획, 업그레이드 | migration, upgrade, transition plan | 전환 시 기술 마이그레이션 계획 |
| observability-configurator | 모니터링, 알림, 로그, APM, 메트릭 | monitoring, alerting, logging, APM, observability, grafana, prometheus | 모니터링/로깅/알림 시스템 설정 |
| incident-manager | 장애, 인시던트, 핫픽스, 롤백, 복구 | incident, hotfix, rollback, recovery, outage, postmortem | 장애 대응, 핫픽스, 포스트모템 관리 |
