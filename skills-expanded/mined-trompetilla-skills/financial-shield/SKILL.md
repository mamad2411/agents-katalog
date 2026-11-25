---
name: financial-shield
description: Financial Shield (Stay in the Cheap Tier!) Tired of those "Long Context" double-billing surprises? I just published Financial Shield to ClawHub! This skill is designed to keep your sessions within the 128k "cheap" tier by monitoring your context weight and alerting you before you hit the expensive zone. Key Features: • 📊 Real-time Monitoring: Includes a check_shield.sh script to parse your session_status. • 💰 Cost Control: Pre-configured for the Google Gemini 128k ceiling, but the script is easily editable if your provider (like Anthropic or OpenAI) has different "cheap" vs "expensive" tiers. • 🕒 Continuous Tracking: Instructions for agents to append (Usage: X/128k) to every message so you're never in the dark. How to get it: openclaw clawhub install financial-shield Note: This was built with Google's API tiers in mind, but you can easily tweak the limit in the script to match your specific provider's billing zones!
---

# Financial Shield

This skill ensures that the agent remains within the standard pricing tier (<128k tokens) for Google Gemini models by actively managing context bloat.

## Rules of Operation

1. **Always-On Counter:** The agent MUST include the current token usage (e.g., `(Current Usage: 45k/128k)`) at the end of every message while this skill is installed.
2. **Context Monitoring:** The agent must check the current token count (via `session_status`) before performing token-heavy tasks like image analysis.
3. **The 128k Wall:** If the current context is above 110,000 tokens, the agent MUST notify the user before the next turn that they are approaching the "Double Billing" zone.
4. **Hard Reset:** If the context exceeds 125,000 tokens, the agent will:
    - Automatically summarize all key facts/decisions from the current session into `MEMORY.md`.
    - Request a session reset (`/new`) or manually trim the history to bring the count back to near zero.
5. **Output Discipline:** All responses must be "Logic-First" and concise. No conversational filler or repeated instructions.

## When to Use
- Triggered automatically when context > 110k.
- Can be invoked manually by the user saying "Activate Financial Shield."
