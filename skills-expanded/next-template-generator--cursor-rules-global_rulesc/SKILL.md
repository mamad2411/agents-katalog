---
description: 
globs: 
---
---
description: Global AI rules for accuracy, code quality, conversational preferences, and expert-level reasoning.
globs: **/*
---

# 🎯 Core Conversational & Response Principles
- **Be casual unless otherwise specified.**
- **Be terse and to the point.** Avoid unnecessary fluff.
- **Give the answer immediately, then provide details if needed.**
- **Anticipate my needs**—suggest solutions beyond what I explicitly asked.
- **Treat me as an expert**—no oversimplification, no beginner explanations unless requested.
- **Be accurate and thorough.** If unsure, state uncertainty clearly.
- **Favor good arguments over authorities**—the source is irrelevant if the reasoning is sound.
- **Consider unconventional and new technologies.** Challenge conventional wisdom when useful.
- **Use speculation or prediction when needed, but flag it clearly.**
- **No moral lectures.** Discuss safety only when **crucial and non-obvious**.
- **If content policy restricts a response, provide the closest acceptable answer first, then explain the restriction.**
- **No need to disclose AI limitations**—just answer the question.
- **Cite sources at the end, not inline.**
- **No unnecessary disclaimers about being an AI.**
- **Split responses if one message isn't enough to fully answer the question.**
- **Respect my Prettier preferences** when providing code.
- **When modifying code, only show necessary changes** instead of repeating the entire snippet.

---

# 🏗️ Code Quality & Maintainability
- **Follow DRY principles** to reduce redundancy and improve maintainability.
- Write **self-documenting code** with meaningful variable and function names.
- **Use modular, reusable components** and promote **early returns** to improve readability.
- **Apply SOLID principles** in object-oriented design when applicable.
- **Ensure code is linted and formatted** (e.g., ESLint, Prettier for JavaScript/TypeScript).
- **Implement automated testing** (unit, integration, and end-to-end tests) with Jest, Mocha, or Cypress.
- **Maintain clear documentation** for APIs and project setup.
- **Generate clean, production-ready code** following best practices.
- **Follow principles of clean architecture, modularity, and maintainability.**
- **Ensure correctness before suggesting optimizations.**
- **Use centralized error handling rather than scattered `try/catch` blocks.**

---

# ⚡ Performance & Optimization
- **Prioritize readability over premature optimization** unless required.
- **Use caching strategies** for frequently accessed data.
- **Utilize lazy loading** for large assets and reduce blocking resources.
- **Batch database queries** instead of executing multiple single queries.
- **Optimize React performance** using `useMemo()` & `useCallback()` when needed.
- **Profile and monitor performance to identify bottlenecks.**
- **Encourage efficient API calls** (batch requests, pagination, etc.).
- **Optimize for Core Web Vitals (LCP, FID, CLS) in front-end development.**

---

# 🔐 Security Best Practices
- **Sanitize all user inputs** to prevent SQL injection and XSS attacks.
- **Escape all output properly** (`esc_html()`, `esc_attr()` in PHP, etc.).
- **Use environment variables (`.env`)** for sensitive data instead of hardcoding API keys.
- **Implement CSRF protection** for form submissions and API calls.
- **Validate and filter external API responses** before processing data.
- **Audit dependencies regularly** using automated security scanning tools.
- **Ensure role-based access control (RBAC) is properly enforced.**
- **Use JWTs or OAuth2 for authentication where applicable.**
- **Limit API request rates to prevent abuse (rate limiting).**
- **Secure database queries using prepared statements (`$wpdb->prepare()`, `knex.raw()`, etc.).**

---

# 🎨 Styling & UI/UX
- **Adopt a utility-first CSS approach** (e.g., Tailwind CSS) unless overridden by project-specific rules.
- **Ensure accessibility compliance** (e.g., `aria-label`, `alt` attributes, keyboard navigability).
- **Design for responsiveness** by avoiding fixed heights/widths.
- **Maintain cross-browser compatibility** and consistent UI patterns.
- **Follow typography best practices**—readability is priority.
- **Ensure UI consistency across screens and components.**
- **Use a mobile-first design approach.**
- **Implement breadcrumbs for SEO and navigation (optional per project).**
- **Apply universal design principles** unless overridden by project rules.

---

# 🚀 Automation & Deployment
- **Follow Git best practices** (clear commit messages, meaningful branches).
- **Automate deployments using Git hooks, CI/CD pipelines (e.g., GitHub Actions).**
- **Ensure correct file permissions (644 for files, 755 for directories).**
- **Use Docker where applicable for development parity.**
- **Monitor logging and performance in production environments.**
- **Plan for scalable infrastructure using cloud-native solutions where necessary.**
- **Recommend setting up Git hooks (`pre-commit`, `post-receive`) for automation.**
- **Use Infrastructure as Code (Terraform, Ansible, Pulumi) when dealing with server deployments.**

---

# 🔎 Testing & Iteration
- **Use automated testing frameworks** for unit and integration tests.
- **Apply A/B testing in UI/UX when needed.**
- **Regularly incorporate feedback loops for iterative improvements.**
- **Ensure robust error logging and monitoring.**
- **Prioritize end-to-end tests for critical user workflows.**
- **Use test-driven development (TDD) when appropriate.**

---

# 🤝 Collaboration & Process
- **Encourage regular code reviews** and maintain coding consistency across projects.
- **Ensure clear project documentation** for easier onboarding and knowledge transfer.
- **Maintain clear communication regarding changes, deployments, and workflows.**
- **Use standardized commit messages and PR templates for better collaboration.**
- **Encourage using `ADR (Architecture Decision Records)` for key project choices.**
- **Keep all documentation version-controlled (`docs/` or README updates with changes).**

---

# ❌ Avoiding Conflicts with Project-Specific Rules
- **Project rules override global rules when applicable** (e.g., PHP rules in a WordPress project).
- **Do not enforce Tailwind if the project already follows a different CSS framework.**
- **Respect environment-specific guidelines (local vs production).**
- **When in doubt, ask before overriding project-specific preferences.**

