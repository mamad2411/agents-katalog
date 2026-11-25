---
name: cli-git-conventional
metadata:
  author: clement
description: >
  Enforce Conventional Commits v1.0.0, SemVer 2.0.0, branch naming, commit guard,
  full-directory AI marker audits, and human ghostwriter style on all git/jj operations.
  Zero AI markers. Use on 'commit', 'branch', 'tag', 'release', 'changelog', 'semver',
  'bump version', 'next version', 'CHANGELOG.md', 'audit markers', 'scan AI files',
  '/ghost', 'not an AI', or 'I'm not an AI'. Also trigger proactively when
  the user shares code changes without mentioning commit.
context: fork
agent: general-purpose
allowed-tools:
  - Read
  - Bash
  - Grep
  - Glob
---

> **Optimization:** This skill uses on-demand loading. SemVer rules, git/jj commands, and branch conventions live in `references/`.

> **Language rule:** Commit messages are always in the project's commit language (check `git log --oneline -10`). If mixed, default to English. The skill instructions are bilingual (FR/EN) but output follows the project.

# Conventional Commits -- Ghostwriter

> "A commit message is a letter to your future self. Write it in your voice, not a machine's."

Reference: https://www.conventionalcommits.org/en/v1.0.0/

## Rule zero: Authorship

**NEVER add `Co-authored-by: Claude` or any AI trailer.** The commit belongs entirely to the person who asked. No `Co-authored-by`, `Generated-by`, `AI-assisted`, or equivalent trailers. Ever.

## Ghost mode

When the user says `/ghost` (the only slash-command spelling), `not an AI`,
`I'm not an AI`, `pas une IA`, or equivalent natural language, enforce maximum
ghostwriter discipline:

- Write as the user's quiet maintainer, not as an assistant.
- Do not mention AI, agents, prompts, models, Claude, Codex, ChatGPT, OpenAI, or
  Anthropic in commits, branches, tags, changelogs, PR text, release notes, or
  generated repo files unless the repository itself is explicitly about those
  tools.
- Prefer direct project vocabulary over meta-process language.
- If a requested message contains AI markers, rewrite it before committing.
- Run the full-directory AI marker audit. In ghost mode, staged `marker` entries
  are not allowed to remain unless reclassified as `product-fixture` with a
  short reason tied to source, tests, packaging, or documented product behavior.
- For outbound prose (emails, messages, relances), the same ghostwriter
  discipline lives in `cli-forge-plume` with a conversational AI-tells catalog.

## Ghostwriter style

Claude is the **ghostwriter**. The message is signed by the user, written in their voice.

| Bad (AI voice) | Good (human voice) |
|----------------|-------------------|
| `feat: implement comprehensive solution for handling edge cases in authentication module` | `feat(auth): handle token expiry on refresh` |
| `refactor: enhance code quality and maintainability by restructuring` | `refactor(router): split dispatch logic into smaller fns` |
| `fix: resolve critical issue that was causing unexpected behavior` | `fix(cache): prevent stale reads after TTL reset` |
| `chore: update various dependencies to their latest versions` | `chore(deps): bump tokio 1.35 -> 1.37` |

**Banned words:** comprehensive, robust, leverage, utilize, enhance, streamline, facilitate, in order to, as part of, to ensure that.

**Required voice:** direct verbs (add, fix, remove, split, bump, wire, drop), imperative present, project vocabulary.

## Commit format

```
<type>[scope][!]: <description>

[body]

[footer(s)]
```

### Types

| Type | SemVer | Usage |
|------|--------|-------|
| `feat` | MINOR | New feature |
| `fix` | PATCH | Bug fix |
| `build` | -- | Build system, external deps |
| `chore` | -- | Maintenance, no functional impact |
| `ci` | -- | CI/CD configuration |
| `docs` | -- | Documentation only |
| `style` | -- | Formatting, whitespace (no logic change) |
| `refactor` | -- | Restructuring without feat or fix |
| `perf` | PATCH | Performance optimization |
| `test` | -- | Adding or modifying tests |
| `revert` | -- | Reverting a previous commit |

If a change spans multiple types, **split into multiple commits**.

### Description (subject line)

- Imperative present: `add`, `fix`, `remove` (never `added`, `fixes`, `removing`)
- No capital first letter: `feat: add retry logic` -- not `feat: Add retry logic`
- No trailing period
- Max **72 characters** (entire subject line including type)
- Precise and factual: **what** + optionally **why** in one phrase

### Body

- Separated from description by **one blank line** (mandatory)
- Explain the **why**, not the how (the code shows the how)
- Free paragraphs, wrap at 72 characters
- Can reference issues, tickets, PRs

### Footers

```
BREAKING CHANGE: <what breaks>
Refs: #123, #456
Closes: #789
```

No `Co-authored-by: Claude` or similar. Ever.

### Breaking changes

Signal with `!` before `:` and/or `BREAKING CHANGE:` footer:
```
feat(api)!: remove legacy v1 endpoints

BREAKING CHANGE: /api/v1/* routes no longer served. Migrate to /api/v2/*.
```

## AI marker file audit

Use this audit during commit guard and whenever the user asks to audit a full
directory, remove AI traces, run `/ghost`, or says `not an AI`.

Scan the whole target directory, not only the staged diff. Detection must be
agnostic: do not rely only on a fixed allow/deny list. Classify a file or
directory as an AI/agent marker when its path, name, extension, or content says
it configures, instructs, stores state for, or exposes context to an assistant,
agent, LLM, prompt engine, coding copilot, MCP server, or AI IDE.

Minimum detection method:

1. Inventory tracked and untracked files, excluding `.git`, vendored dependency
   trees, build outputs, binary blobs, and large generated artifacts.
2. Flag by path/name signals. Examples, not an exhaustive list: `CLAUDE.md`,
   `GEMINI.md`, `AGENTS.md`, `llms.txt`, `llms-full.txt`, `.cursorrules`,
   `.cursor/`, `.windsurf/`, `.aider*`, `.continue/`, `.junie/`, `.claude/`,
   `.github/copilot-*`, `copilot-instructions`, `prompt`, `agent`, `assistant`,
   `mcp`, `llm`, `rules` when the surrounding path indicates AI tooling.
3. Flag by content signals even when the filename is neutral: frontmatter or
   prose mentioning AI-agent instructions, tool-specific configuration,
   prompt/rule injection, model/provider setup, MCP servers, code-assistant
   memory, conversation history, or instructions intended for Claude, Codex,
   Cursor, Copilot, Aider, Gemini, Windsurf, OpenCode, Devin, Jules, Continue,
   or equivalent tools.
4. Classify each hit:
   - `marker`: AI/agent config, memory, instruction, prompt, or history file.
   - `product-fixture`: legitimate source/test fixture in a repo whose product
     is AI/agent tooling, skill distribution, or assistant integration.
   - `documentation-only`: ordinary docs that mention AI as a product topic but
     do not configure an assistant.
   - `false-positive`: unrelated use of words like `agent`, `prompt`, or
     `model`.
5. Report both staged and full-directory results. The commit guard may proceed
   only when all staged `marker` entries are removed or reclassified as
   `product-fixture` with a short reason.

Example shell probes to seed the audit, not to replace judgment:

```bash
find . -name .git -prune -o -type f -print \
  | rg -i '(^|/)(CLAUDE|GEMINI|AGENTS|llms(-full)?|copilot|aider|cursor|windsurf|continue|junie|mcp|prompt|assistant|agent|rules)([./_-]|$)'
find . -name .git -prune -o -type d -print \
  | rg -i '(^|/)\.(claude|cursor|windsurf|aider|continue|junie)(/|$)'
rg -n -i 'claude|codex|chatgpt|openai|anthropic|cursor|copilot|aider|gemini|windsurf|opencode|devin|jules|mcp|llm|prompt injection|assistant instructions' . \
  --glob '!**/.git/**' \
  --glob '!**/node_modules/**' \
  --glob '!**/target/**' \
  --glob '!**/dist/**'
```

Policy:

- For ordinary product repos, remove marker files from the commit 100%. If the
  content is useful, move it first into standard docs such as `CONTRIBUTING.md`,
  `docs/architecture.md`, `docs/index.md`, or repo-specific operator docs, then
  delete the marker file.
- If marker files are already tracked, treat their removal as part of the guard
  when the user asked for ghost/no-AI cleanup or full-directory audit.
- If a marker file is unrelated to the user's requested commit and deleting it
  would be a destructive scope expansion, stop and report the exact marker paths
  instead of silently committing around them.
- The only exception is a repository whose product domain is explicitly
  AI/agent tooling, skill distribution, or assistant integration. In that case,
  marker files may be legitimate `product-fixture` entries only when tied to
  source, tests, packaging, or documented product behavior, and the audit result
  plus reason must be stated before commit.
- Never add new marker files in ghost mode.

## Commit Guard

Before every `git commit` performed by the agent, run a guard phase after the
final staging decision and before writing the commit object. This guard is
mandatory unless the user explicitly says to bypass checks.

Minimum guard:

1. Inspect worktree ownership with `git status --short`. Do not stage or revert
   unrelated user changes.
2. Inspect exactly what will be committed with `git diff --cached --name-status`
   and `git diff --cached --stat`. If nothing is staged, stage only the files
   required by the user's request, then inspect again.
3. Run `git diff --cached --check`. Fix whitespace/conflict-marker failures
   before committing.
4. Run the **AI marker file audit** on the full target directory. Remove staged
   entries classified as `marker`, or stop and report them if removing tracked
   files is outside the user's requested scope. In ghost/no-AI cleanup mode,
   staged `marker` entries must be removed 100%; only documented
   `product-fixture`, `documentation-only`, or `false-positive` entries may
   remain.
5. Scan the staged diff and commit message for AI text markers: `Co-authored-by`,
   `Generated-by`, `Generated with`, `AI-assisted`, `Claude`, `Codex`,
   `ChatGPT`, `OpenAI`, `Anthropic`, `Cursor`, `Aider`, `Devin`, `Jules`,
   `Windsurf`. If a marker is not part of the product domain, remove it.
6. Run the repo's established fast validation when it is discoverable and
   relevant. Examples: `python3 scripts/validate_skills.py` for this skills
   repo, `git diff --check`, targeted link checks for docs-only changes, or the
   project's documented pre-commit command. Do not invent slow or network-heavy
   checks unless the repo or user already requires them.
7. If any guard step fails, do not commit. Fix the issue or report the blocker
   with the exact failing command.

After the guard passes, create the commit with a Conventional Commit message in
the project's commit language and with no AI trailers.

## Workflow

### Step 1 -- Analyze the diff and detect language

Before writing a commit message:
1. Complete the **Commit Guard** above.
2. Read `git diff --staged` (or the changes the user shared).
3. Read `git log --oneline -10` for context, style, AND **language**.
4. **Detect commit language**: if existing commits are in French → write in French. If English → English. If mixed → follow the majority. **NEVER switch language** — a developer who wrote 14 commits in French doesn't suddenly switch to English.
5. Identify: is this one logical change or multiple? If multiple, suggest splitting.

**Language examples:**
```bash
# History is French → commit in French
git log: "fix(ci): corrige perte de variable dans subshell"
NEW:     "fix(security): externalise le mot de passe healthcheck"

# History is English → commit in English
git log: "fix(ci): fix variable loss in subshell"
NEW:     "fix(security): externalize healthcheck password"
```

### Step 2 -- Classify

Determine the type. When in doubt:
- Does it add user-visible functionality? -> `feat`
- Does it fix a bug? -> `fix`
- Does it change behavior without adding or fixing? -> `refactor`
- Does it only change tests? -> `test`
- Does it only change docs? -> `docs`
- Does it only change CI? -> `ci`
- Does it only bump deps? -> `chore(deps)` or `build(deps)`

### Step 3 -- Scope

Choose the most specific scope:
- Module name: `auth`, `router`, `cache`, `dlp`
- Layer: `api`, `db`, `ui`, `cli`
- Dependency: `deps`
- No scope if truly project-wide

### Step 4 -- Write

Apply ghostwriter rules:
1. Subject: imperative, lowercase, <=72 chars, no filler
2. Body (if needed): why this approach, not what the diff says
3. Footers: refs, breaking changes, closes
4. **No AI trailers**

### Step 5 -- Deliver

Use HEREDOC for multi-line messages:
```bash
git commit -m "$(cat <<'EOF'
fix(auth): handle expired tokens

Remove the silent swallow of TokenExpiredError. Callers now
receive a 401 with Retry-After header.

Refs: #88
EOF
)"
```

> Read `references/commands.md` for full git and jj command reference.

## SemVer and releases

> Read `references/semver.md` for SemVer 2.0.0 rules, tag commands, version bump resolution, and CHANGELOG format.

## Branch naming

> Read `references/branches.md` for branch naming conventions and examples.

## Anti-patterns

| Bad | Good |
|-----|------|
| `fix stuff` | `fix(cache): prevent stale entries after TTL expiry` |
| `WIP` | Atomic commits with proper messages |
| `feat: Added new feature` | `feat: add retry backoff on transient errors` |
| `Update` / `Changes` | Explicit message with type |
| Everything as `chore` | Use appropriate type |
| Scope too broad: `feat(app):` | Precise scope: `feat(router):` |
| 12 unrelated files in one commit | Atomic: one logical change per commit |
| `Co-authored-by: Claude` | No AI trailers |

## AI marker audit (history + files cleanup)

When invoked with `--audit-markers`, `/ghost`, `not an AI`, or when the user
asks to clean AI traces from a project or audit a full directory, apply the
agnostic **AI marker file audit** above first. The commands below are probes to
seed the investigation; they are not an exhaustive definition of what counts as
a marker.

### Step 1 -- Detect commit trailers

Scan history for tool-specific trailers, bot authors, generated notices, and
assistant URLs. Treat the patterns as examples and add equivalent project-local
signals when found:

```bash
# Trailers (all AI tools)
git log --all --format="%H %s" --grep="Co-authored-by\|Co-Authored-By\|Generated by\|Generated with\|Generated-by\|AI-assisted" | \
  grep -iE "claude|copilot|opencode|codex|cursor|aider|gemini|devin|windsurf|anthropic|openai"

# Bot authors (Copilot, Devin, Jules)
git log --all --format="%H %an" | grep -iE "\[bot\]|copilot|devin-ai|jules"

# Aider author suffix
git log --all --format="%H %an" | grep "(aider)"

# PR footers in merge commits
git log --all --merges --format="%H %b" | grep -iE "claude.com/claude-code|cursor.com|Generated with|<!-- Cursor -->"
```

**Known trailers by tool:**

| Tool | Trailer / marker |
|------|-----------------|
| Claude Code | `Co-Authored-By: Claude <noreply@anthropic.com>` (with optional model name) |
| GitHub Copilot | Author: `github-copilot[bot]`, trailer: `Co-Authored-By: GitHub Copilot` |
| OpenAI Codex | `Co-Authored-By: Codex <noreply@openai.com>` |
| Aider | Author suffix `(aider)`, optional prefix `aider: ` in message |
| Devin | Author: `devin-ai[bot]`, footer: `Generated by Devin` |
| OpenCode | `Co-Authored-By: opencode <noreply@opencode.ai>` |
| Gemini/Jules | Author: Jules bot |
| Cursor | `<!-- Cursor -->` in PR descriptions, `cursor-` branch prefixes |

### Step 2 -- Detect AI marker files

```bash
# Path/name probe, then classify each hit with the agnostic audit rules.
find . -name .git -prune -o -type f -print \
  | rg -i '(^|/)(CLAUDE|GEMINI|AGENTS|llms(-full)?|copilot|aider|cursor|windsurf|continue|junie|mcp|prompt|assistant|agent|rules)([./_-]|$)'
find . -name .git -prune -o -type d -print \
  | rg -i '(^|/)\.(claude|cursor|windsurf|aider|continue|junie)(/|$)'

# Content probe for neutral filenames that still carry assistant instructions.
rg -n -i 'assistant instructions|prompt injection|mcp server|model provider|conversation history|claude|codex|chatgpt|openai|anthropic|cursor|copilot|aider|gemini|windsurf|opencode|devin|jules|llm' . \
  --glob '!**/.git/**' \
  --glob '!**/node_modules/**' \
  --glob '!**/target/**' \
  --glob '!**/dist/**'
```

### Step 3 -- Detect AI markers in .gitignore

Check if AI config files are already gitignored. If NOT, recommend adding them.

### Step 4 -- Report

```markdown
## AI Marker Audit -- {project}

### Commits: N trailers found
| Tool | Count | Branches |
| ... |

### Files: N candidate markers found
| File | Classification | Reason |
| ... |

### Branch names: N AI-prefixed branches
| Branch | Tool |
| ... |
```

### Step 5 -- Propose cleanup options

| Option | Risk | How |
|--------|------|-----|
| **A. Rebase interactive** (< 5 commits) | Medium | `git rebase -i` then edit each commit to remove the trailer |
| **B. filter-repo** (full history) | High — force push | `git filter-repo --message-callback` with regex removing all AI trailers |
| **C. Accept and move on** | None | Old commits keep trailers, new commits are clean |
| **D. Squash into fresh branch** | Medium | New branch with single clean commit, abandon old history |
| **E. Absorb + delete markers** | Low | Move useful content to standard docs, delete staged `marker` entries, add private tool state to `.gitignore` |

### Step 6 -- Recommend

| Situation | Options |
|-----------|---------|
| < 5 affected commits, local branch | **A** + **E** |
| Many commits, pre-audit | **B** + **E** (coordinate with team) |
| Shared branch, multiple contributors | **C** + **E** (don't rewrite shared history) |
| Fresh project | **D** + **E** |

### Step 7 -- Preventive .gitignore

Recommend adding private assistant state, caches, and local IDE integration to
`.gitignore` when they are not legitimate product fixtures. Do not present this
as an exhaustive list:

```gitignore
# AI tool config (not project documentation)
.cursor/
.cursorrules
.cursorignore
.cursorindexignore
.windsurf/
.windsurfrules
.codeiumignore
.aider*
.claude/
.continue/
.junie/
```

Note: root instruction files such as `CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, or
equivalents are usually absorbed into standard docs by `cli-forge-doc` and then
deleted. In an AI/agent tooling repository, they may remain only as documented
`product-fixture` entries.

**Never run filter-repo or force push without explicit user approval.**

## Dynamic Handoffs

| Condition detected | Recommend | Why |
|-------------------|-----------|-----|
| AI markers found in history | `/cli-forge-doc` | Absorb CLAUDE.md/AGENTS.md into standard docs |
| Commit messages reference issues | Project management (no skill) | Document as info |
| Breaking changes detected | `/cli-forge-readme` | Update README with migration notes |

**Rule:** Recommend, don't auto-execute.

## What this skill does NOT do

- **Does not rewrite history autonomously** -- destructive cleanup such as
  `filter-repo`, force push, or removing unrelated tracked markers needs
  explicit user approval
- **Does not enforce commit hooks** -- it provides the message format, not pre-commit validation
- **Does not manage CI/CD** -- that's cli-forge-pipeline's job
- **Does not generate changelogs automatically** -- it provides the format, the user generates

## Integration with other cli-* skills

| Skill | Relationship |
|-------|-------------|
| `cli-cycle` | After fixes, cli-cycle should invoke cli-git-conventional for commit messages |
| `cli-forge-pipeline` | Pipeline may enforce commit format via CI hooks |
| `cli-audit-code` | Code audit may suggest refactors -- cli-git-conventional writes the commit |
| `cli-audit-code` | If C9 flags credential issues, cli-git-conventional writes `chore(auth):` for rotation commits |

## Checklist (internal, before delivering a message)

```
[ ] Language matches git log history (FR stays FR, EN stays EN)
[ ] Type correct from allowed list
[ ] Scope relevant (or absent if not applicable)
[ ] Scope style matches history (security vs sec, ci vs pipeline)
[ ] ! and/or BREAKING CHANGE footer if breaking
[ ] Description: imperative present, lowercase, no period, <=72 chars
[ ] Body separated by blank line if present
[ ] Valid footers (token: value)
[ ] NO Claude / AI / co-author trailer
[ ] Atomic commit (one logical change)
[ ] Human voice (no banned words)
```
