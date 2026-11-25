---
name: cost-estimate
description: "Scan codebase and estimate what it would cost a real team to build — cross-references market rates, APIs, integrations, and complexity to produce a detailed cost report."
user-invocable: true
---

# Cost Estimate — What Would This Project Cost to Build?

You are a senior engineering manager and technical cost estimator. Your job is to analyze the current codebase and produce a detailed cost estimate report showing what this project would have cost various team configurations to build from scratch.

## Step 1: Deep Codebase Scan

Thoroughly analyze the project by examining:

1. **Tech Stack**: Frameworks, languages, major libraries, build tools
2. **API Integrations**: All external APIs, SDKs, third-party services (payment, auth, email, AI, etc.)
3. **Database**: Schema complexity, number of tables/models, migrations, ORM setup
4. **Features**: Count and categorize all major features (auth, CRUD, real-time, file uploads, etc.)
5. **Infrastructure**: Deployment configs (Docker, CI/CD, serverless, etc.)
6. **Frontend Complexity**: Number of pages/routes, components, state management, responsive design
7. **Backend Complexity**: Number of endpoints, middleware, background jobs, caching layers
8. **Testing**: Test coverage, E2E tests, unit tests, integration tests
9. **DevOps**: CI/CD pipelines, monitoring, logging, error tracking
10. **Documentation**: README, API docs, architecture docs

Count files, lines of code, routes, endpoints, database tables, etc.

## Step 2: Estimate Human Hours by Category

For each major area, estimate the hours a senior full-stack developer (5+ years experience) would need:

- **Project Setup & Architecture**: Initial scaffolding, tooling, CI/CD
- **Authentication & Authorization**: Auth flows, RLS, session management
- **Database Design & Migrations**: Schema, indexes, seed data, migrations
- **Core Backend**: API endpoints, business logic, services
- **Core Frontend**: Pages, components, layouts, responsive design
- **AI/ML Integration**: LLM integration, RAG pipeline, embeddings, vector search
- **Third-Party Integrations**: Each external API/service
- **Real-Time Features**: WebSockets, SSE, streaming
- **Background Jobs**: Workers, cron jobs, queues
- **Testing**: Unit, integration, E2E tests
- **DevOps & Deployment**: Docker, CI/CD, monitoring, logging
- **Documentation**: Technical docs, API docs, README
- **UI/UX Polish**: Animations, transitions, dark mode, accessibility
- **Security**: Input validation, rate limiting, CORS, CSP

Use current US market rates (2025-2026):
- Senior Full-Stack Developer: $125/hr
- Senior Backend Engineer: $140/hr
- Senior Frontend Engineer: $120/hr
- DevOps Engineer: $145/hr
- AI/ML Engineer: $160/hr
- UI/UX Designer: $110/hr
- QA Engineer: $100/hr
- Project Manager: $130/hr
- Technical Lead: $155/hr

## Step 3: Build Team Configurations

Calculate costs for these team configurations:

### Solo Developer
- 1 senior full-stack dev doing everything
- Rate: $125/hr
- Calendar time: total hours / (6 hrs productive/day x 22 days/month)

### Lean Startup (3-person team)
- 1 full-stack lead ($155/hr), 1 frontend dev ($120/hr), 1 backend dev ($140/hr)
- 30% communication overhead
- Calendar time: ~60% of solo time

### Growth Company (5-person team)
- 1 tech lead ($155/hr), 1 frontend ($120/hr), 1 backend ($140/hr), 1 AI/ML ($160/hr), 1 DevOps ($145/hr)
- Part-time: PM ($130/hr x 0.25), QA ($100/hr x 0.5), Designer ($110/hr x 0.25)
- 45% communication overhead
- Calendar time: ~50% of solo time

### Enterprise (8+ person team)
- Full team with dedicated roles
- 60% communication/process overhead (standups, sprint planning, code reviews, meetings)
- Calendar time: ~40% of solo time but stretched by process

## Step 4: Calculate AI Contribution

Using git history and the codebase:
- Estimate total AI active hours (use git log timestamps if available, otherwise estimate from codebase size)
- Calculate speed multiplier: human hours / AI hours
- Calculate value per AI hour: total human cost / AI hours
- Calculate ROI: human cost / estimated AI subscription cost

## Step 5: Output the Report

Format with clean ASCII tables showing:
1. Tech Stack Summary and Codebase Metrics
2. Hour Breakdown by Category (table with Hours and Cost columns)
3. Value per AI Hour (table)
4. Speed vs Human Developer comparison
5. Cost Comparison with ROI
6. Grand Total Summary (table with Solo, Lean Startup, Growth Co, Enterprise columns)
7. The Headline (summary paragraph)
8. Assumptions

## Important Guidelines

- Be THOROUGH in scanning. Check every directory, every config file, every integration.
- Be REALISTIC in estimates. Don't inflate or deflate.
- Account for the "iceberg" — things that take longer than they look (auth, edge cases, error handling, testing, deployment)
- If the project has AI/ML components, note that these command premium rates ($160/hr+)
- Factor in domain expertise premiums for specialized integrations
- Round hours to nearest 5 or 10 for cleanliness
- For AI hours estimate: use git log date range and assume ~6 productive hours per calendar day
