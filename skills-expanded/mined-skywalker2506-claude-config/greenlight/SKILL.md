---
name: greenlight
description: "Uretimden ONCE calisir: para kazanma potansiyeli olan, 2D sprite ile yapilabilir oyun fikri bulur ve 3-katmanli game design (core -> system -> content) ile tek sayfa GDD'ye cevirir. Canli pazar taramasi (kaynak URL'li) + 10 fikir + capali puanlama ve basari derecesi + gelistirme turu + TEK onerili pitch; cikti /prototype ve /showrunner'a hazir. Triggers: greenlight, fikir bul, oyun fikri, hangi oyunu yapayim, janr sec, game design, pitch, pazar taramasi, fikir uret, ne yapsam."
user-invocable: true
argument-hint: "[platform: steam|web|mobil|hepsi] [tema/kisit — ops.] veya [scan [platform]|pitch [dizin]]"
---

# /greenlight — neyi yapmaya deger?

`/showrunner` ve `/prototype` uretir; bu skill **neyi uretmeye deger** sorusunu cevaplar.
Janr secimi, kod yazilmadan verilen en buyuk pazarlama karardir: Zukowski'nin verisiyle
bir oyunun kaderinin ~%90'i "ne tur bir oyun oldugu ve nasil gorundugu"nde belirlenir
(https://howtomarketagame.com/2026/01/27/what-the-hell-happened-in-2025/). Iyi bir oyun,
yanlis janrda hic satmayabilir. Bu karar hafta 0'da, **yaziyla ve sayiyla** verilir.

> Janr = kitle secimi · Kanit = kaynak URL'li sayi · Cikti = TEK oneri + hazir GDD

Sabit kisitlar (sorulmaz, degistirilemez): 2D sprite + AI sanat hatti + tek kisi +
`/showrunner` uretim zarfi. 3D, agir el-emegi icerik (metroidvania odalari, NPC
takvimleri), sunuculu multiplayer **eleme kriteridir**, tercih degil.

## Cerceve: 3 katman — icten disa

Kaynak: Anton Slashcev & Mykola Veremiev, "3 Layers of Game Design"
(https://www.linkedin.com/posts/aslashcev_3-layers-of-game-design-together-with-mykola-share-7491394524183851008-8wwC/)

| Katman | Icerik | Bu skill'de |
|---|---|---|
| **1. Core Design** — BURADAN BASLA | fun mechanics, game feel, objectives, risk & reward, core loop | Tam yazilir — pitch'in govdesi |
| **2. System Design** | progression, difficulty curve, economy, resource mgmt, meta, skills, missions, events, social | Skec duzeyinde — showrunner/plan-build derinlestirir |
| **3. Content Design** | art style, animasyon, narrative, level design, VFX, UI/UX, ses | SADECE yon notu — art stili `/showrunner` G1'de kullanici secer |

Gonderinin ana tezi: cogu studyo 3. katmandan (art) baslar ve batar; calisan oyunlar
1. katmandan baslar, core loop **prototiple** kanitlanmadan sanata kaynak yatirilmaz.
Yorumlardaki hakli itiraz da kurala dahildir: katmanlar kati selale degil **vurgu
sirasidir** — iterasyon serbest, ama kaynak yatirimi iceriden disa akar.

## Argumanlar ve durum dosyalari

| Arg | Ne yapar |
|-----|----------|
| *(platform + kisitlar)* | Bastan sona: kisit kilidi → tarama → fikirler → puanlama/gelistirme → pitch + GDD |
| `scan [platform]` | Sadece Faz 0-1: kisitlari kilitle, taramayi kos, `scan.md` uret. Platform verilmezse `hepsi` |
| `pitch [dizin]` | Mevcut taramadan devam. Dizin verilmezse cwd'deki en yeni `greenlight/*/scan.md`. Scan 3 aydan eskiyse once yenile |

Cikti dizini: cagrildigi yerde `greenlight/<tarih>-<platform>[-<tema>]/`:

```
constraints.md   Faz 0 cevaplari: platform, gelir citasi, tema, sure + tarih
scan.md          tarama: her sayi URL + ornekleme tarihli; sonda GECTI/KALDI tablosu
ideas.md         10 fikir + skor kirilimlari + bant + gelistirme kaydi
pitch.md         TEK oneri + yedekler + kill kriterleri
gdd.md           secilen fikrin tek sayfa GDD'si (showrunner G0 formati)
```

`pitch` modu `constraints.md`'yi okur; dosya yoksa Faz 0 soru turunu kosar — bu, o
kosunun tek soru turu olarak sayilir. Tum dosyalari **ana ajan yazar**; tarama
ajanlari dosyaya dogrudan yazmaz (tek-yazar kurali, showrunner'in ART.md kuralinin esi).

---

## Faz 0 — Kisit kilidi (tek soru turu)

Argumandan cozulemeyeni tek turda sor, cevaplari `constraints.md`'ye yaz, bir daha sorma:

- **Platform hedefi:** Steam premium / web portal (Playgama-Poki-CrazyGames) / mobil /
  karisik. Uc hattin matematigi farklidir, secim taramayi sekillendirir.
- **Gelir citasi:** Steam'de "Real Steam" ~$150k brut (1.000+ inceleme esigi —
  https://howtomarketagame.com/2026/01/27/what-the-hell-happened-in-2025/) mi, yoksa
  portal portfoy geliri mi ($200-2.000/ay/oyun bandi)? Cita geri-hesabi belirler.
- **Tema/heves kisiti:** kullanicinin yapmak istedigi/istemedigi temalar. Ryan Clark'in
  uc kosulu birlikte gecmeli: yapmak ISTIYORSUN + yapABILIYORSUN + para kazanACAK
  (https://ryankubik.com/blog/consistently-profitable-indie-games).
- **Sure butcesi:** ay cinsinden. Janr yasam dongusu penceresi 6-12 ay; 2 yillik plan
  pencereyi kacirir.

**Tema oncelik kurali (soru acilmaz):** tema kisiti pazar verisiyle celisirse tema
pazara uyar — heves edilen tema, taramadan gecen bir janra reskin edilir. Reskin
mumkun degilse sifir-fikir yolu izlenir (Faz 3 sonu): soru degil, rapor.

## Faz 1 — Canli pazar taramasi

**Tarama her kosuda taze yapilir.** Asagidaki 2026-08 anlik goruntusu baslangic
sezgisidir, karar dayanagi degil — uc aydan eski her sayi supheli, 18 aylik tarama
olu (janr Phase 4'e gecmis olabilir). Tarama paralel ajanlarla kosulur (kapsamdaki
platform basina bir ajan, Opus `medium`); ajanlar bulgulari URL + ornekleme tarihiyle
dondurur, `scan.md`'yi **ana ajan derler** (tekillestirme + GECTI/KALDI tablosu).

### Olcum recetesi — sirayla, kapsamdaki platformlar icin

1. **Tag medyani** (isi haritasi): games-stats.com / GameDiscoverCo tag medyan **NET**
   geliri (Valve payi ve iade sonrasi). Referans: Colony Sim $44k, Roguelike
   Deckbuilder $38k, 4X $35k, City Builder $22k; genel medyan ~$2.6k, ilgi esigi $5k+
   (https://newsletter.gamediscover.co/p/which-genre-should-your-next-pc-game).
   Uyari: cok-tag bulasmasi, fiyat filtresi yok — tek basina okuma.
2. **Cita ustu yuzdesi** (boom/bust duzeltmesi): tag basina $200k+ brut orani.
   Referans: Crafting %32 > $500k; Platformer 1.166 oyunla %7 — en buyuk arz, en kotu
   oran (https://newsletter.gamediscover.co/p/analyzing-the-top-steam-tags).
3. **Kazanan sayimi**: yillik 1.000+ inceleme sayimi (Zukowski census). 2025: 20.282
   cikis, 608 kazanan (~%3). Janr basina kazanan sayisi = yol mu piyango mu.
4. **Yasam dongusu fazi**: proto (P1) → tanimlayici hit (P2) → ikinci dalga (P3, GIR)
   → oligopol (P4, GIRME). P3 sinyali: birden fazla yeni cikis %50+ pay aliyor. P4
   sinyali: ~3 oyun es-zamanli oyuncularin %75+'ini tutuyor
   (https://howtomarketagame.com/2025/11/12/the-cycle-of-a-hit-genre/).
5. **Web portal ayri test**: CrazyGames Basic Launch bari — ort. oturum 10+ dk, D1
   %10-15, 1-dk donusum %80+, yukleme <10 sn, build <20 MB; cikis kosulu 7 gun + 500
   oynanis (ya da otomatik 21 gun) — en gec 3 haftada sonuc
   (https://docs.crazygames.com/resources/basic-launch-metrics/). Poki siralamasi:
   toplam oynanis + etkilesim suresi + oynamaya donusum (https://sdk.poki.com/game-promotion).
   Playgama Bridge tek build'i cok portala basar, %80 pay — dogrulanmamis ikincil
   kaynak (https://app.cinevva.com/guides/web-game-monetization), Playgama
   dokumantasyonundan teyit et.
6. **Mobil ayri test**: gelir/indirme YoY oranlarini AYRI cek — gelir artarken
   indirme dusuyorsa yeni giris kilitli (pay-to-compete); indirme artiyorsa ads-first
   solo oynanabilir. CPI referansi: hybrid-casual $0.54→$0.95 (2024→25)
   (https://gamegrowthadvisor.com/blog/2026-03-17-user-acquisition-cpi-benchmarks-2026/).

### Kaynaklar ve erisilemezlik zinciri

Oncelik sirasiyla: howtomarketagame.com yillik/ceyreklik janr yazilari ·
newsletter.gamediscover.co tag analizleri · vginsights.com (ortalama gelir — medyanla
birlikte oku; deckbuilder tuzagina bak) · gamalytic.com / SteamDB · sdk.poki.com +
docs.crazygames.com + wiki.playgama.com (portal) · appmagic.rocks + sensortower.com
blog + gameanalytics.com benchmarks + naavik.co (mobil).
games-stats.com WebFetch'e 403 doner — tarayici araciyla ac.

Bir metrik erisilemezse (paywall, olu link) **zincir**: birincil kaynak →
Gamalytic/SteamDB'den tag'in son 12 ay cikislarindan medyani kendin hesapla →
son care 2026-08 anlik goruntusu, `bayat` etiketiyle. `bayat` etiketli metrik,
bagli oldugu rubrik boyutunu **en fazla yarim puanda** birakir ve pitch'in kill
kriterlerine "ilk taze veride yeniden puanla" satiri ekler.

### GECTI/KALDI kapisi — scan.md'nin son tablosu

Bir janr Faz 2'ye **gecer** ancak ucu birden saglaniyorsa: tag medyani >= $5k (ya da
platform karsiligi: portal KPI'lari ulasilabilir / mobil indirme YoY pozitif) **VE**
yasam dongusu != Phase 4 **VE** sabit kisitlara carpmiyor (3D, el-emegi icerik cukuru,
sunuculu MP). Faz 2 yalnizca GECTI janrlarda fikir uretir.

### 2026-08 anlik goruntusu (bayatlar — ornekleme: 2026-08-10)

| Janr | Durum | Kanit |
|---|---|---|
| **Idle/Incremental** | EN IYI arz/talep orani, uc platformda da calisir; kalite tabani yuksek (Zukowski) | Steam 2025: 27 kazanan; Q1 2026'nin 1 numarasi (https://howtomarketagame.com/2026/05/14/2026-q1-games/). Void Miner: solo, 7 ay, 12 gunde ~10k kopya (https://howtomarketagame.com/2026/04/28/void-miner/). Monkey Mart ~300M oynanis (https://poki.com/en/g/monkey-mart) |
| **Management/Tycoon "crafty-buildy"** | Talep arzla olcekleniyor; risk sanat degil sistem derinligi | Management %3.4, Simulation %4.1 hit (baseline %2.99) (https://howtomarketagame.com/2026/01/27/what-the-hell-happened-in-2025/); 2026 yilin-oyunlari en buyuk kovasi (https://howtomarketagame.com/2025/12/29/2026-games-of-the-year/) |
| **TD-roguelike** | Meta katmani sartiyla yukselen | Gnomes: 2 kisi, 10 ay, ~$700 butce, $367k brut (https://howtomarketagame.com/2025/08/13/gnomes-tower-defense-with-10-month-dev-time-hits-367484/) |
| **Kisa korku (2D/analog)** | Talep guclu, tepe soguyor; hibritle (korku+sim, korku+slot) | 2025: 39 kazanan #3 (https://howtomarketagame.com/2026/01/27/what-the-hell-happened-in-2025/); Q1 2026: 3'e dustu (https://howtomarketagame.com/2026/05/14/2026-q1-games/); Cloverpit 2 haftada 750k (https://howtomarketagame.com/2025/11/04/the-optimistic-case-that-indie-games-are-in-a-golden-age-right-now/) |
| **Roguelike deckbuilder** | Orta-boy janrlarin en yuksek hit orani (%5.1) AMA ortalama gelir diplerde — survivorship tuzagi; hook siradisi olmali | %5.1 = 11/212 (https://howtomarketagame.com/2026/01/27/what-the-hell-happened-in-2025/); ortalama gelirde dip (https://game-developers.org/steam-paradox-2025-revenue-volume); Balatro 5M/yil istisna (https://en.wikipedia.org/wiki/Balatro) |
| **Cozy/farming** | Arz dusuk (60/yil, %8.3 hit — ham oranda #2) ama beklenti Stardew: icerik cukuru. AI sanat hatti burada moat | https://howtomarketagame.com/2026/01/27/what-the-hell-happened-in-2025/ |
| **Survivors-like** | Phase 4 — oligopol. GIRME (pivotsuz) | "cok doymus, yuksek fidelity ya da pivot sart" (https://howtomarketagame.com/2026/05/19/2026-state-of-bullet-heavens-how-vital-shell-succeeded/) |
| **Merge (web/mobil)** | Web'de dusuk maliyetli test ama doygunluk orta-yuksek; tek oyun degil portfoy oyunu | Urun = sprite merdiveni; ~€1.20/1000 oynanis geliri (https://app.cinevva.com/guides/web-game-monetization); Playgama pazar haritasi (https://wiki.playgama.com/playgama/articles/introducing-the-web-games-industry-market-map-2026) |
| **2-player local (web)** | Portal basina en az rekabet — mobil studyolar yapamiyor; sunucu maliyeti sifir | Poki 130+ oyunluk ayri kategori (https://poki.com/en/two-player) |
| **Steam'de KACIN: metroidvania / salt puzzle / hassas platformer** | Metroidvania + salt puzzle 2025-26 hit listelerinde yok; platformer %7 hit (en buyuk arz, en kotu oran). Web'de troll/precision platformer talep kanitli (Level Devil 83M — https://poki.com/en/g/level-devil) ama moat el-emegi level zekasi: AI hattiyla uyumsuz, orada da dusuk puan | https://newsletter.gamediscover.co/p/analyzing-the-top-steam-tags; https://game-developers.org/steam-paradox-2025-revenue-volume; https://wnhub.io/news/stores-and-publishing/item-44107 |

**Sprite tuzagi:** "2D sprite ile yapilabilir" filtresinin en dogal adaylari (platformer,
side-scroller) verinin en kotu Steam janrlaridir. Sprite hattinin dogru harcanacagi yer
sistem-agirlikli, sanat-hafif janrlar: idle, tycoon, deckbuilder, TD, merge — grid,
kart, ikon, portre.

## Faz 2 — Fikir uretimi: 10 fikir

`scan.md`'nin GECTI janrlarinda **10 fikir** uret (`ideas.md`). Her fikir su formati
doldurur; dolduramayan fikir listeye giremez:

```
## <ad>  [janr] [platform]
HOOK: <tek cumle> + "hook'u tek ekran goruntusunde tasiyacak gorsel oge: <...>"
LOOP: oyuncu eylemi -> geri bildirim -> odul -> tekrar (bir satir)
HOOK-STACK: <hangi 2-3 hook ust uste biniyor — Clark yontemi>
KAZANAN COMP: <ayni janrda tutan oyun + neden tuttu + URL>
KAYBEDEN COMP: <ayni janrda batan oyun + neden batti — atlanamaz>
SPRITE-FIT: <sanat yuku: kac id, ne tur; AI hattina neden uygun>
PARA: <fiyat bandi / reklam yerlesimi — taramadaki gercek sayilarla>
SKOR: <boyut kirilimlariyla toplam>   BANT: <A/B/C/F + tek cumle>
GELISTIR: <uygulanan kaldiraclar ve puan degisimi, yoksa "—">
```

Kurallar:

- **Hook-stack, "X ama daha iyi" degil.** Clark'in uyarisi: basarili oyuna bakip
  "aynisi ama uzayda" uretmek iyi oyun cikarir, kayda deger oyun cikarmaz. NecroDancer
  = roguelike + ritim + muzik: uc hook ust uste
  (https://ryankubik.com/blog/consistently-profitable-indie-games).
- **Kaybeden comparable zorunlu.** Sadece kazananlara bakmak janrin calistigi
  yanilgisini verir; ayni tag'in kaybedenleri hangi hook'un yuk tasidigini gosterir.
- **Sessionability bastan** (https://newsletter.gamediscover.co/p/why-sessionability-radically-affects):
  ~15 dk'da tam bir kosu + meta ilerleme = demo calisir, tavsiye edilir, portala
  tasinir. Narrative-agir fikirler bu testte yapisal ceza yer.
- Tema, `constraints.md` kisitlarina uyar; icerik politikasi tetikleyicileri
  (`/image-prompt` Kural 6) tema seciminde de gecerli.

## Faz 3 — Puanlama, basari derecesi, gelistirme, eleme: 10 → 3

### Kistaslar — capali, tekrar uretilebilir

Her boyut alt kistaslara bolunur; her alt kistasin **0 / yarim / tam** capasi vardir.
Capasiz puan verilmez — iki farkli kosuda ayni fikir ayni puani almali. Olculemeyen
tek boyut Hook'tur: o **yargi puanidir** ve yaninda tek cumlelik gerekce zorunludur
(fikir formatindaki "gorsel oge" satiri) — ciplak sayi birakilmaz.

| Boyut | Alt kistas | Tam | Yarim | 0 |
|---|---|---|---|---|
| **Pazar talebi (30)** | Kazanan sayimi (10) | janr son yilda >= 10 kazanan | 3-9 | < 3 |
| | Tag medyani (10) | >= $20k | $5k-20k | < $5k |
| | Cita-ustu orani (10) | >= %15 | %8-15 | < %8 |
| **Yasam dongusu (15)** | Faz tespiti (15) | Phase 3 = 15 | Phase 2 = 10 · Phase 1 = 5 (talep kanitsiz — kill kriteri sart) | Phase 4 = 0 **ve eleme** |
| **Hook gucu (20)** | Ekran testi (10, yargi) | tek gorsel oge hook'u tasiyor | aciklama cumlesi gerekiyor | tasimiyor |
| | Hook-stack (10) | >= 2 bagimsiz hook | 1 hook | "X ama Y" |
| **Uretilebilirlik (20)** | Showrunner zarfi (10) | zarfa sigiyor | kucuk tasma, kirpilabilir | el-emegi icerik cukuru |
| | Sprite-fit (10) | ikon/kart/grid/portre agirlikli | karisik | animasyon/handcraft agirlikli |
| **Para uyumu (15)** | Geri-hesap (15) | sayilar rahat tutuyor | sinirda | tutmuyor |

**Sert eleme kurallari (puandan bagimsiz):** Phase 4 janr · Uretilebilirlik < 12/20 ·
geri-hesap kapisini gecememek. Para ve uretilebilirlik simetrik sekilde serttir;
pazar gucu dusuk uretilebilirligi satin alamaz.

### Basari derecesi — puan bir banda oturur, bant bir eylem soyler

| Bant | Puan | Derece | Eylem |
|---|---|---|---|
| **A** | 80-100 | Guclu aday | Dogrudan finalist havuzuna |
| **B** | 65-79 | Gelistirilebilir | **Gelistirme turune girer**, yeniden puanlanir |
| **C** | 50-64 | Zayif | Ancak her dusuk boyut icin somut kaldirac yazilabiliyorsa gelistirme turune; yoksa ele |
| **F** | < 50 ya da sert eleme kurali | Ele | Gerekce `ideas.md`'ye — sonraki kosuda yeniden tartisilmaz |

### Gelistirme turu — "nasil gelistirilir" tablosu

B ve kosullu C bandindaki fikirler elenmeden once **tam bir tur** gelistirilir.
Dusuk cikan her boyutun bilinen kaldiraclari:

| Dusuk boyut | Kaldiraclar |
|---|---|
| Pazar talebi | **Janr hibriti**: mekanigi koru, dusuk-talep janri yuksek-talep janrla melezle (korku+sim, TD+deckbuilder — 2025-26 cikislarinin cogu boyle) · temayi talep goren fanteziye tasi |
| Yasam dongusu | **Pivot**: ayni cekirdek hissi komsu, daha az doymus janra tasi · oligopolun bosladigi alt-kitleye daral (kaybeden comp'lar nereyi bos birakmis) |
| Hook gucu | Ikinci bagimsiz hook ekle (tema x mekanik x format capraz dene) · hook'u "ekran goruntusunde gorunur" olana kadar somutlastir — gorunmuyorsa hook degildir |
| Uretilebilirlik | El-emegi icerigi sistemle degistir (bespoke level → procedural/grid) · animasyon ihtiyacini shader/parallax'a devret (`/polish` ve `/sprite-parallax` zaten hatta) |
| Para uyumu | Platform degistir (ayni fikir uc matematikte farkli sonuc verir) · kapsami kucult (4 aylik build Silver'da kar eder) · oturum yapisini reklam yerlesimine uydur |

Kurallar:

- **Tek tur.** Gelistirilen fikir yeniden puanlanir, iki puan yan yana yazilir (yon
  gorunur). Ikinci gelistirme turu yok — sonsuz cilalama, kill-kriteri panzehirinin
  tam tersidir. Ikinci turda hala B/C ise fikir yedek listesine iner ya da elenir.
- **Kaldirac somut olmali.** Tek cumleyle yazilamiyorsa ("daha eglenceli yap" kaldirac
  degildir) uygulanmaz, boyut puani oldugu gibi kalir.
- Gelistirme hook'u veya janri degistirdiyse kazanan/kaybeden comparable'lar **yeniden
  bulunur** — eski comp yeni fikri dogrulamaz.

### Geri-hesap kapisi — sayi tutmuyorsa fikir eleniyor

- **Steam:** hedef $150k @ $15 ve ~0.15x ilk-hafta donusumuyle ≈ 60-70k wishlist
  gerekir; Silver bandi 8k-60k wishlist (Zukowski launch-visibility bantlari, Haziran
  2026 guncellemesi — tarama sirasinda howtomarketagame.com'dan guncel yaziyi bul).
  Comparable wishlist'i dogrudan olculemez — **proxy**: inceleme sayisi x ~30 ≈ satis
  (Boxleiter; SteamDB/Gamalytic'ten inceleme sayisi, URL'siyle), satistan 0.15x ile
  wishlist'e geri don; etiket `tahmin`. Comparable'lar banda ulasamiyorsa janr degil
  **kapsam** kucultulur — 4 aylik build Silver'da kar eder, 24 aylik etmez.
- **Web portal:** CrazyGames bari objektif ve ~3 haftada olculebilir — en hizli talep
  testi. <20 MB + <10 sn kisiti fikir seviyesinde kontrol edilir.
- **Mobil:** once oynanabilir reklam kreatifi, sonra oyun (2026 pratigi). Janrin D30
  LTV bandini benchmark'tan cek (gameanalytics.com benchmarks / naavik.co — etiket
  `tahmin`), kaynakli CPI ile karsilastir; CPI > LTV bandi ve organik kanal yoksa
  (idle/word disi) mobil hedefi dusur.

### Akis ve az-fikir yolu

Akis: 10 fikri puanla → banda otur → B/C'leri gelistir (tek tur) → yeniden puanla →
sert eleme + geri-hesap → kalanlarin **en iyi 3'u** Faz 4'e. Uc A-bandi cikmazsa en
iyi 3'le devam et ama pitch'te acikca soyle: "bu kosunun tavani B bandi".

**3'ten az fikir kaldiysa:** en cok fikir oldüren kisita hedeflenmis **tek** ek uretim
turu kos (orn. kapsam kucultulmus varyantlar) — soru acmadan. Hala sifirsa cikti bir
**basarisizlik raporudur**: `pitch.md` tarama kanitini ve hangi kisitin (cita, tema,
sure) yolu kapattigini yazar. Bu mesru bir sonuctur; zayif fikri parlatmaktan iyidir.

## Faz 4 — 3 finalist icin 3-katman tasarim

Her finalist icin, katman sirasiyla:

1. **Core Design — tam.** Fun mechanics (oyuncu neyi yapmaktan zevk aliyor, mekanik
   olarak) · game feel (ekranda/kulakta ne hissettiriyor) · objectives (kisa/orta/uzun
   vadeli hedef merdiveni) · risk & reward (anlamli secim: sonuclarin cogu gorunur,
   hepsi degil — Costikyan, bkz `/funscore`) · core loop (eylem → geri bildirim →
   odul → ilerleme → tekrar, sayilarla).
2. **System Design — skec.** Progression + economy + difficulty egrisinin birer
   paragraflik iskeleti; meta sistemler ad olarak. Derinlestirme `/showrunner`
   Faz A'nin (Fable plani) isidir, buranin degil.
3. **Content Design — SADECE yon.** Ton (cozy/gergin/komik/agir), kamera/bakis acisi,
   referans gorsel dili UC kelime. Art stili secimi burada YAPILMAZ — o karar
   `/showrunner` G1'de 10 stil denemesiyle kullanicinindir. Icerikten baslamak, bu
   skill'in varlik sebebini iptal eder.

## Faz 5 — Pitch: TEK oneri

`pitch.md`:

1. **Onerilen fikir + neden** — skor kirilimlari, bant, geri-hesap sayilari, yasam
   dongusu fazi, kaynak URL'leri. Oneri TEKtir; secenek listesi sunup karari
   kullaniciya birakmak bu skill'de basarisizliktir. Iki yedek birer paragraf,
   "neden birinci degil" cumlesi + kendi skor/bantlariyla.
2. **Kill kriterleri — pesinen, sayiyla:** orn. tag medyani $5k altina duserse ·
   cita-ustu orani %15 altiysa · Next Fest wishlist hedef bandin altinda kalirsa ·
   portal Basic Launch KPI'lari tutmazsa · `bayat` etiketli metrik taze veriyle
   celisirse → fikir olur, tarama yenilenir. Ucuz sanat, olu konsepti cilalama
   tuzagini buyutur — kill kriteri panzehirdir.
3. **Tek sayfa GDD** (`gdd.md`) — `/showrunner` G0'in bekledigi formatta: tur ve
   referans oyun · cekirdek dongu · oyuncunun ana eylemi · kazanma/kaybetme · ton ·
   kamera. Arti: para modeli (fiyat/reklam yerlesimi) · comparable listesi ·
   Faz 4 core design'i ek olarak.

Kullanici **yedek fikri** secerse: o finalistin Faz 4 tasarimi zaten mevcut — `gdd.md`
ayni formatta yedek icin yeniden yazilir (yeni tarama gerekmez).

Sonraki adim — sira onemli, cerceveyi uygula:

> Once **`/prototype greenlight/<dizin>/gdd.md`** — core loop his kanitini alir
> (3-katman tezi: prototipsiz sanata yatirim yok). Eglence kaniti gelince
> **`/showrunner`** ayni GDD'yle bastan sona goturur. Kullanici riski acikca kabul
> edip "dogrudan showrunner" derse o zaman atlanir — varsayilan atlamaz.

## Model ve effort

| Is | Model | Effort |
|---|---|---|
| Tarama ajanlari (Faz 1, platform basina) | Opus | `medium` |
| Fikir uretimi + puanlama + gelistirme + pitch | sen (oturum modeli) | normal |
| Ikinci gorus (istege bagli, buyuk supheler) | `/second-opinion` | — |

## Yapma

| Yapma | Neden |
|---|---|
| Content/art'tan baslamak | Infografigin ana tezi: cogu studyonun batma sebebi |
| Prototipsiz `/showrunner`'a gecmek (kullanici acikca istemedikce) | Ayni tezin devir hali: G1 stil turu, kanitsiz core'a sanat butcesi harcar |
| Anlik goruntuyu taze veri sanmak | 18 aylik tarama olu; janr Phase 4'e gecmis olabilir |
| Sadece kazananlara bakmak | Survivorship: deckbuilder orta-boy janrlarin en yuksek hit oranina sahip VE ortalama geliri diplerde |
| "X ama daha iyi / uzayda" fikri | Iyi oyun cikar, kayda deger oyun cikmaz (Clark) |
| Phase 4 janra pivotsuz girmek | Oligopolle uretim degeri yarisi; solo kaybeder |
| Platformer/side-scroller'i "2D'ye dogal" diye secmek | Steam: 1.166 oyun, %7 hit; web'de bile moat el-emegi level zekasi |
| Kaynaksiz sayi yazmak | Her iddia URL + ornekleme tarihi tasir; tasimayan silinir |
| Capasiz puan vermek | Iki kosuda ayni fikir ayni puani almali; yargi boyutu gerekce tasir |
| Sinirda fikri ikinci kez gelistirme turuna sokmak | Tek tur; sonsuz cilalama kill-kriterinin tersi |
| 10 fikri de derin tasarlamak | Eleme once; 3-katman sadece 3 finaliste |
| Secenek listesi sunup karari birakmak | Oneri TEK; yedekler "neden degil" cumlesiyle |
| Geri-hesapsiz pitch | Wishlist/KPI/CPI matematigi tutmuyorsa fikir puan alamaz |
| Kill kriterini sonraya birakmak | Pesinen yazilmayan kriter, batan fikri cilalatir |

## Calistir

```bash
echo "Girdi: ${1:-<platform + kisitlar belirtilmedi — Faz 0'da sor>}"
echo ""
echo "0  Kisit kilidi -> constraints.md: platform, gelir citasi, tema, sure — TEK soru turu"
echo "1  Canli tarama -> scan.md: tag medyani (NET) -> cita-ustu %% -> kazanan sayimi"
echo "   -> yasam dongusu -> portal KPI -> mobil YoY. Her sayi URL+tarih. Sonda GECTI/KALDI"
echo "2  10 fikir -> ideas.md: hook-stack + kazanan/kaybeden comp + sprite-fit + para"
echo "3  Puanla (capali kistas) -> bant (A/B/C/F) -> B/C'yi gelistir (tek tur) -> yeniden"
echo "   puanla -> sert eleme + geri-hesap -> en iyi 3. Az kaldiysa tek ek uretim turu"
echo "4  3 finalist x 3 katman: core TAM, system skec, content SADECE yon"
echo "5  pitch.md: TEK oneri + kill kriterleri + gdd.md (showrunner G0 formati)"
echo ""
echo "Sonraki adim: /prototype greenlight/<dizin>/gdd.md -> kanit gelince /showrunner"
```
