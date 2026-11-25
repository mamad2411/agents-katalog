---
name: icerik-denetimi
description: Yayınlanmış içeriğin geriye dönük sağlık kontrolü: ne tuttu, ne tutmadı, hangi konu başlığı aç kaldı, hangi söz verilip tutulmadı — ve her kalem için tut / bırak / tazele kararı. YouTube analiz takımı periyodik denetimde, CEO raporu çeyrek bakışında okur.
kaynak: https://github.com/social-media-skills/skills/blob/main/skills/content-audit/SKILL.md (commit 6e30eeb, 2026-07-19)
lisans: MIT
uyarlayan: A Şirketi (2026-09-11)
takimlar: [youtube-analiz]
---

# İçerik denetimi

**Yoğunluk ilerleme değildir.** Her hafta video çıkıyor, sayılar kıpırdıyor, ama hiçbir şey birikmiyor
olabilir. Denetim, yoğunluğun altındaki **sinyali** bulur.

## Ne zaman
- Ayda bir hafif, üç ayda bir derin.
- Büyük bir değişiklikten sonra (yeni seri, format değişikliği, yeni sponsor ilişkisi).
- "Neye ağırlık verelim?" sorusu geldiğinde — cevap tahminle değil geçmişle verilir.

## Denetim ileriye değil, geriye bakar
- `analitik-okuma-ve-raporlama` = sürekli ölçüm (veri kaynağı).
- **Bu skill** = periyodik geriye dönük triyaj.
- Strateji = ileriye dönük plan. Denetim onu **besler**, yerine geçmez.

## Çerçeve: DENET
- **D — Dökümü çıkar.** Son ~90 günün yayınlanan içeriği: video, X article, Instagram paketi, blog/site
  sayfası. Her satırda: tarih, format, konu, sayılar (kaynaklı).
- **E — Esas sinyali bul.** Beğeni değil: **izlenme süresi/tutma**, **yorum**, **abone dönüşümü**,
  **kaynağa dönüş**. En iyi 3 ve en kötü 3; format/konu/saate göre desen.
- **N — Ne eksik.** Konu başlığı (pillar) boşlukları: kanalın iddia ettiği alanların hangisinde
  90 gündür içerik yok? Ton kayması **iki yönde** kontrol edilir — kanal kendinden uzaklaşmış olabilir,
  ya da en iyi işleri tonun **evrilmesi gerektiğini** söylüyor olabilir.
- **E — Emanet sözler.** Videolarda ve yazılarda verilen sözler tutuldu mu?
  ("repo açıklamada", "bunu bir sonraki bölümde anlatacağım", "kupon kodu şurada").
  Tutulmayan söz **borçtur**; rapora ayrı bölüm olarak yazılır, kararı patron verir.
- **T — Triyaj ve yol haritası.** Her kalem için **tut / bırak / tazele**.
  **Önce tazele, sonra bırak.** Silme kararı **her zaman** patronundur — ajan hiçbir şeyi silmez, kaldırmaz.
  Çıktı: hızlı kazanımlar ve uzun vadeliler ayrı, her birinde sahip ve tarih.

## Adımlar
1. Dönemi sabitle (varsayılan son 90 gün) ve envanteri çıkar — kaynak: `takimlar/youtube-analiz/veri/*.json`
   ve önceki `takimlar/youtube-analiz/cikti/*-rapor.md` dosyaları (salt okunur).
2. Sinyal sütunlarını doldur; **veride olmayan sayı boş bırakılır**, uydurulmaz.
3. En iyi 3 / en kötü 3 ve desen notu.
4. Konu başlığı boşlukları + ton kayması (iki yönde).
5. Emanet sözler taraması → tutulmayanlar listesi.
6. Kalem kalem triyaj: tut / bırak / tazele + tek cümle gerekçe.
7. Yol haritası: hızlı kazanım (bu hafta) vs uzun vadeli (bu çeyrek).
8. Çıktı `takimlar/youtube-analiz/cikti/<tarih>-denetim.md`; silme/kaldırma önerileri kuyruğa
   `{"id": "denetim-<konu>", "durum": "bekliyor", "not": "patron karar verecek"}`.

## Çıktı şablonu

```
# İçerik denetimi — <dönem>

## Envanter
| Tarih | Format | Konu | Sinyal | Kaynak |
|---|---|---|---|---|

## En iyi 3 / en kötü 3
...desen notu: ...

## Konu başlığı boşlukları
| Başlık | Son içerik | Boşluk |
|---|---|---|

## Ton kayması
- Uzaklaşma: ...
- Evrilme sinyali: ...

## Emanet sözler
| Söz | Nerede verildi | Durum | Sonraki adım |
|---|---|---|---|

## Triyaj
| Kalem | Karar | Gerekçe |
|---|---|---|
| ... | tazele | ... |

## Yol haritası
### Hızlı kazanım (bu hafta)
### Uzun vadeli (bu çeyrek)
```

## Kalite kontrol listesi
- [ ] Dönem ve envanter kaynakları yazılı mı?
- [ ] Sinyal beğeni değil, tutma/yorum/dönüşüm mü?
- [ ] **Düşük beğeni tek başına "bırak" gerekçesi olarak kullanılmadı mı?**
- [ ] Ton kayması iki yönde de değerlendirildi mi?
- [ ] Emanet sözler taraması yapıldı mı?
- [ ] Her kararın tek cümle gerekçesi var mı?
- [ ] Silme/kaldırma önerileri kuyruğa "patron karar verecek" olarak mı düştü?
- [ ] Yol haritası hızlı/uzun diye ayrıldı mı, sahip ve tarih var mı?

## Yasaklar (ANAYASA)
- **Hiçbir şeyi silmek, kaldırmak, gizlemek, yeniden adlandırmak** — yayındaki içerikte asla,
  yayındakilerde karar patronun (§1).
- Sayı uydurmak ya da eksik sayıyı doldurmak (§2).
- Veri inceyse performans hükmü vermek. İnce veride yalnızca **yapısal denetim** yapılır
  (konu başlıkları, ton, düzen) ve "90 günde tekrar bakılacak" yazılır.
- Denetimi stratejiye çevirmek. Denetim geçmişi okur; planı patron yazar.

## Öğrenilenler
Bu skill koşuda aldığı veriyle **kendini geliştirir**: hangi denetim sütunu karar ürettti, hangisi her
seferinde boş kaldı — `defter.md`'ye tek ders yaz ve bir sonraki denetimde tabloyu sadeleştir.
Üç koşuda tekrarlanan ders için koşu kaydına "yetenek önerisi: `icerik-denetimi` → ## Öğrenilenler" satırı düş.

- (henüz ders yok)

## Kaynak ve değişiklikler
**Alındığı yer:** `social-media-skills/skills` → `content-audit`, MIT.

**Orijinalden alınanlar:** "yoğunluk ilerleme değildir" duruşu; denetimin **geriye dönük**, stratejinin
ileriye dönük olduğu ayrımı; AUDIT çerçevesinin iskeleti (envanter → sinyal → konu başlığı/ton/profil
teşhisi → tut/bırak/tazele → yol haritası); ~90 günlük pencere, aylık hafif / üç aylık derin ritim;
**sinyal ≠ vanity** ve **"düşük beğeni bırakma gerekçesi değildir"** kuralı; **ton kaymasının iki yönde**
okunması; **önce tazele, sonra bırak** ve **silme kararını insan verir, otomatik silme yok**; ince veride
yalnızca yapısal denetim; hızlı kazanım / uzun vadeli ayrımı ve "elektronik tabloda mezarlık yaratma".

**Değiştirilenler:**
- "Profil optimizasyonu" ve platform-başına biyografi/kapak denetimi çıkarıldı; yerine **emanet sözler
  taraması** eklendi (orijinalde yok) — kanalın gerçek borcu videolarda verilen ve unutulan sözlerdir.
- Envanter kaynakları takımın kendi dosyalarına bağlandı (`veri/*.json`, önceki `cikti/*-rapor.md`) —
  hepsi salt okunur.
- Silme/arşivleme maddesi sertleştirildi: orijinal "insan onaylar" diyor, bizde **ajan hiçbir şeyi
  silmez**, öneri kuyruğa düşer (§1).
- WoopSocial / content-recycling gibi dış bağlantılar çıkarıldı; çıktı koşu kaydı ve `defter.md`
  takımlarının okuyacağı dosyaya bağlandı (§5).
- Sayı disiplini `analitik-okuma-ve-raporlama` ile aynı kurala bağlandı: veride yoksa boş kalır.
