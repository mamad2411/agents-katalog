---
name: polish
description: "Kosan ve eglenceli oldugu kanitlanmis bir prototipi cilalar: sanat uretim hatti ve sprite prompt'lari, shader katmani, ses kimligi ve aranjman, gorsel konfor, performans ve UI hizasi. Her cila iddiasi olcumle kanitlanir. Triggers: polish, cila, cilala, prototipi gelistir, sprite prompt, shader ekle, ses polish, gorsel polish, performans polish, juice artir."
user-invocable: true
argument-hint: "[alan: sanat | shader | ses | konfor | performans | ui | hepsi]"
---

# /polish — kosan seyi iyi yap

`/prototype` "bu fikir eglenceli mi" sorusuna cevap verdi. Bu skill baska bir soruyu
cevaplar: **"eglenceli ama ucuz duruyor / kulagi rahatsiz ediyor / takiliyor" nasil gecer.**

> Olculmus > Gorunen · Tek gecis > Yuz kucuk dokunus · Kimlik > Efekt

## Ne zaman bu skill, ne zaman /prototype

| Durum | Skill |
|---|---|
| Cekirdek dongu henuz oynanmiyor | `/prototype` |
| Oyun oynaniyor ama "eglenceli mi" cevaplanmadi | `/prototype` |
| Dongu oynaniyor, kullanici eglenceli buldu, artik **derinlestirme** isteniyor | **`/polish`** |
| Yeni sistem / yeni mekanik / kapsam buyumesi | `plan-build` |

**Uc kosul birden saglanmadan bu skill'e gecme:** (a) cekirdek dongu oynaniyor,
(b) kullanici oynadi ve "eglenceli" dedi, (c) gelen istekler yeni mekanik degil
**var olani iyilestirme**. Sagalanmadiysa `/prototype`'a don.

---

## Degismeyen kural: her cila iddiasi OLCUMLE kanitlanir

Prototipte "bak ve gor" yeterliydi. Cilada yetmez, cunku cilanin coğu **yokken de
ayni gorunur**. Olculmus vaka: sprite flip kodu bastan sona yazilmisti, dogruydu ve
**tamamen oluydu** — `THREE.Sprite` negatif olcegi yok sayiyor. Tek kare ekran
goruntusunde "cevrilmemis sprite" ile "cevrilmesi gereken ama cevrilmeyen sprite"
ayni seydir. Kullanici oynayana kadar fark edilmedi.

| Cila turu | Kanit |
|---|---|
| Durum degistiren gorsel (flip, aktif/pasif, secili, vurgu) | **Iki durumu da yakala ve karsilastir.** Fark yoksa ozellik yok |
| Ses | Master bus'ta tepe ve RMS. Tepe < 0.7 duyulmuyor, > 0.98 kirpiyor |
| Performans | Draw call + ucgen + medyan kare suresi, **once ve sonra** |
| Konfor | Ayar acik/kapali iki kayit; kapaliyken oyun hala okunakli mi |
| Hiza / yerlesim | Kutu ile gorselin ic dikdortgeni piksel olarak; goz karari degil |

"Yaptim" kanit degildir. "Olctum, su cikti" kanittir.

---

## 1 · Sanat uretim hatti

Kullanici gorselleri kendi uretiyor (GPT/AI). Senin isin **prompt vermek** ve
**gelenleri hatasiz gomek**. Kod yazmadan once hattin kendisini kur.

### Prompt paketleme

- **10'arli batch.** Tek mesajda 10 prompt ver; kullanici tek tek uretip toplu indirir.
- Her prompt **kopyalanabilir tek blok** olmali — aciklama prompt'un icine karismasin.
- Batch icinde **tek stil cumlesi** tekrarlanir (palet, isik yonu, kenar, cerceve).
  Stil cumlesi degisirse batch tutarsizlasir.
- Her prompt sonunda teknik kisit: arka plan, cozunurluk, kadraj, kirpma payi.

Sablon:

```
[konu] · [poz/aci] · [karakteristik detay]
Stil: [batch'in ortak stil cumlesi — DEGISTIRME]
Arka plan: [seffaf | duz koyu | tam kadraj]
Kadraj: [tam govde, ayaklar alt kenarda | merkezde, %10 pay]
Cozunurluk: kare, en az 1024
Metin, yazi, imza, watermark YOK
```

### Olculmus prompt tuzaklari

- **Seffaf + beyaz konu birlikte calismaz.** AI seffaf isteyince beyaz bolgeleri de
  siler. Beyaz/acik konularda duz koyu arka plan iste, sonra kodda kes.
- **Ic bosluk isteyen cerceve gelmiyor.** "Ortasi bos suslu cerceve" uc denemede de
  dolu geldi. Cozum promptta degil kodda: dolguyu cercevenin **ustune** katman olarak koy.
- **Kart/plaka gorselinde gomulu kenarlik varsa** o gorsel degisken icerikte kullanilamaz.
  Ya oranini sabitle ya da duz renk + CSS'e dus.
- **Toplu gelen dosyalar sirasiz ve eksik gelir.** Isme gore degil **gorsel icerige gore**
  esle. Bozuk dosyayi tartisma, at ve yerine tek prompt daha ver.
- Batch bitince **eksik olan var mi** diye tek tek dogrula, isim listesiyle degil boyutla.

### Ingestion — elle degil, script

Gelen gorseller **her zaman** ayni hattan gecer. Elle adim birakma; ikinci batch geldiginde
hatirlamayacaksin.

```
trim (seffaf/duz kenar kirp) -> kenar temizligi -> LANCZOS resize
-> webp -> base64 data URI -> uretilmis JS modulu
```

- Script `tools/` altinda dursun, tek komutla tum klasoru islesin.
- Cikti **uretilmis dosya**dir, elle duzenlenmez.
- Boyut tavani koy ve her calistirmada yazdir. Olculmus: 60 gorsel, WebP + trim ile
  toplam build 3,3 MB — kabul edilebilir. PNG ile ayni set 4 katiydi.
- Import tipi sessiz null uretebilir; yukleme sonrasi **kac gorsel yuklendi** say ve logla.

---

## 2 · Shader katmani

Prototipte sprite tek kare cizimdir. Cila, ona **kod yazarak hareket ve tepki** verir —
ek doku, ek dosya, ek draw call olmadan.

> **Bu alanin tam katalogu ayri bir skill'de: `/juice`.** Asagisi ozettir; is
> gercekten shader/efekt/oyun hissi ise (squash, yuruyus, hit flash, hitstop,
> kamera sarsintisi, aura, simsek, cozulme, havuzlanmis efekt katmani) once
> `/juice`'u yukle — calisan koddan cikarilmis tarifler, olculmus sayilar ve
> "hangi katmana yazilir" karari orada. `/polish shader` cagrildiginda oraya gec.

### Ne kazandirir

| Efekt | Nasil | Maliyet |
|---|---|---|
| Yon cevirme | UV'de `u = 1 - u` | sifir |
| Nefes / salinim / surunme | UV'yi zamanla kaydir | sifir |
| Vurus parlamasi | Alfanin `fwidth`'i = siluet kenari | ek doku okumasi yok |
| Olum cozulmesi | Deger gurultusu esigi + `discard` | sifir |
| Darbe itmesi | UV'yi darbe yonunde kaydir | sifir |

### Kirilmadan yazmanin kurallari

1. **Tek `onBeforeCompile` fonksiyonu.** three, program onbellegini fonksiyonun
   **kaynak metniyle** anahtarliyor. Ayni fonksiyon nesnesi kullanilirsa tum sprite'lar
   tek programi paylasir; sadece uniform DEGERLERI farklidir. Her sprite'a ayri closure
   verirsen her sprite ayri program derler.
2. **Dallanma uniform uzerinden.** Bir draw call icinde uniform sabittir, yani
   "uniform control flow" — `fwidth`/`texture` guvenlidir ve dal alinmazsa maliyet sifira yakin.
3. **Ikinci bir efekt eklerken hook'u ezme.** Ikinci `onBeforeCompile` ataması birinciyi
   siler. Tum efektler tek hook'ta, ayri uniform'larla yasar.
4. **Sifir degeri notr olsun.** `uWobA = 0` iken hicbir sey olmamali; boylece efekti
   olmayan nesneler ayni programi kullanip hicbir bedel odemez.
5. **Negatif olcek sprite'ta calismaz.** `sprite_vert` olcegi `length(modelMatrix[0].xyz)`
   ile alir, isaret kaybolur. Cevirme **doku uzayinda** yapilir.

### Izometrik kamerada aci

Ekran yonu dunya yonu degildir. Hizi kamera eksenlerine izdusur:

```
sx = v · camRight      sy = v · camUp      aci = atan2(sy, sx)
```

`atan2(-vz, vx)` izometride **45 derece yanlistir**. Kameranin yonu sabitse
quaternion'i bir kez sakla ve instance matrisine dogrudan yaz.

---

## 3 · Ses cilasi

Prototipte ses "var mi" sorusuydu. Cilada uc ayri soru var: **duyuluyor mu**,
**kimligi var mi**, **kalabalikta dagiliyor mu**.

### Duyuluyor mu — olc

Master bus'a analyser tak, 1 saniye ornekle, tepe ve RMS yazdir. Olculmus vaka:
"hic ses yok" sikayeti; RMS 0.018 cikti. Master 0.9'a, lowpass yukari, limiter eklendi;
RMS 0.123 oldu, tepe 0.91, kirpma yok. Tahminle degil olcumle cozuldu.

- Tepe < 0.7 → duyulmuyor, kazanci ac.
- Tepe > 0.98 → kirpiyor, **limiter** (DynamicsCompressor) ekle, kazanci dusurme.
- Ust uste binen ses sayisina tavan koy ve tavani **gercekten uygula**. Olculmus:
  config'de `maxNotesPerTick` vardi ama koda hic okunmuyordu.

### Kimlik — tini kaynaktan gelsin

Yaygin hata: sesi **olaya** bagliyorsun (hangi kart/silah), oysa oyuncu **kimin**
caldigini duymak istiyor. Ayir:

```
playNote(kaynak, artikulasyon, t, ...)
  kaynak       -> tini (karakter/enstruman/silah ailesi)
  artikulasyon -> ifade (olayin karakteri: vurgu, uzun, kisa, parlak)
```

Yeni kaynak eklemek tek tablo satiri olmali. Boyle ayirmazsan farkli karakterler ayni
sesi cikarir ve kullanici "lirciden davul cikiyor" der.

### Kalabalikta dagilmasin

Cok sesli bir sistemde herkes ayni ezgiyi kendi hizinda okursa **ritim dagilir**.
Olculmus duzeltmeler:

- **Tek ezgi isaretcisi.** Herkes kendi isaretcisini tuketirse iki bar sonra herkes
  parcanin baska yerini calar. Tek isaretci ana sesin vurusunda ilerler; digerleri
  o anki notadan **kendi roluyle** perde turetir (melodi / bas / kontra / sus / armoni).
- **Gama kilitle.** Armoni ve bas seslerini gama snap'le; ezginin kromatik notasi tek
  hatta guzeldir, ust uste binince kucuk ikili yigini olur.
  Olculmus: sert aralik orani %6,8 → %3,8; es zamanli nota cifti 1888 → 612.
- **Yeni ses ana izgaraya otursun.** Sonradan katilan bir ses `now + 0.1`'de baslarsa
  rastgele faz kaymasiyla girer. Mevcut ana sesin bir sonraki vurusuna hizala.
- **Ileriden planlamada indeks turetilmis olsun.** Ses ileriden planlanirken mutasyonla
  ilerleyen sayac kayar; indeksi **vurus sayisindan** turet.
- **Eko/reverb'i register'a gore gonder.** Hizli ve tiz sesler ayni ekoya girerse
  bulamac olur.

### Konfor

Ses de yorar. Ayni ses ust uste calinca perde varyasyonu ekle; surekli calan yuksek
frekansli katmanlari kis; sessizligi bir arac olarak kullan — **beklenen sesin gelmemesi**
en temiz olumsuz geri bildirimdir ve cirkin ses uretmeden calisir.

---

## 4 · Gorsel konfor butcesi

Juice'un yazari her zaman fazla ayarlar, cunku efekti yaparken yuzlerce kez gorur.
Olculmus: goz yorulmasi ve mide bulantisi sikayetleri; flash/shake ~0,42x'e cekildi,
kamera nabzi **varsayilan kapali** yapildi, kamera takibi sikilastirildi.

| Kanal | Tavan | Ayar |
|---|---|---|
| Ekran sarsintisi | yalniz buyuk olaylarda, kucuk genlik | acik/kapali |
| Ekran parlamasi | kisa sonum, dusuk opaklik | acik/kapali |
| Kamera nabzi (vurus zoom'u) | **varsayilan KAPALI** | acik/kapali |
| Vurus donmasi (hitstop) | ≤ 100 ms | acik/kapali |
| Bloom | esik yuksek tutulsun, sahneyi doldurmasin | acik/kapali |
| Partikul | havuz tavani sabit | azalt secenegi |

Iki ek kural:
- **Kamera yonu sabit kalsin.** Takip ederken `lookAt` cagirirsan pozisyon geriden
  geldigi icin bakis acisi kayar ve izometrik sahne egilir. Quaternion'i bir kez sakla,
  her karede kopyala.
- **Renk tek gosterge olmasin.** Zamanlama/durum kalitesi metin + sekil + olcek + ses ile de anlasilsin.

---

## 5 · Performans

Cila asamasi, prototipin "calisiyor" kodunun **olceklenmedigi** yerdir. Once olc, sonra dokun.

### Once teshis

`renderer.info.render` ile draw call ve ucgen, `performance.now()` ile medyan kare suresi.
**Uyari:** `renderer.info` her `render()` cagrisinda sifirlanir; post-processing varken
son deger sana kompozisyon gecisini gosterir. `autoReset = false` yap, kendi dongunde
oku ve sifirla.

### Yaygin darbogazlar — sirayla kontrol et

1. Nesne basina ayri mesh / ayri materyal (sprite'lar en sik suclu)
2. Draw call'un nesne sayisiyla dogrusal artmasi
3. Her karede yeni `Vector3` / `Matrix4` / dizi uretimi
4. Havuzsuz olustur-yok et dongusu (GC tirmalari)
5. Nesne basina tum dusmanlari tarayan carpisma
6. Kullanilmayan nesnelerin sahnede aktif kalmasi
7. Gereksiz isik, golge, pahali materyal

### Cozumler

- **Tip basina tek `InstancedMesh`.** Konum/donus/olcek instance matrisinden;
  renk `instanceColor`'dan. `needsUpdate` **grup sonunda bir kez**.
- Kamera yonu sabitse billboard'i instance matrisine gom: `camQuat × rotZ(aci)`.
  Sprite'in yapamadigi per-instance donusu boylece kazanirsin, ustelik tek draw call.
- **Havuz**: kayit nesnelerini de havuzla, sadece mesh'i degil.
- **Mekansal izgara**: hucre boyu ~ sorgu yaricapinin 2-4 kati; kare basina bir kez kur.
- Gecici matematik nesnelerini modul seviyesinde bir kez ayir.
- Mermi/partikul: `castShadow = false`, `receiveShadow = false`, basit materyal.

### Sonra olc — ayni tabloyla

| Aktif nesne | Draw call | Ucgen | Medyan ms |
|---|---|---|---|

Olculmus ornek: 0 / 50 / 500 / 1000 mermide draw call **49 / 51 / 49 / 51** — yani
mermi sayisindan bagimsiz; ucgen dogrusal; 1000 mermide medyan 8,5 ms. Iddia degil, tablo.

---

## 6 · UI ve yazi hizasi

Suslu cerceve gorselleri cilanin en sinsi alanidir: **yanlis oldugunda da makul gorunur.**

- **Cerceve gorseli degisken icerigi saracaksa `border-image` 9-slice kullan.**
  `background-size:100% 100%` ile esnetme yalnizca kutu gorselin oranini koruyorsa gecerli.
  Olculmus: panel gorselinin kenari yuksekliginin ~%50'siydi; uzun kutuya esnetilince
  kenar kalinlasti, sabit padding'li yazi kenarin ustune bindi.
- **Gorselin ic dikdortgenini olc, tahmin etme.** Alfa/luminans profili cikar, padding'i
  ondan turet. Plaka gorselin dikey ortasinda olmayabilir — dugme gorselinde plaka
  merkezi yuksekligin %60'indaydi, yazi bu yuzden yukarida duruyordu.
- Cok dilli/uzun etiketlerde satir kirilmasini kapat, kutu genisligini icerige gore ac.
- Tum ekranlari **tek tek** gez ve yakala. Bir ekranda dogru olan hiza digerinde bozuk olabilir.

---

## 7 · Ajan kullanimi — burada serbest

`/prototype` ajan kullanimini kasitli olarak kisitlar. Cila asamasinda kisit kalkar,
cunku isler **birbirinden bagimsiz** ve arayuz zaten kurulmus:

| Is | Ajan | Effort |
|---|---|---|
| Sanat prompt'u uretme / batch hazirlama | evet | low |
| Shader efekti yazma | evet | low-medium |
| Performans profilleme ve optimizasyon | evet | medium |
| Hata ayiklama | evet | low |
| **Kendi degerlendiremeyecegin alanda tasarim danismanligi** (muzik aranjmani, renk teorisi, erisilebilirlik) | evet | medium |
| Cekirdek oynanis degisikligi | **hayir** | — |

Son satir onemli: cila oynanisi **degistirmez**. Hasar, hedefleme, carpisma, sure,
pierce, alan etkisi ve hit davranisi aynen korunur. Degisen sey sadece nasil gorundugu,
duyuldugu ve ne kadar hizli kostugu.

---

## Yapma

| Yapma | Maliyet |
|---|---|
| Cilayi olcmeden "yapildi" demek | Sprite flip bastan sona oluydu, kullanici bulana kadar fark edilmedi |
| Modul kaynagini test edip teslim edilen build'i test etmemek | Duzeltilmis bug duzelmemis gorunur; tarayici modul onbellegi eski dosyayi servis eder |
| Sayisal alani `undefined` birakmak | Bir kare sonra NaN olur; AudioParam'a giderse rAF icinde exception atar, sahne kararir, HUD calismaya devam eder |
| Ikinci `onBeforeCompile` atamak | Birinci efekt sessizce silinir |
| Cerceve gorselini her kutuya esnetmek | Yazi kenarin ustune biner, uc turda duzelir |
| Ayni anda hem sanat hem oynanis degistirmek | Bozulan hangisi belirsizlesir |
| Cila sirasinda yeni mekanik eklemek | O `plan-build` isidir; cilayi bitir, sonra gec |

## Teslim

1. Calisir build + tek satirlik calistirma komutu
2. **Once/sonra olcum tablosu**: draw call, ucgen, kare suresi, ses tepe/RMS
3. Degisen dosyalar ve her birinde ne degisti
4. Yeni sanat nasil eklenir (prompt sablonu + ingestion komutu)
5. Bilinen sinirlar ve hala acik teknik riskler

> Teshis: **siyah sahne + calisan HTML HUD = render dongusu oldu.** Once konsol, sonra renderer.
