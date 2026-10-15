---
name: modelgo-call
version: 0.1.5-rc.1
description: "Call ModelGo models with an API key (OpenAI-compatible). Use when the user wants to run a chat/completion, stream a response, list models, create embeddings, do vision/image/audio/multimodal calls, or hit any /v1/* endpoint with their mgk_ API key. Triggers: 调用模型, 跑模型, chat, 对话补全, 流式, embeddings, 向量, 列模型, list models, 多模态, 图片生成, 语音, vision, API key 调用."
metadata:
  requires:
    bins: ["modelgo"]
  cliHelp: |
    modelgo key set [KEY] [--env NAME]
    modelgo key show [--json]
    modelgo chat --model MODEL [--system S] [--stream] [--image SRC] [--max-tokens N] [--temperature T] [PROMPT...]
    modelgo models [--json]
    modelgo embeddings --model MODEL [TEXT...] [--json]
    modelgo call <path> [--method M] [--data JSON | --data-file FILE] [--header "K: V"] [--stream]
---

# modelgo call — invoke models with an API key

Use this skill when the user wants to **call a model** through ModelGo using a
model API key (`mgk_...`). These commands hit the gateway's OpenAI-compatible
`/v1/*` data plane with `Authorization: Bearer <key>` — distinct from the
control-plane commands (balance/permissions/logs) that use the device login.

> **Setup & version check:** install and the skill/CLI version-check protocol
> live in the `modelgo-shared` skill. Align versions there first.

## API key resolution (precedence)

`--api-key FLAG` > `MODELGO_API_KEY` env var > stored per-env key. Get a key from
the ModelGo console (the CLI does not mint keys). Store one to avoid repeating it:

```bash
modelgo key set mgk_xxx                 # stores for the active env
MODELGO_API_KEY=mgk_xxx modelgo key set # keeps it out of shell history
modelgo key show                        # masked; shows which key would be used
```

Prefer the env var when an agent supplies the key, so it never lands in argv.

## Command reference (authoritative)

Per-command flags, usage, and examples are auto-generated from the CLI's own
`--help`:

- [`reference/index.md`](reference/index.md) — index + global conventions + exit codes
- [`reference/chat.md`](reference/chat.md), [`reference/models.md`](reference/models.md), [`reference/embeddings.md`](reference/embeddings.md), [`reference/call.md`](reference/call.md), [`reference/key.md`](reference/key.md)

Don't guess flags — read the reference file or run `modelgo <command> --help`.

## How to use

### Chat

```bash
modelgo chat --model gpt-4o "Write a haiku about Go"
modelgo chat --model gpt-4o --stream "Explain channels"     # token-by-token
modelgo chat --model gpt-4o --system "You are terse." "Hi"
cat prompt.txt | modelgo chat --model claude-opus-4-8       # prompt from stdin
```

Plain text response goes to stdout. Add `--json` for the full response object
(NDJSON `data:` frames when combined with `--stream`).

### Vision / multimodal chat

```bash
modelgo chat --model gpt-4o --image photo.png "What is in this image?"
modelgo chat --model gpt-4o --image https://example.com/x.jpg "Describe it"
```

`--image` is repeatable. Local files are base64-encoded into data URLs; URLs and
`data:` URLs pass through.

### List models

```bash
modelgo models            # one model id per line
modelgo models --json     # full /v1/models payload
```

### Embeddings

```bash
modelgo embeddings --model text-embedding-3-small "hello world"
modelgo embeddings --model text-embedding-3-small "hello" --json   # full vectors
```

### Raw passthrough (`call`) — everything else, incl. multimodal

`modelgo call <path>` forwards any JSON body to any `/v1/*` endpoint and prints
the response verbatim. Use it for images, audio, anthropic `/v1/messages`,
rerank, multimodal embeddings, and any endpoint without a convenience wrapper.

```bash
modelgo call /v1/images/generations --data '{"model":"dall-e-3","prompt":"a cat"}'
modelgo call /v1/audio/speech --data '{"model":"tts-1","input":"hi","voice":"alloy"}' > out.mp3
modelgo call /v1/messages --data-file anthropic_req.json          # Anthropic style
modelgo call /v1/embeddings/multimodal --data-file req.json
echo '{"model":"gpt-4o","messages":[...]}' | modelgo call /v1/chat/completions --stream
```

Body comes from `--data`, `--data-file` (`-` = stdin), or stdin. Method defaults
to POST with a body, GET without. Add `--header "K: V"` for extra headers and
`--stream` to copy a streaming body through unbuffered.

## Notes

- These commands need a **model API key**, not a device login. They never touch
  `auth.json`; key resolution is flag > `MODELGO_API_KEY` > stored key.
- The env (`cn`/`intl`/custom) selects the gateway base URL; switch with
  `modelgo env use <name>` or `--env`.
- On error the CLI prints a plain-text message to stderr and exits non-zero
  (`1` runtime, `2` usage). `HTTP 401` → bad/expired key; `402` → top up
  (`modelgo balance`) or use `modelgo pay` for x402; `429` → rate limited.
- If a command looks like a CLI bug (crash, empty/malformed output), see
  `modelgo-shared/assets/issue-reporting.md` before filing an issue.
