---
name: anlati-kurgusu
description: Bir işin içindeki gerçek hikâyeyi bulur ve yayı kurar: kurulum/sorun → dönüm noktası → ödül; okuyucuyu kahraman, anlatıcıyı rehber yapar, soyut cümle yerine tek somut ayrıntıya bağlar ve hikâye uydurmayı yasaklar. Twitter içerik takımı article yazarken, video içerik takımı omurga kurarken okur.
kaynak: https://github.com/social-media-skills/skills/blob/main/skills/storytelling-and-narrative/SKILL.md (commit 6e30eeb, 2026-07-19)
lisans: MIT
uyarlayan: A Şirketi (2026-09-11)
takimlar: [twitter-icerik]
---

# Anlatı kurgusu

İnsanlar bilgiyi değil **duyguyu ve anlamı** paylaşır. Ama 2026'nın anlatısı uzun bir nutuk değil:
**sıkı bir mikro yay**, **tanıdık bir kahraman** ve **somut ayrıntı**.

Bu bir **zanaat katmanıdır**: yayı kurar, sonra format yazarlarına (`zincir-yazimi`,
`kaydirmali-post-yazimi`, `youtube-uzun-video-omurgasi`) devreder.

## Ne zaman
- Gece article paketinin gövdesi yazılırken (1.200–2.000 kelime, tablo yok).
- Bir videonun omurgasında "neden bunu yaptım" bölümü kurulurken.
- Bir kararın (neden şu aracı bıraktık) arkasındaki hikâye anlatılacağında.

## Çerçeve: YAY
- **Y — Yalnızca gerçek hikâye.** İnsani gerilimi bul: dönüşüm, çatışma, bedel.
  **Her iş hikâye değildir** — hikâye yoksa zorlama, bilgi olarak yaz. **Hikâye asla uydurulmaz.**
- **A — Arkı kur.** Kurulum/sorun → dönüm noktası → ödül. **Okuyucu kahraman, anlatıcı rehberdir.**
  Kanalın dili zaten bu: "ben kurdum, sen de kurabilirsin" — "bakın benim dosyam" değil.
- **Y — Yere bas (somutluk).** Somut duyusal ayrıntı inandırıcılığı yapar: göster, anlatma.
  **Bir gerçek ayrıntı on genellemeyi yener.** "Üç gün kaybettim" değil de "Perşembe akşamı
  CapCut projeyi açmayı reddetti, 512 parçayı elle yeniden kurdum" — ikincisi hikâyedir.

Üstüne iki kural:
- **Tek duygusal hedef.** Rahatlama mı, gurur mu, aidiyet mi, öfke mi? Bir tane seç.
  Okuyucunun **kendini gördüğü** bir nokta bırak.
- **Formata sıkıştır.** Yayı formatın uzunluğuna indir, sonra format yazarına devret.
  Açılış `kanca-yazimi`'nin işidir.

## Adımlar
1. **Malzemeyi topla.** Önceki koşu kayıtları (`takimlar/*/kosu/*.md`), çıktılar (`cikti/`) ve
   `defter.md` dersleri — hepsi salt okunur. Hikâye buradan **çıkarılır**, uydurulmaz.
2. **Gerilimi bul.** "Ne beklendi, ne oldu?" Fark yoksa hikâye yoktur.
3. **Yayı yaz.** Üç beat, her biri tek cümle: kurulum/sorun, dönüm noktası, ödül.
4. **Rolleri ata.** Kahraman kim (okuyucu / patron / takım), rehber kim, engel ne.
5. **Somut ayrıntıları seç.** En az üç: bir dosya adı, bir hata mesajı, bir saat, bir sayı (✅).
   Genelleme cümlelerini bunlarla değiştir.
6. **Duygusal hedefi ve "kendini gördüğü nokta"yı yaz.**
7. **Dürüstlük geçişi.** Olmamış bir şey yazıldı mı? Sıralama gerçeğe uyuyor mu?
   Başarısızlık gizlendi mi? Gizlendiyse geri koy — kanalın en güçlü anları dürüstlük anlarıdır.
8. **Devret.** Yayı formata sıkıştır ve format skill'ine ver.

## Çıktı şablonu

```
## Anlatı yayı — <konu>

- Gerilim: beklenen <...> / olan <...>
- Kahraman: <okuyucu / patron> · Rehber: <...> · Engel: <...>
- Duygusal hedef: <tek kelime>

| Beat | Tek cümle | Somut ayrıntı |
|---|---|---|
| Kurulum / sorun | ... | <dosya, saat, hata mesajı> |
| Dönüm noktası | ... | ... |
| Ödül | ... | ... |

- Okuyucunun kendini gördüğü nokta: ...
- Dürüstlük anı (varsa): ...
- Devredildiği format: `zincir-yazimi` / article gövdesi
```

## Kalite kontrol listesi
- [ ] Hikâye **gerçek** mi, kaynağı (koşu kaydı / çıktı dosyası) yazılı mı?
- [ ] Gerilim var mı (beklenen ≠ olan)?
- [ ] Üç beat de tek cümleye iniyor mu?
- [ ] En az üç somut ayrıntı var mı, genelleme cümleleri değiştirildi mi?
- [ ] Kahraman okuyucu mu, yoksa anlatıcının kendini övdüğü bir metin mi oldu?
- [ ] Tek duygusal hedef mi?
- [ ] Dürüstlük geçişi yapıldı mı, başarısızlık gizlendi mi?
- [ ] Her sayı ✅ etiketli mi?

## Yasaklar (ANAYASA)
- **Hikâye uydurmak.** Olmamış bir an, verilmemiş bir tepki, yaşanmamış bir sorun yazılmaz.
  Kaynaksız iddia yazılmaz (§2).
- Kullanıcı/yorum sahibi adı, e-posta, özel konuşma (§2).
- "Bakın benim dosyam" tonu — kanalın reddettiği ton. Kahraman okuyucudur.
- Her işi hikâyeye çevirmek. Hikâye yoksa bilgi olarak yazılır.
- Yayınlamak (§1).

## Öğrenilenler
Bu skill koşuda aldığı veriyle **kendini geliştirir**: hangi yay tuttu, hangi somut ayrıntı en çok
alıntılandı — `defter.md`'ye tek ders yaz. Üç koşuda tekrarlanan ders için koşu kaydına
"yetenek önerisi: `anlati-kurgusu` → ## Öğrenilenler" satırı düş.

- (henüz ders yok)

## Kaynak ve değişiklikler
**Alındığı yer:** `social-media-skills/skills` → `storytelling-and-narrative`, MIT.

**Orijinalden alınanlar:** "insanlar bilgiyi değil duygu ve anlamı paylaşır" duruşu; BEATS çerçevesinin
üç taşıyıcı adımı (gerçek hikâyeyi bul → yayı kur → somutluğa bağla) ve iki kuralı (tek duygusal hedef,
formata sıkıştır); **kurulum/sorun → dönüm noktası → ödül** yayı; **kitle kahraman, marka rehber**
(StoryBrand) yerleşimi; "bir gerçek ayrıntı on genellemeyi yener" (göster, anlatma); **her post hikâye
değildir**; bunun bir **zanaat katmanı** olduğu ve format mekaniğinin format yazarlarına devredildiği;
**hikâye/referans asla uydurulmaz**, özgünlük cilaya yeğdir; açılışın `hook-writer`'a devredilmesi.

**Değiştirilenler:**
- İstatistikler (stories ~22× daha akılda kalır, %62 daha fazla kaydetme vb.) **çıkarıldı** —
  ANAYASA §2 doğrulanmamış üçüncü taraf sayısını yasaklıyor; bu sayıların birincil kaynağı açılmadı.
- Platform çerçeveleme tablosu (TikTok/LinkedIn/IG/YT) çıkarıldı; bizim iki hedefimiz var:
  X article gövdesi ve video omurgası.
- WoopSocial yayın zinciri ve "serileştirilmiş yay content-calendar'a düşer" katmanı çıkarıldı (§1).
- **Malzeme kaynağı repoya bağlandı** (orijinalde yok): hikâye koşu
  kayıtları, `cikti/` dosyaları ve `defter.md` derslerinden **çıkarılır** — böylece "uydurma" yasağı somut bir kaynak
  zorunluluğuna dönüştü.
- **"Bakın benim dosyam" tonu yasağı** eklendi — kanalın kendi reddettiği ton; kahraman okuyucudur.
- **Dürüstlük geçişi** adımı eklendi: başarısızlık gizlenmişse geri konur (kanalın "dürüstlük anı" deseni).
