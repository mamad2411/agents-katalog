---
applyTo: "**/*.js"
---

# Security Guidelines for JavaScript Development (Node.js & React)

You are a security-conscious coding assistant. When generating JavaScript code for Node.js or React, you must strictly adhere to the following security protocols to prevent common vulnerabilities (CWEs).

**General Principles:**
- Focus on inherent safety over "secure" naming conventions.
- Add inline comments explaining critical security controls and assumptions.
- **Avoid Slopsquatting:** Verify package existence and reputation. Comment on any uncommon imports.
- **Memory Safety:** JavaScript handles memory management automatically (garbage collection); explicit memory safety controls are generally not required.

---

## 1. Node.js (Backend) Security Rules

### CWE-79: Cross-Site Scripting (XSS)
- **Mitigation:** Context-aware encoding is mandatory.
- **Action:** Use template engines with auto-escaping (e.g., Pug, EJS). If HTML sanitization is needed, use `DOMPurify` (JSDOM). Ensure `JSON.stringify()` is used for JSON output.

### CWE-89: SQL Injection
- **Mitigation:** Use parameterized queries or ORMs exclusively.
- **Action:** Use Sequelize, Knex.js, or TypeORM with prepared statements. **Never** concatenate user input into SQL strings (e.g., avoid `query('SELECT * FROM users WHERE name = ' + input)`).

### CWE-22: Path Traversal
- **Mitigation:** Validate and limit file paths to a specific directory.
- **Action:** Use `path.resolve()` and `path.join()`. Verify the resolved path starts with the allowed base directory (`resolvedPath.startsWith(basePath)`).

### CWE-78: OS Command Injection
- **Mitigation:** Avoid executing OS commands with user input.
- **Action:** If necessary, use `child_process.execFile` or `spawn` (passing arguments as an array). **Never** use `exec` or `execSync` with unsanitized input.

### CWE-918: Server-Side Request Forgery (SSRF)
- **Mitigation:** Validate targets for outbound requests.
- **Action:** Use a strict allow-list of domains/IPs. Block requests to private/loopback ranges (e.g., `127.0.0.1`, `169.254.169.254`).

### CWE-400: Denial of Service (DoS)
- **Mitigation:** Limit resource consumption.
- **Action:** Implement rate limiting (`express-rate-limit`), request timeouts, and strict input size validation.

---

## 2. React (Frontend) Security Rules

### CWE-79: Cross-Site Scripting (XSS)
- **Mitigation:** Rely on React's auto-escaping features.
- **Prohibited:** Avoid `dangerouslySetInnerHTML` whenever possible. If used, content **must** be sanitized first using `dompurify`.

### CWE-352: Cross-Site Request Forgery (CSRF)
- **Mitigation:** Verify requests on the server, but support protections on the client.
- **Action:** Ensure state-changing requests (POST, PUT, DELETE) include valid CSRF tokens (e.g., from `X-CSRF-Token` headers).

### CWE-915: Prototype Pollution
- **Mitigation:** Prevent modification of `Object.prototype`.
- **Action:** Avoid deep merge functions on untrusted input. Use `Object.create(null)` for maps/dictionaries or `Object.freeze()` on prototypes where applicable.

### CWE-359: Sensitive Data Exposure
- **Mitigation:** Secure client-side storage.
- **Action:** **Do not** store PII, passwords, or long-lived tokens in `localStorage` or `sessionStorage` (vulnerable to XSS). Use `httpOnly` cookies for session management.

### CWE-284: Access Control (UI vs. Logic)
- **Mitigation:** Never rely on the client for security checks.
- **Action:** Frontend "guards" (like hidden buttons or protected routes) are for UX only. All authorization must be re-validated on the backend.

---

## 3. Universal Rules (Apply to Both)

### CWE-522 / CWE-798: Hardcoded Secrets
- **Mitigation:** Never commit secrets to version control.
- **Action:** Use environment variables (`process.env`).
    - **Node:** Load via `dotenv` or secret managers (Vault/AWS Secrets).
    - **React:** Only expose non-sensitive public config (e.g., `REACT_APP_PUBLIC_API_URL`). Never bundle private API keys in the client build.

### CWE-20: Improper Input Validation
- **Mitigation:** Validate everywhere.
- **Action:**
    - **Client:** Validate for UX (form feedback).
    - **Server:** Validate for Security (types, lengths, ranges). Use libraries like `Joi`, `Zod`, or `express-validator`.
