# AGENTS.md (backend)

Backend-specific guidance for AI coding assistants (Antigravity, Gemini, Codex, Claude Code). Repo-wide overview + 프로젝트 도메인 규칙: root [`AGENTS.md`](../AGENTS.md). 공통 작업 규율(git·검증·시크릿·언어)은 전역 설정이 담당.

## Commands

**Build:** `./gradlew build`

**Run tests (all):** `./gradlew test`

**Single test class / method:**
```bash
./gradlew test --tests "com.curiofeed.backend.domain.repository.ArticleFeedRepositoryTest"
./gradlew test --tests "com.curiofeed.backend.domain.repository.ArticleFeedRepositoryTest.shouldReturnOnlyPublishedArticles"
```

**Run** (requires PostgreSQL at `localhost:5432`): `./gradlew bootRun`
Override DB via env: `SPRING_DATASOURCE_URL`, `SPRING_DATASOURCE_USERNAME`, `SPRING_DATASOURCE_PASSWORD`.

## Architecture

Spring Boot 3.2 + Java 21 backend for a news/article platform. PostgreSQL with Flyway migrations. Admin endpoints (`/api/admin/**`) are secured with a **fail-closed `X-Admin-Token` interceptor** (returns 503 when the token is unset).

**Package layout:**
```
com.curiofeed.backend
├── api
│   ├── controller/          # REST controllers + GlobalExceptionHandler
│   └── dto/                 # Request/response DTOs
├── config/                  # JpaConfig (enables JPA auditing)
└── domain
    ├── entity/              # JPA entities
    ├── model/               # Non-entity domain models (QuizSubmission, QuizOptions, etc.)
    ├── repository/          # Spring Data JPA repositories
    └── service/             # Business logic (interfaces + impls)
```

**API endpoints:**
- `GET /api/articles?cursor=&size=10` — cursor-based feed
- `GET /api/articles/{id}?level=EASY` — article detail with difficulty level
- `POST /api/articles/{articleId}/contents/{contentId}/quizzes/{quizId}/attempt` — quiz attempt

**Core domain model:** `Article` → `ArticleContent` (one per `DifficultyLevel`: EASY/MEDIUM/HARD) → `Vocabulary` + `Quiz`. The detail endpoint selects one `ArticleContent` by `DifficultyLevel` and loads its vocabularies and quizzes in the same query.

**AI generation pipeline:** `ArticleGenerationJob` (one per article) → `ArticleGenerationSubJob` (one per difficulty level, unique constraint on `job_id + level`). `JobStatus`: PENDING → PROCESSING → COMPLETED/FAILED. Sub-jobs track `retryCount` and `lastHeartbeatAt`. Steps SOURCE_DIGEST → CONTENT → VOCABULARY → QUIZ are independently retriable.

**Cursor-based pagination:** token `{publishedAt ISO string}_{uuid}`, ordering `published_at DESC, id DESC`. UUID v7 (time-ordered) makes `id` tie-breaking stable. The feed query fetches `size + 1` rows to determine `hasNext`.

**Quiz evaluation:** `Quiz.evaluate(QuizSubmission)` handles `MULTIPLE_CHOICE` (match by `choiceId`), `SHORT_ANSWER` (normalized text), `SCRAMBLE` (join list/text, normalized). Normalization strips trailing punctuation and collapses whitespace. `QuizOptions` is stored as JSONB.

## Testing

All tests use **Testcontainers** (`postgres:16-alpine`) — no in-memory DB. Docker must be running.

Required annotations on every repository/integration test:
```java
@DataJpaTest
@Testcontainers
@ActiveProfiles("test")
@AutoConfigureTestDatabase(replace = AutoConfigureTestDatabase.Replace.NONE)
@Import(JpaConfig.class)  // needed for @CreatedDate / @LastModifiedDate auditing
```
Entities use `@NoArgsConstructor(access = AccessLevel.PROTECTED)` with no public setters, so tests build entities via reflection helpers (`newInstance` + `setField` walking the class hierarchy). See `ArticleFeedRepositoryTest`.

## Database Migrations

Flyway migrations live in `src/main/resources/db/migration/`. Always add a new `V{n}__description.sql` — never edit existing migrations. Schema uses `TIMESTAMP WITH TIME ZONE` throughout; Java side uses `Instant`. Key pagination index: `idx_articles_status_published_at` on `(status, published_at DESC, id DESC)`.
