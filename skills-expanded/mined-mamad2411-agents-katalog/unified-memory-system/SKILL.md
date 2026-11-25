---
name: unified-memory-system
description: "Gabungan 3 lapis memori: (1) Obsidian vault = memori permanen lintas sesi/AI, (2) MCP Memory = knowledge graph untuk entitas & relasi, (3) Token compression = hemat 70%+ token. AI wajib pakai ini SEBELUM mulai kerja (recall) dan SETELAH milestone (log). Lintas AI: Claude, CodeBuddy, Cline, Codex, Trae, Hermes, Orca, semua."
---

# Unified Memory System (3 Lapis — Hemat Token + Auto-Recall)

> **PRINSIP**: AI gak perlu habis token untuk "mengingat" sesuatu. Tiap sesi = recall 3 detik → kerja → log 3 detik. Token dipakai untuk kerja, bukan re-explain konteks.

## Arsitektur

```
┌─────────────────────────────────────────────┐
│           AI Agent (Claude/CodeBuddy/dll)   │
│                                              │
│  1. RECALL (sebelum kerja)                  │
│     ├─ Obsidian: python3 obsidian-log.py recall "project"  │
│     └─ MCP Memory: search_nodes("keyword")  │
│                                              │
│  2. WORK (pakai token untuk kerja,          │
│     bukan untuk re-explain konteks)          │
│                                              │
│  3. LOG (setelah milestone)                  │
│     ├─ Obsidian: log/decision/daily         │
│     └─ MCP Memory: create_entities/relations │
│                                              │
│  4. COMPRESS (tiap turn)                     │
│     └─ [Project: X | State: Y | Next: Z]    │
└─────────────────────────────────────────────┘
```

## Lapis 1: Obsidian Vault (Memori Permanen)

**Vault**: auto-detect dari `~/Library/Application Support/obsidian/obsidian.json`
**CLI**: `python3 ~/.agents/scripts/obsidian-log.py <cmd>`

| Kapan | Cmd | Untuk Apa |
|-------|-----|-----------|
| **SEBELUM mulai proyek** | `recall "<project>"` | Load konteks: keputusan, progress, blocker |
| **Setelah selesai milestone** | `log <Project> "<summary>"` | Catat apa yang selesai |
| **Setelah keputusan arsitektural** | `decision <Project> "<title>" "<body>"` | Catat keputusan + alasan |
| **Catatan harian cepat** | `daily "<text>"` | Append ke daily note |
| **Buat note referensi** | `note "<Title>"` (body via stdin) | Note di 02 - Notes |

### Protokol Wajib

1. **Sebelum mulai tugas di proyek** → `recall "<nama proyek>"` DULU. Jangan tanya user "apa konteksnya".
2. **Setelah milestone/keputusan** → `log` + `decision`. AI berikutnya bisa lanjut tanpa restart dari nol.
3. **Handoff** → pastikan log terakhir berisi state cukup untuk AI berikutnya.
4. **Jangan log trivia** (typo fix, rename variabel). Log = keputusan, milestone, blocker, state.

## Lapis 2: MCP Memory (Knowledge Graph SHARED Semua AI)

**Server**: `mcp-server-memory` — dikonfigurasi di SEMUA AI dengan file yang sama:
`~/.agents/memory/memory.json` (env `MEMORY_FILE_PATH`). Claude, Codex, Hermes, Cline (standalone + VSCode) menulis ke graph yang sama → memori tidak terpecah.

**Via CLI (hemat token, works di AI mana pun termasuk yang tanpa MCP — Trae dll):**
| Kapan | Cmd | Untuk Apa |
|-------|-----|-----------|
| **Sebelum mulai** | `obsidian-log.py recall "<q>"` | vault + graph SEKALIGUS dalam 1 perintah |
| **Setelah entitas baru** | `obsidian-log.py mcp-log <Entity> <Type> "<obs>"` | Simpan entity+observation |
| **Cari di graph saja** | `obsidian-log.py mcp-recall "<q>"` | Hasil graph ringkas (maks 8) |
| **Inspeksi graph** | `obsidian-log.py entities` | Count per type + entitas terbesar (JANGAN read_graph penuh) |

**Via MCP tool (kalau server tersedia):** `search_nodes` > `read_graph` (hemat token). `create_entities` hanya untuk relasi antar entitas — untuk log harian cukup `mcp-log`.

### Entity Types

- `Project` — nama proyek, status, tech stack
- `Decision` — keputusan arsitektural + alasan
- `Blocker` — masalah yang belum solved
- `Tool` — library/service/CLI yang dipakai
- `Pattern` — solusi yang berulang

### Relation Types

- `uses` — Project uses Tool
- `decided` — Project decided Decision
- `blocked_by` — Project blocked_by Blocker
- `solved_by` — Blocker solved_by Pattern
- `related_to` — Entity related_to Entity

## Lapis 3: Token Compression (Hemat 70%+)

### Auto-Compress Tiap Turn

Setelah tiap turn, compress state jadi 1 baris:

```
[Project: <name> | State: <state> | Done: <X> | Next: <Y> | Blockers: <Z>]
```

Contoh:
```
[Project: GenZysFleetOps | State: Auth-module-80% | Done: JWT+RBAC | Next: Refresh-token | Blockers: none]
```

### Token Rules (Wajib)

1. **Zero fluff** — no "Sure", "Here is", "Let me explain"
2. **Diff-only** — never output full file kalau cuma 5 baris berubah
3. **Surgical reads** — grep/line-range, never read 2000-line file for 1 function
4. **Recall > re-ask** — kalau lupa, recall dari Obsidian/MCP Memory, jangan tanya user ulang
5. **Log > re-do** — kalau selesai, log ke Obsidian, jangan biarkan AI berikutnya redo
6. **Compress state** — tiap turn, ringkas jadi 1 baris state string

## Integrasi Lintas AI

Skill ini universal untuk semua AI agent:

| AI Agent | Cara Akses |
|----------|------------|
| Claude | `/skill obsidian-memory` atau baca `~/.claude/skills/obsidian-memory` |
| CodeBuddy | Skill `obsidian-memory` di `~/.codebuddy/skills/` |
| Cline | Skill `obsidian-memory` di `~/.cline/skills/` |
| Codex | Skill `obsidian-memory` di `~/.codex/skills/` |
| Orca | Skill `obsidian-memory` di `~/.orca/skills/` |
| Hermes | Skill `obsidian-memory` di `~/.hermes/skills/` |
| Trae | Skill `obsidian-memory` di `~/.trae/builtin_skills/` |
| Gemini | Skill `obsidian-memory` di `~/.gemini/skills/` |

## Quick Start (AI: jalankan ini di awal sesi)

```bash
# 1. Cek vault Obsidian
python3 ~/.agents/scripts/obsidian-log.py status

# 2. Recall konteks proyek (ganti <project> dgn nama proyek)
python3 ~/.agents/scripts/obsidian-log.py recall "<project>"

# 3. Search knowledge graph
# (via MCP tool: search_nodes("<project>"))
```

## Quick Log (AI: jalankan ini di akhir sesi/milestone)

```bash
# 1. Log progress ke Obsidian
python3 ~/.agents/scripts/obsidian-log.py log <Project> "<apa yang selesai>"

# 2. Catat keputusan kalau ada
python3 ~/.agents/scripts/obsidian-log.py decision <Project> "<title>" "<alasan>"

# 3. Simpan entity ke MCP Memory
# (via MCP tool: create_entities([...]))
```

## Sinkronisasi Otomatis

Setiap kali `obsidian-log.py log` dipanggil, juga bisa trigger `update_memory` (CodeBuddy built-in) untuk simpan ke knowledge base CodeBuddy juga. Double storage = gak hilang.

## Yang Tidak Boleh Dilakukan

- JANGAN baca seluruh vault Obsidian (token bocor) — selalu `recall` dengan keyword spesifik
- JANGAN dump `read_graph` ke conversation kecuali perlu — gunakan `search_nodes` dulu
- JANGAN log trivia — log hanya keputusan, milestone, blocker, state
- JANGAN tanya user "apa konteks proyek" sebelum `recall` — coba dulu, baru tanya kalau kosong
