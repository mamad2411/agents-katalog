---
name: agent-sharpen
description: "Agent'in bilgi dagarcigini keskinlestir — web'den ve kaynaklardan arastir, knowledge dosyalarini doldur/guncelle. Triggers: agent-sharpen, agent sharpen, bilgi topla, keskinlestir, pekistir."
argument-hint: "{agent-id} [--topic konu] [--deep]"
---

# /agent-sharpen — Knowledge Sharpening

Agent'in kendi alaninda bilgi toplamasini ve knowledge dosyalarini doldurmasini saglar.

## Process

### Phase 0 — Pre-flight
- Agent dizini mevcut mu kontrol et (AGENT.md, knowledge/_index.md)
- Yoksa → `/agent-setup` once calistir
- Agent'in Boundaries section'ini oku — arastirma sinirlarini belirle

### Phase 1-7 — Execution

1. **Agent'i yukle**: `agents/{category}/{agent-name}/AGENT.md` oku
2. **Index oku**: `knowledge/_index.md` — hangi konular var, hangisi bos/eksik
3. **Arastirma plani olustur**: Bos veya eksik konulari listele, oncelik sir
4. **Arastir** (her konu icin):
   - Web'den arastir (fetch, context7, github)
   - Referans repolari tara (references/ dizini)
   - Mevcut kod/config'den pattern cikar
   - Sonuclari `memory/learnings.md`'ye kaydet (tarih + kaynak + ozet)
5. **Knowledge dosyasi yaz/guncelle** (opus ile):
   - Yeterli learning biriktiyse ilgili `knowledge/{topic}.md` dosyasini olustur/guncelle
   - Her dosyanin basina: `last_updated`, `refined_by`, `confidence` ekle
   - Sadece dogrulanmis, kaynakli bilgi yaz
6. **Index guncelle**: `_index.md`'ye yeni/guncellenen dosyalari ekle
7. **Refinement log**: `memory/refinements.md`'ye entry ekle

## When to Use
- Agent ilk setup edildikten sonra (knowledge bos)
- Yeni bir alan/konu eklenmesi gerektiginde
- Bilgiler eskidiyse (3+ ay guncellenmemis)
- `--deep` flag: daha kapsamli arastirma, daha fazla kaynak

## When NOT to Use
- Agent'in yapisi degismesi gerekiyorsa (→ `/agent-setup`)
- Sadece mevcut bilgiyi rafine etmek icin (→ `/agent-refine`)
- Agent'in alani disinda bir konuda (→ Boundary ihlali)

## Boundary Enforcement
- Agent sadece kendi AGENT.md'deki `Boundaries` section'inda tanimli alanlarda bilgi toplar
- Bridge alanlarinda sadece kesisim noktasindaki bilgiyi yazar
- Boundary disina cikarsa → dur, uyar, bilgiyi yazma

## Red Flags
- Kaynak belirsiz veya dogrulanamaz — yazma
- Bilgi baska agent'in alaniyla %80+ cakisiyor — bridge mi gercek cakisma mi kontrol et
- Cok fazla genel bilgi, az spesifik — daha dar odaklan

## Error Handling
- Web arastirma basarisizsa (rate limit, timeout) → mevcut kod/config'den pattern cikar, web'i atla
- Kaynak dogrulanamiyorsa → `confidence: low` ile yaz, sonraki refine'da tekrar degerlendir
- Boundary disina cikildiysa → yazilan bilgiyi sil, uyar

## Verification
- [ ] En az 1 knowledge dosyasi olusturuldu/guncellendi
- [ ] Her dosyada last_updated ve kaynak bilgisi var
- [ ] _index.md guncellendi
- [ ] learnings.md'ye en az 1 entry eklendi
- [ ] Boundary ihlali yok
