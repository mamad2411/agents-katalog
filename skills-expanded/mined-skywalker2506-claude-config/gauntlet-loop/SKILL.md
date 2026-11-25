---
name: gauntlet-loop
description: "Bir hedefi gauntlet dongusu olarak CALISTIRIR: parcalara boler, uretici + ayri kor kritik ajan koser, bar gecilene kadar surdurur. Referans verilmediyse arastirip bulur. Triggers: gauntlet, gauntlet loop, gauntlet calistir, kor kritik, referansa kadar dovus, bar gecene kadar."
user-invocable: true
argument-hint: "[hedef] [--ref <dosya/dizin veya benzemesi istenen urun adi>] [--prompt-only]"
---

# /gauntlet-loop — bar gecilene kadar dovusen dongu

**Bu skill calistirir.** Kullanici hedefi ve varsa referanslari verir; gerisi sende:
parcalara bolmek, uretici ve kritik ajanlari kosmak, bar gecilene kadar donguyu surdurmek.
Kullaniciya prompt uzatip "bunu calistir" **deme**.

`--prompt-only` verilirse — ve yalnizca o zaman — calistirmaz, tek blok gauntlet promptu
uretirsin.

**Ama "calistir" bu skill CAGRILDIGINDA gecerlidir.** Konusma sirasinda bir hedefin adi
gecmesi, o hedefi baslatma yetkisi degildir. Skill'in kendisi uzerinde calisiliyorsa —
kurallarini duzeltiyor, metnini tartisiyorsan — is skill dosyasidir, ornek verilen proje
degil. Ornegi baslatmak, istenmeyen saatler ve baskasinin deposuna commit demektir.

**Tek yazar kurali.** Gauntlet hedef deponun kendi dizininde acilmis bir oturumda kosar.
Baslamadan once o depoya baska kimsenin yazmadigini dogrula: baskasinin biraktigi kirli
agac, ayni proje uzerinde kosan bir build/test sureci, ya da kullanicinin ayri baslattigi
bir gorev. Ikinci yazar varsa **baslatma** — ayni dosyaya iki taraftan yazmak sessiz kayip
uretir, ve ayni anda kosan iki test surecinin cakismasi neredeyse her zaman "test kirmizi"
diye yanlis teshis edilir.

**Kullaniciya donmenin tek mesru sebebi:** yalnizca onun verebilecegi bir karar
(referans hic yok ve uretilmesi gerekiyor, ya da hedef iki farkli isi ayni anda
tarif ediyor). Eksik dosya, yanlis yol, bozuk kapi **sana ait** — duzelt ve devam et.

> Uc parca: **Gorev** · **Build metodu (fan-out + kritik)** · **Bar (kor karsilastirma)**
> Ucu de olmayan prompt gauntlet degildir; sadece uzun bir istektir.

## Neden ise yariyor

Model kendi ciktisini "yeterince iyi" ilan eder. Ayri bir kritik ajan bu ilani elinden alir.
Fan-out ise her parcaya kendi kritigini verir — kalite tek bir genel degerlendirmeye degil,
parca sayisi kadar bagimsiz redde bagli olur. Dongu de bariyeri **cikis kosulu** yapar,
tavsiye degil.

## Iskelet — her uretici/kritik ajana verecegin sozlesme

```
[GOREV]
<tek cumle, somut cikti. "iyi bir X" degil, "su ekranlari olan, su girdiyi alan X".>

[BUILD METODU]
Hedefi mumkun olan en kucuk bagimsiz parcalara bol. Her parca icin bir alt-ajan calistir.
Her alt-ajanin AYRI bir kritik ajani olsun. Kritik ajan uretimi yapan ajan olamaz.
Kritik gorseli/ciktiyi <REFERANS> ile KOR karsilastirir: hangisi daha iyi, neden.
Kritik acimasiz olacak; "iyi olmus" yetmez, gececekse referansi gectigini gosterecek.
Kritik reddederse uretici ajan somut geri bildirimle yeniden calisir.

[BAR]
Her kritik, kor karsilastirmada ciktiyi <REFERANS>'a esit ya da ustun bulana kadar durma.
Tek bir parca bile kirmizi ise dongu devam eder.
```

`<REFERANS>` **daima somut olmali**: gercek bir urun, gercek bir ekran goruntusu, gercek
bir dosya. "AAA kalite", "profesyonel gorunsun" bar degildir — olculemez.

## Referansi nereden bulursun

Bar somut bir goruntu olmadan olculemez. Dort yol var; sirayla dene:

**0. Kullanici referans verdiyse → onu kullan, baskasini arama.**
Dosya, dizin ya da `refs/` gibi bir klasor verildiyse is bitti. Adlandirmayi bir kez
dogrula (hangi goruntu hangi parcanin bari) ve basla; "daha iyi referans bulayim" diye
tur harcama.

**1. Kullanici bir isim verdiyse → kendin arastir, sorma.**
"Call of Duty gibi", "Zelda gibi", "Linear gibi" dendiginde web'den o urunun ekran
goruntulerini bul ve indir. Internette bolca ornek var; kullaniciya "bana referans ver"
deme. Bulduklarini `refs/` altina kaydet, hangisinin ne icin oldugunu yaz.

**2. Kullanici sadece olayi anlattiysa, isim vermediyse → prompt uret, kullanici uretsin.**
Sen gorsel uretmiyorsun. Kullaniciya **kopyalanabilir gorsel uretim prompt'lari** ver;
kullanici GPT/benzeri bir araca verip goruntuleri sana geri getirir, sen onlari referans
olarak kullanirsin.

Prompt kurallari:
- Tek mesajda **en fazla 10 konu** — fazlasi tek sayfaya birlestirilip ise yaramaz hale gelir.
- Her prompt tek bir kare tarif etsin: kamera acisi, isik, palet, malzeme, kompozisyon.
- Cikti formatini yaz (en/boy orani, arka plan, UI var/yok).
- Numaralandir; kullanici geri getirdiginde hangi goruntunun hangi parcaya ait oldugu belli olsun.
- Ciktiyi tek blokta ver ki toplu kopyalanabilsin.

Kullanici goruntuleri getirdiginde `refs/` altina koy, gauntlet promptundaki `<REFERANS>`
alanina **dosya yollariyla** yaz.

**3. Ikisi de yoksa → mevcut ekran / rakip urun / eski surum** referans olur. Hicbir sey
yoksa gauntlet baslatma; olculemeyen bar, kritigi nazik yapar.

## Adimlar

1. **Hedefi netlestir ve referansi TEMIN ET** (asagidaki "Referansi nereden bulursun").
   Belirsizse tek soru sor, sonra ilerle.
2. **Parcalama eksenini sec.** Ekran bazli · sistem bazli · varlik bazli. Parca sayisini
   yaz; 4-12 arasi tut. Daha fazlasi koordinasyon maliyetini kazanctan buyuk yapar.
   **Ajan sayisi: gerekenden az degil, bir tane fazla da degil.** Parcalar ayni dosyalari
   yazacaksa birlestir; ayni gozle dogrulanacaksa tek kritik birden fazla parcaya baksin.
   Sadece **birbirinden bagimsiz basarisiz olabilen** isler ayri ajan hak eder.
3. **Kritik kriterini yaz.** Her parca icin "neye bakacak" bir cumle: kompozisyon, isik,
   tipografi hizasi, hissiyat, veri dogrulugu. Kritik ne olctugunu bilmezse nazik davranir.
4. **Cikis kosulunu yaz.** Kor karsilastirma sonucu + kac ardisik tur yesil kalmali (2 iyi
   bir sayidir; tek tur sans olabilir).
5. **Promptu tek blok halinde ver.** Aciklama, madde isareti, "istersen sunu da ekleyebiliriz"
   yok. Kullanici bunu kopyalayacak.
6. `--run` verildiyse promptu bu oturumda uygula: parcalari `Agent` ile fan-out et, her uretici
   icin ayri kritik ajan ac, kritik kirmizi verdikce ureticiyi geri bildirimle yeniden calistir.

## Calistirma bicimi

Gauntlet promptu tek bir istekle bitmez; **dongu tasiyicisina** ihtiyaci var:

- **Varsayilan: `/loop` + yuksek effort.** `/loop` bar yesillenene kadar turlari surdurur;
  kaliteyi ajan sayisi degil **effort** tasir. Opus'ta tavan `high` — `xhigh`/`max` kullanma.
  Uretici ve kritik ajanlar `high`; mekanik parcalar (dosya tasima, isim degistirme) `low`.
- `ultracode` **varsayilan degil.** Fan-out'u acar ama ajan sayisini da patlatir; ancak
  kullanici acikca isterse veya is tek baglama sigmayacak kadar buyukse (genis migrasyon,
  coklu repo tarama) kullan.
- `/goal` de calisir ama kabul kriterini calistirilabilir hale getirmeni ister; gorsel
  kalite gibi kor-karsilastirmayla olculen barlarda `/loop` daha az surtunme uretir.

Promptun sonuna cikis kosulunu **yaz**; tasiyici durma karari icin oraya bakar.

## Uretim ortami: kritik kendi gozuyle gormeli

Kritik ajan ciktiyi kendisi yakalayabilmeli. Ortam basina yakalama yolu:

| Ortam | Kritigin gorme yolu |
|---|---|
| Web / prototip | Browser pane + `screenshot` |
| Unity | Unity CLI ile sahne screenshot'i (`docs/unity-cli.md` — GUI'yi computer-use ile surme) |
| CLI / veri | ciktinin kendisi + referans dosya diff'i |

Unity tarafinda kazanci saglayan sey ajanin **degistir → screenshot → karsilastir → duzelt**
dongusunu insan olmadan kapatabilmesi. Screenshot adimi yoksa gauntlet yoktur.

### Kritik BAKAR, OLCMEZ — bunu her kritik brief'ine yaz

Kritik goruntuyu bir kez acar ve **gozuyle** yargilar. Bolge kirpma, yakinlastirma, piksel
ornekleme, renk sayma, "iddia edilen 6px izgarayi dogrulayayim" turu olcum **yasak**.

Sebep olculmus: olcume giren arka plan ajani kilitlenir ve tur **verdiktsiz** yanar — gerekce
yok, ilerleme yok, sadece watchdog. Ustelik gereksizdir: iddia edilen ritim gercekse
**gorunur**; gorunmuyorsa sayilar ne derse desin tasarim olarak basarisizdir.
Tasarim kusuru gorulur, olculmez.

Ureticinin ozetini de kritige **kanit diye verme**. Uretici zaten "her seyi duzelttim" der;
kritik ozeti degil resmi yargilar. Goruntude gorunmeyen iddia, basarisiz iddiadir.

### Varlik politikasini promptta belirt

Iki mod var, ikisi de gecerli, ama **secmeden baslama**:

- **Dis varlik yok** — her sey primitive/sahne araclariyla kurulur. Zor, ama tutarli bir
  gorsel dil cikar ve lisans derdi olmaz.
- **Dis varlik serbest** — modular pack'ler kullanilir; hizli, ama kritik ozellikle
  **yanlis yonlendirilmis / ic ice gecmis** parcalari aramali (bu modun tipik hatasi budur).

Sprite gerekiyorsa uretim yolunu da promptta adlandir (orn. bir sprite uretim skill'i),
yoksa ajan placeholder ile yesil ilan eder.

## Baslatmadan once: kuru kosu — promptun yalan soyleyip soylemedigini olc

Gauntlet'in baslamama sebebi genelde model degil, **promptun adlandirdigi seylerin var
olmamasi**. Ilk turu harcamadan su ucunu dogrula; ucu de dosya sisteminden, hafizadan degil:

1. **Yollar gercek mi.** Prompt kritige "su dosyayi ac" diyorsa, o dosyayi **yakalama
   komutunu calistiran arac** gercekten oraya yaziyor mu? Betigin yazdigi dizin ile
   promptta yazan dizin bir harf bile farkliysa kritik bos klasore bakar ve tur olur.
   **Kaynak dogruluk betiktir, promptun iddiasi degil.**
2. **Sayilar esit mi:** parca sayisi = referans sayisi = yakalama sayisi. Referansi olup
   yakalamasi olmayan parca **hicbir zaman yesillenemez**; o parca icin once yakalamayi
   ekle, sonra donguye sok.
3. **Kapilar bugun yesil mi.** Baslamadan once testi ve yakalamayi bir kez kos. Zaten
   kirmizi olan bir kapi, gauntlet'in urettigi kirmiziyla karisir.

Bu uc kontrol dakikalar surer; atlanirsa saatler yanar.

**Kuru kosu bir teslimat degildir.** Kapilari yesillettiginde tur BITMEZ; ayni turda ilk
parcanin ureticisini baslatirsin. "Artik kosabilir", "`/loop` ile surebilirsin", "hazir"
diye biten bir yanit, gauntlet'i baslatmamis olmanin kibar halidir. Sure ve token uyarisi
**baslarken soylenen tek satirdir**, baslamamak icin gerekce degil.

**Uyusmazligi kullaniciya rapor etme — DUZELT.** Yol yanlissa dogrusuna cevir; bir parcanin
yakalamasi yoksa yakalamayi ekle; kapi zaten kirmiziysa once onu yesillet. Bunlar gauntlet'in
onunde duran isler, gauntlet'in yerine gecen sorular degil. Duzelttigini tek satirda soyle
ve donguye devam et.

**On-kirmizilar kritige degil, OLCULEBILIR kapiya baglanir.** "Kosu 10. gune varmali",
"failed=0", "10 sayfa, hicbiri bos degil" gibi. Bunlar icin ayri kritik ajan acma —
kapinin kendisi zaten yargic.

### Aracin dayattigi sira, planin degil

Bazi araclar ayni proje uzerinde **ikinci bir ornek kabul etmez** (Unity bunun tipik
ornegi). Boyle bir arac varsa parcalari paralel calistiramassin; plan ne derse desin
gercek paralellik sinirini arac koyar. Bunu promptta bastan yaz, yoksa ajanlar birbirinin
kosusunu dusurur ve hata "test kirmizi" diye yanlis teshis edilir.

## Izolasyon — sessiz kopyalama riski

Ajan, ayni makinedeki baska projelerden kod, kontrol semasi ve kamera ayari **kendiliginden**
odunc alabilir; cikti "one-shot" gorunur ama degildir. Temiz bir olcum istiyorsan prompta
sunu koy: *"Sadece bu proje dizinini kullan; baska projelerden referans alma."*
Aksi halde sonucu one-shot diye raporlama.

## Sinirlar — bunu bilmeden calistirma

- **Gauntlet sifirdan baslamaz.** Kotu bir temeli cok pahali sekilde cilalar. Once calisan,
  yonu dogru bir MVP; gauntlet ondan sonra hizlandirici olarak.
- **Pahalidir.** Saatler ve ciddi token. Kullaniciya calistirmadan once sureyi soyle.
- **Kritik gormeden karar veremez.** Gorsel isde kritige ekran goruntusu + referans goruntusu
  ver; metin tarifi kor karsilastirma degildir.
- **Sonsuz dongu riski.** Tur sayisina ust sinir koy (orn. parca basina 6). Sinira dayanan
  parcayi yesil ilan etme — **kirmizi olarak raporla**.

## Cikti

Calisirken: iki satirlik acilis (referans + parca sayisi), sonra tur tur ilerleme —
hangi parca, kacinci tur, kritik ne dedi. Sonunda parca basina yesil/kirmizi tablosu;
kirmizilarda hangi eksenin gecmedigi yazili.

`--prompt-only` ile: tek fenced blok icinde gauntlet promptu, ustunde en fazla iki satir.
