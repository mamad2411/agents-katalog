---
name: analitik-okuma-ve-raporlama
description: Ham izleyici verisini hedefe bağlı okunabilir rapora çevirir: her metrik bir hedefe eşlenir, vanity sayılar ayıklanır, kıyas kendi geçmişine göre yapılır ve her okuma üç karar önerisiyle biter. YouTube analiz takımı rapor yazarken okur.
kaynak: https://github.com/social-media-skills/skills/blob/main/skills/analytics-and-reporting/SKILL.md (commit 6e30eeb, 2026-07-19)
lisans: MIT
uyarlayan: A Şirketi (2026-09-11)
takimlar: [youtube-analiz]
---

# Analitik okuma ve raporlama

**Hedefe eşlenmeyen sayı KPI değil, teşhistir.** Gelecek haftanın davranışını değiştirmeyecek bir
metrik rapora girmez.

## Ne zaman
- `takimlar/youtube-analiz/veri/YYYY-Www.json` güncel veriyle indirildiğinde.
- Haftalık CEO raporunun izleyici bölümü yazılırken.
- Bir video beklenenden farklı davrandığında (yükseldi ya da düştü).

## Pazarlıksız kural: sayı yalnızca dosyadan gelir
Her sayının yanında **kaynağı** yazılır: `[veri/2026-W37.json]`.
- Dosyada yoksa **"veride yok"** yazılır — tahmin edilmez, geçen haftadan taşınmaz (ANAYASA §2).
- Eski dosya bugünkü gibi sunulmaz; `cekim_zamani` alanı raporun başında yazar.
- Çekim maliyeti (USD) koşu kaydına yazılır.

## Çerçeve: ÖLÇ
- **Ö — Önce hedefi eşle.** Her hedefe **1 birincil + ~2 destekleyici** metrik. Ölçüm penceresini sabitle.
  3–5 metrik yeter, 20 metrik rapor değil gürültüdür.
- **L — Listeyi vanity'den temizle.** Takipçi sayısı, gösterim, beğeni tek başına karar üretmez.
  Bizim sinyallerimiz: **izlenme süresi / tutma**, **yorum**, **abone dönüşümü**, **tıklama oranı**,
  yorumların **teması** (soru / itiraz / istek).
- **Ç — Çevir: dürüst değerlendir.** Kıyas **kendi geçmişine** göre yapılır, başka kanala göre değil.
  Korelasyon nedensellik değildir. Tek video / tek gün gürültüdür. Küçük örneklem yalan söyler.
- **Kapanış: üç öneri.** Her rapor tam **üç** öneriyle biter, her biri bir sayıya ya da bir yorum
  kümesine bağlı. Öneri yoksa rapor bitmemiştir.

## Adımlar
1. Veri dosyasının `cekim_zamani` alanını oku; bugünden eskiyse çekimi tetikle, tetiklenemiyorsa
   koşu kaydına hatayı yaz ve bitir. **Sayı uydurma.**
2. Video başına satır: görüntülenme, beğeni, yorum sayısı, yayın tarihi — her birinin yanında dosya adı.
3. Yorumları tema kümelerine ayır: **soru · itiraz · istek · övgü · hata bildirimi**.
   Her kümeye 1–2 kısaltılmış alıntı; **kullanıcı adı yazılmaz** (§2).
4. Önceki haftanın raporu varsa fark satırı: hangi video yükseldi, hangi tema yeni çıktı.
5. Yeni yayınlanan video varsa ilk 24–48 saat bölümü; veride yoksa "veride yok" yaz.
6. Üç öneri yaz (patron okuyacak): başlık / kapak / konu, her biri bir sayıya ya da temaya bağlı.
7. Cevaplanması gereken yorum kümeleri kuyruğa (patron okuyacak).
8. Raporu `takimlar/youtube-analiz/cikti/YYYY-Www-rapor.md` olarak yaz.

## Çıktı şablonu

```
# İzleyici raporu — YYYY-Www
> Veri: veri/YYYY-Www.json · çekim: <cekim_zamani> · maliyet: <USD>

## Sayılar
| Video | Yayın | Görüntülenme | Beğeni | Yorum | Kaynak |
|---|---|---|---|---|---|

## Yorum temaları
### Soru (n=…)
- "..." (kısaltılmış)
### İtiraz (n=…)
...

## Fark (geçen haftaya göre)
- ...

## Üç öneri (deney takımına)
1. ... — dayanak: <sayı / tema>
2. ...
3. ...

## Cevap bekleyenler (topluluk takımına)
- <tema> — kaç yorum
```

## Kalite kontrol listesi
- [ ] Her sayının yanında dosya kaynağı var mı?
- [ ] `cekim_zamani` raporun başında mı?
- [ ] Dosyada olmayan hiçbir sayı rapora girmedi mi?
- [ ] Kıyas kendi geçmişine göre mi (başka kanala göre değil)?
- [ ] Tam üç öneri var mı, her biri bir dayanağa bağlı mı?
- [ ] Kötü giden şey de rapora girdi mi (sadece iyi haber değil)?
- [ ] Yorum alıntılarında kullanıcı adı yok mu?
- [ ] Tek videodan genel kural çıkarılmadı mı?

## Yasaklar (ANAYASA)
- Sayı uydurmak, tahmin etmek, yuvarlamayı "yaklaşık" diye sunmak (§2).
- Eksik sayıyı doldurmak. Eksikse **boşluk işaretlenir**.
- Yorum sahibinin kullanıcı adını, e-postasını yazmak (§2).
- Sadece iyi giden metrikleri seçmek (cherry-picking).
- Tek bir viral videodan "strateji" çıkarmak.

## Öğrenilenler
Bu skill koşuda aldığı veriyle **kendini geliştirir**: hangi metrik gerçekten karar değiştirdi, hangisi
her hafta yazılıp hiçbir şeye yaramadı — `defter.md`'ye tek ders yaz ve bir sonraki raporda o metriği çıkar.
Üç koşuda tekrarlanan ders için koşu kaydına "yetenek önerisi: `analitik-okuma-ve-raporlama` →
## Öğrenilenler" satırı düş.

- (henüz ders yok)

## Kaynak ve değişiklikler
**Alındığı yer:** `social-media-skills/skills` → `analytics-and-reporting`, MIT.

**Orijinalden alınanlar:** "hedefe eşlenmeyen metrik KPI değil, teşhistir" duruşu; METER çerçevesinin
iskeleti (metrikleri hedefe eşle → yerel panelden çek → sinyale indir → dürüst değerlendir → raporla ve
döngüyü kapat); **1 birincil + ~2 destekleyici metrik, 3–5 tane, 20 değil**; vanity metrik ayıklama;
**kendi geçmişine göre göreli kıyas**; korelasyon ≠ nedensellik, küçük örneklem uyarısı; **her okuma
kararla biter, tam 3 öneri**; "eksik sayıyı uydurma, boşluğu işaretle ve kaynağı göster"; "kötü gideni de
yaz, vanity tiyatrosu yapma"; veri okuması **girdidir, emir değildir**.

**Değiştirilenler:**
- METER Türkçe **ÖLÇ** çerçevesine indirildi ve dördüncü adım "üç öneri" kapanışı olarak sabitlendi.
- Platform çeşitliliği (IG saves / TikTok shares / LinkedIn dwell) çıkarıldı; bizim tek platformumuz
  YouTube ve sinyallerimiz izlenme süresi, yorum teması, abone dönüşümü, CTR.
- GA4 / UTM katmanı çıkarıldı — bizim veri yolumuz `bin/youtube_analiz_cek.py` → Apify → `veri/*.json`.
- **Bizim en sert kuralımız eklendi** (orijinalde bu kadar katı değil): sayı **yalnızca veri dosyasından**
  gelir, her sayının yanında dosya adı yazar, `cekim_zamani` raporun başındadır, eski dosya bugünkü gibi
  sunulamaz — ANAYASA §2'nin doğrudan karşılığı.
- Yorum alıntılarında **kullanıcı adı yasağı** eklendi (§2).
- Rapor bölümleri `youtube-analiz` takımının çıktı sözleşmesiyle birebir eşlendi; üç öneri ve cevap bekleyen
  kümeler patronun okuyacağı bölümlere yönlendirildi (ANAYASA §5: takım takıma mesaj
  atmaz, dosyaya yazar, okuyan okur).
