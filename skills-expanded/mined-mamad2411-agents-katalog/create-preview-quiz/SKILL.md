---
name: create-preview-quiz
description: Create a shareable RooQuiz preview assessment — a quiz, scorecard, or personality/outcome test — and get a link to open in the browser. No account, login, or API key required. Use this when someone wants to quickly build, try out, or share a quiz, assessment, test, personality quiz, or scored questionnaire and needs a working preview link.
---

# Create a RooQuiz Preview Assessment

POST an assessment as JSON to RooQuiz's open preview endpoint and instantly get a **short-lived (~1 hour)**, **browser-openable** preview link. The creation endpoint is public (`access.create => true`), so this needs **no account, login, API key, or credentials** — anything that can make an HTTP request can use it.

Use it when someone wants to quickly build, try, or share a quiz / assessment / personality test / scored questionnaire. It produces a **temporary preview**, not a permanently published form — the link expires automatically (recreate the assessment in RooQuiz if you need to keep it).

## Three steps

1. **Build the assessment JSON** (structure below; pick the template for your `scene`).
2. **Create it:** `POST {PREVIEW_BASE}/api/preview-forms` with the JSON as the body and header `Content-Type: application/json`. Returns `{ doc: { publicToken, expiresAt }, message }`.
3. **Hand back the link:** `{QUIZ_BASE}/b/{publicToken}` (append `?secret={secret}` only if you set a `secret` when creating).

### Endpoints

| | Default (RooQuiz cloud) | Override env var |
| --- | --- | --- |
| `PREVIEW_BASE` (create) | `https://preview.rooquiz.com` | `ROOQUIZ_PREVIEW_BASE` |
| `QUIZ_BASE` (open preview) | `https://quizster.app` | `ROOQUIZ_QUIZ_BASE` |

Override the env vars only when targeting a self-hosted RooQuiz deployment; otherwise the defaults work as-is.

### Create it

Send one HTTP request. There is no auth — `Content-Type: application/json` is the only required header. Use whatever HTTP client your environment has (an agent's built-in fetch/HTTP tool, `curl`, `requests`, `fetch`, Postman, …):

```http
POST https://preview.rooquiz.com/api/preview-forms
Content-Type: application/json

<the assessment JSON as the raw request body>
```

For example, with `curl` (write the JSON to a file first, or inline it with `--data`):

```bash
curl -sS -X POST https://preview.rooquiz.com/api/preview-forms \
  -H 'Content-Type: application/json' \
  --data-binary @/tmp/preview-form.json
```

The response is JSON shaped like:

```json
{ "doc": { "publicToken": "7k3m9q2p", "expiresAt": "2026-06-16T09:12:00.000Z" }, "message": "..." }
```

Read `doc.publicToken` and build the preview link to hand the user:

```
https://quizster.app/b/<publicToken>
```

If you set a `secret` in the JSON, append `?secret=<secret>` to that link. For a self-hosted RooQuiz, swap the two hosts for your deployment's preview-API and quiz hosts (see the endpoints table above).

## Assessment JSON — top level

```jsonc
{
  "scene": "quiz",                 // required; see "The three scenes". Sets allowed question types and scoring. Cannot change after creation.
  "title": "My Quiz",              // required
  "description": "Optional intro",
  "language": "en_US",             // form language; default zh_CN. See "language values".
  "personalized": {                // appearance; omit to use defaults (list layout, light theme)
    "key": "default",
    "theme": { "name": "light" },
    "layout": "card"               // "list" | "card"
  },
  "indexDisplayMode": "number",    // question numbering: none (default) | number | uppercase | roman
  "fields": [ /* questions — see "Question types" and "Scoring" */ ],
  "report": { /* results page — see "Report configuration" */ },
  "rules": [],                     // conditional-display rules (scorecard only); usually []
  "secret": "optional; if set, the preview link must include ?secret="
}
```

Key points:
- Every question needs a **unique `code`** (string); option `code`s must be unique within their question.
- `name` is the question text; `description` is optional helper text.
- Unknown top-level fields are silently ignored by the server (no error).
- **`secret`**: omit it for a clean link that works with just the token (tokens are random 8-char and expire in ~1 hour — fine for previews). Set it to make the token unguessable, at the cost of requiring `?secret=` on the link. Default: omit.

## The three scenes

| scene | What it is | Allowed question types | Scoring / outcome |
| --- | --- | --- | --- |
| `quiz` | Right/wrong quiz (correct answers earn points) | choice & input types, **no** `Rate` | each question gets `correctAnswer` + `exactScoring`; total = sum of earned points |
| `scorecard` | Scored questionnaire (each option adds points) | choice & input types, **no** `FillBlank`/`Ordering`; `Rate` allowed | choice questions use `partialScoring` to give each option a value; `report` uses a `formula` to total and `levels` to bucket |
| `outcome` | Personality/type test (options vote for result types) | `SingleCheck` / `MultiCheck` / `DropDown` / `TrueFalse` + `Breaker` / `Statement` / `Swiper` | each question uses `outcomeScoring` (option → which result it votes for); most-voted wins; **no** `correctAnswer`/`exactScoring`/`partialScoring` allowed |

The server validates against the scene's rules and returns HTTP 400 with a specific `path` + `message` on any mismatch. Pick the scene matching your assessment: `quiz`, `scorecard`, or `outcome`.

## Question types

Each field is `{ type, code, name, ... }`. Common types:

- **Choice** (carry `choices: [{ code, value }]`, where `value` is the option label):
  `SingleCheck` (single), `MultiCheck` (multiple; optional `min`/`max`), `DropDown`, `Cascade`, `Ordering` (quiz only), `TrueFalse` (no choices)
- **Input**: `FillBlank` (quiz only; optional `multiline`), `NumberField`, `DateField` (needs `precision`), `TimeField`, `Rate` (scorecard only; needs `steps`)
- **Display only** (never scored, allowed in any scene): `Statement` (`content`), `Breaker` (page break / divider), `Swiper` (image carousel, `items`)

Optional shared props: `required`, `description`, `explain`, `hidden`, `activeColor` (`primary`/`secondary`/`accent`/`neutral`), `layout` (`list`/`grid`).

## Scoring

**`correctAnswer` value depends on the question type:** single choice = the correct option's `code` (string); multiple/ordering = array of `code`s; fill-in = string; true/false = boolean.

- **quiz:** add `correctAnswer` + `exactScoring: { mode: "exactMatch", score: 10 }` to each scored question.
  - Optional partial credit: `exactScoring.accuracy` + `extraLevels`, or `partialScoring` on choice questions (using `partialScoring` requires `exactScoring` too).
- **scorecard:** give each option a value with `partialScoring: [{ value: optionCode, score: N }, ...]` (do **not** set `correctAnswer`).
- **outcome:** map each option to the result(s) it votes for with `outcomeScoring: [{ value: optionCode, outcomes: [{ code: resultCode }] }, ...]`. Each `value` must be one of that question's `choice.code`s, and each `outcomes[].code` must exist in `report.outcomeAnalysis.outcomes`.

## Report configuration

`report` configures the results page. `report.overallAnalysis` is **required** (even for `outcome` — give it at least a `title`).

```jsonc
"report": {
  "overallAnalysis": {
    "title": "Your Result",
    "formula": "q1 + q2",          // scorecard only: total score from question codes via + - * / ( ). Quiz auto-sums — omit it.
    "summaryTemplate": "<p><art-field data-type=\"fieldVariable\" data-cid=\"score\"></art-field> pts · <art-field data-type=\"fieldVariable\" data-cid=\"level\"></art-field></p>",
    "levels": [                    // map score → level (see strict rules below)
      { "minScore": null, "maxScore": 10, "label": "Beginner" },
      { "minScore": 10, "maxScore": 20, "label": "Intermediate" },
      { "minScore": 20, "maxScore": null, "label": "Expert", "description": "Top tier!" }
    ]
  },
  "outcomeAnalysis": { /* outcome scene only — see the outcome example */ }
}
```

**Strict `levels` rules** (violations return HTTP 400): the first level's `minScore` must be `null` (−∞); the last level's `maxScore` must be `null` (+∞); middle levels have finite numbers on both ends; for adjacent levels `current.minScore === previous.maxScore`; `maxScore` strictly increases down the array. A single level has `null` on both ends.

Levels may carry a `cta` (results-page button): `{ enabled, type: "link", text, url, newWindow }`. When enabled, `text` and `url` are required, and `url` must be an `http`/`https` link. `summaryTemplate` defaults to a built-in template if omitted.

## Complete examples

### quiz (right/wrong)

```json
{
  "scene": "quiz",
  "title": "World Capitals Quiz",
  "language": "en_US",
  "personalized": { "key": "default", "theme": { "name": "light" }, "layout": "card" },
  "indexDisplayMode": "number",
  "fields": [
    {
      "type": "SingleCheck", "code": "q1", "name": "Capital of France?", "required": true,
      "choices": [
        { "code": "a", "value": "Berlin" },
        { "code": "b", "value": "Paris" },
        { "code": "c", "value": "Rome" }
      ],
      "correctAnswer": "b",
      "exactScoring": { "mode": "exactMatch", "score": 10 }
    },
    {
      "type": "MultiCheck", "code": "q2", "name": "Which are in Asia?", "required": true,
      "choices": [
        { "code": "a", "value": "Japan" },
        { "code": "b", "value": "Brazil" },
        { "code": "c", "value": "Thailand" }
      ],
      "correctAnswer": ["a", "c"],
      "exactScoring": { "mode": "exactMatch", "score": 10 }
    }
  ],
  "report": {
    "overallAnalysis": {
      "title": "Your Score",
      "summaryTemplate": "<p><art-field data-type=\"fieldVariable\" data-cid=\"score\"></art-field> pts · <art-field data-type=\"fieldVariable\" data-cid=\"level\"></art-field></p>",
      "levels": [
        { "minScore": null, "maxScore": 10, "label": "Novice" },
        { "minScore": 10, "maxScore": 20, "label": "Good" },
        { "minScore": 20, "maxScore": null, "label": "Perfect" }
      ]
    }
  }
}
```

### scorecard (scored questionnaire)

```json
{
  "scene": "scorecard",
  "title": "Healthy Habits Score",
  "language": "en_US",
  "personalized": { "key": "default", "theme": { "name": "light" }, "layout": "card" },
  "fields": [
    {
      "type": "SingleCheck", "code": "q1", "name": "How often do you exercise?",
      "choices": [
        { "code": "never", "value": "Never" },
        { "code": "some", "value": "Sometimes" },
        { "code": "daily", "value": "Daily" }
      ],
      "partialScoring": [
        { "value": "never", "score": 0 },
        { "value": "some", "score": 5 },
        { "value": "daily", "score": 10 }
      ]
    },
    {
      "type": "SingleCheck", "code": "q2", "name": "Hours of sleep per night?",
      "choices": [
        { "code": "low", "value": "Under 6" },
        { "code": "ok", "value": "6-8" },
        { "code": "great", "value": "8+" }
      ],
      "partialScoring": [
        { "value": "low", "score": 0 },
        { "value": "ok", "score": 5 },
        { "value": "great", "score": 10 }
      ]
    }
  ],
  "report": {
    "overallAnalysis": {
      "title": "Your Wellness Score",
      "formula": "q1 + q2",
      "levels": [
        { "minScore": null, "maxScore": 10, "label": "Needs Work", "color": "#e57373" },
        { "minScore": 10, "maxScore": null, "label": "Healthy", "color": "#4caf50" }
      ]
    }
  }
}
```

### outcome (personality / type test)

```json
{
  "scene": "outcome",
  "title": "What's Your Travel Style?",
  "language": "en_US",
  "personalized": { "key": "default", "theme": { "name": "light" }, "layout": "card" },
  "fields": [
    {
      "type": "SingleCheck", "code": "q1", "name": "Ideal weekend?",
      "choices": [
        { "code": "a", "value": "Hiking a new trail" },
        { "code": "b", "value": "Cozy at home" }
      ],
      "outcomeScoring": [
        { "value": "a", "outcomes": [{ "code": "explorer" }] },
        { "value": "b", "outcomes": [{ "code": "homebody" }] }
      ]
    },
    {
      "type": "SingleCheck", "code": "q2", "name": "Pick a vacation:",
      "choices": [
        { "code": "a", "value": "Backpacking abroad" },
        { "code": "b", "value": "A quiet cabin" }
      ],
      "outcomeScoring": [
        { "value": "a", "outcomes": [{ "code": "explorer" }] },
        { "value": "b", "outcomes": [{ "code": "homebody" }] }
      ]
    }
  ],
  "report": {
    "overallAnalysis": { "title": "Your Result" },
    "outcomeAnalysis": {
      "source": "votes",
      "outcomes": [
        { "code": "explorer", "name": "The Explorer", "color": "#ff9800", "description": "You crave adventure and new horizons!" },
        { "code": "homebody", "name": "The Homebody", "color": "#4caf50", "description": "You treasure comfort and calm." }
      ]
    }
  }
}
```

## Notes & limits

- **Expiry:** previews self-destruct after about **1 hour** (`expiresAt`); the link 404s afterward. Recreate the assessment in RooQuiz to keep it permanently.
- **Rate limit:** anonymous creation is capped at about **10 previews per hour** per IP.
- **Validation errors:** a 400 response includes `errors[].path` and `message` — fix the JSON and retry. Most common: a question type or scoring style that doesn't match the `scene`, non-contiguous `levels`, or an `outcomeScoring` referencing a result `code` that isn't defined.
- **Results page looks empty?** This is a preview (no submission backend); results are computed in the browser from the returned questions + `report`. Make sure `report.overallAnalysis` exists and scored questions carry the right scoring fields.
- **`language` values:** `en_US` `de_DE` `es` `pt_BR` `fr` `zh_CN` (default) `zh_TW` `ja_JP` `ko_KR`.
