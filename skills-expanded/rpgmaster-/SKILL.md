# RpgMaster - Cursor & Agent Rules (.cursorrules)

You are an expert full-stack developer working on **RpgMaster**, an AI-powered tabletop role-playing game with an AI Game Master and D&D 5.2 rules (CC-BY-4.0).

---

## 1. LLM TEXT ENGINE (OLLAMA CLOUD & GEMMA 4)

*   **Official Support**: The project natively supports both **Local Ollama** (default: `mistral:7b` at `http://localhost:11434`) AND **Ollama Cloud** (direct direct access on `https://ollama.com` via an API key).
*   **Frontier Model**: The official remote model is `gemma4:31b` (tagged `cloud`).
*   **Authentication**: When using Ollama Cloud, authentication must pass through the `OLLAMA_API_KEY` environment variable as a Bearer token (`Authorization: Bearer <key>`).
*   **Timeout Rules**:
    *   **Connection Timeout**: Fast (`3.0s`) to quickly detect offline or network failures and trigger local/fallback states.
    *   **Read Timeout**: Generous (`240.0s` / 4 minutes) to leave enough time for large models like Gemma 4 to think, reason, and generate extensive, high-quality narrative content.
*   **Resilience & Feedback**: Never block the main thread. Always support async calls. If Ollama is offline or times out, the `GMAgent` absorbs the error, returns a fallback narrative (`_FALLBACK_NARRATION`), and the `ActionPipeline` pushes a user-friendly error bandeau via the WebSocket channel (using `EventType.ERROR`) without raising a fatal error that freezes the gameplay session.

---

## 2. TECH STACK & SYSTEM CONTEXT

| Layer | Technology | Key Constraints / Patterns |
|---|---|---|
| **Backend** | Python 3.11+ / FastAPI | Async, app factory in `backend/app/main.py` |
| **Frontend** | Vue 3 / TypeScript | Composition API, `<script setup lang="ts">`, Pinia, Vue Router |
| **CSS** | TailwindCSS v4 | `@theme` tokens + `.rpg-*` utility classes in `src/assets/main.css` |
| **LLM Voice** | Voxtral 4B TTS | Via vLLM-Omni (NOT Ollama) on port 8091 (optional, async) |
| **TTS Local** | Kokoro-ONNX | Python 3.11 subprocess in `tts_service/` (voice parameters) |
| **DB** | SQLite | Async via SQLAlchemy (aiosqlite) + Alembic migrations |
| **WebSockets** | Native FastAPI | `/ws/game/{session_id}` & `/ws/dialogue/{session_id}/{persona_id}` |

---

## 3. ARCHITECTURE PRINCIPLES

1.  **Authoritative Rules Engine**: The `backend/app/engine/` module contains **pure logic with zero I/O** (no DB, no network, no async). The LLM *never* resolves dice rolls, attacks, or mechanics—it only narrates them.
2.  **Structured JSON output**: LLM agents must return validated JSON matching Pydantic schemas, never unformatted free text.
3.  **Non-blocking Voice Layer**: Speech synthesis is fully async and never blocks gameplay.
4.  **No complex SQL relations for State**: Campaign/session state is stored as a validated Pydantic JSON blob in `Campaign.dossier`. Do not create new relational tables.
5.  **Concurrent Session Lock**: Avoid race conditions by ensuring WebSocket handlers do not instantiate direct SQLAlchemy sessions—always reuse the injected `db` and manage locks cleanly.

---

## 4. DESIGN SYSTEM (DARK FANTASY)

*   **Palette (Tokens)**: Use `var(--color-*)` custom tokens in CSS. Do not hardcode hex values.
    *   Accents: `ember` (GM / CTA / Narratives), `gold` (Active Player / Selection / Decisions), `arcane` (AI Companions / Magic), `teal` (NPCs / Allies), `blood` (Enemies / Danger / Low HP), `crit` (Critical Rolls - Gold star).
*   **Typography**:
    *   Titles: `Cinzel` (`--font-display`) uppercase + letter-spacing.
    *   Narration: `Fraunces` (`--font-serif`) `text-wrap: pretty` + high line height.
    *   Metadata / Stats: `JetBrains Mono` (`--font-mono`).

---

## 5. ANTI-PATTERNS TO AVOID

*   **NO** block-calling LLM inside WebSocket connection loops. Always run heavy tasks asynchronously (`asyncio.create_task()`).
*   **NO** API key exposure. Never pass `OPENAI_REALTIME_API_KEY` or `OLLAMA_API_KEY` to the frontend client. All AI and real-time OpenAI/Ollama traffic must transit securely through backend WebSockets.
*   **NO** I/O or async functions in `backend/app/engine/`. Keep it 100% testable and pure.
*   **NO** Vue Options API or hardcoded inline colors in frontend templates.
