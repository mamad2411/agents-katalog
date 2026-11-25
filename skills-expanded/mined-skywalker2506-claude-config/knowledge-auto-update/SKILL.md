---
name: knowledge-auto-update
description: "Agent-local knowledge dosyalarini gorev sonunda ogrenilenlerle guncelle. Triggers: knowledge update, agent knowledge refresh, ogrendigini kaydet."
argument-hint: "[agent-id] [--auto]"
---

# /knowledge-auto-update — Per-Agent Knowledge-First Auto-Update

Bir agent non-trivial bir gorevi bitirdikten sonra kendi `knowledge/` dizinini (sadece kendisininkini) ogrendikleriyle gunceller. Patterns, trial-and-error dersleri, domain bulgulari — hepsi ekleme (additive patch) seklinde.

## Kapsam (zorunlu)

**Agent-local only.** Bu skill SADECE `~/Projects/claude-config/agents/<agent>/knowledge/*.md` altinda yazar.

- Global skill olusturma **YASAK** (SessionStart sisirir — Video 1 / Video 4 uyarisi)
- Baska agent'in knowledge'ini degistirme
- `~/.claude/` altina dogrudan yazma — install.sh ile mirror edilecek
- CLAUDE.md / charter / harness — dokunma

Manuel muadiller: `agent-sharpen` (web'den arastir), `agent-refine-knowledge` (Opus ile kalite review). Bu skill otomatik "gorevden ogrenilen" yakalayici; onlarin yerini tutmaz.

## Tetikleme modlari

| Mod | Nasil |
|-----|-------|
| Manuel | `/knowledge-auto-update <agent-id>` — kullanici veya Jarvis cagirir |
| Auto | Agent kendini `>10 tool call` sonrasi self-trigger — opsiyonel hook wiring (su an devre disi) |

Auto hook wiring bu skill kapsamina **dahil degil** — ayri karar. Su an sadece manuel + explicit trigger.

## Akis

### 1. Agent tespit

- Argument verildiyse `<agent-id>` onu kullan
- Yoksa son dispatch edilen agent'i `/tmp/watchdog/current_dispatch.json`'dan oku
- Hic yoksa → kullaniciya sor, dur

### 2. Gorev ozeti cikar

Son turn'deki (veya son dispatch'teki) tool call'lari ve sonuclari tara:
- Hangi dosyalara dokunuldu?
- Hangi komutlar basarisiz oldu, neden?
- Hangi non-obvious pattern kullanildi?
- Hangi domain gercegi kesfedildi? (API quirk, lib davranisi, repo yapisi)

Max 8 tool call bu adimda.

### 3. Kategorize et

Bulgulari 3 bucket'a ayir:

| Bucket | Ornek |
|--------|-------|
| **Patterns** | "Bu tur task'ta once X, sonra Y yap" |
| **Trial-and-error** | "Z denedim, W yuzunden patladi, V ile calisti" |
| **Domain facts** | "Library A'nin method B'si default'u C degil D" |

Trivial olani at (1 satirlik obvious seyleri kaydetme).

### 4. Safety guard

Her bulguyu yazmadan once kontrol et — asagidakilerden biri varsa **reddet**:

- `rm -rf`, `sudo rm`, `dd if=` gibi destructive komut ornekleri
- `curl ... | bash`, `wget ... | sh` gibi remote-exec patterns
- API key, token, password, secret deger (env var adi OK, deger DEGIL)
- Musteri/kisisel veri (email, telefon, kimlik)
- Baska kullanici/agent isimleri + kisisel yorumlar

Reddet = kaydetme + kullaniciya tek satir bildir: `[GUARD] rejected N entries (reason: secret|destructive|pii).`

### 5. Additive patch

`~/Projects/claude-config/agents/<agent>/knowledge/` altinda:

- Uygun dosya varsa (ornek `patterns.md`, `lessons.md`, `domain.md`) → dosyanin sonuna **ekle**, ustune yazma
- Yoksa yeni dosya olustur: `knowledge/<kategori>.md`
- Her yeni entry'e tarih + gorev kisa ozeti prefix'i: `<!-- 2026-04-23 — task: {ozet} -->`

### 6. Index guncelle

`knowledge/_index.md` dosyasini ac:
- Yeni dosya eklendiyse → index'e 1 satir ekle
- Mevcut dosyaya entry eklendiyse → (opsiyonel) entry count guncelle
- 200 satir limitini koru — asarsa kullaniciya `agent-refine-knowledge` oner

### 7. Rapor

```
## Knowledge Auto-Update — <agent-id>

- Patterns: +N entries → patterns.md
- Lessons: +M entries → lessons.md
- Domain: +K entries → domain.md
- Rejected by guard: R (reasons: ...)
- Index: updated

Next: install.sh gerekirse calistir (runtime mirror icin).
```

## Kurallar

- Max 15 tool call toplam
- ASLA global skill/agent/plugin olusturma
- ASLA baska agent'in klasorune yazma
- Safety guard **opt-out edilemez**
- Dil: entries Turkce+Ingilizce karisik OK (mevcut knowledge stiline uy)
- Duplicate kontrolu yap — ayni pattern zaten varsa ekleme, skip

## When NOT to Use
- Trivial gorev (<10 tool call, cok net yol) — ogrenilecek yeni birsey yok
- Sadece okuma yapan gorev (investigation) — patterns disinda kayit sey yok
- Hatali/yarida kalan gorev — yanlis dersler yazmaktansa atla

## Red Flags
- Ayni entry iki iterasyonda tekrar ekleniyor → duplicate check calismiyor, dur
- Guard > actual saves oranı yuksek → prompt secret/dangerous icerikle kirli
- Knowledge dosyasi 500 satiri astı → `agent-refine-knowledge` oner, ekleme yapma

## Error Handling
- Agent klasoru yok → dur, `agent-setup` oner
- Write izni yok → dur, path'i kullaniciya goster
- Guard tetiklendi → entry'yi sessizce at, final raporda say

## Verification
- [ ] Sadece hedef agent'in knowledge/ altina yazildi
- [ ] Safety guard calisti, reject sayisi raporlandi
- [ ] _index.md guncel
- [ ] Global scope'a dokunulmadi (skill/plugin/agent yaratilmadi)
- [ ] Duplicate kontrol yapildi
