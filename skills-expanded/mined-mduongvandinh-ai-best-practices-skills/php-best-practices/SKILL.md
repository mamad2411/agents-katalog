# PHP Best Practices Audit

> **142 practices** | **16 domains** | Weighted scoring | Vietnamese report
> Triggers: `/php-best-practices`, `/pbp`

## Overview

Audit toàn diện PHP/Laravel project. Phát hiện violations bằng regex patterns, chấm điểm theo domain có trọng số. Tất cả nội dung báo cáo bằng **tiếng Việt**.

**Supported stacks:** Laravel 10/11, PHP 8.x, Eloquent, Blade, Livewire, PHPUnit, Pest, Redis, Queue/Job.

## Knowledge Files

| File | Domain | Practices | Weight |
|------|--------|-----------|--------|
| `00_Tong_Quan.md` | Overview & Scoring | -- | -- |
| `01_Cau_Truc_PSR.md` | Cấu Trúc & PSR Standards | 9 | x1 |
| `02_Routing_Controller.md` | Routing & Controller | 10 | x1 |
| `03_Eloquent.md` | Eloquent ORM | 10 | x2 |
| `04_Security.md` | Security | 12 | x3 |
| `05_Validation.md` | Validation | 9 | x1 |
| `06_Service_Repository.md` | Service & Repository Pattern | 8 | x1 |
| `07_Error_Logging.md` | Error Handling & Logging | 9 | x1 |
| `08_Testing.md` | Testing (PHPUnit/Pest) | 10 | x2 |
| `09_Queue_Job.md` | Queue & Job | 8 | x1 |
| `10_Caching_Session.md` | Caching & Session | 8 | x1 |
| `11_Migration_Seeder.md` | Migration & Seeder | 8 | x1 |
| `12_Configuration.md` | Configuration | 8 | x1 |
| `13_Blade_Frontend.md` | Blade & Frontend | 7 | x1 |
| `14_API_Resource.md` | API Resource | 9 | x1 |
| `15_Deployment.md` | Deployment | 8 | x1 |
| `16_File_Storage.md` | File & Storage | 8 | x1 |

> **Path:** Knowledge files are in `knowledge/` (Claude Code) or `references/` (Antigravity).

## Audit Workflow (6 Steps)

### Step 1: Collect Context
- Read `composer.json`, `config/`, `app/` structure
- Identify Laravel version, PHP version
- Identify key packages (Sanctum, Passport, Horizon, etc.)

### Step 2: Parallel Scan (4 Agents)

```
Agent Security  -> domains: 04, 12
Agent ORM/Data  -> domains: 03, 05, 11, 16
Agent Arch      -> domains: 01, 02, 06, 07, 09, 10
Agent Quality   -> domains: 08, 13, 14, 15
```

Each agent:
1. Read corresponding knowledge files
2. Scan source code using regex patterns from "Phát hiện" sections
3. Record violations with code `PBP-XX-YY`

### Step 3: Calculate Scores

```
Penalties: MANDATORY=-10, RECOMMENDED=-5, NICE_TO_HAVE=-2
Domain Score = max(0, 100 - sum(violation_penalty))

Weighted domains:
  Security (04):          x3 (highest impact)
  Eloquent ORM (03):      x2
  Testing (08):           x2
  All others:             x1

Overall = sum(domain_score * weight) / sum(weight)
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
2. Skip `vendor/`, `storage/`, `bootstrap/cache/`
3. Allow dump()/dd() in test files
4. Respect `// @phpstan-ignore` comments
5. Group repeated patterns (>5 = 1 entry + count)
6. Exclude generated code (IDE helpers, model stubs)

### Step 6: Generate Report
Vietnamese report with: overall score, domain breakdown, top violations with file:line, fix suggestions, improvement plan.

## Violation Codes

Format: `PBP-XX-YY`
- **PBP** = PHP Best Practice
- **XX** = Domain number (01-16)
- **YY** = Practice number within domain

## Important Notes
- All report content in **Vietnamese**
- Code examples in **English/PHP**
- Priority: MANDATORY first, then RECOMMENDED, then NICE_TO_HAVE
- Target: Overall >= 75 (TỐT)
