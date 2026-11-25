---
name: sky-ux-heuristics
description: >-
  UX değerlendirme bilgisi ve sezgisel denetim: Nielsen'in 10 sezgisi, Fitts ve Hick yasaları,
  bilişsel yük ve Miller, Jakob yasası (tanıdıklık), Gestalt ilkeleri, F/Z tarama kalıpları,
  ilerleme ve geri bildirim süreleri (0.1/1/10 sn), hata önleme, varsayılanların gücü,
  progressive disclosure ve 30 dakikalık sezgisel denetim şablonu. "UX'i değerlendir",
  "kullanımı zor", "kullanıcı deneyimi nasıl", "neden kafa karıştırıyor" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · UX Sezgileri

## Nielsen'in 10 sezgisi (soru biçiminde)

1. **Sistem durumunun görünürlüğü** — Kullanıcı her an ne olduğunu biliyor mu? (yükleniyor, kaydedildi, gönderildi)
2. **Gerçek dünyayla eşleşme** — Kullanıcının dili mi, sistemin dili mi? ("Rezervasyon" mu "booking entity" mi)
3. **Kullanıcı kontrolü ve özgürlüğü** — Geri al, iptal, vazgeç var mı? Çıkış yolu açık mı?
4. **Tutarlılık ve standartlar** — Aynı şey her yerde aynı adla, aynı yerde mi? Platform alışkanlıklarına uyuyor mu?
5. **Hata önleme** — Hata yapmak zor mu? (onay, kısıt, akıllı varsayılan, devre dışı geçersiz seçenekler)
6. **Hatırlamak yerine tanımak** — Seçenekler görünür mü, yoksa ezber mi gerekiyor?
7. **Esneklik ve verimlilik** — Uzmanlar için kısayollar (⌘K, klavye, toplu işlem) var mı?
8. **Estetik ve minimal tasarım** — Her öğe yerini hak ediyor mu? Gereksiz bilgi önemli olanı boğuyor mu?
9. **Hataları tanıma, teşhis, kurtarma** — Hata mesajı ne olduğunu ve nasıl düzeleceğini söylüyor mu?
10. **Yardım ve dokümantasyon** — Gerektiğinde bağlamsal yardım var mı?

## Yasalar ve ilkeler

- **Fitts**: hedefe ulaşma süresi mesafe/büyüklükle artar → önemli butonlar büyük ve yakın; ekran kenarları "sonsuz büyük" hedeflerdir.
- **Hick**: seçenek sayısı arttıkça karar süresi artar → seçenekleri azalt, grupla, önerilen seçeneği vurgula.
- **Miller / bilişsel yük**: kısa süreli bellek sınırlı → bilgiyi parçala (telefon numarası gruplama, adımlı formlar).
- **Jakob**: kullanıcılar zamanlarının çoğunu başka sitelerde geçirir → alışılmış kalıpları kullan (logo sol üstte, sepet sağ üstte).
- **Gestalt**: yakınlık (ilişkili öğeler yakın), benzerlik (aynı işlev aynı görünüm), ortak bölge (kart), süreklilik, şekil-zemin.
- **Doherty eşiği**: < 400ms yanıt akıcılık hissi verir.
- **Peak-end**: deneyim en yoğun an ve son anla hatırlanır → başarı ekranları ve kutlamalar önemlidir.
- **Von Restorff**: farklı olan hatırlanır → birincil CTA tek ve belirgin.
- **Tesler**: karmaşıklık yok olmaz, taşınır → karmaşıklığı kullanıcıdan sisteme taşı (akıllı varsayılanlar).

## Yanıt süreleri

| Süre | Algı | Yapılacak |
|---|---|---|
| < 100ms | anlık | geri bildirim gerekmez |
| 100ms–1sn | akış bozulmaz | hafif gösterge (buton durumu) |
| 1–10 sn | dikkat dağılır | ilerleme/adım metni |
| > 10 sn | kullanıcı başka şeye geçer | arka plan işi + bildirim |

## Tarama kalıpları

- **F kalıbı** (metin ağırlıklı): başlıklar ve ilk kelimeler okunur → ilk 2 kelime anlam taşısın, alt başlıklar sık.
- **Z kalıbı** (az metinli sayfalar, landing): logo → menü → çapraz → CTA.
- Katman pastası: tarayan kullanıcı için kalın başlık + kısa paragraf.

## Varsayılanlar ve kademeli ifşa

- Kullanıcıların çoğu varsayılanı değiştirmez → varsayılanı en iyi seçenek yap (en sık kullanılan, en güvenli).
- Gelişmiş seçenekleri "Gelişmiş ayarlar" altında sakla; temel akış sade kalsın.

## 30 dakikalık sezgisel denetim

1. Kritik 3 kullanıcı görevini yaz ("ilk randevuyu oluştur", "müşteriyi bul ve not ekle", "faturayı indir").
2. Her görevi baştan sona yap; her adımda 10 sezgiyi sor.
3. Bulguları kaydet: `[ciddiyet 1–4] ekran — sorun — hangi sezgi — öneri`.
4. Ciddiyet: 4 = görev tamamlanamıyor, 3 = büyük sürtünme, 2 = küçük sürtünme, 1 = kozmetik.
5. İlk 5 bulguyu (ciddiyet × sıklık) düzeltme listesine koy.
Bulgular için `sky-ui-reviewer` yöntemi da kullanılabilir; gerçek kullanıcı testi (5 kişi, sesli düşünme) her zaman daha değerli.
