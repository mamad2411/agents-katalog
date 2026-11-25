---
name: collab-dev
description: Multi-agent collaborative development. Gemini designs UI/UX (design spec + presentation code), Claude Code fills business logic (TODO functions only), Codex reviews code quality. Use when user says "协作开发", "collab dev", "multi-agent build", or requests multi-agent collaboration for building web apps. Best for visually intensive projects (dashboards, data viz, animated UIs). For simple CRUD apps, solo development may suffice.
---

# Collaborative Development

## Roles

| Agent | Does | Does NOT |
|-------|------|----------|
| Gemini | design.md + all visible code (CSS/HTML) | write business logic |
| OpenClaw | spec.md + server skeleton + TODO markers + validation + fixes | write UI styles or fill TODOs |
| Claude Code | fill `// TODO` function bodies only | change CSS/HTML structure |
| Codex | write review report | modify any code |

## First Run: Prerequisites Check

On first trigger, check if `~/.openclaw/skills/collab-dev/.ready` exists. If yes, skip to Phase 0. If not, run:

```bash
READY=1

# 1. Gemini CLI
GEMINI=$(which gemini 2>/dev/null)
if [ -n "$GEMINI" ]; then
  echo "✅ Gemini CLI: $($GEMINI --version 2>&1 | head -1)"
else
  echo "❌ Gemini CLI 未安装"; READY=0
fi

# 2. Claude Code CLI
CLAUDE=$(which claude 2>/dev/null)
if [ -n "$CLAUDE" ]; then
  echo "✅ Claude Code: $($CLAUDE --version 2>&1 | head -1)"
else
  echo "❌ Claude Code 未安装"; READY=0
fi

# 3. Codex CLI
CODEX=$(which codex 2>/dev/null)
if [ -n "$CODEX" ]; then
  echo "✅ Codex CLI: $($CODEX --version 2>&1 | head -1)"
else
  echo "❌ Codex CLI 未安装"; READY=0
fi

# 4. ACP config (optional but recommended)
ACPX_CFG="$HOME/.acpx/config.json"
if [ -f "$ACPX_CFG" ]; then
  echo "✅ ACP 配置: $ACPX_CFG"
else
  echo "⚠️ ACP 配置未找到（可选，OpenClaw 内置 ACP 也可用）"
fi
```

If any ❌, show install guide and stop:

| Tool | Install | Auth |
|------|---------|------|
| Gemini CLI | `npm i -g @google/gemini-cli` | `gemini` (首次运行自动引导登录) |
| Claude Code | `npm i -g @anthropic-ai/claude-code` | `claude` (首次运行自动引导登录) |
| Codex CLI | `npm i -g @openai/codex` | `codex` (首次运行自动引导登录) |

Tell user: "装好后再说一次「协作开发」即可。"

**安装遇到问题？** → 读 [references/troubleshooting.md](references/troubleshooting.md)（涵盖 OAuth、ACP 权限、双 auth 不同步、session 堆积等 6 个常见坑）

If all ✅, write marker and proceed:
```bash
touch ~/.openclaw/skills/collab-dev/.ready
```

## Workflow

### Phase -1: PRD (OpenClaw, if needed)

If user only provides a brief idea (e.g. "做一个番茄钟"), clarify requirements before generating PRD.

**Step 1: Requirement Clarification (ask until clear)**

Ask user these questions one round at a time (don't dump all at once). Stop asking when answers are sufficient:

1. **Target users**: Who will use this? (e.g. individuals, teams, specific audience)
2. **Core problem**: What problem does it solve? What's the user's current pain?
3. **Key features**: What are the 3-5 most important things it must do?
4. **Data ownership**: Is data shared (all users see same) or private (each user owns)?
5. **Real-time needs**: Does anything need live updates across tabs/users?
6. **Auth**: Does it need login/registration?
7. **Platform**: Desktop-first, mobile-first, or both equally?
8. **Tech stack**: What language/framework? (default: Node.js + Express, but any stack works)

Skip questions the user already answered. If user says "你决定" or "随便", make reasonable defaults and state them.

**Step 2: Generate PRD**

Read [references/prd-guide.md](references/prd-guide.md) for template. Generate PRD with user stories, feature list (P0/P1/P2), data model, interaction patterns, acceptance criteria.

**Step 3: User confirms PRD → convert to spec.md**

Skip Phase -1 entirely if user already provides a detailed spec or PRD.

### Phase 0: Spec (OpenClaw)

Write `spec.md` with:
- Data model (shared vs private)
- Features with priority (P0/P1/P2)
- Tech stack (from Phase -1, or user's preference)
- Interaction: `.hidden` class toggle for modals
- SSE scope + exclude current connection
- Security: enum field whitelists
- Search strategy: server OR client (not both)
- Field naming: API = DB column names
- API design + acceptance criteria

**Do not write UI style hints** — leave design freedom to Gemini.

### Phase 1a: Design Spec (Gemini)

`gemini -p` outputs `design.md`. Prompt must include:
```
1. :root {} CSS variables (colors, sizes, shadows, transitions)
2. HTML class naming for every component
3. Interaction states: .hidden class for all JS show/hide
4. Mobile: keep all P0 features accessible (off-canvas/drawer, no display:none)
```

### Phase 1b: Presentation Code (Gemini)

`gemini -p` outputs `public/index.html`. Prompt rules:
```
1. Names must exactly match design.md
2. No business logic
3. Use .hidden class for JS show/hide, never inline display:none
4. Mobile: drawer/off-canvas for sidebars
```

Clean output: `sed -i '' '1{/^```/d}; ${/^```/d}' public/index.html`

Quality gate: verify design.md names appear in code.

### Phase 2: Infrastructure + Skeleton (OpenClaw)

Write server/backend with:
- DB path: absolute, relative to project root (not CWD-dependent)
- Auth secrets: read from env var, with secure random fallback (never hardcode)
- Password hashing: async only (never block main thread/event loop)
- SQL: prepared statements / parameterized queries (never string concat)
- Input validation: enum fields use whitelist, strings trimmed + length-limited
- Real-time (if needed): unique connection ID, online count = deduplicated user count, broadcast excludes sender's connection
- Heartbeat for long connections (30s interval + cleanup)

Integrate Gemini's UI code:
- Add element IDs for JS binding (don't change styles)
- Remove sample/placeholder data
- Verify `.hidden` class mechanism works
- Place empty-state elements outside repeating containers
- Use event delegation (no inline event handlers)

Save Gemini's original UI: `cp <ui-file> <ui-file>.gemini-original`

Inject skeleton with TODO markers:
```
// TODO: functionName — description
// Input: params
// 1. step one
// 2. step two
// Output: return value
```

### Phase 3: Logic + Pre-review (parallel)

**3a. Claude Code fills TODOs** (ACP, 5min timeout):
```
Only modify // TODO function bodies.
Do not change CSS/HTML/DO NOT MODIFY blocks.
```
Fallback: if no file change in 3min → kill, OpenClaw fills.

**3b. Codex pre-reviews skeleton** (ACP, simultaneous).

### Phase 4: Automated Validation (OpenClaw)

Phase 4 checks (adapt commands to project's tech stack):

**4a. Completeness**
- Syntax check passes (language-appropriate tool)
- Zero TODO markers remaining

**4b. Design consistency**
- CSS class/variable names in code match design.md definitions

**4c. CSS/JS integration**
- Every class toggled by JS has corresponding CSS rules
- No inline `display:none` outside `.hidden` class and media queries

**4d. Security**
- Auth secrets come from env vars (no hardcoded strings)
- Password hashing is async
- No raw SQL string concatenation

**4e. DOM/UI structure**
- No inline event handlers (onclick= etc.)
- Empty-state elements outside repeating containers

**4f. Spec coverage**
- All P0 acceptance criteria have corresponding implementation

### Phase 5: Self-review + Fix

- `diff index.html index.html.gemini-original` — Claude didn't touch presentation
- Fix pre-review issues
- Verify mobile, brand elements, port/config

### Phase 6: Codex Final Review (ACP)

Dimensions: functionality, design consistency, security, code quality, performance, bug risk (1-10 each).

### Phase 7-8: Fix + Ship

Fix Critical/High from review → re-validate → deliver.

## Known Issues

| Issue | Workaround |
|-------|-----------|
| Gemini ACP unavailable | Always use `gemini -p` CLI |
| Gemini markdown wrapping | Phase 1b: sed cleanup |
| Claude ACP hangs | 5min timeout + fallback |
| Claude modifies presentation | Phase 5 diff check |
| Standard tool projects: Gemini adds little value | Best for visually intensive projects |
