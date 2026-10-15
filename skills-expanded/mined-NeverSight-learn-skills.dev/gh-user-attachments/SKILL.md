---
name: gh-user-attachments
description: "Upload 2–10 supported local files to GitHub user attachments and return finalized canonical URLs in input order. Use for batch attachment uploads to GitHub issues, pull requests, comments, or discussions. Do not use for one file, Markdown generation, or editing GitHub content."
---
# GitHub user attachments

Use private `gh user-attachments` extension. Uploads files only. Caller owns URL placement.

## Run

1. Require installed `gh user-attachments` exposing required commands:

```bash
gh user-attachments upload --help
gh user-attachments auth --help
```

If either command is missing, report the extension dependency blocker and guide the user (or obtain approval) to install it:

```bash
gh extension install ishinova/gh-user-attachments
```

2. Run:

```bash
gh auth status --hostname github.com
gh user-attachments auth status
```

If attachment auth fail, ask user run:

```bash
gh user-attachments auth login
```

3. Inspect every file. No upload secrets, credentials, private customer data, unintended content.
4. Upload 2–10 distinct files to explicit repo:

```bash
gh user-attachments upload \
  --repo OWNER/REPO \
  --file /absolute/path/to/first.png \
  --file /absolute/path/to/second.mp4
```

Use GitHub-supported attachment types. Let CLI enforce file type, size, content, duplicate-path rules.

## Interpret

- Exit `0`: all files finalized. Each stdout line canonical URL, ordered like input files.
- Exit `2`: options or local validation failed. No remote mutation started.
- Exit `3`: auth, repo lookup, or other pre-mutation step failed.
- Exit `4`: one or more URLs finalized, remote state changed, or failure where remote mutation can't be ruled out.

Trust only stdout URLs matching:

```text
https://github.com/user-attachments/assets/UUID
```

On exit `4`, stdout contains only finalized URLs, maybe none. Never treat stderr as result URL. Report completed URLs, warn incomplete remote state may remain or can't be ruled out. Don't retry whole batch blindly.

## Guardrails

- Never expose `GH_USER_ATTACHMENTS_SESSION`. Account session secret, not scoped token.
- Never pass session values in arguments, logs, source, issues, pull requests.
- Don't read personal browser cookie stores. `auth login` uses one-shot tool-owned Chrome profile deleted after sign-in; stored session file is reusable credential.
- Don't fall back to another storage service.
