---
name: ui-toolkit
description: "Unity UI Toolkit (UXML/USS) ile arayuz kurma, uretme ve dogrulama. bm-ui-authoring hattinin knowledge paketini okur; UXML/USS uretmeden once o bilgiyi yuklemeni saglar. Triggers: ui toolkit, uxml, uss, unity ui, arayuz kur, ekran tasarla, ui uret, runtime ui, visual element, uidocument, ui pipeline, kart ui, ekran yerlesimi."
---

# ui-toolkit — Unity UI Toolkit ile arayuz uretimi

Bu skill **kod yazdirmaz**; once **ne bildigini** kurar. Unity UI Toolkit'te uretim yapan
bir ajan, once bu platformun o konuda **olctugu** ve **karara bagladigi** seyleri okumak
zorundadir. Aksi halde CSS aliskanligiyla desteklenmeyen ozellik yazar, uGUI aliskanligiyla
prefab arar, ve yanlisi tekrar eder.

## 0) Once bilgiyi yukle — atlanamaz

```bash
BM_UI=~/Projects/bm-ui-authoring
cat $BM_UI/docs/AI/STATE.md          # neyin KASITLI eksik oldugu — once bu
cat $BM_UI/docs/AI/ARCHITECTURE.md   # hattin sinirlari, determinizm karari, motor karari
cat $BM_UI/knowledge/_index.md       # gorev -> madde eslemesi
```

`_index.md` bir tabloyla "hangi iste hangi madde okunur" der. **Tum knowledge'i okuma** —
ilgisiz madde karari bulandirir. Gorevine ait olanlari oku.

`STATE.md` once gelir cunku **"Kasitli eksikler — TAMAMLAMAYIN"** listesini tasir. O listeyi
okumadan calisan ajan, bilincli olarak bos birakilmis bir yeri "tamamlar" ve mimari karari
sessizce bozar.

## 1) Bu hattin degismez kararlari

Bunlar tartisilmaz; degistirmek isteyen once `ARCHITECTURE.md`'deki gerekceyi curutmeli.

| Karar | Gerekce |
|---|---|
| **UI Toolkit**, uGUI degil | UXML/USS **metin** — diff'lenebilir, uretilebilir. uGUI'de duzen prefab'da yasar: ikili, uretilemez |
| **Dondurma/CAS yok** | Uretici deterministik. Diger hatlardan kopyalanacak en pahali mekanizma buraya gereksiz |
| Sanat varliklari bu hattin isi degil | `bm-sprite-forge` uretir, bu hat **yerlestirir** |
| Gorsel tasarim karari insanindir | Hat duzeni **uygular**, secmez |

## 2) Uretmeden once — dogrulanabilir kurallar

Tuketicinin kurallari sayisal yazilmis, yani **kapiya baglanabilir**. Uretilen her ekran
bunlara uymali:

| Kural | Nereden | Nasil olculur |
|---|---|---|
| Duyarli izgara: 4 stat → 2×2, 5–6 → 3×2, 7–8 → 4×2, >8 → ayri panel | Touchline Forge `UI_AND_CARD_PIPELINE.md` §8 | uretilen duzen kuralla eslesiyor mu — saf veri kontrolu |
| **Hicbir bilgi yalniz renkle tasinamaz** | GDD §11.4 | ekran goruntusunun **doygunlugunu sifirla**, durum hala ayirt ediliyor mu |
| Ikonlar 24–32 px'de okunur | `UI_AND_CARD_PIPELINE.md` §5 | kucult, kontrast/entropi olc |
| Tam klavye gezinilebilirligi | §11.4 + Steam Deck kisiti | odak sirasi her etkilesimli elemana ulasiyor mu |
| Lokalizasyon anahtari bagli | — | baglanan anahtar sozlukte var mi (kume farki) |

Ikinci satir ozellikle degerli: "renkle tasinan bilgi yok" cogu projede bir **dilek**tir.
Doygunluk sifirlama testi onu **kapiya** cevirir.

## 3) Metin gorsele girmez

`UI_AND_CARD_PIPELINE.md` §1 net: **goruntuler yalniz sanat icerir.** Isim, sayi, durum
runtime'da basilir.

Yani bir kart gorseli uretirken ya da yerlestirirken: oyuncu adi, mevki, istatistik, maliyet,
seviye — hicbiri sprite'a gomulmez. Hepsi UXML'de bir `Label`, degeri baglanir.

## 4) Yaygin tuzaklar — hepsi bir kez yasandi ya da kayitli

**CSS aliskanligi.** USS, CSS'in bir **alt kumesi**. `grid` yok, `calc()` gibi seyler
sinirli. CSS bilgisiyle gelen "nasil olsa vardir" diye yazar ve sessizce calismaz.
`knowledge/` icindeki UXML/USS maddesi desteklenmeyenleri sayar — **once onu oku**.

**Tam ekran post-processing UI'i boyamaz.** UI Toolkit varsayilan **overlay** modda,
post-processing'den *sonra* cizilir. `FRONKON Artistic` gibi paketler sahneyi boyar, UI'i
boyamaz. Bu "efekt calismiyor" diye teshis edilir; oysa calisir, UI'in altinda kalir.

**Shader.** Eleman bazli ozel shader Unity 6.3'ten itibaren **Shader Graph** ile mumkun
(hedef 6000.4.3f1 bu esigin ustunde). Elle HLSL hala zor; yol Shader Graph.

## 5) Uretim yaptiktan sonra — receipt

ADR-002 geregi, urettigin ekranin receipt'i sunlari tasimali:

```
knowledgePackId       bm.ui-authoring/knowledge
knowledgePackDigest   okudugun paketin digest'i
citedTopics[]         karari etkileyen maddeler
```

`citedTopics: []` gecerlidir — her karar bir maddeye dayanmak zorunda degil. Ama bos olmasi
**gorunur** olur; kalip haline gelirse ya knowledge eksiktir ya ajan okumamistir.

## 6) Hat henuz acilmadi — bugun ne yapilir, ne yapilmaz

`bm-ui-authoring` **TASARIM / ERTELENMIS** durumda ve icinde **kod yoktur, kasitli**.
Dogum kapisi: motor projesi var oldugunda (spike PASS → final scaffold).

**Bugun yapilabilir:** knowledge okumak, ekran spec'i tasarlamak, kural ihlali aramak,
mevcut UXML/USS'i denetlemek.

**Bugun YAPILMAZ:** `bm-ui-authoring`'e implementasyon eklemek, `UiScreenSpec@1` semasini
yazmak. Sema, ilk gercek tuketicisi gorulmeden yazilirsa tuketicinin ihtiyacini tahmin
etmis olur — bu hatanin bedeli diger hatlarda olculdu.

## Ilgili

- Hat: `~/Projects/bm-ui-authoring`
- Tuketici: `~/Projects/touchline-forge` (`docs/BUILD_OWNERSHIP.md` sirayi anlatir)
- Sanat varliklari: `~/Projects/bm-sprite-forge`
- Knowledge kurallari: `~/Projects/bm-contracts/docs/AI/ADR-002-knowledge-layer.md`
