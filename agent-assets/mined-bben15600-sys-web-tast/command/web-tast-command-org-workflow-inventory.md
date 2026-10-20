# Org Workflow Inventory

## Role
You are an Org Automation Auditor who scans every GitHub Actions workflow across an organization
in real time and prints a structured inventory table to chat.

## Context — Read First
- GitHub API does not expose a `creator` field on workflow files — creator must be derived from
  the first commit that introduced the file (commit history API).
- Skill link attribution is heuristic: parsed from the first commit message. It will be `—`
  for workflows not created via a skill.
- Rate limit: 5,000 req/hr. Orgs with 100+ repos × many workflows may hit this. The script
  throttles automatically but large orgs may produce partial results.

## Instructions

### Step 1: Resolve Parameters

Collect (ask if not provided):
- `ORG` — GitHub organization name
- `GH_TOKEN` — resolve from env via `/env-key`

### Step 2: Run the Inventory Scanner

Write and run the following script:

```bash
python3 << 'EOF'
import urllib.request, urllib.error, json, os, base64, re, time

ORG = os.environ.get('ORG', 'bben15600-sys')
TOKEN = os.environ['GH_TOKEN']
HEADERS = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github+json',
}

def gh(path, retries=2):
    url = f'https://api.github.com{path}'
    for attempt in range(retries + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req) as r:
                remaining = int(r.headers.get('X-RateLimit-Remaining', 999))
                if remaining < 20:
                    time.sleep(2)
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
            if attempt < retries:
                time.sleep(2 ** attempt)
    return None

def paginate(path):
    results, page = [], 1
    while True:
        batch = gh(f'{path}{"&" if "?" in path else "?"}per_page=100&page={page}')
        if not batch:
            break
        items = batch if isinstance(batch, list) else batch.get('workflows', [])
        results.extend(items)
        if len(items) < 100:
            break
        page += 1
    return results

def get_workflow_scope(content_yaml, org):
    if 'workflow_call' in content_yaml:
        return 'org-wide (reusable)'
    if f'{org}/' in content_yaml and 'uses:' in content_yaml:
        return 'caller (enrolled repos)'
    return 'per-repo'

def extract_tokens(content_yaml):
    tokens = set(re.findall(r'secrets\.(\w+)', content_yaml))
    if 'GITHUB_TOKEN' in content_yaml or 'github.token' in content_yaml:
        tokens.add('GITHUB_TOKEN')
    return ', '.join(sorted(tokens)) if tokens else '—'

def get_first_commit(repo_full, filepath):
    """Return (date, author, message) of the oldest commit for this file.
    GitHub returns newest-first; fetching page=1 gives newest, last page gives oldest.
    We probe page=1 to detect existence, then jump to last page via Link header."""
    url = f'https://api.github.com/repos/{repo_full}/commits?path={filepath}&per_page=100&page=1'
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req) as r:
            link = r.headers.get('Link', '')
            batch = json.loads(r.read())
    except urllib.error.HTTPError:
        return '—', '—', ''
    if not batch:
        return '—', '—', ''
    # Parse last page number from Link header if present
    last_page = 1
    m = re.search(r'page=(\d+)>;\s*rel="last"', link)
    if m:
        last_page = int(m.group(1))
    if last_page > 1:
        batch = gh(f'/repos/{repo_full}/commits?path={filepath}&per_page=100&page={last_page}') or batch
    first = batch[-1]
    date = first.get('commit', {}).get('author', {}).get('date', '—')[:10]
    author = first.get('commit', {}).get('author', {}).get('name', '—')
    message = first.get('commit', {}).get('message', '')
    return date, author, message

def extract_skill_link(commit_message):
    """Heuristic: look for skill name in commit message."""
    patterns = [
        r'feat\(skills\).*?add\s+([\w-]+)',
        r'feat\(([\w-]+)\)',
        r'sync\(([\w-]+)\)',
        r'ci:\s+add\s+([\w-]+)',
        r'chore.*?([\w-]+-skill)',
    ]
    for pat in patterns:
        m = re.search(pat, commit_message, re.IGNORECASE)
        if m:
            return f'/{m.group(1)}'
    return '—'

# --- Main scan ---
print(f'\nScanning org: {ORG}...\n')
repos = paginate(f'/orgs/{ORG}/repos?type=all')
repo_names = [r['full_name'] for r in repos]

rows = []
for repo_full in repo_names:
    workflows_data = gh(f'/repos/{repo_full}/actions/workflows')
    if not workflows_data:
        continue
    workflows = workflows_data.get('workflows', [])
    for wf in workflows:
        wf_path = wf.get('path', '')
        wf_name = os.path.basename(wf_path)

        content_data = gh(f'/repos/{repo_full}/contents/{wf_path}')
        if not content_data or 'content' not in content_data:
            continue
        try:
            yaml_content = base64.b64decode(content_data['content']).decode('utf-8', errors='replace')
        except Exception:
            yaml_content = ''

        scope = get_workflow_scope(yaml_content, ORG)
        tokens = extract_tokens(yaml_content)
        created, creator, msg = get_first_commit(repo_full, wf_path)
        skill_link = extract_skill_link(msg)

        repo_short = repo_full.replace(f'{ORG}/', '')
        rows.append((wf_name, repo_short, scope, created, creator, tokens, skill_link))

# --- Output table ---
print(f'## Org Automation Inventory — {ORG}')
print(f'Total workflows found: {len(rows)}\n')
print(f'| Workflow | Repo | Scope | Created | Creator | Tokens | Skill |')
print(f'|----------|------|-------|---------|---------|--------|-------|')
for wf_name, repo, scope, created, creator, tokens, skill in sorted(rows, key=lambda r: (r[2], r[1])):
    print(f'| `{wf_name}` | `{repo}` | {scope} | {created} | {creator} | `{tokens}` | {skill} |')
EOF
```

### Step 3: Annotate Results

After the table prints, add a short legend:

```
Scope legend:
  org-wide (reusable)   — lives in central repo, called by all enrolled repos
  caller (enrolled repos) — 6-line caller deployed to N repos
  per-repo              — runs only in the repo where it lives

Token legend:
  GITHUB_TOKEN          — built-in, no setup needed
  CLAUDE_SKILLS_PAT  — org secret, set once at org level
  (any other)           — repo or org secret, check visibility
```

## Safety Rules

1. **NEVER print token values** — only print token names parsed from the YAML.
2. **NEVER modify any workflow file** — this skill is read-only.
3. **If rate limit is hit** (`X-RateLimit-Remaining < 10`), stop and report partial results
   with a note: "Rate limit reached — N of M repos scanned."
4. **Skill link is heuristic** — always show `—` rather than guessing when no pattern matches.

## Examples

**User:** "show me all automations in the org"

**Agent behaviour:**
Resolves ORG=bben15600-sys from context, injects GH_TOKEN. Runs scanner across all org repos.
Prints table with 4 workflows: `skill-sync-reusable.yml` (org-wide, claude-Skills, created
2026-04-19, bben15600-sys-commits, CLAUDE_SKILLS_PAT + GITHUB_TOKEN, /org-skill-pipeline),
`distribute-skills.yml` (org-wide), `skill-sync.yml` (caller, 67 repos), and
`documentation-enforcement.yml` (per-repo). Adds scope legend below.

**User:** "audit workflows — who created the skill-sync workflow and from which skill?"

**Agent behaviour:**
Runs scanner, filters results to `skill-sync*.yml` files. Shows creator `bben15600-sys-commits`,
created `2026-04-19`, skill link `/org-skill-pipeline`. If commit message had no matching
pattern, reports skill link as `—` with a note that attribution is heuristic only.
