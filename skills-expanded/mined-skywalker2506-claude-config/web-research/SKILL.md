---
name: web-research
description: Web arastirmasi — rakip, kullanici yorumlari, pazar trendleri, UX, monetizasyon. Odak parametrik.
argument-hint: "[odak konusu] — competitors, ux, trends, monetization, reviews, ai, growth, pedagogy, accessibility, localization"
---

## Ne yapar

Arka plan agent ile **web arastirmasi** yapar. Projenin alanindaki rakipleri, kullanici ihtiyaclarini, yorumlari ve trendleri arastirip detayli rapor doner.

**Odak verilirse** o perspektiften bakar. **Verilmezse** genel arastirma.

## Arguman

| Input | Davranis |
|-------|----------|
| `/web-research` | Genel pazar arastirmasi |
| `/web-research competitors` | Rakip analizi |
| `/web-research ux` | UX pattern'lari, onboarding, gamification |
| `/web-research trends` | Pazar trendleri |
| `/web-research monetization` | Monetizasyon stratejileri |
| `/web-research reviews` | Kullanici yorumlari (App Store, Reddit) |
| `/web-research ai` | AI/LLM entegrasyonu |
| `/web-research growth` | ASO, viral loop, retention |
| `/web-research pedagogy` | Ogrenme bilimi, SRS |
| `/web-research accessibility` | WCAG, a11y |
| `/web-research localization` | Coklu dil, RTL |
| Herhangi bir konu | O konu odakli arastirma |

## Çalıştırma

**Model:** Opus Max — arka plan agent.

**Tek tur:** Döngü değil, tek seferlik derinlemesine araştırma.

Ana oturum şu agent'ı başlatır:

```python
Agent(
  prompt=<aşağıdaki şablon>,
  model="opus",
  run_in_background=True,
  description="web-research"
)
```

### Agent prompt şablonu

```
Sen bir pazar arastirma uzmanisin. Mevcut projenin alanini ve ekosistemini arastir.

Proje bilgisi icin projenin CLAUDE.md dosyasini oku — proje adi, alani, mevcut ozellikler oradan alinir.

ODAK: [varsa kullanicinin verdigi odak, yoksa "Genel pazar arastirmasi"]

## ADIMLAR

### 1. RAKIP ANALIZI (WebSearch + WebFetch)
Projenin alanindaki basica rakipleri bul ve arastir.

Her biri icin:
- One cikan ozellikler
- Kullanici sayisi/rating
- Monetizasyon modeli
- Projede olmayan farkli ozellikleri

### 2. KULLANICI YORUMLARI (WebSearch)
Arama terimleri:
- "[proje alani] app review 2025/2026"
- "best [proje alani] app reddit"
- "[rakip1] vs [rakip2] vs [rakip3]"
- "[proje alani] app complaints"
- "[proje alani] app feature request"

Topla:
- En sik sikayet edilen sorunlar
- En cok istenen ozellikler
- Kullanicilari mutlu eden seyler
- Retention/churn sebepleri

### 3. PAZAR TRENDLERİ (WebSearch)
- Language learning market size & growth
- Mobile education app trends
- AI in language learning
- Gamification trends
- Subscription vs one-time purchase trends

### 4. UX BEST PRACTICE (WebSearch)
- Onboarding best practices (education apps)
- Gamification patterns that work
- Retention strategies
- Feedback collection UX
- Tutorial/coach marks patterns

### 5. PROJE ICIN FIRSATLAR
Arastirma bulgularini projeye uygula:
- Rakiplerden ogrenilecekler
- Kullanici ihtiyaclarindan cikan feature gap'ler
- Quick wins (düşük efor, yüksek etki)
- Stratejik yatırımlar (yüksek efor, yüksek etki)

### 6. RAPOR YAZ

## Rakip Analizi Özeti
| Uygulama | Rating | Kullanici | Monetizasyon | Projede Olmayan |
(tablo)

## Kullanıcı İçgörüleri
- En sık şikayetler (top 5)
- En çok istenen özellikler (top 5)
- Retention faktörleri

## Pazar Trendleri
- Öne çıkan trendler
- Proje icin firsatlar

## UX Önerileri
- Onboarding
- Gamification
- Retention

## Task Önerileri
| # | Başlık | Açıklama | Öncelik | Efor | Kaynak |
(tablo — kaynak: hangi rakip/trend/kullanıcı ihtiyacından çıktı)

## Öncelik Sırası
1. Quick win — sebep
2. Stratejik — sebep
...

## KURALLAR
- WebSearch ve WebFetch kullan — güncel bilgi topla
- Somut, actionable öneriler sun
- Her öneri için kaynak belirt (hangi rakip, trend, kullanıcı yorumu)
- Task formatında öner (başlık, açıklama, öncelik, efor)
- Kod yazma, dosya düzenleme YAPMA
- Raporu Türkçe yaz
- Max 30 tool call
```

## Çıktı

Agent tamamlandığında rapor döner. Ana oturum:

1. Raporu kullanıcıya gösterir
2. Task önerileri varsa **3 seçenek** sunar:

```
Ne yapalım?
  1) Sprint dosyasına task olarak ekle (onaylananları `forge/sprints/`e yazar)
  2) Kenara not al (docs/tavsiyeler.md'ye ekler, sprint dosyasına dokunmaz)
  3) Hiçbir şey yapma (sadece rapor bilgi amaçlı)
```

- **Secenek 1:** onaylanan onerileri sprint dosyasina `todo` statusuyle ekler
- **Secenek 2:** Onerileri `docs/tavsiyeler.md`'ye tarih ve kaynak ile ekler
- **Secenek 3:** Hicbir islem yapmaz, rapor bilgi amaclidir

## When NOT to Use
- Tek satirlik basit soru/cevap ise
- Skill'in scope'u disindaysa
- Riskli/destructive is ise (ayri onay gerekir)

## Red Flags
- Belirsiz hedef/kabul kriteri
- Gerekli dosya/izin/secret eksik
- Ayni adim 2+ kez tekrarlandi

## Error Handling
- Gerekli kaynak yoksa → dur, blocker'i raporla
- Komut/akıs hatasi → en yakin guvenli noktadan devam et
- 3 basarisiz deneme → daha uygun skill/agent'a yonlendir

## Verification
- [ ] Beklenen cikti uretildi
- [ ] Yan etki yok (dosya/ayar)
- [ ] Gerekli log/rapor paylasildi
