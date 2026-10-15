---
name: django-audit
description: Performs a complete technical audit of Django applications, covering security, architecture patterns, performance, database, and code quality. Use this skill whenever you need to review a Django app for bugs, security risks, or technical debt. Supports both English and Portuguese.
---

# Django Technical Audit

This skill guides a rigorous technical audit in Django applications, focusing on security, patterns, performance, and quality.

**Language Note**: You should perform the audit and generate the report in the same language the user is using (e.g., if the user asks in Portuguese, the report should be in Portuguese).

## How to Work

1. **Scan**: Identify the main files of the target directory/app (models, views, urls, forms/serializers, templates, admin, services, tests, migrations).
2. **Evaluation**: Read and evaluate file by file, pointing out inconsistencies with reference to the path and, when possible, the method/class name.
3. **Classification**: Classify each finding by **Severity** (CRITICAL, URGENT, MEDIUM, LOW) and **Category** (Security, Bugs, Django best practices, Performance, DB, Tests, Architecture, Maintainability, Observability, DX/DevOps).
4. **Focus**: Focus on incremental and safe fixes. Do not invent files.

## Audit Checklist

### 1. Security (Mandatory)
- **Authentication & Authorization**: Check use of `@login_required`, `permission_required`, group checks, `user.is_staff`, `user.is_superuser`.
- **Data Exposure**: Check for exposure of tokens, secrets, logs, or debug info.
- **Vulnerabilities**:
    - **SQL Injection**: Use of `.extra()`, `raw()`, f-strings in SQL, or direct concatenation.
    - **XSS**: Templates without escaping or improper use of `safe`/`mark_safe` filters.
    - **CSRF**: Unprotected views in form submissions.
- **Settings**: Check `DEBUG=True` in production, loose `ALLOWED_HOSTS`, missing `SECURE_*` headers, cookies without `Secure/HttpOnly/SameSite`.

### 2. Django Patterns & Architecture
- **Models**: Normalization, validations (`clean`), choices, constraints, indexes.
- **Views**: Logic separation (View vs Service/Layer), avoid excessive business logic in views.
- **Forms/Serializers**: Adequate validation.
- **Admin**: Permissions, `list_display`, `search_fields`.
- **Transactions**: Use of `transaction.atomic()` for operations involving multiple tables.
- **Signals**: Avoid uncontrolled side effects.

### 3. Performance & Database
- **N+1 Queries**: Lack of `select_related` or `prefetch_related`.
- **Indexes**: Absence in FKs and frequent filter fields.
- **Queries**: Heavy queries inside loops or lack of pagination in listings.

### 4. Tests & Quality
- **Coverage**: Existence of tests for critical rules and main flows.
- **Security**: Tests for authorization and permissions.
- **Style**: PEP 8, docstrings, exception handling (avoid `except: pass`).

## Report Format (Deliverable)

The final report must be in Markdown with the following structure:

## 📌 Executive Summary
- 5 to 10 key points focusing on CRITICAL/URGENT risks.

## ✅ Analyzed Inventory
- List of reviewed directories and files (with paths).

## 🚨 Findings by Severity

### CRITICAL
- **[Category]** path/file.py::ClassOrFunction
- **Impact**: ...
- **Risk**: ...
- **How to fix**: Detailed steps.
- **Suggested Test**: How to validate the fix.

*(Repeat for URGENTE, MÉDIO and BAIXO as needed)*

## 🧪 Recommended Test Plan
- List of new tests to create, grouped by area.

## 🛠️ Suggested Fixes (Prioritized)
- Ordered checklist from most critical to least critical.

## 🧭 Next Steps
- Recommendations for incremental improvement (refactor, patterns, tooling).

---

## 🛠️ Utility Scripts

The skill includes a script to facilitate the execution of audit tools:

- `scripts/audit_check.py`: Runs automatic checks (Django deploy check, Bandit, Ruff, pip-audit).
  - **Automation**: The script creates an isolated virtual environment (`.audit_venv`), installs audit tools, and attempts to install project dependencies (`requirements.txt`) for a complete and safe analysis.
  - Usage: `python scripts/audit_check.py [app_dir]`
