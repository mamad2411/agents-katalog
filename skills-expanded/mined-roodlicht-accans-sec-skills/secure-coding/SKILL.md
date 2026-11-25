---
name: secure-coding
description: Language-agnostic secure-coding patterns — input validation, injection-safe APIs, authN/authZ, crypto, secrets, dependency hygiene. The default lens when no framework-specific skill applies.
---

# Secure Coding Standards

## When to use

This skill is the substrate layer for code work. It triggers when Claude is writing or reviewing code and there's no framework-specific skill that goes deeper.

Activates on:

- A question like "is this safe?", "review for security issues", "could someone abuse this?", "what could go wrong?".
- New code that takes untrusted input, handles secrets, performs auth, touches crypto, or talks to external systems.
- A patch or PR review without a sharper skill (such as `django-security` or `api-security`) active.
- As a backstop for code generation in a language without a specific skill (Go, Rust, C#, PHP, Kotlin).

### When NOT to use (handoff to sharper skills)

- Framework-specific: Django → `django-security`, Rails → `rails-security`, Spring Boot → `spring-security`, Next.js → `nextjs-security`.
- API design or REST/GraphQL endpoints → `api-security`.
- Infrastructure: Terraform/Ansible/Pulumi → `iac-security`, Dockerfile or OCI → `container-hardening`, Kubernetes manifests → `k8s-security`, CI/CD workflows → `cicd-hardening`.
- Vulnerability triage on dependencies → `cve-triage`, SBOM and provenance → `supply-chain`, secrets in git history → `secrets-scanner`.
- Full PR review as a workflow (not just patterns) → `security-review`. This skill is its pattern library.

If one of the above skills applies, use that first. `secure-coding` remains relevant for the parts they don't cover.

## Approach

Six phases. Work through them sequentially during a review. When generating code you can jump between them depending on what you're writing. Each phase has the same shape: **rule → code signal (red flags to spot) → do/don't**.

The phases correspond to OWASP Top 10 2021 and Proactive Controls v3, but here they are organized in the order a developer encounters them in practice.

### 1. Map trust boundaries

The first question with any piece of code: where does untrusted data enter, and which code runs with more privilege than the data producer?

- **Inventory trust sources.** HTTP parameters, headers, cookies, file uploads, database content (previously written by an untrusted source), environment variables in multi-tenant contexts, message queues, cross-service RPC, files from object storage.
- **Separate privilege zones.** Setuid binaries, service accounts, cloud IAM roles, container caps: every privilege escalation crosses a trust boundary. Code running with elevated privilege must treat input as if it were a fresh attack.
- **Data integrity at serialization boundaries.** Every place you serialize (JSON, protobuf, custom binary, YAML) or deserialize is a boundary. A signature plus integrity check belongs with data that travels between trust zones (think JWT, cookies, cached computations).

**Red flag — trust loss.** Code that says "this comes from the database so it's safe" — unless you've also validated the write path to that database, that's an assumption. Cached untrusted data is still untrusted.

### 2. Input validation and output encoding

Two separate concerns that often get conflated. Validate at the boundary (parse, don't validate-after-parse); encode at the output point based on the destination context.

- **Allowlist over denylist.** Validate on type, length, format, range, character class. "Anything except `<script>`" is a denylist and always loses to encoding tricks, Unicode homoglyphs, or new payload shapes.
- **Parse, don't validate.** Where possible, convert input into a type that enforces the invariant (`int`, UUID, enum) instead of passing the string along with a separate validation check. See Alexis King's "Parse, don't validate".
- **Context-aware output encoding.** The same string must be escaped differently in HTML body, HTML attribute, JavaScript string, URL query, CSS value, and shell argument. Use framework primitives (`safe_join`, template auto-escape, `shlex.quote`).
- **Parameterized queries for every query language.** SQL via prepared statements, OS commands via arg-array instead of shell-string, LDAP via escaped filters, XPath via variable binding, templates via auto-escape mode (Jinja2 `autoescape=True`, ERB `h()`, etc.).

**Red flags in code:**
```
# SQL — string interpolation in query
cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
cursor.execute("SELECT * FROM users WHERE id = " + user_id)

# Command — shell=True with user input
subprocess.Popen(f"git clone {url}", shell=True)
os.system("convert " + filename + " out.png")

# Template — raw HTML insertion
element.innerHTML = userInput        # JS/DOM
v-html="userInput"                   # Vue
dangerouslySetInnerHTML={{ __html }} # React
{{ user.bio | safe }}                # Jinja2 with | safe on untrusted
```

**Safe variants:**
```
# SQL
cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))       # psycopg2
db.query("SELECT * FROM users WHERE id = $1", userID)                 # Go
PreparedStatement s = conn.prepareStatement("SELECT ... WHERE id = ?") # Java

# Command
subprocess.run(["git", "clone", url], check=True)                     # no shell
child_process.execFile("git", ["clone", url])                         # Node

# Template — keep auto-escape on by default, deliberately disable only for trusted data
```

### 3. Identity: authentication, sessions, authorization

No hand-rolled auth. Use vetted frameworks (Spring Security, Django auth, auth.js, Devise, Keycloak, Auth0). If you do build something yourself, build it around a vetted primitive only.

- **Password hashing: argon2id (preferred), scrypt, or bcrypt.** Never MD5, SHA-1, SHA-256 without a KDF, no PBKDF2 with low iteration counts. Use library defaults; custom parameters are a red flag.
- **MFA from day one for admin and privileged accounts.** TOTP, WebAuthn/passkeys, push-based. SMS is a legacy fallback, not primary.
- **Sessions: signed, HttpOnly, Secure, SameSite=Lax or Strict, short TTL, rotate on privilege change.** No session ID in URL.
- **Authorization per resource, not per route.** IDOR (Insecure Direct Object Reference) happens when `/api/documents/123` only checks authentication and not whether the actor may see `123`. Check ownership or role on every lookup path.
- **Fail-closed default.** No access unless explicitly granted. Middleware that returns "allow" on an unknown route is a bug.

**Red flags:**
```
# Password handling
hashlib.md5(password.encode()).hexdigest()
hashlib.sha256(password.encode()).hexdigest()    # no salt, no KDF
bcrypt.hashpw(password, bcrypt.gensalt(4))       # cost factor too low

# Session
document.cookie = "sid=" + sessionId             # JS can read it → XSS steals
session.permanent = True                         # without TTL set

# AuthZ
@app.route("/api/documents/<id>")
def get_doc(id):
    return Document.objects.get(id=id)           # no ownership check

# Generic "is logged in" as the only check
if (user.isAuthenticated()) { return adminPanel }
```

### 4. Secrets, keys, crypto

Implementing crypto yourself is the classic foot-gun. Use high-level APIs. For secrets: never in source, ideally in a vault, env-vars are acceptable as a secondary path.

- **Secrets management hierarchy.** Vault (HashiCorp Vault, AWS Secrets Manager, GCP Secret Manager, Azure Key Vault) > platform-provided injection (K8s secret, ECS task role) > env-var on host > `.env` file outside git. Never in source, never in logs, never in error messages.
- **Key rotation + per-environment separation.** Dev/staging/prod never share keys. Rotate on a schedule and on suspicion of leak. Keep the previous key briefly to allow graceful rotation.
- **Symmetric crypto: AES-GCM or ChaCha20-Poly1305.** ECB never. CBC only with verified HMAC. Unique nonce per message.
- **Asymmetric: Ed25519 for signatures, X25519 for key exchange, RSA ≥ 3072 bits as legacy.** MD5/SHA-1 are dead for signatures.
- **TLS 1.2+ minimum, 1.3 preferred. Certificate validation always on.** `verify=False` in requests/curl is a staging hack, not a production config.
- **Randomness: `os.urandom` / `crypto.randomBytes` / `SecureRandom`.** Never `Math.random()` / `random.random()` for security purposes (tokens, IDs, nonces).

**Red flags:**
```
# Hardcoded secrets
const API_KEY = "sk-proj-..."
db_password = "Welcome2024!"
# AWS / GitHub / Slack tokens in source → caught with gitleaks or trufflehog

# Crypto wrong
cipher = AES.new(key, AES.MODE_ECB)              # ECB
requests.get(url, verify=False)                  # TLS validation off
token = str(random.random())                     # not crypto-safe
hashlib.sha1(data).hexdigest()                   # for signatures/integrity

# Key management
KEY = "hardcoded-32-byte-string-right-here"       # also as env-var fallback
```

### 5. Robustness: errors, deserialization, logging

What happens when something goes wrong? Fail closed, no sensitive data in errors, no dangerous deserialization, structured logging without secrets.

- **Exception handling: catch specifically, not generically.** `catch (Exception e) { }` (Java/C#) or `except: pass` (Python) masks bugs that may be security-relevant. Log the error, return a generic message to the user.
- **No stack traces or internal paths to the client.** Production error pages show `request-id`, not `/home/app/lib/.../db.py line 47 in _execute`.
- **Deserialization of untrusted data is RCE-prone with native formats.** Java `ObjectInputStream`, Python `pickle.loads`, PHP `unserialize`, Ruby `Marshal.load`, YAML `yaml.load` (without SafeLoader), .NET `BinaryFormatter`. Use JSON, protobuf, or msgpack with schema validation.
- **Signed integrity for cross-boundary data.** JWTs must be validated with the *expected* algorithm (prevent `alg: none` and algorithm confusion). Cookies that encode server state are signed with HMAC.
- **Logging hygiene.** Never log passwords, tokens, card numbers, API keys, PII (BSN, full email, etc.). Mask at the source, not at the log pipeline. Do log security events: auth failures, authz denials, admin actions, rate-limit hits.

**Red flags:**
```
# Swallowed exceptions
try: risky()
except: pass
catch (Exception e) { /* empty */ }

# Dangerous deserialization
pickle.loads(request.body)
yaml.load(user_input)                            # without Loader=SafeLoader
ObjectInputStream ois = new ObjectInputStream(sock.getInputStream())

# JWT
jwt.decode(token, key, algorithms=None)          # accept any alg
jwt.decode(token, None, options={"verify_signature": False})

# Logging
logger.info(f"Login for {user.email} with password {password}")
logger.error(f"Payment {card_number} failed")
```

### 6. Dependencies and runtime hygiene

Inherited vulnerabilities through libraries are the largest share of modern exploits (OWASP A06). Treat this as a first-class concern.

- **Pin.** `package-lock.json` / `poetry.lock` / `Gemfile.lock` / `go.sum` committed in git. Transitive dep versions must be reproducible.
- **Generate an SBOM.** CycloneDX or SPDX via `cyclonedx-bom`, `syft`, `sbom-tool`. In CI, every build. See the `supply-chain` skill for provenance.
- **Vulnerability scanning.** Dependabot/Renovate for updates, `osv-scanner` or `grype` for scans, Snyk/Mend for enterprise. Scan on a per-PR basis, not just nightly.
- **Typosquatting defence.** Look critically at new dependencies: author, age, download trend, scoped name. Consider an internal mirror for critical packages.
- **Runtime minimalism.** Container does not run as root. Filesystem read-only where possible. Seccomp/AppArmor defaults on. Egress network policies. See `container-hardening` and `k8s-security` for depth.
- **Update cadence.** Critical CVE in a direct dependency: patch within days. In a transitive: risk-weighted via `cve-triage` (reachable path plus EPSS).

**Red flags:**
```
# requirements.txt without version pin
requests
flask

# package.json with caret on everything (^) → auto-drift
"dependencies": { "lodash": "^4.0.0" }

# Dockerfile
FROM node:latest           # latest tag = unreproducible
USER root                  # or no USER directive
ADD http://... /app/       # ADD with URL bypasses integrity

# Runtime
process.env.NODE_ENV not "production" in prod
DEBUG=True in production config (Django, Flask)
```

## Output

When this skill is used for a code review or scan, it produces a structured report. During code generation the skill works "silently": it influences what you write but produces no separate output.

Report structure for review:

```
Findings per phase:
  1. Trust boundaries: <ok | issues: ...>
  2. Input/output: <ok | issues with file:line>
  3. Identity: <ok | issues with file:line>
  4. Secrets/crypto: <ok | issues with file:line>
  5. Robustness: <ok | issues with file:line>
  6. Dependencies: <ok | issues with versions>

Per issue:
- Phase: <1–6>
- Location: <file:line>
- Classification: <CWE-ID, OWASP A0x>
- Severity: <blocker | high | medium | low>
- Pattern: <short name, e.g. "SQL string concat", "pickle.loads", "verify=False">
- Fix: <concrete suggestion, ideally with code alternative>
- Handoff: <if applicable: use <skill-id> for deeper review>

Overall conclusion: <blocker count, overall verdict>
```

Always tie issues to a CWE-ID where possible — that's the language tools (SAST, CI, issue trackers) speak. Use only CWE numbers you can verify; mark with `[verify: CWE]` when in doubt (see `verification-loop` Layer 2).

## References

- OWASP Top 10 2021 — [https://owasp.org/Top10/](https://owasp.org/Top10/). The canonical list of application risk categories; every finding maps to an A0x.
- OWASP Proactive Controls v3 — [https://owasp.org/www-project-proactive-controls/](https://owasp.org/www-project-proactive-controls/). What developers should *do* (as opposed to Top 10 which describes what goes wrong).
- OWASP ASVS v4 — [https://owasp.org/www-project-application-security-verification-standard/](https://owasp.org/www-project-application-security-verification-standard/). Verification checklist at three levels; usable as a requirement set for new services.
- OWASP Cheat Sheet Series — [https://cheatsheetseries.owasp.org/](https://cheatsheetseries.owasp.org/). Per-topic depth (Input Validation, Authentication, Session Management, Cryptographic Storage, etc.). Summarize and link, don't transcribe.
- CWE Top 25 — [https://cwe.mitre.org/top25/](https://cwe.mitre.org/top25/). Class-level catalogue; use CWE-IDs in findings for tool interoperability.
- NIST SP 800-218 (SSDF v1.1) — [https://csrc.nist.gov/pubs/sp/800/218/final](https://csrc.nist.gov/pubs/sp/800/218/final). Secure Software Development Framework; procedural context for these patterns.
- SEI CERT Coding Standards — [https://wiki.sei.cmu.edu/confluence/display/seccode](https://wiki.sei.cmu.edu/confluence/display/seccode). Language-specific rule sets for C/C++/Java/Perl; consult for per-language detail.
- Alexis King — "Parse, don't validate" ([https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/](https://lexi-lambda.github.io/blog/2019/11/05/parse-don-t-validate/)). The framing behind the input-validation pattern in phase 2.

## Categories

- core
- appsec
