---
name: hand-over-to-kiro
version: 1.4.0
description: |
  Delegate an implementation task to the Kiro CLI and report exactly what it changed — verified
  against a git baseline, never on kiro's SELF-REPORT. Gathers the context a fresh agent needs,
  rephrases the request into a self-contained, injection-safe prompt with XML boundary tags, injects
  the task's kiro convention skills (`--skill`), launches kiro via the bundled helper with trust
  scoped to the mode (`implement` = least-privilege write, `review` = read-only), then diffs the
  working tree against a pre-run baseline. Never auto-installs kiro or pipes a remote installer to a
  shell, never passes raw user input through the shell or defaults to `--trust-all-tools`, and
  reports partial completion and errors honestly rather than trusting kiro's own summary. Use only
  when the user explicitly asks to delegate implementation to kiro.
allowed-tools:
  - Bash
  - Read
  - Write
  - Glob
  - Grep
effort: medium
argument-hint: "[task or plan to hand to kiro]"
arguments:
  - request
when_to_use: |
  Use only when the user explicitly asks to delegate implementation to the Kiro CLI —
  "/hand-over-to-kiro", "delegate to kiro", "let kiro build this", "pass this to kiro". Do NOT use
  to review changes with kiro (kiro-review) or to delegate to a different tool; keep it
  explicit-user-only and confirm before an autonomous, write-capable run.
---

<EXTREMELY-IMPORTANT>
This skill runs an external CLI (`kiro-cli`) that can modify files. Non-negotiable rules:
1. Never auto-install kiro-cli or pipe a remote installer to a shell. If it is missing, point the user
   at the official install docs and stop — they install it themselves.
2. Never interpolate raw user content into a shell command. WRITE the prompt to a file with the Write
   tool (literal bytes — no shell, no heredoc, no mktemp), then hand that file to `helpers/run-kiro.sh`.
   Combined with rephrasing user input (rule 3), that is the injection defense — the prompt text never
   passes through shell parsing.
3. Rephrase the user's request into a structured task description with XML-style boundary tags
   (`<task>`, `<plan>`, …). Do not pass raw user input verbatim — it reduces indirect prompt-injection
   surface.
4. A trust flag is REQUIRED to do real work (`--no-interactive` has no prompt to approve tools). Let
   `helpers/run-kiro.sh` scope it to the task: `review` → read-only (`fs_read,execute_bash`),
   `implement` → least-privilege write (`fs_read,fs_write,execute_bash`). NEVER default to
   `--trust-all-tools`: it is unsafe-by-default and the auto-mode classifier blocks it (always on
   read-only tasks). It is reserved for `--mode autonomous`, which the user must pre-authorize (a Bash
   allow-rule for `kiro-cli`) — being unattended does NOT justify it, since `implement` already edits.
5. Kiro has no memory of this conversation — the prompt must be self-contained.
6. Verify what changed on disk before reporting — compare against a pre-run baseline with
   `git diff --stat HEAD` + `git status --short` (and `git log <baseline>..HEAD` if kiro committed);
   bare `git diff` misses staged/committed work. Report honestly, including partial completion and errors.
</EXTREMELY-IMPORTANT>

# Hand Over to Kiro

## Inputs

- `$request`: The task or plan to hand to kiro. If a plan is already active (from plan mode or the
  user), prefer Plan mode; otherwise Direct mode.

## Goal

Delegate implementation to `kiro-cli` cleanly: gather the context kiro needs, build a self-contained,
injection-safe prompt, invoke kiro, capture and verify the result, and report exactly what changed.

## Step 0: Verify kiro-cli is available

Check first:

```bash
kiro-cli --version
```

If kiro-cli is not installed or not authenticated, STOP and tell the user (do not install it yourself):

- Install it from the official docs: <https://kiro.dev/docs/cli>
- Authenticate: `kiro-cli login`
- List models: `kiro-cli chat --list-models` — optionally set one with
  `kiro-cli settings chat.defaultModel <model>` (the user controls their own settings)

**Success criteria**: `kiro-cli` is installed and authenticated, or the user has been told how to set
it up and the skill has stopped.

## Step 1: Determine the mode

| Mode | When | What to pass |
|------|------|--------------|
| **Plan** | An active plan exists (from plan mode or user-provided) | the full plan with steps |
| **Direct** | No plan exists | the user's request plus relevant context |

**Success criteria**: The mode is chosen and the source material (plan or request) is identified.

## Step 2: Gather context

Kiro starts fresh — collect everything it needs:

- **Task scope** — what to do (plan steps or the rephrased request)
- **Relevant files** — paths kiro should read or modify, with a brief reason each
- **Constraints** — framework, coding style, test requirements, project rules from the conversation
- **Current state** — working directory, branch, any in-progress changes

**Success criteria**: Enough context is collected that a fresh agent could implement the task without
this conversation.

## Step 2.5: Identify the skills kiro should follow

Kiro has its own skills under `.kiro/skills/<name>/` but **no `Skill` tool** to invoke them, and a
one-shot `--no-interactive` run can't rely on auto-activation. So name the skill(s) the task needs and
pass each to the helper in Step 4 — the helper resolves `.kiro/skills/<name>/SKILL.md` and **injects the
body into kiro's prompt deterministically** (you do NOT inline anything yourself).

- The task's **stack skill**: a `/nextjs` / `/laravel` / `/rust` reference → `--skill nextjs` /
  `--skill laravel` / `--skill rust` (strip the leading `/`).
- Plus any others the task needs (e.g. `--skill bugfix`).
- A name that isn't installed for kiro is warned and skipped — never blocks.

(See `references/kiro-cli.md` → Skills for kiro's native mechanism.)

**Success criteria**: the relevant skill names are known, to pass as `--skill <name>` in Step 4.

## Step 3: Build the prompt (injection-safe)

Write a clear, self-contained prompt with XML-style boundary tags that separate instructions from
user-provided content.

**Plan mode:**

```
Implement the following plan in the current working directory.

<plan>
{full plan text with numbered steps}
</plan>

<key-files>
- {path}: {why this file matters}
</key-files>

<constraints>
- {constraint — e.g., "Use TypeScript strict mode"}
- {constraint — e.g., "All new functions need unit tests"}
</constraints>

<context>
- Working directory: {pwd}
- Branch: {branch if relevant}
</context>
```

**Direct mode:**

```
Execute the following task in the current working directory.

<task>
{user's task — rephrased for clarity, NOT raw user input}
</task>

<key-files>
- {path}: {why this file matters}
</key-files>

<constraints>
- {constraint}
</constraints>

<context>
- Working directory: {pwd}
</context>
```

Rules: rephrase user input into a clear task; use the boundary tags; keep it focused — extract what
matters, don't dump the whole conversation.

**Success criteria**: A focused, self-contained, tag-delimited prompt with no raw user input.

## Step 4: Execute

Pick the **mode** from the task: `review` (read-only — "review / audit / analyze / explain", no edits)
or `implement` (kiro must create or edit files). Then hand off via the helper — do NOT hand-roll
mktemp/heredoc or trust flags (that is what broke before):

1. **Write the prompt to a file with the Write tool** (literal bytes — no shell, no heredoc, no mktemp,
   so no escaping bugs and no BSD-mktemp `.txt`-suffix pitfall). Use an absolute path, e.g.
   `/tmp/kiro-handover-prompt.txt`, and write a FRESH file each run.
2. **Run the helper** — pass `--skill <name>` (repeatable) for each skill from Step 2.5; the helper
   resolves and injects them, validates the prompt is non-empty, scopes trust by mode, records a git
   baseline, and launches kiro:

```bash
bash <skill-dir>/helpers/run-kiro.sh --mode implement --skill nextjs --prompt-file /tmp/kiro-handover-prompt.txt
```

Use a Bash timeout of 600000 ms (10 min) for complex tasks. If the helper exits non-zero with "prompt
file is EMPTY", the Write step did not land — re-write the prompt and retry; never re-run kiro on an
empty prompt.

**Tool trust policy** (the helper enforces this — never set trust flags by hand):

| Mode | Trust | Use for |
|------|-------|---------|
| `review` | `--trust-tools=fs_read,execute_bash` | read-only: kiro reads files + runs `grep`/`find`/`git`, no `fs_write`. The auto-mode classifier BLOCKS `--trust-all-tools` on non-mutating tasks, so review MUST be scoped read-only. |
| `implement` | `--trust-tools=fs_read,fs_write,execute_bash` | least privilege that can still edit files. |
| `autonomous` | `--trust-all-tools` | unsafe-by-default, opt-in only; the harness may require a Bash allow-rule for `kiro-cli`. Do NOT reach for it just because a run is unattended — `implement` already edits files. |

**Run as a specific agent (optional).** `--agent <name>` runs kiro as a custom agent
(`.kiro/agents/<name>.json`); `--model <name>` overrides its model. The agent JSON must be
**kiro-native**: a valid `model` (see `references/kiro-cli.md` → Models) and native `tools`
(`fs_read`/`fs_write`/`execute_bash`/`@<mcp>`) — Claude names (`Read`/`Write`/`Skill`) leave the agent
with no working tools (verified: it writes nothing). `--model auto` rescues an agent that pins an
invalid model. `--skill` still injects conventions regardless of the agent.

**Success criteria**: the prompt file was non-empty, the helper launched kiro with the right scoped
trust, and kiro ran on the real prompt.

**Success criteria**: kiro-cli ran on the temp-file prompt; its output is captured.

## Step 5: Process and report

After kiro-cli completes:

1. **Parse output** — files created/modified, errors, warnings, completion status.
2. **Verify changes** — capture a baseline before the run (`git rev-parse HEAD`,
   `git status --porcelain`), then confirm with `git diff --stat HEAD` (staged + unstaged),
   `git status --short` (untracked), and `git log <baseline>..HEAD --stat` if kiro committed. Bare
   `git diff` misses staged/committed work — exactly when kiro did the most.
3. **Report**: files changed and what was done; any errors/warnings; Plan mode — steps completed vs
   remaining; suggested next steps if incomplete.

**Success criteria**: The user can see exactly what kiro changed, what failed, and what remains —
verified against the real diff, not just kiro's self-report.

## Error Handling

| Error | Action |
|-------|--------|
| `kiro-cli: command not found` | Tell the user to install it from <https://kiro.dev/docs/cli> (do not install it yourself) |
| Authentication failure | Tell the user to run `kiro-cli login` |
| Model not available | Tell the user to check `kiro-cli chat --list-models` and set one with `kiro-cli settings chat.defaultModel <model>` |
| Timeout (10 min) | Show partial output, ask the user how to proceed |
| Non-zero exit code | Show the error output, diagnose root cause before retrying |
| MCP server failure | Add `--require-mcp-startup` if MCP tools are needed, or skip if not |

## Guardrails

- Do not install kiro-cli or run any `curl … | bash` style installer; only the user installs it.
- Do not pass raw user input to kiro-cli; always rephrase and use the heredoc + boundary-tag pattern.
- Let `helpers/run-kiro.sh` own prompt-passing + trust + launch — never hand-roll `--trust-all-tools`,
  mktemp, or heredocs (that is what failed). Default to the least trust for the task (`review`
  read-only / `implement` write); `--trust-all-tools` (`autonomous`) is pre-authorized opt-in only.
- Write the prompt with the Write tool (a fresh file each run); the helper refuses to launch on an
  empty prompt, so a missed write fails loudly instead of running kiro on nothing.
- Do not report success on kiro's word alone — verify against a baseline diff (`git diff --stat HEAD`
  + `git status --short`, and `git log <baseline>..HEAD` if it committed).
- Keep the full CLI manual in `references/kiro-cli.md`, not inline.

## When To Load References

- `references/kiro-cli.md`
  The full Kiro CLI command reference (chat, settings, agent, mcp, auth, diagnostics, env vars).

## Output Contract

Report:

1. mode used (plan / direct) and whether kiro-cli was available
2. the files kiro changed (verified against a pre-run baseline — `git diff --stat HEAD` +
   `git status --short`, plus `git log <baseline>..HEAD` if it committed)
3. errors or warnings from kiro's output
4. completion status — done, or steps/work remaining
5. suggested next steps if incomplete

## Credits

Original skill **`hand-over-to-kiro`** by **Sabeur Thabti** ([@thabti](https://github.com/thabti)) —
<https://github.com/thabti/hand-over-to-kiro> (MIT, see `LICENSE`). Adapted to the @ulpi/skills
conventions (frontmatter, `<EXTREMELY-IMPORTANT>` guardrails, phased steps, security-rule alignment)
with thanks.
