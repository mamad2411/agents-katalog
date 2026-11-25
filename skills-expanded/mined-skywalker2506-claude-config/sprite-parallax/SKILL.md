# /sprite-parallax — Duz bir resme gercek derinlik verme

Tek bir 2D gorsel (kart sanati, sprite, illustrasyon) imlece veya kameraya
tepki veren bir derinlige kavusur. Hearthstone kartlarindaki etki budur ve
tekniğin adi **parallax occlusion mapping**: yukseklik alani piksel basina
taranir, isin ilk carptigi yerde durur, boylece one yakin olan arkadakini
gercekten kapatir.

Kaynak: `~/Projects/world-dominion` — `scripts/gen-depth.py`,
`src/parallax-card.js`, `src/card-parallax.js`. Olculmus sonuc: kart
genisliginin **%2.9'u** kadar yakin-uzak ayrismasi, gorunur bozulma yok.

---

## Yapmayacagin sey: resmi kaydirmak

Ucuz yontem tum UV'yi tek bir derinlik ornegiyle oteler:

```glsl
vec2 offset = pointer * (depth - 0.5) * strength;   // YANLIS
```

Yakin ve uzak ayni kurala gore hareket eder. Hicbir sey hicbir seyin onune
gecmez; kart menteseye takilmis bir posterdir. **Okluzyon yoksa derinlik
yoktur.** CSS ile yapilan `translate` da aynen bu sinifa girer.

---

## 1. Yukseklik haritasi

`gen_depth.py` her gorsel icin 8-bit gri bir harita uretir (beyaz = yakin):

```bash
python3 gen_depth.py                  # public/assets/cards -> public/assets/depth
python3 gen_depth.py --check <id>     # kaynak | harita yan yana onizleme
```

Uc ipucu birlestirilir:

| Ipucu | Neden |
|---|---|
| **Detay enerjisi** | Yakin nesneler yuksek frekansli doku tasir; uzak, puslu ve duzdur. Ozne siluetini takip eden tek ipucu budur. |
| **Kompozisyon rampasi** | Kart sanati yakin ozneyi asagi, gokyuzunu yukari koyar. Zayif ama detayin kor noktasini (kalabalik gokyuzu) kapatir. |
| **Ton** | Hava perspektifi uzagi aciklastirir. En zayifi, gece sahnelerinde tersine doner, o yuzden en kucuk pay. |

**Toplama degil, ustune bindirme.** Rampa zemindir, detay o zeminin ustune
kalkan seydir:

```python
height = np.maximum(ramp, W_LIFT * detail + ramp * (1 - W_LIFT) * 0.5)
```

Toplarsan on plandaki dokusuz camur "uzak" cikar ve zemin geriye kacar.

**Kuantalama denedim, daha kotu.** Yukseklik alanini 5 duzleme oturtmak
makaslamayi yok etmez, gorunur bir kirilmaya cevirir: bir kurek sapi bant
sinirini gecerken bukulur. Alan **surekli ve bilerek yumusak** kalir
(`GaussianBlur(4.5)`), ucu uclari da iceri cekilir (`RANGE = 0.82`) — cunku
en buyuk kaymayi ve dolayisiyla en gorunur bozulmayi dagilimin ucu uretir.

---

## 2. Shader

Tam kaynak: `world-dominion/src/parallax-card.js` (`POM_VERTEX`,
`POM_FRAGMENT`). Iskelet:

```glsl
// Gorus vektoru duzlemin KENDI uzayinda olmali. Duzlem XY hizali oldugu icin
// object space = tangent space; TBN gerekmez, ama kamerayi tasimak gerekir.
vView = uCamObj - position;         // uCamObj CPU'da hesaplanir
```

```glsl
float depthAt(vec2 uv) { return 1.0 - texture2D(uDepth, uv).r; }

vec3 V = normalize(vView);
float steps = mix(44.0, 16.0, clamp(abs(V.z), 0.0, 1.0));  // sıyırma acisi daha cok adim ister
vec2 march = (V.xy / max(abs(V.z), 0.35)) * uScale / steps;

vec2 uv = baseUv; float rayDepth = 0.0; float surface = depthAt(uv);
for (int i = 0; i < MAX_STEPS; i++) {
  if (rayDepth >= surface) break;
  uv -= march; surface = depthAt(uv); rayDepth += 1.0 / steps;
}

// Sekant duzeltmesi: bu olmadan kesisim siluetı adim sayisina kuantalanir ve
// imlecle birlikte titrer.
vec2 prevUv = uv + march;
float after = surface - rayDepth;
float before = depthAt(prevUv) - rayDepth + 1.0 / steps;
uv = mix(uv, prevUv, clamp(after / (after - before), 0.0, 1.0));
```

Ustune iki sey daha — ikisi de "boyanmis" gorunumunu kaldirir:

- **Oz-golge:** carpma noktasindan isiga dogru yuru; yol uzerinde isinin
  ustune cikan her sey bu pikseli golgeler.
- **Specular:** yukseklik alaninin egimi normal yerine gecer, kalkik yerler
  isigi yakalar.

---

## 3. Uc tuzak (hepsi yasandi)

**sRGB kodlamasi.** Three, sRGB dokuyu ornekleyince lineere cevirir ve kendi
materyallerinin ciktisini geri kodlar — ama `ShaderMaterial`'in fragment
shader'ini oldugu gibi kullanir. Lineer degeri dogrudan yazarsan gorsel
kaynagin **%43'u** parlaklikta cikar. Sanat tercihi gibi durur; eksik transfer
fonksiyonudur.

```glsl
vec3 toSRGB(vec3 c) {
  return mix(c * 12.92, 1.055 * pow(max(c, vec3(0.0)), vec3(1.0/2.4)) - 0.055,
             step(vec3(0.0031308), c));
}
```

**Kenar sürünmesi.** Uzaga giden isin resmin disina cikar ve son pikseli
yayar. En kotu durumu kirpmayla karsilamak sanatin beste birini atmak demek.
Bunun yerine yer degistirmeyi kenara dogru sondur — **ama yurumeye degil,
sonuca uygula.** Yuruyusu olceklersen komsu pikseller ayni alanda farkli
mesafe yurur ve sonumleme bolgesi boydan boya yirtilir.

```glsl
uv = mix(baseUv, uv, edge);   // DOGRU
// float scale = uScale * edge;  // YANLIS — cizgi cizgi yirtar
```

**Bozulma butcesi.** `uScale * tilt` isinin katedebilecegi en uzun yoldur ve
bu bir **guc ayari degil, bozulma butcesidir**: yukseklik alani bir tahmin
oldugu icin her piksellik yol ayni zamanda potansiyel carpilmadir. Genisligin
**%7'sini** gecince nesneler makaslanmaya baslar, %12'de kurek sapi gorunur
sekilde bukulur. Olculmus tatli nokta: **~%5 yol, ~%3 ayrisma.**

Kalan gosterisi resmi bukerek degil, **kartin kendisini oynatarak** al: egim,
kalkma, imleci takip eden parlama.

---

## 4. Yazi bukulmesin

Tum karti `rotateX/rotateY` ile dondururssen baslik ve istatistikler de
perspektife girer; egik tipografi derinlik degil, render hatasi gibi okunur.

Donusu **yalniz sanat penceresine** ver:

```css
.card { perspective: 760px; transform: translateY(calc(var(--lift,0) * -6px)); }
.card__art { transform: rotateX(var(--rx)) rotateY(var(--ry)) scale(1.05); }
/* scale(1.05): donusun iceri cektigi koseler kart arkasini gostermesin */
```

---

## 5. DOM + WebGL melezi

Sayfa DOM ise her elemani WebGL'e cevirmeye gerek yok. Etki zaten sadece
isaret edilen elemanda yasiyor:

- Tek bir `WebGLRenderer` kartlar arasinda dolasir; ayni anda yalnizca imlecin
  ustundeki eleman canli.
- Cerceve ve metin DOM'da kalir — yazi keskin ve secilebilir kalir.
- Sanat penceresine bir `<canvas>` konur, `<img>` gizlenir; ikisi ayni
  dikdortgende oldugu icin gecis gorunmez.

Ornek: `world-dominion/src/card-parallax.js` (`acquire` / `aim` / `release`).

**Kanvas boyutunu her karede dogrula.** Ilk isaret olayindaki dikdortgen daha
oturmamis bir duzen olabilir: buyutulmus bir kart 2:1 olculup tabloyu ezik
render etti.

---

## 6. Dogrulama — goz yetmez, olc

Iki uc egimde birer kare al, sonra **bantlara ayirip yatay kaymayi olc**:

```python
# ust (uzak) / orta (ozne) / alt (on plan) icin capraz korelasyon
# 4x upsample: iki piksellik kayma tam sayi aramada kaybolur
```

Iki sey ararsin:

1. **Ayrisma monoton mu?** uzak > orta > yakin. Hepsi esitse okluzyon yok,
   sadece tum resmi kaydiriyorsundur — yukseklik dokusu yuklenmemis olabilir.
2. **Nesneler katı mı?** Kurek sapi, kutu kenari egriliyor mu? Egriliyorsa
   bozulma butcesini asmissindir.

Olcum tuzaklari:

- Kirpmaya **sabit cerceve kenarligini alma** — yuksek kontrastli sabit
  yapi korelasyonu sifira civiler, "hic hareket yok" dersin.
- Otomatik supurme calisiyorsa kapat; her tick imleci geri alir ve olctugun
  sey senin verdigin poz olmaz.
- Arama penceresini yeterince genis tut; doyuma ulasan korelasyon (`±maxs`)
  sahte bir tavan uretir.

---

## Iliskili

- Gorsel uretimi: [/image-prompt](../image-prompt/SKILL.md),
  [/image-run](../image-run/SKILL.md)
- Gizli panelde video kaydi: rAF olur, timer 1 Hz'e sikisir — MediaRecorder
  yerine deterministik kare dokumu + ffmpeg.
