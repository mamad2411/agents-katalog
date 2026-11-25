# Go Best Practices Audit

> **146 practices** | **15 domains** | Weighted scoring | Vietnamese report
> Triggers: `/go-best-practices`, `/gbp`

## Overview

Audit toàn diện Go project (Chi/Gin/Echo/Fiber + stdlib). Phát hiện violations bằng regex patterns, chấm điểm theo domain có trọng số. Tất cả nội dung báo cáo bằng **tiếng Việt**.

**Supported stacks:** Chi, Gin, Echo, Fiber, net/http, sqlx, GORM, pgx, slog, zap, zerolog, gRPC, protobuf.

## Knowledge Files

| File | Domain | Weight |
|------|--------|--------|
| `00_Tong_Quan.md` | Overview & Scoring | -- |
| `01_Cau_Truc_Package.md` | Cấu Trúc Dự Án & Package | x1 |
| `02_Error_Handling.md` | Error Handling | x2 |
| `03_Concurrency.md` | Concurrency (Goroutine & Channel) | x3 |
| `04_HTTP_REST.md` | HTTP & REST API | x1 |
| `05_Security.md` | Security & Crypto | x3 |
| `06_Database.md` | Database (sqlx/GORM/pgx) | x2 |
| `07_Testing.md` | Testing | x2 |
| `08_Interface_DI.md` | Interface & Dependency Injection | x1 |
| `09_Logging.md` | Logging & Observability | x1 |
| `10_Configuration.md` | Configuration & Environment | x1 |
| `11_Memory_Performance.md` | Memory & Performance | x2 |
| `12_Context.md` | Context & Cancellation | x2 |
| `13_Code_Style.md` | Code Style & Idioms | x1 |
| `14_Deployment.md` | Deployment & Docker | x1 |
| `15_gRPC.md` | gRPC & Protobuf | x1 |

> **Path:** Knowledge files are in `knowledge/` (Claude Code) or `references/` (Antigravity).

## Audit Workflow (6 Steps)

### Step 1: Collect Context
- Read `go.mod` module path and dependencies
- Identify framework (Chi / Gin / Echo / Fiber / stdlib)
- Identify DB layer (sqlx / GORM / pgx / ent)
- Identify test patterns (testing / testify / gomock)

### Step 2: Parallel Scan (4 Agents)

```
Agent A (Foundation) -> domains: 01, 02, 03, 04
Agent B (Sec & Data) -> domains: 05, 06, 07, 08
Agent C (Ops)        -> domains: 09, 10, 11, 12
Agent D (Style)      -> domains: 13, 14, 15
```

Each agent:
1. Read corresponding knowledge files
2. Scan source code using regex patterns from "Phát hiện" sections
3. Record violations with code `GBP-XX-YY`

### Step 3: Calculate Scores

```
Penalties: MANDATORY=-10, RECOMMENDED=-5, NICE_TO_HAVE=-2
Domain Score = max(0, 100 - sum(violation_penalty))

Weighted domains:
  Concurrency (03):              x3
  Security & Crypto (05):        x3
  Error Handling (02):           x2
  Database (06):                 x2
  Testing (07):                  x2
  Memory & Performance (11):     x2
  Context & Cancellation (12):   x2
  All others:                    x1

Overall = sum(domain_score * weight) / sum(weight)  [/24]
```

### Step 4: Ranking

| Score | Rank |
|-------|------|
| 90-100 | XUẤT SẮC (Excellent) |
| 75-89 | TỐT (Good) |
| 60-74 | TRUNG BÌNH (Average) |
| 40-59 | YẾU (Weak) |
| 0-39 | NGUY HIỂM (Critical) |

### Step 5: Filter Noise
1. Only report with file path + line evidence
2. Skip `vendor/`, `*.pb.go`, `*_gen.go`
3. Allow error ignore in `_test.go`
4. Allow fmt.Println in `examples/`, `cmd/` tools
5. Respect `//nolint:` comments
6. Group repeated patterns (>5 = 1 entry + count)

### Step 6: Generate Report
Vietnamese report with: overall score, domain breakdown, top violations with file:line, fix suggestions, improvement plan.

## Violation Codes

Format: `GBP-XX-YY`
- **GBP** = Go Best Practice
- **XX** = Domain number (01-15)
- **YY** = Practice number within domain

## Important Notes
- All report content in **Vietnamese**
- Code examples in **English/Go**
- Priority: MANDATORY first, then RECOMMENDED, then NICE_TO_HAVE
- Target: Overall >= 75 (TỐT)
