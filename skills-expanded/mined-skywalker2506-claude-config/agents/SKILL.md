---
name: agents
description: "Tum agent'lari gruplu listele — aktif/pool, kategori, model, capability. Triggers: agents, agent listesi, agent grupları, hangi agentlar var, agent seçenekleri."
argument-hint: "[active | pool | all | <kategori>]"
---

# /agents — Agent Listesi

`config/agent-registry.json` + `agents/` dizininden tum agent'lari gruplu goster.

## Cikti formati

Her kategori icin tablo:

```
## 🧠 Orchestrator & Sistem (A)
| ID  | İsim              | Model   | Durum  | Capabilities           |
|-----|-------------------|---------|--------|------------------------|
| A0  | Jarvis            | sonnet  | active | session, dispatch, UX  |
| A1  | Lead Orchestrator | sonnet  | active | dag, multi-agent       |
...
```

Alt kısımda özet:
```
Toplam: 134 agent (30 active / 104 pool)
Kategoriler: 15
```

## Akis

### 1. Registry oku
`~/.claude/config/agent-registry.json` oku:
- `categories` → kategori listesi + prefix + description
- `active_agents` → aktif agent ID listesi

### 2. Agent dosyalarini oku
`~/.claude/agents/` dizinini tara (ya da `$(ls ~/.claude/agents/ | head -50)` ile listele).

Her agent .md dosyasinin frontmatter'indan al:
- `name`, `id`, `primary_model`, `capabilities`, `effort`

### 3. Grupla ve goster

Kategorilere gore sirala (prefix sirasina gore: A, B, C, D...):

- Arguman `active` → sadece active_agents listesindekiler
- Arguman `pool` → sadece pool'dakiler
- Arguman `all` veya bos → hepsi (once active, sonra pool)
- Arguman bir kategori ismi (orn. `backend`, `orchestrator`) → sadece o kategori

### 4. Renklendirme / isaretleme
- Active agent: normal
- Pool agent: _(pool)_ italik olarak belirt
- Dispatcher/Orchestrator (A prefix): **bold** ID

## Kurallar
- Max 10 tool call
- Agent .md okuma yerine registry + ls kombinasyonu kullan (daha hizli)
- Frontmatter okumak icin agent dosyasinin sadece ilk 20 satirini oku
- Hata varsa (dosya yoksa) skip et, saymaya devam et

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
