---
name: prototype
description: "Bir GDD'yi Three.js + Web Audio ile oynanabilir, juicy bir prototipe cevirir. Tasarim bastan kilitlenir, kodu tek ajan yazar, sanat arka planda paralel uretilir: 10 stil denemesi -> kullanici secer -> asset'ler indikce oyuna girer. Oyunun eglenceli olup olmadigini kanitlar, oyunu bitirmez. Triggers: prototype, prototip uret, gdd den prototip, hizli prototip, playable prototype, three.js prototip, oyun prototipi."
user-invocable: true
argument-hint: "[GDD dosya yolu veya oyun fikri]"
---

# /prototype — fikrin ise yaradiginin kaniti

> Model yonlendirmesi: global/model-routing.md

Oyun yapmiyorsun. **Oyun fikrinin ise yaradiginin kanitini** yapiyorsun.

> Hiz > Mimari · His > Icerik · Oynanir > Mukemmel

**Hedef:** tarayiciyi ac -> tikla -> **saniyeler icinde oyna.** Yukleme ekrani, giris akisi,
menu labirenti yok.

## Tek ajan kurali — olculmus, tercih degil

**Isi bolme. Sen yaz.** Ayni GDD, iki kosu:

| | tek akis | 19 pakete bolunmus, 14 ajan |
|---|---:|---:|
| Sure | **18 dk** | 5 sa 6 dk |
| `src/` satir | 2.588 | 19.801 (7,7x) |
| Icerik | 7 gun · 10 kart · 5 kaynak · 3 tren | **birebir ayni** |
| Paralellik kazanci | — | **1,04x** |

Paralellik zinciri kisaltmaz. Her paket bir oncekinin arayuzunu **kesfetmeyi** bekledi; iki paket
ayni nesne icin iki sema uydurdu ve ~50 dakika gitti. Prototipte koordinasyon maliyeti,
paralellik kazancindan buyuktur.

**Mikro ajan yalnizca su ucu icin, ve yalnizca prototip KOSTUKTAN sonra:**
hata ayiklama · optimizasyon · tek seferlik arastirma. Temel kodlama, ses, UI icin
**asla ajan bekleme**.

**Tek gercek paralel hat: sanat uretimi.** Yukaridaki olcum kodun paralelligini
olcuyor — paketler birbirinin *arayuzunu* bekledigi icin kaybettik. Sanat hattinda
boyle bir bagimlilik yok: ChatGPT'de gorsel uretmek 3-5 dakika **bekleme**, kod
degil. O hat `assets/` ve manifest disinda hicbir dosyaya dokunmaz, senin yazdigin
kodla arayuz paylasmaz. Bu yuzden arka planda kosar ve saati durdurmaz —
detay: "Paralel sanat hatti".

## Bu skill NEREDE biter

Prototip, "bu fikir eglenceli mi" sorusunu cevapladiginda isini bitirmistir. Su uc kosul
birden saglaninca **dur ve `/polish`'e devret**:

1. Cekirdek dongu oynaniyor,
2. Kullanici oynadi ve cevap verdi,
3. Gelen istekler yeni mekanik degil **var olani derinlestirme** (gercek sanat, shader,
   ses kimligi, performans, UI hizasi).

Shader efektleri, ses kimligi ve aranjman, konfor ayarlari, instancing ve sprite
animasyon hatti **bu skill'in isi degildir** — `/polish`. Yeni sistem/mekanik ise
`plan-build`. Bu siniri asmak prototipi sessizce testsiz bir urune cevirir.

**Sanat hatti bir istisnadir, ama dar bir istisna.** Prototip bir stil secer ve o
stilde **ilk asset setini** uretip oyuna takar — cunku "eglenceli mi" sorusunun
cevabi ekranda ne gorundugune bagli ve placeholder kutularla verilen cevap yaniltir.
Prototipin isi **stili kilitlemek ve ilk seti gecirmektir**; asset envanterini
tamamlamak, varyant uretmek, animasyon ve atlas cikarmak `/polish`'in isi.

## Basari olcutu: DOGRULUK degil HIS

Bu bir MVP. Sorulan soru **"dogru mu"** degil, **"guzel mi, oynanir mi, tekrar etmek istiyor
muyum"**. Cevabi **bakarak** verilir, test kosturarak degil.

Bu yuzden: kabul kriteri yok, kapi suiti yok, mutasyon yok, determinizm kaniti yok. Tek
dogrulama **ekran goruntusu + 60 saniye oynamak**. Bir sey calismiyorsa zaten goreceksin;
calisiyor ama sikici ise hicbir test bunu soylemez.

> Olculmus: bir kosuda dogrulugu kovalamak ~5.000 satir kapi uretti ve kirmizilarin yarisi
> kapinin kendi hatasiydi. O sure hissi iyilestirmeye harcansa prototip daha iyi olurdu.

## Model ve effort politikasi — hiz icin ayarlanir

| Is | Model | Effort |
|---|---|---|
| Sen (ana ajan): analiz, iskelet, cekirdek dongu, juice, entegrasyon | oturumun modeli | **dusuk tut** — uzun muhakeme etme, ilk makul cozumu yaz |
| Sanat prompt'u yazmak (stil blogu, sahne cumleleri) | oturumun modeli, **sen** | normal — `/image-prompt` Kural 2, ucuzlatilan prompt tum turu cope atar |
| Sanat hatti ajani (gonder / bekle / indir / tasi) | `agy (Gemini)` | **`low`** — mekanik, `/image-run` "Model ve efor" |
| Mikro ajan (debug / optimizasyon, prototip kostuktan SONRA) | `opus` | **`low`** |
| Plan/analiz delegasyonu | — | **yok**. 3 dakikalik analizi delege etmek, yapmaktan uzun surer |

**`effort: high` bu skill'de yasak.** Olculmus: `high` paketler 24-38 dakika, `medium` olanlar
7-19 dakika surdu. Prototipte fark kaliteye degil sureye gidiyor.

**Kendi muhakemeni de kis.** Her karari olcme, her alternatifi tartma. Bir sayi makul
gorunuyorsa yaz, sonra ekranda bak. "Hangi yaklasim daha dogru" sorusu bu skill'in sorusu
degil; **"su an ekranda ne var"** sorusu.

## Butce ve saat

**30 dakika bir PLANLAMA kisitidir, bir kesme sayaci degil.**

Faz 1'de kapsami **30 dakikada bitecek sekilde** sec — bu skill'in asil isi budur. Ama is
uzarsa **saat doldu diye birakma**: calismayan bir sey teslim etmek, gec teslim etmekten
kotudur. Kural tek cumle:

> Kapsami 30 dakikaya gore planla. Tasarsa **calisir hale gelene kadar devam et**, sonra dur.

Yani tavan **kapsamin** tavanidir, **calismanin** degil. 30. dakikada elinde yarim bir dongu
varsa dogru hamle durmak degil, o donguyu kapatmak.

**Sanat hatti saatin disindadir.** Tablodaki dakikalar senin klavyende gecen suredir;
arka planda donen gorsel uretimi bu butceyi harcamaz. 30. dakikada elinde calisan bir
dongu ve yarim inmis bir asset seti varsa **prototip hazirdir** — inmeyenler
placeholder kalir, hat arkada donmeye devam eder.

| Faz | Sure | Cikti |
|---|---:|---|
| 0 · Tasarim kilidi | 2 dk | tek sayfa GDD **onaylanmis** |
| 1 · GDD analizi | 3 dk | cekirdek dongu + kesikler + asset listesi |
| 2 · Iskelet | 5 dk | `index.html`, `data/config.js`, bos sahne, kamera |
| 3 · Cekirdek dongu | 12 dk | oyuncu eylemi -> geri bildirim -> odul |
| 4 · Juice + ses | 6 dk | partikul, shake, punch, procedural ses |
| 5 · Bak ve tek gecis | 4 dk | ekran goruntusu, **en yuksek etkili tek** duzeltme |

### Saat kayarsa — ne KESILIR, ne kesilmez

Kontrol noktalari **kapsami** daraltmak icindir, isi yarida birakmak icin degil:

| Dakika | Elinde yoksa | Kes |
|---:|---|---|
| 15 | cekirdek dongu calismiyor | icerigi yariya indir (2 gun -> 1, 4 kart -> 2), donguyu bitir |
| 22 | juice yok | ikincil sistemleri at ve juice'a gec — **juice'suz prototip sorusunu cevaplamaz** |
| 26 | hala eksik var | kalan "olsa iyi" maddelerinin hepsini at |

**Asla kesilmeyen uc sey:** cekirdek dongunun calisir olmasi, juice katmani, ve teslim
edilenin **hatasiz acilmasi**. Bunlar bitmeden saat bahane degildir.

Yarim biten bir sistem, hic baslamamis sistemden pahalidir: entegrasyonu bozar ve neyin
calistigi belirsizlesir. O yuzden **kesmek erteleme degil karardir**, ve `README.md`'nin
"yapilmayanlar" bolumunde gorunur olur.

Sure tasarsa **kullaniciya soyle** — tahmin degil olcum: kac dakika oldu, ne kaldi, neden.
Sessizce uzatma.

---

## Faz 0 — Tasarim kilidi (2 dk)

**Oyun tasarimi bastan belli olmali.** Sanat hatti Faz 1'de tetikleniyor ve stil
sorusuna cevap verebilmek icin oyunun ne oldugunu bilmesi gerekiyor: tur, ton,
kamera, oyuncunun ekranda ne gordugu. Tasarim yolda sekillenirse uretilen 10 stil
denemesi bos yere uretilmis olur ve kota gider.

| Girdi | Ne yap |
|---|---|
| GDD dosyasi verildi | Oku, bir paragrafla ozetle, **onay al**, devam et. Dokuman supheliyse (kapsam sisik, mekanikler sayisiz) once **`/gdd-review`** — puanla ve v2'yi onaylat |
| Sadece fikir verildi | **Tek sayfa GDD'yi sen yaz** (asagidaki 6 baslik), goster, onay al |
| Fikir de belirsiz | Tek turda sor — tur, ton, kamera, oyuncunun ana eylemi. Cevabi bekle |

Tek sayfa GDD'nin alti basligi: **tur ve referans oyun · cekirdek dongu · oyuncunun
ana eylemi · kazanma/kaybetme · ton (cozy / gergin / komik / agir) · kamera ve bakis
acisi.**

Bu tek bloklayan adimdir; onaysiz Faz 1'e gecme. Onaydan sonra **hicbir sey icin
durma** — sanat stili onayi dahil, o hat arkada doner.

## Faz 1 — GDD analizi (3 dk)

> Bu fazin tam tarifi **`/gdd-review extract`**'tedir. Buradaki ozet kendi basina
> yeterlidir; GDD buyukse ya da kapsam belirsizse o skill'i cagir, `SCOPE.md` +
> `ART.md` hazir gelsin — ama **bekleme, ayni oturumda kendin de yapabilirsin.**

Kod yazmadan once **cekirdek donguyu** cikar:

```
oyuncu eylemi -> geri bildirim -> odul -> ilerleme -> tekrar
```

Ve dort soruyu cevapla: ana oyuncu eylemi ne · kazanma sarti ne · kaybetme sarti ne ·
**hangi anlar gorsel geri bildirim istiyor**.

Sonra `SCOPE.md` — 10 satir:

- **Olmali:** cekirdek mekanik, oyuncu etkilesimi, minimum UI, kazan/kaybet, geri bildirim efektleri
- **Olsa iyi:** ikincil sistemler, ekstra icerik
- **Yok:** save, tutorial, ayarlar, erisilebilirlik, coklu oyuncu, ECS, backend

**Ilk prototip 1-3 dakikalik oynanis.** GDD 7 gun istiyorsa 2 gun yap; 10 kart istiyorsa 4 kart.
GDD'nin "kabul kriterleri" bolumu varsa o **urun hattinindir**, seni baglamaz.

**Bu fazin ikinci ciktisi: asset listesi.** `SCOPE.md`'nin yanina `ART.md` yaz —
kesilmis kapsamda ekranda gorunen her sey, id'siyle:

```
hero          oyuncu karakteri, 3/4 acidan, tek poz
enemy_wolf    dusman, yandan
card_frame    kart plakasi, bos
tile_grass    zemin karosu, tileable
ui_panel      HUD paneli, 9-slice
bg_forest     arka plan katmani, parallax
```

Liste 10'un altindaysa tek tur, ustundeyse **goruntuleme sikligina gore sirala** —
oyuncunun en cok baktigi sey ilk tura girer. Bu liste bittigi anda sanat hattini
tetikle ve **beklemeden** Faz 2'ye gec.

---

## Paralel sanat hatti — arka planda doner, seni bekletmez

Faz 1 biter bitmez baslar, Faz 2-5 boyunca arkada calisir. **Ana isi asla bloklamaz:**
sen kodu placeholder'la yazarsin, gorseller indikce yerlerine oturur.

```
ART.md hazir
   ↓
stil arama turu (10 stil, TEK sahne, 10 mesaj) ─┐
   ↓                                        │ sen bu sirada Faz 2-3 yaziyorsun
kullanici bir stil secer                    │
   ↓                                        │
stil blogu KILITLENIR                       │
   ↓                                        │
asset turlari (10'arli, sikliga gore) ────┘
   ↓ her gorsel indikce
post-process → assets/ → manifest satiri → oyunda gorunur
```

### Adim 1 — Stil arama: 10 stil, tek sahne

Stil aramasinda **konu sabit, stil degisir**: ayni sahne, 10 farkli stil.

**Sahne, oyunun ONEMLI bir ic sahnesi olmali ve oyun ici goruntu gibi kadrajlanmali** —
oyunun kamerasi, oyunun kompozisyonu, arayuzun oturacagi kenar bosluklari dahil. Bagimsiz
bir illustrasyon ya da "karakter portresi" **degil**. Iki sebep:

1. Secilen sey bir resim degil, **oyunun nasil gorunecegi**. Guzel duran bir portre,
   oyun ekraninda kotu durabilir; ancak ekranin kendisine bakarak karar verilebilir.
2. O kare cope gitmez — secilen stilin karesi **oyunun ilk gercek ekran gorseli** olur ve
   dogrudan `ART.md`'ye girer.

**Sahne, oyunun en yogun ANI olmali** — oyuncunun ekranda en cok zaman gecirdigi ve oyunun
ne oldugunu anlatan durum:

| Oyun | Dogru sahne | Yanlis sahne |
|---|---|---|
| Dovus/aksiyon | savasin tam ortasi, iki taraf da is basinda | menu, karakter secimi |
| Kafe/dukkan simulatoru | musteriler siparis veriyor, tezgah dolu, kafe islerken | bos kafe, gun sonu ekrani |
| Deckbuilder | kartlar elde, masa kurulu, hamle aninda | kart destesi kapak gorseli |
| Kesif/expedition | yolculugun icinde, tehlike gorunurken | harita ekrani |

**Oyun sonu / kazandin / kaybettin / yukleme ekranlari yanlis secimdir** — onemsiz anlardir
ve stil hakkinda bilgi tasimazlar. Sahneyi secerken "bu kareyi oyunun magaza sayfasina
koyar miydim" diye sor; cevap hayirsa yanlis sahnedir.

**Stil secildikten sonra:** ayni disiplinle, secilen stilde **birkac ayri onemli ekran**
uret (en cok bakilan iki ekrani sabit tut, kalanlari cesitlendir). Amac artik stil secmek
degil, **stilin butun ekranlarda tutup tutmadigini** gormek — bir stil dovus sahnesinde
harika, ust-bakis kesif ekraninda cokebilir ve bu ancak bakinca anlasilir.

**On stil = TEK mesaj.** `/image-prompt` Kural 1: on konu tek mesajda gider, damga en
sonda durur; uretim yine sirayla olur ama 10 yerine 1 istek gonderilir. Stil aramasinda
sabit olan **sahne**, degisen **stil** — yani numarali liste stilleri sayar:

```
Generate 10 separate images, one for each numbered style below.
IMPORTANT: output each as its OWN separate image file. Do not combine them into a grid,
contact sheet, collage or single canvas.

SUBJECT (identical in all 10): <oyun ici sahne, bir-iki cumle>
FRAMING (identical in all 10): <oyun ici kadraj notu>
NEGATIVE (identical in all 10): no text, letters, numbers, logos, watermarks, no UI.

Render the SAME subject ten times, once in each style below.
1. <teknik + palet + isik, ~25 kelime>
...
10. ...

[CLAUDE — <tarih saat> — <proje>, stil arama]
```

**On stil gercekten farkli eksenlerde olmali**, ayni seyin on tonu degil. Ornek
havuz: gouache masal kitabi · duz vektor · pixel art · kil/clay · cel-shaded · mürekkep
yikama · kagit kesme (cutout) · yari-gercekci painterly · low-poly · risograph ·
sulu boya + ince kontur · art nouveau/vitray · chiaroscuro.

**Havuzu projenin kalite barina gore ayikla.** On stilin hepsi ayni uretim degerinde
gorunmek zorunda: proje "guzel, yuksek uretim degeri" hedefliyorsa retro/ucuz okunan
stiller (pixel art, kaba vektor) listeye alinmaz — yoksa secim on secenek arasindan
degil, uc ciddi secenek arasindan yapilir.

Her stil **kendi paletini** tasisin — `/image-prompt` Kural 2: palet projeye aittir,
"vivid saturated" sablonu degil. Oyunun tonu cozy ise solgun ve sicak paletler de
listede olsun; hepsi canli olmak zorunda degil.

### Adim 2 — Onay: sor, ama durma

Inen 10 kareyi kullaniciya **numaralayarak** goster ve secmesini iste. Bu **tek
bloklayan sanat adimidir**, ama seni bloklamaz — sen bu sirada cekirdek donguyu
yaziyorsun. Kullanici "3 ve 7 karisimi" derse iki stil blogunu birlestir ve
**tek cumlelik onay** al; ucuncu tura cikma.

Secilen stil blogu **kilitlenir**: bundan sonraki her prompt onu **harfi harfine ayni**
kopyalar. Tek kelime degistirirsen set ikiye bolunur.

### Adim 3 — Asset turlari, arka plan ajaniyla

`ART.md` listesini 10'arli turlara bol; **her tur tek mesajdir** (10 numarali konu, ortak
stil blogu, damga en sonda). Promptlari `/image-prompt` kurallariyla **sen yaz** (prompt
yazimi low'a verilmez), calistirmayi `/image-run`'a devret:

```bash
~/Projects/ClaudeHQ/scripts/hq agy "<ajan gorevi>" --dir <proje> --slug art-run &
```

Claude'un `Agent` tool'u Gemini kabul etmez — mekanik serit **Bash'ten `hq agy`**
ile acilir, arka planda. Model/efor wrapper'da: `gemini-3.8-flash-medium`, `medium` (is tipine gore global/model-routing.md). Argon kullanilmaz. Sorun cikan seridi `AGY_MODEL=gemini-3.8-flash-high AGY_EFFORT=high` (gerekirse `-high`/`high`) ile yeniden kos.

Ajanin gorevi dar ve yazili: sohbeti ac → promptu gonder → 1 dk'da bir kontrol →
seriyi indir → icerige bakarak esle → `assets/`'a tasi → manifest satirini ekle →
rapor et. **Ajan `src/` altina dokunmaz.** Kod ile tek temas noktasi manifest
dosyasidir; olcumdeki "iki paket ayni nesne icin iki sema uydurdu" tuzagi bu sinirla
kapanir.

Kesilmis asset'ler (id + tek cumle) icin `/asset-prompt-gen`, tek kare illustrasyon
ve kart gorselleri icin `/image-prompt` — ikisini karistirma.

### Adim 4 — Placeholder sozlesmesi: kod dosya yolu bilmez

Bu, hattin tamaminin dayandigi tek kural. **Faz 2'de kur**, sonradan eklenmez.

```js
// data/art.js — ajanin dokundugu TEK kod dosyasi
export const ART = {
  hero: 'assets/hero.webp',
}

// src/Art.js
Art.get('hero')   // manifestte varsa ve yuklendiyse texture; yoksa prosedurel placeholder
```

`src/` icinde **hicbir yerde** `assets/...` yazmaz. Bir gorsel indiginde entegrasyon
tek satirlik manifest eklemesidir — oynanis dosyalarina dokunulmaz, dongu bozulmaz.
Placeholder tarafi Faz 3'teki oncelikle ayni: prosedurel geometri > basit texture >
duz renk kutu.

**Yukleme basarisiz olursa placeholder'a dus.** Eksik dosya yuzunden siyah sahne
almak, bu hattin en pahali hatasidir.

### Adim 5 — Indikce devreye girsin

Her tur raporu geldiginde, elindeki isi **bitirdikten sonra** (yarim birakma):

1. WebP'ye cevir — `cwebp -q 82`, kart boyutunda fark gorunmuyor
2. `assets/<id>.webp` olarak yaz, manifest satirini ekle
3. Ekran goruntusu al ve **bak** — Faz 5'in okunabilirlik olcumu burada da gecerli:
   ayirt edilmesi gereken sey viewport genisliginin **>= %6'si** mi?
4. `README.md`'de hangi asset'in gercek, hangisinin placeholder oldugunu guncelle

Prototip **hangi asset'in indigine bakmadan** her an teslim edilebilir olmali.

### Adim 6 — Begenilmezse: hedefli yeniden uretim

Kullanici bir asset'i begenmezse **tum seti yeniden uretme.** Sadece o id'yi bir
sonraki tura koy, prompt'una neyin yanlis gittigini tek cumleyle ekle
(`too dark`, `wrong silhouette`, `reads as a rock not a tent`). Eski dosya yenisi
inene kadar yerinde kalir — oyun hicbir an kirik gorunmez.

**Stil degisirse durum farklidir:** kullanici stili begenmediyse Adim 1'e don, ama
bunu **bir kez** yap. Ikinci stil turundan sonra secilen stil kilitlidir; ucuncu tur
prototipin sorusunu cevaplamiyor, sadece kota harciyor.

### Hattin sinirlari

- Gorsel uretimi **kullanicinin ChatGPT kotasini** harcar. Kac gorsel olacagini
  Faz 1'de, liste ciktiginda soyle.
- Bir gorsel ~1-2 dk uretim + ~1 dk indirme; 10'luk bir tur ~20-30 dk. 30 asset ≈ 3 tur
  ≈ 1-1,5 saat arka planda. Bu, prototip suresinden uzundur — o yuzden hat **arka planda**
  doner ve prototip her an placeholder'la teslim edilebilir kalir.
- Chrome MCP **tek tarayiciyi** surer. Sanat ajani Chrome'dayken sen Chrome'a dokunma;
  prototipe ekran goruntusu icin bakacaksan ajanin raporunu bekle.
- Diskte yer kontrolu: 10'luk tur ~25 MB PNG iner. Yer yoksa dosyalar sessizce
  eksik iner ve **eslesme kayar** — tur oncesi `df -h` bak.

### 3B calisiyorsak — gorsel zinciri modele kadar uzar

**Sprite varsayilandir; bu bolum yalnizca brief acikca 3B model istediginde acilir.**
img2threejs'in var olmasi bir sprite oyununu 3B'ye cevirmek icin gerekce degildir.

3B ise zincir sudur:

```
Gemini generate_image  →  referans kare  →  img2threejs  →  TS factory  →  sahnede canli
```

1. **Referans kareyi uret.** Nesneyi tek basina, temiz zeminde, silueti okunur bir
   aciyla. Oyun ici kare degil — burada istedigimiz **nesnenin kendisi**. Karakterde
   T/A-poz, propta uc-ceyrek acisi.
2. **`img2threejs` skill'ini yukle ve calistir.** Cikti: `createXModel(): THREE.Group`
   TypeScript factory'si + `ObjectSculptSpec` JSON'u. Mesh dosyasi yok, indirme yok —
   okunabilir, diff'lenebilir, **animasyona hazir** kod (pivot + socket hiyerarsisi).
3. **Sahneye tak.** Factory `data/art.js` manifestinin degil, `src/` altindaki model
   modulunun isidir — cunku ciktisi kod, asset degil. Placeholder sozlesmesi burada da
   gecerli: model gelene kadar primitive dursun, gelince degissin.
4. **Animasyon** factory'nin verdigi pivotlardan surulur. Bu, img2threejs'i primitive
   yiginina tercih etmenin asil sebebi: kutu yiginini rig'leyemezsin, bunu rig'lersin.

**Kurulum yoksa** `img2threejs-setup` skill'i kurar (tek checkout + Claude/Antigravity
symlink'leri). Sculpt hatti deterministik ve mekaniktir — **`agy` uzerinden Gemini'ye
delege edilir**; Claude'da kalan tek sey kabul karari: benzedi mi, oyunun stiline
oturdu mu.

**Sinir:** tek gorsel gizli geometriyi gostermez, sonuc yaklasiktir — ozellikle
karakterlerde. Arac guven seviyesini kendi isaretler; o isareti teslim raporuna tasi.
Ve bu hat **kahraman nesne** icindir. Sahnedeki her cop parcasini boyle kurmaya
kalkarsan prototip suresi patlar.

## Faz 2 — Iskelet (5 dk)

```
index.html          tek giris, import map ile three
src/main.js         boot + dongu
src/Game.js         game.state = { score:0, day:1, coins:0 }   <- duz nesne
src/systems/…       Effects.js, Audio.js, Input.js
src/entities/…      oyuna ozgu olanlar
data/config.js      TUM ayarlanabilir sayilar, tek dosya
```

**Basit tut.** Redux benzeri sistem yok, dependency injection yok, her yere EventBus yok.
Kalitim yerine kompozisyon: `entity.addComponent(new Health())`.

**`data/config.js` bastan doldur, gercek degerlerle.** Sayilar koda gomulurse her ayar bir
kod degisikligi olur ve iterasyon durur.

**Bir sozlesme sart:** `game.advance(seconds)` — simulasyonu **gercek zaman beklemeden**
sabit adimlarla ilerletir. Bunsuz 7 gunluk bir kampanyayi test etmek 35 dakika surer; bununla
saniyenin altinda. Olculmus.

`advance()` yalniz oyun mantigini degil, **simulasyonun dokundugu her saati** sanallastirmali:
ses saati, `performance.now()`, animasyon zamani. Bir saat gercek kalirsa sim **sessizce hicbir
sey yapmaz**. Olculmus: `advance()` hic vurus uretmedi, cunku `AudioContext.currentTime` senkron
dongu boyunca donuyordu — sanal saat + `beginSim()/endSim()` ile cozuldu.

### three.js: vendor mi CDN mi

Cevrimdisi calismasi ya da tek dosya paylasilmasi gerekiyorsa **vendor'la**
(`vendor/three.module.js`, import map). Yoksa CDN daha hizli. **Bunu bastan sor ya da karar
verip yaz** — sonradan degistirmek dagitim adimini yeniden yazmak demek.

### Kamera tipi — bastan sec, sonra degistirme
3D aksiyon/platform -> `PerspectiveCamera`. Strateji, izometrik, cozy -> `OrthographicCamera`.
Zoom, yumusak hareket ve shake **her ikisinde de** olmali. **Kamera eylemi anlatir**, sadece
gostermez.

### Girdi — `InputManager` soyutlamasi
Oynanis kodu **asla** DOM olayina dogrudan baglanmaz:

```js
input.isPressed('ACTION')   //  klavye, mouse ya da touch — cagiran bilmez
input.position()            //  ekran ya da dunya konumu
```

Masaustunde mouse+klavye, mobilde touch. Bu soyutlama olmadan mobil destegi eklemek her
oynanis dosyasina dokunmak demektir.

## Faz 3 — Cekirdek dongu (12 dk)

Sirasiyla: oyuncu bir sey yapabiliyor -> dunya tepki veriyor -> odul goruluyor -> tekrar
edilebiliyor. **Her adim calisir halde birak.** Yarim sistem, hic olmayan sistemden pahalidir.

**Asset onceligi:** procedural geometri > uretilmis basit texture > placeholder > gercek asset.
Agac = silindir govde + kure yaprak + partikul. Ev = kutu + egik cati. **Once oynanisi dogrula**,
sanat sonra gelir ve prototipin sorusunu degistirmez.

## Faz 4 — Juice + ses (6 dk) — bu faz atlanamaz

**Her onemli eylem gorsel VE isitsel karsilik alir.** Bu prototipin varlik sebebi: fikrin
eglenceli olup olmadigi hissten anlasilir.

| Katman | Zorunlu |
|---|---|
| Hareket | smooth interpolation, ease, kamera takibinde yumusama |
| Etki | scale punch (1.2x), kucuk rotasyon shake, partikul burst, ses |
| Kamera | zoom, yumusak hareket, **shake tek kanaldan** (`camera.setShakeOffset(x,y)`) |
| Girdi | mouse + klavye + **touch**; oynanis DOM olayina baglanmaz |
| Partikul | hit (kucuk, rastgele hiz, fade) · collect (yukari, altin his) · level up (halka + shake) |

Partikuller **havuzlanir**, tek tek olusturulup yok edilmez. Tavan koy (300 iyi bir sayi).
Harici partikul kutuphanesi yok.

**Ses — Web Audio API, harici dosya yok.** `AudioManager`: oscillator + frequency sweep +
gain fade. Collect = yukselen sweep. Hit = noise burst + dusuk frekans. Hata = alcalan
sawtooth. Basari = uc notali arpeggio. **Pitch varyasyonu ekle**, ayni ses ust uste calinca
yorucu olur. AudioContext'i **ilk kullanici etkilesiminde** resume et.

> Juice oyuna ozgu degildir. Bir onceki prototipten `Effects.js` ve `AudioManager.js`
> kopyalanabiliyorsa **kopyala**. Olculmus: kodun %32'si oyundan bagimsizdi.

## Faz 5 — Bak ve tek gecis (4 dk)

**Ekran goruntusu al ve KENDIN BAK.** Rapor gorsel kanit degildir.

Sonra **uc sayiyi olc**, goz karariyla karar verme:

1. **Okunabilirlik.** Oyuncunun ayirt etmesi gereken sey (birim, bina, kart) varsayilan
   kamerada viewport genisliginin **>= %6'si** olmali. Olcum: mesh'in kose noktalarini
   kameraya projekte et, ekran genisligini piksel olarak al.
   *Neden kural:* bir kosuda "olcek yanlis, kasabalar nokta gibi" diye teshis koydum;
   olcunce 1280 px'de **129 piksel (%10)** cikti — teshis yanlisti ve bir ajani dunyayi
   yeniden olceklemeye gonderecektim. **"Yanlis gorunuyor" olculmeden teshis degildir.**
2. **Bosluk.** Varsayilan kameranin gosterdigi her "yer"de bir sey olmali. Olculmus hata:
   5 ada uretip 3 yerlesim koymak — iki ada bombos kaldi ve ekran bos gorundu.
   Kural: **yer sayisi <= icerik sayisi.**
3. **Duyulabilirlik.** Master bus'a analyser tak, 1 sn ornekle: tepe ve RMS yazdir.
   Tepe < 0,7 → duyulmuyor. Tepe > 0,98 → kirpiyor, limiter ekle.
   *Neden kural:* "hic ses yok" sikayetinde olcum RMS **0,018** cikti; tahminle degil
   olcumle duzeldi (0,123'e). Prosedurel seste bu, okunabilirligin muadilidir.

Sonra dort soruyu sor ve **yalnizca en yuksek etkili olani** duzelt:

- Cekirdek dongu 10 saniyede anlasiliyor mu?
- Geri bildirim tatmin edici mi?
- Tekrar etmek icin sebep var mi?
- En buyuk eksik eglence unsuru ne?

**En fazla 3 duzeltme. Yuzey detayina dokunma** — sis, dalga, cok katmanli kiyi, gun ici isik
tonu. Olculmus: bunlara 25 dakika harcadim ve ekran goruntusunde hicbiri oyunu daha oynanir
yapmadi. Ayirt edici soru: *bu efekt oyuncunun bir seyi ANLAMASINA yardim ediyor mu, yoksa
sadece guzel mi?* Teslimat yayi anlatiyor; sis anlatmiyor.

---

## Yapma — her biri olculmus bir maliyet

| Yapma | Maliyet |
|---|---|
| Isi 19 pakete bolmek, 8 dalga | 1,04x hizlanma, 5 saat |
| Kabul kriteri suiti + tarayici surucu kapilar | ~5.000 satir; kirmizilarin yarisi kapinin kendi hatasiydi |
| Pakete mutasyon testi yazdirmak | ~60 dk |
| `effort: high` | 24-38 dk/paket; `medium` 7-19 dk |
| Ajanlarin kendi fixture'ini uydurmasi | iki sema, ~50 dk |
| Save/tutorial/ayarlar/erisilebilirlik | GDD istese bile prototip disi |
| Determinizm/digest kaniti | GDD'nin tasarim sorusu bu degilse gereksiz |
| Ekran goruntusune bakmadan "polish yapildi" demek | kompozisyon hatasi sona kadar tasinir |
| Durum degistiren gorseli **tek** ekran goruntusuyle dogrulamak | Sprite flip kodu dogruydu ama `THREE.Sprite` negatif olcegi yok sayiyor — ozellik bastan sona oluydu, kullanici oynayana kadar fark edilmedi. **Iki durumu da yakala ve karsilastir** |
| Modul kaynagini test edip **teslim edilen build'i** test etmemek | Tarayici modul onbellegi eski dosyayi servis eder; duzeltilmis bug duzelmemis gorunur. Ciktiyi cache-bust parametresiyle test et |
| Sayisal alani `undefined` birakmak | Bir kare sonra NaN; AudioParam'a giderse rAF icinde exception atar. **Siyah sahne + calisan HTML HUD = dongu oldu; once konsol, sonra renderer** |
| Gorsel insin diye kodu bekletmek | Hat saatlerce donebilir; o sure cekirdek donguye gider. Placeholder'la yaz, gorsel gelince manifest satirini ekle |
| Damgayi uretim talimatinin onune koymak | Model tum istegi tek konu sanip kolaj uretir — olculmus. Damga EN SONDA (`/image-prompt` Kural 1) |
| Sanat ajanina `src/` acmak | Olcumdeki iki-sema tuzagi. Ajanin tek kod temasi `data/art.js` manifestidir |
| Stil onayini beklemek | Onay bloklayan tek sanat adimi ama **seni** bloklamaz; sen Faz 2-3'tesin |
| Ucuncu stil turu | Ikinci turdan sonra secim kilitli. Ucuncu tur prototipin sorusunu cevaplamiyor, kota harciyor |
| Asset promptunu `low` ajana yazdirmak | Bozuk stil blogu 10 gorseli cope atar; tasarrufun tamami geri gider |

**Test yazma.** Tek istisna: prototip kostuktan sonra, 40 satirlik bir duman kontrolu —
sifir console error, canvas var, bir frame render edildi, 60 saniye ilerlet ve oyun ilerliyor.

## Teslim

1. Calisan build + tek satirlik calistirma komutu
2. `README.md`: nasil calistirilir · kontroller · cekirdek oynanis · **yapilanlar** ·
   **yapilmayanlar** · sonraki iterasyon fikirleri
3. Bir ekran goruntusu
4. Iki olcum: okunabilirlik yuzdesi ve "her yerde bir sey var mi"
5. **Sanat durumu:** secilen stil (tek cumle) · `ART.md`'de kac id'nin gercek gorseli
   var, kaci placeholder · arka planda hala donen tur varsa hangisi

Kullanici daha fazlasini isterse: gercek sanat / shader / ses kimligi / performans / UI
cilasi ise **`/polish`**, yeni sistem veya mekanik ise **`plan-build`**. Prototip,
"bu fikir eglenceli mi" sorusunu cevapladiginda isini bitirmistir.
