# Vertex AI Billing Switch for Gemini CLI

[![Version](https://img.shields.io/badge/version-1.4.1-blue.svg)](./skills/en/SKILL.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[![Platform](https://img.shields.io/badge/platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey.svg)]()

[繁體中文版](./README.zh-TW.md)

A **Gemini CLI Skill** that automates GCP Vertex AI authentication setup and deploys a global billing auto-switch Hook — helping newcomers get Vertex AI running with zero manual configuration.

---

> [!WARNING]
> **IMPORTANT DISCLAIMER**
>
> This tool is designed **only** for Google Cloud accounts **without any credit card or payment method attached**.
>
> If a payment method is attached to your account, unexpected charges may occur. **The authors are not responsible for any charges incurred.** Please verify your account has no payment method before proceeding.

---

## Features

- **Interactive setup wizard** — 7-step guided process, no manual configuration needed
- **Auto-create GCP project** — create a new GCP project via `gcloud` CLI without leaving the terminal
- **Quick switch mode** — returning users can switch GCP projects without re-authentication; switching Google accounts still opens a browser
- **Billing account renaming** — rename billing accounts to include expiration dates for easier identification (e.g., `Trial_Exp_20260501`)
- **Automatic gcloud installation** — detects and installs Google Cloud CLI if missing (Windows / macOS / Linux)
- **ADC authentication** — configures Application Default Credentials for Vertex AI
- **Billing auto-switch Hook** — deployed as a Gemini CLI `SessionStart` hook, runs automatically on every startup
- **Smart account switching** — scans available billing accounts and switches when quota is exhausted
- **Cross-platform** — supports Windows, macOS, and Linux
- **Non-destructive** — never overwrites existing `settings.json` keys; only adds what's needed
- **Bilingual** — available in English and Traditional Chinese

---

## Prerequisites

- [Gemini CLI](https://github.com/google-gemini/gemini-cli) installed
- [Node.js](https://nodejs.org/) (for the Hook script at runtime)
- A Google Cloud account (**no credit cards attached to billing accounts**)
  - If you already have a GCP project: the skill will use it directly
  - If not: the skill can auto-create one for you (requires at least one billing account with credits)
  - Each billing account needs an active billing plan set up in Google AI Studio

---

## Quick Start

### Run in your standard terminal / command prompt:

1. **Install the Skill:**

   ```bash
   gemini extensions install https://github.com/AndyAWD/VertexAiBillingSwitchSkill
   ```

2. **Update the Skill:**

   ```bash
   gemini extensions update vertex-ai-billing-switch-skill
   ```

### Run in Gemini CLI:

1. **Run the Skill:**

   ```
   /vertex-ai-billing-switch-skill:en run the skill workflow
   ```

2. After setup completes:
   - Type `/quit` to exit Gemini CLI
   - **Restart Gemini CLI**, then type `/auth` to switch to **Vertex AI** authentication mode
   - Type `/model` to choose your preferred model

---

## How It Works

### Setup Wizard

```
/en run the skill workflow
        │
        ▼
  Step 0 ── Disclaimer confirmation
        │
        ▼
  Step 1 ── Environment detection
             ├─ All ready (returning user) → Switch project, Rename accounts, or Full reset
             │   ├─ Switch project → Same account: skip to Step 4
             │   │                 → Switch account: Step 3 → Step 4
             │   └─ Rename accounts → Step R → Done
             └─ Not ready (first-time) → Continue full flow ↓
        │
        ▼
  Step 2 ── Check / auto-install gcloud CLI
        │
        ▼
  Step 3 ── GCP auth login
        │
        ▼
  Step 4 ── Get / Create GCP project
             ├─ Enter existing project ID
             └─ Auto-create via gcloud (detect billing → name → create → link)
        │
        ▼
  Step 5 ── GCP config + Gemini CLI deployment
             ├─ gcloud config set project
             ├─ Enable Vertex AI API
             ├─ gcloud auth application-default login (ADC)
             ├─ ~/.gemini/.env  (GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION)
             ├─ ~/.gemini/settings.json  (register Hook)  [first-time only]
             └─ ~/.gemini/hooks/vertex-ai-billing-switch-hook.mjs  [first-time only]
        │
        ▼
  Step 6 ── Verify all items → Done
```

### Billing Auto-Switch Hook (every Gemini CLI startup)

```
Gemini CLI starts → SessionStart Hook fires
        │
        ▼
  Check current billing account status
        │
        ├─ OK ──────────────────────────────► Continue normally
        │
        └─ Quota exhausted / Account closed
                │
                ▼
          Scan all available billing accounts
                │
                ▼
          Switch to an available account
                │
                ▼
          Verify link success → Continue
```

---

## What Gets Deployed

| File | Location | Purpose |
|------|----------|---------|
| `.env` | `~/.gemini/.env` | Sets `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION` |
| `settings.json` | `~/.gemini/settings.json` | Registers the `SessionStart` hook |
| Hook script | `~/.gemini/hooks/vertex-ai-billing-switch-hook.mjs` | Billing auto-switch logic |

---

## Repository Structure

```
VertexAiBillingSwitchSkill/
├── README.md                              # This file (English)
├── README.zh-TW.md                        # Traditional Chinese version
├── package.json                           # NPM package manifest
├── gemini-extension.json                  # Gemini CLI extension manifest
│
└── skills/                                # Gemini CLI Skills directory
    ├── en/       # English Skill
    │   ├── SKILL.md                       # Skill definition (loaded by Gemini CLI)
    │   ├── references/                    # On-demand reference docs
    │   │   ├── config-and-verify.md       # Config and Verification (Step 5 & 6)
    │   │   ├── install-gcloud.md          # Platform-specific gcloud installation
    │   │   ├── create-project.md          # Auto-create GCP project sub-flow
    │   │   ├── deploy-hook.md             # First-time Hook deployment
    │   │   └── rename-accounts.md         # Batch rename billing accounts
    │   ├── assets/
    │   │   └── vertex-ai-billing-switch-hook.mjs
    │   └── scripts/
    │       ├── install-gcloud.mjs
    │       └── consume-credits.mjs
    │
    └── zh-tw/    # Traditional Chinese Skill
        ├── SKILL.md                       # Skill 定義（由 Gemini CLI 載入）
        ├── references/                    # 按需讀取的參考文件
        │   ├── config-and-verify.md
        │   ├── install-gcloud.md
        │   ├── create-project.md
        │   ├── deploy-hook.md
        │   └── rename-accounts.md
        ├── assets/
        │   └── vertex-ai-billing-switch-hook.mjs
        └── scripts/
            ├── install-gcloud.mjs
            └── consume-credits.mjs
```

---

## Contributing a New Language

Want to add your language? You only need to translate a few Markdown files — the code files can be copied as-is. No engineering skills required.

### What to do with each file

| File | Action |
|------|--------|
| `skills/en/SKILL.md` | Translate + update paths |
| `skills/en/references/config-and-verify.md` | Translate + update paths |
| `skills/en/references/deploy-hook.md` | Translate + update paths |
| `skills/en/references/create-project.md` | Translate |
| `skills/en/references/install-gcloud.md` | Translate |
| `skills/en/references/rename-accounts.md` | Translate |
| `skills/en/assets/vertex-ai-billing-switch-hook.mjs` | Copy as-is — no changes needed |
| `skills/en/scripts/install-gcloud.mjs` | Copy as-is — no changes needed |
| `skills/en/scripts/consume-credits.mjs` | Copy as-is — no changes needed |

### Use AI to do it in one shot

Copy the prompt below to your AI. Replace `[LANG_CODE]` with your language code (e.g. `ja`) and `[TARGET_LANGUAGE]` with the language name (e.g. `Japanese`):

````
I want to add a [TARGET_LANGUAGE] translation of this Gemini CLI skill (language code: [LANG_CODE]).

## Files to translate
Translate the Markdown body (everything after the `---` frontmatter block) from English to [TARGET_LANGUAGE] for these files:
- `skills/en/SKILL.md`
- `skills/en/references/config-and-verify.md`
- `skills/en/references/deploy-hook.md`
- `skills/en/references/create-project.md`
- `skills/en/references/install-gcloud.md`
- `skills/en/references/rename-accounts.md`

## Rules — MUST follow
- Keep ALL code blocks (``` blocks) unchanged — do NOT translate code
- Keep ALL JSON objects unchanged — do NOT translate keys or values
- Keep ALL variable placeholders like `{home_dir}`, `{project_id}`, `{skill_dir}` unchanged
- Keep ALL markdown headings (##), tables, and formatting unchanged
- Only translate human-readable prose and UI strings (questions, labels, descriptions, and informational messages)

## After translating — apply these exact string replacements

In `SKILL.md` frontmatter, replace:
- `name: en` → `name: [LANG_CODE]`

In `SKILL.md` body, replace these 3 exact strings:
1. `{home_dir}/.gemini/skills/en` → `{home_dir}/.gemini/skills/[LANG_CODE]`
2. `/en run the skill workflow` → `/[LANG_CODE] [TRANSLATED_COMMAND]`
3. `` run `/en run the skill workflow` `` → `` run `/[LANG_CODE] [TRANSLATED_COMMAND]` ``

In `references/config-and-verify.md`, replace this exact string:
1. `/.gemini/skills/en` → `/.gemini/skills/[LANG_CODE]`

In `references/deploy-hook.md`, replace these 2 exact strings:
1. `extensions/VertexAiBillingSwitchSkill/skills/en` → `extensions/VertexAiBillingSwitchSkill/skills/[LANG_CODE]`
2. `/.gemini/skills/en` → `/.gemini/skills/[LANG_CODE]`

## Files to copy WITHOUT modification
Copy these files exactly as-is (do not translate):
- `skills/en/assets/vertex-ai-billing-switch-hook.mjs`
- `skills/en/scripts/install-gcloud.mjs`
- `skills/en/scripts/consume-credits.mjs`

## Output structure
Save everything under `skills/[LANG_CODE]/` with this exact structure:
```
skills/[LANG_CODE]/
├── SKILL.md
├── references/
│   ├── config-and-verify.md
│   ├── deploy-hook.md
│   ├── create-project.md
│   ├── install-gcloud.md
│   └── rename-accounts.md
├── assets/
│   └── vertex-ai-billing-switch-hook.mjs
└── scripts/
    ├── install-gcloud.mjs
    └── consume-credits.mjs
```

## Self-check before finishing
- [ ] `SKILL.md` frontmatter has `name: [LANG_CODE]`
- [ ] No occurrence of `skills/en` remains in any translated file
- [ ] No occurrence of `/en ` (as a skill command) remains in SKILL.md
- [ ] All `.mjs` files are identical to the originals in `skills/en/`
````

Once done, open a Pull Request with the `skills/[LANG_CODE]/` directory!

---

## Testing the Hook

A `consume-credits.mjs` script is included to intentionally exhaust quota and verify the auto-switch mechanism works:

```bash
node skills/en/scripts/consume-credits.mjs
```

The script sends large Vertex AI API requests in a loop until a `402`, `BILLING_DISABLED`, or quota-exceeded error is returned, which triggers the Hook on next Gemini CLI startup.

---

## License

MIT © 2024

See [LICENSE](./LICENSE) for details.

