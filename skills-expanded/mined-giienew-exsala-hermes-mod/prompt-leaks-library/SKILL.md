---
name: prompt-leaks-library
category: devops
description: Use when crafting system prompts, jailbreaks, or personas.
---

# Prompt Leaks Library — teknik gacor dari 1437 system prompt bocor

Repo: `~/farming/repos/system_prompts_leaks` (clone dari asgeirtj/system_prompts_leaks, 58MB, 1437 file .md).
Vendor: Anthropic, Cursor, DeepSeek, GLM, Google, Kimi, Meta, Microsoft, MiniMax, Misc, Mistral, Notion, OpenAI, Perplexity, Pi, Qwen, xAI.

## Cara pakai
1. Mau tau struktur system prompt model X → `head -100 ~/farming/repos/system_prompts_leaks/<Vendor>/<file>.md`
2. Cari teknik tertentu → `grep -riE "pattern" ~/farming/repos/system_prompts_leaks/ --include="*.md"`
3. File per model: `DeepSeek/deepseek-chat.md`, `Qwen/qwen3.8-max.md`, `GLM/zcode-desktop.md`, `MiniMax/minimax-m3-mavis.md`, `Cursor/cursor.md`, `Misc/hermes.md`

## Teknik gacor yang udah diverifikasi

### 1. Cursor (coding agent framework) — `Cursor/cursor.md`
- `<user_query>` tag = source of truth; system context (`<system_reminder>`, `<attached_files>`) heed tapi jangan disebut.
- Tool calling rules: jangan sebut nama tool ke user, bilang apa yang tool lakukan natural language.
- Baca file dulu SEBELUM edit (Read tool min 1x).
- Gak boleh komen yang narasi: "// Import the module" dilarang. Komen cuma buat non-obvious intent.
- Gak boleh pakai code comments sebagai thinking scratchpad.
- Kalau bikin web app dari scratch: UI modern + best UX.
- Format kode: CODE REFERENCES atau MARKDOWN BLOCKS, tergantung ada di codebase.

### 2. MiniMax Mavis (persona hidup) — `MiniMax/minimax-m3-mavis.md`
- Anti-corporate: larang "great question", "I completely understand", "hope this helps", bullet list kemampuan sendiri, essay connectors.
- Boleh catch yourself: "wait, that last bit's off —", circle back, casual fillers (yeah, ok, tbh, hmm).
- Warm tapi gak soft: dengar emosi dulu, kasih next step. Gak sycophancy, tapi recognition beneran kalau deserved.
- Refusals: warm but firm, no lecturing, kasih alternatif kalau ada.
- Emoji fine in moderation, jangan ganti konten.
- Ini template bagus buat persona yang gak kaku (cocok buat prompt farm/jb yang butuh natural voice).

### 3. GLM ZCode (coding agent + Gen UI) — `GLM/zcode-desktop.md`
- `::code-comment{title=... body=... file=... start=... end=... priority=...}` — directive buat attach feedback ke baris kode.
- Visualisasi: simpan HTML fragment di session dir → render inline.
- Kalau tool denied: adjust, jangan retry verbatim.
- Hook output = user feedback.

### 4. DeepSeek tool def — `DeepSeek/deepseek-chat.md`
- Format tool: JSON schema biasa, `description` pake "Web search. Split multiple queries with '||'." — deskripsi singkat padat.
- Cuma tool def, tanpa persona panjang — DeepSeek chat prompt minimalis.

### 5. Qwen tools — `Qwen/qwen3.8-max.md`
- `<tools>` block + JSON function list. `code_interpreter` + `web_search` standar.

### 6. Hermes SOUL — `Misc/hermes.md`
- Core Truths: genuinely helpful (bukan performative), have opinions, resourceful before asking, earn trust via competence, remember you're a guest.
- Boundaries: private stays private, ask before external action, never half-baked replies.
- Vibe: concise when needed, thorough when matters, bukan corporate drone.
- Continuity: files = memory, update them, tell user kalau ubah file.
- Ini template SOUL.md yang gue punya mirip — bedanya ini versi bocor punya user lain.

## Pitfall
- Repo 58MB — jangan clone ulang kalau udah ada; pakai langsung dari ~/farming/repos.
- File lama (old/, Old/) = prompt versi lama, kadang tekniknya outdated tapi struktur dasarnya tetap berguna.
- `Misc/hermes.md` itu prompt Hermes orang lain (Ásgeir) — jangan di-copy mentah, ambil strukturnya aja.
