---
name: apfel-cli-tools
description: Reference for the "apfel" family of macOS terminal tools (apfel, auge, translate, apfel-run, apfel-mcp) that expose Apple's on-device AI — the on-device LLM, Vision framework, and Translation framework — as UNIX CLIs and OpenAI/DeepL/LibreTranslate-compatible HTTP servers. Use this skill whenever the user is working on a Mac (Apple Silicon, macOS 26 Tahoe) and wants to run AI, OCR/vision, or translation locally without cloud APIs or API keys — including writing shell one-liners or scripts around `apfel`, `auge`, or `translate`, wiring up MCP servers with `--mcp` or `apfel-run`, debugging an `apfel-run` TOML config, or asking "how do I run AI/OCR/translation on my Mac without the internet / without an API key / for free." Also trigger if the user mentions Apple Intelligence, FoundationModels, the Vision framework, or the Translation framework from a terminal/scripting context, or references Arthur-Ficial's tools by name even loosely (e.g. "that apple offline AI cli", "the on-device translate tool").
---

# apfel CLI tools

`apfel`, `auge`, `translate`, `apfel-mcp`, and `apfel-run` are five small, independent Swift/Python CLIs by Arthur-Ficial (franzai.com) that each wrap one Apple on-device framework and expose it to the shell. They share one philosophy: zero config, zero API keys, zero network calls for inference, MIT-licensed, Homebrew-installable. Reach for this skill whenever you're generating shell commands, scripts, or MCP wiring that should run *entirely on the user's Mac* instead of calling a cloud LLM/OCR/translation API.

**Hard requirements for all five tools:** macOS 26 (Tahoe) or newer, Apple Silicon, Apple Intelligence enabled in System Settings. None of them work on Intel Macs or pre-Tahoe macOS — say so up front if the user's setup is unclear, rather than writing commands that will fail silently.

Demo video (what a real session looks like end to end): "No API Key. No Cloud. Just Mac AI (Apfel)" — https://www.youtube.com/watch?v=wiQo9gayiqU

## Which tool does what

| Tool | Apple framework | Does | Install |
|---|---|---|---|
| `apfel` | FoundationModels (~3B LLM) | Text generation: CLI, OpenAI-compatible server, interactive chat | `brew install apfel` |
| `auge` | Vision | OCR, classification, barcodes, faces, poses, masks, embeddings, more | `brew install Arthur-Ficial/tap/auge` |
| `translate` | Translation | Translate/detect language: CLI filter + DeepL/LibreTranslate/Google v2-compatible server | `brew install Arthur-Ficial/tap/translate` |
| `apfel-mcp` | — (calls the open web) | 3 MCP servers giving `apfel` web search + URL fetch, tuned for its 4096-token window | `brew install Arthur-Ficial/tap/apfel-mcp` |
| `apfel-run` | — (wraps `apfel`) | TOML-based config/profile manager and drop-in replacement for the `apfel` binary | `brew install Arthur-Ficial/tap/apfel-run` |

All are MIT-licensed and open source under github.com/Arthur-Ficial/.

---

## apfel — on-device LLM

A ~3B-parameter model Apple already ships with macOS Tahoe. `apfel` is the front door: no downloads, no API key, 4,096-token context window (input+output combined).

**Three modes, one binary:**

```bash
# UNIX filter — stdin/stdout, pipe-friendly
apfel "What is the capital of Austria?"
echo "some text" | apfel "summarize in 3 bullets"
apfel -f README.md "summarize in 3 bullets"        # read a file
apfel -o json "translate to German: Apple" | jq .content
apfel --code "flush the dns cache on macos"        # command only, no prose

# OpenAI-compatible HTTP server
apfel --serve                                       # http://127.0.0.1:11434
# any OpenAI SDK works — just point base_url at localhost, api_key is unused

# Interactive chat, multi-turn, with context trimming
apfel --chat -s "You are a coding assistant"
```

**MCP tool use:** attach any MCP server (local script or remote URL) and the model gets tools automatically — no extra flags, auto-discovered via `tools/list`.

```bash
apfel --mcp ./calc.py "What is 15 times 27?"
apfel --mcp ./calc.py --mcp ./weather.py "sqrt(2025)?"   # stack multiple
apfel --mcp https://mcp.example.com/v1 "query"            # remote, HTTPS
apfel --serve --mcp ./calc.py                              # tools available server-wide
```

**When to reach for `apfel` in a script:** anything where the user wants a quick, free, private text transform chained with other shell tools — grammar fixes on clipboard text, summarizing `git log`, explaining a cryptic command, narrating system stats, watch-and-announce patterns with `say`. See `references/one-liners.md` for 30 tested examples (clipboard round-trips, git summaries, watch-a-process-then-speak patterns, regex/date/math one-offs) — read that file before improvising a one-liner from scratch, since most common patterns are already there verbatim.

**What it's good at vs. not:** shell scripting, text transforms, classification, short summaries, JSON restructuring, translation. Weak at: math, factual recall, long conversations, complex code generation — it prefers to refuse over hallucinating. Don't use it for anything needing more than ~3,000 words of combined context.

**Full flag reference:** https://github.com/Arthur-Ficial/apfel/blob/main/docs/EXAMPLES.md and https://github.com/Arthur-Ficial/apfel/blob/main/docs/tool-calling-guide.md

---

## auge — Apple Vision from the terminal

Point it at an image (or PDF, or stdin, or clipboard) and get structured OCR/classification/barcode/face/pose output. Zero third-party dependencies — pure Vision framework wrapper, hard-network-blocked at runtime.

```bash
auge --ocr image.png                       # text recognition (handwriting, screenshots, scans)
auge --ocr --langs en-US,de-DE doc.png     # constrain/hint OCR languages (BCP-47)
auge --classify photo.jpg                  # 1000+ category labels with confidence
auge --barcode qr.png                      # QR/EAN/UPC/Code128/PDF417/DataMatrix, decoded payload
auge --faces group.jpg                     # bounding boxes per face
auge --all photo.jpg                       # everything in one pass
auge --all -o json scan.pdf                # PDF input, structured JSON out
auge --all --clipboard                     # read image straight from NSPasteboard
auge --all --md doc.png | apfel "summarize"  # chain into apfel
```

v1.5+ adds subject/person masks (`--subject`, `--persons-mask`), custom Core ML models (`--model my.mlmodel`), and video/sequence analysis (`--motion`, `--track`, `--video clip.mp4 --every 1s`). Output formats: plain, `json`, `--compact`, `ndjson`, `md`. Full capability list and every barcode symbology / OCR language: https://auge.franzai.com/#capabilities.

**When to reach for `auge`:** any "extract text from this screenshot/PDF," "what's in this image," "read this QR code," or "how many faces are in this photo" task where the user is on their own Mac and doesn't want to upload the image anywhere.

---

## translate — Apple Translation from the terminal

UNIX filter *and* an HTTP server that speaks three real translation APIs (DeepL v2, LibreTranslate, Google Translate v2) — existing SDKs work unmodified against it, you just override the base URL.

```bash
translate "Hallo Welt" --to en                        # auto-detect source
translate "hello world" --from en --to de
translate --detect-only "Ceci est une phrase française."   # → fr  0.999956
printf 'Line one.\n\nLine two.\n' | translate --to en --from de --format ndjson
translate --batch --to en < lines.txt                  # each line = independent unit
translate --serve --port 8989                          # DeepL/LibreTranslate/Google v2 server
```

Server endpoints once running: `POST /v2/translate`, `GET /v2/languages`, `GET /v2/usage` (DeepL-shaped); `POST /translate`, `POST /detect` (LibreTranslate-shaped); `POST /language/translate/v2` (Google-shaped); `GET /health`. Point the official `deepl` Python SDK or `libretranslatepy` at `http://127.0.0.1:PORT` and it just works.

Code spans, URLs, and emails inside text pass through untranslated automatically. Preserves line breaks/paragraph cadence by default.

**When to reach for `translate`:** batch-translating files, wiring a translation step into a pipeline, or replacing a paid DeepL/Google Translate API call with a free local one during dev — swap the base URL, keep the client code.

---

## apfel-mcp — give apfel the web

`apfel`'s 3B model can't browse. `apfel-mcp` ships three stdio MCP servers, engineered for the 4096-token budget (hard char caps, Readability extraction, arg-name tolerance for a small model's hallucinated field names):

| Binary | Does | Cap |
|---|---|---|
| `apfel-mcp-url-fetch` | Fetch a URL, strip nav/ads, convert to Markdown | 6000 chars |
| `apfel-mcp-ddg-search` | DuckDuckGo HTML scrape, no API key (unofficial) | 2000 chars |
| `apfel-mcp-search-and-fetch` ★ | Search **and** fetch top N results in ONE call — saves a round-trip vs. chaining the two above | 5000 chars, default 2 results |

```bash
brew install Arthur-Ficial/tap/apfel-mcp
apfel --mcp $(which apfel-mcp-search-and-fetch) "use the search tool to find what macOS Tahoe is"
```

Prefer `search-and-fetch` over chaining `ddg-search` + `url-fetch` separately — it's declared under both `search` and `web_search` in `tools/list` so the small model's inconsistent tool-naming still routes correctly, and it saves ~500 tokens of schema overhead per turn that apfel's tiny context can't spare. Private-network URLs (10.0.0.0/8, 127.0.0.0/8, etc.) are SSRF-blocked by default.

---

## apfel-run — persistent config for apfel

`apfel` itself has zero config file — every setting is a CLI flag. `apfel-run` is the optional stateful layer on top: a TOML (or JSON) config with named profiles, drop-in for the `apfel` binary itself.

```bash
brew install Arthur-Ficial/tap/apfel-run
apfel-run config init                      # writes ~/.config/apfel/config.toml
$EDITOR ~/.config/apfel/config.toml
apfel-run "your prompt"                    # runs apfel using the active profile
apfel-run -p research "summarize this url" # switch profile
apfel-run config show --format flags       # see the exact argv it will produce
```

Example profile wiring MCP servers persistently instead of typing `--mcp` every time:

```toml
[profile.research]
system_prompt = "Ground every answer in real sources."
[[profile.research.mcp.server]]
path = "/opt/homebrew/bin/apfel-mcp-search-and-fetch"
```

Config discovery follows the XDG cascade (project-local `./apfel.toml` first, then `$XDG_CONFIG_HOME`, then `~/.config/apfel/`, then `/etc/xdg/`). Secrets never go in the file directly — use `token_env = "MY_TOKEN_VAR"` to point at an environment variable instead; `apfel-run config validate` refuses configs with raw tokens.

**When to reach for `apfel-run`:** the user wants apfel behavior (system prompt, temperature, attached MCP servers) to persist across invocations instead of re-typing flags, or wants multiple named setups (e.g. a "chat" profile vs. a "research" profile with web MCPs attached).

---

## Quick troubleshooting

- **"command not found" after brew install:** confirm `/opt/homebrew/bin` is on PATH; these are Apple Silicon-only formulae.
- **Model seems to refuse or give short/odd answers:** likely hitting the 4,096-token combined context window, or a prompt Apple's model is designed to refuse rather than hallucinate through — shorten the input or split the task.
- **Nothing works at all:** check Apple Intelligence is actually enabled (System Settings → Apple Intelligence & Siri) — enabling it triggers the on-device model download, it's a prerequisite for all five tools, not just `apfel`.
- **Server mode security:** off by default; `--token` enables Bearer auth. Don't expose `--serve` on a non-loopback interface without it.
