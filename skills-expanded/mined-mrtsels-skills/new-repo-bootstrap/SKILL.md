---
name: new-repo-bootstrap
description: 'Use when turning a directory into a GitHub repo: docs, git init, publish. Covers both greenfield
  and existing code.'
license: MIT
metadata:
  hermes:
    tags:
    - repo
    - bootstrap
    - github
    - greenfield
    - AGENTS
    - README
  source_frontmatter:
    version: 1.1.0
    author: Hermes Agent
  imported_from: hermes
---

# New Repo Bootstrap

Start a repo from an empty directory and publish it to GitHub in one pass. Verified flow for the user's public repos (mrtsels): greenfield docs → git init → explicit-path commits → `gh repo create --push`.

## When to Use

- Empty/near-empty directory that will become a repo (only design docs, no manifests yet)
- Existing directory with code that needs to become a standalone published repo (e.g. a subfolder of a monorepo being extracted)
- User says "git -> my public repo", "publish this", "make a README", "push成单独仓库"
- New repo that wraps/embeds an upstream open-source project

## ⚠️ CRITICAL: Don't Copy the Directory

When the user says "把这个文件夹 push 成仓库", **the folder IS the repo**. Run `git init` directly inside it. **NEVER** copy to /tmp or elsewhere — this creates a detached duplicate, loses the original path context, and the user gets a repo pointing at a temp dir they didn't ask for. Always work IN the directory the user specified. If the directory already has a `.git`, it's already a repo — just `git remote add origin` and push.

## 1. Greenfield AGENTS.md — verify, don't guess

When the repo has NO manifests (no package.json / pyproject.toml / Makefile), there are no local commands to observe — do not invent them:

1. Survey first: `ls -la` (may reveal TASK.md, references/, design docs), `git status` (may not be a repo yet).
2. If the repo wraps an upstream project, fetch the upstream manifests from raw.githubusercontent to learn the REAL commands:
   ```sh
   for f in package.json pnpm-workspace.yaml README.md docs/architecture.md apps/web/package.json; do
     echo "===== $f ====="; curl -sL --max-time 20 "https://raw.githubusercontent.com/<owner>/<repo>/master/$f" | head -80
   done
   ```
3. Label command provenance in AGENTS.md: upstream-verified commands vs `本仓库尚无命令,脚手架完成后补齐` (TBD). Never present a planned command as a working one.
4. Check the user's LOCAL toolchain too (`node -v`, `pnpm -v`, `dsh --version`) — installed versions often differ from upstream master (e.g. rc.5 on master vs rc.6 installed); note the mismatch as a pitfall.
5. If the project carries a design doc (suggestions.md / TASK.md), treat it as SSOT and cite its section numbers (§12/§17/§18) for layout, routes, phases.

## 2. README for a greenfield repo

- State current status honestly (设计阶段,尚无代码) and link the design doc + AGENTS.md.
- "怎么用" = what actually works TODAY (e.g. `npx @deepseek-ai/dsh web`), plus a placeholder for future install steps. No invented commands.
- User convention: public repo docs in Chinese; identifiers/commands in English.
- LICENSE: ask the user which license they want — do NOT assume MIT.

## 3. Git init + publish (one-shot)

```sh
git init -b main
git add <specific paths>    # 禁 `git add .` / -A (user rule); include a TASK.md found untracked — it's part of the repo
git commit -m "<type>: <summary>"
gh repo create <owner>/<name> --public \
  --description "<one-sentence Chinese about>" \
  --source . --remote origin --push
```

Verify after push: `gh repo view <owner>/<name>` (description set) + `git log --oneline` + `git status` clean.

## 4. Submodule Extraction (subfolder → standalone repo + submodule)

When a subfolder of a monorepo needs to become its own GitHub repo **while remaining embedded in the parent**:

```sh
# Step 1: Initialize the subfolder as its own repo
cd /path/to/monorepo/subfolder
git init
git add <specific files>
git commit -m "feat: initial release"
git remote add origin https://github.com/owner/new-repo.git
git push -u origin main

# Step 2: Add it back as a submodule in the parent
cd /path/to/monorepo
git submodule add https://github.com/owner/new-repo.git subfolder
git commit -m "chore: add subfolder as git submodule"
git push
```

Pitfalls:
- If `git submodule add` says "Adding existing repo", it detected the `.git` dir — this is correct behavior, not an error.
- If the subfolder has uncommitted changes, commit + push them inside the submodule **before** adding the submodule reference to the parent.
- `gh repo create` needs `delete_repo` scope to delete repos — if you created one by mistake, you may need `gh auth refresh -h github.com -s delete_repo` to clean it up.

## 5. License Choice

Don't assume MIT. Ask the user which license they want before creating the LICENSE file. Common choices:

| License | Character |
|---------|-----------|
| MIT | Maximum freedom, allows闭源 commercial use |
| Apache 2.0 | Permissive + patent grant |
| LGPL-2.1 | Library copyleft: derivative works must open-source changes to this file, but can close-source the rest |
| GPL-3.0 | Strong copyleft: entire derivative work must be open-source |
| MPL-2.0 | File-level copyleft: only modified files must be open-source |

For DSH ecosystem plugins, LGPL-2.1 and MPL-2.0 are common choices — they keep the plugin itself open while allowing proprietary extensions.

## Pitfalls

- **Don't copy the directory** — when the user says "把这个文件夹 push 成仓库", the folder IS the repo. Run `git init` directly inside it. Copying to /tmp or elsewhere is wrong — it creates a detached duplicate, loses the original path context, and the user gets a repo pointing at a temp dir they didn't ask for. Always work IN the directory the user specified.
- **`gh repo create` TLS handshake timeout** — usually NOT a gh problem. Diagnose: `curl --proxy http://127.0.0.1:1082 https://api.github.com/users/<owner>` → 000, direct → 000, but baidu → 200 = **proxy node dead** (the proxy port can still be LISTENing — MacPacket/Shadowrocket at 1082). The user must switch node in the proxy client; then rerun the SAME one-shot command. Full chain: `macos-git-proxy-troubleshoot`.
- **`gh auth status` can succeed minutes before the node dies** — a passing auth check is not a green light; verify connectivity at the moment of the API call.
- **Piping gh through `tail` masks the exit code** (pipe returns tail's 0) — a retry loop with `2>&1 | tail -3 && break` can look successful while failing. Read the actual error text.
- **Dev-preview dependencies**: when the new repo depends on a dev-preview tool, pin the version and record it in the repo's own docs (AGENTS.md/TASK.md), not in memory — versions go stale.
