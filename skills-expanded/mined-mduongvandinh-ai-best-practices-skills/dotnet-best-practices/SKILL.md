# .NET Best Practices Audit

> **163 practices** | **18 domains** | Weighted scoring | Vietnamese report
> Triggers: `/dotnet-best-practices`, `/dbp`

## Overview

Audit toàn diện .NET/ASP.NET Core/C# project. Phát hiện violations bằng regex patterns, chấm điểm theo domain có trọng số. Tất cả nội dung báo cáo bằng **tiếng Việt**.

**Supported stacks:** .NET 8/9, ASP.NET Core, Entity Framework Core, Identity, SignalR, MediatR, FluentValidation, xUnit/NUnit, Serilog.

## Knowledge Files

| File | Domain | Practices | Weight |
|------|--------|-----------|--------|
| `00_Tong_Quan.md` | Overview & Scoring | -- | -- |
| `01_Cau_Truc_Solution.md` | Solution Structure | 9 | x1 |
| `02_Dependency_Injection.md` | Dependency Injection | 10 | x1 |
| `03_REST_API_Controller.md` | REST API & Controller | 10 | x1 |
| `04_Middleware_Pipeline.md` | Middleware Pipeline | 8 | x1 |
| `05_EF_Core.md` | Entity Framework Core | 12 | x2 |
| `06_Identity_Security.md` | Identity & Security | 12 | x3 |
| `07_Exception_Handling.md` | Exception Handling | 9 | x1 |
| `08_Async_Task.md` | Async/Await & Task | 10 | x2 |
| `09_Testing.md` | Testing (xUnit/NUnit) | 10 | x2 |
| `10_Logging.md` | Logging (Serilog/NLog) | 8 | x1 |
| `11_Configuration.md` | Configuration | 8 | x1 |
| `12_Validation.md` | Validation | 8 | x1 |
| `13_Caching.md` | Caching | 8 | x1 |
| `14_SignalR.md` | SignalR & Real-time | 7 | x1 |
| `15_Background_Services.md` | Background Services | 8 | x1 |
| `16_Migration.md` | EF Migrations | 7 | x1 |
| `17_Deployment.md` | Deployment & Docker | 9 | x1 |
| `18_LINQ_Performance.md` | LINQ & Performance | 9 | x1 |

> **Path:** Knowledge files are in `knowledge/` (Claude Code) or `references/` (Antigravity).

## Audit Workflow (6 Steps)

### Step 1: Collect Context
- Read `*.csproj`, `Program.cs`, `appsettings.json`
- Identify .NET version, ASP.NET Core version
- Identify key packages (EF Core, Identity, MediatR, etc.)

### Step 2: Parallel Scan (4 Agents)

```
Agent Security  -> domains: 06, 11
Agent Data      -> domains: 05, 08, 12, 16, 18
Agent Arch      -> domains: 01, 02, 03, 04, 07, 10
Agent Quality   -> domains: 09, 13, 14, 15, 17
```

Each agent:
1. Read corresponding knowledge files
2. Scan source code using regex patterns from "Phát hiện" sections
3. Record violations with code `DBP-XX-YY`

### Step 3: Calculate Scores

```
Penalties: MANDATORY=-10, RECOMMENDED=-5, NICE_TO_HAVE=-2
Domain Score = max(0, 100 - sum(violation_penalty))

Weighted domains:
  Identity & Security (06):     x3 (highest impact)
  Entity Framework Core (05):   x2
  Async/Await & Task (08):      x2
  Testing (09):                 x2
  All others:                   x1

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
2. Skip `bin/`, `obj/`, `Migrations/` (auto-generated)
3. Allow Console.WriteLine in test projects
4. Respect `#pragma warning disable`, `[SuppressMessage]`
5. Group repeated patterns (>5 = 1 entry + count)
6. Exclude generated code (*.Designer.cs, *.g.cs)

### Step 6: Generate Report
Vietnamese report with: overall score, domain breakdown, top violations with file:line, fix suggestions, improvement plan.

## Violation Codes

Format: `DBP-XX-YY`
- **DBP** = Dotnet Best Practice
- **XX** = Domain number (01-18)
- **YY** = Practice number within domain

## Important Notes
- All report content in **Vietnamese**
- Code examples in **English/C#**
- Priority: MANDATORY first, then RECOMMENDED, then NICE_TO_HAVE
- Target: Overall >= 75 (TỐT)
