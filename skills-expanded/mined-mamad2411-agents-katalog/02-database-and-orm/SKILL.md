# Database & ORM — PerfectJob

> PostgreSQL 17 + pgvector, Spring Data JPA, Hibernate 6, Flyway migrations.

## Description

PerfectJob uses PostgreSQL 17 as its primary database with pgvector extension for vector similarity search. The ORM layer is Spring Data JPA with Hibernate 6. All schema changes are versioned via Flyway migrations. The design prioritizes performance for Brazilian job search workloads: high-read job listings, write-heavy scraping pipelines, and vector similarity queries for matching.

**Stack**: PostgreSQL 17, pgvector 0.7.x, Spring Data JPA 3.4.x, Hibernate 6.6.x, Flyway 10.x, HikariCP.

## Checklist

1. Create a Flyway migration for every schema change — V{N}__description.sql
2. Use `SEQUENCE` strategy for all entity IDs — never IDENTITY or AUTO
3. Disable `open-in-view` in application.yml (already done)
4. Define all column types explicitly — never rely on Hibernate DDL auto-generation
5. Use JSONB for flexible schema fields (job metadata, scraper config)
6. Use `TEXT[]` for array fields (skills list, job tags)
7. Use `vector(1024)` for embedding columns with HNSW index
8. Create indexes for every foreign key and frequently queried column
9. Use `@Transactional(readOnly = true)` on all repository/service read methods
10. Enable batch inserts with `hibernate.jdbc.batch_size=50`
11. Use `@Embeddable` for value objects shared across entities (Money, Address)
12. Set `hibernate.order_inserts=true` and `hibernate.order_updates=true` for batching

## Key Rules

- **NEVER** use `GenerationType.IDENTITY` — it disables batch inserts; always use `SEQUENCE`
- **NEVER** modify an existing Flyway migration — create a new one
- **NEVER** use `spring.jpa.hibernate.ddl-auto=create` or `update` in any environment — only `validate`
- **NEVER** use eager fetching (`FetchType.EAGER`) — always lazy with explicit joins
- **NEVER** put business logic in `@Entity` classes beyond simple computed fields
- **NEVER** use raw SQL strings in code — use Spring Data `@Query` or Specification API
- **ALWAYS** use `@Column(columnDefinition = "...")` for non-standard types
- **ALWAYS** create a Flyway migration for pgvector extension: `CREATE EXTENSION IF NOT EXISTS vector`
- **ALWAYS** index foreign keys, JSONB fields (GIN), and text search columns (GIN with tsvector)
- **ALWAYS** use `@Entity` only in `domain/model/` packages — never leak to service/controller
- **ALWAYS** use `@Transactional(readOnly = true)` by default, remove `readOnly` only for writes
- **ALWAYS** allocate IDs with `allocationSize` matching the database INCREMENT BY

## Entity Design

### Core Schema

```sql
-- V1__create_extensions.sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;
```

```sql
-- V2__create_users.sql
CREATE TABLE users (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    external_id     UUID NOT NULL DEFAULT uuid_generate_v4() UNIQUE,
    email           VARCHAR(255) NOT NULL UNIQUE,
    password_hash   VARCHAR(255),
    full_name       VARCHAR(255) NOT NULL,
    phone           VARCHAR(20),
    cpf_encrypted   VARCHAR(512),
    avatar_url      VARCHAR(1024),
    auth_provider   VARCHAR(20)  NOT NULL DEFAULT 'LOCAL',
    provider_id     VARCHAR(255),
    email_verified  BOOLEAN      NOT NULL DEFAULT FALSE,
    enabled         BOOLEAN      NOT NULL DEFAULT TRUE,
    lgpd_consent    BOOLEAN      NOT NULL DEFAULT FALSE,
    consent_date    TIMESTAMP,
    created_at      TIMESTAMP    NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP    NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users (email);
CREATE INDEX idx_users_external_id ON users (external_id);
```

```sql
-- V3__create_resumes.sql
CREATE TABLE resumes (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title           VARCHAR(255) NOT NULL,
    summary         TEXT,
    skills          TEXT[] NOT NULL DEFAULT '{}',
    experience      JSONB NOT NULL DEFAULT '[]',
    education       JSONB NOT NULL DEFAULT '[]',
    languages       JSONB NOT NULL DEFAULT '[]',
    certifications  JSONB NOT NULL DEFAULT '[]',
    embedding       vector(1024),
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_resumes_user_id ON resumes (user_id);
CREATE INDEX idx_resumes_embedding ON resumes
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
```

```sql
-- V4__create_weighted_skills.sql
CREATE TABLE weighted_skills (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    resume_id   BIGINT NOT NULL REFERENCES resumes(id) ON DELETE CASCADE,
    skill_name  VARCHAR(255) NOT NULL,
    weight      SMALLINT NOT NULL DEFAULT 3 CHECK (weight BETWEEN 1 AND 5),
    category    VARCHAR(50),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_weighted_skills_resume_id ON weighted_skills (resume_id);
CREATE INDEX idx_weighted_skills_skill_name ON weighted_skills (skill_name);
```

```sql
-- V5__create_jobs.sql
CREATE TABLE jobs (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source          VARCHAR(50) NOT NULL,
    source_id       VARCHAR(255) NOT NULL,
    source_url      VARCHAR(1024) NOT NULL,
    url_hash        VARCHAR(64) NOT NULL UNIQUE,
    title           VARCHAR(500) NOT NULL,
    company_name    VARCHAR(500),
    company_logo_url VARCHAR(1024),
    description     TEXT NOT NULL,
    location        VARCHAR(255),
    city            VARCHAR(100),
    state           VARCHAR(2),
    country         VARCHAR(3) DEFAULT 'BRA',
    is_remote       BOOLEAN DEFAULT FALSE,
    job_type        VARCHAR(30),
    experience_level VARCHAR(30),
    salary_min      DECIMAL(12,2),
    salary_max      DECIMAL(12,2),
    salary_currency VARCHAR(3) DEFAULT 'BRL',
    benefits        TEXT[],
    tags            TEXT[],
    requirements    TEXT,
    embedding       vector(1024),
    posted_date     TIMESTAMP,
    expires_date    TIMESTAMP,
    metadata        JSONB DEFAULT '{}',
    is_active       BOOLEAN NOT NULL DEFAULT TRUE,
    scraped_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_jobs_url_hash ON jobs (url_hash);
CREATE INDEX idx_jobs_source ON jobs (source, source_id);
CREATE INDEX idx_jobs_active ON jobs (is_active) WHERE is_active = TRUE;
CREATE INDEX idx_jobs_location ON jobs (city, state);
CREATE INDEX idx_jobs_posted_date ON jobs (posted_date DESC);
CREATE INDEX idx_jobs_embedding ON jobs
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);
CREATE INDEX idx_jobs_title_gin ON jobs USING gin(to_tsvector('portuguese', title));
CREATE INDEX idx_jobs_description_gin ON jobs USING gin(to_tsvector('portuguese', description));
```

```sql
-- V6__create_scraping_tasks.sql
CREATE TABLE scraping_tasks (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    source          VARCHAR(50) NOT NULL,
    status          VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    query           VARCHAR(500),
    location        VARCHAR(255),
    jobs_found      INTEGER DEFAULT 0,
    jobs_new        INTEGER DEFAULT 0,
    jobs_updated    INTEGER DEFAULT 0,
    error_message   TEXT,
    started_at      TIMESTAMP,
    completed_at    TIMESTAMP,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_scraping_tasks_status ON scraping_tasks (status);
CREATE INDEX idx_scraping_tasks_source ON scraping_tasks (source);
```

```sql
-- V7__create_job_matches.sql
CREATE TABLE job_matches (
    id              BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id         BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id          BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    resume_id       BIGINT REFERENCES resumes(id) ON DELETE SET NULL,
    score           DECIMAL(5,2) NOT NULL,
    explanation     TEXT,
    skill_match     JSONB DEFAULT '{}',
    embedding_score DECIMAL(5,4),
    structured_score DECIMAL(5,4),
    is_dismissed    BOOLEAN NOT NULL DEFAULT FALSE,
    created_at      TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, job_id)
);

CREATE INDEX idx_job_matches_user_score ON job_matches (user_id, score DESC);
CREATE INDEX idx_job_matches_user_not_dismissed ON job_matches (user_id, score DESC)
    WHERE is_dismissed = FALSE;
```

```sql
-- V8__create_favorites.sql
CREATE TABLE favorites (
    id          BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id     BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    job_id      BIGINT NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    notes       TEXT,
    created_at  TIMESTAMP NOT NULL DEFAULT NOW(),
    UNIQUE (user_id, job_id)
);

CREATE INDEX idx_favorites_user ON favorites (user_id);
```

```sql
-- V9__create_subscriptions.sql
CREATE TABLE subscriptions (
    id                  BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    user_id             BIGINT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    plan                VARCHAR(20) NOT NULL DEFAULT 'FREE',
    platform            VARCHAR(20) NOT NULL,
    transaction_id      VARCHAR(255) UNIQUE,
    status              VARCHAR(20) NOT NULL DEFAULT 'ACTIVE',
    started_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMP,
    auto_renew          BOOLEAN NOT NULL DEFAULT FALSE,
    created_at          TIMESTAMP NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_subscriptions_user ON subscriptions (user_id);
CREATE INDEX idx_subscriptions_status ON subscriptions (status) WHERE status = 'ACTIVE';
```

## Code Examples

### Entity with SEQUENCE Strategy

```java
package com.perfectjob.job.domain.model;

import jakarta.persistence.*;
import lombok.*;
import org.hibernate.annotations.JdbcTypeCode;
import org.hibernate.annotations.Type;
import org.hibernate.type.SqlTypes;
import pgvector.PGvector;

import java.math.BigDecimal;
import java.time.LocalDateTime;

@Entity
@Table(name = "jobs")
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
@AllArgsConstructor(access = AccessLevel.PRIVATE)
@Builder
public class Job {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE, generator = "jobs_seq")
    @SequenceGenerator(name = "jobs_seq", sequenceName = "jobs_id_seq", allocationSize = 50)
    private Long id;

    @Column(name = "source", nullable = false, length = 50)
    private String source;

    @Column(name = "source_id", nullable = false, length = 255)
    private String sourceId;

    @Column(name = "source_url", nullable = false, length = 1024)
    private String sourceUrl;

    @Column(name = "url_hash", nullable = false, length = 64, unique = true)
    private String urlHash;

    @Column(name = "title", nullable = false, length = 500)
    private String title;

    @Column(name = "company_name", length = 500)
    private String companyName;

    @Column(name = "description", nullable = false, columnDefinition = "TEXT")
    private String description;

    @Column(name = "location", length = 255)
    private String location;

    @Column(name = "city", length = 100)
    private String city;

    @Column(name = "state", length = 2)
    private String state;

    @Column(name = "is_remote")
    private Boolean isRemote;

    @Column(name = "job_type", length = 30)
    private String jobType;

    @Column(name = "salary_min", precision = 12, scale = 2)
    private BigDecimal salaryMin;

    @Column(name = "salary_max", precision = 12, scale = 2)
    private BigDecimal salaryMax;

    @Column(name = "embedding", columnDefinition = "vector(1024)")
    private PGvector embedding;

    @JdbcTypeCode(SqlTypes.JSON_ARRAY)
    @Column(name = "tags", columnDefinition = "TEXT[]")
    private String[] tags;

    @JdbcTypeCode(SqlTypes.JSON)
    @Column(name = "metadata", columnDefinition = "jsonb")
    private Object metadata;

    @Column(name = "is_active")
    private Boolean isActive;

    @Column(name = "posted_date")
    private LocalDateTime postedDate;

    @Column(name = "scraped_at")
    private LocalDateTime scrapedAt;

    @Column(name = "created_at", nullable = false, updatable = false)
    private LocalDateTime createdAt;

    @Column(name = "updated_at", nullable = false)
    private LocalDateTime updatedAt;

    @PrePersist
    protected void onCreate() {
        createdAt = LocalDateTime.now();
        updatedAt = LocalDateTime.now();
    }

    @PreUpdate
    protected void onUpdate() {
        updatedAt = LocalDateTime.now();
    }
}
```

### Spring Data JPA Repository

```java
package com.perfectjob.job.adapter.out;

import com.perfectjob.job.domain.model.Job;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.Pageable;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;

import java.util.Optional;

public interface JobJpaRepository extends JpaRepository<Job, Long> {

    Optional<Job> findByUrlHash(String urlHash);

    @Query("""
        SELECT j FROM Job j
        WHERE j.isActive = true
          AND (:city IS NULL OR j.city = :city)
          AND (:state IS NULL OR j.state = :state)
          AND (:jobType IS NULL OR j.jobType = :jobType)
          AND (:query IS NULL OR LOWER(j.title) LIKE LOWER(CONCAT('%', :query, '%')))
        ORDER BY j.postedDate DESC
    """)
    Page<Job> searchActive(
            @Param("query") String query,
            @Param("city") String city,
            @Param("state") String state,
            @Param("jobType") String jobType,
            Pageable pageable);

    @Query(value = """
        SELECT j.*, 1 - (j.embedding <=> :queryEmbedding) AS similarity
        FROM jobs j
        WHERE j.is_active = true
          AND j.embedding IS NOT NULL
        ORDER BY j.embedding <=> :queryEmbedding
        LIMIT :limit
    """, nativeQuery = true)
    List<Object[]> findSimilarJobs(
            @Param("queryEmbedding") PGvector queryEmbedding,
            @Param("limit") int limit);
}
```

### Embeddable Value Object

```java
@Embeddable
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Money {

    @Column(name = "amount", precision = 12, scale = 2)
    private BigDecimal amount;

    @Column(name = "currency", length = 3)
    private String currency;

    public static Money of(BigDecimal amount, String currency) {
        Money money = new Money();
        money.amount = amount;
        money.currency = currency != null ? currency : "BRL";
        return money;
    }

    public String formatted() {
        NumberFormat format = NumberFormat.getCurrencyInstance(new Locale("pt", "BR"));
        return format.format(amount);
    }
}
```

## References

- PostgreSQL 17: https://www.postgresql.org/docs/17/
- pgvector: https://github.com/pgvector/pgvector
- Spring Data JPA: https://docs.spring.io/spring-data/jpa/reference/
- Hibernate 6: https://hibernate.org/orm/releases/6.6/
- Flyway: https://flywaydb.org/documentation/
- HikariCP: https://github.com/brettwooldridge/HikariCP
