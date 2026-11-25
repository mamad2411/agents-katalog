---
name: memory-prune
description: "Memory dosyalarini tara — stale/duplicate/yanlis kayitlari temizle, MEMORY.md indeksini guncelle. Triggers: memory-prune, memory temizle, hafiza temizle."
argument-hint: "[--dry-run]"
---

# /memory-prune — Memory Cleanup

Memory sistemindeki stale, duplicate ve yanlis kayitlari tespit edip temizler. MEMORY.md indeksini gunceller.

## Akis

### 1. Tara

`MEMORY.md` indeksini oku → her referans edilen `.md` dosyasini oku:

| Kontrol | Aksiyon |
|---------|---------|
| **Stale** | Referans verdigi dosya/fonksiyon/path artik yok → sil veya guncelle |
| **Duplicate** | Ayni bilgiyi farkli dosyalarda tekrar ediyor → birlestir |
| **Yanlis** | Kod/repo state ile celisiyor → dogrula, duzelt veya sil |
| **Orphan** | Memory klasorunde var ama MEMORY.md'de referans yok → indekse ekle veya sil |
| **Eskimis proje** | Project tipi memory — proje artik yok veya durum degismis → sil |

### 2. Dogrulama

Her memory icin:
- Dosya path referansi varsa → dosya hala var mi? (`Glob` ile kontrol)
- Fonksiyon/flag referansi varsa → hala kodda var mi? (`Grep` ile kontrol)
- Proje durumu referansi varsa → guncel mi? (`git log` ile kontrol)

### 3. Rapor

```
## Memory Prune Raporu

- Taranan: N memory dosyasi
- Stale: X (silinecek/guncellenecek)
- Duplicate: Y (birlestirilecek)
- Orphan: Z (indekse eklenecek/silinecek)

### Detay
| # | Dosya | Sorun | Oneri |
|---|-------|-------|-------|
| 1 | feedback_xxx.md | path artik yok | Sil |
| 2 | project_yyy.md | proje tamamlandi | Sil |
```

### 4. Uygulama

- `--dry-run` varsa: sadece rapor, degisiklik yapma
- Aksi halde: onay al → sil/guncelle → MEMORY.md indeksini yeniden yaz

## Kurallar

- Max 15 tool call
- Kullanici tipi memory'leri silmeden once sor (kisisel tercihler hassas)
- Feedback tipi memory'ler stale olsa bile dikkatli ol — kural hala gecerli olabilir
- MEMORY.md 200 satir limitini koru

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
