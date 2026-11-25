---
name: funscore
description: "Bir oyun prototipinin EGLENCELI olup olmadigini 100 uzerinden puanlar. Denge degil his olcer. Bot skoru otomatik, insan hissiyat testi ayri iz. Triggers: funscore, eglence puani, eglenceli mi, fun score, oyun zevkli mi, playtest puani."
user-invocable: true
argument-hint: "[bot|insan|rapor] — bos birakilirsa bot skoru"
---

# /funscore — "Bu oyun eglenceli mi" sorusunu olculebilir yap

Denge assertion'lari **adaleti** olcer: kazanma oranlari bantta mi, yollar esit mi,
imkansiz durum var mi. Hicbiri **eglenceyi** olcmez. Dengeli bir oyun sikici olabilir
ve genelde oyle olur — cunku dengelemek sayi cevirmektir, eglence ise his.

Bu skill iki AYRI 100'luk skor uretir:

| Iz | Ne olcer | Ne zaman |
|---|---|---|
| **Bot skoru** | Yapisal his proxy'leri — otomatik, tekrarlanabilir | her build |
| **Insan skoru** | Hissiyat — bot'un asla goremeyecegi | surum kilometre taslarinda |

Ikisi **toplanmaz**. Bot skoru "yapisi saglam mi", insan skoru "keyifli mi" der.
Bot 90 alip insan 30 alabilir; bu bir celiski degil, en yaygin sonuctur.

---

## Arastirma temeli

Bu skill uc kaynaktan turetildi, hepsi olculebilir iddia iceriyor:

- **Slay the Spire ekibi** (~90 grafik): en kritik ikisi *kart secilme orani* ve
  *kazanan destelerde gorulme*. Ama kendi sozleri: *"Sayilar bize nasil HISSETTIRDIGINI
  soylemiyor."* Sabit esik yayinlamamislar.
- **Roguebook postmortem**: oyuncular *"nasil kaybettigini anlamadiysa ve bir dahakine
  ne yapacagini bilmiyorsa"* birakir. Cozum: aldigi risk uzerinde kontrol.
- **Costikyan**: anlamli secim = sonuclarinin **cogunu** gorebilmek ama **hepsini** degil.
  Cok az secenek monotonluk, cok fazla secenek felc.

---

## Faz 1 — Bot skoru (100 puan)

Dort boyut. D3 (kayip okunabilirligi) bilerek **yok** — bot bunu olcemez, olcuyormus
gibi yapmak yalancı yesildir.

| Boyut | Puan | Alt metrikler |
|---|---:|---|
| **D1 Karar yogunlugu** | 30 | secim **sonuc** ayrismasi (20) · hakim secenek yok (10) |
| **D2 Motor kimligi** | 30 | ivme orani (20) · ayni-build kart ortusmesi (10) |
| **D4 Gerilim** | 25 | kararsiz tur orani (10) · dar marjla kazanma (15) |
| **D5 Cesitlilik** | 15 | kazanan strateji cesidi (7) · acilis ortusmesi (8) |

### Metriklerin tanimi

**Secim sonuc ayrismasi.** Ayni seed'de her secenegi ZORLA oynat, kosuyu bitir,
sonuclari karsilastir. Fark yoksa secim kozmetiktir.
*Bunu botun tercihinden olcme* — bot'un skorlama fonksiyonu kendi onyargisini olcer,
oyunun karar alanini degil. Ucunu de oynat.

**Hakim secenek yok.** Secenekler arasi kazanma orani yayilimi. Ayrisma yuksek ama
bir secenek hep daha iyiyse, secim *onemli* ama *dogru cevabi var* — ilk birkac
kosudan sonra karar oluyor.

**Ivme orani.** Son ceyrek / ilk ceyrek, birim zamandaki ilerleme. Deckbuilder'in
cekirdek hazzi "kurdugum makine donmeye basladi"dir. Dusukse motor hissi yok;
cok yuksekse erken oyun anlamsiz.

**Kararsiz tur.** Oyuncunun tek oynanabilir hamlesi oldugu veya hicbir eylemin ise
yaramadigi turlar. Karar yoksa tur oludur — ekranda hareket olsa bile.

**Dar marjla kazanma.** Kazanilan kosularin ne kadari kil payi bitti. Cok dusukse
kazanmak rahat, gerilim yok. Cok yuksekse yipratici.

### Puanlama kurali

**Bant ici DOGRUSAL, kademeli degil.** 0/0.5/1.0 uc kademe iterasyon yonunu gizler:
belirgin iyilesme skoru hic oynatmayabilir. Skorun asil isi *yonu* gostermek.

### Esikler

Esikler oyuna gore ayarlanir ama **her esik kaynak etiketi tasir**: `arastirma`,
`mantik`, `tahmin`. Tahminse tahmin yaz. Ilk playtest'te bant kaydirilabilir ama
**kaydirma kayda gecer** — sessizce gevsetilen esik fail-closed ihlalidir.

---

## Faz 2 — Insan skoru (ayri 100 puan)

Bot'un **asla** cevaplayamayacagi uc soru:

1. **Ajans** — "Kazandiginda sen mi kazandin, deste mi kazandi?"
2. **Fantezi** — tema mekanikten *hissediliyor* mu, yoksa bu bir spreadsheet mi?
3. **Sikilma ani** — oyuncunun telefonuna baktigi ilk an hangi sistemde geldi?

### Minimum test

**7 oyuncu** (5 oruntu esigi + 2 fire), en az 3'u turu bilen, en az 2'si bilmeyen.
Oyuncu basina **2 zorunlu kosu** (ogrenme + bilgili) + **sinirsiz serbest sure**.
Tekrar cekimi serbest surede olculur, sorarak degil **gozleyerek**.

| Boyut | Puan | Soru |
|---|---:|---|
| Kayip okunabilirligi | 30 | "Neden kaybettin, sonraki sefer ne yapardin?" — spesifik + dogru |
| Tekrar cekimi | 25 | Gozlem: zorunlu kosular bitince kendiliginden yeni kosu |
| Karar gerekcesi | 20 | "Neden o secimi yaptin?" — gerekce verebiliyor mu |
| Kimlik | 15 | "Ne kurdun, tek cumle" — spesifik mi genel mi |
| Gerilim | 10 | "En gergin an neydi?" — an gosterebiliyor mu |

### Anlama kapisi (puanlanmaz, gecilmesi zorunlu)

Tutorial suresi, ilk combo'yu gorme suresi, temel kavram sorusu.
**Kapi duserse insan skoru hesaplanmaz** — anlasilmayan oyunun eglence olcumu gurultudur.

---

## Faz 3 — Yalanci sinyaller

Her boyut icin "bu metrik yesil ama oyun kotu" senaryosu yaz. Ornekler:

- **Ayrisma yuksek ama secenekler esit derecede sikici** — Costikyan'in monotonlugu.
  EV esitligi ikilem degil kayitsizlik olabilir.
- **Sayisal ayrisma var ama oyuncunun GORMEDIGI arka plan sayilarinda.**
  Ekranda her sey ayni gorunuyorsa kimlik sifir, metrik yesil.
- **Dar marj yuksek ama hep ayni mekanizmadan.** "Yine kira turu" gerilimi
  3. kosuda rutine doner.
- **Acilis cesitliligi yuksek ama "hangisi olsa olur" kayitsizligindan.**
  Dusuk ortusme merakin da umursamazligin da imzasidir.
- **Genel:** bot optimal oynar, insanlar oynamaz. Botun "kararsiz tur %2"si,
  kurallari ogrenen insan icin %30 olabilir.

---

## Faz 4 — Kirmizi cizgi

Iki kosullu, ikisi de somut. **Tek metrik asla iptal ettirmez.**

1. **Anlik:** kendiliginden yeni kosu <%30 **VE** kaybini aciklama <%40, ayni testte.
   Bu, Roguebook'un tarif ettigi birakma dongusudur.
2. **Iterasyon:** bir playtest + bir duzeltme turundan sonra **ikinci kez** bot skoru
   <40/100 ve dusus karar yogunlugu + kayip okunabilirliginden geliyorsa.

Gerekce: gerilim ve cesitlilik ayar isidir. Iki iterasyonda duzelmeyen karar
yogunlugu yapisal kusurdur — sayi cevirerek degil cekirdek dongu degistirerek
duzelir, o da artik ayni prototip degildir.

---

## Kalibrasyon

Mutlak skor referanssiz okunamaz. 55/100 "kotu" mu, tur icin normal mi?
**Ayni rubrigi bilinen-iyi bir oyunda calistir** ve skoru yalnizca *fark* olarak oku.
Kalibrasyon yoksa skoru iterasyonlar arasi **yon** icin kullan, mutlak yargi icin degil.

---

## Yapma

- **Bot skorunu optimize etme.** Bot metrikleri proxy'dir; onlari yesillendirmek
  eglenceyi degil proxy'yi iyilestirir. Goodhart yasasi.
- **D3'u bota olcturme.** Kayip okunabilirligi oyuncunun kafasinda olur, log'da degil.
  "Bot 4 hamlede kurtarabilirdi" teknik okunabilirliktir, insani degil.
- **Iki skoru toplama.** Ayri sorular, ayri cevaplar.
- **Esigi sessizce gevsetme.** Kaydiracaksan kaydirdigini yaz.
- **Tek kosuda karar verme.** Skor yon icindir; tek olcum gurultudur.
