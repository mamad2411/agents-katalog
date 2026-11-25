---
name: reference-style
description: "Referans gorselden stil aktarimi: elde referans varken stili TARIF ETME, GOSTER. Adherence'i olcerek ayarlar — stil yakinligi ve icerik sizintisi AYRI olculur. Triggers: referans, reference, stil aktarimi, style transfer, buna benzesin, ayni tarzda, referansa gore uret, IP-Adapter, agirlik ayari."
user-invocable: true
argument-hint: "[referans gorsel yolu] — orn. 'art/raw/01_player.png'"
---

# /reference-style — Referansa gore uret

**Tek cumlelik kural: elinde referans varken stili TARIF ETME, GOSTER.**

Bu skill uc art uretim skill'inin ortak kuralini tutar
(`/image-prompt`, `/asset-prompt-gen`, `/animate`). Kural bir kez burada
yazili; oteki skill'ler buraya isaret eder, kopyalamaz.

---

## Kural 1 — Referans varsa prompt stili TARIF ETMEZ

Referans verildiginde prompt neredeyse bosalir: yalniz **ozne** ve
**kisitlar** kalir. Stil tarifi (kontur, palet, isik, golge, oran) prompta
YAZILMAZ — referans onu zaten tasiyor.

### Neden — olculdu, tahmin degil

bm-sprite-forge'da bir sanat stili once **metinle** tanimlandi:

| tur | ne cikti | sebep |
|---|---|---|
| 1 | kurumsal vektor illustrasyon | oran sart kosuldu ama onu gizleyen kadraj istendi |
| 2 | cizgi film cocugu | yetiskin isaretleri toplu silindi |
| 3 | pastel/bulanik | sevimliligi yapan doku "tutarlilik icin" yasaklanmisti |
| 4 | sevimli ama yanlis aile | oran, kontur, golgeleme hala uzak |

Sonra referans **dogrudan verildi**, prompt bosaltildi: **tek turda** oturdu —
kontur, rim isigi, cel shading ve palet ayni anda geldi.

Uc sebep, ucu de genellenebilir:

- **Stil cok boyutludur, metin sirayla ilerler.** Her duzeltme baska bir
  ekseni bozar. Referans hepsini bir kerede tasir.
- **Tarif eden, tarif ettigini gordugunu sanir.** O turda tanim, karakter
  sanatinin kendi boyutunda HIC GORULMEDEN yazildi ve "kontur yok" dendi;
  oysa kalin kontur stilin imzasiydi.
- **Negatif talimat yon degil sapma uretir.** "not childish" modeli
  yetiskinlige degil gercekcilige itti.

---

## Kural 2 — "Benzesin" IKI ayri sey, ve biri otekinin hatasi

| istenen | teknik | basarisizlik bicimi |
|---|---|---|
| ayni **sanat yonu** (kontur, palet, isik) | stil aktarimi | yetersiz stilizasyon |
| ayni **icerik** (ayni yuz, ayni logo) | — | **icerik sizintisi** |

Adherence sikildikca ikincisi artar. Bu bir ayar meselesi, cozulmus bir
problem degil:

- IP-Adapter agirligi **0.3** -> %40-50 marka logosu sizdi (44 gorselde
  olculdu). **0.6** kanonik taban.
- Tek koyu tenli referans, prompt'taki TUM cesitlilik talimatlarini ezdi;
  44 portrenin hepsi ayni ten rengiyle cikti.
- Qwen-Image-Edit'in bilinen kusuru **semantic leakage**: stil referansindan
  istenmeyen ogeleri getiriyor. FLUX.2 tarafinda ters kusur: yetersiz
  stilizasyon.

**Cesitlilik agirligi dusurerek saglanmaz** — referansi degistirerek
saglanir (anchor swap).

---

## Kural 3 — Kucuk ornekle agirlik dogrulanmaz

Agirlik 0.3, **uc gorselluk** bir testi gecti ve uretimde 44 gorselde marka
sizintisi yapti. Bir adherence ayarini **~20 gorselden az** ornekle
onaylama.

---

## Kural 4 — Iki sayi ayri olculur

Tek bir "benzerlik" skoru yaniltir: referansi birebir kopyalayan bir cikti o
skorda MUKEMMEL gorunur. O yuzden her zaman iki ayri olcum:

1. **stil yakinligi** — cikti referansin sanat yonune ne kadar yakin
2. **icerik sizintisi** — referanstaki nesne/yuz/logo/metin ciktiya tasindi mi

Ikisi birlikte raporlanir. Biri raporlanmadan agirlik degistirilmez.

---

## Kural 5 — Kapi yesili yeterli degil

Olcum ayar icindir, karar icin degil. Son bar **PNG'ye bakmaktir**
(`#0E1520` zemin). Bu depoda iki kez olculdu: decontam'i iki kez kosturmak
`alpha.edge` metrigini yesillendiriyor ama hale gozle hala duruyor.

---

## Yerel arac secimi (2026-08, RTX 5080 / 16 GB)

| ihtiyac | arac | lisans |
|---|---|---|
| karakter KIMLIGI tekrari | SDXL + IP-Adapter @0.6 | Open RAIL++-M |
| referanstan stil aktarimi | Qwen-Image-Edit-2511 (3 referans) | Apache 2.0 |
| okunur metin | Qwen-Image | Apache 2.0 |

FLUX.2 dev 24 GB — bu makineye sigmiyor; lisans tartismasina girmeye gerek
kalmiyor. Lisansi tartismasiz FLUX varyanti yalniz klein 4B.

Model dosyalari: `bm-sprite-forge/tools/model_indir.py`.
Secim mantigi ve "olculmemis secim uretimde kullanilmaz" kapisi:
`bm-sprite-forge/pipeline/models.py`.

---

## Kontrol listesi

Referansli bir uretim baslatmadan once:

- [ ] Referans gorsel VAR ve yolu belli
- [ ] Prompt stil tarifi ICERMIYOR (yalniz ozne + kisit)
- [ ] Agirlik olculmus bir degerde (varsayilan 0.6), tahmin degil
- [ ] Cesitlilik gerekiyorsa anchor swap planlandi, agirlik dusurulmedi
- [ ] Stil yakinligi VE icerik sizintisi ayri raporlanacak
- [ ] Ornek sayisi >= 20 (agirlik degisikligi onaylanacaksa)
- [ ] Son karar icin PNG'ler acilacak
