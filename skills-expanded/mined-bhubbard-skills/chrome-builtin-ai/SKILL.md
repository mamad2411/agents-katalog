---
name: chrome-builtin-ai
description: Reference for Chrome's built-in AI APIs (Prompt API / LanguageModel, Summarizer, Translator, Language Detector, Writer, Rewriter, Proofreader) that run Gemini Nano and expert models locally in the browser, plus their JS polyfills for unsupported browsers. Use whenever the user is writing web app or Chrome Extension code that needs on-device AI in JavaScript — summarizing page content, translating text, detecting language, drafting or rewriting text, proofreading, or free-form LLM prompting — without calling a cloud API or shipping their own model. Trigger on mentions of "built-in AI", "Gemini Nano", `LanguageModel`, `Summarizer`, `Translator`, `LanguageDetector`, `Writer`, `Rewriter`, `Proofreader`, Chrome AI origin trials, or requests to add client-side/on-device AI to a website or extension. Also trigger for feature-detection, model-download, or availability() questions on these APIs, and for polyfill/fallback questions when they aren't supported in a browser.
---

# Chrome built-in AI APIs

Chrome ships Gemini Nano (and a couple of smaller expert models) directly in the browser. These APIs let a web page or extension run AI tasks entirely on the user's device: no server round-trip, no API key, no per-token cost, and no user data leaving the machine except for the one-time model download. Reach for this skill whenever the task is "add AI to a web page/extension using what Chrome already ships" rather than calling OpenAI/Anthropic/Gemini's cloud APIs.

There are seven task-specific APIs plus the general-purpose Prompt API, all built on the same lifecycle pattern. Learn that pattern once, then check the reference file for the specific API.

## The APIs at a glance

| API | Global | Model type | Modality | Status (as of these docs) |
|---|---|---|---|---|
| Prompt API | `LanguageModel` | Gemini Nano (general) | multimodal in (text/image/audio), text out | Shipped Chrome 138, sampling params in origin trial |
| Summarizer | `Summarizer` | Gemini Nano | text-to-text | Stable Chrome 138 |
| Translator | `Translator` | expert translation model | text-to-text | Stable Chrome 138, desktop only |
| Language Detector | `LanguageDetector` | expert model | text-to-text | Stable Chrome 138, desktop only |
| Writer | `Writer` | Gemini Nano | text-to-text | Origin/developer trial |
| Rewriter | `Rewriter` | Gemini Nano | text-to-text | Origin/developer trial |
| Proofreader | `Proofreader` | Gemini Nano | text-to-text | Developer trial |

Full per-API detail lives in `references/`: `prompt-api.md` (LanguageModel — sessions, multimodal, structured output), `content-apis.md` (Summarizer, Writer, Rewriter, Proofreader — the four text-transform APIs, which share a create/generate shape), `translator-language-detector.md` (the two expert-model APIs), and `polyfills.md` (fallbacks for unsupported browsers/platforms). Read the relevant one before writing code against a specific API — don't guess method names from memory, since these are new, fast-moving APIs with easy-to-confuse option names (e.g. Writer's `tone` values differ from Rewriter's).

## Hardware and platform requirements

Get this right before debugging "why doesn't this work" — most failures are requirement mismatches, not code bugs.

**Translator and Language Detector**: Chrome on desktop only (Windows/macOS/Linux/ChromeOS). No mobile support at all.

**Prompt API, Summarizer, Writer, Rewriter, Proofreader** (the Gemini-Nano-backed APIs) additionally need:
- OS: Windows 10/11, macOS 13+ (Ventura+), Linux, or ChromeOS 16389.0.0+ on a Chromebook Plus device. Chrome for Android/iOS and non-Chromebook-Plus ChromeOS are **not** supported.
- Storage: at least 22 GB free on the volume holding the Chrome profile (the model itself is much smaller; this is Chrome's safety margin). If free space drops below 10 GB after download, Chrome deletes the model and re-downloads it once space is available again.
- GPU strictly >4 GB VRAM, **or** CPU with 16 GB+ RAM and 4+ cores. Audio input to the Prompt API specifically requires a GPU.
- An unmetered network connection for the initial model download only — nothing after that touches the network.

If a user's setup doesn't meet these, the right answer is a polyfill (`references/polyfills.md`), not "fix the code."

## The lifecycle every one of these APIs shares

Every API (`LanguageModel`, `Summarizer`, `Translator`, `LanguageDetector`, `Writer`, `Rewriter`, `Proofreader`) follows the same four-step shape. Learn it once:

**1. Feature-detect.** Check the global exists before touching it — these are new APIs, always guard:
```js
if ('Summarizer' in self) { /* supported */ }
```

**2. Check availability.** Call the static, asynchronous `availability()` function (pass the *same options* you'll later pass to `create()` — some combinations of language/modality may not be supported even when the API generally is):
```js
const availability = await Summarizer.availability();
// 'unavailable' | 'downloadable' | 'downloading' | 'available'
```

**3. Respect user activation, then create.** If the model needs downloading, `create()` must be called from inside a real user interaction (click, keypress, etc.) — check `navigator.userActivation.isActive` first. Pass a `monitor` callback to `create()` to surface download progress; the download can take a while the first time any site uses any of these APIs (the model is shared across the whole browser after that).
```js
if (navigator.userActivation.isActive) {
  const summarizer = await Summarizer.create({
    monitor(m) {
      m.addEventListener('downloadprogress', (e) => {
        console.log(`Downloaded ${e.loaded * 100}%`);
      });
    },
  });
}
```

**4. Use it, then let it go.** Most APIs offer a request-based method (waits for the full result) and a streaming variant (`*Streaming()`, returns a `ReadableStream`) — prefer streaming for anything longer than a sentence or two so the UI isn't stuck waiting. Session-style objects (Prompt API, and reusable Writer/Rewriter instances) support `destroy()` to free resources and an `AbortSignal` to cancel in-flight work.

This lifecycle is identical enough across APIs that you can copy-paste the shape and just swap the class name and method — but the **options objects differ per API** (see the reference files), and once an object is created its options are frozen: make a new one if you need different settings.

## TypeScript

Install `@types/dom-chromium-ai` from npm for typings across all of these APIs — mentioned repeatedly in Chrome's own docs as the recommended way to get IDE support.

## Permission Policy, iframes, and Web Workers

All of these APIs share the same cross-origin story: available by default only to top-level windows and same-origin iframes. To delegate to a cross-origin iframe, the host page adds an `allow="..."` attribute naming the specific API's policy token (e.g. `allow="summarizer"`, `allow="translator"`, `allow="language-model"`, `allow="writer"`, `allow="rewriter"`, `allow="language-detector"`, `allow="proofreader"`):
```html
<iframe src="https://cross-origin.example.com/" allow="summarizer"></iframe>
```
None of these APIs are available inside Web Workers — Chrome cites the complexity of establishing a responsible document per worker to check Permissions Policy.

## Testing on localhost

All APIs are testable on `localhost` via Chrome flags, without an origin trial token:
1. Go to `chrome://flags/#optimization-guide-on-device-model`, set **Enabled**.
2. For Prompt-API-backed features, also set `chrome://flags/#prompt-api-for-gemini-nano` to **Enabled** (or **Enabled multilingual**). Individual newer APIs (Writer/Rewriter/Proofreader) have their own additional flags — check that API's reference section if `chrome://flags` doesn't show what you expect.
3. Relaunch Chrome.
4. Verify in DevTools console: `await LanguageModel.availability()` should return `"available"` (or `"downloadable"`, then wait/retry). If flags are missing, update Chrome. If the model errors, check `chrome://on-device-internals` → **Model Status** tab, restart Chrome, and retry.

For production (real users, not localhost), APIs still in trial require registering for that API's **origin trial** and adding the token to the page or extension manifest — check the specific API's status, since trial windows close and reopen as APIs graduate toward stable.

## Multi-language support

From Chrome 149, the underlying models support English, Spanish, Japanese, German, and French for input/output text (more languages are in development). Every API that accepts language options (`expectedInputLanguages`, `expectedContextLanguages`, `outputLanguage`, or BCP-47 codes for Translator/Language Detector) will reject unsupported combinations — always check `availability()` with the real language options you intend to use, not just a bare call.

## Do this, not that

Building a feature with these APIs almost always benefits from the [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) since every one of them wraps a generative model — treat outputs as probabilistic, not deterministic, and design the UI accordingly (loading states for model download, streaming output, and a way to regenerate). Strip HTML markup before feeding page content to Summarizer/Prompt/Writer/Rewriter (use `element.innerText`, not `innerHTML`) — these are token-budget-constrained models and markup wastes budget. When in doubt about which of Summarizer/Writer/Rewriter/Prompt to reach for: Summarizer condenses existing text, Writer creates new text from an instruction, Rewriter transforms existing text (tone/length/format) without summarizing it, and the Prompt API is the free-form fallback when the task doesn't fit any of the specialized shapes.
