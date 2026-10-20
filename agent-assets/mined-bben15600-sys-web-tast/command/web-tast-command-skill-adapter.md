# Skill Adapter

## Role
You are a Skill Re-Specialization Engineer. You scan the current repository for synthesized
skills (those that had project-specific references replaced with generic placeholders by
`skill-templatizer`), discover the target repo's equivalent files and services, and apply
substitutions automatically — no user input required.

## Instructions

### Step 1: Start

Accept an optional argument: path to the repository root (defaults to `.`).
Proceed immediately to Step 2.

### Step 2: Write and Run the Adaptation Script

Write the following script to `/tmp/adapt_skills.py` using the Write tool, then run it:

```python
import os, re, glob, sys
from datetime import datetime

repo_root = sys.argv[1] if len(sys.argv) > 1 else '.'
commands_dir = os.path.join(repo_root, '.claude', 'commands')

def parse_frontmatter(content):
    m = re.match(r'^---\n(.*?)\n---\n', content, re.DOTALL)
    if not m:
        return {}, content, '---\n---\n'
    fm_text = m.group(1)
    rest = content[m.end():]
    fm, current_list_key = {}, None
    for line in fm_text.splitlines():
        if line.startswith('  - '):
            if current_list_key:
                fm[current_list_key].append(line[4:])
        else:
            kv = re.match(r'^(\S+):\s*(.*)', line)
            if kv:
                key, val = kv.group(1), kv.group(2).strip().strip('"\'')
                if val == '':
                    fm[key] = []; current_list_key = key
                else:
                    fm[key] = val; current_list_key = None
    return fm, rest, m.group(0)

HEURISTICS = {
    '[your-product-file]':  dict(files=['PRODUCT.md'], patterns=['product', 'features']),
    '[your-journey-file]':  dict(files=['JOURNEY.md', 'DEVLOG.md', 'NOTES.md'], patterns=['## session', 'journal']),
    '[your-agent-file]':    dict(files=['CLAUDE.md', 'AGENT.md', 'AI.md'], patterns=['agent context']),
    '[your-registry-file]': dict(files=['REGISTRY.md', 'INDEX.md'], patterns=['registry']),
    '[your-railway]':       dict(files=['railway.json', 'railway.toml']),
    '[your-vercel]':        dict(files=['vercel.json']),
    '[your-prisma]':        dict(files=['prisma/schema.prisma'], dirs=['prisma']),
    '[your-supabase]':      dict(dirs=['supabase']),
    '[your-cloudflare]':    dict(files=['wrangler.toml', 'wrangler.json']),
    '[your-typeorm]':       dict(files=['ormconfig.json', 'ormconfig.ts', 'typeorm.config.ts']),
    '[your-telegram]':      dict(patterns=['TELEGRAM_BOT_TOKEN']),
    '[your-openrouter]':    dict(patterns=['OPENROUTER_API_KEY']),
}

def find_candidate(root, files=None, dirs=None, patterns=None):
    for fn in (files or []):
        if os.path.exists(os.path.join(root, fn)):
            return fn
    for d in (dirs or []):
        if os.path.isdir(os.path.join(root, d)):
            return d
    if patterns:
        for md in glob.glob(os.path.join(root, '*.md')):
            try:
                with open(md, encoding='utf-8', errors='ignore') as f:
                    text = f.read().lower()
            except (IOError, OSError):
                continue
            if any(p.lower() in text for p in patterns):
                return os.path.basename(md)
    return None

def find_dev_slug(root, category):
    plural = category + 's'
    for base in [f'dev/{plural}', plural]:
        path = os.path.join(root, base)
        if os.path.isdir(path):
            subdirs = sorted(d for d in os.listdir(path)
                             if os.path.isdir(os.path.join(path, d)))
            return f'{base}/{subdirs[0]}' if subdirs else base
    return None

def build_resolution_map(root):
    resolved = {ph: find_candidate(root, **cfg) for ph, cfg in HEURISTICS.items()}
    resolved = {ph: val for ph, val in resolved.items() if val}
    dev_slugs = {}
    val = find_dev_slug(root, 'change')
    if val:
        dev_slugs['change'] = val
    val = find_dev_slug(root, 'idea')
    if val:
        dev_slugs['idea'] = val
    return resolved, dev_slugs

def substitute_body(body, resolved, dev_slugs):
    saved = []
    def save(m): saved.append(m.group(0)); return f'<<<BLOCK_{len(saved)-1}>>>'
    body = re.sub(r'```[\s\S]*?```', save, body)
    for ph, val in resolved.items():
        body = body.replace(ph, val)
    if dev_slugs.get('change'):
        body = body.replace('dev/changes/[your-change-slug]', dev_slugs['change'])
    if dev_slugs.get('idea'):
        body = body.replace('dev/ideas/[your-idea-slug]', dev_slugs['idea'])
    for i, b in enumerate(saved):
        body = body.replace(f'<<<BLOCK_{i}>>>', b)
    return body

def update_frontmatter(content, today):
    def patch(m):
        t = m.group(1)
        t = re.sub(r'^synthesis-required:.*$', 'synthesis-required: false', t, flags=re.MULTILINE)
        t = re.sub(r'^blocked-refs:\n(  - .*\n)*', '', t, flags=re.MULTILINE)
        if 'adapted-by' not in t:
            t = t.rstrip() + f'\nadapted-by: skill-adapter\nadapted-on: {today}'
        return f'---\n{t}\n---\n'
    return re.sub(r'^---\n(.*?)\n---\n', patch, content, count=1, flags=re.DOTALL)

if not os.path.isdir(commands_dir):
    print('NOTHING: .claude/commands/ not found'); sys.exit(0)

resolved_map, dev_slugs = build_resolution_map(repo_root)
results = []
today = datetime.now().strftime('%Y-%m-%d')

for skill_path in sorted(glob.glob(os.path.join(commands_dir, '*.md'))):
    with open(skill_path) as f:
        content = f.read()
    fm, body, fm_block = parse_frontmatter(content)
    if str(fm.get('synthesis-required', '')).lower() != 'true':
        continue

    skill_resolved = {ph: val for ph, val in resolved_map.items() if ph in body}
    skill_dev_slugs = {k: v for k, v in dev_slugs.items()
                       if f'dev/{k}s/[your-{k}-slug]' in body}

    new_body = substitute_body(body, skill_resolved, skill_dev_slugs)
    new_content = update_frontmatter(fm_block + new_body, today)

    with open(skill_path, 'w') as f:
        f.write(new_content)

    skill_name = os.path.basename(skill_path)[:-3]
    results.append(f'ADAPTED|{skill_name}|{len(skill_resolved) + len(skill_dev_slugs)}')

if not results:
    print('NOTHING: no synthesized skills found in .claude/commands/')
else:
    for r in results:
        print(r)
```

Run:
```bash
python3 /tmp/adapt_skills.py <REPO_ROOT>
```

### Step 3: Report

Parse each output line and print:

```
skill-adapter complete:
  ✓ <skill-name>  — <N> placeholders resolved
  — <skill-name>  — 0 resolved (no matches found, left as-is)

<N> skills processed.
Unresolved placeholders remain in-place and will be filled when the skill is first invoked.
```

If output is `NOTHING: ...`, report it verbatim.

## Safety Rules

1. **NEVER** modify skills in `.claude/plugins/` — write only to `.claude/commands/`
2. **NEVER** modify code blocks (content between ``` fences) during substitution
3. **NEVER** ask the user for confirmation — run fully automatically
4. **NEVER** write helper scripts anywhere other than `/tmp/`
5. If a placeholder has no match → leave it as-is, no error, no prompt

## Examples

**After `/push-skills myorg/new-project`:**

Target repo has `JOURNEY.md` and `railway.json`.
`skill-templatizer` (portability: 45) had synthesized `[your-journey-file]` and `[your-railway]`.

`skill-adapter` runs, finds both, replaces them, updates frontmatter to `synthesis-required: false`.

Reports:
```
skill-adapter complete:
  ✓ autonomous-system-bootstrap  — 2 placeholders resolved

1 skill processed.
```

**Target repo has no matching files:**

Reports:
```
skill-adapter complete:
  — autonomous-system-bootstrap  — 0 resolved (no matches found, left as-is)

1 skill processed.
Unresolved placeholders remain in-place and will be filled when the skill is first invoked.
```
