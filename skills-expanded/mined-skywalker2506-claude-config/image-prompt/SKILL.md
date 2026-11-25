---
name: image-prompt
description: "Gorsel uretim promptlarini dogrulanmis formatta yazar: tek mesajda 10 numarali konu, damga en sonda, indirme teker teker. Cikan paleti olcerek dogrular; sepya-yikama ve kolaj tuzaklarini prompt seviyesinde onler. Triggers: image prompt, gorsel prompt, resim promptu, asset prompt, kart gorseli, art prompt, 10 resim, stil arama."
user-invocable: true
argument-hint: "[konu/proje] — orn. 'kart gorselleri' veya 'ikon seti'"
---

# /image-prompt — Image Prompt Generator

Illustration, key art, ikon ve prop promptlarini **tek mesajda 10 numarali konu** formatinda
yazar (damga en sonda); istek bir kez gider, uretim teker teker olur. Uretim sonrasi paleti olcup dogrular.

**Promptu yazdirmakla kalmayip uretimi de calistirmak istiyorsan:**
`/image-run <sohbet adi>` — adi verilen ChatGPT sohbetinde promptu gonderir,
1 dk'da bir kontrol eder, biten gorselleri teker teker indirir.
Bu skill promptu **yazar**, `/image-run` onu **calistirir**; ikisi birlikte kullanilir.

**Bu skill degil, sunun icin:** sprite strip / animasyon / asset-browser hattina asset
uretiyorsan `/asset-prompt-gen` kullan — o config-driven, magenta BG'li, 1×8 strip mantigi.
Bu skill tek kare illustrasyon ve kart gorselleri icin.

---

## Kural −1 — Referans varsa STILI TARIF ETME

**Bu kural otekilerin hepsinden once gelir.** Elde bir referans gorsel varsa
prompt stil tarifi ICERMEZ: yalniz ozne ve kisitlar kalir, stil blogu
BOSALTILIR.

Olculdu: metinle stil tanimlama dort tur surdu ve dordu de iskaladi; referans
dogrudan verilince **tek turda** oturdu. Gerekce, olculmus agirliklar ve
"benzesin" isteginin iki ayri anlami:
**[/reference-style](../reference-style/SKILL.md)**.

Kullanici "buna benzesin" diyor ama referans verilmemisse **referansi ISTE**.
Tarif etmeye kalkma — dort tur boyunca denendi.

---

## Kural 0 — Prompt her zaman Ingilizce

Gorsel uretim modelleri Ingilizce promptta belirgin sekilde daha iyi sonuc veriyor:
sahne tarifi daha isabetli, negatifler daha guclu tutuyor, stil terimleri
("gouache", "alla prima", "atmospheric perspective") karsiligini buluyor.

**Prompt metninin tamami Ingilizce yazilir** — stil blogu, sahne cumleleri,
negatifler, hepsi. Kullaniciyla sohbet Turkce kalir; sadece ChatGPT'ye giden
metin Ingilizcedir. Turkce sahne tarifi yazma, ceviri de yaptirma.

---

## Kural 0.5 — Once EKSIKLERI cikar, sonra uret

Uretime baslamadan once **neyin zaten var oldugunu** diskten oku ve yalnizca
eksikleri kuyruga koy. Var olani yeniden uretmek iki sekilde zarar verir: kota
yakar ve elde duran, onaylanmis bir varligi daha kotusuyle degistirme riski
dogurur.

```bash
# ornek: hedef listesi ile diskteki dosyalari karsilastir
ls art/raw/*.png | sed 's/.*\///' > /tmp/var.txt
# hedefte olup /tmp/var.txt'te olmayanlar = uretilecekler
```

Projede eksik hesabini yapan bir arac varsa (orn. animation-creator'daki
`scripts/eksikler.py`) **once onu calistir**, listeyi elle cikarma.

Kullaniciya gonderilen ozet de eksik listesini soyler: "24 varliktan 6'si eksik,
o 6'yi uretiyorum" — "hepsini uretiyorum" cumlesi, var olani ezmenin habercisi.

---

## Kural 0.5 — Once EKSIKLERI cikar, sonra uret

Uretime baslamadan once **neyin zaten var oldugunu** diskten oku; kuyruga yalnizca
EKSIKLER girer. Var olani yeniden uretmek iki turlu zarar: kotayi yakar ve elde
duran, onaylanmis bir varligi daha kotusuyle degistirme riski dogurur.

```bash
# hedef listesi eksi diskte olanlar = uretilecekler
ls art/raw/*.png | sed 's|.*/||' > /tmp/var.txt
```

Projede eksik hesabini yapan bir arac varsa (orn. animation-creator'daki
`scripts/eksikler.py`) listeyi elle cikarma, **once o araci calistir**.

Kullaniciya verilen ozet de eksik listesini soyler: "24 varligin 6'si eksik, o
6'yi uretiyorum". "Hepsini uretiyorum" cumlesi, var olani ezmenin habercisidir.

---

## Kural 1 — Tek mesajda 10 konu, damga EN SONDA

**Tek mesaj = tek istek. Uretim yine teker teker olur, ama sen 10 yerine 1 istek
gondermis olursun.** Istek sayisini dusurmek onemli: cok sayida arka arkaya istek hem
kotayi hem oturumu zorluyor.

```
Generate 10 separate images, one for each numbered subject below.        <- ILK SATIR
IMPORTANT: output each as its OWN separate image file. Do not combine them into a
grid, contact sheet, collage or single canvas.

STYLE (identical in all 10): <stil blogu — harfi harfine sabit>
LIGHT (identical in all 10): <isik dili>
NEGATIVE (identical in all 10): <negatifler>

1. <konu bir cumle + kadraj notu>
2. ...
10. ...

[CLAUDE — <tarih saat> — <proje>, <tur adi>]                             <- DAMGA, EN SON
```

### Ilk satiri guclendirmeden 10'luk gonderme

Tek basina `Generate 10 separate images` yetmiyor: model onu "on konuyu tek tuvale
diz" diye okuyabiliyor (olculdu 2026-08-16 — on karakter tek siyah tuvalde izgara
halinde dondu, kadraj ve yon talimatlari da o izgarada eridi).

Ilk blok bu uc cumleyi **birlikte** tasimali:

```
Generate 10 separate images, one for each numbered subject below.
Produce them SEQUENTIALLY, one image file at a time: finish subject 1 as its own
image, then subject 2, and so on through subject 10.
IMPORTANT: each output is its OWN separate image file. Do not combine them into a
grid, contact sheet, collage, line-up or single canvas. One single subject per image.
```

"Sequentially / one at a time" cumlesi kritik olan: kolaj, modelin isi **tek uretim
cagrisi** sanmasindan cikiyor. Sirali uretim istendiginde her konu kendi cagrisini
aliyor ve per-konu kadraj/yon talimatlari ayakta kaliyor.

### Damga neden sonda

Bu iki kez yer degistirdi, ikisinin de sebebi olculdu:

1. Damga **en basa** konunca `Generate N separate images` ilk satir olmaktan cikti ve
   model tum istegi tek konu sanip **tek birlesik tuval** uretti (2026-08-09).
2. Bunun uzerine damga ikinci satira alindi, sonra da toplu format tamamen birakilip
   "tek mesaj tek gorsel"e gecildi. **Bu asiri duzeltmeydi:** asil sorun toplu istek
   degil, damganin uretim talimatinin onune gecmesiydi.

Damga **en sonda** dururken toplu format calisiyor: ilk satir uretim talimati kaliyor,
numarali liste kesintisiz okunuyor, damga da liste bittikten sonra geliyor ve hicbir
konuyu golgelemiyor. Damgayi listeye **numarasiz** ve **bos satirla ayrilmis** yaz ki
11. konu sanilmasin.

Damgaya konu/id listesi yazma; proje adi, tarih-saat ve tur adi yeter.

### Parca boyutu — 10 tavan

| Istenen | Nasil gonderilir |
|---|---:|
| 3 gorsel | tek mesajda 3 |
| 10 gorsel | tek mesajda 10 |
| 15 gorsel | once 10, sonra 5 |
| 30 gorsel | 10 + 10 + 10 |

10'dan fazlasini tek mesaja koyma — fazlasi tek contact sheet'e birlesiyor.

### Indirme yine teker teker

Toplu **istek** gonderilir; indirme toplu yapilmaz. Model gorselleri sirayla uretir;
her biri bittikce **tek tek** indirilir ve diskte dogrulanir (`/image-run` 4. adim).
Toplu "seri indir" akisi bir kez ayni seriyi ikinci kez indirdi, bir kez de pozisyon
kaymasi uretti.

### Kolaj gelirse

**Once tespit, sonra karar.** Kolaji indirmeden yakalamanin uc olculmus yolu var;
ekran goruntusune bakmadan once bunlara bak:

| olcut | kolaj isareti |
|---|---|
| `img.alt` metni | "Alti ... Amblemi", "Six ... icons" gibi COKLUK bildiren ad (2026-08-13'te tam boyle yakalandi) |
| donen benzersiz dosya sayisi | Istenen N iken 1-2 dosya dondu |
| en/boy orani | Kare istendi, 3:2 / 2:3 geldi |

Kolaj gorursen o gorseli **indirme** ve `Generate N separate images` formatini
tekrar gondermeyi **bir kez** dene. **Ikinci kez zorlama:** ilk tekrar da kolaj
verirse o tur icin tek-mesaj-tek-gorsele dus. (Once "iki kez dene" yaziyordu;
olculdu, ikinci toplu deneme 5 dakika yakip yine kolaj verdi. Tek tek gonderim
konu basina ~1.5 dk ve %100 ayri dosya dondurdu.)

Tek-tek moda dusunce STYLE/BACKGROUND/NEGATIVE bloklari **harfi harfine ayni**
tasinir; yalniz konu satiri degisir. Bloklari kisaltirsan seri tutmaz.

---

## Kural 2 — Sepya-yikama tuzagi

En sik ve en sinsi failure mode. Su kelimeler **birlikte** yazildiginda model resmi
boyamak yerine ustune tek renk filtre geciyor:

> ❌ `aged paper tint over the whole image` · `warm dust haze` · `low contrast` ·
> `desaturated` · `muted` · `overcast diffused light` · `faded` · `vintage`

Sonuc: tum kareler 35-45° ton bandinda, gorsel *ici* ton yayilimi 5°, golge tonu = isik
tonu. Konusu ne olursa olsun — colde piyade, acik denizde gemi, karanlik sunucu odasi —
hepsi ayni kahverengi. **"AI ciktisi gibi durmak" dedigimiz sey teknik olarak budur.**

**Hastalik doygunluk eksikligi degil, tek filtre.** Karsiti "her seyi ciglastir"
degil; **paleti tasarlamak.** Solgun, tozlu, kirli yesil, gri-mavi, neredeyse tek
renkli bir palet — *secilmisse* ve kendi icinde ton/isi ayrimi tasiyorsa — tamamen
saglikli. Bozuk olan, konu ne olursa olsun ayni kahverengiyi ustune geciren
otomatik filtre.

Yerine yaz — uc parcali:

> ✅ **Isik:** `HDR tone mapping: luminous highlights, deep shadows that still hold
> detail, strong local contrast`
> ✅ **Palet:** projenin kendi paletini **acikca say** — hakim aile, aksan, ne
> olmayacagi. Orn. `a cool grey-green and slate palette, rust and bone as the only
> warm accents` ya da `sun-bleached ochre and chalk white, with deep teal shadow`.
> ✅ **Negatif:** `NO single-hue filter over the whole image, NO sepia or amber
> overlay, shadows must differ in temperature from the lights`

Negatif cumleyi **her zaman** ekle; pozitif tarif tek basina yetmiyor.

### Palet projeye aittir — sablon degil

Bu skill bir oyunun ihtiyacindan cikti ve o oyunun paleti (`vivid saturated colour
led by cool blues and greens`) ornekten cok kural gibi okunmaya basladi. **Oyle
degil.** Her yeni is icin paleti bastan sec:

1. Isin ne oldugunu sor — cozy oyun mu, karanlik survival mi, teknik illustrasyon mu?
2. Referansi varsa oradan cikar; yoksa 3-4 renkten olusan bir aile + 1 aksan yaz.
3. Ayni paleti turun tumune tasi (ortak stil blogu harfi harfine sabit), ama **sahnelerin
   kendi tonu olsun** — magara sicak, nehir soguk. Toplam ton bandini kendin dengele.

Doygunlugu "canli" diye yukseltme; ton *ayrimi* aradigin sey, sat% degil.

---

## Kural 3 — Tek yone asiri duzeltme yapma

Palet duzeltmesi isterken "olabildigince mavi" dedigimizde model **her kareyi gokyuzune**
cevirdi. Bir sonraki tur "abartma" geldi.

Ayni tuzak doygunlukta da var: sepyayi kovalarken "vivid saturated" yazip her kareyi
ciglastirmak da tek yone asiri duzeltmedir ve o da AI ciktisi gibi durur. Kural 2'deki
palet bolumu bunun icin var.

**Cozum:** kadraji sahne bazinda acikca yaz, dagilimi kendin dengele. 10'luk bir tur icin
saglikli dagilim:

| kadraj | adet |
|---|---|
| gok agirlikli (konu zaten gokte) | 2 |
| ic mekan / gok yok | 2 |
| yer seviyesi, ufuk 1/3, gok ust bant | 4-5 |
| yakin plan, ozne kadraji dolduruyor | 1-2 |

Her sahne cumlesine ufuk cizgisinin nerede duracagini yaz: `Horizon one third up; sky only
the top third.`

---

## Kural 4 — Arka plan: konuya gore karar ver

| icerik | arka plan |
|---|---|
| kart illustrasyonu, key art, sahne | **full-bleed** — seffaf degil. Kart plakasi opak, resim icine gomulu duruyor |
| ikon, amblem, kesme obje, portre, prop | **seffaf**: `transparent background, alpha channel, cut out, no backdrop, no shadow on the ground` |
| beyaz/acik VFX (shine, glow, burn, smoke) | **siyah zeminde maske** olarak iste, alpha'yi parlakliktan turet — seffaf isteyince model bosluga uydurma dolgu yapiyor |

Magenta chroma-key **isteme** — bu arac gercek alpha veriyor, magenta gereksiz ara adim.

---

## Kural 5 — Metin yok

Hicbir promptta baslik, wordmark, birlik isareti, rakam, logo, watermark isteme. Model
harfleri bozuyor, cikti kullanilamiyor. Wordmark ayri compositing adimi.

Her stil blogunun sonuna:
`Absolutely no text, letters, numbers, unit markings, logos or watermarks.`

---

## Kural 6 — Ictirik politikasi tetikleyicileri

`/asset-prompt-gen` icindeki tetikleyici kelime tablosu burada da gecerli — `battle damage`
→ `surface wear`, `muzzle flash` → `ignition flare`, `scorched` → `soot stain` vb. Askeri
konularda promptun tamami reddedilebiliyor; gorsel/mekanik dilde kal.

---

## Kural 7 — Sonradan ANIMASYON uretilecekse form bastan degisir

Bir karakter/yaratik gorseli ileride I2V ile canlandirilacaksa (bkz. `/animate`),
gorselin **yonu, pozu, kadraji ve zemini** o anda karara baglanir. Model verilen kareyi
canlandirir, **icerigini degistiremez**: onden bakan bir figure yuruyus, kilic tutan bir
figure silahsiz saldiri, cuppeli bir figure adim verilemez. Sonradan duzeltilmiyor —
sprite yeniden uretiliyor.

Tam standart ve kabul kapisi: **`~/.claude/skills/animate/animation-ready-sprite.md`**.
Prompt yazarken zorunlu ozet:

| | |
|---|---|
| Yon | **screen-right**, govde yan 3/4 (~20-30 derece kameraya donuk). Sol taraf uretilmez, runtime flip |
| Poz | notr dovus durusu; ayaklar ayrik, kollar govdeden ayrik. T/A-pose degil, donmus aksiyon degil |
| Bacak | yuruyecekse ayak bilegi + alt bacak gorunur |
| Silüet | kol-govde, bacak-bacak arasinda negatif bosluk; pelerin/sac govdeye yapisik degil |
| Kadraj | tam boy, ~%6 pay, ortalanmis, ayak tabani sabit taban cizgisinde |
| Zemin | **duz saf siyah**; gradient/zemin plakasi/temas golgesi yok |
| Isik | duz onden; sert rim/arka isik yok |
| Efekt | motion blur / partikul / aura / emissive tasma yok — emissive ayri maske |
| Tek figur | kolaj, contact sheet, bust, uzuv parcasi animasyon kaynagi olamaz |

Bu tur icin **Kural 4'un "seffaf zemin" satiri gecersizdir** — animasyona girecek
karakter siyah zeminde uretilir. Saydami model boslugu uydurarak dolduruyor.

Metin yasagi (Kural 5) burada iki kat onemli: sprite flip edildiginde harf ters okunur.

Ingilizce prompt karsiligi — ortak blogun icine harfi harfine:

> `Full-body character, facing screen-right, body turned to a side three-quarter view
> about 25 degrees toward camera. Neutral combat stance, feet apart, arms clear of the
> torso, knees slightly bent. Ankles and lower legs visible. Whole figure inside frame
> with even margin, feet resting on a consistent baseline, centred. Flat pure black
> background, no floor, no contact shadow, no gradient, no vignette. Even frontal
> lighting, no strong rim or backlight. One single figure only. No motion blur, no
> particles, no glow spill outside the silhouette. Absolutely no text, letters, numbers
> or logos.`

---

## Uretim sonrasi — olc, goz karari verme

Cikti geldiginde paleti **olc**. Goz "iyi gibi" der, sayi yalan soylemez.

```bash
python3 ~/.claude/skills/image-prompt/check_palette.py ~/Downloads/*.png
```

Ciktidaki dort sayi:

| olcum | saglikli | bozuk |
|---|---|---|
| ton yayilimi (spread) | 30-60° | **< 10° = tek renk filtre** |
| golge tonu vs isik tonu | belirgin fark | **ayni = sicak/soguk ayrimi yok** |
| gok B−R (ust ucte) | pozitif (mavi) | **negatif = gok kirmizi, sepya** |
| deger araligi | > 55 | < 40 = duz |

**`sat%` bir kapi degil.** Tabloda yok cunku gecme sarti degil; sadece bilgi. Solgun
bir palet dusuk sat% verir ve bu **basarisizlik degildir** — spread ve sicaklik ayrimi
tutuyorsa palet saglamdir. Doygunlugu sirf sayi yukselsin diye artirma.

**`WARM-SKY` sahnede gok varsa anlamlidir.** Bayrak karenin ust seridini olcer; magara
ici, yakin plan ve altin saat sahnelerinde ust serit zaten sicaktir. Once "bu karede gok
var mi?" diye sor, sonra bayragi ciddiye al.

Turun gorselleri **arasindaki** ton farkina da bak: 10 farkli konu 15° bandina
sikismissa palet tasarlanmamis, filtrelenmis demektir. Genis ton bandi da tek basina
hedef degil — proje bilincli olarak dar bir palet secmis olabilir; o zaman **kare ici**
spread ve sicaklik ayrimina bak.

Kurtarma: `check_palette.py --grade` split-tone uygular (golgeleri soguga ayirir, cast'i
kaldirir, vibrance ekler). Ama **var olmayan rengi icat edemez** — baştan tek tonda uretilmis
kareyi ancak cilalar. Yapisal olarak bozuk olani yeniden uret.

---

## Teslim formati

- Tur basina **tek fenced blok**: ortak stil/isik/negatif basligi + numarali konu listesi + sondaki damga
- Prompt **Ingilizce**; sohbet Turkce
- Blogun disinda numarali dosya adi eslemesi: `1 push, 2 resupply, 3 mobilize, ...`
- Kullaniciya sirayi ve "icerige bakarak esle" notunu hatirlat

---

## Cikti bir prototipe baglanacaksa

Gorseller geldiginde: WebP'ye cevir, veri dosyasina `art` alani olarak bagla, tek-dosya
build'de base64 goml. Harici istek birakma.

```bash
cwebp -q 82 in.png -o out.webp     # ~%80 kucultme, kart boyutunda fark gorunmuyor
```

---

## Calistir

```bash
echo "Konu: ${1:-<belirtilmedi>}"
echo ""
echo "1. Konuyu 10'luk turlara bol (goruntuleme sikligina gore onceliklendir)"
echo "2. Stil blogunu yaz — Kural 2'deki yasak kelimeleri kullanma"
echo "3. Kadraj dagilimini Kural 3'teki tabloya gore dengele"
echo "4. Tek fenced blok halinde teslim et, dosya eslemesini disinda ver"
echo "5. Cikti gelince: python3 ~/.claude/skills/image-prompt/check_palette.py <dosyalar>"
```
