---
name: weekly-meeting
description: Prepare complete, easy-to-say weekly meeting updates from KPA workspace records. Use when the user asks for this week's work, weekly meeting notes, a spoken status update, completed/in-progress/next-week work, or project-grouped weekly reporting. Reconcile actual work evidence across MCP project history, tasks, raw logs, schedules, subdomains, deployments, requests, coordination, analysis, infrastructure, and CI/CD work.
---

# Purpose

Produce a weekly update the human can read aloud without translating ticket logs into natural speech.

# Source Rules

Use the DB-backed `agent_mcp` virtual filesystem first.

For each project:

1. Read project metadata, then project rules.
2. List project knowledge files and subdirectories. Do not miss generic names such as `README.md`.
3. Read active tasks, raw daily logs, schedules, and the central checklist.
4. Reverse-check deployment, verification, infrastructure, DB, CI/CD, observability, research, handover, and cross-team coordination records.
5. Merge records by ticket or business subject rather than listing files or ticket numbers.

Do not rely on date or keyword search alone. MCP search may match paths and names better than body events.

# Reporting Period

- Default `이번 주` to Monday through Sunday.
- If today is before Sunday, report actual work through today and future weekend work only as planned.
- Use recent-seven-day and user-mentioned dates only to audit omissions.
- Do not include out-of-period work unless the user explicitly changes the reporting period.

# Actual Work Date

Determine dates from actual human execution:

- implementation or correction
- development, staging, or production deployment
- verification or smoke test
- analysis, investigation, handover, or documentation
- requirement review, estimate, schedule coordination, or cross-team discussion

Never use these as completion dates without explicit human confirmation:

- ticket status change
- checklist update
- MCP resource creation or update
- report writing
- retrospective cleanup

Keep implementation, development-server deployment, staging deployment, production deployment, and post-deploy verification as separate events.

If actual completion evidence is missing, say `완료일 미확인`. Do not count status cleanup as completed development.

# Date Presentation

Development work does not need a date unless the date affects understanding.

Always mention dates for:

- production or staging deployments
- DB, infrastructure, migration, or configuration operations
- new requests and estimates
- schedule agreements or changes
- cross-team coordination decisions
- deadlines and next-week release windows

When one subject has multiple important dates, join them with commas:

```text
문의하기 기능: BO 목록과 DB 구성을 진행했고, 6/9 엠티처 BO API 연동 방향을 확인했으며, 6/10 에듀플랫폼1팀 협업 예정으로 범위가 변경됐습니다.
```

# Completeness Anchors

Before writing, explicitly check every project for:

- user-facing feature implementation
- backend, frontend, BO, DB, and configuration work
- production and staging deployments
- post-deploy verification
- new requests, feasibility review, and estimates
- schedule coordination and release planning
- external waiting and cross-team collaboration
- domain analysis, handover, and system understanding
- CI/CD, GitLab, Jenkins, ArgoCD, EKS, Grafana, logs, metrics, observability, and infrastructure transition work
- work stored under project subdomains such as `timetable/` or `yeolgong-attendance/`

Do not omit planning or investigation because no code changed. For example, CI/CD and observability requirement analysis is weekly work when the human reviewed current operations, risks, migration requirements, or response content.

# Grouping

Group by project, then business subject.

Within each project, present:

1. `이번 주 작업`
2. `진행 중`
3. `차주 예정`

Avoid ticket numbers unless the user asks for them or disambiguation requires them.

For each subject:

- lead with the subject name
- explain what changed or what value was delivered
- include important collaboration or policy changes
- state the remaining work
- connect next-week action to the current state

# Spoken Output

Write natural Korean suitable for reading aloud.

- Use full, short sentences.
- Avoid branch names, table names, method names, and internal status codes unless necessary.
- Prefer business meaning over implementation detail.
- Avoid repetitive `완료했습니다` endings by varying sentence structure.
- Do not overload one sentence with unrelated work.
- Keep uncertainty explicit but easy to say.

Example:

```text
카드톡 문의하기 기능은 BO 목록 화면과 데이터 구조를 구성했습니다. 이후 엠티처 BO API를 통해 데이터를 전달하는 방향으로 변경됐고, 6월 10일 에듀플랫폼1팀과 협업 예정으로 확인돼 현재 API 규격과 역할 범위를 조율하고 있습니다.
```

# Priority For Next Week

Prioritize next-week work in this order:

1. fixed production deployments, QA, or deadlines
2. work blocked by requirements or cross-team decisions
3. implementation needed for the next release
4. verification of already implemented work
5. longer-term analysis and external waiting

Do not present external waiting as direct implementation. Name the expected input or decision.

# Final Gate

Do not publish until all are true:

- reporting period is explicit and respected
- every production deployment and DB/infrastructure operation in range was checked
- every new request and schedule decision in range was checked
- project subdomains and generic files were checked
- CI/CD, observability, and infrastructure work was checked
- actual execution dates were separated from status-change dates
- subjects include collaboration and policy changes
- output is understandable without ticket numbers
- next-week plans follow from current work and known schedules
