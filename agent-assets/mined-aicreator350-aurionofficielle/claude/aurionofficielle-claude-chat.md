# AURION CHAT — CONTEXTE SPÉCIFIQUE

## URL
https://chat-aurion1.vercel.app

## ARCHITECTURE
- Entry : src/main.tsx → src/App.tsx → src/components/aurion-chat/AurionChatInterface.tsx (1923 lignes)
- 64 fichiers .tsx, ~954 KB total — outil le mieux structuré
- API : api/chat.ts (SSE streaming), api/mcp.ts (18 MCP tools), api/memory.ts, api/tts.ts, api/stt.ts, api/generate-media.ts, api/execute-code.ts, api/proxy.ts, api/projects.ts, api/sync.ts
- Lib partagée : api/_lib/ (auth, cors, rate-limit, usage-tracker)

## MCP TOOLS (18)
web_search (Brave), semantic_search (Exa), find_similar (Exa), deep_research (Exa),
read_url (Firecrawl), execute_code (E2B), generate_image (Replicate),
text_to_speech (ElevenLabs), memory_load/save (Mem0), plus outils fichiers/analyse

## FEATURES FONCTIONNELLES
- Streaming SSE avec tous les modèles OpenRouter
- Artifacts : code, Sandpack preview, Mermaid, KaTeX, Recharts
- Slash commands : /search, /run, /image, /video, etc.
- Voice : Groq Whisper STT (api/stt.ts) + ElevenLabs TTS (api/tts.ts)
- Upload : PDF (Tesseract OCR + PDF.js), Office (mammoth + SheetJS + PPTX parser)
- Projets : Supabase CRUD via api/projects.ts
- Mémoire : Mem0 + Supabase fallback
- Médias : Image + vidéo generation

## USAGE TRACKER (CHANGEMENT RÉCENT)
- tools-deploy/chat/api/_lib/usage-tracker.ts était un Map() en mémoire (perdu au cold start)
- FIXÉ : maintenant persiste dans Supabase usage_quotas table avec fallback cache local
- trackUsage() est maintenant ASYNC → tous les callers doivent await

## MODÈLES DISPONIBLES
Claude Sonnet 4, Claude 3.5 Sonnet, GPT-4o, GPT-4o-mini, Gemini Flash, DeepSeek R1,
Llama 3.3 70B (free), Gemma 3 27B (free), Qwen3 Coder (free), Mistral Small (free)

## TESTER
1. Ouvrir https://chat-aurion1.vercel.app
2. Envoyer un message → vérifier streaming SSE
3. /search test → vérifier MCP tool call
4. Upload un PDF → vérifier OCR
5. Console DevTools = zéro erreur
