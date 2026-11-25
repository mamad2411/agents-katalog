---
name: gdd-review
description: "Bir GDD'yi inceler, capali puanlama ile zayif yerlerini isaretler ve uygulanabilir hale getirilmis v2'sini yazar. Ayrica prototipe girdi olan cekirdek dongu / SCOPE / ART cikarimini uretir. Uretimden once calisir; kod yazmaz. Triggers: gdd incele, gdd review, gdd degerlendir, gdd iyilestir, gdd puanla, tasarim dokumani incele, gdd analizi, gdd v2, design doc review."
user-invocable: true
argument-hint: "[GDD dosya yolu] [review|improve|extract — ops., varsayilan review+improve]"
---

# /gdd-review — dokuman uygulanabilir mi?

> Model yonlendirmesi: global/model-routing.md

`/greenlight` **neyi** yapmaya deger sorusunu cevaplar, `/prototype` **eglenceli mi**
sorusunu. Bu skill ikisinin arasindaki bosluktur: elde bir GDD var, **bu dokumandan
oyun cikar mi?**

> Puan = capali ve tekrar uretilebilir · Bulgu = alintili · Cikti = yeniden yazilmis v2

Bu skill **kod yazmaz, asset uretmez, prototip kosmaz.** Ciktisi metindir.

## Modlar

| Arg | Ne yapar |
|-----|----------|
| *(yok)* veya `review improve` | Tam kosu: okuma → puanlama → bulgular → v2 GDD |
| `review` | Sadece puanlama + bulgu raporu. v2 yazmaz |
| `improve` | Mevcut `review.md`'yi okur, sadece v2'yi yazar |
| `extract` | Puanlama yok: `/prototype` girdisi uretir — cekirdek dongu, `SCOPE.md`, `ART.md` |

Cikti dizini, GDD'nin yaninda `gdd-review/<tarih>-<ad>/`:

```
review.md    puan kirilimi + bant + alintili bulgular + kill/duzelt listesi
gdd-v2.md    yeniden yazilmis GDD (sadece review+improve ve improve modlarinda)
SCOPE.md     extract modu: olmali / olsa iyi / yok
ART.md       extract modu: goruntuleme sikligina gore sirali asset listesi
```

**Orijinal GDD'ye dokunma.** v2 ayri dosyadir; kullanici karsilastirabilmelidir.

---

## Faz 1 — Okuma ve haritalama

Dokumani bastan sona oku, sonra **tek sayfaya indir**: tur ve referans oyun · cekirdek
dongu · oyuncunun ana eylemi · kazanma/kaybetme · ton · kamera. Bu alti basliktan biri
dokumanda yoksa, o zaten bir bulgudur — uydurma, **eksik** olarak isaretle.

Ayni gecte iki sayim yap, ikisi de rapora girer:

| Sayim | Nasil | Ne demek |
|---|---|---|
| **Sayilastirilmis mekanik** | icinde en az bir sayi olan mekanik / toplam mekanik | uygulanabilirlik orani |
| **Benzersiz asset** | ekranda ayri gorunen her sey (yaratik, kart cercevesi, arena, UI paneli) | uretim yuku |

Ikisi de tahmin degil **sayim**: hangi satirdan geldigini yaz.

Sayim mekaniktir — **`agy`'ye ver**, sen okumaya devam et. Brief'e "her kalem icin
satir numarasi dondur, carpimlari acikca yaz" koy. Donen listeden iki kalemi
dokumandan dogrula; tutmuyorsa sayimi kendin yap.

---

## Faz 2 — Puanlama: 7 boyut, capali

Her boyut 0-5. Capa yoksa puan yoktur — her puani **dokumandan alintiyla** gerekcelendir.

| # | Boyut | 0 | 3 | 5 |
|---|---|---|---|---|
| 1 | **Cekirdek dongu netligi** | dongu yazilmamis | dongu var, adimlarin biri sayisiz | dongu tek diyagramda, her adimin girdi/ciktisi belli |
| 2 | **Karar kalitesi** | oyuncu secim yapmiyor ya da tek dominant strateji var | secimler var ama takas belirsiz | her secim baska bir seyden vazgecmek; takaslar isimle yazilmis |
| 3 | **Degisim egrisi** | 30. dakika 3. dakikayla ayni | icerik artiyor, tur degismiyor | oyuncunun *yaptigi is* run boyunca degisiyor, ornekle gosterilmis |
| 4 | **Kapsam gercekciligi** | benzersiz asset >150 ya da sistem sayisi tek kisiyi asiyor | MVP tanimli ama sayisiz | MVP sayiyla kesilmis; her sistem icin "yoksa ne olur" yazili |
| 5 | **Sayilastirma** | hicbir mekanikte sayi yok | orani ~%50 | >%80; hasar, sure, maliyet, spawn hizi yazili |
| 6 | **Hook / farklilik** | tur tarifi, hook yok | hook var ama komsu oyunla ayni | 10 saniyede anlatilan, ekranda gorunen tek cumlelik hook |
| 7 | **Kanitlanmamis varsayim** | tasidigi risk hic adlandirilmamis | riskler listelenmis, sinanmamis | her buyuk varsayim icin **prototiple sinanacak** somut soru yazili |

Toplam 35. Bant, eylem soyler:

| Puan | Bant | Eylem |
|---:|---|---|
| 29-35 | **A** | v2 kozmetik; `/prototype`'a gonder |
| 22-28 | **B** | v2 yaz, 2-3 boyutu duzelt, sonra `/prototype` |
| 15-21 | **C** | v2 zorunlu; 3'un altindaki her boyut yeniden yazilir |
| 0-14 | **F** | dokuman degil fikir sorunu — `/greenlight`'a geri gonder |

**Boyut 4 ya da 7'den 0 gelirse bant otomatik en fazla C'dir.** Kapsami tutmayan ya da
riskini adlandirmayan bir GDD, diger boyutlar parlasa da uretime giremez.

---

## Faz 3 — Bulgular: alintili, tek tek

Her bulgu su ucunu tasir, yoksa bulgu degil izlenimdir:

```
BULGU  — tek cumle, ne yanlis
ALINTI — GDD'den, satir/bolum numarasiyla
DUZELT — yerine ne yazilacak, SOMUT (sayiyla ya da kesilmis kapsamla)
```

Iki bulgu turu ozellikle aranir, cunku ikisi de gec fark edilir:

**1. Sessiz kapsam patlamasi.** Dokuman "6 aile, her aile 5 kademe" der; bu 30 yaratik
+ 30 evrim gorseli demektir. Carpimi **sen yap ve yaz** — GDD yazari carpmaz.

**2. Kendi kendini yalanlayan pilar.** "Kaos eglenceli olmali, rastgele olmamali" diyen
bir dokuman, sonra oyuncuya kaosu okuma araci vermiyorsa pilar ihlal edilmistir. Pilarlari
sistemlerle **capraz kontrol et**: her pilar icin onu tasiyan sistem hangisi?

Bulgular siddet sirasina gore siralanir; en fazla 12 bulgu. 12'yi asiyorsa dokuman zaten
C ya da F bandindadir, tek tek listelemek yerine **yapisal teshis** yaz.

---

## Faz 4 — v2: yeniden yaz, yamalamak degil

v2 orijinalin yorumlanmis hali degil, **yerine gecen dokumandir**. Kurallar:

- 3'un altinda puan alan her boyut **yeniden yazilir**; 3 ve ustu boyutlar korunur
- Her mekanige en az bir sayi girer; bilmiyorsan makul bir sayi yaz ve `[tahmin]` etiketle
- MVP bolumu sayiyla keser: kac yaratik, kac kart, kac arena, kac dakika
- Sonuna **"prototiple sinanacak sorular"** bolumu: 3-5 madde, her biri evet/hayir
- Kesilen her sey `v1'den cikarilanlar` basliginda gorunur — sessiz silme yok

v2'nin uzunlugu orijinali **asmamalidir**. Iyi bir revizyon genelde kisaltir: karar
verilmis her sey, karar verilmemis uc paragraftan kisadir.

---

## `extract` modu — `/prototype`'in girdisi

Puanlama yok. Uc cikti:

1. **Cekirdek dongu:** `oyuncu eylemi -> geri bildirim -> odul -> ilerleme -> tekrar`
   ve dort cevap: ana eylem · kazanma sarti · kaybetme sarti · hangi anlar gorsel
   geri bildirim istiyor.
2. **`SCOPE.md`** — 10 satir. *Olmali:* cekirdek mekanik, etkilesim, minimum UI,
   kazan/kaybet, geri bildirim efektleri. *Olsa iyi:* ikincil sistemler, ekstra icerik.
   *Yok:* save, tutorial, ayarlar, erisilebilirlik, coklu oyuncu, ECS, backend.
3. **`ART.md`** — kesilmis kapsamda ekranda gorunen her sey, id + tek cumle tarif.
   Liste 10'un ustundeyse **goruntuleme sikligina gore sirala**; oyuncunun en cok
   baktigi sey ilk tura girer.

Uc ciktinin ucu de cikarimdir, muhakeme degil: **`agy`'ye delege edilir.** Kesme
karari — neyin *Olmali*, neyin *Yok* oldugu — sende kalir; ajana kesilmis kapsami
verirsin, ajan listeyi cikarir.

**Ilk prototip 1-3 dakikalik oynanistir.** GDD 7 gun istiyorsa 2 gun, 10 kart istiyorsa
4 kart. GDD'nin "kabul kriterleri" bolumu urun hattinindir, extract'i baglamaz.

---

## Model ve effort

Bu skill'in isinin buyuk kismi **mekanik**: saymak, listelemek, cikarmak. Onlar
`agy` uzerinden Gemini'ye gider. Claude'da kalan tek sey **yargi**: puan, bant,
bulgunun siddeti, neyin kesilecegi.

| Is | Nereye | Neden |
|---|---|---|
| Sayilastirilmis mekanik sayimi | **`agy`** | sayim, yorum degil |
| Benzersiz asset sayimi ve carpimi ("6 aile × 5 kademe = 30") | **`agy`** | aritmetik |
| Cok uzun GDD (>1500 satir) bolum ozeti | **`agy`**, bolum basina bir serit | paralel, birbirini beklemez |
| `extract` modu — `SCOPE.md`, `ART.md`, cekirdek dongu cikarimi | **`agy`** | cikarim, muhakeme degil |
| Alinti toplama (bir iddianin gectigi satirlari bulmak) | **`agy`** | arama |
| **Puanlama, bant, bulgu siddeti** | **Claude** | delege edilmez |
| **v2'nin yeniden yazimi** | **Claude** | neyin neden degistigi karardir |
| Terminoloji/format birlestirme, baslik duzeni, tablo hizasi (v2 yazildiktan sonra) | **`agy`** | mekanik temizlik |

```bash
~/Projects/ClaudeHQ/scripts/hq agy --file <brief> --dir <gdd-dizini> --slug gdd-<is> --json
```

**Puanlama delege edilmez:** farkli ajanlar farkli capa okur, puanlar
karsilastirilamaz hale gelir. Ayni sebeple bant ve kill/duzelt karari da kalir.

**Delege edilen her sayim satir numarasi ile doner.** Sayi tek basina kanit degil —
`hq agy` ciktisi iddiadir; en az iki satiri dokumandan **kendin** dogrula, tutmuyorsa
sayimi kendin yap. Yanlis bir asset sayimi dogrudan Boyut 4'un puanini bozar.

---

## Yapma

| Yapma | Neden |
|---|---|
| Alintisiz bulgu yazmak | dogrulanamaz; yazar hangi cumleyi degistirecegini bilemez |
| "Denge ayarlanmali" demek | bu bulgu degil temenni. Hangi sayi, hangi yone |
| Orijinal GDD'yi duzenlemek | karsilastirilamaz hale gelir; v2 ayri dosyadir |
| Kapsami sormadan buyutmek | GDD'ye yeni sistem eklemek bu skill'in isi degil |
| Puan vermeden v2 yazmak | neyin neden degistigi kaybolur |
| Pazar/janr karari vermek | o `/greenlight`'in isi; buradan cikan sinyal varsa **oraya yonlendir** |
| Prototip kosmak, kod yazmak | `/prototype` |

## Teslim

1. `review.md` yolu + **puan tablosu ve bant** yanitin icinde
2. En siddetli 3 bulgu, tek satir ozetleriyle
3. `gdd-v2.md` yazildiysa: neyin degistigi ve v1'den neyin cikarildigi, iki cumle
4. Sonraki adim onerisi: **A/B → `/prototype`** · **C → v2'yi onayla, sonra `/prototype`**
   · **F → `/greenlight`**
