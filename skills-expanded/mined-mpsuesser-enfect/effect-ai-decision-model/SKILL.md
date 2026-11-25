---
name: effect-ai-decision-model
description: Use Effect's Decision and DecisionModel APIs for System One models such as Jev. Covers typed classify/rate/probability/locate definitions, settled outcomes, images, TypeSafe/OpenRouter/OpenAI/Cloudflare providers, errors, and test implementations.
---

# Effect AI Decision Model

Baseline: `effect@4.1.0` and matching `@effect/*` packages. These AI APIs carry
`@stability unstable`; inspect the consuming version's source before using newer
contracts. References below are pinned to the stable tag.

## Define and call

`Decision.make({ input, decisions })` pairs an input schema with a nonempty record
of named decisions. One `DecisionModel.decide(definition, { input })` encodes one
input and sends every decision together in one provider call. Answers retain the
decision keys and inferred label literals. Keep definitions inferred rather than
widening them to `Record<string, Decision.Any>`.

<!-- typecheck -->
```ts
import * as Decision from 'effect/ai/Decision';
import * as DecisionModel from 'effect/ai/DecisionModel';
import * as Effect from 'effect/Effect';
import * as Schema from 'effect/Schema';

class Ticket extends Schema.Class<Ticket>('Ticket')({
  subject: Schema.String,
  body: Schema.String
}) {}

const Triage = Decision.make({
  input: Ticket,
  decisions: {
    department: Decision.classify({
      instructions: 'Which team should handle the ticket?',
      criteria: {
        billing: 'Payments, invoices, and refunds',
        technical: 'Bugs, outages, and integrations',
        other: 'Neither billing nor technical'
      }
    }),
    frustration: Decision.rate({
      instructions: 'How frustrated is the customer?',
      criteria: ['Calm or neutral', 'Expresses frustration', 'Expresses intense anger']
    }),
    urgent: Decision.probability({
      instructions: 'Does the ticket need immediate attention?',
      criteria: { false: 'Can wait', true: 'Needs action now' }
    })
  }
});

type TriageAnswers = Decision.Answers<typeof Triage.decisions>;

const triage = Effect.fn('Ticket.triage')(function* (raw: unknown) {
  const input = yield* Schema.decodeUnknownEffect(Ticket)(raw);
  return yield* DecisionModel.decide(Triage, { input });
});
```

### Constructors and answers

Every constructor takes an options object. `Decision.Description` is
`string | Schema.JsonObject | Schema.JsonArray`; instructions and descriptions
can carry structured context without pre-stringification.

| Constructor | Criteria | Answer |
| --- | --- | --- |
| `Decision.classify` | Record of at least two labels to `Description \| null`; null means no description | `{ label, probabilities, confidence? }`; both label and distribution keys use the inferred label union |
| `Decision.rate` | At least two ordered strings or `{ label, description: Description }` entries, with unique labels | `{ rating, label, probabilities, confidence? }`; keys use labels, not descriptions |
| `Decision.probability` | Optional `{ false: Description, true: Description }`; both required when supplied, neither nullable | `{ probability }`, the probability of true in `[0, 1]` |

`rate` normalizes string entries to `{ label, description }`; stored
`Rate.criteria` is always an array of these objects. Custom adapters must read
each entry's `label` and `description`, not treat it as a string.

- `classify` preserves the provider's chosen label, even if it differs from the
  distribution's maximum. The core checks membership, not argmax consistency.
- `rate.rating` is the provider's probability-weighted zero-based position, in
  `[0, criteria.length - 1]`, potentially fractional. The core range-checks it but
  does not recompute it or check agreement with the distribution. `rate.label` is
  derived from the highest probability, breaking ties by criteria order.
- Classify/rate confidence is optional and provider-defined in `[0, 1]`; preserve
  absence (for example with `Option.fromNullishOr`). Probability answers have
  neither confidence nor a distribution. Public answers have no `_tag` field.
- `classify`, `rate`, and `make` synchronously throw on the cardinality/uniqueness
  violations above. Define valid static literals; parse dynamic definitions at
  their boundary before construction. These throws are outside `decide`'s error
  channel. Treat definitions and their nested inputs as immutable.

Exported types: `Classify<Label>`, `Rate<Level>`, `Probability`, `Locate<Path>`, their union `Any`,
`ClassifyAnswer<Label>`, `RateAnswer<Level>`, `ProbabilityAnswer`, `LocateAnswer`, conditional
`Answer<D>`, mapped `Answers<Decisions>`, and `Definition<Input, Decisions>`.
`Definition` holds `input`, `decisions`, and the `Decision.TypeId` brand.

### Execution and encoding

- Static `DecisionModel.decide` requires `DecisionModel.DecisionModel` plus
  `Input["EncodingServices"]`. Alternatively, `yield* DecisionModel.DecisionModel`
  once and call `model.decide(definition, { input })`; only encoding services then
  remain in that call's requirements.
- `DecideOptions<Input>` contains only `input: Input["Type"]`. Declare images
  inside the input schema with `Decision.Image`, whose decoded value is
  `{ mediaType: string, data: string | Uint8Array | URL }`. Refer to image paths
  in instructions. The removed top-level `images` option is not supported.
  Pass the decoded input, not its encoded representation. Unknown input still needs boundary
  decoding; its `SchemaError` is separate from `decide`'s `AiError`.
- Encoding uses `Schema.encodeEffect(Schema.toCodecJson(definition.input))`.
  Providers receive JSON **values**, not a pre-stringified document. Existing
  schema transformations apply: e.g. `FiniteFromString` sends a number as a string;
  derived codecs can encode nested bigint/date values. Explicit `undefined`
  becomes `null`, while absent fields stay absent. Custom declarations need JSON
  codec annotations or encoding fails before the provider runs.
- `DecideResponse<Decisions>` is `{ answers: Decision.Answers<Decisions>, usage,
  id?, modelId?, metadata }`. `metadata` defaults to `{}` and is keyed by provider;
  `modelId` can differ from the requested alias. Do not assume all adapters report it.
  `usage` is a `DecisionUsage` schema-class instance with optional finite-number
  `inputTokens` / `outputTokens`. Unknown counts are `undefined`, not zero.
  Answer and distribution dictionaries have null prototypes; use record helpers
  rather than methods inherited from `Object.prototype`.
- This is a single-response API with no prompt/history, tools, streaming, model,
  or sampling options on `decide`. Provider configuration belongs in layers or
  scoped provider services. Multiple inputs require separate calls; use bounded
  `Effect.forEach` concurrency. Built-in spans are `DecisionModel.decide` and
  `DecisionModel.decideSettled`.

### Images and target locations

`Decision.locate({ image: 'photo', instructions })` returns
`{ box: { left, top, right, bottom }, confidence? }`, with normalized coordinates
in `[0, 1]`. `Decision.make` checks that the image path names a required image
field. Locate has no not-found result; pair it with a probability question when
target presence is uncertain. Providers must support both images and locate.

<!-- typecheck -->
```ts
import { Decision, DecisionModel } from 'effect/ai';
import { Schema } from 'effect';

const Target = Decision.make({
  input: Schema.Struct({ photo: Decision.Image }),
  decisions: {
    present: Decision.probability({ instructions: 'Is a submit button visible in photo?' }),
    button: Decision.locate({ image: 'photo', instructions: 'Locate the submit button' })
  }
});
const locate = (data: Uint8Array) => DecisionModel.decide(Target, {
  input: { photo: { mediaType: 'image/png', data } }
});
```

### Strict versus settled outcomes

`decide` is all-or-nothing. Any refusal becomes `ContentPolicyError`, taking
precedence over other unanswered decisions. Otherwise the first unanswered
decision in definition order becomes `InvalidOutputError`.

`decideSettled` makes the same single call but returns `{ outcomes, usage, id?,
modelId?, metadata }`. `Decision.Outcomes<Decisions>` maps each key to
`Result<Decision.Answer<D>, Decision.Unanswered>`. An unanswered value has
`{ _tag: 'Unanswered', reason, description }`, where reason is `Missing`,
`Refused`, `NoDistribution`, or `Invalid`. It records the first failed validation
check; `NoDistribution` requires an otherwise valid answer. Input encoding,
transport, provider, and wire-response decoding failures still fail the whole
effect; settled is not a blanket recovery API. Usage covers the entire request.

<!-- typecheck -->
```ts
import * as Decision from 'effect/ai/Decision';
import * as DecisionModel from 'effect/ai/DecisionModel';
import * as Effect from 'effect/Effect';
import * as Option from 'effect/Option';
import * as Result from 'effect/Result';
import * as Schema from 'effect/Schema';

const Review = Decision.make({
  input: Schema.String,
  decisions: {
    severity: Decision.rate({
      instructions: { task: 'Rate severity', context: ['Consider available workarounds'] },
      criteria: [
        'cosmetic',
        { label: 'blocking', description: { impact: 'Cannot complete the workflow' } }
      ]
    }),
    urgent: Decision.probability({ instructions: 'Needs action today' })
  }
});

const review = Effect.fn('Review.run')(function* (input: string) {
  const { outcomes } = yield* DecisionModel.decideSettled(Review, { input });
  return {
    severity: Result.match(outcomes.severity, {
      onFailure: (unanswered) => `review: ${unanswered.reason}`,
      onSuccess: (answer) => answer.label
    }),
    urgency: Result.match(outcomes.urgent, {
      onFailure: () => Option.none<number>(),
      onSuccess: (answer) => Option.some(answer.probability)
    })
  };
});
```

## TypeSafe / Jev provider

Install `@effect/ai-typesafe` at the same release as `effect`; for Bun also install
matching `@effect/platform-bun`. Compose the graph:
HTTP transport → TypeSafe client → decision model.

<!-- typecheck -->
```ts
import * as TypeSafeClient from '@effect/ai-typesafe/TypeSafeClient';
import * as TypeSafeDecisionModel from '@effect/ai-typesafe/TypeSafeDecisionModel';
import * as BunHttpClient from '@effect/platform-bun/BunHttpClient';
import * as Decision from 'effect/ai/Decision';
import * as DecisionModel from 'effect/ai/DecisionModel';
import * as Effect from 'effect/Effect';
import * as Layer from 'effect/Layer';
import * as Schema from 'effect/Schema';

const JevLive = TypeSafeDecisionModel.layer({ model: 'jev-latest' }).pipe(
  Layer.provide(TypeSafeClient.layerConfig()),
  Layer.provide(BunHttpClient.layer)
);

const Urgency = Decision.make({
  input: Schema.String,
  decisions: {
    urgent: Decision.probability({ instructions: 'Does this need action today?' })
  }
});

const program = DecisionModel.decide(Urgency, {
  input: 'My card was charged twice; please fix this today.'
}).pipe(Effect.provide(JevLive));
// Run at the application entrypoint; program has no remaining service requirements.
```

### Provider and client surface

| API | Contract |
| --- | --- |
| `TypeSafeDecisionModel.make({ model })` | `Effect<DecisionModel, never, TypeSafeClient>`; captures the client |
| `TypeSafeDecisionModel.layer({ model })` | `Layer<DecisionModel, never, TypeSafeClient>` |
| `TypeSafeDecisionModel.model(modelId)` | `Model.Model<"typesafe", DecisionModel, TypeSafeClient>`; usable as a layer, adding `Model.ProviderName` and `Model.ModelName` metadata |
| Model IDs | Known union: `jev-latest`, `jev-preview`, `jev-1.14.0`, `jev-1.13.0`; arbitrary strings also accepted. Use client model discovery for current availability |
| `TypeSafeClient.make(options)` / `layer(options)` | Require `HttpClient.HttpClient`; construction error is `never` |
| `TypeSafeClient.layerConfig(options?)` | Same HTTP requirement, construction error `Config.ConfigError`; defaults to `Config.Redacted('TYPESAFE_API_KEY')` |

Client options: optional `apiKey: Redacted<string>`, `apiUrl: string`, and
`transformClient: (HttpClient) => HttpClient`. Default URL:
`https://api.typesafe.ai/v1`. Explicit `make`/`layer` options do not read the
environment. In `layerConfig`, `apiKey` and `apiUrl` are `Config` values;
`transformClient` remains a plain function.

`TypeSafeConfig.withClientTransform(effect, transform)` or
`effect.pipe(TypeSafeConfig.withClientTransform(transform))` scopes HTTP
customization at request execution time, after the constructor transform. Nested
scoped transforms replace rather than compose; compose explicitly when both are
needed. The module also exports the `TypeSafeConfig` service and its
`getOrUndefined` effect. There is no per-call TypeSafe model override; provide a
different decision-model layer.

TypeSafe supports image input and locate questions. Locate requires `jev-preview`
or `jev-1.14.0`. PNG/JPEG images must be 256–1568 pixels per side; remote URLs are
rejected and EXIF orientation is ignored. Assets are keyed by image reference;
locate maps to a Box question. Wire codecs include Box questions/answers and assets.

### Wire mapping and adapter limits

- `classify` → Choice (`choice` → `label`); `rate` → Score (`score` → `rating`,
  index-keyed probabilities → level-string keys); `probability` → Noul (`noul` →
  `probability`). The decision provider drops response `model` and Score `legend`.
  TypeSafe's Choice/Score wire codecs require confidence even though the generic
  decision answer types allow it to be absent. Score legend values are
  `Schema.Json`, not just strings.
- TypeSafe and OpenRouter use `probabilityPrecision: 2` for rounded
  distributions. Core normalization does not recompute the supplied rating or
  confidence.
- TypeSafe and OpenRouter preserve structured instructions/descriptions and send
  rating descriptions in order, remapping index-keyed probabilities to labels.
  TypeSafe's wire `Entry` also permits null; this is broader than core
  `Description`. The old 4.0.0 string-only workaround is no longer needed.
- Core state is `Schema.Json`, but the live TypeSafe endpoint documents top-level
  string/object/array. Wrap scalar boolean/number/null state in a named input field.
  Current HTTP limits (255 Choice options, 10 Score levels) are provider limits,
  not constructor checks; consult the [live API](https://docs.typesafe.ai/api.md)
  when building dynamic definitions.

For model discovery or wire-level access, yield
`TypeSafeClient.TypeSafeClient`: `listModels()` returns `{ models }` (entries have
`name`, optional `description` / `release_date`); `systemOne({ model, state,
questions })` returns decoded `{ model, answers, usage? }`; both fail with
`AiError`. The service also exposes its configured `client`. Low-level calls keep
wire names, discriminated `type` fields, and optional snake-case token counts;
they do not apply `DecisionModel`'s definition-relative validation/normalization.
`TypeSafeSchema` exports Choice/Score/Noul question and answer codecs, `Question`,
`Answer`, `SystemOneRequest`, `SystemOneResponse`, and `ListModelsResponse`.

For **Jev through OpenRouter**, including request overrides and raw metadata,
read [the OpenRouter adapter reference](openrouter.md).

## OpenAI and Cloudflare decision providers

These are decision adapters, not `LanguageModel` layers. Match their package
versions to `effect` and provide their client plus an HTTP transport.

| Adapter | Construction and behavior |
| --- | --- |
| `@effect/ai-openai/OpenAiDecisionModel` | `model(modelId)`, `layer({ model })`, `make({ model })`; requires `OpenAiClient`. Model IDs follow `CreateDecisionsRequest` (the tagged example uses `gpt-6-luna`). Uses two-decimal distribution tolerance. |
| `@effect/ai-cloudflare/CloudflareDecisionModel` | `model(modelId)`, `layer({ model })`, `make({ model })`; requires `CloudflareClient`. Supports Clef/Clef-flash and uses four-decimal distribution tolerance. |

Both accept inline image bytes, base64 strings, or `new URL('data:...')` values,
but reject remote `URL` objects with `InvalidUserInputError`. String data is
treated as base64, so represent an already-complete data URL as a `URL`, not a
string. The common `Image` type does not imply every representation works on
every provider. OpenAI stringifies structured
descriptions for its wire format and appends probability outcome descriptions to
the instruction. Its adapter does not forward response ID/model metadata.
OpenAI refusals become per-decision `Refused` outcomes; use these instead of the
removed `OpenAiContentPolicyMetadata` / `metadata.openai.refusedDecisions`.

`CloudflareClient` supports optional `gatewayId` (in `layerConfig`,
`CLOUDFLARE_AI_GATEWAY_ID`). It sets the `cf-aig-gateway-id` request header;
keep account and API-token configuration in the client layer.

`AiError.NetworkError` records `method` and `url` instead of `request` and may
carry an unredacted `HttpClientError` in `cause`; inspect it deliberately when
logging. Providers use `NetworkError.fromHttpClientError`; `fromRequestError`
remains available. `AiError.HttpRequestDetails`, `Response.HttpRequestDetails`,
and request fields in HTTP context/response metadata were removed.

## Failures

`decide` fails with outer `AiError.AiError` (`_tag: 'AiError'`) containing a tagged
`reason`, `module`, and `method`. Encoding failures use `InvalidUserInputError`;
missing, mismatched, or invalid answers use `InvalidOutputError`. A provider's
`AiError` propagates unchanged. Recover by reason with
`Effect.catchReason('AiError', 'RateLimitError', handler)` or `catchReasons`;
`catchTag('RateLimitError', ...)` targets the wrong level.

TypeSafe's client maps response decoding failures to `InvalidResponseError`, body
encoding failures to `InvalidRequestError`, transport/URL/HTTP encoding failures
to `NetworkError`, 404/422 to `InvalidRequestError`, and 429 to `RateLimitError`.
Other statuses use the shared `AiError.reasonFromHttpStatus` mapping. Rate-limit
reasons preserve optional `retryAfter` as `Duration` (milliseconds header first,
then seconds or HTTP-date) and TypeSafe request/error metadata.

`InvalidResponseError` is nonretryable and means the provider envelope/SSE failed
its schema contract, optionally retaining HTTP context. `InvalidOutputError`
means decoded model output failed validation and remains retryable.

The Effect TypeSafe client has **no automatic retries**. Add a bounded retry
policy at the owned request boundary when appropriate, honoring retry metadata;
native TypeSafe SDK retry defaults do not apply here. See `effect-scheduling` for
policy construction and `effect-error-handling` for reason-based recovery.

## Test implementations and custom providers

`DecisionModel.make({ decide, probabilityPrecision?, supportsImages?, supportsLocate? })` returns
`Effect<DecisionModel>`; provide it with `Layer.effect`. Its provider callback is
`(ProviderOptions) => Effect<ProviderResponse, AiError>` with no remaining service
requirements: acquire dependencies while constructing the layer and close over
them. `ProviderOptions` contains encoded `state: Schema.Json` and all `decisions`.
`ProviderResponse` contains `answers` and a required `usage` object with
`inputTokens` / `outputTokens`, each `number | undefined`. Optional `id`, `modelId`,
and `metadata` pass through; absent metadata becomes `{}`. Set `supportsImages:
true` only if the callback supports nonempty image input; otherwise core rejects
it before invoking the provider. `ProviderOptions.images` is omitted when empty;
otherwise each item is `{ reference, path, image }`, with a `(string | number)[]`
path and base64-string or `URL` image data. Encoded state substitutes references
for image values. Enable `supportsLocate: true` only when the callback handles
locate decisions.

Provider answers use `_tag: 'Classify' | 'Rate' | 'Probability' | 'Locate'` and the public
answer fields above, except a provider Rate answer has **no label**. The core
derives it. `ProviderAnswer` additionally includes `ProviderRefusalAnswer`
(`{ _tag: 'Refusal' }`). Provider classify/rate `probabilities` is optional: omit
it to report an unavailable distribution, not an empty dictionary. `make`
supplies both strict and settled methods; hand-built service implementations
must now implement `decideSettled` too.

<!-- typecheck -->
```ts
import * as Decision from 'effect/ai/Decision';
import * as DecisionModel from 'effect/ai/DecisionModel';
import * as Effect from 'effect/Effect';
import * as Layer from 'effect/Layer';
import * as Schema from 'effect/Schema';

const Urgency = Decision.make({
  input: Schema.String,
  decisions: {
    urgent: Decision.probability({ instructions: 'Does this need action today?' })
  }
});

const UrgencyTest = Layer.effect(
  DecisionModel.DecisionModel,
  DecisionModel.make({
    decide: Effect.fnUntraced(function* (_request) {
      return {
        answers: { urgent: { _tag: 'Probability', probability: 0.9 } },
        usage: { inputTokens: undefined, outputTokens: undefined }
      } satisfies DecisionModel.ProviderResponse;
    })
  })
);

const result = DecisionModel.decide(Urgency, { input: 'Please fix this today.' })
  .pipe(Effect.provide(UrgencyTest));
```

This fixture handles the `Urgency` definition specifically. In an `it.effect`
test, yield `result` and assert `answers.urgent.probability`; inspect the provider
request when testing encoding. Returning incomplete/wrong answers through `make`
exercises real validation rather than bypassing it with a mocked `decide` method.

Validation requires every requested answer with a matching tag, every expected
distribution key with a finite probability in `[0, 1]`, a known classify label,
finite/range-valid ratings and probabilities, and optional finite/range-valid
confidence. Extra answers, probability keys, and answer fields are discarded.
Distributions must have a positive total within `1e-6` of 1 by default. With
`probabilityPrecision: p`, permitted drift is
`labelCount * 0.5 * 10 ** -p + 1e-6`; accepted drift greater than `1e-6` is
normalized. Precision describes provider rounding, not output rounding.

## Pinned source

Resolve these paths under the Effect reference at tag `effect@4.1.0`:

- `packages/effect/src/ai/{Decision,DecisionModel}.ts` — complete core surface.
- `packages/effect/test/ai/DecisionModel.test.ts` and `typetest/ai/DecisionModel.tst.ts`
  — runtime edge cases and inference contracts.
- `packages/ai/typesafe/src/{TypeSafeDecisionModel,TypeSafeClient,TypeSafeConfig,TypeSafeSchema}.ts`
  — adapter, transport, scoped customization, and wire codecs.
- `packages/ai/typesafe/test/` and `typetest/` — adapter contract tests.
- `packages/ai/{openai,cloudflare}/src/*DecisionModel.ts` — image and wire mappings.
- `packages/effect/CHANGELOG.md` — #9124 structured descriptions, #9422 metadata,
  #9437 settled outcomes; inspect the 4.0.7 and 4.1.0 entries and matching provider changelogs.
