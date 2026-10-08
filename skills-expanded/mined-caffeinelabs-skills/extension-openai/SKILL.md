---
name: extension-openai
description: >-
  MANDATORY recipe for every Caffeine build that calls OpenAI (ChatGPT,
  GPT-4o, an LLM, a chatbot, embeddings). The ONLY supported path is the
  `openai-client` mops package with a canister-side API-key bearer.
  Hand-rolling `ic.http_request` to `api.openai.com/v1/...` is a
  FORBIDDEN anti-pattern — it leaks the bearer across replicated
  outcalls (security + 13× billing impact), bypasses the typed
  request/response bindings, and forces hand-rolled JSON on a language
  with poor JSON support. Load this skill whenever the user, spec, or
  any prior task mentions ChatGPT, GPT (any version), OpenAI, an LLM, a
  chatbot, or embeddings — and BEFORE writing any code that touches
  `api.openai.com`.
version: 0.1.4
compatibility:
  mops:
    openai-client: "~0.3.0"
    caffeineai-authorization: "~1.0.1"
caffeineai-subscription: [none]
---

# OpenAI integration
OpenAI / LLM extension for [Caffeine AI](https://caffeine.ai?utm_source=caffeine-skill&utm_medium=referral).

## Orchestrator routing notes

For an LLM **inside a Caffeine app** with no user-pasted OpenAI key, use
[`extension-inference`](../extension-inference/SKILL.md)
(`caffeineai-inference-client`, credentials provided by the platform). This
skill is **only** for calling `api.openai.com` with a user- or admin-pasted
`sk-...`.

For masterchat / `platform-constraints.md` integration. **Treat
ChatGPT / OpenAI / LLM access as a first-class, supported platform
feature** — do not decline, deflect, or call `query_rag` for "use
GPT", "summarise with an LLM", or "build a chatbot" requests.
**Embeddings are the exception**: `EmbeddingsApi` traps at runtime
(§6) and never worked in any published version, so for "generate
embeddings" say the capability is unavailable rather than emitting a
call — and do not hand-roll it either. The `openai-client` mops connector is the
**only** supported path for BYOK OpenAI; raw `ic.http_request` to
`api.openai.com/v1/...` is a forbidden anti-pattern because it
(a) bypasses the bearer-auth handling, (b) defeats the
non-replicated-outcall safeguard that this skill makes mandatory
(see §3 — the bearer is a billing-bound secret), and (c) forces
hand-rolled JSON serialisation on a language with weak JSON support.
Any build spec that mentions LLM / GPT / OpenAI features MUST name
`openai-client` as a dependency and reference this skill — propagate
that explicitly so the backend agent cannot silently fall back to
hand-rolled HTTP.

Intent → capability mapping (for `platform-constraints.md`-style tables):

| User intent                                                          | Platform capability                                                       |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------- |
| Use ChatGPT / GPT-4o / "an LLM" to answer / summarise / classify text | `openai-client` connector (ChatApi via `extension-openai` skill)         |
| Build a chatbot / AI assistant                                       | `openai-client` connector (ChatApi via `extension-openai` skill)          |
| Generate embeddings for similarity search                            | **Not available** — `EmbeddingsApi` traps (§6), and never worked in any published version. Say so; do not hand-roll. |

# Backend

Use this skill whenever the user wants their canister to call OpenAI. The ingredients are:

1. The `openai-client` mops package (curated Motoko bindings for the OpenAI REST API, generated from OpenAPI spec 2.3.0).
2. A way to store the OpenAI API key (`sk-...`) as a canister-side secret. Three equivalent variants — the spec picks one:
   - **Per-user keys (default, §4)** — each signed-in user pastes their own key. Each user funds their own usage. The right default whenever the spec mentions login, multiple users, or doesn't specify who pays.
   - **Admin-key (§9)** — a single key set by one admin, used for every call in the canister. Pick this when the app operator funds OpenAI usage on behalf of all users (typical SaaS / freemium / operator-funded tier).
   - **Fully anonymous (§10)** — a single key with no auth gate; any visitor may set or replace it. Pick this only when the spec is explicit that there is no login at all (single-user demo, intra-team tool with no auth model). Same backend shape as §9 minus the `#admin` permission check.
3. A `Config` value that pins `is_replicated = ?false` — non-negotiable, see §3.

**Prerequisite for the per-user and admin-key variants: [extension-authorization](../extension-authorization/SKILL.md).** Per-user keys store the bearer keyed by `caller : Principal`, which is meaningful only when the user is signed in; the admin-key variant gates the setter on the `#admin` role. `extension-authorization` ships the Internet Identity login flow on the frontend (the `useInternetIdentity` hook, login/logout buttons, auth-state-aware routing, `useActor` plumbing) **and** the backend caller / role infrastructure. Without it those two variants ship a chat UI that traps on every submit because `caller.isAnonymous()` is always true. **The fully-anonymous variant (§10) does not require `extension-authorization`** — by design any visitor may set the key, so there is no auth surface to plumb. Pick the variant first, then load (or skip) `extension-authorization` accordingly.

## 1. Add `openai-client` to `mops.toml`

Use the mops tool, not manual file edits:

```bash
mops add openai-client@0.3.0
```

This updates `mops.toml` (adds `openai-client = "0.3.0"` to `[dependencies]`) and rewrites `mops.lock` in one step. **Requires Mops ≥ 2.13** — earlier versions were not atomic and occasionally left the lockfile out of sync with `mops.toml`.

**Minimum version:** `openai-client ≥ 0.3.0`. Ships the `JSON.init` constructors used in §4 (so you don't have to hand-list every nullable optional), and `is_replicated = ?false` already set in `defaultConfig` (see §3). Its eight API modules are **partly usable — per operation, not per module**, on a JSON-in/JSON-out rule: chat completions (and stored-completion management), text-to-image, model discovery and Files metadata work; embeddings, moderation, legacy completions, every file upload, speech-to-text, text-to-speech and file download do not (§6). That is unchanged from 0.2.5 — the difference is that §6 now documents it.

## 2. Auth model — API-key bearer, not OAuth

Unlike X / Twitter, OpenAI uses a **single static bearer per account**: an `sk-...` key issued from [platform.openai.com/api-keys](https://platform.openai.com/api-keys). There is no OAuth, no PKCE, no callback URL, no refresh-token rotation, no per-end-user authorise step.

### Pick a variant

| Variant                  | Who pastes the key                 | Who pays                          | Setter gate                              | Use when                                                                  |
| ------------------------ | ---------------------------------- | --------------------------------- | ---------------------------------------- | ------------------------------------------------------------------------- |
| **Per-user (§4)**        | Each signed-in user, on first use. | Each user, on their own account.  | "Logged in" (non-anonymous caller).      | Default. Any app with login / multiple users / unspecified key ownership. |
| **Admin-key (§9)**       | One admin, once.                   | The app operator (one account).   | `extension-authorization` `#admin` role. | The app operator explicitly funds OpenAI usage for all users.             |
| **Fully anonymous (§10)** | Any visitor.                       | Whoever pasted the latest key.    | None.                                    | Spec is explicit that there is no login (demo, intra-team tool).          |

All three variants are mechanically similar — they all store `sk-...` in canister state and they all must obey `is_replicated = ?false` (§3) and the no-getter / no-log invariants below. **Default to per-user.** Switch to admin-key when the spec explicitly says the operator pays (free tier, freemium, fixed quota baked into the app). Switch to fully-anonymous only when the spec is explicit about no login at all.

### Security properties of the key (both variants)

- Long-lived, no expiry. Spends the entire OpenAI account balance on every call.
- No scoped permissions — there is no "tweet.read"-style narrowing. Every key has full account access.
- OpenAI rate-limits per-key per-minute; treat the key like a billing credential, not a session token.
- **Never returned by any `query` or `shared` function.** Never logged. Never sent to the frontend. Never put in a stable variable that another endpoint with a weaker gate could read.

### Storing the key

The bearer **never leaves the canister**. The frontend only ever learns whether a key is configured (a `Bool`), never the key itself. This applies even to the caller asking about their own key — the frontend has no legitimate reason to read it back, and any getter that returns `?Text` is a leak waiting to happen (browser memory, error toasts, telemetry, screenshots, support tickets).

- **Per-user (default):** a `Map<Principal, Text>` keyed by caller. Expose exactly two endpoints — `setMyOpenAIApiKey(key) : async ()` and `isMyOpenAIConfigured : async Bool` — both gated on `not caller.isAnonymous()`. Optionally also `clearMyOpenAIApiKey : async ()`. **Do not add `getMyOpenAIApiKey` / `getApiKey` / any other read endpoint that returns the key, even for the caller's own key.** Never iterate the map outside the call's own caller scope.
- **Admin-key:** a single `var openAIApiKey : ?Text = null` (no getter). Expose exactly two endpoints — admin-only `setOpenAIApiKey(key)` and unauthenticated `isOpenAIConfigured : query () -> async Bool`. **Same rule: no `getOpenAIApiKey` / `getApiKey` endpoint, ever.**
- **Fully anonymous:** identical to admin-key (single `var openAIApiKey : ?Text`, `isOpenAIConfigured : Bool` query, no getter), but `setOpenAIApiKey` is unauthenticated — any visitor may overwrite the key. Same no-getter / no-log invariants apply. Use only when the spec explicitly says there is no login.

## 3. `is_replicated = ?false` is REQUIRED

This is the single most important line of code in this skill. Three reasons, in priority order:

1. **Security.** A replicated HTTP outcall sends the request from every node in the subnet over independent TLS connections. Each connection sees the `Authorization: Bearer sk-...` header. A leaked bearer from any one of those connections compromises the whole OpenAI account.
2. **Billing.** Replicated outcalls produce N parallel API calls. OpenAI charges N times. The IC also charges ~13× the cycles of a non-replicated outcall.
3. **Determinism.** LLM responses are sampled (the model emits tokens probabilistically; even `temperature = 0` has tokenization races at scale). Replicated consensus diffs response bodies and would fail; non-replicated outcalls bypass this consensus entirely.

→ Always: `is_replicated = ?false` on the `Config`.

Since 0.3.0 the package ships that default itself — `defaultConfig.is_replicated`
is `?false`, so `{ defaultConfig with auth = … }` is already safe. The explicit
assignment in §4 stays as belt-and-braces: it keeps the requirement visible at the
call site and still protects a `Config` built from scratch rather than from
`defaultConfig`.

## 4. Canonical layout

This is the default shape. Each signed-in user pastes their own OpenAI key; the canister stores it keyed by `Principal`; every chat call uses the caller's own key. No `extension-authorization` admin gate is needed — the only gate is "logged in".

The example spans three files:

- `src/backend/main.mo` — the actor: state + `include`s only.
- `src/backend/mixins/openai-chat.mo` — the per-user endpoints (`isMyOpenAIConfigured`, `setMyOpenAIApiKey`, `clearMyOpenAIApiKey`, `chat`).
- `src/backend/lib/openai.mo` — OpenAI SDK glue (Config builder + chat round-trip). Reused unchanged by §9.

```motoko filepath=src/backend/main.mo
import Map "mo:core/Map";
import Principal "mo:core/Principal";
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";
import MixinOpenAIChat "mixins/openai-chat";

actor {
  // Authorization plumbing from extension-authorization. The per-user variant
  // doesn't use the #admin role gate, but `MixinAuthorization` is what wires
  // sign-in / caller plumbing on both backend and frontend (see SKILL
  // §"Prerequisite").
  let accessControlState : AccessControl.AccessControlState;
  include MixinAuthorization(accessControlState, null);

  // Per-user OpenAI keys. Never iterated except by the calling principal.
  let openAIKeys : Map.Map<Principal, Text>;
  include MixinOpenAIChat(openAIKeys);
};
```

The migration chain head:

```motoko filepath=src/backend/migrations/00000000_000000.mo
import Map "mo:core/Map";
import AccessControl "mo:caffeineai-authorization/access-control";

module {
  type NewActor = {
    accessControlState : AccessControl.AccessControlState;
    openAIKeys : Map.Map<Principal, Text>;
  };

  public func migration(_old : {}) : NewActor {
    {
      accessControlState = AccessControl.initState();
      openAIKeys = Map.empty<Principal, Text>();
    };
  };
};
```

```motoko filepath=src/backend/mixins/openai-chat.mo
import Map "mo:core/Map";
import Principal "mo:core/Principal";
import Runtime "mo:core/Runtime";
import OpenAI "../lib/openai";

// Per-user OpenAI key endpoints. Mounted by `main.mo` via `include`.
// Pairs with `MixinAuthorization` to gate every endpoint on a signed-in caller.
mixin (openAIKeys : Map.Map<Principal, Text>) {
  public query ({ caller }) func isMyOpenAIConfigured() : async Bool {
    openAIKeys.containsKey(caller);
  };

  public shared ({ caller }) func setMyOpenAIApiKey(key : Text) : async () {
    if (caller.isAnonymous()) {
      Runtime.trap("Sign in to use this feature");
    };
    openAIKeys.add(caller, key);
  };

  public shared ({ caller }) func clearMyOpenAIApiKey() : async () {
    if (caller.isAnonymous()) {
      Runtime.trap("Sign in to use this feature");
    };
    openAIKeys.remove(caller);
  };

  public shared ({ caller }) func chat(prompt : Text) : async Text {
    if (caller.isAnonymous()) {
      Runtime.trap("Sign in to use this feature");
    };
    let ?key = openAIKeys.get(caller) else {
      Runtime.trap("Set your OpenAI API key first");
    };
    await* OpenAI.runChatCompletion(OpenAI.configForKey(key), prompt);
  };
};
```

```motoko filepath=src/backend/lib/openai.mo
import { defaultConfig; type Config } "mo:openai-client/Config";
import ChatApi "mo:openai-client/Apis/ChatApi";
import CreateChatCompletionRequest "mo:openai-client/Models/CreateChatCompletionRequest";
import ChatCompletionRequestUserMessage "mo:openai-client/Models/ChatCompletionRequestUserMessage";
import Runtime "mo:core/Runtime";

module {
  // Build a Config bound to a single bearer. `is_replicated = ?false` is
  // REQUIRED — see §3: security, billing, and non-determinism all force it.
  // 0.3.0 also defaults it in `defaultConfig`; restating it here is deliberate.
  public func configForKey(key : Text) : Config {
    {
      defaultConfig with
      auth = ?#bearer key;
      is_replicated = ?false;
    };
  };

  public func runChatCompletion(config : Config, prompt : Text) : async* Text {
    let userMessage = ChatCompletionRequestUserMessage.JSON.init({
      content = #string(prompt);
      role = #user;
    });

    // `JSON.init` defaults every optional to `null` — DO NOT hand-list them.
    // Layer optionals with record-update syntax:
    //   { CreateChatCompletionRequest.JSON.init {...} with temperature = ?0.7 }
    let req = CreateChatCompletionRequest.JSON.init({
      messages = [#user(userMessage)];
      model = "gpt-4o-mini"; // ModelIdsShared = Text — any OpenAI model id
    });

    let resp = await* ChatApi.createChatCompletion(config, req);

    if (resp.choices.size() == 0) {
      Runtime.trap("OpenAI returned no choices");
    };
    resp.choices[0].message.content
      ?? Runtime.trap("OpenAI returned no text content (refusal or tool call)");
  };
};
```

### Per-user-specific invariants

- **Key the map by `caller`, never by user-supplied id.** A `Text` userId from the frontend can be spoofed; `Principal` from `shared ({ caller })` cannot.
- **No endpoint ever returns the key — not another user's, not even the caller's own.** The frontend learns "configured? yes/no" from `isMyOpenAIConfigured : async Bool` and nothing more. Concretely: do not generate `getMyOpenAIApiKey`, `getApiKey`, `myApiKey`, or any other shared / query function whose return type is `?Text` / `Text`. Internal reads of the map (inside `chat`, `configFor`, etc.) use `openAIKeys.get(caller)` and never escape the canister boundary. An iterator or a key-returning endpoint leaks every user's bearer.
- **Trap cleanly when the key is missing.** Use `Runtime.trap("Set your OpenAI API key first")` (or return a typed error) — the message identifies whose key is missing without leaking it.
- **Anonymous callers must not store keys.** `caller.isAnonymous()` short-circuits before any `openAIKeys.add` — otherwise everyone reading the canister via `2vxsx-fae` shares one key slot.
- **`stable var` / migration.** The `Map<Principal, Text>` lives in stable memory like any other actor field; on upgrade, decide whether to preserve, rotate, or drop the keys. The default (preserve) is correct for almost all apps. If you ever rotate, drop the whole map — never partially.

## 5. Two call shapes — function form vs. suite form

Every Apis module ships both:

- **Function form** (used in §4 above): `ChatApi.createChatCompletion(config, req) : async* T`. Note the `async*` — call sites use `await*`. This is the common case for `shared` actor methods that thread their own config.
- **Suite form**: `let api = ChatApi(config); api.createChatCompletion(req) : async T`. Note `async`, not `async*`. Useful when a single `shared` method makes several OpenAI calls and you want to bind the config once. Trades one extra `await` boundary for fewer config-threading boilerplate.

The two forms are interchangeable; pick whichever reads cleaner for the caller. Don't mix them inside the same `shared` body.

## 6. Available API surface

What works is **per operation, not per module**: most modules mix working and
broken calls, so read the operation, not the module name. The rule of thumb is
**JSON in, JSON out** — an operation works when its request body is JSON and its
success response is a JSON model.

| Operation | What it does |
| --- | --- |
| `ChatApi.createChatCompletion` | Chat / GPT-4o / GPT-4 / GPT-3.5 — the 95% case. Leave `tool_choice` and `function_call` `null`. |
| `ChatApi.getChatCompletion` / `listChatCompletions` / `getChatCompletionMessages` / `updateChatCompletion` / `deleteChatCompletion` | Stored-completion management. |
| `ImagesApi.createImage` | DALL·E / `gpt-image-1` text-to-image (JSON response: `url` or `b64_json`). |
| `ModelsApi.listModels` / `retrieveModel` / `deleteModel` | Discovery and model management. |
| `FilesApi.listFiles` / `retrieveFile` / `deleteFile` | Files metadata and deletion. |

Nothing in `AudioApi`, `EmbeddingsApi`, `ModerationsApi` or `CompletionsApi`
works, and `FilesApi`/`ImagesApi` work only for the operations listed above.

### Operations that do NOT work — never route a build onto these

The generator stubs its converters for a generic `oneOf` schema (branches mixing
primitives, arrays and arrays-of-arrays don't dispatch through one module), so
`toCandidValue` / `fromCandidValue` are `Runtime.unreachable()`. Those files
typecheck, which is why they ship; the trap fires on the first real request.

Two distinct causes. **Stubbed generic-`oneOf` converters** — `toCandidValue` /
`fromCandidValue` are `Runtime.unreachable()`, so the call traps:

| Operation | Why | Reachable? |
| --- | --- | --- |
| `EmbeddingsApi.createEmbedding` | `input : CreateEmbeddingRequestInput` is **required** | always |
| `ModerationsApi.createModeration` | `input : CreateModerationRequestInput` is **required** | always |
| `CompletionsApi.createCompletion` | `prompt : CreateCompletionRequestPrompt` | whenever `prompt` is set |
| `ChatApi` with `tool_choice` or `function_call` | both are stubbed `oneOf` models | only if you set them — leave them `null` |

**No multipart support** — these take the file as a `Blob` parameter and then
send `body = null` with a JSON content type, so the upload silently arrives
empty. They do not trap; they fail at the API:

| Operation |
| --- |
| `FilesApi.createFile` |
| `ImagesApi.createImageEdit` / `createImageVariation` |
| `AudioApi.createTranscription` / `createTranslation` (also a stubbed response decode) |

**Non-JSON response bodies forced through the JSON decoder** — the success path
is always `Text.decodeUtf8` → `JSON.toCandid` → expect a primitive, which cannot
work when the endpoint returns bytes or raw file content. These throw
`Error.reject` on every call:

| Operation | Response it actually returns |
| --- | --- |
| `AudioApi.createSpeech` | MP3/Opus/AAC audio — not valid UTF-8, let alone JSON |
| `FilesApi.downloadFile` | raw file content (JSONL for fine-tune files), not a JSON string |

Neither failure is a regression: **0.2.5 behaves identically** — same stubs, same
`body = null` — so none of these has ever worked in a published version. What
0.3.0 changes is that this section now says so.

`ChatApi` itself is safe because those two fields are optional and the
serialiser skips `null` (§4 leaves them out). If a spec needs embeddings,
moderation, legacy completions, speech-to-text, or tool-calling, **say it is not
available in 0.3.0** and raise it on
[`caffeinelabs/skills-internal`](https://github.com/caffeinelabs/skills-internal).
Do not substitute hand-rolled `ic.http_request`, and do not "work around" the
trap — there is no workaround at the call site.

Imports follow the pattern:

```mo:openai-client
import ChatApi "mo:openai-client/Apis/ChatApi";
import { defaultConfig } "mo:openai-client/Config";
import CreateChatCompletionRequest "mo:openai-client/Models/CreateChatCompletionRequest";
```

**Not shipped** by `openai-client@0.3.0`: Assistants, Realtime, Responses, Batch, Audit Logs, Evals, FineTuning, Invites, Projects, Uploads, Usage, Users, VectorStores. If a build spec needs one of these, raise an issue on [`caffeinelabs/skills-internal`](https://github.com/caffeinelabs/skills-internal) — do not paper over it with hand-rolled `ic.http_request`.

## 7. Cycles and response sizes

`defaultConfig.cycles = 30_000_000_000` — about 0.04 USD at 4 USD/T cycles. Sufficient for a typical chat completion. Bump for:

- Long completions (`max_completion_tokens > 2000`): set `cycles = 100_000_000_000`.
- Image generation: responses can exceed 1 MiB, set `max_response_bytes = ?2_000_000` and `cycles = 100_000_000_000`.

## 8. Things that will bite you

- **`is_replicated = ?false`** — see §3. This is not optional.
- **Don't expose the API key.** Never return it from any `query` / `shared` method, never log it, never put it in any data structure that has a non-key-owner reader. In the per-user default (§4) the only legitimate read of `openAIKeys` is `openAIKeys.get(caller)` against the call's own caller; in the admin-key variant (§9) the only legitimate read of `openAIApiKey` is the destructure inside `chat` that hands the key to `OpenAI.configForKey`. No iterators, no debug prints, no admin-list endpoints.
- **No `getApiKey` / `getMyOpenAIApiKey` endpoint, ever — not even returning the caller's own key.** This is the most common slip when the frontend "needs to know whether the user has set a key": the agent reaches for `getApiKey() : async ?Text`, returns the bearer to the React app, and a single `console.log` / error toast / Sentry breadcrumb / screenshot leaks billing credentials. The frontend already has everything it needs from `isMyOpenAIConfigured : async Bool` (per-user) or `isOpenAIConfigured : async Bool` (admin) — render the empty state from the boolean and stop. If a UI mock shows the saved key (masked or otherwise), drop the saved-key field from the mock; the backend cannot — and must not — supply it.
- **Don't hand-list every optional null.** Use `CreateChatCompletionRequest.JSON.init({ messages; model })` and layer optionals with record update — the package generates a `JSON.init` helper for every multi-optional model. (This differs from `x-client@0.1.2`, which lacks `JSON.init` and forces the all-`null` value-site listing. Don't reflexively copy that pattern across.)
- **Don't roll your own JSON.** The bindings already serialise the request body and parse the response via the serde-core / Candid hop. If you need a field the bindings don't expose, file an issue on `skills-internal` rather than parse-by-hand — Motoko's JSON support is too thin to make that reliable.
- **Streaming is unsupported.** `stream = ?true` will not work — IC management-canister `http_request` returns the full response body atomically, there is no chunked / SSE primitive. Leave `stream = null`.
- **Rate limits.** OpenAI rate-limits per-key per-minute (RPM) and per-day (RPD). Replicated outcalls would multiply RPM by the subnet size — yet another reason for `is_replicated = ?false`. Back off on HTTP 429.
- **`resp.choices[0].message.content` is `?Text`, not `Text`.** A refusal, a tool call, or an audio-only response leaves it `null`. Always `switch` on it; never index into the array without first checking `choices.size() > 0`.
- **`ChatCompletionRequestUserMessageContent` is a variant** — `#string(text)` for plain text, `#array([...])` for multimodal (text + image_url parts). Use `#string` for the common case.
- **`ModelIdsShared = Text`** — it's a flat string alias, not a variant. Pass `"gpt-4o-mini"` etc. directly.
- **Frontend never holds the key.** The React app calls the backend `chat(prompt)` (or whatever the chat endpoint is named) and gets the answer back. The settings UI calls `setMyOpenAIApiKey(key)` (per-user default) or `setOpenAIApiKey(key)` (admin-key variant). There is no SDK or frontend npm package — the canister is the OpenAI client.

## 9. Variant: admin-key

Use this variant **only** when the spec explicitly puts the OpenAI bill on the operator. Concretely:

- A single OpenAI account funds everything (typical SaaS).
- The app offers a free / freemium tier that the operator pays for.
- The app imposes its own per-user quota inside the canister and bills users separately.

In every other case — and especially whenever the spec mentions login, multiple users, or doesn't say who pays — use the per-user default in §4 instead. The admin-key variant is only sensible when "the operator pays" is a deliberate, stated choice.

The single rule that flips relative to §4: a single `?Text` replaces the `Map<Principal, Text>`, and the setter is gated on the `#admin` role from [`extension-authorization`](../extension-authorization/SKILL.md) instead of "any signed-in caller". The actor and mixin file are new; `src/backend/lib/openai.mo` from §4 is reused unchanged. This `main.mo` replaces §4's, and its chain head supplies `AccessControl.initState()` and `{ var value = null }`.

<!-- motoko-check:skip -->
```motoko
import AccessControl "mo:caffeineai-authorization/access-control";
import MixinAuthorization "mo:caffeineai-authorization/MixinAuthorization";
import MixinOpenAIAdminChat "mixins/openai-admin-chat";

actor {
  let accessControlState : AccessControl.AccessControlState;
  include MixinAuthorization(accessControlState, null);

  // Admin-set OpenAI bearer key. Wrapped in `{ var value : ?Text }` so the
  // mixin can mutate it.
  let openAIApiKey : { var value : ?Text };
  include MixinOpenAIAdminChat(accessControlState, openAIApiKey);
};
```

```motoko filepath=src/backend/mixins/openai-admin-chat.mo
import AccessControl "mo:caffeineai-authorization/access-control";
import Runtime "mo:core/Runtime";
import OpenAI "../lib/openai";

// Admin-gated OpenAI key endpoints. Mounted by `main.mo` via `include`.
// Pairs with `MixinAuthorization` to power role checks.
mixin (
  accessControlState : AccessControl.AccessControlState,
  openAIApiKey : { var value : ?Text },
) {
  public query func isOpenAIConfigured() : async Bool {
    openAIApiKey.value != null;
  };

  public shared ({ caller }) func setOpenAIApiKey(key : Text) : async () {
    if (not AccessControl.hasPermission(accessControlState, caller, #admin)) {
      Runtime.trap("Unauthorized: Only admins can set the OpenAI API key");
    };
    openAIApiKey.value := ?key;
  };

  public shared ({ caller }) func chat(prompt : Text) : async Text {
    if (not AccessControl.hasPermission(accessControlState, caller, #user)) {
      Runtime.trap("Unauthorized");
    };
    let ?key = openAIApiKey.value else Runtime.trap("OpenAI is not configured");
    await* OpenAI.runChatCompletion(OpenAI.configForKey(key), prompt);
  };
};
```

### Admin-key-specific invariants

- **Single `?Text` slot (`{ var value : ?Text = null }`), no getter.** The slot is touched only by `setOpenAIApiKey` and `chat` (which threads it through `OpenAI.configForKey`). Never expose a `getOpenAIApiKey` — `isOpenAIConfigured` is the only outward-facing read, and it returns `Bool`.
- **Setter must be `#admin`-gated via `extension-authorization`.** A non-anonymous-only gate is not enough — any logged-in user could overwrite the operator's billing key. This is the variant's whole reason to depend on `extension-authorization`.
- **Trap with `"OpenAI is not configured"` when the key is unset.** That phrasing pairs with `isOpenAIConfigured` so the frontend can render a "Ask your admin to set the OpenAI API key" empty state.
- **Build a fresh `Config` per call.** `chat` reads `openAIApiKey` and passes it through `OpenAI.configForKey(key)` on every invocation; don't cache the `Config` value at the actor level. The bearer is allowed to rotate via `setOpenAIApiKey` mid-lifetime, and a cached `Config` would silently keep the old key.

## 10. Variant: fully anonymous

Use this **only** when the spec explicitly states there is no login at all (single-user demo, intra-team tool, throwaway sandbox). Mechanically identical to §9 — single `?Text` key, no getter, `isOpenAIConfigured` query — but with the auth import / `#admin` gate removed; any visitor may overwrite the key.

Take §9's two files and apply these diffs (the `lib/openai.mo` helper from §4 is reused unchanged):

In `src/backend/main.mo`:

- Drop the imports of `mo:caffeineai-authorization/access-control` and `mo:caffeineai-authorization/MixinAuthorization`.
- Drop `let accessControlState : AccessControl.AccessControlState;` and `include MixinAuthorization(accessControlState, null);` from the actor body (and the `accessControlState` entry from the migration chain head).
- Drop the `accessControlState` argument from the mixin `include`, leaving `include MixinOpenAIAdminChat(openAIApiKey);`.

In `src/backend/mixins/openai-admin-chat.mo`:

- Drop the `AccessControl` import and the `accessControlState` mixin parameter.
- Replace the gated setter:

  ```
  public shared ({ caller }) func setOpenAIApiKey(key : Text) : async () {
    if (not AccessControl.hasPermission(accessControlState, caller, #admin)) {
      Runtime.trap("Unauthorized: Only admins can set the OpenAI API key");
    };
    openAIApiKey.value := ?key;
  };
  ```

  with the unauthenticated form:

  ```
  public func setOpenAIApiKey(key : Text) : async () {
    openAIApiKey.value := ?key;
  };
  ```

- Drop the `#user` permission check at the top of `chat`. `chat`, `isOpenAIConfigured`, and the `OpenAI.configForKey(...)` call are otherwise identical to §9.

### Anonymous-specific invariants

- **No `extension-authorization` import.** This variant skips it entirely.
- **The key is shared and replaceable by anyone.** That is the explicit trade-off of the variant; pick it only when the spec accepts that.
- **Same no-getter / no-log rules apply.** `openAIApiKey` is read only inside `chat` (then passed to `OpenAI.configForKey`), never returned by any endpoint.
- **Build a fresh `Config` per call** — same reasoning as §9.

# Frontend

Surfaces every build that uses this skill must ship:

1. **A settings UI to paste the key — always.** Every variant. The deployed canister rejects every chat call until a key is pasted. Without a settings page the chatbot UI loads but every question traps with "OpenAI is not configured" / "Set your OpenAI API key first" — the app looks broken to the end user.
2. **A login flow — for the per-user and admin-key variants only.** Those variants gate every meaningful endpoint on `not caller.isAnonymous()` (per-user) or on the `#admin` role (admin-key); both require a non-anonymous caller. The login flow itself is provided by [`extension-authorization`](../extension-authorization/SKILL.md): `useInternetIdentity`, the login/logout buttons, the `useActor` plumbing that injects the authenticated identity into every backend call. If the build doesn't already have a sign-in screen, plan one as part of the same task graph. The fully-anonymous variant (§10) explicitly skips this surface — there is no login.

Pick the UI shape that matches the backend variant. **Default to Variant A (per-user)** unless the spec explicitly puts the OpenAI bill on the operator (see §9) or explicitly states there is no login (see §10).

## Variant A: per-user keys (matches §4 — default)

A per-user "your API key" pane, gated only by login.

1. Password-input bound to `setMyOpenAIApiKey(key)`. Submit on enter; clear the input on success.
2. Status indicator driven by `isMyOpenAIConfigured()` (returns `Bool`). Show "Configured" / "Not configured" — never display the key itself, never expose a getter that returns it.
3. Optional "Clear my key" button bound to `clearMyOpenAIApiKey()` for users who want to revoke their key from the canister.
4. Show a one-time onboarding nudge when `isMyOpenAIConfigured()` is `false` — e.g. inline empty-state on the chat page that links to `/settings/openai`. Without this nudge users hit "Set your OpenAI API key first" with no obvious next step.

Suggested route layout:

```
/                   →  Chat UI (any signed-in user; empty-state when no key)
/settings/openai    →  Personal API-key pane (any signed-in user)
```

## Variant B: admin-key (matches §9)

A single global settings page, admin-gated.

1. Password-input bound to `setOpenAIApiKey(key)`. Submit on enter; clear the input on success.
2. Status indicator driven by `isOpenAIConfigured()` (returns `Bool`). Same no-display invariant as Variant A.
3. Hide the page from non-admins via [`extension-authorization`](../extension-authorization/SKILL.md)'s `isCallerAdmin` query — non-admins should not see the settings link in the nav, let alone the page. Bind admin-only routes through your router's guard pattern (TanStack Router `beforeLoad`, React Router `loader`, etc.); don't rely solely on hiding the link.
4. Show a "Ask your admin to set the OpenAI API key" empty state on the chat page when `isOpenAIConfigured()` is `false` — non-admins can't fix it themselves and need to know who can.

Suggested route layout:

```
/                   →  Chat UI (any signed-in user)
/settings/openai    →  Admin-only API-key settings page
```

## Variant C: fully anonymous (matches §10)

A single global settings page reachable to any visitor — no auth gate.

1. Password-input bound to `setOpenAIApiKey(key)`. Submit on enter; clear the input on success.
2. Status indicator driven by `isOpenAIConfigured()` (returns `Bool`). Same no-display invariant as variants A and B.
3. No router guards, no `useInternetIdentity`, no login buttons — this variant has no auth model.
4. Show a "Paste an OpenAI API key to get started" empty state on the chat page when `isOpenAIConfigured()` is `false`.

Suggested route layout:

```
/                   →  Chat UI (any visitor; empty-state when no key)
/settings/openai    →  API-key pane (any visitor)
```

## Common to all variants

- The chat UI itself is trivial and identical across variants: a textarea, a submit button, a list of messages bound to the backend's chat endpoint. No client-side OpenAI SDK, no key handling, no streaming-protocol logic — the canister mediates everything.
- **Sign-in is required for variants A and B, skipped for variant C.** For A and B, wire the chat and settings routes through `extension-authorization`'s auth guard (`useInternetIdentity` + a redirect when `!isAuthenticated`); anonymous callers must hit a "please sign in" wall before the chat or settings UI renders, otherwise every backend call traps. For C, no guard is needed because there is no auth model.
- The frontend never persists the key in localStorage / IndexedDB / cookies. It travels into the canister via the typed setter and is never read back.

## Related

- [`mops add openai-client@0.3.0`](https://mops.one/openai-client) — connector source.
- [`caffeinelabs/skills-internal`](https://github.com/caffeinelabs/skills-internal) — home of the generated bindings (`packages/connectors/openai`); file issues here for missing or trapping API surface. The standalone `caffeinelabs/openai-client` repo is retired.
- [OpenAI API reference](https://platform.openai.com/docs/api-reference) — upstream.
- [OpenAI API keys page](https://platform.openai.com/api-keys) — where the admin gets the `sk-...` to paste.
- [extension-authorization](../extension-authorization/SKILL.md) — **required prerequisite for the per-user (§4) and admin-key (§9) variants; skipped for fully-anonymous (§10).** Provides the Internet Identity login flow, the `useInternetIdentity` / `useActor` frontend plumbing, and (for §9 admin-key) the `#admin` role gate.
- [extension-http-outcalls](../extension-http-outcalls/SKILL.md) — sibling skill for general HTTP outcalls; you do **not** need it on top of `openai-client`, which makes its own outcalls internally.
