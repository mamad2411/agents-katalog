---
name: api-integration-category-pointer
description: "Pointer to a library of 30 specialized Api Integration skills. Use when working on api-integration-related tasks."
risk: none
---

# Api Integration Capability Library 🎯

This is a **pointer skill**. The 30 specialized Api Integration skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **2slides-ppt-generator** — AI-powered presentation generation via the 2slides API — create slides from text, match a reference image style, summarize documents into decks, add AI voice narration, and export pages/audio. Use for any "make slides", "create a deck", or "slides from this document" request.
- **algolia-search** — Expert patterns for Algolia search implementation, indexing strategies, React InstantSearch, and relevance tuning
- **discord-automation** — Automate Discord tasks via Rube MCP (Composio): messages, channels, roles, webhooks, reactions. Always search tools first for current schemas.
- **famulor-skill** — Operate Famulor assistants, communication history, campaigns, knowledge, automations, telephony, and workspace administration through its hosted MCP server.
- **hubspot-integration** — Expert patterns for HubSpot CRM integration including OAuth authentication, CRM objects, associations, batch operations, webhooks, and custom objects. Covers Node.js and Python SDKs.
- **microsoft-teams-automation** — Automate Microsoft Teams tasks via Rube MCP (Composio): send messages, manage channels, create meetings, handle chats, and search messages. Always search tools first for current schemas.
- **moodle-external-api-development** — This skill guides you through creating custom external web service APIs for Moodle LMS, following Moodle's external API framework and coding standards.
- **openapi-spec-generation** — Generate and maintain OpenAPI 3.1 specifications from code, design-first specs, and validation patterns. Use when creating API documentation, generating SDKs, or ensuring API contract compliance.
- **pakistan-payments-stack** — Design and implement production-grade Pakistani payment integrations (JazzCash, Easypaisa, bank/PSP rails, optional Raast) for SaaS with PKR billing, webhook reliability, and reconciliation.
- **payment-integration** — Integrate Stripe, PayPal, and payment processors. Handles checkout flows, subscriptions, webhooks, and PCI compliance. Use PROACTIVELY when implementing payments, billing, or subscription features.
- **paypal-integration** — Master PayPal payment integration including Express Checkout, IPN handling, recurring billing, and refund workflows.
- **plaid-fintech** — Expert patterns for Plaid API integration including Link token flows, transactions sync, identity verification, Auth for ACH, balance checks, webhook handling, and fintech compliance best practices.
- **postmark-automation** — Automate Postmark email delivery tasks via Rube MCP (Composio): send templated emails, manage templates, monitor delivery stats and bounces. Always search tools first for current schemas.
- **riffkit** — Riff a winning TikTok into your own short video — study a proven video's emotion formula and regenerate it with your product, character, and language (9 supported). Also makes UGC ad creative.
- **salesforce-automation** — Automate Salesforce tasks via Rube MCP (Composio): leads, contacts, accounts, opportunities, SOQL queries. Always search tools first for current schemas.
- **salesforce-development** — Expert patterns for Salesforce platform development including Lightning Web Components (LWC), Apex triggers and classes, REST/Bulk APIs, External Client Apps, and Salesforce DX with scratch orgs and 2nd generation packages (2GP).
- **sendblue-api** — Send and receive iMessage, SMS, and RCS from application code via the Sendblue HTTP API — text, media, group messages, send styles, reactions, typing indicators, status callbacks, and inbound webhooks.
- **sendblue-cli** — Send iMessage and SMS from the shell via the @sendblue/cli npm package — outbound sends, contact management, and account setup with no API client or webhook server required.
- **shopify-apps** — Expert patterns for Shopify app development including Remix/React Router apps, embedded apps with App Bridge, webhook handling, GraphQL Admin API, Polaris components, billing, and app extensions.
- **shopify-development** — Build Shopify apps, extensions, themes using GraphQL Admin API, Shopify CLI, Polaris UI, and Liquid.
- **slack-bot-builder** — Build Slack apps using the Bolt framework across Python, JavaScript, and Java. Covers Block Kit for rich UIs, interactive components, slash commands, event handling, OAuth installation flows, and Workflow Builder integration.
- **square-automation** — Automate Square tasks via Rube MCP (Composio): payments, orders, invoices, locations. Always search tools first for current schemas.
- **stripe-integration** — Implement and verify Stripe checkout, subscriptions, webhooks and refunds with explicit server-side authorization and retry boundaries.
- **telegram-automation** — Automate Telegram tasks via Rube MCP (Composio): send messages, manage chats, share photos/documents, and handle bot commands. Always search tools first for current schemas.
- **telegram-bot-builder** — Expert in building Telegram bots that solve real problems - from simple automation to complex AI-powered bots. Covers bot architecture, the Telegram Bot API, user experience, monetization strategies, and scaling bots to thousands of users.
- **twilio-communications** — Build communication features with Twilio: SMS messaging, voice calls, WhatsApp Business API, and user verification (2FA). Covers the full spectrum from simple notifications to complex IVR systems and multi-channel authentication.
- **unsplash-integration** — Integration skill for searching and fetching high-quality, free-to-use professional photography from Unsplash.
- **us-property-data** — Use when a task needs real U.S. residential property data: valuation, listings, price or tax history, schools, or a zillow.com URL.
- **whatsapp-automation** — Automate WhatsApp Business tasks via Rube MCP (Composio): send messages, manage templates, upload media, and handle contacts. Always search tools first for current schemas.
- **youtube-full** — Fetch YouTube transcripts, search videos, browse channels, and extract playlists via TranscriptAPI — no yt-dlp, no Google API key, works from any cloud server.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `view_file` to read its `SKILL.md` from the vault:
   `<CONFIG_ROOT>/.config/opencode/skill-libraries/api-integration/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `<CONFIG_ROOT>/.config/opencode/skill-libraries/api-integration`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
