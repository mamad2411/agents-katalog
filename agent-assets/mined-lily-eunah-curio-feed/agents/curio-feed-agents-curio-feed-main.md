# AGENTS.md / Project AI Guidelines

This is the single source of AI-assistant guidance for this repo. `CLAUDE.md`, `GEMINI.md` point here; Codex/Cursor read this file natively.

> 공통 작업 규율(git 워크플로·검증·시크릿·언어·PowerShell 인코딩)은 **전역 설정이 담당**한다 (`~/.claude/rules`, `~/.codex/AGENTS.md`, `~/.gemini/GEMINI.md`). 이 파일에는 **프로젝트 고유만** 둔다.

## Repository structure

Monorepo with three top-level directories:

```
backend/    Spring Boot 3.2 / Java 21 REST API
frontend/   React 18 + Vite + TypeScript + Tailwind (MVP shell only)
infra/      docker-compose.yml wiring all three services
```

백엔드 상세(명령·아키텍처·테스트·DB 마이그레이션)는 [`backend/AGENTS.md`](backend/AGENTS.md).

## Running locally

**Start the database** (required for backend):
```bash
cd infra && docker compose up -d db
```
Default connection: `postgres://curio:curio_password@localhost:5432/curio_feed`

**Backend** (from `backend/`):
```bash
./gradlew bootRun
```
Override DB connection: `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD`.

**Frontend** (from `frontend/`):
```bash
npm install
npm run dev      # dev server at http://localhost:5173
npm run build    # tsc + vite build
npm run lint     # eslint with zero-warnings policy
```

**Full stack via Docker** (from `infra/`):
```bash
docker compose up --build   # backend -> :8080, frontend -> :3000
```

## 프로젝트 도메인 규칙 (curio-feed 고유)

- **콘텐츠 품질 게이트 (fail-closed)** — 생성 콘텐츠는 검증 통과분만 발행. 저작권 안전: 원문 미복제, SOURCE_DIGEST(핵심 사실만) 재작성 + 제목 유사도(bigram Jaccard 0.30) 차단. CEFR-floor 어휘, 최근 기사 cross-article dedup.
- **LLM 비용/쿼터** — Gemini 무료 티어. 전역 rate limit(Semaphore, 15 RPM/4s 간격), 3층 캐시(DB sha256/run-memo/process)로 재생성 방지, 시험은 최저가 모델. 자동 재시도보다 수동.
- **provenance** — 재생성 가능한 산출물만 커밋 + 생성 방법을 코드/메타로 기록.
- **admin fail-closed** — `/api/admin/**`은 `X-Admin-Token`, 토큰 미설정 시 503.

## 유용한 skill

- 큰 스펙을 멀티-PR로 구현: `four-role-team`
- 중단된 세션 복구/도구 핸드오프: `handoff-recovery`
- UI 작업: `frontend-design`
