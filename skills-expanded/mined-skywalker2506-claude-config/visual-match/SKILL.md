---
name: visual-match
description: "Bir referans karesine BENZETIR: kareyi olcer, sapmayi bant bant cikarir, kod/yerlesim/grade duzeltir, tekrar olcer. Ton kapisi + dokuz bantlik mikroskop kurar; 'gozle bakip guzel oldu' demeyi engeller. Triggers: visual match, gorsele benzet, referansa benzet, birebir ayni olsun, look match, kamera effect ayni, ekrandakine benzesin, art direction olc, gorsel hedef."
user-invocable: true
argument-hint: "[referans gorsel yolu] — orn. docs/media/image1.jpg"
---

# /visual-match — Referans kareye benzetme

"Ekrandakine benzesin" cumlesi tek basina calistirilamaz, cunku **benzemek**
olculebilir bir sey degildir — ta ki olculur hale getirilene kadar. Bu skill onu
sayiya cevirir, sonra sayilar referansin bandina girene kadar dongu doner.

Bu dosyadaki her kural **olculmus bir hatadan** cikti. Kaynak:
`veil-of-the-last-king/docs/VISUAL-LESSONS.md`.

---

## Kural 0 — Hicbir gorsel iddiada bulunma, olc

"Daha iyi oldu", "artik benziyor", "atmosfer yakalandi" — bunlarin hicbiri
teslim degil. Teslim, referansin sayisi ile senin sayin yan yana.

```
capture (referansin TAM boyutunda)  →  olc  →  bak  →  TEK sinif seyi degistir  →  hepsini yeniden olc
```

Son adim pazarlik konusu degil: bir bantta yaptigin duzeltme baska bir bandi
kaydirir, ve bunu ancak hepsini yeniden kosarak gorursun.

---

## Kural 1 — Once iki arac kur: kapi ve mikroskop

Bunlar ayni sey degil ve biri digerinin yerine gecmez.

| arac | ne yapar | ne zaman kosar |
|---|---|---|
| `tools/look-check.mjs` | KAPI. Esikli, pass/fail, CI'da kosar | her commit |
| `tools/band-diff.mjs` | MIKROSKOP. Bant bant fark, esik yok, hicbir sey fail etmez | her duzeltme turunda |

Neden ikisi: kaba bantli bir kapi, **iki zit hatayi birbiriyle ortalayip
"saglikli" der.** Olculdu — on bir metrikten hepsi gecerken orta katman
referansin 2.6 kati mesgul, alt ucte bir bombostu.

### Kapinin metrikleri (referanstan olcelerek doldurulur)

Ton: ortalama parlaklik · ton yayilimi (p10-p90) · ton ortancasi · en parlak
bandin konumu ve degeri · oyun duzlemi degeri · alt ceyrek degeri · doygun
piksel orani.

**Ve en az bir DOKU metrigi.** Bkz. Kural 2.

### Mikroskobun bantlari

Kareyi 9 yatay banda bol ve her biri icin parlaklik / doygunluk / **kenar
yogunlugu** ver. Bantlari yaptigi ise gore adlandir — `tavan`, `ust harabe`,
`isik bolgesi`, `orta kat`, `kemer`, `oyun duzlemi`, `zemin cizgisi`, `on plan`,
`alt band` — cunku duzeltme o isme nisan alir.

Ayrica iki **isaret noktasi** ver: en parlak satirin konumu, ve karenin
karanliga dustugu satir. Bunlar kompozisyonu tek sayida ozetler.

---

## Kural 2 — Ton kapisi bos odayi gecirir

En sinsi tuzak. Ilk kapida sekiz ton metrigi vardi; referans kendi kapisini
gecti, sonra **uc prop + duz gradyandan olusan bos bir oda sekizden yedisini
gecti.**

Karede dogru tonlar vardi ve **hicbir sey yoktu.**

Ayiran sey **kenar yogunlugu**: her bandin ne kadar detay tasidigi. Referans
0.21/0.23/0.29; bizimki 0.10/0.14/0.14.

> **Kural.** Bir gorunum kapisinda, **bos bir tuvalin gecemeyecegi** en az bir
> metrik olmak zorunda. Butun ton metrikleri bir gradyanla tatmin edilebilir.

---

## Kural 3 — Kenar yogunlugu cozunurluge bagimlidir

Ayni sahne HiDPI ekranda 0.09, referansin 1536x864'une kucultuldugunde 0.14.
Sahnede hicbir sey degismedi. Gradyan esigi, ayni detay daha cok piksele
yayildiginda daha az piksel sayar.

> **Kural.** Olcmeden ONCE her kareyi referansin tam boyutuna resize et. Kendi
> yerel boyutunda alinmis bir metrik hicbir seyle karsilastirilamaz.

---

## Kural 4 — Detay mürekkep miktari degil, iz sayisidir

Ilk yaprak gecisi `min(w,h)*0.06 + 6` px boyutunda lekeler ciziyordu. Duvara
yapistirilmis nilufer gibi duruyordu ve 0.09 olcuyordu — cunku buyuk seklin
alanina gore cevresi kucuktur. Yapragi sabit bir piksel boyutuna sabitleyip
sayiyi alana gore artirmak ayni bandi 0.30'a tasidi.

---

## Kural 5 — Iki turlu gorunmez olma, ikisi de "sprite bozuk" gibi gorunur

- **Ustune boyanmis.** Odalar on plani tam genislikte, karakterin durdugu
  yuksekligi kapsayan bir plaka olarak yazmisti. Bant grade'i o plakalari
  siyaha ezince karakter kareden **boyanarak silindi**. Sprite sahnedeydi,
  dogru yerdeydi, dogru olcekteydi, dokusu yuklüydu — siyah bir duvarin
  arkasindaydi.
- **Kirpilarak disari itilmis.** Odanin kamera `bounds`'u kameranin **merkezinin**
  durabilecegi yeri sinirlar, gorunur kenarin ulasabilecegi yeri degil. Kenar
  siniri gibi okununca kamera 18.7'ye park etti, karakter karenin 14.7 birim
  solunda kaldi. Oda bos gorundu.

> **Kural.** Bir sey "eksik" oldugunda, yeniden cizmeden **yok oldugunu kanitla.**
> Once sahne grafigini sorgula: nesnenin konumu, olcegi, dokusu.

---

## Kural 6 — Konfigürasyonda olup okunmayan deger

`GRADE.lift` "atmosferi ustune sis plakasi olarak ekler" diye belgelenmisti ve
**hicbir renderer dosyasi onu okumuyordu.** Orta katmanin fazla keskinligini
yumusatmak icin degeri yukseltmek hicbir sey degistirmedi — var olmayan bir kol
cevriliyordu.

> **Kural.** Bir sayiyi ayarlamadan once `grep` ile **okundugunu** dogrula.
> Ayarladigin degerin etkisini goremiyorsan ilk hipotez "yeterince degistirmedim"
> degil, "bu deger okunmuyor" olmali.

---

## Kural 7 — Uzaklik karanlik degil, kontrast kaybidir

Boyanmis bir karede orta katman one dogru **havada erir**. Bizimki dogru
ortalama degerdeydi ama referansin 2.6 kati keskindi.

Cozum sabit ortalamada atmosferik karisim:

```
sonuc = sanat * gain * (1 - lift) + sis * lift
```

Sanat, sisin ekleyecegi payla tam olarak kisilir. Boylece `lift` yalnizca
kontrast kaybi satin alir. Naif uygulandiginda — sanat tam parlaklikta, ustune
sis — her bant 18-22 puan parlak cikti ve yumusatmasi gereken keskinlik
kipirdamadi.

---

## Kural 8 — Odayi iki kez aydinlatma

Uretilmis plakalar kendi isik kaynagini tasimaya baslayinca motorun additive key
light'i onun ustune bindi: isik bandi L 92, referans 67. Motor isigi prosedurel
arka planlar icin dogruydu, boyanmis olanlar icin yanlis.

> **Kural.** Her aydinlatma katkisinin **tek bir sahibi** olur. Sanat, motorun
> yaptigi bir isi devralmaya basladiysa motor o isi birakmali.

---

## Kural 9 — Kirpma hizalamayi bozar

Plakalar "su cizgisi karenin %69'unda" diye istendi, oyle de geldi. Sonra
hazirlik adimi her birini alfa kutusuna kirpti — ve kirpma bos gogu attigi icin
o oran degisti: %69.0 / %70.0 / **%76.7** / **%38.1**.

Ortak kutuya yerlestirilince su kemerinin ayaklari, karakterin yurudugu zeminin
dort birim ustunde asili kaldi. "Sanat yanlis cizilmis" gibi gorunur.

> **Kural.** Herhangi bir kirpma adiminin ARDINDAN hizalama oranlarini
> manifest'in trim dikdortgeninden yeniden turet. Bir orani kirpmanin obur
> tarafina tasima.

---

## Kural 10 — Yazili kutu bir KOMPOZISYON niyetidir, olcek emri degil

Bu, tek bir odada bir kez degil, **on iki odada birden** yasandi ve hicbiri
gozle "esnemis" diye okunmuyordu.

Odalar arka plan plakalarini `w`/`h` ile yazar. O kutu kompozisyon niyetidir:
"bu bant sunu kaplasin". Sanatin kendi orani bambaska olabilir. Ikisini
esitlemek = resmi germek.

Olculdu: `L1_stone_arch` **1.02:1** sanat, oda onu **5.50:1** kutuya yazmis —
kare bir kemer yana **bes buçuk kat** cekilmis. Platformlar yedi kata varmis.

> **Kural.** Fazla genisligi **doseyerek** doldur, gererek degil. Sanatin orani
> korunur, tekrar sayisi degisir.

Iki bant kurali birbirinden ayrilir ve **karistirilmasi iki yonlu hata**dir:

| bant | boyut nereden | neden |
|---|---|---|
| oyun / on plan (prop) | **sanattan** | heykel, fener; Cael'e gore olceklenmis |
| oyun (platform, dekor) | **kutudan** (`sizeLock`) | 9 birimlik yurume yolu 1.6 birimlik suse donuyor |
| arka plan | oran sanattan, genislik dosemeden | uzaktaki yapinin karesi kadraja gore, resmi degil |

### Plaka yerlesim cozumu

Parallax bandi `f` faktorunde `baseX + cameraX * (1 - f)` konumunda cizilir.
Bundan iki sonuc cikar ve ikisi de hesaplanir, tahmin edilmez:

```
merkez  = f * kameraMerkezi
yariGen >= gorusYarisi + f * (kameraMenzili / 2)
y       = -h * (1 - ufukOrani) - kameraY * (1 - f) * dikeyParallax
```

Bir odanin sayilarini digerine **kopyalamak** ayni siniftan hatadir: kamerasi
8..56 icin ortalanmis bir plaka, 8..104 kosan odada kadrajdan kayar — germek
kadar yanlis, sadece daha az gorunur.

---

## Kural 10.5 — Kisa plakanin ust kenari sert bir cizgidir

Doseme sanati kendi boyunda tutar, yani plaka **kisa** kalir. Kisa plakanin ust
kenari karenin ortasindan gecen sert bir yatay cizgi olur — olculdu, karenin
%25'inde, her odada.

Bir odada gorunmemesi duzeldigi anlamina gelmez: DG-00'da o kenar tesadufen
karanlik bir bandin ve tavan ezmesinin altinda kaliyordu.

**Denenip basarisiz olan:** dikisi bandin kendi rengiyle "yumusatmak". Bir
plakanin **alfasini maskelemek**, ustune renk cizmekle ayni islem degil — ortaya
cikan sey bir bant, cozunme degil. Ya plaka kareyi asacak kadar uzatilir (bedeli
daha buyuk bir yapi, ki arka plan icin kompozisyon karari), ya da alfa rampasi
dokuya **pisirilir**.

---
## Kural 11 — Olcum aracinin kendisi de bozulur

Bunlar hepsi yasandi ve her biri once "oyun bozuk" gibi okundu:

- Canvas ekran goruntusu **bos** dondu, cunku `preserveDrawingBuffer` kapaliydi.
  Bir gorunum olcumu neredeyse bos bir goruntuyu notlandiriyordu.
- Ekran goruntusu araci, hic bosa dusmeyen bir sayfada **zaman asimina** ugrar
  (oyun surekli `requestAnimationFrame` kosar, "stabil bekle" hic tetiklenmez).
  Kareyi **sayfa disari itmeli**, arac iceri cekmemeli.
- Ilk dovus probu "sifir dusman, sifir olay" dedi ve kirik bir encounter sistemi
  gibi okundu. Surucü `right: true` gonderiyordu; simulasyon `moveX` okuyor.
  Oyun saglamdi.
- Baslangictaki ve sondaki HP karsilastirmasi, **dovulup olen ve tam canla
  dirilen** oyuncuyu "hic hasar almamis" gosterdi.

> **Kural.** Bir harness ilk kosusunda felaket bir hata buluyorsa, bozuk taraf
> genellikle harness'tir. Once kendi araciniza inanmayi birakin.

### Ve duzelten ile olcen AYRI arac olmali

Bir kare-ici zoom duzeltmesi yazdim, oran ters yazilmisti: kaldirmasi gereken
kaymayi **artiriyordu**. Build memnuniyetle `scale-fixed %7` diyordu, denetim
ayni klipte hala %8.2 olcuyordu.

Yakalanmasinin **tek** sebebi ikisinin ayri arac olmasi ve birbirini
tutmamasiydi. Duzeltmeyi uygulayan arac kendi basarisini rapor ediyorsa, o rapor
bir dilek listesidir.

> **Kural.** Duzeltmeyi uygulayan kod, duzeltmeyi olcen kod olamaz. Ikisi ayni
> sayiyi bagimsiz uretmeli.

---

## Kural 12 — Zaten dogru olani "duzeltme"

Kayda deger, cunku duzeltmek icin neredeyse zaman harcandi: kamera olcegi
(karakter kare yuksekliginin %16'si, referans %16-19) ve zemin cizgisi (ayaklar
%66, referans %67) **bastan dogruydu.**

> **Kural.** Ayarlamadan once olc. Gorsel bosugun yarisi kompozisyon ve boru
> hattidir; hicbiri kamera degildi.

---

## Yapma

- **Sadece metrige gore ayarlama.** Sayilar sana ne kadar oldugunu soyler,
  goz neyin oldugunu. Ikisini birlikte kullan, yoksa asiri uydurma yaparsin.
- **Ton metrigi ekleyip doku metrigi eklememe.** Kapi bos odayi gecirir.
- **Bir turda birden fazla sinif seyi degistirme.** Hangisinin isledigini
  ayirt edemezsin.
- **Daha guzel bir kareyi kabul etme** — bir metrigi banttan cikaran daha guzel
  bir kare gerileme, iyilesme degil.
- **"%99 benzedi" deme.** Sayilari koy, referansi yanina koy, kullanici karar
  verir.
- **Yedek painter'i cilalama.** Sanati olmayan oda prosedurel bir painter'a
  duser; onu guzellestirmek yanlis seyi cilalamaktir. Ya gercek plaka uret, ya
  var olan plakayi odaya gore yeniden coz.
- **Bir bandin ici bant olmali.** 9 birim yuksek bir on plan seridine "alt
  yarisina" yaprak serpmek, dort birim acik havaya leke asmaktir.
- **Tek turda iki sinif duzeltme yapma** — hangisinin isledigini ayirt edemezsin,
  ve bu dosyadaki hatalarin yarisi o yuzden iki tur surdu.
