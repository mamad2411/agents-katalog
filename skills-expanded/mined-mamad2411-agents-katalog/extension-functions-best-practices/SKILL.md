---
name: extension-functions-best-practices
description: Best practices for implementing browser extension features across 13 categories. Reference this skill when developing video, audio, image, translation, download, userscript, AI (including Chrome built-in AI / Gemini Nano), ad-blocker, theme, email, game, password manager, or Web3 wallet features.
---

# Extension Functions Best Practices

Implementation guidance for browser extension features across 13 categories. Each category includes reference open-source projects and links to detailed implementation guides.

## When to Use

- Building extension features in any supported category
- Looking for proven patterns and reference implementations
- Choosing libraries and APIs for specific functionality
- Understanding permission requirements

## How Reference Projects Are Chosen

- **Verifiable**: Prefer projects you can install from a store, or build into a loadable extension from GitHub, with real Issues/Releases.
- **Behavior-aligned**: Table **Highlights** describe user-visible behavior (e.g. “merge HLS segments”) rather than only “call the downloads API”.
- **Download / streaming**: Tutorial-style `chrome.downloads` + an `m3u8` URL is often **not** enough for a playable file; treat [rules/download.md](rules/download.md) (“Reality check & common pitfalls”) and repos such as **Cat Catch**, **Live Stream Downloader**, and **Video DownloadHelper** as the ground truth.

---

## Feature Categories

### 1. Video
**Common Features**: Enhancement (rotation, speed, zoom), download (media sniffing, M3U8/MPD), screen recording

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Video Roll](https://github.com/VideoRoll/VideoRoll) | Enhancement | Rotation, zoom, filters, VR mode (in-page `<video>` UX) |
| [Cat Catch](https://github.com/xifangczy/cat-catch) | Download | Sniffing, M3U8/MPD parsing, handoff to N_m3u8DL-RE and similar (high activity) |
| [Live Stream Downloader](https://github.com/chandler-stimson/live-stream-downloader) | Download | In-extension HLS detection and multi-threaded merge to disk (store build for comparison) |
| [Video DownloadHelper](https://github.com/aclap-dev/video-downloadhelper) | Download | General sniffing + [vdhcoapp](https://github.com/aclap-dev/vdhcoapp) companion (production-grade OSS core) |
| [HLS Downloader](https://github.com/puemos/hls-downloader) | Download | HLS detection and download flow |
| [Screenity](https://github.com/alyssaxuu/screenity) | Recording | Screen/camera recording with annotations |

**Key Libraries**: Mediabunny (lightweight media processing), Native MediaRecorder API

**Implementation Guide**: [rules/video.md](rules/video.md)

---

### 2. Audio
**Common Features**: Volume boost, per-tab volume control, audio visualization

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Better Volume Booster](https://github.com/zWolfrost/Better-Volume-Booster) | Volume Boost | Domain memory, mono/stereo toggle |
| [Tab Volume](https://github.com/wokalek/tab-volume) | Volume Control | Per-tab control with hotkeys |

**Key APIs**: Web Audio API (AudioContext, GainNode), chrome.tabCapture

**Implementation Guide**: [rules/audio.md](rules/audio.md)

---

### 3. Image
**Common Features**: Batch download, hover preview, background image extraction, screenshot (visible/full page/element)

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Image Downloader](https://github.com/PactInteractive/image-downloader) | Download | Batch download with filtering |
| [Pic-Grabber](https://github.com/venopyx/pic-grabber) | Download | Shadow DOM, lazy-load support |
| [screenshot-extension](https://github.com/lxieyang/screenshot-extension) | Screenshot | Full-page / region capture flow (MIT) |
| [webpage-screenshot](https://github.com/Aminadav/webpage-screenshot) | Screenshot | Classic full-page capture (ISC) |

**Key Techniques**: Canvas processing, Shadow DOM traversal, chrome.tabs.captureVisibleTab

**Libraries**: html2canvas, dom-to-image (for full page screenshots)

**Implementation Guide**: [rules/image.md](rules/image.md)

---

### 4. Translation
**Common Features**: Page translation, bilingual display, select-to-translate, PDF translation

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Immersive Translate](https://github.com/immersive-translate/immersive-translate) | Page Translation | Bilingual, PDF support |
| [Read Frog](https://github.com/mengxi-ream/read-frog) | AI Translation | Context-aware explanations |
| [OpenAI Translator](https://github.com/openai-translator/openai-translator) | AI Translation | ChatGPT-based translation |

**Key Libraries**: Readability.js (content extraction), PDF.js

**Implementation Guide**: [rules/translation.md](rules/translation.md)

---

### 5. Download
**Common Features**: Resource sniffing, batch download, external downloader integration

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Cat Catch](https://github.com/xifangczy/cat-catch) | Sniffing | Resource sniffing, M3U8/MPD, external downloaders (end-to-end “finish the file”) |
| [Live Stream Downloader](https://github.com/chandler-stimson/live-stream-downloader) | HLS | Merge segments in-extension vs. `chrome.downloads` saving only the playlist |
| [Video DownloadHelper](https://github.com/aclap-dev/video-downloadhelper) | Sniffing + app | Browser + native companion |
| [Stream Detector](https://github.com/54ac/stream-detector) | Detection | Export cookies for aria2 / yt-dlp, etc. |
| [Turbo Download Manager v2](https://github.com/inbasic/turbo-download-manager-v2) | Manager | Multi-connection, resume (direct URLs / files) |

**External Tools**: N_m3u8DL-RE, yt-dlp, aria2

**Implementation Guide**: [rules/download.md](rules/download.md)

---

### 6. Userscript
**Common Features**: Script manager, page enhancement, automation

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Tampermonkey](https://github.com/Tampermonkey/tampermonkey) | Manager | Most popular, cloud sync |
| [Violentmonkey](https://github.com/violentmonkey/violentmonkey) | Manager | Open source, lightweight |
| [Greasemonkey](https://github.com/greasemonkey/greasemonkey) | Manager | Firefox native |

**Dev Tools**: [vite-plugin-monkey](https://github.com/lisonge/vite-plugin-monkey) - Modern development with HMR

**Implementation Guide**: [rules/userscript.md](rules/userscript.md)

---

### 7. AI
**Common Features**: Sidebar chat, page summarization, reading assistant, prompt enhancement

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [BrainyAI](https://github.com/luyu0279/BrainyAI) | Sidebar | Multi-model sidebar (check Issues/Releases for maintenance) |
| [ChatGPT Box](https://github.com/josStorer/chatGPTBox) | Integration | Selection, summarize, site integrations (GPL-3.0, buildable reference) |
| [Scroll](https://github.com/asker-kurtelli/scroll) | Navigation | LLM web UI navigation helpers (MIT) |

**Chrome built-in AI (on-device)**: [Extensions and AI](https://developer.chrome.com/docs/extensions/ai) — Prompt, Summarizer, Translator, Language Detector, Writer, Rewriter, Proofreader ([status table](https://developer.chrome.com/docs/ai/built-in-apis)). Official samples: [ai.gemini-on-device](https://github.com/GoogleChrome/chrome-extensions-samples/tree/main/functional-samples/ai.gemini-on-device), [ai.gemini-on-device-summarization](https://github.com/GoogleChrome/chrome-extensions-samples/tree/main/functional-samples/ai.gemini-on-device-summarization).

**Built-in AI implementation guide**: [rules/chrome-built-in-ai.md](rules/chrome-built-in-ai.md)

**Key APIs**: OpenAI API, Google Gemini API, Anthropic Claude API, Ollama (local); **built-in**: `LanguageModel` (Prompt API), `Summarizer`, `Translator`, `LanguageDetector`, etc. ([docs](https://developer.chrome.com/docs/ai/built-in-apis))

**SDKs**: Vercel AI SDK, LangChain.js, LlamaIndex (TypeScript); typings: [`@types/dom-chromium-ai`](https://www.npmjs.com/package/@types/dom-chromium-ai)

**Implementation Guide**: [rules/ai.md](rules/ai.md)

---

### 8. Ad Blocker
**Common Features**: Ad blocking, tracker blocking, privacy protection, malware protection

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [uBlock Origin](https://github.com/gorhill/uBlock) | Ad Blocker | Efficient, low resource |
| [Privacy Badger](https://github.com/EFForg/privacybadger) | Privacy | Algorithmic tracker detection |

**Filter Lists**: EasyList, EasyPrivacy, uBlock filters

**Implementation Guide**: [rules/adblocker.md](rules/adblocker.md)

---

### 9. Theme
**Common Features**: Dark mode, custom CSS injection, theme management

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Dark Reader](https://github.com/darkreader/darkreader) | Dark Mode | Smart inversion, dynamic themes |
| [Stylus](https://github.com/openstyles/stylus) | CSS Manager | UserCSS support, cloud sync |

**NPM Package**: `darkreader` - Use in your projects

**Implementation Guide**: [rules/theme.md](rules/theme.md)

---

### 10. Email
**Common Features**: Email notifications, quick preview, multi-account support

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Mail Checker Plus](https://github.com/AndersSahlin/MailCheckerPlus) | Gmail | Unread badge, list preview, mark read, etc. (GPL-3.0, Gmail API reference) |
| [gmail-api-chrome-extension](https://github.com/anatelli10/gmail-api-chrome-extension) | Gmail API | Minimal OAuth + Gmail REST sample (MIT, auth flow learning) |

**Key APIs**: Gmail API, chrome.identity

**Implementation Guide**: [rules/email.md](rules/email.md)

---

### 11. Game
**Common Features**: WebAssembly modification, memory editing, auto-click

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Cetus](https://github.com/Qwokka/Cetus) | WASM Hacking | Memory search, freeze, breakpoints |

**Note**: Use responsibly, only on single-player/offline games

**Implementation Guide**: [rules/game.md](rules/game.md)

---

### 12. Password Manager
**Common Features**: Password storage, auto-fill, password generation, encryption

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [Bitwarden](https://github.com/bitwarden/clients) | Full Featured | Cloud sync, cross-platform |
| [KeePassXC-Browser](https://github.com/keepassxreboot/keepassxc-browser) | Integration | Local password database |

**Key APIs**: Web Crypto API (AES-256-GCM, PBKDF2)

**Implementation Guide**: [rules/password-manager.md](rules/password-manager.md)

---

### 13. Web3 Wallet
**Common Features**: Wallet management, transaction signing, DApp connection, multi-chain

| Reference Projects | Type | Highlights |
|-------------------|------|------------|
| [MetaMask](https://github.com/MetaMask/metamask-extension) | Wallet | Industry standard, EIP-1193 |
| [Rabby](https://github.com/RabbyHub/Rabby) | Wallet | Multi-chain, transaction simulation |
| [Rainbow](https://github.com/rainbow-me/browser-extension) | Wallet | Extension source (distinct from mobile app repo) |

**Key Libraries**: ethers.js, viem

**Standards**: EIP-1193 (Provider API), EIP-712 (Typed Data)

**Implementation Guide**: [rules/web3.md](rules/web3.md)

---

## Library Choices Summary

| Domain | Preferred | Avoid (in extension) |
|--------|-----------|---------------------|
| Video/Audio processing | Mediabunny | FFmpeg.wasm (large, slow) |
| Recording | Native MediaRecorder | Heavy encoder libs |
| Screenshots | chrome.tabs.captureVisibleTab | Large image libs |
| AI | Remote API calls | Large local models (WASM/ONNX) |
| Translation | Remote API | Bundled NLP models |
| Userscript execution | Sandboxed iframe | Direct eval() |
| Download | chrome.downloads + stream | In-memory buffering |
| Encryption | Web Crypto API | Custom crypto implementations |

## Permissions Quick Reference

| Feature | Key Permissions |
|---------|-----------------|
| Video Download | `downloads`, `webRequest`/`declarativeNetRequest` |
| Audio Processing | `tabCapture`, `offscreen` (MV3) |
| Image Download | `downloads`, `activeTab` |
| Translation | `activeTab`, `storage` |
| Userscript | `<all_urls>`, `storage` |
| AI | `sidePanel`, `storage` |
| Ad Blocker | `declarativeNetRequest`, `<all_urls>` |
| Theme | `activeTab`, `scripting` |
| Email | `identity`, `notifications` |
| Password Manager | `storage`, `activeTab`, `scripting` |
| Web3 | `storage`, `activeTab`, `scripting` |

## Additional Resources

- **Detailed References**: [reference.md](reference.md)
- **Addfox Best Practices**: Use the addfox-best-practices skill for project structure
- **Chrome Extension Docs**: https://developer.chrome.com/docs/extensions/
- **Firefox Extension Docs**: https://developer.mozilla.org/en-US/docs/Mozilla/Add-ons/WebExtensions
