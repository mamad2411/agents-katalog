---
name: skill-github-ops
description: Secure GitHub repository management and API interaction without the GitHub CLI. Optimized for authenticated git operations and permission troubleshooting.
---

# GitHub Operations Workflow

## 1. Authentication with PAT
When the `gh` CLI is unavailable, use Personal Access Tokens (PAT) directly in the remote URL. 
**Security Note:** Never log the full URL. Use `git remote set-url` to update remotes securely.

### URL Formatting
```bash
# Standard format
git remote add origin https://<username>:<token>@github.com/<username>/<repo>.git

# Alternative (x-access-token)
git remote set-url origin https://x-access-token:<token>@github.com/<username>/<repo>.git
```

## 2. Permission Verification (No curl/gh)
If `curl` or `gh` is missing, use Python to verify token scopes and repository access:
```python
import urllib.request, json
url = 'https://api.github.com/repos/<user>/<repo>'
headers = {'Authorization': 'token <token>', 'Accept': 'application/vnd.github.v3+json'}
req = urllib.request.Request(url, headers=headers)
with urllib.request.urlopen(req) as res:
    data = json.loads(res.read().decode())
    print(data.get('permissions'))
```

## 3. Handling Common Errors
- **403 Forbidden:** Usually means the PAT lacks "Contents: Read and Write" permissions. For fine-grained tokens, explicitly check "Repository permissions > Contents".
- **Rejected Push:** If the remote has unique files (LICENSE/README), use `git fetch origin main`, `git rebase origin/main`, and then `git push -f` if safe to align local and remote structures.

## 4. Initializing Professional Repos
Always include a standard folder structure, a descriptive `README.md`, and an `MIT` or `GPL` license file during the initial push.
