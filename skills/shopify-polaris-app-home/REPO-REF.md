# Repo Referensi: shopify/shopify-ai-toolkit

Repo: https://github.com/shopify/shopify-ai-toolkit
Ref lokal: /Users/chaali0324/.agents/repo-refs/shopify_shopify-ai-toolkit
API: curl "localhost:27126/repos/readme?name=shopify_shopify-ai-toolkit"
Dibuat: 2026-09-16

## Cuplikan README
# shopify/shopify-ai-toolkit

Source: https://github.com/shopify/shopify-ai-toolkit
Fetched: 2026-09-16

## README
# Shopify AI Toolkit - AI Agent Plugin

Connect your AI tools to the Shopify platform.

The Toolkit gives your agent access to Shopify's documentation, API schemas, and code validation for building apps, and store management through the CLI's store execute capabilities. For more info, [see the docs](https://shopify.dev/docs/apps/build/ai-toolkit).

## Install

- **For Claude Code**: In your terminal, run `claude plugin install`:

  ```
  claude plugin install shopify-ai-toolkit@claude-plugins-official
  ```

- **For OpenAI Codex**: In your terminal, run `codex plugin add`:

  ```
  codex plugin add shopify@openai-curated
  ```

- **For Antigravity CLI**: In your terminal, install the Shopify plugin:

  ```
  agy plugin install https://github.com/Shopify/shopify-ai-toolkit
  ```

- **For Cursor**: In Cursor Chat, add the Shopify plugin:

  ```
  /add-plugin shopify
  ```

- **For Hermes**: In your terminal, download the install script and run it:

  ```
  curl -fsSL https://raw.githubusercontent.com/Shopify/Shopify-AI-Toolkit/main/.hermes-plugin/install.sh -o /tmp/shopify-hermes-install.sh
  bash /tmp/shopify-hermes-install.sh
  ```

- **For OpenClaw**: In your terminal, install the package from npm:

  ```
  openclaw plugins install npm:@shopify/ai-toolkit
  ```

  Alternatively, install from ClawHub with `openclaw plugins install clawhub:@shopify/ai-toolkit`, or directly from the git mirror with `openclaw plugins install git:github.com/Shopify/Shopify-AI-Toolkit`. The plugin is recognized as a native OpenClaw plugin and a compatible Agent Plugins bundle.

- **For Pi**: In your terminal, install the package from npm:

  ```
  pi install npm:@shopify/ai-toolkit
  ```

  Alternatively, install directly from the git mirror:

  ```
  pi install git:github.com/Shopify/Shopify-AI-Toolkit
  ```

- **For VS Code**:
  1. Ensure the [Agent plugins](https://code.visualstudio.com/docs/copilot/customization/agent-plugins) preview is enabled in your VS Code settings.

  2. Open the Command Palette (`Cmd+Shift+P` on macOS, `Ctrl+Shift+P` on Windows/Linux) and run:

     ```
     Chat: Install Plugin From Source
     ```

  3. When prompted, enter the repository URL:

     ```
     https://github.com/Shopify/shopify-ai-toolkit
     ```

## What you get

- **Docs and API schemas**: Search Shopify's documentation and API schemas without leaving your editor
- **
