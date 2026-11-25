---
name: animate
description: "VIDEO hatti: duragan bir gorselden hareketli klip uret (Wan 2.2 I2V + olc-ve-karar ver dongusu). Sprite sheet istiyorsan /spritesheet-character-generator kullan. Triggers: animate, video uret, sinematik, kesme sahne, i2v, wan, animation-creator, klip uret."
user-invocable: true
---

# Animate — VIDEO hatti (duragan gorselden hareketli klip)

> **Sprite sheet mi ariyorsun?** Bu hat degil.
> Oyun icine girecek yuruyus/saldiri/idle sprite'lari icin
> **[/spritesheet-character-generator](../spritesheet-character-generator/SKILL.md)**.
> Hangisi oldugundan emin degilsen:
> **[/uretim-hatti-sec](../uretim-hatti-sec/SKILL.md)**.
>
> Ayirt edici soru: cikti oyun motoruna **sprite olarak** mi girecek, yoksa
> ekranda **video olarak** mi oynayacak? Sprite ise oteki hat.
>
> Bu belge sprite sheet uretimini hala anlatiyor (kod duruyor ve calisiyor),
> ama yeni sprite isleri icin kullanilmiyor.

Tek bir karakter gorselini image-to-video ile canlandirip sprite sheet'e cevirir.
Uretimi `animation-creator` yapiyor; bu belge **operatorun** ne yapmasi
gerektigini anlatir. Modelin ne yaptigini zaten repo'daki rehber anlatiyor —
pahaliya patlayan hatalarin hepsi operator tarafinda oldu.

- Repo: `~/Projects/animation-creator`
- Inceleme sitesi: https://animation-review-skywalker2506s-projects.vercel.app
- Kuyrugu suren surec: GPU'lu makinede `python -m animcreator.agent --watch`

**Kaynak kare = referans.** Bu hatta stil zaten tarif edilmiyor, kaynak
gorselden geliyor — ve o yuzden kaynak karenin kendisi tek stil otoritesi.
Ayni karakterin farkli animasyonlari icin **ayni kaynak sprite** kullanilir;
yuruyuste kapusonlu, saldirida kel bir karakter tutarsizligi buradan cikar.
Genel kural: **[/reference-style](../reference-style/SKILL.md)**.

---

## Isin akisi

**Sprite ekle** — kaynak gorseli yukler ve karaktere baglar. Once
[hazirla](#2-kaynagi-hazirla--ajan-bunu-yapmaz), sonra:

```bash
python -m animcreator.cli add-character --project necrobeat \
    --name "Crypt Spider" --image "D:/Projects/necrobeat/art/raw/spider-p.png"
```

**Istedigin animasyonlari kuyruga ver** — `--anim` tekrarlanabilir, her biri bir
yuva. Prompt'u yazmazsan o yuvanin preset'i kullanilir.

```bash
python -m animcreator.cli queue --character crypt-spider \
    --anim idle --anim walk.side --anim attack.melee
```

**Prompt'u kendin yaz** — preset yerine geceni istiyorsan:

```bash
python -m animcreator.cli queue --character crypt-spider --anim attack.melee \
    --prompt "the spider rears back on its hind legs and strikes forward once, \
black background, side view"
```

Preset'te `{subject}` gecen yerleri doldurmak icin `--subject "a bone spider"`
yeter; prompt'un tamamini yeniden yazmaya gerek yok.

**Bir surunu birden** — plan dosyasiyla:

```bash
python -m animcreator.cli batch --file plan.json
```

**Ayarlar**: `--frames` uretim karesi (17/25/33/49/65/81, Wan 4n+1),
`--width/--height` (sprite icin 512×512, sahne icin 832×480),
`--variants N` ayni yuvadan N farkli seed, `--dry-run` once ne gidecegini goster.

### Sirayi kendin belirle — kimseye sormadan

Kuyruk `created_at`'e gore islenir; en eski bekleyen is once uretilir. Sirayi
degistirmenin iki yolu var ve **hangisini kullanacagini isin yasi belirler**:

```bash
# YENI is, kuyrugun onune girsin
python -m animcreator.cli queue --character crypt-spider --anim idle --basa

# DUN kuyruga girmis isleri one al (proje / karakter / klip suzgeciyle)
python -m animcreator.cli sira --project necrobeat --basa
python -m animcreator.cli sira --character crypt-spider --sona
python -m animcreator.cli sira --clip idle --basa --dry-run   # once ne tasinacagini gor
```

**O an uretilmekte olan ise dokunulmaz.** Sira yalnizca bekleyenler arasinda
degisir, yani "basa al" bir sonraki isten itibaren gecerlidir; yarim uretim
cope gitmez.

Ikisinin ayri komut olmasinin sebebi yetki: olculdu — anon anahtar is
**eklerken** `created_at` yazabiliyor (yani yeni is dogrudan basa girebiliyor)
ama var olan bir satiri PATCH edemiyor; istek **0 satir etkileyip 200
donuyor**, yani sessizce hicbir sey yapmiyor. `sira` bu yuzden istegi depoya
birakir ve servis anahtarini tasiyan ajan uygular; komut uygulanana kadar
bekler. Ajan kapaliysa istek depoda durur, acilinca islenir.

`sira` tasiyacagi isleri **komutu verdiginde secip id olarak yazar**, suzgec
olarak degil: arada kuyruga giren isler kapsama girmez, yani gormedigin bir sey
tasinmaz.

Sheet karesi diye ayri bir ayar **yok** ve olmamali — sheet uretilen her kareyi
tasir. Kisa animasyon istiyorsan `--frames` dusur.

### Yuva anahtari

`<action>[.<kind>][.<direction>][.<variant>]` — siralamasi onemli degil,
`attack.melee.right` ile `attack.right.melee` ayni yuvadir.

| | |
|---|---|
| action | idle, walk, run, attack, hurt, death, jump, cast, block, dodge, play, scene |
| kind | melee, range, magic, unarmed |
| direction | left, right, forward, back, side |

Ayni karakterin butun animasyonlari **ayni kaynak gorselden** uretilmeli, yoksa
birinde kapsonlu birinde kel cikar. Karakter bir kez eklenir, yuvalar uzerine
binir.

### Nerede gorulur

Uretilenler inceleme sitesinde belirir: izle, **Onayla** / **Reddet**, ya da
"neyin degismesi gerekiyor" kutusuna yalnizca degisikligi yazip revize iste.
Her videonun altinda **indir** ve **paylas** var; paylas videonun kendi acik
adresini verir, karsi tarafin giris yapmasi gerekmez.

Onaylananlarin listesi ve oyuna verilecek manifest:

```bash
python -m animcreator.cli kabul --olc --json kabul.json
```

### Yalnizca video — ve uzun video

Sprite sheet oyuna giren bir sprite icin lazim; sinematik bir sahnede kullanilan
sey videonun kendisi. Olculdu: sahne klibinde sheet asamasi 37 saniye harcayip
**hicbir sey uretmiyor** (BiRefNet tum sahneyi "konu" saymaya calisiyor).

```bash
python -m animcreator.cli video --project "Survival Oyun" \
    --image kare.png --prompt "..." --saniye 6 --basa
```

`scene` yuvasinda sheet zaten uretilmiyor; `queue --no-sheet` ile her yuvada
kapatilabilir.

**Uzunluk parca ekleyerek geliyor.** Wan tek kosuda uzun veremiyor: 81 karede
sahnedeki nesneler klibin ortasinda dagiliyor, saglam sinir **49 kare = 3.06
saniye**. `--saniye 12` dort parca uretir; her parca bir oncekinin SON
KARESINDEN devam eder ve parcalar bitince tek videoda birlesir.

Olculdu (2 parca): 98 kare / 6.12 sn, ek yerindeki kare farki 2.64 — normal
kare farki 1.85, yani gecis goze carpmiyor.

Durust ol: zincir uzadikca sapma birikir. Ilk parca referansa birebir uyar,
dorduncu biraz uzaklasir. Uzun istiyorsan ya kisa tut ya da birkac parcada bir
yeni referans kare ver.

### LOGLARI VE OLCUMLERI OKU — indirdiginle birlikte gelir

Bir klip "temiz" gorunup kullanilamaz olabilir. Kapilar bunu olcuyor ama
uyarilar bugune kadar YALNIZCA uretici makinedeki `work/agent.log`'da
kaliyordu ve o dosya **gitignored** — baska bir makinede calisan kimse
goremiyordu. Olculdu: ince kanali esigin ustunde 20, dongu dikisi esigin
ustunde 300 deneme vardi ve indiren taraf hicbirini bilmiyordu.

`download` artik dosyalarin YANINA rapor yaziyor:

```
out/olcumler.md     insan icin: her deneme + "GOZLE BAK" uyarilari
out/olcumler.json   makine icin: ayni veri, ham
```

**Indirdikten sonra once `olcumler.md`'yi oku, sonra videoyu ac.** Rapor sana
nereye bakacagini soyluyor; uyari "bozuk" demek degil, "gozunle bak" demek.

Esikler: ince kanal > 6.5, delik > 8.0, dongu dikisi > 12.0.

Ayni veri her makineden **sorguyla** da alinabilir (SQL gerekmiyor):

```bash
# dikisi 12'nin ustunde olan denemeler
curl "$URL/rest/v1/anim_takes?select=id,measured->sheet->>seam&measured->sheet->>seam=gt.12"
# govdesi yenmis olabilecekler
curl "$URL/rest/v1/anim_takes?select=id&measured->sheet->>thinPiercePct=gt.6.5"
```

Uretici makinedeysen ham log da orada:

```bash
tail -40 work/agent.log          # uretim, sheet, uyarilar, istekler
grep "GOZLE BAK\|basarisiz\|UYARI" work/agent.log
```

### ONAY HICBIR SEYI SILMEZ

Bir denemeyi onaylamak `approved_take` ve `is_current` isaretlerini tasir,
**baska hicbir seye dokunmaz**. Ayni klibin oteki varyasyonlari yerinde kalir:
sonradan donup "aslinda ikincisi daha iyiydi" demek mumkun olmali, onay geri
alinabilir bir karar.

Silme yalnizca ACIKCA istendiginde olur ve yalnizca istenen sey silinir:

| ne dedin | ne silinir |
|---|---|
| denemede 🗑 Sil | yalnizca O deneme (video, sheet, kayit) |
| klip basliginda 🗑 | klip ve butun denemeleri |
| `cli sil` | eslesen BEKLEYEN isler (uretilmis denemeye dokunmaz) |

Denemesi kalmayan klip de **silinmez** — prompt'u, kaynak gorseli ve karar
gecmisi onun uzerinde duruyor; silinirse ayni yuvayi yeniden uretmek icin hepsi
bastan yazilmak zorunda kalir. (Onceki surum bunu yan etki olarak siliyordu.)

Reddetmek silmek DEGIL: deneme listeden cikar ama kayit durur, "Reddedilen"
sekmesinde gorunur ve sebebi okunur.

### Iki sira: ORTAK ve OZEL

Kuyruk ortak — kim bastiysa, GPU'su bos olan makine uretir. Ama iki uretici
ayni kuyruktan beslendiginde biri "once benim su isim ciksin" diyemiyordu:
oncelik ortak oldugu icin otekinin isini de one aliyordu.

```
params.kuyruk yok    -> ANA SIRA (ortak, herkesin)
params.kuyruk = "ad" -> o makinenin OZEL sirasi
```

Her makine **once kendi ozel sirasini** bosaltir, sonra ortak siradan devam
eder. Baskasinin ozel sirasindaki is o makinede uretilmez — listede "baska
makinenin ozel sirasi" diye gorunur, yani kimin bekledigi bellidir.

**Ilk kurulumda ad sorulur** — makinenin adi degil, KISININ adi:

```bash
python -m animcreator.cli kurulum        # "ad: " diye sorar -> secrets'a yazar
python -m animcreator.cli kurulum --ad furkan     # sormadan
```

Ad makine adindan (DESKTOP-XYZ) da turetilebilir ama kuyruga bakan kimse kimin
oldugunu anlamaz; `furkan` okunur. Yeni bir makine kurarken bu adim atlanmaz.

```bash
python -m animcreator.cli queue ... --ozel     # KENDI sirama
python -m animcreator.cli queue ...           # ORTAK siraya (varsayilan)
python -m animcreator.cli kuyruklar           # ikisini birlikte gor
python -m animcreator.cli sira --clip X --ana --basa   # ozelden ortaga tasi
```

**Hangi veriye bakiliyor:**

| yaparken | okunan |
|---|---|
| `--ozel` ile is basmak | yalnizca KENDI ozel siran; baska makinede uretilmez |
| ortak siraya is basmak | ORTAK kuyrugun kendisi — kac is var, sonuna eklenir |
| `kuyruklar` / panel / web | ikisi birden, ayri basliklar altinda |

Ortak siraya bakan her sey ortak veriyi ceker (`params.kuyruk` bos olanlar);
ozel siraya bakan yalnizca kendi adini. Baskasinin ozel sirasindaki is
gorunur ama "baska makinenin ozel sirasi" diye isaretlidir ve buradan
uretilmez — kimin bekledigi bellidir, kimse otekinin isini kapmaz.

Iki sira AYRI duraklatilabiliyor (panelde iki dugme): ozel sirayi durdurup
ortaktan devam etmek anlamli bir istek.

Yeni bir makineyi bastan kurmak: depodaki `KURULUM.md`.

### Silmek ve degistirmek — TOPLU, tek istekle

Anon anahtarin SILME ve GUNCELLEME yetkisi yok, ve bunu **sessizce** yapiyor:
PostgREST kapali bir DELETE/UPDATE'i hata ile degil **"0 satir etkilendi"** ile
donduruyor. Yani istek 200 doner, govde bos gelir, satir yerinde kalir ve
cagiran taraf sildigini sanir. Olculdu: 82 silme denemesi, hepsi basarili
gorundu, tabloda hicbir sey degismedi — "33 is iptal edildi" raporu bu yuzden
yanlisti.

Dogru yol istek birakmak; ajan servis anahtariyla uyguluyor:

```bash
python -m animcreator.cli sil --project "World Dominion" --dry-run
python -m animcreator.cli sil --clip ambient2
python -m animcreator.cli guncelle --project "World Dominion" \
    --negative "poz degistirme, kollari indirme, ayaga kalkma, yurume, donme"
```

**Is basina bir istek YOLLAMA.** Iki komut da eslesen butun isleri **tek** dosyada
gonderiyor (`{"isler": [...]}`); 200 is silmek 200 dosya degil, bir dosya.
Dongu icinde tek tek istek birakmak depoyu doldurur ve ajanin her turunu
yavaslatir. Once `--dry-run` ile neyin gidecegini gor.

Ikisi de **gercekten uygulanana kadar bekliyor** ve satirin gittigini/yazildigini
dogruluyor — "istek gonderildi" ile "is degisti" ayni sey degil.

Yalnizca **bekleyen** isler silinir/degisir. Uretilmis bir isi silmek take'i
sahipsiz birakir, prompt'unu degistirmek de o klibin neyle uretildigi kaydini
bozar.

### Yanlis yere dustuyse

```bash
python -m animcreator.cli tasi --clip cicek --project "Survival Oyun"
```

Klip ve ona bagli isler BIRLIKTE tasinir. Web'de her klibin ustunde "projeyi
degistir" var. Silmek icin web'de 🗑 — reddetmekten ayri: reddetmek bir
karardir (deneme gecmiste kalir, sebebi okunur), silme geri alinamaz.

### Ciktiyi almak

Sprite sheet her zaman lazim olmuyor — bazen videonun kendisi kullaniliyor
(fragman, sunum, bir sahnenin oldugu gibi girmesi).

```bash
# yalnizca adresler, indirme yok — gomecek olan icin dosya gereksiz
python -m animcreator.cli download --project necrobeat --what all --json adresler.json

# gercekten indir
python -m animcreator.cli download --clip gitarci --what video --takes latest --out out/
```

`--what` video / sheet / atlas / poster / all, `--takes` approved (varsayilan) /
latest / all. Dosya adi klip anahtarindan kurulur (`gitarci_calma_v1.mp4`);
depodaki ad `take_<hash>.<hash>.mp4` ve hangi klip oldugu anlasilmiyor.

### Yeni proje

Proje satiri olmadan o projenin isi kuyruga giremez (`anim_jobs.project_id`
foreign key; eksikse yirmi isin yirmisi de 23503 ile duser). Proje acmak
servis anahtarinin isi ama beklemek zorunda degilsin:

```bash
python -m animcreator.cli add-project --name "World Dominion" --note "kart sanati"
```

Istek depoya birakilir, GPU makinesindeki ajan saniyeler icinde projeyi acar,
komut proje gorunene kadar bekler. Donunce is basabilirsin.

---

## 1. Kollarin nerede oldugunu bil

Iki anahtar var ve hangisinin neyi yapabildigini bilmeden baslarsan bir saatini
`42501` hatasina yatirirsin.

| | anon anahtar | service anahtar |
|---|---|---|
| nerede | web sayfasi, CLI, herkes | **yalnizca GPU'lu makine** |
| yapabildigi | `sources/` altina gorsel yukle, is kuyruga ekle (`pending`), karar yaz | proje olustur, is sil, preset yaz, take/onay yaz |

Kural: sayfadan gelen her sey yalnizca **niyet ekler**. Onayin kendisi bir kayit;
onu duruma ceviren ajandir. Bir yazma denemesi `42501` ya da "row-level security"
diyorsa yanlis anahtarla dogru isi yapmaya calisiyorsundur — anahtari degistir,
politikayi degil.

## 2. Kaynagi hazirla — ajan bunu yapmaz

**Once forma bak: [animation-ready-sprite.md](animation-ready-sprite.md).** Sprite
hangi yone bakiyor, pozu ne, bacaklari gorunuyor mu, zemini ne — animasyonun
kalitesini bunlar belirliyor, prompt degil. Yanlis formda uretilmis bir sprite
hazirlik adimlariyla kurtarilmaz; o belge hem uretim standardini hem kabul kapisini
tasiyor. **Sprite'i uretirken de o belgeye gore uret** — animasyon uretecegini
biliyorsan form karari sprite promptunda verilir, burada degil.

Ozet: saga bakan yan 3/4, notr durus, ayaklar gorunur, tek figur, duz siyah zemin,
golge yok, tam boy + %6 pay. Sol taraf uretilmez — runtime flip.

Yukledigin gorsel ne ise model onu canlandirir. Hazirlik senin isin:

1. Alfa kutusuna kirp
2. Kare tuvale otur, kenarda ~%6 pay birak
3. Alfayi **duz siyah** zemine duzlestir
4. 512×512'ye LANCZOS ile indir

Olculdu: ham RGBA sanat eserleri oldugu gibi yuklendiginde **39 klip kullanilmaz
cikti** — model siyah zemin yerine turuncu/yesil/mavi studyo fonu uydurdu ve
figurun basi ile ayaklari kadraj disina tasti. Sebep prompt degil, girdinin
bicimiydi.

Saydam PNG'yi oldugu gibi verme. Model boslugu karakterin renkleriyle doldurur.

## 3. Tam uzunluk iste, dongu icin kisaltma

Varsayilan **33 kare** (Wan 4n+1 disini sessizce yuvarlar: 17, 25, 33, 49, 65).

Dongu bozuksa kare sayisini dusurme. Olculdu: 46 klip 25 kareye indirildi, **55
tanesi hala sinirda kaldi** ve onay orani degismedi. Kisa cikti uretimden degil,
**dongu kirpicisindan** geliyor: az hareketli kliplerde gurultuyu "en iyi kesim
noktasi" sanip klibin yarisini atiyor. 8 kare @ 16 fps = 0.50 saniye; bir olcumde
219 sheet'in 97'si bir saniyenin altindaydi.

Duzeltmeyi orada yap: kirpici ancak **en iyi dikis kalintisi medyanin %60'inin
altindaysa** kessin. Uretim hattinda kirpma varsayilan olarak kapali
(`--loop-trim` ile acilir) ve `--keyframes 0` uretilen her kareyi tutar.

Dikis raporlanirken hangi sayinin okundugu onemli: **kesilmeyen** bir sheet'te
dogru sayi son karedeki kalintidir, en iyi kesim noktasindaki degil. Ikisi
karistirilirsa dongular oldugundan iyi gorunur (olculdu: ayni klipte 12.66'ya
karsi 15.96).

## 4. Yuva siluete uymali

Model verilen kareyi canlandirir; icerigini degistiremez.

- **Bacagi gorunmeyen, yere kadar cuppeli bir figure yuruyus verme.** Olculdu:
  yatay yer degistirme 5 px — gercek bir adimda 17 px. Prompt'u ne kadar
  duzeltirsen duzelt degismiyor, cunku sorun yapisal.
- **Elinde kilic olan karaktere "silahsiz saldiri" verme.** Kilic karede duruyor;
  model onu silemez. Nesneyi once gorselden cikarman gerekir.
- Arkasi donuk hali de ayni sebeple uretilemez: karakteri dondurmek yeni
  iceriktir, o acinin kendi gorseli gerekir.

Yeni bir nesne istiyorsan onu **hareket olarak** yaz: "ates ekle" calismaz,
"egilip feneri yere birakiyor, onunde ates yaniyor, elini uzatiyor" calisir.

Bu bolumdeki uc madde de ayni koke bakiyor: **kaynagin formu**. Yuva/silüet
uyusmazligini tek tek kovalamak yerine sprite'i bastan animasyona uygun uret —
[animation-ready-sprite.md](animation-ready-sprite.md) o formu ve kabul kapisini
tanimliyor. Elinde zaten yanlis formda master varsa cope atma: kimlik kilidini
master'dan okuyup ondan **ayri bir anchor** turet (§9), master kanon olarak kalir.
