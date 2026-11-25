---
name: sky-refactor
description: >-
  Güvenli yeniden düzenleme (refactor): önce karakterizasyon testleri, küçük adımlar ve her
  adımda yeşil testler, büyük dosya/bileşen bölme, tekrar eden kodu birleştirme (ama erken
  soyutlamadan kaçınma), ölü kod temizliği (knip), adlandırma iyileştirme, strangler fig ile
  kademeli yeniden yazım, codemod (jscodeshift/ts-morph) ile toplu değişiklik ve refactor PR'ı
  yazımı. "Kod karışık", "bu dosya çok büyük", "temizle", "yeniden düzenle" dendiğinde kullan.
disable-model-invocation: true
---

# Sky · Refactor

Refactor = **davranışı değiştirmeden** yapıyı iyileştirmek. Davranış değişikliği ile refactor aynı commit'te olmaz.

## 0. Güvenlik ağı

- Dokunacağın kodun testi yoksa önce **karakterizasyon testi** yaz: mevcut davranışı (hatalarıyla birlikte) kilitleyen testler.
  Girdi → mevcut çıktı snapshot'ı, kritik akışlar için E2E (bkz. `sky-testing`).
- `typecheck`, `lint`, `test` yeşil başla. Kırmızıyla başlanan refactor bitmez.

## 1. Küçük adımlar

Her adım: tek tür değişiklik → testler → commit. Örnek sıra:
1. Yeniden adlandır (anlamlı isimler) → 2. Fonksiyon çıkar → 3. Dosyaya taşı → 4. Tekrarı birleştir → 5. Tipleri sıkılaştır → 6. Ölü kodu sil.
Bir şey bozulursa son commit'e dön; hangi adımın bozduğu belli.

## 2. Büyük bileşen bölme (React)

- 300+ satırlık bileşen: veri çekme (hook/server), durum mantığı (reducer/hook), sunum (alt bileşenler) olarak ayır.
- Önce sunumsal parçaları çıkar (en güvenli), sonra mantığı custom hook'a.
- Prop sayısı patlarsa composition (`children`, slot) (bkz. `sky-design-system`).
- Bölmeden sonra re-render davranışını kontrol et (Profiler).

## 3. Tekrar ve soyutlama

- **Üç kuralı**: aynı şey üçüncü kez yazılınca soyutla; ikinci kezde değil.
- Yanlış soyutlama tekrardan pahalıdır — "neredeyse aynı" iki kodu 6 parametreli tek fonksiyona sıkıştırma. Geri açmak da bir refactor'dur.
- Benzer görünen ama farklı nedenlerle değişen kod (farklı iş kuralları) ayrı kalsın.

## 4. Ölü kod

- `knip` (kullanılmayan dosya, export, bağımlılık), `ts-prune`, `depcheck`.
- Feature flag'i %100 olmuş eski dallar (bkz. `sky-feature-flags`), yorum satırına alınmış kod blokları, kullanılmayan CSS.
- Silmeden önce dinamik kullanım (string ile import, reflection) kontrolü.

## 5. Toplu değişiklik: codemod

Yüzlerce dosyada aynı dönüşüm (prop adı değişikliği, import yolu, API göçü) → elle değil:
- **ts-morph** (TS AST, tip bilgili) veya **jscodeshift**; regex yalnızca gerçekten basit durumlarda.
- Önce 3 dosyada dene, diff'i incele, sonra hepsine uygula; codemod'u repoda sakla (`scripts/codemods/`).

## 6. Strangler fig (büyük yeniden yazım)

"Her şeyi baştan yazalım" yerine: yeni modülü eskisinin yanına kur, trafiği/çağrıları parça parça yeniye yönlendir
(feature flag veya route bazlı), eski parçayı en son sil. Her an çalışan bir sistem olur.

## 7. Ne zaman durmalı

Refactor bir hedefe hizmet eder (yeni özelliği kolaylaştırmak, hatayı önlemek, performans). "Daha güzel olsun" diye
sonsuz devam etme; kapsamı baştan yaz ve orada dur.

## PR

Başlık: `refactor: …`; açıklama: neden, ne değişti, **davranış değişmedi** kanıtı (testler, ekran görüntüsü karşılaştırması),
gözden geçirme ipucu ("dosya taşımaları ayrı commit'te, mantık değişikliği yok"). Taşıma + değişikliği aynı commit'e koyma (diff okunmaz).
