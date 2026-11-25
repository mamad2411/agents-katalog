---
name: juice
description: "Animasyonu OLMAYAN bir oyunu canli gosteren her seyin katalogu: squash/stretch, yuruyus, hit flash, vurus kenari, hitstop, kamera sarsintisi, sprite shader'i, havuzlanmis efekt katmani, aura, simsek, cozulme. Her teknik olculmus, calisan koddan cikarilmis ve kopyalanabilir. Triggers: juice, game feel, oyun hissi, hit feedback, vurus hissi, shader efekt, shader ekle, squash, flash, ekran sarsintisi, hitstop, canlandir, hareketli gostersin, efekt ekle, guzellestir, animasyon hissi, olu duruyor."
user-invocable: true
argument-hint: "[katman: transform | shader | efekt | konfor | hepsi] veya serbest istek"
---

# /juice — animasyonun yokken canli gorunmesi

Elinde tek kare sprite'lar var. Sprite sheet uretmek AI ile tutturulamiyor
(alti kare istersin, alti farkli karakter gelir). Bu skill o sorunu **cozmuyor**,
**atliyor**: hareketi gorselden degil **motordan** aliyor.

> Siluet degisir > Ic detay degisir · Tek program > Efekt basina program
> · Anlatan efekt > Guzel efekt

Kaynak: `~/Projects/necrobeat`. Buradaki her sayi o oyunda olculdu; teknikler
oradan **kopyalanabilir**. Dosya haritasi `references/katalog.md`'de.

## Ne zaman bu skill

| Durum | Skill |
|---|---|
| "Oyun olu duruyor", "hareket etmiyor gibi", "vurunca hissedilmiyor" | **`/juice`** |
| "Shader'la guzellestir", "efekt ekle", "daha dolu olsun" | **`/juice`** |
| Genis cila turu: sanat hatti + ses + performans + UI hizasi | `/polish` (shader alani bu skill'e devreder) |
| Cekirdek dongu henuz oynanmiyor | `/prototype` |

`/polish` bu skill'in ustunde durur: `/polish shader` cagrildiginda **buraya gelinir**.
Ters yon de gecerli — bu skill bir efekti kanitlarken `/polish`'in olcum kuralini
kullanir: *"yaptim" kanit degildir, "olctum, su cikti" kanittir.*

---

## Uc katman — hangi isi hangisi yapar

Bir sey "hareketsiz duruyor" dendiginde once **hangi katmanin eksik oldugunu**
tespit et. Yanlis katmana yazmak en pahali hata (bkz. Demir Kural 1).

| Katman | Nerede calisir | Ne tasir | Maliyet |
|---|---|---|---|
| **1 · Transform** | JS, kare basina | siluet: squash, yuruyus, punch, sarsinti, hitstop, zoom | ~0 |
| **2 · Sprite shader** | tek fragment programi, uniform dallar | doku ici: cevirme, dalgalanma, vurus kenari, flash, alev, cozulme | dal alinmazsa ~0 |
| **3 · Efekt katmani** | havuzlanmis InstancedMesh + ayri malzemeler | sahneye eklenen sey: halka, patlama, sutun, aura, simsek, hasar sayisi | tek draw call |

---

## Demir kurallar — hepsi olculdu, hicbiri tahmin degil

**1 · Dolu bir govdenin ICINDE UV kaydirmak gorunmez.**
Agir dusmanlar (kemik, golem, can-kafa, elit) olu kagit gibi duruyordu. Shader'la
dikey UV ezilmesi ve sicak hava titresimi denendi; uc ayarda (kapali / normal / x5)
yan yana bakildi — **siluet degismedi**. Sebep mekanik: goz siluete bakar, ic
dokuya degil. Hayaletin kuyrugunda ayni teknik ISE YARIYOR cunku etki ince ve alta
yigili, yani siluetin kendisi.
→ **Kural: govde hareketi Katman 1'e (olcek), kenar/etek hareketi Katman 2'ye.**

**2 · `THREE.Sprite` negatif olcegi yok sayar.**
`sprite_vert` olcegi `length( modelMatrix[0].xyz )` ile alir; isaret kaybolur.
Bastan sona dogru yazilmis bir flip kodu **tamamen olu** kalmisti ve tek kare ekran
goruntusunde "cevrilmemis" ile "cevrilemeyen" ayni goruntudur.
→ Cevirme dokuda yapilir: `uFlip=1` iken u ekseni ters okunur.

**3 · Tek program, uniform dallar.**
three, program onbellegini `onBeforeCompile`'in **kaynak metniyle** anahtarlar.
Hook tek ve degismez ise tum sprite'lar ayni programi paylasir; sprite basina
yalnizca uniform DEGERI degisir. Dallar uniform uzerinden yazildigi icin bir cizim
cagrisinda kosul sabittir (uniform control flow): `fwidth`/`texture` guvenlidir ve
**dal alinmadiginda maliyet sifira yakindir**. Alev dalinin icindeki ikinci doku
okumasini sahnedeki diger 350 sprite odemez.

**4 · Iki yolu birden yaz: WebGL (GLSL) ve WebGPU (TSL).**
Masaustu profili WebGPU kosuyor. Tek yola yazmak, **oyuncunun oynadigi surumde
efektin hic olmamasi** demek. Bu tuzak once boss telegrafinda cokmeye yol acti,
sonra alevde sessizce olu kaldi.

**5 · Ayni anda kosan seylerin PERIYODU/FAZI ayni olmamali.**
Ayni tipteki 40 dusman ayni adimi ayni anda atarsa tek bir organizma gibi okunur;
cozum indeksle faz kaydirmak (`sin((t + i * 0.61) * freq)`). Ayni sey sahnedeki
auralar, mesaleler ve dongusel efektler icin de gecerli — her orneğe kendi fazi
verilir. Parlaklikta tek sinus da metronom gibi okunur: iki FARKLI hizda gurultu
kullan (biri yavas nefes, biri catirti).

**6 · Zamana yayilan bir iddia TEK KAREDEN kanitlanmaz.**
Dongunun iki ucundan >= 24 ornek al ve degerin gercekten degistigini goster.
Tek kare, "efekt yok" ile "efekt var ama o an notr" arasindaki farki gostermez.

**7 · Olcerken simulasyon KOSUYOR olmali.**
Bir olcum "0 hareket" raporladi ama efekt saglamdi: kart secim ekrani acikken
orneklenmisti, simulasyon duruyordu. Kapi once oyunu oynanir duruma getirmeli.
Ayrica gecis animasyonu bitmis olmali — solma sirasinda olcen bir kapi 88 px
raporladi, oturmus deger 106 px'ti.

**8 · Havuzla ve tek draw call'a indir.**
Eski halka havuzu 18 ayri `Mesh`'ti; draw call efekt sayisiyla dogrusal buyuyordu.
Simdi tek `InstancedMesh`: tur/yas/renk per-instance attribute. **1 efekt de 150
efekt de tek draw call.** Instance verisi yalnizca dogum/olumde yazilir, her kare
degil; kare basina tek uniform (`uTime`) yeter. Suresi dolan instance sondan
takasla cikarilir, yoksa olu instance fill-rate yer.

**9 · Genlik tavani UZUNLUKLA olceklenmeli.**
Yay genligi tavani sabit 0.82'ydi. 13 birimlik gok simsegi `len*0.105 = 1.37`
istiyor, 0.82 aliyordu — **neredeyse duz bir cizgi**. Tavan 1.7'ye cikinca simsek
simsek gibi durdu. Kisa yaylar zaten tavana carpmiyordu, yani hata uzun yaylarda
gizliydi.

**10 · Konfor bir ayar degil, tasarim siniri.**
Kullanici asiri flash/shake/bloom'dan rahatsiz oldu. Her siddet carpani uzerinden
gecer (`fxShake`, `fxFlash`, `fxHitstop`) ve ayarlardan **kapatilabilir**; kapaliyken
oyun hala okunakli kalmali. Ayirt edici soru: *bu efekt oyuncunun bir seyi
ANLAMASINA yardim ediyor mu, yoksa sadece guzel mi?*

**11 · WebGPU'da flash icin `material.color`'a guvenme.**
Node materyalinde runtime renk degisimi bazi backend'lerde **bir kare gec ya da
hic** geliyor. Ayri bir uniform ac (`uHitFlash`) ve tum govdeyi onunla tasi.

**12 · Hitstop'un cooldown'u olmali.**
Yoksa zincirlenir ve oyun kekeleyerek durur. Ayrica kuyruklanan deger tavana
kirpilir.

**13 · Havuza donen nesne TEMIZ donmeli.**
`resetFx`: dissolve/hit/hitFlash/olcek/golge sifirlanmazsa yeni dusman **yari
cozulmus dogar**.

---

## Katalog — ne, nerede, hangi sayi

Tam liste, kod sekli ve kopyalama yolu: `references/katalog.md`.
Ozet (necrobeat'teki dosya → teknik):

| Teknik | Kaynak | Ozu |
|---|---|---|
| squash + yuruyus (gait) | `Billboards.setSquash` | boy ile en TERS oynar; +gait uzayip incelir, −gait basiklasip genisler |
| yuruyus tablosu | `Enemies.GAIT` | tip basina `amp`/`freq`: kemik 0.055/5.0, golem 0.080/2.4, larva 0.095/12.0 |
| vurus punch | `Player.punch` | `beat()` 1'e set eder, `dt*6.5` ile soner; olcek ve flash bunu okur |
| vurus kenari | `uHit` + `fwidth(alpha)` | siluet kenari alfanin turevinden — **ek doku okumasi yok** |
| kalici siluet konturu | `uRim` (0.85) | kalabalikta ust uste binen dusmanlari ayirir, ~6 ALU |
| hasar flash'i | `uHitFlash` | beyaz cekirdek + pembe kenar (`1.14, 0.72, 0.84`), doku detayini silmez |
| yumusak kenar | `uSoft` | hayalet tiplerinde alphaTest merdivenini rampaya cevirir (esik 0.12 → 0.03, **0'a inme**) |
| dalgalanma | `uWob*` | 4 mod; hayalette iki harmonik + tum siluetin yavas suruklenmesi |
| alev | `uFlame` | maske dokudan: `warm = (r−b)·2.2`; dibi sabit, ucu savrulur; iki hizda gurultu |
| olum cozulmesi | `uDissolve` | ince gurultu (x14), dar parlayan serit, asagidan yukari |
| tek draw call efektler | `fx/FlatFX.js` | halka/patlama/sutun/muhur/koni tek InstancedMesh'te |
| aura | `fx/Aura.js` | tier RENK degil **DAVRANIS** degistirir; tek shader, uniform dal |
| yay / simsek | `fx/ArcFX.js` | genlik tavani uzunlukla olcekli; gok simseginde ardil cakmalar kuyrukta |
| hasar sayisi | `fx/DamageNumbers.js` | 0.16 s'de 1.38→1.00 punch, sonra sonen sinus salinimi |
| kamera | `Game.frame` | sarsinti **kamerayi kendi ekseninde** kaydirir (bakis hedefini degil) → sahne egilmez |
| hitstop | `Game.hitstop` | kuyruk + tavan + cooldown (0.075 s) |

---

## Yeni efekt eklerken — sirasi bu

1. **Hangi katman?** Siluet mi degisiyor, ic doku mu, yoksa sahneye yeni bir sey mi
   ekleniyor? Yanlis katman = gorunmeyen efekt (Demir Kural 1).
2. **Var olan hooka sigiyor mu?** Sprite uzerindeki her sey `spriteHook`'a bir uniform
   dali olarak girer — yeni malzeme acma, program sayisini buyutur.
3. **Sahneye eklenen bir sey mi?** `FlatFX`'e yeni stil olarak gir. `STIL_SAYISI`'ni
   **artirmayi unutma** — compat yolu o kadar mesh kurar.
4. **Iki yolu da yaz.** GLSL + TSL. Tek yol yazdiysan bunu raporda soyle.
5. **Ayarlanabilir sayilari `fxconfig.js`'e koy**, koda gomme.
6. **Siddeti konfor carpanindan gecir**, kapatilabilir olsun.
7. **Kapisini yaz** (asagi). Kapi yoksa efekt yok sayilir.
8. **Havuza donusu temizle.**

## Kapilar — bir efekt ne zaman "var" sayilir

| Efekt turu | Kanit |
|---|---|
| Zamana yayilan hareket (yuruyus, nefes, dalgalanma, aura) | dongunun iki ucundan >= 24 ornek; deger gercekten degismeli, ayni anda kosanlar ayni degerde olmamali |
| Durum degistiren gorsel (flip, flash, secili) | **iki durumu da yakala ve karsilastir**; fark yoksa ozellik yok |
| Sahne efekti (halka, aura, simsek) | efekt aktifken ve kapaliyken kare farki; degisen piksel orani |
| Performans | draw call + medyan kare suresi, **once ve sonra**, ayni dusman sayisinda |
| Konfor | ayar acik/kapali iki kayit; kapaliyken oyun hala okunakli mi |

Olcum simulasyon **kosarken** ve gecis bitmis oldugunda yapilir (Demir Kural 7).

## Yapma

| Yapma | Olculmus maliyet |
|---|---|
| Govde hareketi icin shader'da UV ezmek | uc ayarda bakildi, siluet degismedi — bos is |
| Her efekt icin ayri Mesh/malzeme | draw call efekt sayisiyla dogrusal buyudu |
| Yalniz GLSL yazmak | masaustunde (WebGPU) efekt olu kaldi; bir kez de cokme |
| `material.color` ile WebGPU flash | bir kare gec ya da hic |
| Sabit genlik tavani | uzun yaylar duz cizgiye dondu |
| Tek sinus ile parlaklik | metronom gibi okunuyor; goz periyodu yakaliyor — iki hizda gurultu kullan |
| Ekrani doldurmak | kullanici asiri flash/shake'ten rahatsiz oldu; efekt anlatmali |
| Tek kareye bakip "efekt calisiyor" demek | duran bir simulasyonda olcum "0 hareket" verdi, efekt saglamdi |

## Teslim

1. Degisen/eklenen efektlerin listesi, hangi katmanda oldugu
2. **Her efekt icin kapi ciktisi** — sayiyla, once/sonra
3. Performans: draw call + medyan kare suresi, ayni yuk altinda once/sonra
4. Hangi yollarin yazildigi (WebGL / WebGPU) — biri eksikse acikca soyle
5. Konfor ayarlarindan kapatildiginda oyunun hala okunakli oldugu
