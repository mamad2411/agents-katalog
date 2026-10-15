---
name: lite-git
description: Help non-technical users use Git for office files and simple project snapshots. Use when initializing a repository, preparing safe commits, checking what should be ignored or tracked with Git LFS, or switching to an older or newer version without losing work.
argument-hint: Describe the goal, such as "initialize this folder", "save the current version", or "switch to the version from last week".
---

# Lite Git

Use this skill when the user is not comfortable with Git and wants a safe, plain-language workflow for basic version control tasks.

Primary goals:

- Initialize a repository with sensible defaults for office and media files.
- Save a new version safely.
- Switch to another version safely.
- Catch files that should be ignored or stored with Git LFS before they cause problems.

Default operating mode:

- Be proactive for safe read-only checks and low-risk file preparation.
- Do not wait for confirmation to inspect status, review files, or propose a concrete plan.
- If the next step is safe and reversible, prefer doing it instead of only describing it.
- Ask before destructive actions or when user intent is materially ambiguous.

## Interaction Style

- Use plain language first and Git terms second.
- Explain risk before any action that can hide, overwrite, or detach work.
- Prefer the safest reversible path over the shortest path.
- Avoid asking broad open-ended questions. Ask only the minimum needed to proceed safely.
- When possible, summarize choices as 2-4 concrete options.

## Default Safety Rules

Always do these checks before changing Git state:

1. Detect whether the folder is already a Git repository.
2. Check whether there are uncommitted changes.
3. Check whether Git LFS is installed if the folder contains likely binary office or media files.
4. Inspect untracked files for obvious junk, temporary files, caches, and lock files.
5. Inspect tracked and untracked files for likely LFS candidates.

Default question policy:

- Do not ask permission for status checks, file inspection, or drafting .gitignore and .gitattributes changes.
- Do not ask broad questions like "What do you want to do?" when the user intent already maps to initialize, save, or switch.
- Ask only when one of these is true:
  - A destructive action is required.
  - Multiple reasonable interpretations would lead to different commits or checkouts.
  - User content might be ignored or excluded by mistake.

Never do these without explicit user intent:

- Discard local changes.
- Force checkout, reset, clean, or restore.
- Rewrite history.
- Migrate existing history to Git LFS.

## File Classification Heuristics

### Usually ignore

Prefer adding these to .gitignore when present and not intentionally tracked:

- OS clutter: .DS_Store, Thumbs.db
- Editor clutter: .vscode/, .idea/ when the repo is document-focused and the user does not need editor settings versioned
- Office temp and lock files: ~$*.docx, ~$*.xlsx, ~$*.pptx, *.tmp
- Logs and caches: *.log, tmp/, temp/, .cache/

Be conservative. If a file might be user content, ask before ignoring it.

### Usually use Git LFS

Prefer Git LFS for binary or bulky files such as:

- Office files: .doc, .docx, .xls, .xlsx, .ppt, .pptx
- PDFs and design assets: .pdf, .psd, .ai, .sketch, .fig
- Images and media: .png, .jpg, .jpeg, .tif, .tiff, .gif, .mp4, .mov
- Archives and packaged deliverables: .zip, .7z, .rar
- Any large binary file that is painful to diff or merge

### Usually keep in native Git

Prefer native Git for text files such as:

- .md, .txt, .csv, .tsv
- .json, .jsonc, .yaml, .yml, .toml, .xml
- .html, .css, .js, .ts, .py, .sh
- .gitignore, .gitattributes, .editorconfig

If the repository is primarily for office documents, it is acceptable to recommend a broad LFS policy with a text whitelist, but call out the tradeoff that some future text formats may need to be added to the whitelist.

## Built-In Templates

Prefer reusing the templates in this skill instead of inventing new patterns each time.

- Conservative office-focused ignore rules: [templates/office.gitignore](./templates/office.gitignore)
- Simple document-repository LFS policy with text whitelist: [templates/office-default-lfs.gitattributes](./templates/office-default-lfs.gitattributes)
- Mixed repository LFS policy for explicit binary types only: [templates/mixed-binary-lfs.gitattributes](./templates/mixed-binary-lfs.gitattributes)

Template selection rules:

1. If the folder is mostly Word, Excel, PowerPoint, PDF, images, and exports, prefer the default-LFS template.
2. If the folder mixes code, config, notes, and office files, prefer the explicit-binary LFS template.
3. If no likely binary office or media files are present, still initialize Git LFS and use a conservative baseline (explicit-binary template) so LFS is enabled from day one.

## Workflow A: Initialize Repository

Use this when the folder is not yet a Git repository.

1. Inspect the folder contents and explain what you found in plain language.
2. Identify likely ignore candidates and likely LFS candidates.
3. Propose an initialization plan before editing files.
4. Initialize Git with the default branch set to main unless the user specifies otherwise.
5. Create or update .gitignore with conservative defaults suited to the folder contents, preferably starting from [templates/office.gitignore](./templates/office.gitignore).
6. Set up Git LFS by default during initialization and create .gitattributes rules using the most suitable built-in template.
   - If Git LFS is missing, install it first with one minimal confirmation, then run `git lfs install` and continue initialization.
7. Stage only the intended files.
8. Create the initial commit with a simple message such as "Initial snapshot" unless the user asked for something else.
9. Report exactly what was initialized, ignored, and moved to LFS.

Default initialization behavior:

- Enable Git LFS by default for every new repository initialization.
- For a document-heavy folder, default to broad LFS with a text whitelist.
- For a mixed folder, default to explicit binary LFS patterns only.
- If LFS is missing, prefer helping the user install it immediately instead of skipping LFS setup.
- Prefer creating the first commit automatically after showing the exact scope, unless the user asked for review-only help.

Completion checks:

- The folder is now a Git repository.
- .gitignore and .gitattributes, if needed, are present and understandable.
- The first commit exists.
- The user is told the next safe commands in plain language.

## Workflow B: Save A New Version

Use this when the user says things like "提交版本", "保存当前版本", "帮我提交", or "记录一下现在的状态".

1. Check repository status.
2. Summarize changed, new, deleted, and renamed files in plain language.
3. Review whether any changed or new files should be ignored.
4. Review whether any changed or new files should move to Git LFS.
5. If ignore or LFS rules need to change, update those first and explain why.
6. Stage only files that belong in this version.
7. If the scope is ambiguous, ask a narrow question such as "Do you want to include only document changes, or also these temporary/export files?".
8. Create a short, user-friendly commit message. Prefer one of these patterns:
   - Update monthly report
   - Save current draft of slides
   - Add source images for presentation
   - Snapshot before revision round 2
9. Confirm the commit hash and what it contains.

Default commit behavior:

- If the user asks to save or commit the current state, assume they want a real commit, not only a dry run.
- If only one coherent group of user files changed, commit it directly after the safety checks.
- If changes split into clearly different groups, ask a short scoping question before committing.
- If only junk files changed, do not commit; explain what was excluded.

Completion checks:

- The commit includes intended content only.
- Junk files were not accidentally committed.
- Binary office/media files use LFS when appropriate.
- The user gets a short summary of what was saved.

## Workflow C: Switch Version Safely

Use this when the user wants to go back, view an older state, or move to another branch, tag, or commit.

1. Check for uncommitted changes first.
2. If the worktree is dirty, do not switch immediately. Offer safe choices:
   - Commit current work first
   - Create a backup branch first
   - Stash only if the user explicitly agrees
3. Ask what the user means by "switch version":
   - another branch
   - a tag or named release
   - a specific commit
   - the previous version
4. Prefer a normal branch checkout when possible.
5. If switching to a specific historical commit and the user may keep editing, prefer creating a new branch from that commit instead of leaving them in detached HEAD unless they explicitly want a read-only view.
6. After switching, confirm where HEAD is and whether the working tree is clean.
7. Explain, in one or two sentences, how to return to the earlier place.

Default switching behavior:

- For "look at an older version", prefer a read-only checkout only if the user clearly indicates they just want to inspect.
- For "go back and continue editing", prefer creating or moving to a branch.
- For "the previous version", inspect recent history and propose the most likely target instead of asking the user to translate that into Git terminology.

Completion checks:

- No local work was silently lost.
- The user understands whether they are on a branch or a historical snapshot.
- The target version is checked out successfully.

## Decision Rules

### If Git LFS is not installed but needed

- Tell the user plainly that large binary files are better stored with Git LFS.
- During repository initialization, prefer installing Git LFS immediately with one minimal confirmation, then continue the same workflow.
- Detect platform and package manager, then use the nearest standard command:
   - macOS (Homebrew): `brew install git-lfs && git lfs install`
   - Windows (winget): `winget install GitHub.GitLFS && git lfs install`
   - Windows (Chocolatey): `choco install git-lfs -y && git lfs install`
   - Debian/Ubuntu: `sudo apt-get update && sudo apt-get install -y git-lfs && git lfs install`
- If automatic installation is unavailable, provide exact manual commands and pause before LFS-dependent steps.
- Do not pretend LFS is active unless `git lfs install` has completed successfully.

### If the repository is mostly documents

- You may recommend a broad LFS policy with a text whitelist.
- Explain that this is simple to operate but requires maintaining the text whitelist over time.
- Prefer [templates/office-default-lfs.gitattributes](./templates/office-default-lfs.gitattributes) as the starting point.

### If the repository mixes code and documents

- Do not recommend "everything goes to LFS".
- Prefer explicit binary type patterns for LFS and keep text/code in native Git.
- Prefer [templates/mixed-binary-lfs.gitattributes](./templates/mixed-binary-lfs.gitattributes) as the starting point.

### If the user asks for something risky

- Explain the risk in one sentence.
- Offer the nearest safe alternative first.
- Proceed with the risky action only if the user clearly confirms.

## Response Template

When acting on this skill, structure the response like this:

1. Current state
2. Risks or decisions that matter
3. Action taken or plan to take
4. Result in plain language
5. Optional next safe step

Keep the output concise. Non-technical users should be able to understand the result without knowing Git internals.

## Example Prompts

- /lite-git initialize this folder for versioning office files
- /lite-git save the current version and check what should be ignored or moved to lfs
- /lite-git switch to the version from yesterday without losing current work
- /lite-git help me commit these Word and PPT updates safely
- /保存版本 帮我把这批办公文件安全地入库并自动检查 ignore 和 lfs

## What Good Looks Like

- The agent catches junk files before they are committed.
- The agent notices likely LFS candidates before they bloat Git history.
- The agent avoids destructive commands unless the user explicitly asks for them.
- The agent explains status and results in plain language.
- The agent leaves the repository in a predictable, recoverable state.