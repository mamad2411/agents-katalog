---
name: agent-refine-knowledge
description: "Agent'in AGENT.md ve knowledge dosyalarini opus ile review et, kaliteyi artir, gereksizi at, eksigi tamamla. Triggers: agent-refine, agent refine, agent rafine, bilgi rafine."
argument-hint: "{agent-id} [--scope agent|knowledge|all]"
---

# /agent-refine — Knowledge Refinement

Agent'in tum dosyalarini opus ile review eder, kaliteyi artir.

## Process

### Phase 0 — Pre-flight
- Agent dizini mevcut ve knowledge dosyalari dolu mu kontrol et
- Knowledge bos ise → kullaniciya "once /agent-sharpen calistir" de, refine'i iptal et
- Web arastirma YAPMA — mevcut dosyalari oldugu gibi al, dis kaynak ekleme

### Phase 1-5 — Execution

1. **Agent dizinini oku**: AGENT.md + knowledge/*.md + memory/*.md
2. **Kalite audit** (opus ile):
   - AGENT.md: Identity 1-3 cumle mi? Boundaries keskin mi? Process gate'li mi? Output Format var mi?
   - knowledge/*.md: Bilgi guncel mi? Kaynakli mi? Tekrar var mi? Belirsiz ifade var mi ("best practices", "uygun sekilde" gibi)?
   - memory/learnings.md: Knowledge'a tasinmasi gereken learning var mi?
   - **Anti-pattern kontrolu**: Vague imperatives, missing boundaries, placeholder outputs, silent assumptions (bkz. anti-patterns.md)
3. **Aksiyonlar**:
   - Gereksiz/tekrar bilgiyi sil
   - Eksik section'lari tamamla (ozellikle: Output Format, When NOT to Use, Error Handling)
   - Belirsiz ifadeleri somut talimatlara cevir
   - Learnings → knowledge promosyonu yap (yeterli birikimde)
   - Boundary disina tasmis bilgiyi kaldir
4. **Refinement log**: `memory/refinements.md`'ye ne degisti, neden, kim (model) yapti
5. **Index guncelle**: Silinen/eklenen dosyalari `_index.md`'de yansit

## Refine Model Kurali

**Knowledge dosyalarini dusunup guncellemek HER ZAMAN opus ile yapilir.**
Bu dosyalar surekli kullanilacak — kalite kritik. Tier ne olursa olsun refine = opus.

**Opus sadece review eder** — mevcut dosyalari analiz eder, yeniden yazar, gereksizi atar.
Web arastirmasi, dis kaynak ekleme, sharpen islemi YAPILMAZ.
Araştirma gerekiyorsa → kullaniciya `/agent-sharpen` one calistirmasini soy, dur.

## When to Use
- Knowledge dosyalari dolduktan sonra kalite artirma
- Duzensiz/dagink bilgiyi yapilandirma
- Periyodik bakim (ayda 1)
- Agent performansi dusukse (bilgi kalitesi sorunu olabilir)

## When NOT to Use
- Knowledge bos ise (once `/agent-sharpen`)
- Agent yapisi degismesi gerekiyorsa (→ `/agent-setup`)

## Scope Secenekleri
- `--scope agent`: Sadece AGENT.md refine
- `--scope knowledge`: Sadece knowledge/*.md refine
- `--scope all` (default): Her sey

## Error Handling
- Dosya okunamazsa → atla, raporla, diger dosyalarla devam et
- Refine sonrasi %50+ degisim varsa → kullaniciya bildir, onay al, otomatik merge etme

## Red Flags
- Refine sonrasi knowledge dosyasi %50'den fazla degistiyse — buyuk sorun, onceki sharpen kalitesiz
- Tum bilgi silindiyse — kaynak kalitesi sorunu
- Ayni refinement'i 3+ kez yapmak gerekiyorsa — AGENT.md boundary'si yanlis olabilir

## Verification
- [ ] Tum dosyalar tutarli ve cakismasiz
- [ ] Gereksiz tekrar yok
- [ ] Her knowledge dosyasinda kaynak ve tarih var
- [ ] refinements.md'ye entry eklendi
- [ ] _index.md guncel
