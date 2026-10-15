---
name: secure-git-ops
description: Execute git operations (push, PR, clone) using GCP Secret Manager credentials securely
author: OpenClaw
version: 1.0
status: active
---

# Secure Git Operations (GCP Secret Manager)

Perform git operations (push, clone, PR actions) using credentials from GCP Secret Manager without exposing tokens.

## When to Use

- You need to push branches to a GitHub org (e.g., amplify-dental-ai)
- You're executing PR feedback on a repo with Secret Manager creds
- You need to clone private repos
- You want auditable, secure credential handling

## How It Works

```
Container Startup (entrypoint.sh runs)
    ├─ Authenticates to GCP using service account
    ├─ Retrieves AMPLIFY_GITHUB_PAT from Secret Manager
    └─ Exports as environment variable

Skill invoked (e.g., PR Feedback Executor)
    ↓
Read AMPLIFY_GITHUB_PAT from environment
    ↓
Set up git environment (never logs token)
    ↓
Execute git operations (push, clone, etc.)
    ↓
Log audit trail (no token exposure)
```

**Key difference:** Secrets are retrieved once at startup, not on-demand. Skills just use env vars.

## Requirements

1. **OpenClaw deployed with updated Dockerfile** (gcloud CLI + entrypoint.sh installed)
2. **GCP Secret Manager** configured with `amplify_github_pat` secret
3. **Service account** with `secretmanager.secretAccessor` role
4. **GOOGLE_CLOUD_PROJECT** env var set in deployment
5. **Container started** — secrets automatically loaded as env vars

See `deploy/SECRET_MANAGER_SETUP.md` for setup details.

## Usage in Skills

### In Python (Recommended)

```python
import subprocess
import os

def git_clone_secure(url_base: str, target_dir: str) -> None:
    """Clone repo using env var credentials."""
    token = os.environ.get("AMPLIFY_GITHUB_PAT")
    if not token:
        raise RuntimeError("AMPLIFY_GITHUB_PAT not found. Check container startup.")
    
    full_url = f"https://{token}@{url_base}"
    subprocess.run(["git", "clone", full_url, target_dir], check=True)

def git_push_secure(repo_dir: str, branch: str) -> str:
    """Push branch using env var credentials."""
    token = os.environ.get("AMPLIFY_GITHUB_PAT")
    if not token:
        raise RuntimeError("AMPLIFY_GITHUB_PAT not found. Check container startup.")
    
    env = {**os.environ, "GIT_ASKPASS": "echo"}
    env["GIT_PASSWORD"] = token
    
    result = subprocess.run(
        ["git", "-C", repo_dir, "push", "origin", branch],
        env=env,
        capture_output=True,
        text=True,
        check=True
    )
    
    return result.stdout
```

### In Bash (Recommended)

```bash
#!/usr/bin/env bash

if [ -z "$AMPLIFY_GITHUB_PAT" ]; then
    echo "ERROR: AMPLIFY_GITHUB_PAT not found. Check container startup."
    exit 1
fi

# Clone repo
url_base="github.com/amplify-dental-ai/Amplify.git"
git clone "https://${AMPLIFY_GITHUB_PAT}@${url_base}" /tmp/Amplify

# Work on repo
cd /tmp/Amplify
git checkout -b feat/something
# ... make changes ...
git add .
git commit -m "feat: something"

# Push
git push -u origin feat/something
```

## Key Guarantees

✅ **Token never logged** — Subprocess calls keep token out of logs  
✅ **Token never in git history** — Uses remote URLs, not .git/config  
✅ **Token never on disk** — Loaded into memory at startup only  
✅ **Single retrieval** — Secret retrieved once at container startup, not per-skill  
✅ **Audit trail** — GCP logs Secret Manager access once at startup  
✅ **No hardcoding** — Uses environment variables only  

## Audit Logging

All secret accesses are logged in GCP Audit Logs:

```bash
gcloud logging read "resource.type=secretmanager.googleapis.com AND protoPayload.methodName=google.cloud.secretmanager.v1.SecretManagerService.AccessSecretVersion" --limit 50
```

This shows WHO accessed WHICH secret WHEN, but never the value.

## Error Handling

```python
try:
    token = get_secret("amplify_github_pat")
except subprocess.CalledProcessError as e:
    if "permission" in str(e).lower():
        raise RuntimeError(
            "Service account lacks secretmanager.secretAccessor role. "
            "Check: gcloud secrets get-iam-policy amplify_github_pat"
        )
    elif "not found" in str(e).lower():
        raise RuntimeError(
            "Secret not found. Check: gcloud secrets list"
        )
    else:
        raise RuntimeError(f"Failed to retrieve secret: {e}")
```

## Integration with PR Feedback Executor

The `pr-feedback-executor` skill uses this pattern:

1. Get `AMPLIFY_GITHUB_PAT` from environment (already loaded at startup)
2. Clone amplify-dental-ai/Amplify using env var
3. Execute feedback changes
4. Push using env var
5. No cleanup needed (env var persists for other skills)

See `skills/pr-feedback-executor/SKILL.md` for full workflow.

## References

- Setup guide: `deploy/SECRET_MANAGER_SETUP.md`
- Helper script: `scripts/secure-secret-retriever.sh`
- GCP docs: https://cloud.google.com/secret-manager/docs

