---
name: showrunner
description: "Bir oyun fikrini tek komutla BITMIS oyuna cevirir. Perde 1 (etkilesimli): 10 stil uret -> kullanici secer -> secilen stilde sahne gorselleri (1-2 tur, onay) -> tek soru turu -> 'Basliyorum'. Perde 2 (otonom): bir daha soru sormadan multi-agent uretim — plani Fable+Opus tartisir, kodu Opus yazar, cekirdek oyun + tam asset seti + ses kimligi + polish + funscore kapisi, tek dosya teslim. Triggers: showrunner, bastan sona oyun, tek komutla oyun, oyunu bitir, full oyun uret, sifirdan oyun yap, oyunu son haline getir."
user-invocable: true
argument-hint: "[GDD dosya yolu veya oyun fikri] veya [status|resume]"
---

# /showrunner — tek komut, bitmis oyun

> Model yonlendirmesi: global/model-routing.md

`/prototype` "bu fikir eglenceli mi" sorusunu cevaplar ve durur. `/polish` kosan seyi
iyilestirir. Bu skill ikisini ve sanat hattini **tek akista birlestirir**: basta stil ve
sahne gorselleriyle gorsel kimligi kullaniciya SECTIRIR, kalan tum kararlari tek soru
turunda toplar, sonra **"Basliyorum" der ve bir daha hicbir sey sormadan** oyunu son
haline getirir: Three.js + Web Audio, gercek sanat, cila, tek dosya teslim.

> Perde 1 = sorular · Perde 2 = sifir soru · Teslim = cift tikla acilan tek dosya

## Hangi skill ne zaman

| Durum | Skill |
|---|---|
| Ortada fikir bile yok — "hangi oyunu yapayim?" | [`/greenlight`](../greenlight/SKILL.md) |
| "Fikir eglenceli mi" hala belirsiz, hizli kanit lazim | `/prototype` |
| Kosan prototip var, derinlestirilecek | `/polish` |
| Fikirden **bitmis, cilali, gorselleri gercek** oyuna tek komutta | **`/showrunner`** |

Bu skill alt skill'leri **calistirir**, kurallarini yeniden yazmaz. Her fazda ilgili
SKILL.md'nin adi gecen bolumu okunur ve oradaki kurallar aynen uygulanir:
[/prototype](../prototype/SKILL.md) · [/polish](../polish/SKILL.md) ·
[/image-prompt](../image-prompt/SKILL.md) · [/image-run](../image-run/SKILL.md) ·
[/plan-build](../plan-build/SKILL.md) · [/goal](../goal/SKILL.md) ·
[/funscore](../funscore/SKILL.md) · [/sprite-parallax](../sprite-parallax/SKILL.md)

## Sozlesme — soru perdesi

**Perde 1'in isi kullanicidan karar toplamaktir; Perde 2'de karar sormak yasaktir.**

- Perde 1: konsept onayi, stil secimi, sahne onayi, soru turu. Bloklayan adimlar
  yalnizca burada yasar; bir onay kapisi tikanirsa (orn. sahne redosu tavani doldu)
  kullaniciya **burada** sorulur — kapiyi kendi kendine onaylamak yasaktir.
- Perde 2: `AskUserQuestion` cagrilmaz, onay beklenmez, "ister misin?" yazilmaz.
  Karar gerekirse makul varsayilan secilir ve `.showrun/decisions.md`'ye tek satir
  yazilir. Kullanicinin uretebilecegi ama senin uretemeyecegin girdiler (insan
  playtest'i, hesap bilgisi, urun karari) `/goal`'daki `blocked_by_human`'a gider,
  dongu durmaz, sonda acikca listelenir.
- Kullanici Perde 2 sirasinda mesaj yazarsa cevap verilir ve isaret ettigi sey
  duzeltilir — yasak olan senin soru ACMAN, onun konusmasi degil.

## Durum dosyalari

```
.showrun/
  brief.md        kilitlenen her sey: GDD ozeti, stil blogu (harfi harfine), sahne
                  listesi, soru turu cevaplari, kapsam zarfi
  ART.md          tam asset envanteri (id + tek cumle), durum kolonu: gercek |
                  placeholder | eksik | insan-kilidi
  decisions.md    Perde 2'de varsayilanla verilen kararlar, tek satir + gerekce
  log.md          faz gecisleri, gorsel/tur durumlari, olcumler
.goal/criteria.json   kabul kriterleri (Perde 2 Faz A'da yazilir)
```

**Yazma disiplini — status/resume buna dayanir:**

- Her kapida onaylanan cikti, onay mesajindan **hemen sonra** `brief.md`'ye yazilir
  (G0 ozeti, G1 stil blogu, G2 sahne listesi + onay notu, G3 cevaplar).
- Her faz girisinde/cikisinda ve her gorsel gonderim/indirme durumunda `log.md`'ye
  tek satir eklenir (faz / gorsel id, zaman, sonuc).
- `status` bu dosyalardan ozet cikarir; `resume` `log.md`'nin son satirindan devam
  eder — inmis gorselleri yeniden uretmez, biten paketleri yeniden calistirmaz
  (`.plan-build/` ve `.goal/` kendi durumunu zaten tasir).

**Calisma dizini ve repo:** icinde bulunulan proje. ClaudeHQ'dan fikirle cagrildiysa
once `~/Projects/<oyun-adi>` olustur (`hq new` akisi), orada calis. G0 onayindan hemen
sonra repo hattini kur — Perde 2'nin commit noktalari buna dayanir:

1. Repo yoksa `git init` + ilk commit.
2. Remote yoksa **private** GitHub reposu ac ve bagla:
   `gh repo create <oyun-adi> --private --source . --remote origin --push`
   Gorunurluk pazarlik konusu degil: oyun repolari private acilir.
3. **GitHub Desktop'a ekle:** `open -a "GitHub Desktop" <proje-yolu>` — Desktop kurulu
   degilse atla ve rapora tek satir yaz, akisi bloklamaz.

Bundan sonra her commit noktasi **commit + push** demektir; push'suz commit birikmez.

---

# PERDE 1 — Etkilesimli kapi

## G0 — Konsept kilidi

`/prototype` Faz 0 aynen: GDD verildiyse oku ve bir paragrafla ozetle; sadece fikir
verildiyse **tek sayfa GDD'yi sen yaz** (tur ve referans oyun · cekirdek dongu ·
oyuncunun ana eylemi · kazanma/kaybetme · ton · kamera) ve onaya sun. Bu kapi
bloklar cunku stil aramasi oyunun ne oldugunu bilmek zorunda — tasarim yolda
degisirse 10 stil denemesi bosa uretilmis olur, kota gider.

Baska soru sorma — kapsam ve tur sayisi sorulari ileride kendi yerlerinde. Onaydan
sonra ozet `brief.md`'ye yazilir ve G1 **hemen** tetiklenir.

## G1 — Stil turu: 10 stil, tek sahne

`/prototype` "Adim 1 — Stil arama" formati aynen: **ayni sahne, 10 farkli stil**.

- **On stil tek mesajda** gider (`/image-prompt` Kural 1): numarali liste + ortak sahne
  blogu + **damga en sonda**. Uretim sirayla olur, indirme teker teker; istek sayisi
  10 kat duser.
- **Sahne oyun ici goruntu gibi kadrajlanir**: oyunun kamerasi, oyunun kompozisyonu,
  bagimsiz bir illustrasyon gibi degil. Secilen sey oyunun nasil gorunecegidir. Sahne
  oyuncunun en cok bakacagi ekran olmali (genelde ana oynanis ekrani).
- **On stil projenin kalite barinda olmali.** Hepsi ayni uretim degerinde gorunmezse
  secim on secenek arasindan degil, birkac ciddi secenek arasindan yapilir.

Prompt `/image-prompt` kurallariyla Ingilizce yazilir, `/image-run` ile arka plan
ajaninda (`agy (Gemini)`, `effort: low`) uretilir ve indirilir. Gorsel uretim icin izin
istenmez — uretim kararlari G0 onayiyla verilmis sayilir.

Inen 10 kareyi **numaralayarak** goster, sectir. Ayni mesajda tek ek soru:
**sahne turu 1 mi 2 mi** (10 mu 20 gorsel mi)? Sahne cesidi 6'dan fazlaysa 2 oner.

"3 ve 7 karisimi" gelirse iki stil blogunu birlestir, tek cumlelik onay al. Kullanici
hicbirini begenmezse **bir kez** yeni 10'luk tur at; ikinci turdan sonra secim
kilitlidir (`/prototype` "ucuncu stil turu" kurali — kota).

Secilen stil blogu `.showrun/brief.md`'ye **harfi harfine** yazilir. Bundan sonraki
her prompt onu aynen kopyalar; tek kelime degisirse set ikiye bolunur.

## G2 — Sahne turlari: 10 ya da 20

Kilitli stille, oyunun **farkli sahnelerini** uret. Sahne listesini GDD'den sen cikar:
ana oynanis ekrani (varyantlariyla) · baslangic/menu arka plani · kilit anlar (kazanma,
kaybetme, seviye atlama) · ortamlar/bolgeler · ana karakter(ler) yakin plan. Oyun
**alan bazliysa** (oda/bolge ekranlari: mutfak, kazan dairesi, ambar gibi gidilebilen
yerler) her alan **ayri sahne olarak** uretilir — bunlar Faz D'de parallax derinlik
alacak gorsellerdir, tam kadraj ve tek bakis acisiyla iste.

G1'de secilen tur sayisina gore 10 ya da 2x10 = 20 gorsel; **her tur tek mesajdir**
(10 numarali sahne, ortak stil blogu, damga en sonda). Uretim sirayla olur; her gorsel
bittikce **teker teker** indirilir ve diskte dogrulanir. Bir tur tamamen inmeden sonraki
turu gonderme.

Inen kareleri sahne adlariyla etiketlenmis **tek kontak sayfasi** olarak goster, onay
iste. Begenilmeyen icin `/prototype` "Adim 6" kurali: **tum seti yeniden uretme**,
sadece o sahneleri tek duzeltme cumlesiyle (`too dark`, `wrong silhouette`) yeni
tura koy. En fazla 2 duzeltme turu; tavan dolduysa **kendi kendine devam etme** —
Perde 1'desin, sorabilirsin: "eldeki setle mi devam, yoksa su sahneler placeholder mi
kalsin?" Cevap `brief.md`'ye yazilir.

**Bu gorseller cope gitmez.** Onay araci olduklari kadar oyunun key art / arka plan /
menu gorselleridir — ingestion hattina girer, `ART.md`'de id alir.

## G3 — Soru turu ve kilit

Sahne onayi gelince kalan **tum** kararlari tek turda topla (`AskUserQuestion`, gerekirse
ust uste iki cagri ama tek tur — sonra bir daha yok):

- **Kapsam zarfi.** Varsayilan kural: **GDD'nin acikca istedigi her sey kapsamdadir.**
  GDD'nin hic anmadigi save / tutorial / ayarlar / coklu dil ise kendiliginden
  EKLENMEZ (istenmeyen ozellik yasagi). Zarf ancak GDD sessiz ve belirsizlik gercekse
  sorulur: "bitmis oyun" tabani = cekirdek dongu + baslangic ekrani + kazanma/kaybetme
  + yeniden baslama + ilerleme (skor/seviye) + tam sanat + ses kimligi + cila.
- Perde 1'de biriken belirsizlikler (GDD'de celisen/eksik noktalar)
- Platform ve girdi: masaustu mu mobil de mi (touch), oturum uzunlugu
- Icerik olcegi: kac seviye/dalga/kart/bolge — sayiyla
- Ses tonu: cozy/gergin/epik; muzik istenip istenmedigi
- three.js vendor mi CDN mi (tek dosya teslim icin **vendor varsayilan**, itiraz yoksa sorma)

Cevaplar `.showrun/brief.md`'ye islenir. Sonra kullaniciya kilit ozetini yaz — stil,
sahneler, kapsam zarfi, cevaplar, tahmini gorsel sayisi ve ChatGPT kota maliyeti
(kaynak: G2 sahne listesi + GDD'den kaba id sayimi — sahne + karakter + prop + UI,
+1 yedek tur; etiket `tahmin`) ve su notu ekle: hatlar (kod · sanat · ses)
ilk dakikadan paralel kosar, yalnizca cekirdek dongu paketi olcum geregi tek akistir
(19 paket = 1,04x hizlanma, 5 saat kayip). Sonra su cumleyle Perde 2'ye gec:

> **Basliyorum. Bundan sonra soru yok; bitmis oyunla donecegim.**

Bu, Perde 1'in son mesajidir. Onay bekleme — soru turu cevaplanmissa kilit tamamdir.

---

# PERDE 2 — Otonom uretim, sifir soru

## Faz A — Kriterler, envanter, plan

**Kod yazmadan once** `/goal` Faz 1: 3-8 calistirilabilir kabul kriteri (bu skill'in
standart cekirdegi 7 satir), `.goal/criteria.json`. Oyuna gore ozellestir, gevsetme:

| Kriter | Olcum |
|---|---|
| Acilis temiz | tek dosya `file://` ile acilir, konsolda 0 hata |
| Duman | 40 satirlik kontrol: canvas var, 1 kare render, 60 sn `advance()` ile ilerliyor |
| Sanat tam | `ART.md`'de durum=placeholder/eksik olan id sayisi 0 (insan-kilidi satirlari sayilmaz, raporda listelenir) |
| Ses | master bus tepe 0.7-0.98, kirpma yok (`/polish` §3 olcumu) |
| Performans | hedef sahnede medyan kare < 16 ms, draw call nesne sayisindan bagimsiz |
| His | funscore bot: >= 3 seed ortalamasi **85-90 bandinda**, YA DA >= 70 ve son iki olcum yukari yonlu (etiket: `tahmin`) |
| Teslim | `~/Downloads`'a kopyalanmis tek `.html`, boyut <= tavan (Faz F) |

Funscore metrikleri deckbuilder kokenli; oyunun turu farkliysa Faz A'da **tur-uyarlanmis
metrik eslemesi** yazilir (hangi metrik neye denk geliyor, her esik `tahmin` etiketli)
ve criteria.json'a girer. Kalibrasyonsuz mutlak okuma yapilmaz: bant hedeftir, tek
olcum gurultudur (>= 3 seed), 100 kovalanmaz.

Ayni fazda `ART.md` **tam envanteri** yazilir — `/prototype`'in "ilk set yeter"
istisnasi burada gecerli degil, hedef bitmis oyun: ekranda gorunecek her sey id alir,
G2'de inen sahne gorselleri de dahil. Goruntuleme sikligina gore siralanir, 10'arli
10'arli turlara bolunur; her id kendi promptunu ve kendi mesajini alir.

Sonra plan — `/plan-build` Faz 1-2 semasiyla. Faz 0 recon'un yerine **brief.md +
ART.md + criteria.json** gecer ve Fable prompt'una aynen girer; recon yine delege
edilmez. Plan tek modelin degil **iki modelin tartismasinin** urunudur:

1. **Fable taslagi yazar** (paketler, `owns` ayrik, calistirilabilir `gate`, dalgalar).
2. **Opus uygulayici gozuyle itiraz eder:** paket sisman mi, gate gercekten kosulabilir
   mi, `owns` gercek modul sinirlariyla ortusuyor mu, hangi paket stall riski tasiyor.
   Itiraz somut olmali ("P3'un gate'i sunucu acmadan kosulamaz" gibi), begeni degil.
3. **Fable itirazlari isler ve son karari verir.** En fazla iki tartisma turu; sonra
   Fable'in plani kesindir, tartisma uzatilmaz.
4. `/plan-build` Faz 2'nin bes veri kontrolu (kapi) yine kosulur — tartisma kapiyi
   ikame etmez.

Plana **dort kisit sabit** girer:

- **Cekirdek dongu paketi tek akistir** — `/prototype`'in olcumu burada da gecerli.
  Dalgalara yalnizca cekirdek KOSTUKTAN sonraki isler girer: ekran akislari, ilerleme
  sistemi, icerik uretimi, cila paketleri. Paralellik hat seviyesinde zaten surer.
- **Funscore harness'i plandadir, atlanamaz:** seed'li bot oyuncu, `game.advance()`
  uzerinden kosar, her secenegi zorla oynatir, JSON metrik cikarir. Cekirdek dongu
  kosar kosmaz Faz B'de ana ajan yazar — bu paket olmadan "His" kriteri kosulabilir
  degildir ve criteria.json kapida reddedilir.
- **Sanat hatti hicbir paketin bagimlisi degildir.** Kod placeholder'la yazilir
  (`/prototype` Adim 4 manifest sozlesmesi: `src/` dosya yolu bilmez, tek temas
  `data/art.js`), gorseller indikce manifest satiri eklenir.
- **Hat dosyalari hicbir paketin `owns`'una girmez:** `assets/**` ve `data/art.js`
  sanat hattinindir; ses kimligi dosyalari (`Audio.js` / `AudioManager`) ana ajanin
  ses hattinindir. Plan kapisi paket-paket cakismaya bakar, hatlari goremez — bu
  cit o kor noktayi kapatir.

## Faz B — Uc paralel hat

Ayni anda uc hat kosar; birbirini beklemez:

| Hat | Kim | Ne |
|---|---|---|
| **Kod** | sen (ana ajan) | `/prototype` Faz 2-4 disiplininde iskelet + cekirdek dongu + juice; `data/config.js`, `game.advance()`, `InputManager`, kamera kurali aynen. Cekirdek kosunca **funscore harness'i** yaz |
| **Sanat** | arka plan Agent (`agy (Gemini)`, `low`) | `ART.md` kuyrugunu `/image-run` ile **teker teker** uret-indir-esle; **yalnizca** `assets/` ve `data/art.js` manifestine yazar |
| **Ses** | sen, cekirdek kostuktan sonra | Web Audio kimligi: `/polish` §3 — kaynak/artikulasyon ayrimi, tek ezgi isaretcisi, gama kilidi |

`ART.md` durum kolonunu **ana ajan** gunceller — sanat ajaninin her tur raporundan
sonra ilgili satirlar `gercek` cevrilir, curuk cikan `eksik` isaretlenir. Sanat ajani
ART.md'ye dokunmaz; iki yazar ayni dosyada bulusmaz.

Sanat hatti kurallari: **tur basina tek mesaj, 10 konu** · stil blogu harfi harfine · damga EN SONDA · kolaj gelirse durdur-duzelt-yeniden gonder · indirmeden once seri sayisinin
arttigini dogrula · esleme icerige bakarak, kontak sayfasiyla · WebP her iki hatta
ayni ayarla: `cwebp -q 82` · Chrome MCP'yi ayni anda tek taraf kullanir.

**Eksik asset'te durma.** Batch curuk cikti, gorsel inmedi — placeholder kalir, id
`ART.md`'de `eksik` isaretlenir, is devam eder. **Iki yeniden uretim turundan sonra
hala curuk olan ya da kota bittiginde bekleyen id `insan-kilidi`ne tasinir** — "Sanat
tam" kriterine sayilmaz, teslim raporunda listelenir. Hicbir eksik donguyu bloklamaz.

**Commit noktalari:** cekirdek dongu ilk kostugunda bir commit + push; her sanat
turu entegre edildiginde bir commit + push. Saatlerce commitsiz calisma yasak —
`resume`'un kod tarafindaki tek dayanagi budur ve push'suz commit makine olunce kaybolur.

## Faz C — Genisleme dalgalari

Cekirdek dongu kosunca `/plan-build` Faz 3-4: plandaki dalgalar paralel **Opus**
ajanlariyla, paket basina kendi `effort`u, `owns` disina cikmak yasak, her paketin
kapisi calistirilir. Es zamanli paket 4-6'yi gecmez. Entegrasyon kapisi: tam derleme +
duman + plan disi dosya kontrolu; yesilse commit + push.

**Takilinca Fable'a danis.** Bir paket ayni kirmiziya **iki farkli teshisle** saldirip
cozemezse ucuncu denemeye girme: Fable'a dar bir danisma sorusu yaz — belirti, iki
denemenin ne oldugu ve neden tutmadigi, eldeki hipotez. Donen teshisi Opus uygular.
Bu, `/goal`'un "3 tur ilerleme yok = dur" kuralina varmadan yon degistiren erken
supaptir; ayni duvara ucuncu kez Opus'la kosmak devam etmek degildir.

## Faz D — Cila gecisi

`/polish`'in tamami, tek gecis: ingestion script'i (`tools/`, trim → WebP → data URI →
uretilmis modul) · shader katmani (tek `onBeforeCompile`, sifir notr) · ses olcumu
(tepe/RMS) · gorsel konfor butcesi (kamera nabzi varsayilan kapali) · performans
(once/sonra tablosu, InstancedMesh, havuz) · UI hizasi (9-slice, ic dikdortgen olcumu).
Gecis bitince commit.

### Derinlik ve kart efektleri

Iki cila kalemi bu skill'de standarttir; ikisi de `/polish` §2 shader kurallarina
(tek `onBeforeCompile`, uniform dallanma, sifir degeri notr) ve §4 konfor butcesine tabidir:

- **Alan/sahne derinligi — [/sprite-parallax](../sprite-parallax/SKILL.md).** G2'de
  uretilen alan gorselleri (odalar, bolgeler, kart sanati) duz resim olarak kalmaz:
  `gen_depth.py` ile yukseklik haritasi uret, parallax occlusion mapping ile imlece/
  kameraya tepki veren derinlik ver. UV kaydirma **yasak** — okluzyon yoksa derinlik
  yoktur, kural o skill'de. Sabit kamerali alan ekranlari ve kart hover'i dogal hedef.
- **Kart ustu parilti.** Kartli oyunlarda shine/glint sweep, kenar isiltisi, nadirlik
  parlamasi — shader katmaninda, ek doku ve ek draw call olmadan. Parilti **olay
  bazlidir** (hover, cekilis, nadir kart), surekli yanip sonmez; konfor butcesindeki
  acik/kapali ayari buna da uygulanir. Kart cercevesi/plaka isi buyurse
  [/deckcraft](../deckcraft/SKILL.md) hattina devret.

**Her cila iddiasi olcumle kanitlanir** — durum degistiren gorselde iki durum yakalanip
karsilastirilir (parallax icin: imlec iki uc konumda iki kare, fark yoksa efekt yok);
"yaptim" kanit degildir. Cila oynanisi degistirmez.

## Faz E — Kapi dongusu

`/goal` Faz 2-4: **tum** kriterleri kos → kirmizi varsa teshis yaz → tek duzeltme →
tekrar hepsini kos. Funscore bot skoru her turda >= 3 seed'le olculur ve **yon**
okunur: bant (85-90) hedeftir, 70 tabandir, 100 kovalanmaz. Dusen boyuta gore
duzeltme: gerilim/cesitlilik ayar isidir; karar yogunlugu yapisalsa cekirdege
donulebilir — **ama sinirla**: G0'da kilitlenen "cekirdek dongu" ve "oyuncunun ana
eylemi" cumleleri dogru kalmali. Ana eylemi degistirmek urun karardir: kriter kirmizi
kalir, `blocked_by_human`'a gecer, teshisle birlikte teslim edilir.

Yesil taklidi yasak: kriter gevsetme, skip, "manuel dogruladim" yok. Dur kosullari
`/goal` Faz 3'tekiler: hepsi yesil = bitti · 3 tur ilerleme yok = dur ve uc teshisi
yaz · insan kilidi = `blocked_by_human`, kalanla devam. Takilma supabi Faz C'dekiyle
aynidir: iki teshis tutmadiysa Fable'a danis, sonra devam.

## Faz F — Teslim

1. **Tek dosya build:** esbuild inline bundle; gorseller base64 gomulu, harici istek
   sifir. Iki bilinen tuzak: `String.replace` ikinci argumaninda `$&` genisler —
   replacement'i **fonksiyon** olarak ver; `public/` altindaki dosyalar singlefile'a
   gomulmez — asset'leri import zincirinde tut.
2. **Boyut tavani: 25 MB** (decisions.md'ye yazarak degistirilebilir). Asilirsa sirali
   kucultme, her adim decisions.md'ye: (a) WebP kalitesini dusur (82 → 70), (b) arka
   plan / key art cozunurlugunu ekran boyutuna kirp, (c) en az gorunen `ART.md`
   id'lerini placeholder'a dusur ve isaretle.
3. Build'i `file://` ile ac ve **teslim edilen dosyayi** test et (modul onbellegi
   tuzagina karsi cache-bust) — kaynak agaci degil.
4. `~/Downloads/<oyun-adi>.html`'e kopyala — teslim her zaman buraya.
5. Son commit + push — private repo ve GitHub Desktop baglantisi zaten Perde 2
   basinda kuruldu ("Calisma dizini ve repo"); kurulamadiysa (orn. `gh` girisi yok)
   burada tekrar dene, hala olmuyorsa rapora yaz.
6. Rapor: ne kuruldu (tek paragraf) · kriter tablosu (hepsi yesil/istisnalar) ·
   funscore bot skoru (seed sayisi + yon) · once/sonra performans · sanat durumu
   (kac id gercek, kac insan-kilidi) · `blocked_by_human` listesi (insan playtest'i
   dahil) · harcanan gorsel sayisi · `decisions.md`'den kayda deger varsayilanlar.

Insan funscore'u ve gercek playtest **teslimden sonra** kullanicinin isidir; rapor
bunu acikca soyler, beklemez.

## Model ve effort — kim ne yapar

**Rol ayrimi sabittir: Fable dusunur, Opus kodlar.** Plani Fable ile Opus tartisir,
son karar Fable'indir; kodu Opus yazar; Opus takilirsa Fable'a danisilir.

| Is | Model | Effort |
|---|---|---|
| Perde 1 promptlari (stil blogu, sahne cumleleri) | oturum modeli, **sen** | normal — asla low; ucuz prompt 10 gorseli cope atar |
| `/image-run` calistirma ajani | `agy (Gemini)` | `low` |
| Cekirdek dongu + harness + ses (Faz B) | oturum modeli, sen | dusuk tut — `/prototype` kurali, `high` yasak |
| Plan taslagi + son karar (Faz A) | Fable | **duruma gore kendi secer**: bolme kolaysa `medium`, cok modullu/girift ise `high` |
| Plan itirazi (Faz A) | Opus | `medium` |
| Dalga paketleri (Faz C) | Opus | paket bazinda; **tavan `high`, asilamaz** — `xhigh`/`max` bu skill'de Opus'a kapali |
| Takilma danismasi (Faz C/E) | Fable | duruma gore kendi secer: dar soru `low`/`medium`, girift teshis `high` |
| Debug mikro ajan | Opus | `low` |

## Yapma

| Yapma | Neden |
|---|---|
| Perde 2'de `AskUserQuestion` cagirmak | Sozlesmenin ihlali; varsayilan sec, `decisions.md`'ye yaz |
| Perde 2'de "ister misin / onaylar misin" yazmak | Ayni ihlalin cumle hali |
| Perde 1 kapisini kendi kendine onaylamak | Onay kullanicinindir; tikanirsa Perde 1'de sorulur |
| Damgayi uretim talimatinin onune koymak | Model tum istegi tek konu sanip kolaj uretir — olculmus |
| Tek mesaja 10'dan fazla konu koymak | Fazlasi tek contact sheet'e birlesir |
| Stil blogunu "iyilestirmek" | Set ikiye bolunur; kilit kilittir |
| G2 gorsellerini onay sonrasi cope atmak | Onlar oyunun key art'i; ingestion'a girer |
| Sanat insin diye kodu bekletmek | Placeholder sozlesmesi bunun icin var |
| Eksik asset'te durmak | Isaretle, devam et, sonda listele |
| Cekirdek dongoyu paketlere bolmek | Olculdu: 1,04x hizlanma, 5 saat kayip |
| Opus'u `high` ustunde kosturmak | Tavan serttir; maliyet katlanir, kazanc kucuk (`/plan-build` olcumu) |
| Ayni kirmiziya ucuncu kez Opus'la saldirmak | Iki teshis tutmadiysa sorun gorunmeyen yerde; Fable'a danis |
| Plan tartismasini ucuncu tura uzatmak | Karar Fable'indir; tartisma kapiyi ikame etmez |
| Funscore'u tek kosuyla/mutlak okumak | Tek olcum gurultu, kalibrasyonsuz mutlak yargi yasak (`/funscore`) |
| Funscore bot skorunu optimize etmek | Goodhart; proxy yesillenir, oyun iyilesmez |
| Kriteri sessizce gevsetmek | Hedef degisikligidir; gorunur yapilir ya da yapilmaz |
| Insan playtest'ini bekleyerek durmak | `blocked_by_human`'a yaz, teslim et |
| Uc hatti seri kosturmak | Sanat turu ~20-30 dk bekleme; o sure kod hattinindir |
| Saatlerce commitsiz calismak | Crash = is kaybi; `resume` kod tarafinda commit'e dayanir |

## Calistir

```bash
echo "Girdi: ${1:-<fikir/GDD belirtilmedi — kullanicidan iste>}"
echo ""
echo "PERDE 1 — sorular:"
echo "  G0  Konsept kilidi: tek sayfa GDD, ONAY (baska soru yok)"
echo "      Onay sonrasi repo: git init + gh repo create --private + GitHub Desktop'a ekle"
echo "  G1  Stil turu: ayni sahne x 10 stil (/image-prompt + /image-run), SECIM + tur sayisi (10/20)"
echo "  G2  Sahne turlari: 10 ya da 20 gorsel, kontak sayfasi, ONAY (hedefli redo, max 2)"
echo "  G3  Soru turu: kapsam zarfi + kalan kararlar tek turda -> kilit ozeti -> 'Basliyorum'"
echo ""
echo "PERDE 2 — sifir soru:"
echo "  A   /goal kriterleri + ART.md tam envanter + plan: Fable taslak, Opus itiraz, Fable karar"
echo "  B   Uc paralel hat: kod+harness (tek akis) | sanat (agy (Gemini) low) | ses — commit+push noktalari"
echo "  C   /plan-build dalgalari (Opus, tavan high) — takilinca Fable'a danis"
echo "  D   /polish tam gecis + /sprite-parallax derinlik + kart parilti — her iddia olcumlu"
echo "  E   /goal dongusu + /funscore bot (>=3 seed, bant 85-90, yon)"
echo "  F   esbuild tek dosya (<=25 MB) -> file:// testi -> ~/Downloads -> commit+push -> rapor"
```
