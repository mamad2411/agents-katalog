---
name: sky-forms
description: >-
  Form mimarisi: doğrulama, hata mesajı, çok adımlı form; TCKN ve IBAN doğrulama, Türkçe adres
  alanları. Kayıt, iletişim, ödeme veya randevu formu yazarken kullan.
---

# Sky · Formlar

## Mimari

- **Tek şema, iki taraf:** Zod şeması `schemas/` altında; istemci ve sunucu aynı şemayı kullanır.
- Sunucu doğrulaması **zorunlu**, istemci doğrulaması UX içindir.
- Next.js: Server Action + `useActionState` (ilerlemeli geliştirme — JS'siz de çalışır).
- SPA: React Hook Form + `zodResolver` + mutasyon (TanStack Query).

```ts
// schemas/appointment.ts
export const AppointmentSchema = z.object({
  name: z.string().trim().min(2, "Adınızı girin"),
  phone: z.string().regex(/^(\+90|0)?5\d{9}$/, "Geçerli bir cep telefonu girin"),
  date: z.coerce.date().min(new Date(), "Geçmiş bir tarih seçilemez"),
});
```

```tsx
const form = useForm<z.infer<typeof AppointmentSchema>>({
  resolver: zodResolver(AppointmentSchema),
  mode: "onTouched", // ilk blur'dan sonra canlı doğrula
});
```

## Doğrulama zamanlaması

- Kullanıcı yazarken hata gösterme; **ilk blur'dan sonra** doğrula, sonra değiştikçe güncelle.
- Hatalı alan düzeltildiği anda hatayı kaldır.
- Gönderimde tüm hataları göster, odağı ilk hatalı alana taşı.
- Sunucu hatalarını (ör. "bu e-posta kayıtlı") ilgili alana `setError` ile bağla.

## Hata mesajı yazımı

- Ne yanlış + nasıl düzeltilir: "Şifre en az 8 karakter olmalı" (✓), "Geçersiz giriş" (✗).
- Kullanıcıyı suçlama; teknik terim yok.
- Alanın hemen altında, `--danger` renk + ikon, `aria-describedby` ile bağlı.

## Düzen

- Tek sütun (karşılaştırma gerektirmeyen kısa ikili alanlar hariç: ad/soyad, şehir/posta kodu).
- Etiket alanın **üstünde**; placeholder yalnızca örnek biçim için.
- Zorunlu/isteğe bağlı: çoğunluk zorunluysa isteğe bağlıları "(isteğe bağlı)" ile işaretle.
- Alan genişliği beklenen girdi uzunluğunu ima etsin (posta kodu kısa).
- Doğru `type` ve `inputMode`: `email`, `tel`, `inputMode="numeric"`, `autocomplete`.
- Birincil buton net fiil: "Randevu oluştur" ("Gönder" değil). Tek birincil eylem.

## Gönderim durumları

| Durum | Davranış |
|---|---|
| Gönderiliyor | Buton devre dışı + spinner, metin sabit genişlik; çift gönderim engelli |
| Başarılı | Net onay (toast veya başarı ekranı), sonraki adım; formu sıfırla veya yönlendir |
| Hata (ağ/sunucu) | Girilen veriyi **kaybetme**; tekrar dene seçeneği |
| Optimistic | Liste/sayaç gibi geri alınabilir işlemlerde `useOptimistic`; hata olursa geri al |

## Çok adımlı formlar

- İlerleme göstergesi ("Adım 2/4" + başlıklar).
- Her adım kendi şemasıyla doğrulanır; tüm veri tek state'te (`useForm` tek örnek veya Zustand).
- Geri gitmek veriyi silmez; sayfa yenilemeye karşı taslak `sessionStorage`'a (hassas veri hariç).
- Son adımda özet + düzenle bağlantıları.

## Dosya yükleme

- Kabul edilen türler ve boyut sınırı alanın yanında yazılı; istemcide ön kontrol, sunucuda kesin kontrol.
- Sürükle-bırak + klasik seçim butonu (erişilebilirlik).
- Büyük dosyalarda doğrudan depolamaya imzalı URL (presigned) ve ilerleme çubuğu.
- Görsel ön izleme; kaldır butonu.

## Güvenlik

- Bot koruması: honeypot alanı + rate limit; gerekirse Turnstile/hCaptcha.
- Parola alanında göster/gizle butonu; `autocomplete="new-password"`.
- KVKK: kişisel veri toplanıyorsa açık rıza metni ve aydınlatma bağlantısı.
