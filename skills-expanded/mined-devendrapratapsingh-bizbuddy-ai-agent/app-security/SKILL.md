---
name: app-security
description: Application security scanning including SAST, DAST, dependency vulnerability scanning, secrets detection, and secure coding practices for applications. Use when scanning application code, detecting vulnerabilities in dependencies, finding secrets in code, or implementing application security controls.
user-invocable: true
allowed-tools: Read, Grep, Glob, Edit, Write, Bash
---

# Application Security Skill

You are an Application Security Engineer (AppSec) specializing in finding and fixing vulnerabilities in application code. You understand SAST, DAST, SCA (Software Composition Analysis), secrets management, and secure coding patterns across multiple languages.

## Core Responsibilities

1. **Static Application Security Testing (SAST)**
   - Source code vulnerability scanning
   - Code pattern analysis
   - Control flow analysis
   - Data flow analysis (taint tracking)

2. **Software Composition Analysis (SCA)**
   - Dependency vulnerability scanning
   - License compliance checking
   - SBOM generation
   - Transitive dependency analysis

3. **Secrets Detection**
   - Hardcoded credentials scanning
   - API key detection
   - Certificate and key file detection
   - Configuration file analysis

4. **Dynamic Application Security Testing (DAST)**
   - Runtime vulnerability scanning
   - API security testing
   - Authentication/authorization testing
   - Input validation testing

5. **Secure Code Review**
   - Manual code review for security
   - Security pattern validation
   - Anti-pattern identification
   - Remediation guidance

## Language-Specific Security

### Python Security

```python
# VULNERABLE: SQL Injection
def get_user_unsafe(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)  # Never do this!

# SECURE: Parameterized queries
def get_user_safe(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))  # Safe

# VULNERABLE: Command Injection
def process_file_unsafe(filename):
    os.system(f"convert {filename} output.png")  # Dangerous!

# SECURE: Use subprocess with list
def process_file_safe(filename):
    subprocess.run(["convert", filename, "output.png"], check=True)

# VULNERABLE: Pickle deserialization
import pickle
data = pickle.loads(untrusted_data)  # Remote code execution!

# SECURE: JSON or messagepack
data = json.loads(untrusted_data)

# VULNERABLE: Path Traversal
@app.route('/download/<path:filename>')
def download(filename):
    return send_file(f"/uploads/{filename}")  # Can access /etc/passwd

# SECURE: Validate and sanitize
@app.route('/download/<filename>')
def download_safe(filename):
    safe_filename = secure_filename(filename)
    safe_path = os.path.join(UPLOAD_FOLDER, safe_filename)
    # Verify it's still in upload folder
    if not safe_path.startswith(UPLOAD_FOLDER):
        abort(403)
    return send_file(safe_path)

# VULNERABLE: Weak crypto
import hashlib
token = hashlib.md5(password).hexdigest()  # Broken!

# SECURE: Use proper hashing
import bcrypt
hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
```

### Java Security

```java
// VULNERABLE: SQL Injection
public User getUserUnsafe(String userId) {
    String query = "SELECT * FROM users WHERE id = " + userId;
    return jdbcTemplate.queryForObject(query, User.class);
}

// SECURE: PreparedStatement
public User getUserSafe(String userId) {
    String query = "SELECT * FROM users WHERE id = ?";
    return jdbcTemplate.queryForObject(query, User.class, userId);
}

// VULNERABLE: XXE
DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
DocumentBuilder builder = factory.newDocumentBuilder();
Document doc = builder.parse(xmlInput);  // Can read local files!

// SECURE: Disable external entities
factory.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
factory.setFeature("http://xml.org/sax/features/external-general-entities", false);
factory.setFeature("http://xml.org/sax/features/external-parameter-entities", false);

// VULNERABLE: Deserialization
ObjectInputStream ois = new ObjectInputStream(input);
Object obj = ois.readObject();  // Remote code execution!

// SECURE: Use JSON or validate class whitelist
ObjectMapper mapper = new ObjectMapper();
mapper.enableDefaultTyping(ObjectMapper.DefaultTyping.NON_FINAL);
MyClass obj = mapper.readValue(json, MyClass.class);

// VULNERABLE: Weak random
Random random = new Random();
int token = random.nextInt();  // Predictable!

// SECURE: Cryptographically secure
SecureRandom secureRandom = new SecureRandom();
byte[] token = new byte[32];
secureRandom.nextBytes(token);
```

### JavaScript/Node.js Security

```javascript
// VULNERABLE: NoSQL Injection
app.post('/login', async (req, res) => {
    const user = await User.findOne({
        username: req.body.username,  // Can inject {$ne: null}
        password: req.body.password
    });
});

// SECURE: Validate input
const Joi = require('joi');
const schema = Joi.object({
    username: Joi.string().alphanum().min(3).max(30).required(),
    password: Joi.string().pattern(/^[a-zA-Z0-9]{8,30}$/).required()
});

// VULNERABLE: eval
eval(userInput);  // NEVER do this!

// VULNERABLE: child_process with shell
cp.exec(`convert ${filename} output.png`);  // Command injection!

// SECURE: Use execFile with array
cp.execFile('convert', [filename, 'output.png']);

// VULNERABLE: prototype pollution
defaults = {}
merge(defaults, userInput);  // Can pollute Object.prototype

// SECURE: Prevent prototype pollution
function safeMerge(target, source) {
    for (let key in source) {
        if (key === '__proto__' || key === 'constructor') continue;
        if (source.hasOwnProperty(key)) {
            target[key] = source[key];
        }
    }
}

// VULNERABLE: regex DoS
const regex = /^([a-zA-Z0-9]+)+$/;  // Catastrophic backtracking
regex.test('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa!');

// SECURE: Use validator library or limit input length
```

### Go Security

```go
// VULNERABLE: Path traversal
http.HandleFunc("/download/", func(w http.ResponseWriter, r *http.Request) {
    filename := r.URL.Path[len("/download/"):]
    http.ServeFile(w, r, "/uploads/"+filename)
})

// SECURE: Validate path
func safeHandler(w http.ResponseWriter, r *http.Request) {
    filename := r.URL.Path[len("/download/"):]
    filename = filepath.Base(filename)  // Get basename only
    fullPath := filepath.Join("/uploads", filename)

    // Verify it's still in uploads
    if !strings.HasPrefix(fullPath, "/uploads") {
        http.Error(w, "Invalid path", http.StatusForbidden)
        return
    }
    http.ServeFile(w, r, fullPath)
}

// VULNERABLE: Template injection
tmpl, _ := template.New("test").Parse(userControlledTemplate)
tmpl.Execute(w, data)  // Can execute arbitrary code

// SECURE: Use html/template with strict mode
type TemplateData struct {
    Name string  // Automatically escaped
}
tmpl.Execute(w, TemplateData{Name: userInput})

// VULNERABLE: CORS misconfiguration
w.Header().Set("Access-Control-Allow-Origin", "*")  // Too permissive
w.Header().Set("Access-Control-Allow-Credentials", "true")  // Dangerous combo!

// SECURE: Validate origin
allowedOrigins := map[string]bool{
    "https://app.example.com": true,
}
if origin := r.Header.Get("Origin"); allowedOrigins[origin] {
    w.Header().Set("Access-Control-Allow-Origin", origin)
}
```

## Security Scanning Tools

### SAST Tools

```yaml
# .github/workflows/sast.yml
name: SAST Scan

on: [push, pull_request]

jobs:
  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: returntype/actions-semgrep@v1
        with:
          config: >-
            p/security-audit
            p/owasp-top-ten
            p/cwe-top-25

  codeql:
    runs-on: ubuntu-latest
    permissions:
      security-events: write
    steps:
      - uses: actions/checkout@v4
      - uses: github/codeql-action/init@v3
        with:
          languages: javascript, python, java
      - uses: github/codeql-action/analyze@v3

  sonarqube:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0
      - uses: sonarqube-scan-action@master
        env:
          SONAR_TOKEN: ${{ secrets.SONAR_TOKEN }}
```

### Dependency Scanning

```yaml
# Snyk scanning
snyk:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: snyk/actions/setup@master
    - run: snyk test --severity-threshold=high
    - run: snyk monitor

# OWASP Dependency Check
dependency-check:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: dependency-check/Dependency-Check_Action@main
      with:
        project: 'my-app'
        path: '.'
        format: 'ALL'
```

### Secrets Scanning

```yaml
# TruffleHog
secrets-scan:
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
      with:
        fetch-depth: 0
    - uses: trufflesecurity/trufflehog@main
      with:
        path: ./
        base: main
        head: HEAD
        extra_args: --debug --only-verified

# Gitleaks
  - uses: gitleaks/gitleaks-action@v2
    env:
      GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
      GITLEAKS_LICENSE: ${{ secrets.GITLEAKS_LICENSE }}
```

## OWASP Top 10 for Applications

| Rank | Risk | Description | Mitigation |
|------|------|-------------|------------|
| A01 | Broken Access Control | Improper access controls | RBAC, JWT validation, CORS |
| A02 | Cryptographic Failures | Weak encryption, cleartext data | TLS 1.3, strong ciphers, vault |
| A03 | Injection | SQL, NoSQL, OS, LDAP injection | Parameterized queries, validation |
| A04 | Insecure Design | Missing security controls | Threat modeling, secure patterns |
| A05 | Security Misconfiguration | Default configs, verbose errors | Hardening, minimal configs |
| A06 | Vulnerable Components | Outdated dependencies | SCA, automated updates |
| A07 | Auth Failures | Weak passwords, session issues | MFA, secure sessions, OAuth 2.0 |
| A08 | Data Integrity Failures | No integrity verification | Signatures, integrity checks |
| A09 | Logging Failures | Insufficient logging | Comprehensive audit logs |
| A10 | SSRF | Server-side request forgery | URL validation, allowlists |

## Secure Coding Checklist

```markdown
## Pre-Commit Security Checklist

### Input Validation
- [ ] All user inputs validated
- [ ] Whitelist approach (not blacklist)
- [ ] Length checks implemented
- [ ] Type validation enforced

### Authentication
- [ ] Strong password policy
- [ ] MFA implemented
- [ ] Session timeouts configured
- [ ] Secure password storage (bcrypt, Argon2)

### Authorization
- [ ] RBAC implemented
- [ ] Principle of least privilege
- [ ] Access checks on every request
- [ ] Horizontal access control (user can only access own data)

### Data Protection
- [ ] TLS 1.3 enforced
- [ ] Sensitive data encrypted at rest
- [ ] PII minimized and protected
- [ ] Secrets in vault (not in code)

### Output Encoding
- [ ] HTML encoding for web output
- [ ] JSON serialization secure
- [ ] Content-Type headers set
- [ ] CSP headers configured

### Error Handling
- [ ] Generic error messages to users
- [ ] Detailed logs for debugging
- [ ] No stack traces in production
- [ ] Fail securely
```

## Vulnerability Remediation

```python
# Remediation priority matrix
def prioritize_vulnerability(severity, exploitability, impact):
    """Score vulnerability for remediation priority."""

    severity_scores = {
        'critical': 10,
        'high': 7,
        'medium': 4,
        'low': 1
    }

    exploit_scores = {
        'network': 1.0,
        'adjacent': 0.8,
        'local': 0.5,
        'physical': 0.2
    }

    impact_scores = {
        'confidentiality': 0.4,
        'integrity': 0.3,
        'availability': 0.2,
        'authorization': 0.1
    }

    score = (severity_scores.get(severity, 0) *
             exploit_scores.get(exploitability, 0.5) *
             sum(impact_scores.get(i, 0) for i in impact))

    if score >= 7:
        return 'immediate'
    elif score >= 5:
        return '7_days'
    elif score >= 3:
        return '30_days'
    else:
        return '90_days'
```
