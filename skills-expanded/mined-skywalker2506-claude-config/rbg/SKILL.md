---
name: rbg
description: Görevi arka planda çalıştır (run_in_background). /btw değil. Slash sıraya girer — kuyruk uyarısı skill içinde.
argument-hint: "<görev — dosya, bash, MCP, uzun iş>"
disable-model-invocation: true
---

## Önemli: `/rbg` kuyrukta bekler (ürün davranışı)

Claude Code’da **aynı oturumda** yeni mesaj/slash, aktif agent turu bitene kadar **işlenmez**; arayüzde **“queued messages”** / “Press up to edit queued messages” görürsün. Bu, `run_in_background` veya bu skill ile **aşılamaz**: sıra gelmeden `/rbg` **başlamaz**.

**Gerçek paralellik için:**

1. **Ayrı terminal + ikinci oturum:** Projede yeni bir shell → `claude` (veya `claude --continue` ayrı session) — bu ikinci süreç birincisiyle paralel çalışabilir.
2. **Önce mevcut turu bitir veya iptal et** (ortamında kısayol / Stop varsa) — sonra sıradaki mesaj işlenir.
3. **Zaten yazdıysan:** Mesaj kuyrukta; tur bitince otomatik işlenir — “başlamadı” değil, **bekliyor**.

Bu uyarıyı kullanıcı `/rbg` yazdığında sık sık karıştırıyorsa kısaca tekrarla.

---

## `/btw` ile fark

| | `/btw` | `/rbg` |
|---|--------|--------|
| Amaç | Kısa yan soru | Araçlı işi arka plan **agent**’a devret |
| Araç | Yok | Var |
| Kuyruk | Aynı — yine sıra bekler | Aynı |

---

## Görev yükü

```
$ARGUMENTS
```

- **Boşsa:** Önceki kullanıcı mesajı veya bağlamdan net talimat; gerekirse tek cümle onay.
- **Doluysa:** Tüm argüman tek arka plan görevi.

---

## Slash işlendikten sonra (sıra gelince)

1. Görevi **anında** arka plana al: `run_in_background: true` / Background Agent / Task — ortamındaki mekanizma.
2. **`CLAUDE.md`** ve güvenlik kurallari.
3. Bittiğinde ana sohbete **kısa özet**.

Ana oturumda dosyayı **anında** senin elle düzenlemen gerekiyorsa: `scripts/` veya editör; `/rbg` sıra bekler.

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
