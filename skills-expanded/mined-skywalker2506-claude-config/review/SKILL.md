---
name: review
description: "Tek task/PR/commit review — C3 (AI Reviewer) veya C1 (Lead Reviewer) tetikler, puan verir, eksik varsa düzeltir. Triggers: review, incele, kod incele, PR review, commit review, kontrol et."
argument-hint: "[PR# | commit-hash | dosya-yolu | task-id]"
---

# /review — Tek İş Review

Tek bir task, PR veya commit'i C-level reviewer agent'larla incele.

> **WARNING — DO NOT invoke via forked subagent.** Fork would inherit the context of the code being reviewed and bias the reviewer toward "I wrote this, it's fine." Always spawn review as a normal (blank) subagent, regardless of how the parent session arrived here.

## Akış

### 1. Kapsam belirle

| Argüman | Ne yapar |
|---------|---------|
| PR# | O PR'ı GitHub'dan çek, diff incele |
| commit hash | O commit'i incele |
| Task ID (T-001) | Task'ı sprint dosyasında bul, ilgili commit/PR'ı çek |
| dosya yolu | O dosyayı incele |
| argümansız | Son commit'i incele |

### 2. C3 dispatch et (her zaman)

C3 (Local AI Reviewer) her review'da otomatik tetiklenir:
- Doğruluk, güvenlik, basitlik
- Commit convention kontrolü
- PR kuralı uyumu (kaç dosya değişti?)

### 3. Eskalasyon

| Durum | Agent |
|-------|-------|
| Güvenlik şüphesi | C3 → B13 (Security Auditor) |
| Mimari etki | C3 → C1 (Lead Reviewer, Opus) |
| Test eksikliği | C3 → B6 (Test Writer) |
| Genel onay | C3 yeterli |

### 4. Çıktı

```
## Review: CC-10 / feat: add /sprint-plan sync

Skor: 8.5/10

✅ Doğruluk: Sync workflow amaçla örtüşüyor
✅ Güvenlik: Risk yok
⚠️ Basitlik: 3 iç içe koşul — flatten edilebilir (nice-to-have)
✅ Git: Kural uygun (tek commit, 1 dosya)
✅ Task: done, yorum mevcut

Aksiyon: Onaylandı. Nice-to-have iyileştirme için CC-XX açıldı.
```

### 5. Aksiyon

| Skor | Aksiyon |
|------|---------|
| ≥ 8 | Onayla |
| 6-8 | Sprint dosyasına improvement notu, kullanıcıya sor |
| < 6 | Yeniden yap — B7 (Bug Hunter) veya ilgili agent'a ver |

## Pipeline entegrasyonu

Bu skill A1/B-agent'ların son adımı olarak da çağrılabilir:
- A1 task tamamlayınca: `→ /review <task-id>` ile kapat
- Otomatik pipeline: implement → test → review → done

## Kurallar
- Max 15 tool call
- C3 her zaman primary — C1/B13 sadece eskalasyonda
- Revize gerekirse orijinal agent'a geri ver, yeni agent başlatma

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
