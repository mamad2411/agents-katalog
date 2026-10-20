---
name: filesystem-first-agents
description: >-
  Scaffold, migrate, and run filesystem-first durable agents (Vercel eve and
  Agent Skills-shaped layouts) as a git-backed directory tree. Triggers when
  the user wants eve scaffolding, agent-as-directory setups, non-Vercel/direct
  provider routing, colonizing a repo with agent/tools/skills/channels, or
  comparing OpenClaw/Hermes workspace layouts to eve.
---

# Filesystem-first agents (eve + portable skills)

Build agents whose **source of truth is the directory tree in git** — markdown for identity/procedures, TypeScript for tools/runtime — not a central registry or cloud console.

Primary framework: **[eve](https://eve.dev)** (`eve` npm package). Portable skill format: **[Agent Skills](https://agentskills.io)** (`SKILL.md` packages).

## When to use

- User wants eve (or “like eve”) without lock-in
- Repo should fully represent the agent in git
- Scaffold / replace an existing clue-style agent tree
- Direct Anthropic/OpenAI providers instead of Vercel AI Gateway
- OpenAI-compatible gateways (LiteLLM / custom baseURL) e.g. `glm-5.2-fp8`
- Eve eval suites (`eve eval`, mockModel unit vs live LLM tags)
- Self-host vs `eve deploy`

## Decision criteria (Cooper preferences)

1. **Filesystem layout first** — the agent must be a readable directory contract in git.
2. **Vendor lock-in optional** — prefer direct AI SDK providers + local sandbox over Gateway/Sandbox/Workflows until explicitly wanted.
3. Eve OSS is fine when layout match matters; OpenClaw/Hermes workspaces are the nearest non-Vercel harness peers.

## Eve project layout

```text
my-agent/
├── package.json
├── tsconfig.json
├── .env.example
├── AGENTS.md                 # coding-agent pointers to eve docs
└── agent/                    # THE agent
    ├── agent.ts              # defineAgent({ model, … })
    ├── instructions.md       # always-on system prompt
    ├── tools/*.ts            # defineTool; filename = snake_case tool name
    ├── skills/<name>/SKILL.md  # or skills/<name>.md — progressive disclosure
    ├── channels/eve.ts       # HTTP; optional Slack/Discord/…
    ├── sandbox/sandbox.ts  # optional; defaultBackend() for local
    ├── connections/          # MCP / OpenAPI
    ├── subagents/<id>/
    ├── schedules/
    ├── hooks/
    ├── workspace/            # seeded into sandbox
    └── lib/
```

## Scaffold paths

### A. Official init (empty dir)

```bash
npx eve@latest init my-agent
# or into existing package.json project with no agent/ yet:
npx eve@latest init .
```

Notes:
- Does **not** create a Vercel project.
- Interactive tail often launches `eve dev`; stop with Ctrl+C after scaffold if you only wanted files.
- Target directory must be empty except `.git` / `.DS_Store` / `.gitkeep` / `.hg`.

### B. Manual scaffold (preferred when repo already has history)

Write the layout by hand (template below), then:

```bash
npm install
npx eve build
npx eve info
```

Migrate prior clue-style roots (`AGENTS.md`, `SOUL.md`, `RULES.md`, `agent.yaml`, old `skills/`) into:
- `agent/instructions.md` (identity + rules)
- `agent/skills/**/SKILL.md`
- archive originals under `_legacy-*/` in the same commit

## Models: avoid Vercel when unwanted

```ts
// agent/agent.ts — DIRECT provider (no AI Gateway)
import { anthropic } from "@ai-sdk/anthropic";
import { defineAgent } from "eve";

export default defineAgent({
  model: anthropic("claude-sonnet-4-5"),
});
```

### OpenAI-compatible gateway (LiteLLM / custom baseURL)

Cooper’s default for `czxtm/agents` is LiteLLM, **not** Anthropic direct:

```ts
import { createOpenAI } from "@ai-sdk/openai";
import { defineAgent } from "eve";

const litellm = createOpenAI({
  name: "litellm",
  apiKey: <REDACTED>
  baseURL: process.env.LITELLM_BASE_URL ?? "https://litellm.drkmttr.dev/v1",
});

export default defineAgent({
  // Chat Completions — what LiteLLM exposes at /v1/chat/completions
  model: litellm.chat(process.env.LITELLM_MODEL ?? "glm-5.2-fp8"),
  // REQUIRED for non-gateway / unknown catalog models or build fails:
  // "Cannot compile agent compaction because … does not have known AI Gateway context window metadata."
  modelContextWindowTokens: <REDACTED>
    process.env.LITELLM_CONTEXT_WINDOW_TOKENS ?? 1_000_000,
  ),
});
```

| Mode | Config | Env |
| --- | --- | --- |
| LiteLLM / OAI-compat | `createOpenAI({ baseURL, apiKey }).chat("glm-5.2-fp8")` + `modelContextWindowTokens` | `LITELLM_API_KEY` (or `OPENAI_API_KEY`); optional `LITELLM_BASE_URL`, `LITELLM_MODEL` |
| Direct Anthropic | `anthropic("claude-sonnet-4-5")` from `@ai-sdk/anthropic` | `ANTHROPIC_API_KEY` |
| Direct OpenAI | `openai("…")` / `createOpenAI().chat` | `OPENAI_API_KEY` |
| AI Gateway | string `"anthropic/claude-sonnet-5"` | `AI_GATEWAY_API_KEY` or Vercel OIDC |

Install provider packages as normal deps. Match `@ai-sdk/*` major line to the `ai` version eve pins (eve 0.27 → `ai` ^7). Prefer **`.chat(modelId)`** for LiteLLM (Completions API); default `openai(id)` / responses may not match the gateway.

Verify routing after build/start: `GET /eve/v1/info` → `agent.model.routing.kind` should be `"external"` for direct/custom providers. Manifest should show the model id (e.g. `glm-5.2-fp8`) and provider name (e.g. `litellm`).

Native Anthropic ids use hyphens (`claude-sonnet-4-5`); gateway ids use `provider/model` with dots in versions.

Key location on Cooper’s box for LiteLLM: `~/.secrets/litellm-api-key` (also some tooling reads `~/.config/litellm/key`). Write into project `.env` as `LITELLM_API_KEY=…` (gitignored). Eve loads `.env` / `.<REDACTED>` / `.env.development*` in dev/eval automatically.

## HTTP channel + auth

Default HTTP routes exist even without authoring `channels/eve.ts`. When authoring, **`auth` is required**:

```ts
import { eveChannel } from "eve/channels/eve";
import { localDev, placeholderAuth, vercelOidc } from "eve/channels/auth";

export default eveChannel({
  auth: [vercelOidc(), localDev(), placeholderAuth()],
});
```

- `eveChannel()` with no args throws / fails eval (`uploadPolicy` on undefined).
- `localDev()` unlocks localhost for `eve dev`.
- Replace `placeholderAuth()` before production exposure.

Routes: `/eve/v1/health`, `/eve/v1/info`, `/eve/v1/session`, stream, cancel. Self-host must also proxy `/.well-known/workflow/`.

## Sandbox (local-first)

```ts
import { defaultBackend, defineSandbox } from "eve/sandbox";

export default defineSandbox({
  backend: defaultBackend(), // Docker → microsandbox → just-bash; not Vercel
});
```

Do not use `vercel()` sandbox backend unless creating hosted Vercel sandboxes on purpose.

## Skills format

- Plain: `agent/skills/forecast.md` with description frontmatter (or filename slug).
- Packaged: `agent/skills/<name>/SKILL.md` + optional `references/`, `scripts/`, `assets/`.
- Agent Skills Standard ports in as-is; eve exposes `load_skill`.
- Skills are per-agent scoped (root vs subagent); put shared executables in `lib/`.

## Local run / self-host

```bash
# Node >= 24 required by eve
export PATH="/opt/homebrew/opt/node@25/bin:/opt/homebrew/bin:$PATH"  # example on Cooper's Mac

cp .env.example .env   # provider key
npm install
npm run dev            # TUI + HMR
npm run build && npm start
curl -sf localhost:3000/eve/v1/health
```

- Persist `.eve/.workflow-data` across restarts.
- Optional durable worlds: `experimental.workflow.world` in `agent.ts` (e.g. postgres world package matching eve’s `@workflow/*` line).

## Dependency pins (eve 0.27 era)

```json
{
  "dependencies": {
    "@ai-sdk/anthropic": "^4.0.21",
    "ai": "^7.0.34",
    "eve": "^0.27.6",
    "zod": "4.4.3",
    "@vercel/connect": "0.4.2"
  },
  "engines": { "node": ">=24" }
}
```

Prefer `engines.node: ">=24"` over `"24.x"` when hosts may run Node 25/26.

## Evals / “unit tests” (`eve eval`)

Eve does **not** use Jest-style unit tests for agent behavior. First-class harness:

```bash
eve eval                       # all evals under evals/
eve eval --tag unit            # offline fixtures
eve eval --tag live            # real model
eve eval --list
eve eval --strict --junit .eve/junit.xml   # CI
```

Layout:

```text
evals/
  evals.config.ts              # required root; defineEvalConfig({}) is enough
  unit-smoke.eval.ts           # tags: ['unit']
  smoke-live.eval.ts           # tags: ['live']
```

- Identity = file path (`evals/weather/foo.eval.ts` → id `weather/foo`).
- Evals drive **real HTTP sessions** against a booted local (or `--url` remote) agent.
- Artifacts: `.eve/evals/<timestamp>/summary.json` + per-eval streams.
- Exit: `0` pass, `1` fail, `2` config.

### Offline unit path (`mockModel`)

Swap the agent model when `EVE_MOCK_MODEL=1`:

```ts
import { mockModel } from "eve/evals";
// model: process.env.EVE_MOCK_MODEL === "1" ? mockModel(responder) : liveModel()
```

`mockModel` callback gets `{ lastUserMessage, toolResults, tools, … }` and may return text or `{ toolCalls: [{ name, input }] }` for tool loops.

Recommended npm scripts:

```json
{
  "test": "eve eval",
  "test:unit": "EVE_MOCK_MODEL=1 eve eval --tag unit",
  "test:live": "eve eval --tag live",
  "test:list": "eve eval --list"
}
```

Guard mixed suites: live evals `t.skip` when `EVE_MOCK_MODEL===1`; unit evals `t.skip` when mock is off. Put fixture routing keywords carefully (e.g. don’t put `"ping"` in a smoke prompt if that triggers the mock’s tool branch).

Assertions that matter: `t.succeeded()`, `t.calledTool` / `t.notCalledTool` / `t.usedNoTools()`, `t.check(t.reply, includes(/…/))`.

Note: post-success local runs may log workflow queue `503 socket hang up` during teardown — noise if gates already passed.

## Verification checklist

1. `npx eve info` — Compile ready, 0 errors; skills/tools counts look right
2. `npx eve build` — exits 0, `.output` present
3. `npx eve start` then `curl …/eve/v1/health` → `ok: true`
4. `/eve/v1/info` model routing matches intended provider
5. `npm run test:unit` (offline) and optionally `npm run test:live` (creds)
6. Agent tree + lockfile committed; secrets only in `.env` (gitignored)

## Pitfalls

- **Non-empty in-place init** — `eve init .` refuses dirs with real files; stash/move first or scaffold manually.
- **Empty `eveChannel()`** — always pass `{ auth: […] }`.
- **Gateway vs direct model strings** — string ids hit Gateway and need gateway creds.
- **Custom / LiteLLM models need `modelContextWindowTokens`** — otherwise compaction compile fails with “no known AI Gateway context window metadata”.
- **Use `.chat()` for LiteLLM** — Completions path; don’t assume Responses API.
- **Reasoning models (GLM 5.2, etc.)** — may fill `reasoning_content` and leave `content` empty at tiny `max_tokens`; give room and assert with loose includes (`/pong/i`), not brittle exact equality.
- **vite-plus / vp npm shim** — on Cooper’s machine `~/.vite-plus/bin/npm` can reject `packageManager` fields; use Homebrew Node’s npm (`/opt/homebrew/opt/node@25/bin` ahead of vite-plus) for install/build.
- **Don’t commit** `.eve/`, `.output/`, `node_modules/`, `.env`.
- **Preview software** — eve APIs can change; re-read `node_modules/eve/docs/` when versions bump.

## OpenClaw / Hermes peer (when eve is wrong fit)

If the goal is a personal multi-channel assistant workspace rather than a deployable agent app framework:

```text
workspace/
  AGENTS.md SOUL.md IDENTITY.md USER.md TOOLS.md
  skills/**/SKILL.md
```

Still filesystem-first and git-friendly; runtime differs. Hermes skills already follow Agent Skills packaging.

## Support files

- `references/eve-direct-provider-scaffold.md` — scaffold notes, LiteLLM/`glm-5.2-fp8`, eval results for `czxtm/agents`
- `templates/` — copy-paste starters for agent.ts / channel / sandbox / skill / tool

## Related

- Official docs: https://eve.dev/docs (also `node_modules/eve/docs/`)
- Self-host: `guides/deployment/self-hosting.md` in package docs
