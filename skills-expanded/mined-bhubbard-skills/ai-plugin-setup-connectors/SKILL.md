---
name: ai-plugin-setup-connectors
description: "How to install and configure AI connectors for the official WordPress AI plugin (slug: ai) including Anthropic, Google, and OpenAI integrations."
---

# Setup and Connectors (WordPress AI Plugin)

The official WordPress [AI Plugin](https://wordpress.org/plugins/ai/) brings AI-powered features directly into the WordPress admin and editing experience. 

## The Connector Architecture

By design, the AI plugin **does not include any provider credentials or API implementations by itself**. It relies on independent "AI Connector" plugins to provide the actual bridge to Large Language Models.

To use the AI plugin, you must install and authenticate at least one connector.

### Supported Connectors

*   **Anthropic (Claude):** `ai-provider-for-anthropic`
*   **Google (Gemini):** `ai-provider-for-google`
*   **OpenAI (ChatGPT):** `ai-provider-for-openai`
*   **Ollama (Local/Free):** `ai-provider-for-ollama`

### Configuration Workflow

1.  **Install the Base Plugin:** Install and activate the `ai` plugin.
2.  **Install a Connector:** Install and activate one or more of the provider plugins listed above.
3.  **Authenticate:** Navigate to `Settings -> Connectors` in the WordPress admin area to enter the relevant API keys for your chosen providers.
4.  **Enable Features:** Go to `Settings -> AI`. First, globally enable AI functionality. Then, selectively enable the specific "experiments" (features) you wish to use.

## Important Notes

*   **API Keys Required:** Unless a hosting provider or agency pre-configures credentials using constants or environment variables, the site owner must supply their own API keys and pay for their own token usage.
*   **Connector Approvals:** Administrators can use the "Connector Approvals" experiment to explicitly govern which other plugins or themes on the site are permitted to use the configured AI connectors, ensuring security and cost control.
*   **Fallback Handling:** If a user triggers an AI feature without a connector configured, the plugin will gracefully show actionable guidance directing them to the Connectors settings page.
