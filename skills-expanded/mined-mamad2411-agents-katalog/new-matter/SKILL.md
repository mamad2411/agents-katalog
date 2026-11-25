---
name: new-matter
description: Use when starting a legal matter, an open-source investigation, or a document review — provisions a workspace from a variant template, records the facts that define the matter so later work need not re-ask, and initialises version control. Triggers - "start a new case", "set up an investigation workspace", "new document review".
disable-model-invocation: true
allowed-tools: Bash(mkdir *), Bash(cp *), Bash(test *), Bash(find *), Bash(git init *), Bash(git add *), Bash(git commit *), Bash(gh repo create *), Bash(gh auth status), Read, Write
---

# New Matter

Provision a workspace for a matter and record the facts that define it, so no later
operation has to ask again.

## When to use

- Starting a legal matter, an open-source investigation, or a document review.
- Splitting an existing matter that has grown two distinct threads.

This skill is not invoked automatically. It creates directories and may create a remote
repository, so it runs only when asked for by name.

## Inputs

- **Name** — kebab-case, used as the directory and any repository name. Required.
- **Parent path** — where to create it. Defaults to the current working directory.
- `--variant <legal-research|osint-investigation|document-analysis>` — defaults to
  `legal-research`.
- `--jurisdiction <code>` — free text, recorded as a workspace fact.
- `--private` — make any created repository private.
- `--local-only` — skip repository creation entirely.

## Procedure

### 1. Resolve the template

Templates live under `assets/templates/<variant>/` in this skill's directory. Resolve that
directory at runtime. Create any empty directories the variant's README lists, since some
tools drop empty folders when they install a skill. Confirm the variant directory exists before doing anything else, and name the
valid variants if it does not.

### 2. Refuse to clobber

If the target directory already exists and is non-empty, stop. Report what is there and
offer to pick a different name. Never merge a template into occupied space.

### 3. Copy the template

```bash
mkdir -p "$TARGET"
cp -R "$TEMPLATE"/. "$TARGET"/
```

Copy the contents, not the directory itself. The workspace is data — do not copy any
agent configuration directory into it.

### 4. Record the defining facts

Fill in the labelled fact block in the workspace's `AGENTS.md`. Read any ambient
identity, locale, and timezone facts already available rather than asking for them.
Then ask only for what cannot be inferred:

- **legal-research** — `MATTER`, `JURISDICTION`, `PARTIES`, `CONFIDENTIALITY`.
- **osint-investigation** — `SUBJECT`, `SCOPE`, `BOUNDARIES`, `CONFIDENTIALITY`.
- **document-analysis** — `CORPUS`, `JURISDICTION`, `CONFIDENTIALITY`.

For an investigation, treat `BOUNDARIES` as a real constraint rather than a formality.
Write down what is out of scope in terms specific enough to refuse against later.

### 5. Initialise version control

```bash
git init -b main "$TARGET"
git -C "$TARGET" add .
git -C "$TARGET" commit -m "Initial matter workspace"
```

### 6. Publish only if asked

Unless `--local-only` was given, ask whether to create a remote repository. Default to
private, and say plainly what would be published — a matter workspace usually contains
material that should not be public. Never create a public repository without an explicit,
specific yes.

```bash
gh repo create "$NAME" --private --source="$TARGET" --push
```

### 7. Point at the next step

Name the two or three skills that matter for the chosen variant, and say that evidence
handling — hashing, custody, timestamping — comes from the companion evidence agent's
`init-evidence-store` when the matter needs it.

## Output

- A workspace directory with the variant's structure and a filled-in fact block.
- A git repository with one commit.

## Notes

- The workspace never contains agent configuration. Updating this plugin cannot change
  or break an existing workspace.
- Jurisdiction is free text. It shapes how citations are formatted and which limitation
  questions get flagged; it is not a lookup into any legal database.
