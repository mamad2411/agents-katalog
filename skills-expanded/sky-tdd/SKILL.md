---
name: sky-tdd
description: >-
  Test güdümlü geliştirme (TDD) iş akışı: kırmızı → yeşil → yeniden düzenle döngüsü, önce
  hangi testin yazılacağı (test listesi), en küçük adımlar, hata düzeltmede önce başarısız
  test, dıştan içe (outside-in) ve içten dışa yaklaşımlar, sahte nesne ölçüsü, TDD'nin işe
  yaradığı ve yaramadığı yerler, AI ile TDD (önce testi yazdırıp onaylatmak). "TDD ile yap",
  "önce test yaz", "test-first" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · TDD

Test araçları ve kalıpları `sky-testing`'de; burada **iş akışı**.

## Döngü

```
1. TEST LİSTESİ  → davranışları madde madde yaz (kod değil)
2. KIRMIZI       → listeden en basit maddeyi test olarak yaz, çalıştır, **doğru sebeple** başarısız olduğunu gör
3. YEŞİL         → testi geçiren en basit kodu yaz (zarafet değil, geçmek)
4. REFACTOR      → testler yeşilken tekrarı/isimleri/yapıyı düzelt
5. Listeye dön   → yeni fark ettiğin durumları listeye ekle
```
Kırmızıyı görmeden yeşile geçme: hiç başarısız olmayan test hiçbir şeyi test etmiyor olabilir.

## Örnek: slot hesaplama

Test listesi:
- [ ] çalışma saati 09–12, 30 dk hizmet → 6 slot
- [ ] mevcut randevu 10:00–10:30 → o slot yok
- [ ] tampon 10 dk → randevu sonrası 10 dk boş
- [ ] mola 12–13 → slot molaya taşmaz
- [ ] geçmiş saatler listelenmez
- [ ] hizmet süresi kalan boşluğa sığmıyorsa slot yok
- [ ] Türkiye saat diliminde gün sınırı doğru

```ts
test("09–12 arası 30 dk hizmet 6 slot üretir", () => {
  const slots = generateSlots({ hours: [{ start: "09:00", end: "12:00" }], durationMin: 30, bookings: [], date: "2026-12-01" });
  expect(slots.map((s) => s.start)).toEqual(["09:00", "09:30", "10:00", "10:30", "11:00", "11:30"]);
});
```
Önce bunu geçir (belki sabit kodla bile), sonra ikinci test "sabit kodu" kırar ve gerçek algoritmayı zorlar.

## Hata düzeltme = TDD'nin en kolay kazancı

1. Hatayı yeniden üreten testi yaz → kırmızı (hata kanıtlandı).
2. Düzelt → yeşil. 3. Test kalıcı olarak regresyonu önler.
Bkz. `sky-debug`.

## Yaklaşımlar

- **Dıştan içe**: önce kabul/E2E veya uç nokta testi (kullanıcı davranışı), sonra içeri doğru birim testleri — gereksiz kod yazmazsın.
- **İçten dışa**: saf iş mantığı (hesaplama, durum makinesi) ile başla — algoritma ağırlıklı işlerde doğal.
- Sahte nesneleri (mock) yalnızca sınırlarda kullan (ağ, saat, rastgelelik, ödeme); iç sınıfları mock'lamak testleri kırılgan yapar.

## Nerede parlar, nerede zorlar

✓ İş kuralları, hesaplamalar, ayrıştırıcılar, durum makineleri, hata düzeltmeleri, API sözleşmeleri.
~ UI: davranış testleri (Testing Library) TDD'ye uygun; görsel tasarım değil — onu tarayıcıda doğrula.
✗ Keşif/prototip (ne yapacağını bilmiyorsan önce dene, sonra testle sabitle), üçüncü parti entegrasyonun ilk denemesi.

## AI ile TDD

1. Davranış listesini birlikte yaz → kullanıcı onayı.
2. Önce **yalnızca testleri** yaz ve çalıştır (kırmızı), testleri kullanıcıya göster.
3. Sonra uygulama; testleri değiştirerek geçirme yasak (test yanlışsa ayrı ve açık değişiklik).
4. Refactor + kapsam kontrolü.
Bu, "kod çalışıyor ama yanlış şeyi yapıyor" riskini ciddi azaltır. Komut: `/sky-tdd`.
