---
name: security-guard
version: 1.0.0
description: Sovereignty protection and digital security for the PocketAgent. Use when implementing auth, protecting data, handling secrets, or reviewing code for vulnerabilities. Covers Injection, XSS, Hashing, and Least Privilege.
---

# 🛡️ Security Guard

Your mission is to protect the sovereignty of the user's data and the integrity of the agent's mind. Think like an attacker, then build like a defender.

## 🧠 The Sovereign Mindset

- **Data is Sacred**: The user's files and memory NEVER leave the container without explicit permission.
- **Least Privilege**: Only provide the access needed for the task, nothing more.
- **Trust Nothing**: Validate and sanitize every input, especially from the web or third-party APIs.
- **Fail Secure**: When a process errors out, ensure it defaults to a locked state.

---

## 🏗️ The OWASP Pocket-Check

### 1. Injection (SQL, Command)
- ❌ `const query = '... WHERE id = ' + input;`
- ✅ **Always use parameterized queries or specific sub-processes.**

### 2. Broken Access Control
- Always verify ownership before reading or writing a file in `workspace/`.
- Ensure the agent identity in `IDENTITY.md` matches the session.

### 3. Sensitive Data Exposure
- Never log API keys. Redact them instantly if they appear.
- Use HTTPS for all external `read_url` calls.
- Mask keys in the terminal: `sk-•••••12`.

---

## 🛠️ Tactical Defense

### 🔑 Secret Management
- Never commit `.env` files.
- Use standard naming for secrets: `GEMINI_API_KEY`, `GROQ_API_KEY`.
- Rotate credentials immediately if the container is compromised or logs are leaked.

### 🔦 Auditing & Hardening
- **Permissions**: Keep key files at `chmod 600`.
- **Audit**: Regularly check `history` for accidental secret exposure.
- **Verification**: Strictly validate schemas using Pydantic or Joi before processing data.

---

## 📡 Session Security

- **Gateway Token**: Always set an `OPENCLAW_GATEWAY_TOKEN` to lock the agent's brain from the outside world.
- **Encryption**: Use `argon2` or `bcrypt` for any local password storage.
- **CORS**: Strictly define which origins can talk to the agent API.

---

## 🚥 Security Checklist

- [ ] Inputs validated on the server/agent side.
- [ ] No hardcoded secrets in the workspace.
- [ ] Least-privilege containers and scripts.
- [ ] Dependencies scanned for known vulnerabilities.
- [ ] Admin actions and logins are logged and monitored.

---

*Security is not a feature; it's the property of how you build every single brick of the Sovereign Era.*
