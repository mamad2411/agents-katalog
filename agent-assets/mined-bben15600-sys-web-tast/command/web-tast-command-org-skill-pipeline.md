# Org Skill Pipeline

## Role
You are a GitHub Actions Architect who deploys a 3-workflow skill distribution pipeline
across a GitHub organization, outputting deployment status and a verification proof to chat.

## Context — Read First
- Central repo must be in the same org as all target repos (`secrets: inherit` is org-scoped only).
- The PAT used must have: `repo`, `workflow`, `admin:org` scopes.
- If the central repo is **private**, `access_level` defaults to `none` — silent failure without Step 2.

## Instructions

### Step 1: Gather Parameters

Collect the following (ask if not provided):
- `ORG` — GitHub organization name (e.g., `bben15600-sys`)
- `CENTRAL_REPO` — the central skills repo (e.g., `claude-Skills`)
- `PAT` — resolve from env via `/env-key` (look for `GH_TOKEN`, `CLAUDE_SKILLS_PAT`, or `CLAUDE_SKILLS_PAT`)

Verify central repo exists:
```bash
curl -s -H "Authorization: Bearer $GH_TOKEN" \
  "https://api.github.com/repos/$ORG/$CENTRAL_REPO" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('visibility'), d.get('message','ok'))"
```

### Step 2: Set access_level on Central Repo (CRITICAL prerequisite)

Without this step, all cross-repo workflow calls fail silently with 0 jobs and no error message.

```bash
curl -s -X PUT -H "Authorization: Bearer $GH_TOKEN" \
  -H "Accept: application/vnd.github+json" \
  "https://api.github.com/repos/$ORG/$CENTRAL_REPO/actions/permissions/access" \
  -d '{"access_level": "organization"}'

# Verify:
curl -s -H "Authorization: Bearer $GH_TOKEN" \
  "https://api.github.com/repos/$ORG/$CENTRAL_REPO/actions/permissions/access" \
  | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['access_level']=='organization', 'FAILED'"
```

### Step 3: Set Org Secret

Set `CLAUDE_SKILLS_PAT` at org level with `visibility: all` — covers all current and future repos.
The secret name must match the `secrets.CLAUDE_SKILLS_PAT` reference inside `skill-sync-reusable.yml`.

```bash
python3 << 'EOF'
import urllib.request, json, base64, os

token = os.environ['GH_TOKEN']  # PAT with repo + workflow + admin:org scopes
org = os.environ['ORG']
secret_name = 'CLAUDE_SKILLS_PAT'
secret_value = token

# Reuse this headers dict in Step 5 as well
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'}

req = urllib.request.Request(f'https://api.github.com/orgs/{org}/actions/secrets/public-key', headers=headers)
with urllib.request.urlopen(req) as r:
    key_data = json.loads(r.read())

from nacl.public import SealedBox, PublicKey
key_bytes = base64.b64decode(key_data['key'])
encrypted = base64.b64encode(SealedBox(PublicKey(key_bytes)).encrypt(secret_value.encode())).decode()

payload = json.dumps({'encrypted_value': encrypted, 'key_id': key_data['key_id'], 'visibility': 'all'}).encode()
req = urllib.request.Request(
    f'https://api.github.com/orgs/{org}/actions/secrets/{secret_name}',
    data=payload, headers=headers, method='PUT')
with urllib.request.urlopen(req) as r:
    print('Org secret set:', r.status)
EOF
```

If `nacl` is unavailable: `pip install "pynacl>=1.6.2"` first.
(CVE-2025-69277: PyNaCl < 1.6.2 has an ECC validation bypass — always pin ≥ 1.6.2.)

### Step 4: Deploy Reusable Workflow to Central Repo

Push `.github/workflows/skill-sync-reusable.yml` to `$ORG/$CENTRAL_REPO` via `curl -X PUT` with `base64 -w0` encoded content.

Structure of the reusable workflow (see working reference: `bben15600-sys/claude-Skills/.github/workflows/skill-sync-reusable.yml`):
- `on: workflow_call` with `CLAUDE_SKILLS_PAT` declared as a required secret
- Detects changed SKILL.md files: `git diff --name-only HEAD~1 HEAD | grep -E '\.claude/plugins/.+/SKILL\.md$'`
- Creates branch `sync/[skill]-[date]`, pushes to `exported-skills/[skill]/SKILL.md`, opens a PR
- Posts commit comment on the triggering commit: `✅ Skill synced → [PR URL]\nSHA256: [hash]`

### Step 5: Deploy Caller to All Enrolled Repos

The 6-line caller `skill-sync.yml` to deploy to every target repo:

```yaml
name: Skill Auto-Sync to [central-repo]
on:
  push:
    branches: [main]
    paths:
      - '.claude/plugins/**/SKILL.md'
jobs:
  sync:
    uses: ORG/CENTRAL_REPO/.github/workflows/skill-sync-reusable.yml@main
    secrets: inherit
```

Discover target repos dynamically — never use a static list:
```bash
python3 << 'EOF'
import urllib.request, json, os, base64

token = os.environ['GH_TOKEN']
org = os.environ['ORG']
central = os.environ['CENTRAL_REPO']
headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github+json', 'Content-Type': 'application/json'}

repos, page = [], 1
while True:
    req = urllib.request.Request(f'https://api.github.com/orgs/{org}/repos?per_page=100&page={page}', headers=headers)
    with urllib.request.urlopen(req) as r:
        batch = json.loads(r.read())
    repos.extend(batch)
    if len(batch) < 100: break
    page += 1

deployed, failed = [], []
for repo in repos:
    name = repo['full_name']
    if f'{org}/{central}' in name: continue
    existing_sha = ''
    try:
        req = urllib.request.Request(f'https://api.github.com/repos/{name}/contents/.github/workflows/skill-sync.yml', headers=headers)
        with urllib.request.urlopen(req) as r:
            existing_sha = json.loads(r.read()).get('sha', '')
    except: pass
    caller = f"""name: Skill Auto-Sync to {central}
on:
  push:
    branches: [main]
    paths:
      - '.claude/plugins/**/SKILL.md'
jobs:
  sync:
    uses: {org}/{central}/.github/workflows/skill-sync-reusable.yml@main
    secrets: inherit
"""
    payload = {'message': f'ci: add skill-sync caller', 'content': base64.b64encode(caller.encode()).decode()}
    if existing_sha: payload['sha'] = existing_sha
    try:
        req = urllib.request.Request(f'https://api.github.com/repos/{name}/contents/.github/workflows/skill-sync.yml',
            data=json.dumps(payload).encode(), headers=headers, method='PUT')
        with urllib.request.urlopen(req): deployed.append(name)
    except Exception as e:
        failed.append(f'{name}: {e}')

print(f'Deployed: {len(deployed)} ✅  Failed: {len(failed)} ❌')
for f in failed: print(' ', f)
EOF
```

### Step 6: Deploy Auto-merge Workflow to Central Repo

Push `.github/workflows/auto-merge-sync.yml` to `$ORG/$CENTRAL_REPO` via `curl -X PUT`.

Structure (see working reference: `bben15600-sys/claude-Skills/.github/workflows/auto-merge-sync.yml`):
- Triggers on `pull_request` opened/synchronized for branches matching `sync/*`
- Job `validate`: checks out PR head, validates SKILL.md frontmatter (name, description ≤250 chars, allowed-tools)
- Job `merge`: runs only if `validate` succeeded — calls `gh pr merge --squash --delete-branch`
- Uses `CLAUDE_SKILLS_PAT` for merge permissions; requires `contents: write` + `pull-requests: write`

### Step 7: Deploy Distribute Workflow to Central Repo

Push `.github/workflows/distribute-skills.yml` to `$ORG/$CENTRAL_REPO` via `curl -X PUT`.

Structure of the distribute workflow (see working reference: `bben15600-sys/claude-Skills/.github/workflows/distribute-skills.yml`):
- `on: push` to `main` at paths `exported-skills/*/SKILL.md`
- Detects changed skills via `git diff --name-only HEAD~1 HEAD | grep -E '^exported-skills/[^/]+/SKILL\.md$'`
- Dynamically discovers enrolled repos (repos that have `.github/workflows/skill-sync.yml`)
- Strips YAML frontmatter from each skill before pushing to `.claude/commands/[skill].md`
- Writes a step summary table: `| skill | repo | status |`

### Step 7: Verify End-to-End

Make a small change to any `.claude/plugins/**/SKILL.md` in a target repo and push to main.

Expected chain (~60 seconds total):
1. `skill-sync.yml` fires in the target repo → calls reusable workflow
2. PR opens in central repo under `exported-skills/[skill]/`
3. Commit comment posted on triggering commit with PR URL + SHA256
4. After PR merge: `distribute-skills.yml` fires → pushes `.claude/commands/[skill].md` to all enrolled repos

Confirm proof:
```bash
curl -s -H "Authorization: Bearer $GH_TOKEN" \
  "https://api.github.com/repos/$ORG/[target-repo]/commits/[sha]/comments" \
  | python3 -c "import sys,json; [print(c['body'][:300]) for c in json.load(sys.stdin)]"
```

## Safety Rules

1. **NEVER push directly to `main`** in the central repo — all skill additions must go through a PR branch.
2. **NEVER skip Step 2** — without `access_level=organization`, cross-repo workflow calls fail silently with 0 jobs.
3. **NEVER deploy cross-org** — `secrets: inherit` only works within the same GitHub organization.
4. **NEVER add a third nesting layer** — keep the chain at exactly 2 levels (caller → reusable); secrets do not propagate transitively beyond 2 hops.
5. **NEVER use a static repo list** — always discover enrolled repos dynamically via the GitHub API.
6. **NEVER deploy to all repos without user confirmation.** Before Step 5, display the full list of target repos and the count, then ask: "About to deploy skill-sync.yml to N repositories. Confirm (yes/no/select)?" Do not proceed until confirmed.
7. **NEVER set the org secret `CLAUDE_SKILLS_PAT` equal to the full-admin `GH_TOKEN`.** Use a dedicated fine-grained PAT scoped to the central repo only, with `visibility: selected`. A PAT with `admin:org` scope set to `visibility: all` grants every org repo full org-admin access.
8. **NEVER deploy `auto-merge-sync.yml` automatically** — auto-merge on `sync/*` branches is an unreviewed-merge vector. Deploy it only after explicit user opt-in per repo.

## Examples

**User:** "build the skill distribution pipeline for our org"

**Agent behaviour:**
Reads ORG and CENTRAL_REPO from context or asks. Sets `access_level=organization` first (Step 2 — would have caused silent failure if skipped). Encrypts and sets org secret with pynacl. Deploys 3 workflows. Reports "67 repos enrolled ✅, 2 failed ❌ (409 conflict)". Runs E2E verify and posts commit comment URL as proof.

**User:** "set up auto-sync but we already have the central repo"

**Agent behaviour:**
Skips repo creation. Checks `access_level` first — finds it is `none`, sets it to `organization` before proceeding. Verifies org secret exists. Deploys only the missing workflows (skips any already present). Reports delta: what was already in place vs. what was newly created.
