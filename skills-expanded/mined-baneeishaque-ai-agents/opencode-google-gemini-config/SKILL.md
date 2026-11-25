---
name: opencode-google-gemini-config
description: Configure and troubleshoot Google AI Studio Gemini models in OpenCode CLI — credential setup, the restart-retention bug, and the explicit config-block fix using opencode-provider-persistence-config
category: Tool-Configuration
---

# opencode Google Gemini Configuration Skill (v1)

## Composition Rationale

This skill is a **composer**: it does NOT re-document the OpenCode credential
storage model or the startup registration gap — those are owned by the base
skill [`opencode-provider-persistence-config`](../opencode-provider-persistence-config/SKILL.md).

It composes the base skill as follows:

1. Consumes the base skill's §2 (Startup Provider Registration) and §3 (Config
   Declaration Requirement) to explain *why* the Google/Gemini API key saved
   via `/connect` disappears after restart.
2. Adds domain-specific value on top of the base: the exact Google AI Studio
   credential setup workflow, the concrete `"google": {}` config stanza, and
   the verification steps specific to Gemini models.

The composer's value-add over the base alone: a single, self-contained
procedure that a user can follow to diagnose and fix the Gemini-specific
version of the general "provider key disappears after restart" problem.

---

## 1. Google AI Studio Credential Setup

### 1.1 Prerequisites

- A Google account with access to [Google AI Studio](https://aistudio.google.com/).
- An API key created in AI Studio (available at `https://aistudio.google.com/apikey`).

### 1.2 Connect via /connect

1. Launch OpenCode and run the `/connect` command in the TUI.
2. Search for and select **Google** from the provider list.
3. Select **Manually enter API Key**.
4. Paste your Google AI Studio API key.
5. Run `/models` to verify the Gemini models are available.

### 1.3 Verify Credential Storage

After `/connect` succeeds, confirm the key was persisted:

```bash
opencode auth list
# Expected output includes: google  ✓
```

The key is stored in `<user-home>/.local/share/opencode/auth.json` under the
`google` key.

---

## 2. The Restart-Retention Bug

### 2.1 Symptom

1. User runs `/connect`, selects **Google**, enters API key.
2. Gemini models appear in `/models`. User selects one and works normally.
3. User quits OpenCode and relaunches.
4. The Google provider is no longer in the model picker. `/models` shows no
   Gemini models.
5. The user must re-run `/connect` and re-enter the API key.

### 2.2 Root Cause

The API key IS successfully persisted to `<user-home>/.local/share/opencode/auth.json`
— it survives the restart at the file level (per `opencode auth list`).

However, OpenCode's startup registration logic (§2 of the base skill) only
auto-loads providers that are explicitly declared in the `provider` section
of `opencode.json`. The `google` provider was connected via `/connect` but
was NOT declared in `opencode.json`. On restart, the `google` provider ID is
missing from the provider registry, so even though the credential exists in
`auth.json`, it is never loaded.

### 2.3 Diagnosis Steps

1. **Check if the key is stored:**

   ```bash
   cat <user-home>/.local/share/opencode/auth.json
   ```

   Look for a `"google"` entry. If it exists, the key is persisted — the issue
   is in the startup registration, not the storage.

2. **Check if the provider is declared in config:**

   ```bash
   cat ~/.config/opencode/opencode.json
   ```

   Look for a `"provider"` section containing `"google"`. If absent, this is
   the root cause.

---

## 3. The Fix: Declare Google in opencode.json

### 3.1 Add the Provider Block

Edit `~/.config/opencode/opencode.json` (or project-level `opencode.json`)
to add the `google` provider entry:

```json
{
  "provider": {
    "google": {}
  }
}
```

If the file already has a `"provider"` section (e.g., with other providers),
add the `"google"` entry inside the existing section:

```json
{
  "provider": {
    "openrouter": {},
    "google": {}
  }
}
```

The empty object `{}` tells OpenCode to use the Google Gemini API defaults
(standard Gemini API endpoint at `generativelanguage.googleapis.com`).

### 3.2 Restart OpenCode

1. Quit OpenCode completely.
2. Relaunch OpenCode.
3. Run `/models`.
4. Confirm Gemini models appear in the list.
5. Select a Gemini model (e.g., `gemini-2.5-pro`, `gemini-2.5-flash`).

### 3.3 Verification

Send a test prompt to confirm the connection works:

```text
/ The Google provider is configured. List 3 available Gemini models.
```

If the model responds, the fix is confirmed.

---

## 4. Alternative: Environment Variable

As an alternative to declaring the provider in config, set the API key via
environment variable:

```bash
export GOOGLE_GENERATIVE_AI_API_KEY="your-key-here"
opencode
```

When the environment variable is set, OpenCode picks it up automatically
and registers the Google provider without needing the config declaration.
This is useful for ephemeral sessions or CI environments.

---

## 5. Related Skills

- [`opencode-jsonc-util`](../opencode-jsonc-util/SKILL.md) — Base JSONC utility for OpenCode config files
- [`opencode-provider-persistence-config`](../opencode-provider-persistence-config/SKILL.md)
  — **Base skill.** Owns the generic OpenCode credential storage model and
  startup registration knowledge that this composer builds upon. Refer to
  that skill for the architectural fundamentals — this skill documents only
  the Google/Gemini-specific layer.
- [`opencode-permission-config`](../opencode-permission-config/SKILL.md) —
  OpenCode permission system configuration (complementary domain).

## Source Rules

- [OpenCode Docs — Providers](https://opencode.ai/docs/providers/)
- [OpenCode JSON Schema](https://opencode.ai/config.json)
- [Google AI Studio API Keys](https://aistudio.google.com/apikey)
