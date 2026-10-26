---
name: prototype-full
description: >-
  Bir GDD'yi ya da oyun fikrini UCTAN UCA, tam otonom, coklu ajan takimiyla
  oynanabilir Three.js prototipe cevirir: derin plan -> takim kurulumu ->
  paralel dalgalar (sanat/icerik/QA) -> goal dongusu -> rapor. Plan onaylandiktan
  sonra soru sormaz, bitene kadar calisir. Kullan: "tam prototip", "prototipi
  sonuna kadar yap", "multi agent prototip", "prototype-full", "oyunu bastan
  sona uret", "takimla prototip".
metadata:
  version: v1
  publisher: musab
---

# prototype-full — takimla, bastan sona, durmadan

Bu skill bir orkestratordur. Kod zanaatinin kurallari **`prototype`** skill'indedir:
**ilk is olarak onu yukle ve uygula** — Three.js/Web Audio zorunlulugu, faz sureleri,
`game.advance()` sozlesmesi, placeholder sozlesmesi, juice tablosu, kesme kurallari
hep orada. Bu dosya onun **uzerine** takim, paralellik ve otonomi katmanini koyar.

---

## 0. Degismeyen dort kural

1. **Derin dusun, bir kez.** Ortamdaki en yuksek muhakeme kademesini kullan. Kod
   yazmadan once cozumlemeyi tek seferde derinlemesine yap ve `PLAN.md`'ye yaz.
   Sonra uygulamada muhakemeyi kis ve hizli ilerle.
2. **Bir tur soru, sonra sessizlik.** Faz 0'da en fazla bir tur soru. Plan
   onaylandiktan sonra **hicbir sey icin sorma** — en makul varsayimi sec,
   `PLAN.md`'ye tek satir not dus, devam et. Istisna: veri kaybi ve para harcayan
   islemler.
3. **Cekirdek kodu bolme.** Takim, cekirdek dongunun *etrafinda* calisir; icinde
   degil. Gerekcesi Bolum 2'de, olculmus.
4. **Bitene kadar surdur.** `goal` kriterleri yesillenene kadar dur yok. Uc ardisik
   turda hicbir kriter degismezse dur ve nedenini yaz.

---

## 1. Faz 0 — Tasarim kilidi (tek bloklayan adim)

| Girdi | Ne yap |
|---|---|
| GDD dosyasi var | Oku, tek paragrafla ozetle, **tek soru**: "boyle mi anladim?" Onay al. |
| Sadece fikir var | Tek sayfa GDD'yi sen yaz (alti baslik), goster, onay al. |
| Fikir de bulanik | `/grill-me` ile **TEK tur** mulakat. Bir tur, sonra kes. Ya da tek mesajda 4 soru: tur+referans oyun · ton · kamera · oyuncunun ana eylemi. |

Alti baslik: **tur ve referans oyun · cekirdek dongu · oyuncunun ana eylemi ·
kazanma/kaybetme · ton · kamera ve bakis acisi.**

Onaydan sonra bu skill **konusmayi birakir, is yapmaya baslar.**

---

## 2. Faz 1 — Derin plan (`PLAN.md`)

Bu, "Deep Think"in yerini tutan adimdir. Tek seferde, derinlemesine, yaziya dokerek.
`PLAN.md` su sekiz basligi **doldurmadan** kod yazma:

1. **Cekirdek dongunun tam akisi** — oyuncu eylemi -> geri bildirim -> odul ->
   ilerleme -> tekrar. Her okun ne kadar surdugu (saniye) dahil.
2. **Gorsel geri bildirim anlari** — hangi olayda ne patlar: partikul, shake, punch,
   ses. Liste halinde, olay adiyla.
3. **Veri modeli** — `game.state` icindeki her alan, tipi, baslangic degeri.
4. **Dosya haritasi ve sahiplik** — hangi dosyayi kim yazar (Bolum 3 matrisi).
5. **`data/config.js` anahtarlari** — ayarlanabilir her sayi, gercek baslangic degeriyle.
6. **Kesilen kapsam** — GDD'de olup prototipte olmayan her sey, tek satir gerekceyle.
7. **Ilk uc kirilma noktasi** — bu prototipin en muhtemel uc arizasi ve her birinin
   karsi tedbiri. Ornek: "AudioContext suspended kalir -> ilk tikta resume";
   "`advance()` ses saatini sanallastirmazsa sim sessiz kosar -> beginSim/endSim".
8. **Kabul kriterleri** — 3-8 adet, calistirilabilir. Bunlar `.goal/criteria.json`'a
   yazilir; formati `goal` skill'inde.

`PLAN.md` yazildiktan sonra **onay bekleme**, uygulamaya gec.

---

## 3. Faz 2 — Takimi kur

`define_subagent` ile ajanlari tanimla, `invoke_subagent` ile arka planda baslat,
`send_message` ile durum sor. Buyuk kapsamda `/teamwork-preview` ile takimi tek
seferde ayaga kaldir.

### Neden cekirdek kod tek elde kalir

Olculmus: ayni GDD, iki kosu. Tek akis **18 dakika**, 2.588 satir. 19 pakete bolunmus
14 ajanli kosu **5 saat 6 dakika**, 19.801 satir — **birebir ayni icerik**. Paralellik
kazanci 1,04x. Sebep: her paket bir oncekinin **arayuzunu kesfetmeyi** bekledi ve iki
paket ayni nesne icin iki ayri sema uydurdu.

Ders paralelligi yasaklamak degil, **bagimliligi olmayan eksende paralellemek.** Sanat,
icerik verisi, QA ve arastirma birbirinin arayuzunu beklemez. Cekirdek dongu bekler.

### Takim kadrosu ve DOSYA SAHIPLIGI

Bu matris pazarliksizdir. Iki ajan ayni dosyaya yazarsa kosu coper.

| Ajan | Isi | **Sadece su dosyalara yazar** |
|---|---|---|
| **Sen (orkestrator)** | Iskelet, cekirdek dongu, juice, ses, entegrasyon | `src/**`, `index.html`, `data/config.js`, `PLAN.md` |
| `art-runner` | `generate_image` turlari, post-process, manifest satiri | `assets/**`, `data/art.js` |
| `content-smith` | Seviye/kart/dalga/ekonomi verisi, dengeleme tablolari | `data/content/**` |
| `qa-scout` | Sayfayi ac, konsolu oku, screenshot al, kriterleri kos, bulgu yaz | `docs/qa/**` (kod duzeltmez, **rapor eder**) |
| `scout` | Tek seferlik arastirma (kutuphane, API sekli, teknik) | `docs/research/**` |
| `fixer` × N | **Prototip KOSTUKTAN SONRA** debug/optimizasyon | orkestratorun atadigi tek dosya |

Her `define_subagent` sistem promptunun **son satiri** su olmali:

> Yukarida listelenen dosyalar disinda hicbir dosyaya yazma. Baska bir dosyada
> degisiklik gerekiyorsa yapma — rapor et.

### Dalgalar

```
DALGA 0  (sen, tek)      PLAN.md + .goal/criteria.json
                              |
DALGA 1  (paralel)  ┌── art-runner: stil arama turu (10 stil, TEK sahne)
         baslatir   ├── content-smith: icerik verisi taslagi
                    └── scout: varsa acik teknik soru
                              |
         SEN bu sirada beklemeden: iskelet + cekirdek dongu yaziyorsun
                              |
DALGA 2  stil secildi ─→ art-runner: asset turlari (10'arli, sikliga gore)
         sen: juice + ses
                              |
DALGA 3  (paralel)  ┌── qa-scout: kriterleri kos, screenshot, konsol
                    └── sen: qa bulgularini duzelt
                              |
DALGA 4  goal dongusu — kriterler yesillenene kadar
         takilan kriter varsa: fixer ajani, tek dosya atamasiyla
```

**Ajan beklemek yok.** Dalga 1'i baslattigin anda kod yazmaya donersin. Rapor
geldiginde elindeki isi **bitirip** entegre edersin — yarim birakma.

---

## 4. Sanat hatti — `generate_image`

1. **Stil arama:** ayni sahne, 10 farkli stil. Sahne oyunun **en yogun ANI** olmali ve
   oyun ici goruntu gibi kadrajlanmali — kamera, kompozisyon, HUD'un oturacagi kenar
   bosluklari dahil. Menu, kapak, "kazandin" ekrani **yanlis secimdir**. Test: "bu
   kareyi oyunun magaza sayfasina koyar miydim?" Hayirsa yanlis sahne.
2. **On stil gercekten farkli eksenlerde** olsun, ayni seyin on tonu degil: gouache ·
   duz vektor · kil/clay · cel-shaded · murekkep yikama · kagit kesme · painterly ·
   low-poly · risograph · sulu boya. Projenin kalite barina uymayanlari **listeye alma**
   — yoksa secim on secenek arasindan degil, uc ciddi secenek arasindan yapilir.
3. **En-boy orani** sahneye gore: oyun ici kare `16:9`, kart/portre `3:2` veya `1:1`.
4. **Onay:** 10 kareyi numaralayarak goster. Bu tek bloklayan sanat adimidir ama seni
   bloklamaz — sen cekirdek donguyu yaziyorsun. "3 ile 7 karisimi" denirse birlestir,
   tek cumlelik onay al, ucuncu tura cikma.
5. **Stil kilidi:** secilen kareyi `ImagePaths` referansi olarak sonraki her uretime
   gecir. Stil blogu harfi harfine sabit kalir — tek kelime degistirirsen set ikiye
   bolunur.
6. **Entegrasyon:** her gorsel indikce -> WebP (`cwebp -q 82`) -> `assets/<id>.webp`
   -> `data/art.js`'e **tek satir**. `src/` altina dokunulmaz.
7. **Begenilmezse:** tum seti degil, sadece o id'yi yeniden uret; prompta neyin yanlis
   oldugunu tek cumleyle ekle (`too dark`, `reads as a rock not a tent`). Eski dosya
   yenisi inene kadar yerinde kalir — oyun hicbir an kirik gorunmez.

### 3B ise: gorselden modele

Sprite varsayilandir; bu adim **brief acikca 3B model istediginde** acilir.

```
generate_image  →  referans kare  →  img2threejs  →  TS factory  →  sahnede canli
```

Referans kare **nesnenin kendisidir**, oyun ici kare degil: temiz zemin, okunur
siluet, propta uc-ceyrek acisi, karakterde T/A-poz. `img2threejs` skill'ini yukle ve
kos — ciktisi `createXModel(): THREE.Group` factory'si ve `ObjectSculptSpec` JSON'u.
Mesh dosyasi yok; **kod**, o yuzden `assets/` degil `src/` altina girer ve
`art-runner`'in degil **senin** sahipligindedir.

Animasyon factory'nin pivot/socket hiyerarsisinden surulur — kutu yigini rig'lenmez,
bu rig'lenir. **Kahraman nesne icin**; sahnedeki her ufak parcayi boyle kurma.
Tek gorsel gizli geometriyi gostermez: sonuc yaklasiktir, arac guven seviyesini
kendi isaretler, o isareti rapora tasi.

**Video uretimi bu ortamda yok.** Hareket gerekiyorsa sahte video yerine Three.js ile
**gercekten calisan** sahneyi yap; zaten daha iyi cevap verir.

Asset gecikirse prototip **placeholder ile teslim edilebilir** kalir. `README.md`'de
hangisinin gercek hangisinin placeholder oldugunu yaz.

---

## 5. Faz 3 — goal dongusu

`goal` skill'ini yukle ve `.goal/criteria.json` uzerinden don:
**OLC -> TESHIS -> DUZELT -> TEKRAR OLC.**

- Her turda **butun** kriterleri kos, kismi degil — bir duzeltme baskasini kirabilir.
- Kirmizilardan **birini** sec: en cok digerini acan hangisiyse o. Sebebini yaz.
  Sebep yazilmadan yapilan duzeltme tahmindir.
- Kriteri **gevsetme**. Esigi dusurmek hedefi degistirmektir; gerekiyorsa acikca soyle.
- Bu asamada kullaniciya soru yok — sadece tur raporu: `tur 3 — C1 yesil, C2 kirmizi
  (sebep: ...), C3 yesil`.

Durma kosullari: hepsi yesil (basari) · uc turda hic degisim yok (dur, anlat) ·
insan kilidi (kriteri `blocked_by_human`'a tasi, kalanlarla devam et).

---

## 6. Basari olcutu ve sinir

Sorulan soru **"dogru mu" degil, "guzel mi, oynanir mi, tekrar etmek istiyor muyum".**
Kapi suiti, mutasyon testi, determinizm kaniti yok. Dogrulama: goal kriterleri +
**kendi gozunle** ekran goruntusu + 60 saniye oynamak. Rapor gorsel kanit degildir.

**Prototip sunlar saglaninca biter:** cekirdek dongu oynaniyor · kullanici oynadi ve
cevap verdi · gelen istekler yeni mekanik degil, var olani derinlestirme.

Shader katmani, ses kimligi/aranjman, instancing, sprite animasyon hatti, asset
envanterini tamamlama — **bu skill'in isi degil.** O sinir asilirsa prototip sessizce
testsiz bir urune doner.

---

## 7. Teslim

**`docs/runs/<YYYY-MM-DD-HHMM>-prototype-<oyun>.md`** — repo icine, kendi
scratch/brain dizinine degil, baska hicbir yere kopya cikarmadan:

Gorev · Yapilanlar (dosya yollariyla) · Degisen dosyalar (`git diff --stat`) ·
Dogrulama (hangi kriter yesil, screenshot alindi mi, konsolda kac hata) ·
Yapilmayanlar (yoksa "yok", bos birakma) · **Takim ozeti** (hangi ajan calisti, ne
uretti, kac tur).

**`README.md`** — nasil calistirilir · kontroller · ne yapildi · **ne YAPILMADI ve
neden** · hangi asset gercek hangisi placeholder.

Raporda yazilan her iddia diskteki gercek durumla uyusmali. Yapilmamis bir sey
yapilmis gibi, olculmemis bir sey olculmus gibi yazilmaz.
