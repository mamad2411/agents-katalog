---
name: latitude-telemetry
description: Install or audit Latitude LLM observability — sends traces from LLM SDKs (OpenAI, Anthropic, Bedrock, Cohere, TogetherAI, Vertex AI, Google AI Platform, OpenAI Agents, Vercel AI SDK, Mastra, LangChain, LlamaIndex) to a Latitude project. TypeScript via `@latitude-data/telemetry`, Python via `latitude-telemetry`, and any other OpenTelemetry-supported language (Go, Java, Ruby, .NET, PHP, Rust, Elixir, …) via direct OTLP HTTP. Use when the user asks to add Latitude tracing, wire Latitude into an existing OpenTelemetry setup, fix missing traces in Latitude, or audit an existing integration. Covers codebase discovery (existing OTel, conflicting LLM-observability vendors, which LLM SDKs are in use, where LLM calls happen), class-based bootstrap (`new Latitude({...})` in TS, `Latitude(...)` in Python), advanced setup with `LatitudeSpanProcessor` and `registerLatitudeInstrumentations`, optional `capture()` for user/session/tags context (and per-capture `projectSlug` for multi-project apps), env vars (`LATITUDE_API_KEY`, `LATITUDE_PROJECT_SLUG`), and an OTLP fallback path for non-TS/Python codebases.
---

# Latitude Telemetry

Install Latitude LLM observability into a user's codebase **correctly the first time**. Most failed installs share the same root cause: telemetry was added in a place that does not actually run an LLM call, so no traces appear. This skill guides you through codebase discovery before writing any code.

## Rules you must not break

**Rule 1 — `capture()` does NOT create spans.** It only attaches user/session/tags/metadata to spans that auto-instrumentation creates from inside the callback.

**Rule 2 — TypeScript only: always `await latitude.ready` before the first LLM call.** The TS `new Latitude({...})` returns immediately and registers patches in the background. If the first LLM call fires before `ready` resolves, the patch may not have hooked the SDK yet and the trace is silently lost. Past installs by this skill have shipped without the await and produced empty trace lists. Make this the first line after `new Latitude({...})`. **Python does not have this rule** — `Latitude(...)` registers instrumentations synchronously in `__init__`; there is no `ready` attribute and nothing to await.

**Rule 3 — Always look up the latest pre-release version and pin to it.** The SDK is on the `alpha` / `beta` channel and changes frequently; the `@alpha` dist-tag and `--pre` flag both float, which means re-running this skill (or the user's CI) can silently land on a different version with a different API surface. At install time, run the lookup command (Step 2 below) to find the current latest, and pin the install to that exact version. Update the user's lockfile so the version is captured. Do not skip this — half the "the docs say X but my code says Y" bug reports trace back to a floating pre-release tag landing on an older version than the skill expects.

**Rule 4 — Never silently fall through on missing env vars.** When `LATITUDE_API_KEY` is missing (or set to a placeholder like `your-api-key`, `xxx`, `<replace-me>`), surface the gap to the user with explicit ❌ markers — never just continue. See Step 1a / 1b for the exact checklist format. The user must see at a glance which variables are missing and where to add them. (`LATITUDE_PROJECT_SLUG` is **optional** under the class-based SDK — see Step 1 — but if the user is on the single-project pattern they still need it. Treat it as required unless you've confirmed they need the per-capture override pattern.)

**Rule 5 — Never write credential values to `.env` (or any secrets file) yourself.** The user must paste the API key and project slug into the file with their own hands. You do not have a way to know whether the values you'd write are real — past runs of this skill have invented plausible-looking but fake keys (`lat_sk_...`, `proj_abc123`) and saved them to `.env`, so the install "completed" but no traces ever flowed. Even if the user pastes a value into the chat, **do not transcribe it into `.env`** — show them the exact line to add and have them write it themselves. You may create or edit `.env.example` with empty placeholders (`LATITUDE_API_KEY=`, `LATITUDE_PROJECT_SLUG=`) and you may confirm `.env` is in `.gitignore`, but the real values are user-write-only.

Concretely for Rule 1:

- ✅ `capture("handle-chat", () => openai.chat.completions.create(...))` — the OpenAI auto-instrumentation creates the span; `capture` decorates it.
- ❌ `capture("compute-prompt", () => buildPromptString(...))` — no LLM call inside, no span, no trace.
- ❌ Wrapping the whole HTTP server `register` callback — telemetry has not started yet.

If the user reports "no traces appear," 90% of the time the `capture()` callback does not invoke an auto-instrumented LLM SDK, **or** Rule 2 was skipped (TS), **or** the version pinned by Rule 3 has drifted from what the install code expects. Verify those three before debugging anything else.

## Workflow

Run these steps in order. Do not skip discovery — that is what makes this skill different from "read a README and paste a snippet."

### Step 1 — Confirm credentials exist and reach the project

Latitude needs an API key, and (in the simplest pattern) one project slug. This skill targets production Latitude only — the ingest endpoint is `https://ingest.latitude.so` and is not configurable through this skill.

| Variable | Required | Where to find it |
| --- | --- | --- |
| `LATITUDE_API_KEY` | yes | [https://console.latitude.so/settings/api-keys](https://console.latitude.so/settings/api-keys) → click **New key** → copy the value (it is shown once). |
| `LATITUDE_PROJECT_SLUG` | usually yes (see note) | Open the project in the console; the URL is `https://console.latitude.so/projects/<slug>`. The `<slug>` segment is the value. |

**Note on `LATITUDE_PROJECT_SLUG`**: the class-based SDK accepts a constructor without a `projectSlug` / `project_slug` — useful when a single process emits to several Latitude projects and each `capture()` declares its own slug. Default behavior in this skill is still "one project, slug in the constructor" because that covers the vast majority of installs. Switch to the multi-project pattern only if the user explicitly says they want it; see [references/project-scoping.md](references/project-scoping.md).

#### 1a. Look in the repo first

Before asking the user, search for already-configured credentials in this order:

1. `.env`, `.env.local`, `.env.development`, `.env.production`, `.env.example`
2. Host-specific secrets files (`fly.toml`, `vercel.json`, IaC manifests, Helm `values.yaml`, GitHub/GitLab CI variables in workflow files)
3. Existing `process.env.LATITUDE_*` / `os.environ["LATITUDE_*"]` references in code

For each variable, classify it as one of:

- ✅ **Set with a real value** in one of the locations above.
- ❌ **Missing** — not present anywhere, or only present as an empty string / placeholder (`""`, `your-api-key`, `xxx`, `<replace-me>`, `changeme`).

If both values are ✅, jump to 1c. If anything is ❌, go to 1b — and only ask for the variables that are actually missing.

#### 1b. How to ask, if missing

When one or more variables are missing, **report the gap to the user using ❌ explicitly** — do not bury it in prose. The user must be able to see at a glance which variables are missing and where they need to be set. Use a checklist format like this (adapt to whatever target file you detected — `.env`, `.env.local`, `fly.toml`, `vercel.json`, GitHub Actions secrets, Helm values, etc.):

```
Latitude credentials check — target: .env

❌ LATITUDE_API_KEY — missing
❌ LATITUDE_PROJECT_SLUG — missing
```

If only one is missing, mark the present one with ✅ and the missing one with ❌, so the user sees both states. Detect the right target file from what already exists in the repo (e.g. if the repo uses `.env.local`, write there; if it uses Doppler / Fly secrets / Vercel env, name those instead of inventing a `.env`).

Then **walk the user through how to get each missing value** — give them clickable URLs and step-by-step instructions, not vague "look in settings" hints. **You will not write the values to the file; the user will.** Use this template, including only the bullets for variables that are ❌:

> Here is how to get the missing values. **You will need to add them to `<file>` yourself — I will not write secrets to that file for you.**
>
> **`LATITUDE_API_KEY`**
> 1. Open [https://console.latitude.so/settings/api-keys](https://console.latitude.so/settings/api-keys) (sign up at [https://console.latitude.so](https://console.latitude.so) first if you don't have an account).
> 2. Click **New key**, give it a name (e.g. `local-dev` or the service name), and copy the value — it is only shown once.
>
> **`LATITUDE_PROJECT_SLUG`**
> 1. Open the project you want to send traces to in the console. The URL will look like `https://console.latitude.so/projects/<slug>`.
> 2. Copy the `<slug>` segment from the URL — that is the value.
> 3. If you don't have a project yet, create one at [https://console.latitude.so](https://console.latitude.so) and the slug is generated from the project name.
>
> Then paste these two lines into `<file>` (replacing `…` with the values you just copied) and save the file:
>
> ```
> LATITUDE_API_KEY=…
> LATITUDE_PROJECT_SLUG=…
> ```
>
> Tell me when it is saved and I will re-check.

**Do not transcribe the values into `<file>` yourself, even if the user pastes them into the chat.** If the user pastes a key into the chat, acknowledge it but instruct them to put it in `<file>` themselves — you cannot verify it is a real key, and prior runs of this skill have written invented or placeholder values that broke the install silently.

What you *may* do without a real value:
- Create or edit `.env.example` with empty placeholders: `LATITUDE_API_KEY=` and `LATITUDE_PROJECT_SLUG=` so collaborators know which keys to set.
- Confirm `.env` (or whichever target you detected) is listed in `.gitignore` and add it if missing.
- Re-run the ❌/✅ check after the user reports they've saved the file, and show the updated checklist so they can confirm everything is now ✅ before moving on.

Never hardcode the key in source code either; load from `process.env` / `os.environ` only.

#### 1c. Verify credentials reach the project before writing any code

Run the curl probe in [references/otlp-fallback.md](references/otlp-fallback.md#verify-with-curl) — it works regardless of language and tells you in one shot:

- `202` → credentials valid, project exists. Continue.
- `401` → bad API key. Re-check at [https://console.latitude.so/settings/api-keys](https://console.latitude.so/settings/api-keys).
- `400` with a missing-project message → wrong project slug or wrong header name.

Do not write SDK code until the probe returns `202`. This catches the LAT-558 class of bug ("code looks fine, no traces appear") at the credential layer instead of after a full implementation.

### Step 2 — Look up the latest pre-release and pin to it (mandatory)

The SDK is still on the `alpha` / `beta` channel and the API surface changes between releases. The default install tags (`@alpha` on npm, `--pre` on pip) **float** — they resolve to whatever is current at the moment of install. That means re-running this skill, or re-running the user's CI weeks later, can silently land on a different version than the one this skill was written against. Past installs hit this exact bug: the skill prescribed an API the floating tag could no longer resolve, and the install produced no traces.

Look up the current latest *before* writing any install command, then pin the user's package manifest to that exact version (do not use ranges like `^` or `~`).

#### TypeScript

```bash
# Returns something like 3.0.0-alpha.10 (or 3.0.0-beta.0 once the channel moves).
npm view @latitude-data/telemetry@alpha version
```

Cross-check the package's public CHANGELOG for the same version at [`packages/telemetry/typescript/CHANGELOG.md`](https://github.com/latitude-dev/latitude-llm/blob/main/packages/telemetry/typescript/CHANGELOG.md) — if you see a newer entry there than the npm response, the publish is in flight; wait or use the npm value (the source of truth for installs is the registry, not the changelog).

If the SDK has moved past alpha to beta, `npm view @latitude-data/telemetry@beta version` is the right command instead. When in doubt, run both and use the higher version.

Install with the exact version:

```bash
npm install @latitude-data/telemetry@3.0.0-alpha.10  # substitute the actual version
# or pnpm add / yarn add / bun add — same exact-version syntax
```

#### Python

```bash
# Lists all versions; the first non-stable entry is the current pre-release (alpha or beta).
pip index versions latitude-telemetry --pre
# Or with uv:
uv pip install --prerelease=allow latitude-telemetry --dry-run 2>&1 | grep latitude-telemetry
```

Install with the exact version:

```bash
pip install "latitude-telemetry==3.0.0a10"  # substitute the actual version
# or uv pip install "latitude-telemetry==3.0.0a10"
# or poetry add "latitude-telemetry==3.0.0a10" --allow-prereleases
```

#### Why the lockfile matters

After install, confirm the user's lockfile (`package-lock.json` / `pnpm-lock.yaml` / `yarn.lock` / `uv.lock` / `poetry.lock` / `requirements.txt`) captures the exact version. If the project uses a manifest format that allows floating ranges (some `requirements.txt` setups, pre-lock-era `package.json`), call out the risk explicitly so the user can decide whether to add a lock or live with the float.

If the user's CI later picks a newer version with a different API, the next debug session starts with `npm view @latitude-data/telemetry@alpha version` to confirm the drift — make sure they know.

### Step 3 — Discover the codebase

Before deciding which install path to use, gather these facts. Read code and grep — only ask the user when the codebase truly cannot answer.

#### 3a. Language gate (do this first)

Detect the host language **before** anything else. Latitude ships first-class SDKs only for TypeScript and Python; everything else uses a different install path.

| Language | Path |
| --- | --- |
| TypeScript / JavaScript / Node | Continue with this skill — `@latitude-data/telemetry` |
| Python | Continue with this skill — `latitude-telemetry` |
| Go, Java, Ruby, .NET, PHP, Rust, Elixir, Kotlin, Swift, anything else | **Stop and switch to [references/otlp-fallback.md](references/otlp-fallback.md)** — there is no Latitude SDK for this language; install standard OpenTelemetry pointed at the OTLP HTTP endpoint instead |

If the codebase mixes languages (e.g. Python backend + Go data pipeline), instrument each independently using the right path per language. Do not bridge them through one SDK.

Once the language is confirmed as TS or Python, also note:

- TypeScript / Node — Plain Node, Next.js, NestJS, Hono, Fastify, Express, CLI script?
- Python — FastAPI, Flask, Django, Celery worker, plain script, notebook?
- Process shape — long-running server, cron, serverless function, one-shot CLI, batch job?

#### 3b. Existing OpenTelemetry instrumentation

Grep for these. If any are present, the install path changes from bootstrap to advanced.

| Search term | What it indicates |
| --- | --- |
| `@opentelemetry/sdk-node`, `@opentelemetry/sdk-trace-node`, `NodeSDK`, `NodeTracerProvider` | Existing TS OTel SDK |
| `opentelemetry.sdk.trace`, `TracerProvider()` | Existing Python OTel SDK |
| `OTEL_EXPORTER_*`, `OTEL_SERVICE_NAME`, `OTEL_TRACES_*` env vars | Configured OTel exporter |
| `instrumentation.ts`, `instrumentation.js` (Next.js) | OTel hook already wired |

If found, the class-based SDK auto-detects the existing provider and attaches `LatitudeSpanProcessor` to it — `new Latitude({...})` is still the right entry point, just pass `tracerProvider` (TS) / `tracer_provider` (Py) when you want to be explicit. Do not create a second provider; the SDK will warn if it cannot attach.

#### 3c. Conflicting LLM observability vendors

Grep for these. If any are present, do not silently overlap — ask the user whether they want to keep, replace, or run in parallel.

```
langfuse  langsmith  traceloop  helicone  arize  phoenix  openllmetry  weights-and-biases  wandb
```

Special cases:

- **Traceloop OpenLLMetry**: shares the same underlying instrumentations Latitude uses. Two registrations of the same instrumentation can cause double-counting. Pass Traceloop's `TracerProvider` to `new Latitude({ tracerProvider: ... })` so Latitude attaches instead of duplicating.
- **Langfuse / LangSmith**: independent vendors. They can coexist with Latitude through OTel, but the user should explicitly want both.

#### 3d. Which LLM SDKs are in use

Grep imports for the supported instrumentations. The result drives the `instrumentations` array.

| If you see in code | Add to `instrumentations` |
| --- | --- |
| `import OpenAI from "openai"` / `from openai import OpenAI` | `"openai"` (also covers `AzureOpenAI` from the same `openai` package) |
| `@anthropic-ai/sdk` / `anthropic` | `"anthropic"` |
| `@aws-sdk/client-bedrock-runtime` (TS) / `boto3` Bedrock client (Py) | `"bedrock"` |
| `cohere-ai` (TS) / `cohere` (Py) | `"cohere"` |
| `together-ai` (TS) / `together` (Py) | `"togetherai"` |
| `@google-cloud/vertexai` (TS) / `google-cloud-aiplatform` (Py) | `"vertexai"` |
| `@google-cloud/aiplatform` (TS) / `google-cloud-aiplatform` (Py) | `"aiplatform"` |
| `langchain`, `@langchain/*` (TS) / `langchain-core` (Py) | `"langchain"` |
| `llamaindex` (TS) / `llama-index` (Py) | `"llamaindex"` |
| `ai` (Vercel AI SDK) | **none** — see special case below |
| `@mastra/core` (Mastra) | **none** — TypeScript-only special case; do not install `@latitude-data/telemetry` at all. See special case below |
| `@openai/agents` (OpenAI Agents SDK) | `"openai-agents"` — has its own dedicated instrumentation; do NOT use `"openai"` for this. See [docs.latitude.so/telemetry/frameworks/openai-agents](https://docs.latitude.so/telemetry/frameworks/openai-agents) |

Special cases:

- **Vercel AI SDK (`ai`, `@ai-sdk/openai`, etc.)**: do **not** add an instrumentation entry for it. The AI SDK has native OpenTelemetry support. Initialize Latitude (`new Latitude({ apiKey, projectSlug })`) and pass `experimental_telemetry: { isEnabled: true, metadata: {...} }` on each `generateText` / `streamText` call. Latitude's smart filter picks up the AI SDK's `ai.*` spans automatically. Adding `"openai"` here would not produce extra traces and may cause double-counting.
- **Mastra (`@mastra/core`)**: TypeScript only. Mastra ships its own OpenTelemetry pipeline via `@mastra/observability` and `@mastra/otel-exporter`, emitting `gen_ai.*` spans natively. **Do not install `@latitude-data/telemetry`** — the integration is configured entirely through Mastra's `OtelExporter` with a `custom` provider pointed at Latitude's OTLP endpoint and the standard `Authorization` / `X-Latitude-Project` headers. See [references/typescript.md](references/typescript.md#mastra-example-shape) for the full setup. Source: `docs/telemetry/frameworks/mastra.mdx`.
- **LangChain / LlamaIndex**: register the wrapper instrumentation (`"langchain"` / `"llamaindex"`); you do **not** also need to register the underlying vendor.
- **Gemini consumer SDK (`@google/generative-ai`)**: not in the supported list. If the app is on Gemini, ask the user whether they can switch to `@google-cloud/aiplatform` / `@google-cloud/vertexai`, or fall back to manual span creation.
- **Custom HTTP clients (raw `fetch` to OpenAI, Anthropic, etc.)**: not covered by any auto-instrumentation. Either switch to the vendor SDK or write manual spans — `capture()` alone produces no traces.

#### 3e. Where LLM calls happen

This is the step the failed demo skipped. Find the actual call sites:

```bash
# TypeScript / Node
grep -rE "chat\.completions\.create|messages\.create|generateText|streamText|embeddings\.create" .
# Python
grep -rE "chat\.completions\.create|messages\.create|generate_content|complete\(" .
```

For each call site, walk back up the call stack to find the **entry point** (HTTP route handler, queue consumer, CLI command, agent loop iteration). The entry point is where `capture()` belongs — if `capture()` is used at all. Telemetry initialization belongs **earlier**, at process startup.

If you cannot determine the entry point, ask the user: *"I see LLM calls in `X.ts:42`. What triggers this code — an HTTP request, a background job, a CLI command? I need this to know where to wrap the request boundary."*

### Step 4 — Decide the install path

The class-based SDK collapses the old two-path decision into one constructor: `new Latitude({...})` detects an existing OpenTelemetry provider and attaches its span processor to it; if none exists, it creates and registers one. You almost never need a second code path.

```
Existing OTel TracerProvider in the codebase?
├─ Yes (registered globally) → new Latitude({ apiKey, projectSlug, instrumentations }) auto-attaches
├─ Yes (held in a variable)  → new Latitude({ apiKey, projectSlug, instrumentations, tracerProvider })
└─ No                         → new Latitude({ apiKey, projectSlug, instrumentations }) creates + registers
```

Conflicting LLM-observability vendor?

- **Traceloop** → pass Traceloop's `TracerProvider` explicitly via `tracerProvider`, so Latitude attaches instead of registering a duplicate.
- **Langfuse / LangSmith** → confirm intent with user; if keeping both, ensure both are processors on the same provider.
- **None** → default constructor is fine.

The legacy `initLatitude` / `init_latitude` functions still exist as thin wrappers, but new installs should use `new Latitude({...})` / `Latitude(...)` directly — the class exposes `.provider`, `.flush()`, and `.shutdown()` as proper methods/attributes, and the Python class makes the old "use item access on the dict return value" rule obsolete.

### Step 5 — Place the initialization correctly

Initialization must run **once per process** at startup, **before** the first LLM call. Patch-based auto-instrumentation also requires init to run **before** the LLM client is constructed when the patch hooks the constructor.

#### TypeScript: keep it inline, do not create new files

For TypeScript installs, **do not invent a new telemetry module** (`telemetry.ts`, `lib/latitude.ts`, `setup/observability.ts`, etc.). Add `new Latitude({...})` directly to the file where the LLM call already lives, at the top, before the LLM SDK is used. Less indirection means less to debug when traces don't appear.

Minimal shape — copy this when adding to a single-file script that uses the Vercel AI SDK:

```typescript
import { Latitude, capture } from "@latitude-data/telemetry";
import { generateText } from "ai";
import { openai } from "@ai-sdk/openai";

const latitude = new Latitude({
  apiKey: process.env.LATITUDE_API_KEY!,
  projectSlug: process.env.LATITUDE_PROJECT_SLUG!,
});

await latitude.ready; // REQUIRED — see Rule 2 at top of skill

await capture("generate-support-reply", async () => {
  const { text } = await generateText({
    model: openai("gpt-4o"),
    prompt: "Hello",
    experimental_telemetry: { isEnabled: true },
  });
  return text;
});

await latitude.shutdown();
```

The only times you should put init in a separate file are framework-mandated bootstrap files that **already exist** (e.g. Next.js `instrumentation.ts`, NestJS `main.ts`, an existing `server.ts` / `index.ts`). Even then: edit the existing file, do not create a wrapper module around the constructor.

Common locations by stack:

| Stack | Place init in |
| --- | --- |
| Next.js (App Router) | `instrumentation.ts` `register()` hook (Node runtime only) |
| Plain Node server | top of `server.ts` / `index.ts`, before any LLM client import |
| NestJS | `main.ts` before `NestFactory.create` |
| Express / Fastify / Hono | top of the bootstrap file, before route registration |
| Python FastAPI | app factory or `lifespan` startup, before route imports trigger LLM client creation |
| Python Celery | worker `__init__` or `worker_process_init` signal |
| CLI / one-shot script | very top of the entrypoint, before any LLM client import |

For TypeScript, **import order matters**. Telemetry imports first, then the LLM SDK. If the bundler reshuffles imports (Next.js, esbuild with certain settings), pass `modules` to `registerLatitudeInstrumentations` (see [references/typescript.md](references/typescript.md)).

#### Python: drop the dict-access idiom

The class-based `Latitude(...)` exposes real attributes and methods: `latitude.provider`, `latitude.flush()`, `latitude.shutdown()`. The old `init_latitude(...)` returned a `TypedDict`, which forced `latitude["flush"]()` — that idiom is gone for new installs and any audit should flag it (see [references/audit-checklist.md](references/audit-checklist.md)). The legacy function still exists as a thin wrapper that returns the same dict for back-compat; do not use it in new code.

#### Short-lived and serverless processes

Long-running servers can rely on the batch span processor flushing on its own schedule. Anything that exits quickly cannot:

- CLI scripts, one-shot jobs, notebooks → `await latitude.shutdown()` (TS) or `latitude.shutdown()` (Py) before exit.
- Serverless handlers (Lambda, Vercel Functions, Cloud Run, Cloud Functions) → `await latitude.flush()` (TS) / `latitude.flush()` (Py) after the LLM work completes, before the response is returned (or before the isolate suspends). Decide per route whether the latency cost is acceptable; for streaming responses, flushing after the stream completes is usually correct.
- Next.js App Router on Edge runtime → not supported; force `runtime = "nodejs"` on any route that calls LLM SDKs.

### Step 6 — Add `capture()` only where it makes sense

Re-read the rule at the top of this skill before adding `capture()`. Then:

- Wrap **coarse** boundaries: a request handler, a queue job, an agent turn.
- Wrap code that **definitely** invokes an auto-instrumented LLM SDK.
- Do not wrap pure functions, prompt builders, parsers, validators — they create no spans, so `capture()` decorates nothing.
- Do not wrap the application bootstrap or `register()` hook.

If the user only needs raw spans (no user/session attribution), skip `capture()` entirely. Auto-instrumentation alone produces useful traces.

#### Per-capture project override (multi-project apps)

`capture()` accepts an optional `projectSlug` (TS) / `project_slug` (Py) that routes the wrapping span and its children to a specific Latitude project, overriding whatever default the constructor set. This is the right pattern when one process should emit traces to several projects (e.g. multiple agents in the same runtime). Full guidance, the precedence chain, and the bare-OTel resource-attribute alternative live in [references/project-scoping.md](references/project-scoping.md). Do **not** spin up a second `Latitude` instance to reach a second project — use the per-capture override.

### Step 7 — Verify before reporting done

Do not declare success based on "the code compiles." Verify a trace lands in Latitude:

1. Run the app (or the relevant script) and trigger one LLM call.
2. Open the Latitude UI → Traces and confirm at least one new trace appears.
3. If no trace:
   - Re-check `LATITUDE_API_KEY` and `LATITUDE_PROJECT_SLUG`.
   - Re-check the version pin from Step 2 — running `npm view @latitude-data/telemetry@alpha version` again should match what's installed; if it's higher, the alpha tag has moved and the install needs an update.
   - Re-check that the `instrumentations` array includes the SDK actually being called.
   - For TypeScript: pass `modules: { openai: OpenAI }` (or matching vendor) to `registerLatitudeInstrumentations` — bundler-resolved module instances may not match the SDK's auto-`require`.
   - For short-lived processes: ensure `await latitude.shutdown()` (or `latitude.flush()`) runs before exit.
   - Check whether the smart filter is dropping spans (`disableSmartFilter` for diagnostic runs).

### Step 8 — Add context (optional, infer first, ask second)

Once raw traces are flowing, suggest context additions based on what the codebase already exposes. **Infer from code; only ask when the answer is not in the code.**

| If you see in code | Suggest |
| --- | --- |
| `req.user.id`, `session.userId`, auth middleware | `userId` on the wrapping `capture()` |
| Conversation history, `messages` array, chat threads | `sessionId` |
| Multiple distinct routes / agents | `tags: ["<feature-name>"]` |
| Tenant or workspace identifiers | `metadata: { tenantId }` |
| Environment differentiation (`process.env.NODE_ENV`) | `tags: ["production" | "staging"]` |

Do not blanket-add context. Each addition has a maintenance cost; prefer small, intentional sets.

## Documentation workflow

When package APIs may have drifted, fetch the current README:

- TypeScript: `https://raw.githubusercontent.com/latitude-dev/latitude-llm/main/packages/telemetry/typescript/README.md`
- Python: `https://raw.githubusercontent.com/latitude-dev/latitude-llm/main/packages/telemetry/python/README.md`
- Product docs: `https://docs.latitude.so/telemetry/overview`

If the README and this skill disagree, **the README wins**. Offer to update this skill when drift is found.

## When to read which reference

| Situation | Open |
| --- | --- |
| TypeScript / Node specifics, ESM gotchas, `modules` option, per-SDK notes, Next.js | [references/typescript.md](references/typescript.md) |
| Python specifics | [references/python.md](references/python.md) |
| Multi-project apps (per-capture `projectSlug`, resource attribute, bare-OTel routing) | [references/project-scoping.md](references/project-scoping.md) |
| Non-TS/Python codebases (Go, Java, Ruby, .NET, PHP, Rust, Elixir, …) | [references/otlp-fallback.md](references/otlp-fallback.md) |
| Auditing an existing integration or a PR | [references/audit-checklist.md](references/audit-checklist.md) |

## Packages

**Step 2 is mandatory — look up the latest pre-release and pin to it.** Don't use floating tags like `@alpha` or `--pre` for the final install command; use them only to *discover* the current version, then write that exact version to the user's package manifest. See Step 2 above for the lookup commands.

| Language | Public surface |
| --- | --- |
| TypeScript / Node | `Latitude` (class), `LatitudeSpanProcessor`, `registerLatitudeInstrumentations`, `capture`. Legacy: `initLatitude` (wrapper around the class). |
| Python (3.11+) | `Latitude` (class), `LatitudeSpanProcessor`, `register_latitude_instrumentations`, `capture`. Legacy: `init_latitude` (returns a dict — only present for back-compat; new code uses the class). |

Other package managers translate the exact-version pin the same way: `pnpm add @latitude-data/telemetry@<version>`, `yarn add @latitude-data/telemetry@<version>`, `bun add @latitude-data/telemetry@<version>`, `uv pip install "latitude-telemetry==<version>"`, `poetry add "latitude-telemetry==<version>" --allow-prereleases`. The exact pin is mandatory; floating tags will silently drift.

## Common mistakes

| Mistake | Why it fails | Fix |
| --- | --- | --- |
| `capture()` wraps a non-LLM function | No span is created — `capture()` only decorates existing spans | Move `capture()` to the boundary that calls the LLM SDK |
| `await latitude.ready` skipped (TS) | First LLM call races the patch registration; trace silently dropped | Always put `await latitude.ready` directly after `new Latitude({...})`. (Python has no equivalent — registration is synchronous.) |
| New `telemetry.ts` / `lib/latitude.ts` module created to hold init | Adds an import layer that often runs the LLM SDK before init; pure indirection | Inline `new Latitude({...})` in the file that already runs the LLM call |
| `new Latitude({...})` runs after the LLM client is constructed | Patch never applied | Import telemetry first; in Next.js use `instrumentation.ts` |
| Floating `@alpha` / `--pre` install tag | Re-runs land on different versions; the skill's API surface may not match what's installed | Use Step 2's lookup command, then pin to the exact version |
| `instrumentations: []` while OpenAI is in use | No vendor patched, no spans | Add `"openai"` (or matching vendor) |
| Adding `"openai"` to `instrumentations` for Vercel AI SDK code | Double-counted spans, confusing traces | The AI SDK has native OTel; just enable `experimental_telemetry: { isEnabled: true }` per call. Do not register `"openai"` for AI SDK paths. |
| Python: `latitude["shutdown"]()` (item access on the class) | The class has methods, not dict keys — item access fails | Use `latitude.shutdown()` / `latitude.flush()`. Item access is only correct for the legacy `init_latitude(...)` return value, which new installs should avoid. |
| Two `new Latitude({...})` instances to reach two projects | Second instance warns about provider attachment; double-processes spans | Use one instance + per-capture `projectSlug` override — see [references/project-scoping.md](references/project-scoping.md) |
| Hardcoded API key | Leaks in repo, breaks per-env config | Read from `process.env` / `os.environ` |
| Agent writes the API key / slug to `.env` itself | Agent has no way to know if the value is real; past runs have invented plausible-looking fakes (`lat_sk_...`, `proj_abc123`) and the install silently never produced traces | The user must write `.env` themselves; agent only shows the lines to add and may edit `.env.example` with empty placeholders |
| Script exits before flush | Buffered batches dropped | `await latitude.shutdown()` (TS) or `latitude.shutdown()` (Py) |
| Two OTel `TracerProvider` instances | Spans split across providers | Pass the existing provider to `new Latitude({ tracerProvider })` |
| Edge runtime on Next.js | OTel exporters/patches assume Node | Force `runtime = "nodejs"` on the route |
| Bundler resolves a different `openai` module | Auto-require patches the wrong instance | Pass explicit `modules: { openai: OpenAI }` to `registerLatitudeInstrumentations` |

## Skill maintenance

If this skill gives wrong or outdated guidance, the README under `packages/telemetry/{typescript,python}` and the docs at `docs.latitude.so/telemetry/*` are the source of truth. Offer to file an issue or open a PR against `latitude-dev/skills` when drift is found.
