# AGENTS.md

How a coding agent works on AgentLog. Humans start at [README.md](./README.md).

**Package 0.3.0** · spec **0.2.0** · last product freeze 2026-03-30 ·
upgraded 2026-08-17 against Watchtower 5.x.

## What this repo is

The **interchange format**. Watchtower captures. AgentLog validates and
converts. Do not add a second capture engine here.

| Lives here | Does not live here |
|---|---|
| Spec, JSON Schema, Zod, types | Floor, board, Fly indexer |
| Converters *to* AgentLog JSON | Disk discovery of ~/.codex, ~/.cursor |
| `AGENT_SOURCES` | Ora `ActorContext` (that stays in ora-ai `packages/agentlog` 0.1.0) |

The ora-ai workspace copy is still **0.1.0** plus ActorContext. Do not
overwrite it from this tree. Do not copy ActorContext into this Apache
repo.

## Do this first

1. `npm install && npm test && npm run typecheck && npm run build`
2. A new converter must emit a document `validateAgentLog` accepts.
3. New Watchtower sources go in `src/sources.ts` and the watchtower
   name/provider maps. Do not invent a parallel enum.
4. Capture on disk stays in `@braintied/watchtower` /
   `github.com/braintied/watchtower`. This package consumes
   `SessionPayload`.

## Convert paths

```ts
import { exportFromPayload } from '@braintied/agentlog/convert/payload';
import { exportWatchtowerSession } from '@braintied/agentlog/convert/watchtower';
import { convertGrokHistory } from '@braintied/agentlog/convert/grok';
```

`exportWatchtowerSession(..., { messages })` uses live
`session_messages`. Without that it falls back to
`metadata.raw_content` (`[user] ` / `[assistant] `), which is the
March 2026 reconstruction and loses tool rows.

Session keys are `source:<uuid>` (`grok:…`, `claude:…`). The converter
splits on the first colon.

## Do not

- Bump `specVersion` for a converter-only change. Spec 0.2.0 stays
  until the schema grows.
- Publish `@braintied/agentlog` from ora-ai. This repo is the public
  package.
- Point strangers at `ora-watchtower.fly.dev`.
- Add Aider/Codex disk parsers that duplicate Watchtower adapters
  unless Watchtower itself grew a new on-disk format this package
  must read without Watchtower installed.
