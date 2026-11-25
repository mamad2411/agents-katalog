---
name: ajanla-video-kurgu
description: "Claude Code, Codex ya da başka bir kodlama ajanıyla slop çıkarmayan video kurgu hattı: ses ve Whisper transkripti, boşluk/tekrar kesimi, pano haritası, tek şef altında paralel ajanlar, dosya sözleşmesi ve teslim formu, kapılar (aynı hata iki kez olursa koda yaz), marka kilidi, dört parçalı prompt, görsel/video üretim maliyeti, render kuyruğu, kısa form kesit ve dikey motion. Tetikleyiciler: 'videomu editle', 'motion video yap', 'sesten video', 'HyperFrames ile kurgu', 'ajanla kurgu', 'paralel ajanla edit', 'Reels/TikTok kesiti çıkar', 'slop olmasın', 'video atölyemi kur', 'edit my video with agents', 'AI video editing pipeline'."
---

# Ajanla video kurgu: atölye düzeni

Bu skill bir kurgu programı değil, bir **düzen**. Videoyu güzelleştiren şey ajan sayısı değil,
ajanların etrafına kurulan düzen: kim neyi yapar, iş nerede kontrol edilir, hata bir daha nasıl olmaz.
Kaynak: Avenox'un videosu. Transkript ve bölüm notları skill'le gelmez; reponun `notlar/` klasöründe: https://github.com/avenoxai/avenox-video-kurgu-notlari

Videodaki kendi hattının birebir kopyası değil, arkasındaki mantık. Kopyalanan düzen herkesi
aynı videoya götürür, slop da tam olarak budur. Bu yüzden ilk iş, düzeni kullanıcının markasına ve
imkanlarına göre kurmak.

## Ajan için ilk adım: atölyeyi kullanıcıya göre kur

Kurguya başlamadan kullanıcıdan şunları öğren (eksikse sor, tahmin etme):

1. **Malzeme türü:** yalnız ses mi, ekran kaydı + ses mi, yoksa biten uzun videodan kısa form mu? (Üç hat, bkz. `references/01-atolye.md`.) Kamera çekiminde ekran kaydı hattını kullan: kesime dokunma, üstüne bindir.
2. **Marka:** maskot ya da karakter, renkler (hex kodlarıyla), zemin, yazı tipi, yasaklar. Yoksa önce marka dosyasını birlikte oluştur (`references/05-marka-kilidi.md`). Marka dosyası olmadan çıkan iş ortalamaya kayar.
3. **Araçlar:** transkript (Whisper yerelde mi, API mi), kodla video aracı (ör. HyperFrames), görsel/video üretim eklentisi var mı, ses efekti ve müzik kaynağı.
4. **Bütçe ve hız:** limit bol mu, acele mi? Detay seviyesi buna göre ayarlanır: limit bolsa hareket ve özel görsel artar, acele varsa azalır.
5. **Son söz kimde:** kullanıcı. Taslağı o izler, beğenmediğini söyler; sen tarihiyle not alırsın.

Cevapları proje kökünde `atolye/atolye.md`, marka kararlarını `atolye/marka.md` dosyasına yaz (şablon: `templates/marka.md`). Sonraki her oturum oradan başlar: ajanlar her oturuma sıfırdan başlar,
kalıcı kararlar dosyada durmazsa her seferinde ortalama iş çıkar.

## Atölyenin özeti

Kayıt bir uçtan girer, istasyonlardan geçer, öbür uçtan yayına hazır video çıkar. Neredeyse her
istasyonda bir ajan çalışır, her istasyonun çıkışında bir **kapı** bekler: bir ajan işi yapar,
başka bir kontrol (ajan ya da kod) geçmeden iş bir sonraki istasyona gitmez.

1. Kayıt ve ses: az işle, yayın seviyesine çek (`references/06-ses-transkript.md`)
2. Transkript: modeller sesi duyamaz, metin şart; temizlik ajanı adları düzeltir
3. Kesim: boşluklar ve tekrarlar; kesimden sonra kesime dokunulmaz
4. Pano haritası: her pasaj için "sadece dinleyen anlar mı?" (`references/02-pano-haritasi.md`)
5. Bölüm brief'leri: tek şef yazar, dosya sözleşmesi (`references/03-orkestrasyon.md`)
6. Görsel ve video üretimi: brief'teki ihtiyaç; görsel ucuz, video pahalı; etiketli kütüphane (`references/07-uretim.md`)
7. Paralel kurulum: alt ajanlar kendi bölümünü kurar, teslim formunu yazar
8. Render ve yayın: render tek sırada; altyazı, kapak, kısa form, dikey motion (`references/08-kisa-form.md`)

## Değişmez kurallar

- **Tek şef.** Kullanıcı tek bir ana ajanla konuşur. Ortak dosyaları (plan, kesim listesi, pano haritası, bölüm brief'leri) ortak klasöre yalnız ana ajan koyar; istasyon ajanlarının çıktısını kontrol ettikten sonra. Alt ajanlar yalnız kendi bölümünü kurar.
- **Dosya sözleşmesi.** Ajanlar birbiriyle konuşmaz, dosyadan okur: transkript, kesim listesi, pano haritası, bölüm brief'i, teslim formu.
- **Dosyaya yazılmadıysa bitmedi.** Alt ajan işini teslim formuna yazmadıysa iş bitmemiş sayılır. "Bitti" demesi yetmez.
- **Aynı hata iki kez olduysa nota değil koda yaz.** Kural kapı olur; kod geçmezse video çıkmaz (`references/04-kapilar.md`).
- **Bilinen arızaların kapısını ilk günden kur.** Ses-görüntü senkronu, teslim formu kontrolü, render kuyruğu (`references/09-pahali-dersler.md` arıza kataloğu). Yaşanmış sorunları ajana anlatırsan sen yaşamadan çözer. Yeni her hatayı `atolye/hatalar.md`'ye tarihiyle yaz; yazmadan önce orada ara, ikinci kayıt kapı açar.
- **Çıtayı yaz, tarifi ajana bırak.** Alt ajana üç şey ver: değişmeyecek kararlar, kalite çıtası, bilerek boş bırakılan kısımlar. Fazla ayrıntı kaliteyi düşürür.
- **Sayı verebiliyorsan sayı ver.** "Biraz yavaş" yerine "10 saniyede ortalama 10-10,5 hareket". "Doğru göz rengi" yerine hex kodu.
- **Neyi istemediğini net yaz.** "Daha iyi yap" bir şey ifade etmez; yasak listesi uygulanır.
- **Render tek sırada.** Kod paralel yazılır, render sırayla alınır; yoksa ajanlar birbirini patlatır.
- **Son söz kullanıcının.** Ne transkripte ne ajan raporuna körü körüne güven. Kullanıcı izler, beğenmediğini söyler, sen tarihiyle yazarsın (`templates/begenmeme-defteri.md`).

## Prompt: dört parça

Kısa ya da uzun fark etmez. İyi bir görevde dört parça olur (`references/03-orkestrasyon.md` > Prompt sözleşmesi):

1. **Hedef:** tam olarak ne istendiği
2. **Kısıt:** neyin asla olmayacağı
3. **Kalite çıtası:** neye "iyi" denecek, ölçülebilir
4. **Örnek:** referans görsel ya da beğenilen eski bir iş

Araya bir **kontrol noktası** koy: ör. storyboard'u önce göster, onay gelmeden üretime geçme.
Kullanıcı tek satır yazsa bile ana ajanın işi bunu alt ajanlar için ölçülebilir bir sözleşmeye çevirmektir.

## Referanslar

| Dosya | Ne zaman oku |
|---|---|
| `references/01-atolye.md` | Hattı kurarken: üç malzeme türü, istasyonlar, her istasyonun girdisi, çıktısı ve kapısı |
| `references/02-pano-haritasi.md` | Kesimden sonra, grafiğe geçmeden önce |
| `references/03-orkestrasyon.md` | Paralel ajan açmadan önce: tek şef, dosyalar, brief, teslim formu, render kuyruğu, prompt sözleşmesi |
| `references/04-kapilar.md` | Bir hata ikinci kez olduğunda; örnek kapılar |
| `references/05-marka-kilidi.md` | Marka yoksa ya da karakter/görsel bozuluyorsa |
| `references/06-ses-transkript.md` | Kayıttan sonra: ses zinciri, Whisper, temizlik, kesim |
| `references/07-uretim.md` | Özel görsel ve video üretirken: maliyet, taslak, kütüphane, model kıyası |
| `references/08-kisa-form.md` | Instagram, TikTok, Reels, dikey motion |
| `references/09-pahali-dersler.md` | Başlamadan bir kez: pahalıya patlayan beş ders ve arıza kataloğu |
| `references/10-baslangic-kiti.md` | Kurulum: araçlar ve linkler |
| `templates/` | Marka dosyası, pano haritası, bölüm brief'i, teslim formu, prompt sözleşmesi, beğenmeme defteri şablonları |
