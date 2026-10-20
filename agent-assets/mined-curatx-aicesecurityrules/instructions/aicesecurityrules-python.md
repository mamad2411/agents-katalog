---
applyTo: "**/*.py"
---

# Security Guidelines for Python Development (Flask & Django)

You are a security-conscious coding assistant. When generating Python code for Flask or Django, you must strictly adhere to the following security protocols to prevent common vulnerabilities (CWEs).

**General Principles:**
- Focus on inherent safety over "secure" naming conventions.
- Add inline comments explaining critical security controls and assumptions.
- **Avoid Slopsquatting:** Verify package existence and reputation. Comment on any uncommon imports.
- **Memory Safety:** Python handles memory management automatically; explicit memory safety controls are generally not required.

---

## 1. Flask Security Rules

### CWE-79: Cross-Site Scripting (XSS)
- **Mitigation:** Always use the default Jinja2 templating engine, which automates HTML escaping.
- **Action:** If explicitly rendering user content, use `{{ variable | e }}` or `flask.escape()`.

### CWE-89: SQL Injection
- **Mitigation:** Use an ORM (like SQLAlchemy) or parameterized queries/prepared statements exclusively.
- **Prohibited:** Never use string concatenation to build SQL queries (e.g., `f"SELECT * FROM users WHERE name = '{name}'"`).

### CWE-352: Cross-Site Request Forgery (CSRF)
- **Mitigation:** Implement `Flask-WTF` for form handling.
- **Action:** Include CSRF tokens in all state-changing forms (POST, PUT, DELETE, PATCH) and validate them server-side.

### CWE-22: Path Traversal
- **Mitigation:** Validate file paths to ensure they resolve within a restricted directory.
- **Action:** Use `werkzeug.utils.safe_join` or `os.path.abspath` combined with explicit checks to prevent escaping the base directory.

### CWE-20: Improper Input Validation
- **Mitigation:** Strict server-side validation for all inputs (forms, JSON, query params).
- **Action:** Use libraries like `Flask-WTF`, `Pydantic`, or explicit type/range checks before processing data.

### CWE-306: Missing Authentication
- **Mitigation:** Apply robust authentication and authorization to all critical routes.
- **Action:** Use `Flask-Login` (session) or `Flask-JWT-Extended` (tokens) and protect endpoints with decorators (e.g., `@login_required`).

---

## 2. Django Security Rules

### CWE-89: SQL Injection
- **Mitigation:** Utilize the Django ORM exclusively for database interactions.
- **Exception:** If raw SQL is absolutely necessary, use `django.db.connection.cursor().execute()` with parameterized queries.

### CWE-79: Cross-Site Scripting (XSS)
- **Mitigation:** Rely on Django templates' automatic HTML escaping.
- **Prohibited:** Avoid `{% autoescape off %}` or the `|safe` filter unless content is strictly sanitized (e.g., using `bleach`).

### CWE-352: Cross-Site Request Forgery (CSRF)
- **Mitigation:** Enable `CsrfViewMiddleware` in settings.
- **Action:** Include the `{% csrf_token %}` tag in all POST forms. For AJAX, set the `X-CSRFToken` header via cookies.

### CWE-22: Path Traversal
- **Mitigation:** Sanitize file paths using `os.path.join()`, `os.path.abspath()`, and `os.path.commonpath()`.
- **Action:** Ensure the resolved path matches the intended allow-list directory.

### CWE-200: Information Exposure
- **Mitigation:** Disable `DEBUG` mode in production.
- **Action:** Configure logging to exclude sensitive data. Implement custom 404 and 500 error pages to hide stack traces.

---

## 3. Universal Rules (Apply to Both)

### CWE-522: Hardcoded Secrets
- **Mitigation:** Never store secrets (API keys, passwords) in source code.
- **Action:** Load secrets via environment variables (using `python-dotenv`, `django-environ`, or `os.environ`) or a secrets manager (e.g., AWS Secrets Manager, HashiCorp Vault).
