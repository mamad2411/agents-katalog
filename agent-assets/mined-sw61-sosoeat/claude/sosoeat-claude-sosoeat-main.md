# 소소잇 프로젝트

## 기술 스택

- **프레임워크**: Next.js (App Router), TypeScript
- **스타일링**: Tailwind CSS v4
- **상태 관리**: Zustand (전역), TanStack Query (서버 상태)
- **테스트**: Jest
- **애니메이션**: framer-motion, tailwind
- **React Compiler 1.0 사용 중** — 기본적으로 `useMemo`, `useCallback` 불필요 (필요 시 사유를 명시하여 사용 가능)

## 주요 명령어

```bash
npm run dev          # 개발 서버 (localhost:3000)
npm run build        # 프로덕션 빌드
npm run lint         # ESLint 검사
npm run type-check   # TypeScript 타입 체크
npm run format       # Prettier 포맷팅
npm run test         # 전체 단위 테스트
npm run test:coverage # 커버리지 리포트
npm run storybook    # Storybook (localhost:6006)
npm run validate     # 타입 + 포맷 + Lint + 테스트 자동 실행
```

---

## 📚 개발 가이드

모든 개발 규칙과 컨벤션은 아래 문서를 참고하세요:

- 📋 **[프로젝트 컨벤션](./docs/CONVENTION.md)** — 명명, FSD 규칙, TanStack Query, 테스트 가이드
- 🏗️ **[프로젝트 구조 & FSD](./docs/architecture.md)** — 폴더 구조, 레이어 규칙, 슬라이스 구조
- 🔌 **[API 패턴 & BFF](./docs/api-patterns.md)** — HTTP 클라이언트, 인증, 프록시
- 📝 **[Git 워크플로우](./docs/git-workflow.md)** — 커밋 메시지, Pre-commit 훅, 브랜치 전략

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:

- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current

## Skill routing

When the user's request matches an available skill, ALWAYS invoke it using the Skill
tool as your FIRST action. Do NOT answer directly, do NOT use other tools first.
The skill has specialized workflows that produce better results than ad-hoc answers.

Key routing rules:

- Product ideas, "is this worth building", brainstorming → invoke office-hours
- Bugs, errors, "why is this broken", 500 errors → invoke investigate
- Ship, deploy, push, create PR → invoke ship
- QA, test the site, find bugs → invoke qa
- Code review, check my diff → invoke review
- Update docs after shipping → invoke document-release
- Weekly retro → invoke retro
- Design system, brand → invoke design-consultation
- Visual audit, design polish → invoke design-review
- Architecture review → invoke plan-eng-review
- Save progress, checkpoint, resume → invoke checkpoint
- Code quality, health check → invoke health
