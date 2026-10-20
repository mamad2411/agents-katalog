# ProjectAI Backend (Kotlin + Spring Boot)

## 프로젝트 개요
AI 서비스의 Kotlin + Spring Boot 백엔드입니다.

## 기술 스택
- Kotlin 1.9.x / Spring Boot 3.x / Gradle (Kotlin DSL)
- Java 17 / PostgreSQL 15.8 / JPA

## 빠른 시작

```bash
./gradlew build          # 빌드
./gradlew bootRun        # 서버 실행
./gradlew test           # 테스트
./gradlew ktlintCheck    # 린트 검사
./gradlew ktlintFormat   # 린트 자동 수정
```

## 디렉토리 구조

```
src/main/kotlin/com/project/ai/
├── global/
│   ├── config/          # 설정 (DB, Security, Swagger 등)
│   ├── error/           # AppException, ErrorCode, GlobalExceptionHandler
│   ├── common/          # BaseResponse, 공통 유틸리티
│   └── middleware/      # 필터, 인터셉터
└── domain/
    └── {도메인명}/
        ├── controller/  # API 컨트롤러
        ├── service/     # 비즈니스 로직
        ├── dto/         # Request/Response DTO
        ├── entity/      # JPA 엔티티
        └── repository/  # JPA 리포지토리
```

## 상세 가이드

| 주제 | 위치 |
|------|------|
| 이슈 해결 전체 플로우 | `.claude/skills/fix-issue/` |
| 이슈 병렬 처리 (worktree) | `.claude/skills/parallel-issues/` |
| 엔지니어링 컨벤션 | `.claude/skills/engineering-conventions/` |
| TDD & Tidy First 원칙 | `.claude/skills/tdd-tidy-first/` |
| 코드 품질, 리뷰 체크리스트 | `.claude/skills/code-quality-guard/` |
| 보안 리뷰 | `.claude/skills/security-review/` |
| Kotlin 소스 규칙 | `.claude/rules/kotlin-src.md` |
| 테스트 규칙 | `.claude/rules/kotlin-tests.md` |
| API 설계 규칙 | `.claude/rules/api-design.md` |
