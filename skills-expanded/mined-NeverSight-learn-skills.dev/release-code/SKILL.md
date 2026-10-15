---
name: release-code
description: Prepare and publish a research code repository for public release alongside a paper (arXiv, conference, GitHub). Use when the user wants to open-source code, create a GitHub release, package a code submission, make code public, or prepare a reproducibility release.
allowed-tools: Read, Write, Edit, Bash, Glob
---

# Release Code

Prepare a research code repository for public release: audit for security issues, generate missing assets (README, citation, license), tag the version, and create a GitHub release.

## Skill Directory Layout

```
<installed-skill-dir>/
├── SKILL.md
├── checklist.md                      # Detailed item-by-item checklist reference
└── templates/
    ├── README_ml_paper.md            # README template for ML paper repos
    └── CITATION.cff                  # Citation file template
```

---

## Steps to Follow

### 1. Understand the release context

Ask the user **in a single message**:

1. **Paper info**: Title, authors, venue/year (e.g. "CVPR 2025"), arXiv ID or URL (if available)
2. **Release type**: Full code release / minimal reproducibility package / anonymous conference submission?
3. **License**: MIT / Apache-2.0 / CC-BY-4.0 / other? (default: MIT for code, CC-BY-4.0 for models/data)
4. **What's included**: Training code? Evaluation? Pre-trained weights? Datasets? Demo?
5. **Version tag**: e.g. `v1.0.0` (default: `v1.0.0` for first release)
6. **GitHub release?**: Create a GitHub release with release notes? (yes/no)
7. **Model weights**: Are pre-trained weights available? If so, where will they be hosted? (HuggingFace Hub / Google Drive / project page)

### 2. Audit the repository

Run the following checks (read output silently, report summary to user):

#### 2a. Security scan — secrets and credentials
```bash
# Check for common secret patterns
git -C "$(git rev-parse --show-toplevel)" log --all --oneline | head -5
grep -rI --include="*.py" --include="*.yaml" --include="*.json" --include="*.env" \
  -E "(password|secret|api_key|token|credential|private_key)\s*=\s*['\"][^'\"]{6}" \
  "$(git rev-parse --show-toplevel)" 2>/dev/null | head -20
```

#### 2b. Large files check
```bash
# Find large files that shouldn't be in the repo
find "$(git rev-parse --show-toplevel)" -type f -size +50M \
  ! -path "*/.git/*" ! -path "*/outputs/*" ! -path "*/wandb/*" 2>/dev/null
```

#### 2c. Sensitive file patterns
```bash
# Check for files that should not be public
find "$(git rev-parse --show-toplevel)" -type f \( \
  -name ".env" -o -name "*.pem" -o -name "*.key" -o \
  -name "secrets.yaml" -o -name "credentials.json" \
  \) ! -path "*/.git/*" 2>/dev/null
```

#### 2d. Check what already exists
```bash
ROOT="$(git rev-parse --show-toplevel)"
for f in README.md LICENSE CITATION.cff .gitignore requirements.txt pyproject.toml setup.py; do
  [ -f "$ROOT/$f" ] && echo "EXISTS: $f" || echo "MISSING: $f"
done
```

#### 2e. Git status
```bash
git -C "$(git rev-parse --show-toplevel)" status --short
git -C "$(git rev-parse --show-toplevel)" log --oneline -5
```

Report audit findings to the user as a checklist:
- 🔴 **BLOCKER** — must fix before release (secrets found, credentials, large binaries)
- 🟡 **WARNING** — recommended to address (missing README, no license, no .gitignore)
- 🟢 **OK** — already in good shape

Ask the user to fix any blockers before continuing.

### 3. Generate missing files

Based on the 2d audit, generate any missing files. **Ask the user's preference before overwriting existing files.**

#### LICENSE

If missing, generate the appropriate license file:
- **MIT** (most common for ML code):
  ```
  MIT License
  Copyright (c) {YEAR} {AUTHORS}
  [standard MIT text]
  ```
- **Apache-2.0**: Use standard Apache 2.0 text
- **CC-BY-4.0**: For data/models if user specified

Write to `{PROJECT_ROOT}/LICENSE`.

#### CITATION.cff

Read the template from `<installed-skill-dir>/templates/CITATION.cff`.

Fill in placeholders:
| Placeholder | Value |
|---|---|
| `{TITLE}` | paper title |
| `{AUTHORS_LIST}` | authors as YAML list (see template format) |
| `{YEAR}` | publication year |
| `{VENUE}` | conference/journal name |
| `{ARXIV_ID}` | arXiv ID (if available) |
| `{GITHUB_REPO}` | `github.com/username/repo` |
| `{DATE_RELEASED}` | today's date (YYYY-MM-DD) |

Write to `{PROJECT_ROOT}/CITATION.cff`.

#### README.md

If README is missing or skeletal (< 50 lines):

Read the template from `<installed-skill-dir>/templates/README_ml_paper.md`.

Fill in all placeholders. Leave `[TODO: ...]` markers where the user must provide content (e.g., exact performance numbers, dataset download links).

**Do NOT overwrite a substantial existing README** — instead, identify what sections are missing and offer to append them.

#### .gitignore

If missing, generate a Python/ML `.gitignore`:
```
# Python
__pycache__/
*.py[cod]
*.egg-info/
.eggs/
dist/
build/
.venv/
venv/

# ML outputs (keep jobs/ but ignore outputs/)
outputs/
wandb/
*.ckpt
*.pt
*.pth
*.pkl
runs/
lightning_logs/

# Data (large files)
data/
datasets/

# Secrets
.env
*.pem
*.key
secrets.yaml
credentials.json

# IDE
.vscode/settings.json
.idea/
*.DS_Store
```

### 4. Pre-release checklist review

Read `<installed-skill-dir>/checklist.md` for the full item list.

Present the user with a condensed checklist grouped by category. For each item, report status (✅ done / ⚠️ needs attention / ❌ missing):

```
📁 Repository hygiene
  ✅ .gitignore covers outputs/, wandb/, *.ckpt
  ⚠️  outputs/ directory exists — confirm not committed

📄 Documentation
  ✅ README.md present (142 lines)
  ❌ No CITATION.cff — will generate
  ⚠️  README missing "Pre-trained Models" section

🔐 Security
  ✅ No secrets detected
  ✅ No large files in git history

📦 Reproducibility
  ✅ requirements.txt / pyproject.toml present
  ⚠️  No environment.yml for conda users
  ⚠️  No Dockerfile

⚖️  Legal
  ✅ LICENSE (MIT) present
```

Ask: **"Are you ready to proceed with tagging and publishing, or do you want to fix any of the above first?"**

### 5. Commit and tag

Once the user confirms:

```bash
ROOT="$(git rev-parse --show-toplevel)"
# Stage only new/modified tracked files (not untracked outputs)
git -C "$ROOT" add LICENSE CITATION.cff README.md .gitignore 2>/dev/null || true
git -C "$ROOT" diff --staged --stat
```

Ask the user to confirm the staged changes, then commit:
```bash
git -C "$ROOT" commit -m "chore: prepare code for public release ({VERSION})"
```

Create annotated tag:
```bash
git -C "$ROOT" tag -a "{VERSION}" -m "$(cat <<'EOF'
Release {VERSION} — {PAPER_TITLE}

Published at {VENUE}
Paper: {PAPER_URL}

Includes: {WHAT_INCLUDED}
EOF
)"
```

Ask: **"Push commit and tag to origin?"**

```bash
CURRENT_BRANCH="$(git -C "$ROOT" branch --show-current)"
git -C "$ROOT" push origin "$CURRENT_BRANCH"
git -C "$ROOT" push origin "{VERSION}"
```

### 6. GitHub Release (optional)

If the user requested a GitHub release:

Check if `gh` is available:
```bash
gh --version 2>/dev/null && echo "gh available" || echo "gh not found"
```

If available, draft the release notes and create the release:
```bash
gh release create "{VERSION}" \
  --title "{PAPER_TITLE} ({VERSION})" \
  --notes "$(cat <<'EOF'
## {PAPER_TITLE}

**{VENUE}** | [Paper]({PAPER_URL}) | [Project Page]({PROJECT_PAGE_URL})

### What's included
{INCLUDED_ITEMS}

### Installation
\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Citation
\`\`\`bibtex
{BIBTEX}
\`\`\`
EOF
)"
```

If `gh` is not available, print the release notes as text for the user to paste into GitHub.

### 7. Summary and next steps

Print a final summary:
```
✅ Release {VERSION} complete!

Files generated/updated:
  • LICENSE
  • CITATION.cff
  • README.md
  • .gitignore

Git:
  • Commit: {COMMIT_HASH}
  • Tag: {VERSION} → pushed to origin

GitHub:
  • Release: https://github.com/{REPO}/releases/tag/{VERSION}

Recommended next steps:
  □ Upload pre-trained weights to HuggingFace Hub / project page
  □ Add repo link to the paper's arXiv abstract page
  □ Tweet / post about the release
  □ Email the mailing list / post to r/MachineLearning
  □ Add a "Code" badge to the paper PDF (camera-ready only)
```

---

## Handling Anonymous Submissions

When the user says this is for an **anonymous conference submission**:

1. **Do NOT** create a public GitHub release.
2. **Do NOT** include author names in any committed files.
3. Generate an **anonymous zip package** instead:
   ```bash
   ROOT="$(git rev-parse --show-toplevel)"
   PROJ=$(basename "$ROOT")
   git -C "$ROOT" archive --format=zip HEAD -o "/tmp/${PROJ}-anonymous.zip"
   echo "Anonymous zip: /tmp/${PROJ}-anonymous.zip"
   ```
4. Check the zip contents for any author-identifying information before submission.
5. Remind the user to anonymize: commit messages visible via git log, personal paths in configs, email addresses in code comments.

---

## Common Patterns

### HuggingFace Hub model upload

When the user wants to push weights to HuggingFace:
```bash
# Requires: pip install huggingface_hub
python -c "
from huggingface_hub import HfApi
api = HfApi()
api.upload_folder(
    folder_path='checkpoints/',
    repo_id='username/model-name',
    repo_type='model',
)
"
```

### Adding a "Code" badge to README

```markdown
[![GitHub](https://img.shields.io/github/stars/username/repo?style=social)](https://github.com/username/repo)
[![arXiv](https://img.shields.io/badge/arXiv-2401.00000-b31b1b.svg)](https://arxiv.org/abs/2401.00000)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
```

### Paper with Code link

After release, submit to [paperswithcode.com](https://paperswithcode.com/add-paper) to link the repository to the paper automatically.
