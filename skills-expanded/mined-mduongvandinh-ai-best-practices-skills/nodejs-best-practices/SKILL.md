# Node.js Best Practices Audit

> **157 practices** | **17 domains** | Weighted scoring | Vietnamese report
> Triggers: `/nodejs-best-practices`, `/nbp`

## Overview

Audit toàn diện Node.js project (Express/NestJS/Fastify + TypeScript). Phát hiện violations bằng regex patterns, chấm điểm theo domain có trọng số. Tất cả nội dung báo cáo bằng **tiếng Việt**.

**Supported stacks:** Express, NestJS, Fastify, Prisma, TypeORM, Drizzle, Mongoose, Jest, Vitest, Pino, Winston, Socket.IO, Redis, Docker, PM2.

## Knowledge Files

Các file knowledge chứa chi tiết từng practice (cách đúng, cách sai, regex phát hiện, checklist):

| File | Domain | Practices | Weight |
|------|--------|-----------|--------|
| `00_Tong_Quan.md` | Overview & Scoring | — | — |
| `01_Cau_Truc_Du_An.md` | Cấu Trúc Dự Án | 9 | x1 |
| `02_Error_Handling_Async.md` | Error Handling & Async | 10 | x2 |
| `03_REST_API_Middleware.md` | REST API & Middleware | 10 | x1 |
| `04_Authentication_Security.md` | Authentication & Security | 12 | x3 |
| `05_Database.md` | Database (Prisma/TypeORM/Mongoose) | 11 | x2 |
| `06_Validation.md` | Validation & Input Sanitization | 9 | x1 |
| `07_Testing.md` | Testing (Jest/Vitest) | 10 | x2 |
| `08_Performance_Memory.md` | Performance & Memory | 10 | x2 |
| `09_Logging_Monitoring.md` | Logging & Monitoring | 8 | x1 |
| `10_Configuration.md` | Configuration & Environment | 8 | x1 |
| `11_Dependency_Management.md` | Dependency Management (npm/pnpm) | 8 | x1 |
| `12_TypeScript.md` | TypeScript Best Practices | 10 | x1 |
| `13_Async_Event_Loop.md` | Async Patterns & Event Loop | 10 | x2 |
| `14_Caching.md` | Caching (Redis/In-memory) | 8 | x1 |
| `15_WebSocket.md` | WebSocket & Real-time | 7 | x1 |
| `16_Deployment.md` | Deployment & Docker | 9 | x1 |
| `17_File_Stream.md` | File Upload & Stream | 8 | x1 |

> **Path:** Knowledge files are in `knowledge/` (Claude Code) or `references/` (Antigravity).

## Audit Workflow (6 Steps)

### Step 1: Collect Context
- Read `package.json`, `tsconfig.json`, `.eslintrc.*`
- Identify framework (Express / NestJS / Fastify)
- Identify ORM (Prisma / TypeORM / Mongoose / Drizzle)
- Identify test runner (Jest / Vitest / Mocha)

### Step 2: Parallel Scan (4 Agents)

```
Agent Security  -> domains: 04, 06, 10
Agent Data      -> domains: 05, 08, 13, 14, 17
Agent Arch      -> domains: 01, 03, 09, 11, 12, 16
Agent Quality   -> domains: 02, 07, 15
```

Each agent:
1. Read corresponding knowledge files
2. Scan source code using regex patterns from "Phát hiện" sections
3. Record violations with code `NBP-XX-YY`

### Step 3: Calculate Scores

```
Penalty per severity:
  BẮT BUỘC (MANDATORY):      -10 points per violation
  KHUYẾN NGHỊ (RECOMMENDED):  -5 points per violation
  NÊN CÓ (NICE TO HAVE):     -2 points per violation

Domain Score = max(0, 100 - sum(violation_penalty))

Weighted domains:
  Authentication & Security (04):       x3 (highest impact)
  Error Handling (02):                   x2
  Database (05):                         x2
  Testing (07):                          x2
  Performance & Memory (08):             x2
  Async Patterns & Event Loop (13):      x2
  All others:                            x1

Overall Score = sum(domain_score * weight) / sum(weight)
```

### Step 4: Ranking

| Score | Rank |
|-------|------|
| 90-100 | XUẤT SẮC (Excellent) |
| 75-89 | TỐT (Good) |
| 60-74 | CẦN CẢI THIỆN (Needs Improvement) |
| 40-59 | YẾU (Weak) |
| 0-39 | NGUY HIỂM (Critical) |

### Step 5: Filter Noise

Before generating report, filter false positives:
1. Only report violations with concrete evidence (file path + line number)
2. Don't report if there's a legitimate comment (e.g., `// eslint-disable`, `// @ts-ignore` with reason)
3. Don't report `console.log` in test files or scripts
4. Consider context - `any` in type declaration files vs application code
5. Group similar violations - if same pattern repeats >5 times, report once with count
6. Exclude generated code - skip `node_modules/`, `dist/`, `*.generated.ts`, `*.d.ts`

### Step 6: Generate Report

```
# Node.js Best Practices Audit Report

## Tổng quan
- Overall Score: XX/100 (RANK)
- Violations: X MANDATORY | Y RECOMMENDED | Z NICE_TO_HAVE
- Framework: Express/NestJS/Fastify
- Node.js: XX | TypeScript: XX

## Bảng điểm theo Domain
| Domain | Tên | Điểm | Vi Phạm | Trọng Số |
|--------|-----|------|---------|----------|
| 01 | Cấu Trúc Dự Án | XX/100 | ... | x1 |

## Top 10 Vi Phạm Nghiêm Trọng
### 1. [NBP-XX-YY] Tên Vi Phạm
Severity: MANDATORY | Domain: XX | Penalty: -10
File: src/path/to/file.ts:42
Code vi phạm: ...
Gợi ý sửa: ...

## Kế Hoạch Cải Thiện
- Ưu tiên cao (fix ngay): ...
- Ưu tiên trung (sprint này): ...
- Ưu tiên thấp (backlog): ...
```

## Violation Codes

Format: `NBP-XX-YY`
- **NBP** = Node Best Practice
- **XX** = Domain number (01-17)
- **YY** = Practice number within domain

Examples:
- `NBP-04-01` = Password hashing (bcrypt/argon2)
- `NBP-05-01` = N+1 query prevention
- `NBP-08-01` = Event loop blocking
- `NBP-13-02` = Promise.all for parallel execution

## Important Notes

- All report content in **Vietnamese (tiếng Việt)**
- Code examples remain in **English/TypeScript**
- Priority: find MANDATORY violations first, then RECOMMENDED, finally NICE_TO_HAVE
- After fixes, re-run audit to verify improvements
- Target: Overall >= 75 (TỐT)
