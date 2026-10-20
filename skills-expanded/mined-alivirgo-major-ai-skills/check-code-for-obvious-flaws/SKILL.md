---
name: check-code-for-obvious-flaws
description: "Review generated code for nonexistent APIs, exposed secrets, unhandled errors, and likely edge-case failures."
category: common-sense
risk: safe
source: self
source_type: self
date_added: "2026-08-26"
tags: ["code-review", "zero-trust", "debugging", "security", "syntax-checking", "prompt-engineering"]
tools: ["claude", "cursor", "gemini", "codex", "chatgpt"]
---

# Check Code for Obvious Flaws (Zero-Trust Code Audit) (AI Skill)

## Overview
AI coding assistants are brilliant at scaffolding boilerplate and common algorithms, but they frequently generate code with **invisible runtime flaws**: deprecated library methods, unhandled null/undefined values, unbounded memory allocations, and hardcoded security assumptions.

The **Zero-Trust Code Audit Protocol** provides a structured pre-execution gate to catch syntax errors, security vulnerabilities, and logic flaws before deploying to staging or production.

---

## The 5 Most Dangerous AI Code Traps

```
┌─────────────────────────────────────────────────────────────┐
│                 The Top 5 AI Code Pitfalls                  │
│                                                             │
│  1. Hallucinated APIs     ──► Invented package methods/flags│
│  2. Unhandled Exceptions  ──► Crashes on 404, null, or empty│
│  3. Hardcoded Secrets     ──► API keys or local paths leaked│
│  4. Concurrency Bugs      ──► Race conditions in async/locks│
│  5. Security Injections   ──► Raw string SQL/Bash injection │
└─────────────────────────────────────────────────────────────┘
```

---

## The Pre-Execution Sanity Checklist

Before running any AI-generated script on your local machine or server:

```
[ ] 1. PACKAGE CHECK: Are all imported libraries real and installed via your package manager?
[ ] 2. INJECTION CHECK: Are database queries parameterized (no f-string or string concat SQL)?
[ ] 3. NULL SAFETY: Does the code guard against None, undefined, or missing dictionary keys?
[ ] 4. DESTRUCTIVE ACTIONS: Does the script contain `rm -rf`, `DROP TABLE`, or unconfirmed delete API calls?
[ ] 5. MOCK TEST: Can you run it on sample data or in a Docker sandbox before production?
```

---

## Master Code Audit Prompt Templates

### Pattern 1: The Automated Flaw & Edge-Case Scanner
Use this immediately after an AI writes code:

```markdown
Act as a Principal Staff Security Engineer and SRE.
Critically review the code above for production readiness.

Audit specifically for:
1. **API Validity**: Are any function signatures or methods deprecated or invented?
2. **Failure Modes**: What happens when network timeouts, 500 errors, or corrupt JSON payloads occur?
3. **Security Vulnerabilities**: Check for injection risks, unsanitized inputs, or plain-text credentials.
4. **Boundary Conditions**: Test mentally with empty inputs (`[]`, `""`, `None`, `0`).

Provide the revised, hardened version with comprehensive `try/catch` error handling and type hints.
```

---

### Pattern 2: The Unit Test Generator (Proof of Correctness)
Forces the AI to prove its code works under edge cases:

```markdown
Write a comprehensive test suite (using `pytest` or `vitest`) for the function above.
Include test cases for:
- Happy path (standard valid input)
- Empty/Null input
- Boundary/Overflow input
- Simulated network failure / timeout
```

---

## Real-World Case Study

### Scenario: Processing User File Uploads

#### Fragile AI-Generated Snippet (Full of Flaws)
```python
# ❌ VULNERABLE AI CODE
import os

def save_uploaded_file(file, filename):
    filepath = "/var/www/uploads/" + filename
    file.save(filepath)
    return {"status": "success", "path": filepath}
```
*Flaws: 1) Path traversal attack (`filename = "../../etc/passwd"`), 2) Overwrites existing files, 3) Crashes if directory doesn't exist, 4) No file size or MIME type validation.*

#### Hardened Zero-Trust Audited Version
```python
# ✅ PRODUCTION-HARDENED CODE
import os
import uuid
from pathlib import Path
from werkzeug.utils import secure_filename

UPLOAD_DIR = Path(os.getenv("UPLOAD_DIR", "/var/www/uploads")).resolve()
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".pdf"}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

def save_uploaded_file(file_stream, raw_filename: str, content_length: int) -> dict:
    if content_length > MAX_FILE_SIZE:
        raise ValueError("File exceeds maximum allowed size (10MB)")
        
    sanitized = secure_filename(raw_filename)
    extension = Path(sanitized).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError(f"Unsupported file extension: {extension}")
        
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    unique_filename = f"{uuid.uuid4().hex}_{sanitized}"
    target_path = (UPLOAD_DIR / unique_filename).resolve()
    
    # Ensure no path traversal escaped the upload root
    if not str(target_path).startswith(str(UPLOAD_DIR)):
        raise PermissionError("Path traversal attempt detected")
        
    with open(target_path, "wb") as f:
        f.write(file_stream.read())
        
    return {"status": "success", "filename": unique_filename}
```

---

## Golden Rule of AI Code
> **"Never run AI code you don't understand, and never deploy AI code without testing its failure states."**
