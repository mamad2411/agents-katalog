---
name: ai-plugin-developer-extensibility
description: "Developer guide for extending the official WordPress AI plugin, using the Abstract_Feature class, Abilities API, and interacting with the Model Context Protocol (MCP)."
---

# Developer Extensibility (WordPress AI Plugin)

The official WordPress AI plugin is designed to act as a reference implementation for the "AI Building Blocks for WordPress" initiative. It exposes a robust API for developers to extend, customize, and study AI integration in WordPress.

## Core Concepts

### 1. The Abilities API
The plugin is built on top of the Abilities API, which standardizes how WordPress asks an AI to perform a task. 
*   **Abilities Explorer:** Available in the WordPress admin when experiments are enabled. This tool allows developers to browse registered AI abilities, view their input/output JSON schemas, and test payloads directly.
*   **Registering Abilities:** Developers can hook into the Abilities API to register their own custom AI capabilities.

### 2. Building Custom Experiments
Developers can create their own AI-powered features by extending the plugin's `Abstract_Feature` base class. 

### 3. Developer Mode
The plugin includes a "Developer Mode" toggle on its settings page. This mode allows developers to override default behaviors and set specific AI providers and models on a *per-feature* basis, which is highly useful for testing how different LLMs perform on specific tasks (e.g., forcing Claude for Summarization, but OpenAI for Title Generation).

## Customization Hooks

The plugin provides extensive filters and actions to override default behavior:
*   **System Instructions:** Hooks exist to customize the system instructions and contextual prompts sent to the LLM during operations.
*   **Authentication Detection:** The `wpai_has_ai_credentials` filter allows third-party connector plugins (especially those not using standard API keys, like local Ollama setups) to report their configured status to the main plugin.
*   **Guidelines:** AI queries can be filtered to inject specific site-wide editorial guidelines.

## Observability and Control

*   **AI Request Logging:** Developers can enable this experiment to log all outbound AI requests. This is critical for debugging prompts, observing token usage, and reviewing raw LLM responses.
*   **Connector Approvals:** A framework allowing administrators to explicitly grant or deny third-party plugins access to the site's configured AI Connectors.
*   **WP-CLI:** Includes commands for automation, such as `wp ai alt-text generate`.

## Looking Forward: MCP Integration
The plugin is actively laying the groundwork to integrate and test **Model Context Protocol (MCP)** capabilities directly within WordPress workflows. Strict JSON schema validation is already enforced on Ability outputs to ensure compatibility with strict REST and MCP consumers.
