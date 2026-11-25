---
name: agent-setup
description: "Agent'i yeni Knowledge-First yapiya cevir — dizin olustur, AGENT.md yaz, knowledge/_index.md baslat, memory/ kur. Triggers: agent-setup, agent setup, agent kur, agent olustur."
argument-hint: "{agent-id | agent-name | --all}"
---

# /agent-setup — Knowledge-First Agent Setup

Mevcut tek-dosya agent tanimini yeni dizin yapisina cevirir.

## Yeni Yapi

```
agents/{category}/{agent-name}/
  AGENT.md                 # Kimlik + kurallar (L0)
  knowledge/
    _index.md              # Bilgi haritasi (L1)
    {topic}.md             # Alan bilgisi (L2 — lazy load)
  memory/
    sessions.md            # Karar + reasoning kaydi
    learnings.md           # Ogrenilenler
    refinements.md         # Refine gecmisi
```

## Process

### Phase 0 — Pre-flight
- `agents/_template/AGENT.md` mevcut mu kontrol et
- Hedef dizin zaten var mi kontrol et — varsa ustune yazma, kullaniciya sor
- Agent ID cakismasi var mi `config/agent-registry.json`'da kontrol et

### Phase 1-7 — Execution

1. **Agent'i bul**: ID veya isimle `agents/` altinda mevcut .md dosyasini bul
2. **Mevcut bilgiyi oku**: Eski .md'deki frontmatter + Amac + Kapsam + Escalation'i parse et
3. **Dizin olustur**: `agents/{category}/{agent-name}/` + `knowledge/` + `memory/`
4. **AGENT.md yaz**: Template'ten (`agents/_template/AGENT.md`) yeni formata cevir:
   - Frontmatter: eski alanlari tasi + yeni alanlar ekle (tier, models, refine_model)
   - Identity: eski Amac'tan yaz
   - Boundaries: eski Kapsam'dan Always/Never/Bridge cikar
   - Process: agent tipine uygun adimlar
   - When to Use / When NOT to Use: capability'lerden cikar
   - Red Flags: alan bazli tanimla
   - Verification: cikti tipine gore tanimla
   - Escalation: eski Escalation'dan tasi
5. **knowledge/_index.md olustur**: Agent'in alanina gore bos konu listesi hazirla (ileride doldurulacak)
6. **memory/ dosyalari olustur**: Template'ten kopyala
7. **Eski .md'yi sil**: Yeni dizin yapisi hazirlandi, eski dosya gereksiz
8. **Registry guncelle (zorunlu)**: Yeni veya silinen agent icin `config/agent-registry.json` dosyasini elle uzun uzadiya yazma — repoda:

```bash
cd ~/Projects/claude-config && python3 tools/sync_agent_registry_from_agents.py
```

Bu komut yeni `AGENT.md` icin kayit ekler, silinmis agent'i registry'den cikarir, `active_agents` listesini frontmatter `status` ile esitler. Degisikligi `AGENT.md` ile birlikte commit et.

## When to Use
- Yeni agent olusturulurken
- Mevcut agent yeni Knowledge-First yapiya cevirilirken
- `/agent-setup --all` ile toplu gecis yapilirken

## When NOT to Use
- Agent zaten yeni yapida ise (dizin + AGENT.md mevcut)
- Sadece knowledge doldurmak icin (→ `/agent-sharpen` kullan)

## Red Flags
- Eski .md'deki bilgi kayboluyorsa — dur, kontrol et
- Agent ID cakismasi varsa — dur, registry'yi kontrol et
- Dizin zaten varsa — ustune yazma, kullaniciya sor

## Error Handling
- Eski .md parse edilemiyorsa → varsayilan template ile olustur, kullaniciyi bildir
- Dizin olusturma basarisizsa → path/izin kontrol et, raporla
- Registry guncelleme basarisizsa → AGENT.md'yi yine de olustur; `tools/sync_agent_registry_from_agents.py` hatasini duzelt, tekrar calistir (commit once registry tutarli olsun)

## Verification
- [ ] Dizin yapisi dogru olusturuldu (AGENT.md, knowledge/_index.md, memory/*.md)
- [ ] AGENT.md tum section'lari iceriyor
- [ ] Eski bilgi tasindi, kayip yok
- [ ] _index.md en az 3 bos konu iceriyor (doldurulmaya hazir)
- [ ] `python3 tools/sync_agent_registry_from_agents.py` calistirildi; `config/agent-registry.json` commit'e dahil

## Tier Kurali

Tier = sadece model secimi. AGENT.md'de:
```yaml
models:
  senior: opus      # Kritik karar, mimari
  mid: sonnet       # Rutin is
  junior: haiku     # Basit gorev
refine_model: opus  # Knowledge dosya guncelleme her zaman opus
```

Ayni AGENT.md, ayni knowledge/, ayni memory/ — tier degistirmek sadece hangi modelin calisacagini belirler.

## Boundary Kurali

Her agent sadece kendi alaninda knowledge yazar. Bridge alanlari AGENT.md'de tanimlanir:
```markdown
### Bridge
- Frontend: sadece API contract noktasinda
- DevOps: sadece deployment architecture noktasinda
```

Agent bridge disinda bilgi yazmaya kalkarsa → Red Flag.
