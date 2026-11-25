---
name: bc-site-setup
description: Create websites using the BC Site Set-up workflow. Integrates Azure Kim (Mistral), Antigravity resources, Gemini CLI, Remotion Video, and AI Services (Gemini/Stammer/WebSpeech).
---

# BC's Site Set-up

This skill orchestrates the creation of high-end, AI-powered websites. It combines the "Kim" thinking model (Azure Mistral) for planning, Google Antigravity for resources, and integrates real-time AI services and video.

## Prerequisites

-   **Azure Agent (Kim)**: `/home/bc/antigravity/skills/ralph_wiggum/resources/mistral_agent.py`
-   **AI Services**:
    -   `src/Services/VoiceService.ts` (Web Speech API - **FREE**)
    -   `src/Services/GeminiService.ts` (Google Gemini 2.0 Flash)
    -   `src/Services/StammerService.ts` (Stammer.ai Voice/Chat - *Premium*)
-   **Video**: `remotion-best-practices` skill & `<Player />` component.
-   **Design**: Tailwind CSS (configured via `tailwind.config.js`).

## Workflow

### 1. Plan with Kim (Azure Mistral)
Consult the Azure Mistral agent for architectural advice. It has access to the `/home/bc/antigravity` knowledge base.
```bash
echo "Plan a website for: [User Prompt]" | python3 /home/bc/antigravity/skills/ralph_wiggum/resources/mistral_agent.py
```

### 2. Design & Build (Antigravity Style)
Implement the frontend using `frontend-design` principles:
-   **Aesthetics**: Bold, distinctive, production-grade.
-   **Styling**: Use Tailwind CSS (preferred) or Vanilla CSS.
-   **Structure**: React + TypeScript + Vite.

### 3. Integrate AI Intelligence
Make the site "smart" by connecting AI services. Choose the right tier for your needs:

-   **Free Voice**: Use `VoiceService.ts`.
    -   *Implementation*: `VoiceService.speak("Hello")` and `VoiceService.listen()`.
    -   *Pros*: Free, client-side only, no setup.
    -   *Cons*: Robotic voices, dependent on browser support.

-   **Gemini (LLM)**: Use `GeminiService.ts`.
    -   *Implementation*: `sendGeminiMessage(...)`
    -   *Requires*: `VITE_GEMINI_API_KEY`.

-   **Stammer (Premium Voice)**: Use `StammerService.ts`.
    -   *Implementation*: `sendStammerMessage(...)`
    -   *Requires*: Paid account, API keys, proxy setup.

### 4. Enhance with Video (Remotion)
Embed high-quality video content using the `<Player />` component:
-   **Hero Section**: Use a Remotion composition (like `RedVsBlueVideo` or `AvatarVideo`) as the interactive hero background.
-   **Reference**: See `src/App.tsx` for embedding examples.

### 5. Deploy & Verify
Finalize the production build:
1.  **Build**: `npm run build` (runs `tsc` + `vite build`).
2.  **Preview**: `npm run preview` to test the production bundle locally.
