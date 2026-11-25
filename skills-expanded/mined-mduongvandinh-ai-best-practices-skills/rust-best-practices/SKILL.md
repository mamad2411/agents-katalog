# Rust Best Practices Audit

> **134+ practices** | **15 domains** | Weighted scoring | Vietnamese report
> Triggers: `/rust-best-practices`, `/rbp`

## Overview

Audit toàn diện Rust project (Actix-web/Axum/Rocket + Tokio). Phát hiện violations bằng regex patterns, chấm điểm theo domain có trọng số. Tất cả nội dung báo cáo bằng **tiếng Việt**.

**Supported stacks:** Actix-web, Axum, Rocket, Tokio, sqlx, Diesel, SeaORM, tracing, serde, clap.

## Knowledge Files

| File | Domain | Weight |
|------|--------|--------|
| `00_Tong_Quan.md` | Overview & Scoring | -- |
| `01_Cau_Truc_Cargo.md` | Cấu Trúc Dự Án & Cargo | x1 |
| `02_Ownership_Borrowing.md` | Ownership & Borrowing | x3 |
| `03_Error_Handling.md` | Error Handling | x2 |
| `04_Async_Tokio.md` | Async & Tokio Runtime | x2 |
| `05_HTTP_Web.md` | HTTP & Web Framework | x1 |
| `06_Security_Unsafe.md` | Security & Unsafe | x3 |
| `07_Database.md` | Database (sqlx/Diesel/SeaORM) | x2 |
| `08_Testing.md` | Testing | x2 |
| `09_Trait_Generics.md` | Trait & Generics | x1 |
| `10_Concurrency.md` | Concurrency | x2 |
| `11_Memory_Performance.md` | Memory & Performance | x2 |
| `12_Logging_Tracing.md` | Logging & Tracing | x1 |
| `13_Configuration_Serde.md` | Configuration & Serde | x1 |
| `14_Deployment.md` | Deployment & Cross-compilation | x1 |
| `15_Macro.md` | Macro & Procedural Macro | x1 |

> **Path:** Knowledge files are in `knowledge/` (Claude Code) or `references/` (Antigravity).

## Audit Workflow (6 Steps)

### Step 1: Collect Context
- Read `Cargo.toml` workspace config, dependencies
- Identify framework (Actix-web / Axum / Rocket)
- Identify async runtime (Tokio / async-std)
- Identify ORM/DB (sqlx / Diesel / SeaORM)

### Step 2: Parallel Scan (4 Agents)

```
Agent A (Foundation) -> domains: 01, 02, 03, 04
Agent B (Web & Data) -> domains: 05, 06, 07, 08
Agent C (Advanced)   -> domains: 09, 10, 11, 12
Agent D (Ops & Meta) -> domains: 13, 14, 15
```

Each agent:
1. Read corresponding knowledge files
2. Scan source code using regex patterns from "Phát hiện" sections
3. Record violations with code `RBP-XX-YY`

### Step 3: Calculate Scores

```
Penalties: MANDATORY=-10, RECOMMENDED=-5, NICE_TO_HAVE=-2
Domain Score = max(0, 100 - sum(violation_penalty))

Weighted domains:
  Ownership & Borrowing (02):    x3
  Security & Unsafe (06):        x3
  Error Handling (03):           x2
  Async/Tokio (04):              x2
  Database (07):                 x2
  Testing (08):                  x2
  Concurrency (10):              x2
  Memory & Performance (11):     x2
  All others:                    x1

Overall = sum(domain_score * weight) / sum(weight)  [/25]
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
2. Skip `target/`, `*.generated.rs`, build scripts
3. Allow unwrap()/expect() in `#[test]` and `#[cfg(test)]`
4. Allow println! in `examples/`
5. Respect `// SAFETY:`, `// ALLOW:` comments
6. Group repeated patterns (>5 = 1 entry + count)

### Step 6: Generate Report
Vietnamese report with: overall score, domain breakdown, top violations with file:line, fix suggestions, improvement plan.

## Violation Codes

Format: `RBP-XX-YY`
- **RBP** = Rust Best Practice
- **XX** = Domain number (01-15)
- **YY** = Practice number within domain

## Important Notes
- All report content in **Vietnamese**
- Code examples in **English/Rust**
- Priority: MANDATORY first, then RECOMMENDED, then NICE_TO_HAVE
- Target: Overall >= 75 (TỐT)
