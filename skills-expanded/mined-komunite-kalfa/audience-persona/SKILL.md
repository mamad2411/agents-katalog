---
description: Solopreneurler icin veri tabanli hedef kitle persona olusturma tarifi — arastirma kaynaklari, sablon ve dogrulama sureci
---

# Hedef Kitle Persona Tarifi

## Amac

Hayal gucuyle degil, gercek veriyle persona olustur. Solopreneurler icin pratik, 1-2 gunde tamamlanabilir, satisa dogrudan etki eden bir persona belgesi uret.

## Girdiler

### Zorunlu
- **Urun/Hizmet**: Ne satiyorsun
- **Mevcut Musteriler**: Var mi? Kac kisi? (yoksa rakip musterilerini arastir)

### Istege Bagli
- **Analytics Verisi**: Google Analytics, sosyal medya istatistikleri
- **Destek Kayitlari**: Musterilerin sordugu sorular

## KRITIK ANTI-PATTERN

**ASLA masabasinda persona uydurma.** "Ayse, 32, istanbul'da yasiyor, kahve sever" tarzinda hayali persona yazmak zarar verir. Her persona alani gercek veriye dayanmali. Verin yoksa Adim 1'deki kaynaklardan topla.

## Adim 1: Veri Toplama (5 Kaynak)

Her kaynak icin 30-45 dakika ayir. Toplam: yarim gun.

### Kaynak 1: Analytics Verisi
- Google Analytics > Kitle > Demografik bilgiler (yas, cinsiyet, konum)
- En cok ziyaret edilen sayfalar = en cok ilgi ceken konular
- Cihaz dagilimi (mobil vs desktop = is basinda mi evde mi)
- **Kayit sablon**: "Ziyaretcilerin %X'i [yas araligidir], %Y'si [cihaz] kullaniyor"

### Kaynak 2: Sosyal Medya Yorumlari
- Kendi hesaplarinin altindaki yorumlar
- Rakip hesaplarinin altindaki yorumlar (ozellikle sikayetler)
- Hashtag arastirmasi: sektorunle ilgili 5 hashtag'deki konusmalar
- **Kayit sablon**: "Insanlar [konu] hakkinda [duygu] hissediyor cunku [neden]"

### Kaynak 3: Rakip Yorumlari
- G2, Capterra, Trustpilot'ta rakiplerin 1-2 yildiz yorumlari (sikayetler = firsat)
- App Store / Google Play yorumlari (mobil urun varsa)
- Bes yildiz yorumlardaki ortak temalar (insanlar neye deger veriyor)
- **Kayit sablon**: "[Rakip] kullanicilari [ozellik]'ten memnun ama [eksik]'ten sikayet ediyor"

### Kaynak 4: Destek Talepleri ve SSS
- En cok sorulan 10 soru (varsa)
- Satin alma oncesi en cok sorulan itirazlar
- Yoksa: Rakiplerin SSS sayfalarini oku
- **Kayit sablon**: "Satin almadan once en cok [konu] hakkinda endise duyuyorlar"

### Kaynak 5: Reddit, Forum ve Topluluklar
- Reddit'te sektorunle ilgili 3-5 subreddit (Turkce icin: donanimhaber, technopat, eksi)
- Facebook gruplari (sektorune ozel)
- "Best [urun kategorin]" baslikli thread'ler = insanlar ne ariyor
- **Kayit sablon**: "Toplulukta en cok tartisilan konular: [1], [2], [3]"

## Adim 2: Persona Sablonu

Asagidaki her alani Adim 1'den topladigi veriyle doldur. Veri yoksa "BOS — dogrulama gerekli" yaz.

```markdown
# Persona: [Isim]

## Demografik
- **Ad**: [Gercekci bir Turkce isim]
- **Yas**: [Aralik degil spesifik: 34, "25-35" degil]
- **Meslek**: [Tam unvan: "3 yillik freelance UI designer", "kucuk e-ticaret isleten" gibi]
- **Gelir**: [Aylik net aralik: 25.000-40.000 TL]
- **Konum**: [Sehir veya calisme sekli: Istanbul, uzaktan calisiyor]
- **Aile Durumu**: [Evli/bekar, cocuk var mi — satin alma kararini etkiler]

## Psikolojik
- **Hedefler** (3 madde):
  1. [Is hedefi — ornek: "Aylik geliri 50.000 TL'ye cikarmak"]
  2. [Beceri hedefi — ornek: "Musterilere daha profesyonel gorunmek"]
  3. [Yasam hedefi — ornek: "Haftada 40 saatten fazla calismamak"]

- **Hayal Kirikliklari** (3 madde):
  1. [Gunluk problem — ornek: "Her gun 2 saat admin isiyle ugrasiyorum"]
  2. [Arac problemi — ornek: "Kullandigim arac cok karisik"]
  3. [Sonuc problemi — ornek: "Deadline kacirinca musteri kaybediyorum"]

- **Bilgi Kaynaklari**:
  - Podcast: [spesifik isimler]
  - YouTube kanallari: [spesifik isimler]
  - Newsletter: [spesifik isimler]
  - Sosyal medya: [hangi platform, kimi takip ediyor]

- **Satin Alma Tetikleyicileri**:
  1. [Olay — ornek: "Buyuk bir musteri kaybedince"]
  2. [Aciliyet — ornek: "Vergi doneminde fatura kaosundan bunalinca"]
  3. [Firsat — ornek: "Rakibinin basarili oldugunu gorunce"]

- **Itirazlar** (satin almama nedenleri):
  1. [Fiyat — ornek: "Ayda 29 dolar, TL'ye cevirince pahali"]
  2. [Zaman — ornek: "Yeni bir arac ogrenmeye vaktim yok"]
  3. [Guven — ornek: "Kucuk bir sirket, yarin kapanir mi?"]
  4. [Alternatif — ornek: "Excel'le idare ediyorum zaten"]
```

## Adim 3: Dogrulama — 5 Musteri Gorusmesi

Persona'yi gercek insanlarla dogrula. 5 gorusme yeterli — daha fazlasi gereksiz tekrar uretir.

### Gorusme Bulmak
- Mevcut musterilere mail at: "15 dakika gorusme karsiliginda 1 ay ucretsiz uzatma"
- Henuz musterin yoksa: Hedef kitlendeki 5 kisiye LinkedIn/Twitter'dan ulas
- Son care: Reddit/forum'da "arastirma icin gorusur musunuz" paylasimi

### Sorulacak 8 Soru (Bu Siralamayla)
1. "Isini tek cumleyle anlatir misin?"
2. "[Problem alani] konusunda en buyuk zorluk ne?"
3. "Bu sorunu cozmek icin simdi ne kullaniyorsun?"
4. "Kullandigin cozumde seni en cok ne rahatsiz ediyor?"
5. "Ideal cozum nasil gorunurdu?"
6. "Boyle bir araci satin almadan once neler seni duraksatir?"
7. "Bu konuda kimi takip ediyorsun, nereden bilgi aliyorsun?"
8. "Bu sorunu cozmek icin ayda ne kadar odemeye razı olurdun?"

### Gorusme Kurallari
- Acik uclu sor, evet/hayir sorma
- Asla kendi urununu pitchleme — dinle
- "Neden?" sorusunu en az 2 kez tekrarla (koke in)
- Not al: kelimesi kelimesine — kendi yorumunu yazma

## Adim 4: Persona'yi Kullanma

Persona bitince su belgelere referans ver:
- **Landing page copy**: Persona'nin kelimelerini kullan (PAS cercevesinde "agitate" bolumu)
- **Icerik plani**: Bilgi Kaynaklari alanina gore kanal sec
- **Fiyatlandirma**: Itirazlar ve gelir alanina gore fiyat belirle
- **Reklam hedefleme**: Demografik + ilgi alanlari dogrudan Facebook/Google Ads'e gider

## Kalite Kontrol

- [ ] Her alan gercek veriye dayaniyor (hayal degil)
- [ ] En az 3 farkli kaynaktan veri toplanmis
- [ ] Itirazlar spesifik (genel "pahali" degil, "ayda 29 dolar TL'ye cevirince pahali")
- [ ] Hedefler olculebilir ("daha iyi" degil, "ayda 50.000 TL")
- [ ] 5 gorusme yapildi veya planlandı

## Ornek Cikti

**Urun**: TaskFlow — Freelancer'lar icin proje yonetim araci ($29/ay)

---

# Persona: Deniz Acar

## Demografik
- **Ad**: Deniz Acar
- **Yas**: 31
- **Meslek**: 4 yillik freelance UI/UX designer, ayni anda 5-8 musteri yonetiyor
- **Gelir**: Aylik net 28.000-45.000 TL (proje bazli, dalgali)
- **Konum**: Ankara, evden calisiyor
- **Aile Durumu**: Bekar, kedi sahibi

## Psikolojik
- **Hedefler**:
  1. Aylik geliri 60.000 TL'ye stabilize etmek
  2. "Tasarimci" degil "design consultant" olarak konumlanmak
  3. Haftada max 35 saat calismak — burnout yasadi, tekrar istemez

- **Hayal Kirikliklari**:
  1. Her gun 1.5 saat admin isi: fatura, takip maili, dosya duzenleme
  2. Notion + Excel + WhatsApp uc farkli yerde proje takibi — surekli bir seyler kayiyor
  3. Gecen ay 2 deadline kacirdi, biri musteri kaybina yol acti

- **Bilgi Kaynaklari**:
  - YouTube: The Futur, Turkce icin Kodluyoruz ve Pratikte Design kanallari
  - Twitter: urun tasarimcilari, indie hacker'lar
  - Newsletter: Dense Discovery, Sidebar.io
  - Topluluk: Freelance Designers Turkey (Facebook), r/freelance

- **Satin Alma Tetikleyicileri**:
  1. Buyuk bir deadline kacirip musteri kaybedince
  2. Yeni yil basinda "bu yil organize olacagim" karariyla
  3. Bir freelancer arkadasinin basarili sistemi gordugunde

- **Itirazlar**:
  1. "29 dolar ayda 900+ TL eder, Notion ucretsiz"
  2. "Yeni bir araci ogrenecek zamanim yok, islerim yogun"
  3. "Kucuk startup — 2 yil sonra kapanirsa verim ne olur?"
  4. "Notion + Google Calendar ile idare ediyorum aslinda"
