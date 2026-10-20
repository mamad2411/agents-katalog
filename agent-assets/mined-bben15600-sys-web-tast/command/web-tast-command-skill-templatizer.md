# Skill Templatizer

## Role
You are a Skill Portability Engineer. You automatically classify every new SKILL.md as globally
portable or project-specific, synthesize placeholders where needed, and copy the result to
`exported-skills/` so it is ready for `/push-skills`.

## Instructions

### Step 1: Locate the Skill

Accept the path to the SKILL.md file as the argument (e.g.,
`.claude/plugins/claude-skills-std/skills/my-skill/SKILL.md`).

Extract the skill name: the directory name immediately before `/SKILL.md` in the path.

### Step 2: Write and Run the Process Script

Write the following script to `/tmp/process_skill.py` using the Write tool, then run it:

```python
import sys, re, os

src_path = sys.argv[1]
dst_path = sys.argv[2]

with open(src_path, 'r') as f:
    content = f.read()

# Strip code blocks before scanning to avoid penalising documented examples
body = re.sub(r'```[\s\S]*?```', '', content)

PROJECT_FILES = {
    'PRODUCT.md':  '[your-product-file]',
    'JOURNEY.md':  '[your-journey-file]',
    'AGENT.md':    '[your-agent-file]',
    'REGISTRY.md': '[your-registry-file]',
}
SERVICES = ['Railway', 'Supabase', 'Telegram', 'OpenRouter', 'TypeORM', 'Prisma', 'Vercel', 'Cloudflare']

score = 100
blocked = []

def penalise(label, amount):
    global score
    if label not in blocked:
        blocked.append(label)
        score -= amount

for m in re.findall(r'dev/(?:changes|ideas)/[\w-]+', body):
    penalise(m, 15)
for ref in PROJECT_FILES:
    if ref in body:
        penalise(ref, 15)
for svc in SERVICES:
    if svc in body:
        penalise(svc, 10)
for p in re.findall(r'`(/(?!tmp)[^`\s]{3,})`', body):
    penalise(p, 15)

fm_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
if fm_match:
    src_exp_match = re.search(r'^source-experiment:\s*"?(\S+?)"?\s*$', fm_match.group(1), re.MULTILINE)
    if src_exp_match and src_exp_match.group(1) != 'core':
        penalise('non-core source-experiment', 20)

score = max(0, min(100, score))
synthesis_required = score < 80
out = content

if synthesis_required:
    saved = []
    def save(block_match):
        saved.append(block_match.group(0))
        return f'<<<BLOCK_{len(saved)-1}>>>'
    out = re.sub(r'```[\s\S]*?```', save, out)

    out = re.sub(r'dev/(changes|ideas)/[\w-]+',
                 lambda m: f'dev/{m.group(1)}/[your-{m.group(1)[:-1]}-slug]', out)
    for ref, ph in PROJECT_FILES.items():
        out = out.replace(ref, ph)
    for svc in SERVICES:
        out = out.replace(svc, f'[your-{svc.lower()}]')

    # Restore code blocks before applying frontmatter-scoped substitution
    for i, block in enumerate(saved):
        out = out.replace(f'<<<BLOCK_{i}>>>', block)

    out = re.sub(r'(source-experiment:\s*)[^\n]+', r'\1core', out, count=1)

meta = [f'scope: global', f'portability: {score}',
        f'synthesis-required: {"true" if synthesis_required else "false"}']
if synthesis_required and blocked:
    meta += ['blocked-refs:'] + [f'  - {b}' for b in blocked]
out = re.sub(r'\n---\n', '\n' + '\n'.join(meta) + '\n---\n', out, count=1)

parent = os.path.dirname(dst_path)
if parent:
    os.makedirs(parent, exist_ok=True)
with open(dst_path, 'w') as f:
    f.write(out)

action = 'synthesized' if synthesis_required else 'direct'
print(f'SCORE:{score}|ACTION:{action}|REFS:{len(blocked)}')
```

Run:
```bash
python3 /tmp/process_skill.py <SKILL_PATH> exported-skills/<skill-name>/SKILL.md
```

### Step 3: Report

Parse the output line (`SCORE:N|ACTION:X|REFS:N`) and print to chat:

```
skill-templatizer: <skill-name>
  Score:    <N>/100
  Action:   direct export | synthesized
  Output:   exported-skills/<skill-name>/SKILL.md
  Replaced: <N> references   (only if synthesized)
```

## Safety Rules

1. **NEVER modify the source SKILL.md** in `.claude/plugins/` — write only to `exported-skills/`.
2. **NEVER skip** the process script even if the skill appears clean — always run Step 2.
3. **NEVER ask the user for confirmation** — this skill runs automatically and silently.
4. If `exported-skills/<skill-name>/SKILL.md` already exists, overwrite it without warning.
5. **NEVER write helper scripts anywhere other than `/tmp/`**.

## Examples

**Invoked automatically after `/build-skill` creates `autonomous-system-bootstrap`:**

Script finds `dev/changes/[your-change-slug]` (×3, −45), `[your-railway]` (−10) → score 45.
Synthesizes replacements, injects metadata, writes `exported-skills/autonomous-system-bootstrap/SKILL.md`.
Reports: "⚙ autonomous-system-bootstrap synthesized (score: 45/100, 4 refs replaced)".

**Invoked automatically after `/build-skill` creates `git-commit`:**

Script finds no project-specific refs → score 100. Copies with metadata injected.
Reports: "✓ git-commit exported directly (score: 100/100)".
