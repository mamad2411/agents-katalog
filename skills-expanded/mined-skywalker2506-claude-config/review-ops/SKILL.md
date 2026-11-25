---
name: review-ops
description: "Orchestrator/A1 büyük iş bitince tetikle — batch task review, PR audit, kalite skoru, sprint kaydı güncel mi, eksik varsa yeniden task aç. Triggers: review-ops, ops review, batch bitti, orchestrator review, büyük iş bitti, toplu review, ne yaptık."
argument-hint: "[task-ids | repo-list | son-batch]"
---

# /review-ops — Orchestrator / Batch İş Sonrası Review

Tamamlanan bir iş grubunu (task seti, repo batch, sprint) incele.
Puan ver, eksik bul, gerekirse yeni task aç veya yeniden yaptır.

> **WARNING — DO NOT invoke via forked subagent.** Fork would inherit the context of the code/work being audited and bias the reviewer toward "I wrote this, it's fine." Always spawn review-ops as a normal (blank) subagent, regardless of how the parent session arrived here.

## Ne zaman tetiklenir

- A1 veya büyük bir agent batch'i tamamlandıktan sonra
- Sprint sonu
- Kullanıcı "bitti mi, iyi mi" tarzında bir şey sorduğunda
- `/review-sprint CC-10,CC-13,CC-14` gibi explicit çağrı

## Akış

### 1. Kapsam belirle (max 3 tool call)

Argüman gelirse parse et:
- `T-010,T-013` → o task'ları sprint dosyasindan oku
- `ccplugin-sprint-planner,ccplugin-code-quality` → o repoları incele
- Argümansız → son 24 saatte `done` olan task'ları sprint dosyasindan çek

### 2. Her task/repo için review (C1/C3 sub-agent dispatch)

Her öğe için paralel C3 (Local AI Reviewer) başlat:

**Task review:**
- Task detayını oku: açıklama, acceptance criteria var mı?
- GitHub'dan ilgili commit'leri bul (task key ile ara)
- PR açılmış mı? (dal kuralına uyulmuş mu?)
- Commit mesajı convention'a uygun mu? (feat/fix/chore...)

**Kod review:**
- İlgili dosyalara bak (değişen dosyalar)
- Doğruluk: amaçla örtüşüyor mu?
- Güvenlik: gizli bilgi, injection riski?
- Basitlik: gereksiz karmaşıklık?

### 3. Puanla

Her task/repo için 0-10 arası skor:

| Kriter | Ağırlık |
|--------|---------|
| Acceptance criteria karşılandı mı? | 30% |
| Kod kalitesi (doğruluk + güvenlik) | 30% |
| Git workflow uyumu (PR, branch, commit) | 20% |
| Sprint kaydı güncelliği (done, yorum, PR linki) | 20% |

### 4. Raporla

```
## Sprint Review Raporu

### ✅ CC-10 — /sprint-plan sync (8.5/10)
- Acceptance: ✓
- Kod: Sync workflow doğru implement edilmiş
- Git: direkt push — kural uygun (tek commit, 1 dosya) ✓  
- Task: done ✓
Yorum: İyi iş. Edge case: sprint kapalıysa ne olur?

### ⚠️ CC-13 — /memory-prune (6/10)
- Acceptance: ✓
- Kod: Temel implement var ama edge case eksik
- Git: PR açılmamış — 3 dosya değişti, PR gerekirdi ✗
- Task: done ✓
Aksiyon: CC-XX açıldı — PR retroaktif aç veya edge case'leri tamamla

Genel Skor: 7.2/10
```

### 5. Aksiyon al

| Skor | Aksiyon |
|------|---------|
| ≥ 8 | Onayla, kapat |
| 6-8 | Uyarı + sprint dosyasına not, kullanıcıya sor |
| < 6 | Yeni task aç (CC-XX: "Revize: [orijinal task]"), A1'e ver |

**PR eksikse:**
- 4+ dosya değişmiş ama PR yoksa → `mcp__github__create_pull_request` ile retroaktif PR aç
- Commit convention uyumsuzsa → PR'a yorum bırak

**Sprint kaydı güncel değilse:**
- Transition uygula, yorum ekle

### 6. Özet

```
Toplam: N task incelendi
✅ Onaylandı: X
⚠️ Uyarı: Y  
🔁 Revize task açıldı: Z
📋 PR retroaktif açıldı: W
```

## Kurallar
- C3 sub-agent'larını paralel çalıştır
- Max 40 tool call (büyük batch'lerde)
- Retroaktif PR açmadan önce kullanıcıya sor — sadece açıkça kötüyse direkt aç
- Revize task'ı orijinal task'a `blocks` alaniyla bağla
- Skor 10 üzerinden, yarım puan hassasiyetle

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
